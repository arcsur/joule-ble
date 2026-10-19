"""Bluetooth Low Energy client for Joule sous vide devices."""

from __future__ import annotations

import asyncio
import logging
import random
import time
from collections.abc import Callable
from typing import Any, cast

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection
from google.protobuf.message import DecodeError

from .const import (
    CHEFSTEPS_KEEPALIVE_INTERVAL,
    DEFAULT_ATT_PAYLOAD_SIZE,
    DEFAULT_COMMAND_TIMEOUT,
    DEFAULT_CONNECT_TIMEOUT,
    DEFAULT_PAIR_TIMEOUT,
    DEFAULT_RECIPIENT_ADDRESS,
    DEFAULT_SENDER_ADDRESS,
    DEFAULT_STREAM_HANDLE,
    MAX_TEMP_C,
    MIN_TEMP_C,
    UUID_BREVILLE_APP_MESSAGE,
    UUID_BREVILLE_APPLIANCE_MESSAGE,
    UUID_BREVILLE_SERIAL_NUMBER,
    UUID_BREVILLE_SERVICE,
    UUID_CHEFSTEP_STREAM_READ,
    UUID_CHEFSTEP_STREAM_SERVICE,
    UUID_CHEFSTEP_STREAM_SUBSCRIBE,
    UUID_CHEFSTEP_STREAM_WRITE,
    UUID_DEVICE_VERSION,
)
from .exceptions import (
    JouleAuthenticationError,
    JouleCommandError,
    JouleConnectionError,
    JouleTimeoutError,
)
from .models import (
    CookState,
    ErrorState,
    JouleAuthData,
    JouleDeviceInfo,
    JouleModel,
    JouleState,
)
from .proto import joule_pb2

_LOGGER = logging.getLogger(__name__)


class JouleClient:
    """Asynchronous client for Joule sous vide devices over BLE."""

    def __init__(
        self,
        ble_device: BLEDevice,
        auth_data: JouleAuthData | None = None,
        model: JouleModel = JouleModel.UNKNOWN,
        recipient_address: bytes | None = None,
    ) -> None:
        """Initialize the Joule client."""
        self._ble_device = ble_device
        self._auth_data = auth_data or JouleAuthData()
        self._model = model

        self._client: BleakClient | None = None
        self._write_char: BleakGATTCharacteristic | None = None
        self._notify_char: BleakGATTCharacteristic | None = None
        self._read_char: BleakGATTCharacteristic | None = None
        self._is_breville_profile: bool = False

        norm_recipient: bytes = DEFAULT_RECIPIENT_ADDRESS
        if recipient_address:
            if isinstance(recipient_address, str):
                try:
                    norm_recipient = bytes.fromhex(
                        recipient_address.replace(":", "").replace("-", "")
                    )
                except ValueError:
                    norm_recipient = recipient_address.encode("utf-8")
            elif isinstance(recipient_address, (bytes, bytearray)):
                norm_recipient = bytes(recipient_address)

        self._device_info: JouleDeviceInfo = JouleDeviceInfo(
            name=ble_device.name or "Joule",
            model=model,
            mac_address=ble_device.address,
            recipient_address=norm_recipient,
        )
        self._state: JouleState = JouleState()
        self._callbacks: list[Callable[[JouleState], None]] = []

        self._write_lock = asyncio.Lock()
        self._stream_lock = asyncio.Lock()
        self._read_lock = asyncio.Lock()
        self._response_futures: dict[str, asyncio.Future[joule_pb2.StreamMessage]] = {}
        self._rx_buffer = bytearray()
        self._max_payload_size = DEFAULT_ATT_PAYLOAD_SIZE
        self._stream_handle: int = DEFAULT_STREAM_HANDLE
        self._sender_address: bytes = DEFAULT_SENDER_ADDRESS
        self._recipient_address: bytes = norm_recipient
        self._keepalive_task: asyncio.Task[None] | None = None
        self._latest_feed_id: int = 0
        self._latest_seq_num: int = 0
        self._feed_ready_event: asyncio.Event = asyncio.Event()

    @property
    def latest_feed_id(self) -> int:
        """Return the latest feedId from live telemetry."""
        return self._latest_feed_id

    @property
    def latest_seq_num(self) -> int:
        """Return the latest sequenceNumber from live telemetry."""
        return self._latest_seq_num

    @property
    def is_connected(self) -> bool:
        """Return True if currently connected via BLE."""
        return bool(self._client and self._client.is_connected)

    @property
    def device_info(self) -> JouleDeviceInfo:
        """Return cached device information."""
        return self._device_info

    @property
    def state(self) -> JouleState:
        """Return current live telemetry state."""
        return self._state

    @property
    def is_breville_profile(self) -> bool:
        """Return True if connected via Breville GATT profile."""
        return self._is_breville_profile

    @property
    def is_chefsteps_profile(self) -> bool:
        """Return True if connected via ChefSteps GATT profile."""
        return not self._is_breville_profile

    def register_callback(
        self, callback: Callable[[JouleState], None]
    ) -> Callable[[], None]:
        """Register a callback for state changes. Returns an unsubscribe function."""
        self._callbacks.append(callback)

        def unsubscribe() -> None:
            if callback in self._callbacks:
                self._callbacks.remove(callback)

        return unsubscribe

    def _notify_listeners(self) -> None:
        """Dispatch current state to all registered listeners."""
        for cb in list(self._callbacks):
            try:
                cb(self._state)
            except Exception as err:
                _LOGGER.exception("Error executing Joule state callback: %s", err)

    async def connect(
        self,
        timeout: float = DEFAULT_CONNECT_TIMEOUT,
        auto_start_feed: bool = True,
    ) -> None:
        """Connect to the Joule via BLE."""
        if self.is_connected:
            return

        _LOGGER.debug("Connecting to Joule (%s)", self._ble_device.address)
        try:
            self._client = await establish_connection(
                BleakClient,
                self._ble_device,
                self._ble_device.name or "Joule",
                disconnected_callback=self._handle_disconnect,
                timeout=timeout,
            )
        except (BleakError, TimeoutError) as err:
            raise JouleConnectionError(
                f"Failed to connect to Joule at {self._ble_device.address}: {err}"
            ) from err

        try:
            await self._setup_services(auto_start_feed=auto_start_feed)
        except Exception as err:
            await self.disconnect()
            raise JouleConnectionError(f"Failed to setup GATT services: {err}") from err

    def _handle_disconnect(self, client: BleakClient) -> None:
        """Handle unexpected BLE disconnection."""
        self._stop_keepalive_task()
        _LOGGER.warning("Disconnected from Joule (%s)", self._ble_device.address)
        self._state.connected = False
        self._cleanup_pending_futures(
            JouleConnectionError("Device disconnected unexpectedly")
        )
        self._notify_listeners()

    def _cleanup_pending_futures(self, exc: Exception) -> None:
        """Cancel/fail any pending reply futures."""
        for _name, fut in list(self._response_futures.items()):
            if not fut.done():
                fut.set_exception(exc)
        self._response_futures.clear()

    async def _setup_services(self, auto_start_feed: bool = True) -> None:
        """Discover services and configure characteristics."""
        if not self._client:
            raise JouleConnectionError("No BLE client available")

        # Negotiate MTU / max payload size
        if hasattr(self._client, "mtu_size") and self._client.mtu_size:
            # ATT MTU includes 3 bytes of header
            self._max_payload_size = max(
                DEFAULT_ATT_PAYLOAD_SIZE, self._client.mtu_size - 3
            )
            _LOGGER.debug("Negotiated MTU payload size: %d", self._max_payload_size)

        # Detect service profile
        services = self._client.services
        if services.get_service(UUID_BREVILLE_SERVICE):
            self._is_breville_profile = True
            self._device_info.model = JouleModel.JOULE_TURBO
            self._write_char = services.get_characteristic(UUID_BREVILLE_APP_MESSAGE)
            self._notify_char = services.get_characteristic(
                UUID_BREVILLE_APPLIANCE_MESSAGE
            )
            _LOGGER.debug("Detected Breville Joule Turbo profile")
        elif services.get_service(UUID_CHEFSTEP_STREAM_SERVICE):
            self._is_breville_profile = False
            self._device_info.model = JouleModel.ORIGINAL_JOULE
            self._write_char = services.get_characteristic(UUID_CHEFSTEP_STREAM_WRITE)
            self._notify_char = services.get_characteristic(
                UUID_CHEFSTEP_STREAM_SUBSCRIBE
            )
            self._read_char = services.get_characteristic(UUID_CHEFSTEP_STREAM_READ)
            _LOGGER.debug("Detected ChefSteps Original Joule profile")
        else:
            raise JouleConnectionError(
                "Neither ChefSteps nor Breville GATT service found on device"
            )

        if not self._write_char or not self._notify_char:
            raise JouleConnectionError(
                f"Missing write or notify characteristic on {self._device_info.model}"
            )
        if not self._is_breville_profile and not self._read_char:
            raise JouleConnectionError(
                "Missing read characteristic on ChefSteps Original Joule"
            )

        # Read static device info if available
        await self._read_static_device_info()

        # Subscribe to notifications
        await self._client.start_notify(self._notify_char, self._handle_notification)

        # For ChefSteps Original Joule, Nordic nRF BLE radio stack requires ~500ms
        # to settle internal buffers post-subscription before accepting stream packets.
        if not self._is_breville_profile:
            _LOGGER.debug(
                "Waiting 500ms for ChefSteps BLE radio to settle post-subscription..."
            )
            await asyncio.sleep(0.5)

        self._state.connected = True
        self._notify_listeners()

        # Initial drain of ChefSteps stream read characteristic if present
        if not self._is_breville_profile and self._read_char:
            try:
                await self._read_chefsteps_stream()
            except Exception as err:
                _LOGGER.debug("Initial ChefSteps stream read skipped/failed: %s", err)

        if auto_start_feed:
            # If secret key exists in auth_data, authenticate to verify proximity
            if self._auth_data and (
                self._auth_data.secret_key or self._auth_data.secret
            ):
                try:
                    await self.authenticate(timeout=5.0)
                    _LOGGER.debug("Authenticated successfully on connect")
                except Exception as auth_err:
                    _LOGGER.debug(
                        "Authentication on connect skipped or failed: %s", auth_err
                    )

            # Request identification
            try:
                await self.identify()
            except Exception as err:
                _LOGGER.debug("Identify query failed or skipped: %s", err)

            # Start live cook feed to receive telemetry
            try:
                await self._start_live_feed()
            except Exception as err:
                _LOGGER.warning("Could not automatically start live cook feed: %s", err)

        # ChefSteps requires periodic KeepAlive to prevent idle disconnect
        if not self._is_breville_profile:
            self._start_keepalive_task()

    async def _read_static_device_info(self) -> None:
        """Attempt to read static serial or version characteristics."""
        if not self._client:
            return

        # Try Breville Serial Number
        if self._is_breville_profile:
            try:
                raw_sn = await self._client.read_gatt_char(UUID_BREVILLE_SERIAL_NUMBER)
                if raw_sn:
                    self._device_info.serial_number = raw_sn.decode(
                        "utf-8", errors="ignore"
                    ).strip()
            except Exception:
                pass

        # Try Device Info Service Version
        try:
            raw_ver = await self._client.read_gatt_char(UUID_DEVICE_VERSION)
            if raw_ver:
                self._device_info.firmware_version = raw_ver.decode(
                    "utf-8", errors="ignore"
                ).strip()
        except Exception:
            pass

    def _handle_notification(
        self, characteristic: BleakGATTCharacteristic, data: bytearray
    ) -> None:
        """Handle raw notification received from Joule."""
        _LOGGER.debug(
            "GATT notification on %s: %d bytes (hex: %s)",
            characteristic.uuid,
            len(data) if data else 0,
            data.hex() if data else "",
        )
        if self._is_breville_profile:
            self._rx_buffer.extend(data)
            self._try_parse_rx_buffer()
        else:
            # ChefSteps Original Joule:
            # Notifications on UUID_CHEFSTEP_STREAM_SUBSCRIBE are alerts
            # signalling that a StreamMessage is ready on
            # UUID_CHEFSTEP_STREAM_READ.
            _LOGGER.debug(
                "ChefSteps stream notification alert received (%s),"
                " triggering stream read",
                data.hex() if data else "empty",
            )
            if data and len(data) > 2:
                try:
                    msg = joule_pb2.StreamMessage()
                    msg.ParseFromString(bytes(data))
                    self._process_stream_message(msg)
                except Exception:
                    pass
            asyncio.create_task(self._read_chefsteps_stream())

    async def _read_chefsteps_stream(self) -> None:
        """Read a pending StreamMessage from ChefSteps read characteristic."""
        if not self._client or not self._read_char:
            return
        async with self._read_lock:
            try:
                raw_bytes = await self._client.read_gatt_char(self._read_char)
                if not raw_bytes:
                    _LOGGER.debug("ChefSteps stream read returned empty bytes")
                    return
                _LOGGER.debug(
                    "Read ChefSteps stream characteristic: %d bytes (hex: %s)",
                    len(raw_bytes),
                    raw_bytes.hex(),
                )
                msg = joule_pb2.StreamMessage()
                msg.ParseFromString(bytes(raw_bytes))
                self._process_stream_message(msg)
            except DecodeError as err:
                _LOGGER.warning(
                    "Failed to decode StreamMessage from ChefSteps read char: %s",
                    err,
                )
            except BleakError as err:
                _LOGGER.debug(
                    "BLE error reading ChefSteps stream characteristic: %s",
                    err,
                )
            except Exception as err:
                _LOGGER.debug(
                    "Error reading ChefSteps stream characteristic: %s",
                    err,
                )

    def _try_parse_rx_buffer(self) -> None:
        """Attempt to parse StreamMessage from the accumulated RX buffer."""
        try:
            msg = joule_pb2.StreamMessage()
            msg.ParseFromString(bytes(self._rx_buffer))
            self._rx_buffer.clear()
            self._process_stream_message(msg)
        except DecodeError:
            if len(self._rx_buffer) > 4096:
                _LOGGER.warning(
                    "Discarding corrupted RX buffer (%d bytes)",
                    len(self._rx_buffer),
                )
                self._rx_buffer.clear()

    def _process_stream_message(self, msg: joule_pb2.StreamMessage) -> None:
        """Process a fully reassembled StreamMessage."""
        if msg.HasField("senderAddress") and msg.senderAddress:
            self._recipient_address = msg.senderAddress
            self._device_info.recipient_address = msg.senderAddress

        # 1. Check for live telemetry CirculatorDataPoint
        if msg.HasField("circulatorDataPoint"):
            self._handle_circulator_data_point(msg.circulatorDataPoint)

        # 2. Check for IdentifyCirculatorReply
        if msg.HasField("identifyCirculatorReply"):
            rep = msg.identifyCirculatorReply
            if rep.name:
                self._device_info.name = rep.name
            if rep.serialNumber:
                self._device_info.serial_number = rep.serialNumber
            if rep.firmwareVersion:
                self._device_info.firmware_version = rep.firmwareVersion
            if rep.hardwareVersion:
                self._device_info.hardware_version = rep.hardwareVersion
            if rep.modelNumber:
                self._device_info.model_number = rep.modelNumber
            self._resolve_pending_reply("identifyCirculatorReply", msg)

        # 3. Check for command replies
        reply_fields = [
            "startProgramReply",
            "stopCirculatorReply",
            "updateProgramReply",
            "clearErrorReply",
            "dropFoodReply",
            "beginLiveFeedReply",
            "buttonPressReply",
            "cancelButtonPressReply",
            "startKeyExchangeReply",
            "cancelKeyExchangeReply",
            "submitKeyReply",
            "submitBearerAuthTokenReply",
            "setMessagingAddressReply",
            "displayLedReply",
        ]
        for f in reply_fields:
            if msg.HasField(f):
                self._resolve_pending_reply(f, msg)

    def _handle_circulator_data_point(self, dp: joule_pb2.CirculatorDataPoint) -> None:
        """Update internal state from incoming CirculatorDataPoint."""
        self._state.connected = True
        self._feed_ready_event.set()
        if dp.HasField("feedId"):
            self._latest_feed_id = dp.feedId
        if dp.HasField("sequenceNumber"):
            self._latest_seq_num = dp.sequenceNumber
        if dp.HasField("bathTemp"):
            self._state.bath_temp_c = round(dp.bathTemp, 2)
        if dp.HasField("heaterTemp"):
            self._state.heater_temp_c = round(dp.heaterTemp, 2)
        if dp.HasField("upperBoardTemp"):
            self._state.upper_board_temp_c = round(dp.upperBoardTemp, 2)
        if dp.HasField("lowerBoardTemp"):
            self._state.lower_board_temp_c = round(dp.lowerBoardTemp, 2)
        if dp.HasField("motorRPM"):
            self._state.motor_rpm = dp.motorRPM
        if dp.HasField("heaterPWM"):
            self._state.heater_pwm = dp.heaterPWM
        if dp.HasField("timeRemaining"):
            self._state.time_remaining_seconds = int(dp.timeRemaining)
        if dp.HasField("programStep"):
            self._state.program_step = CookState.from_proto(dp.programStep)
        if dp.HasField("errorState"):
            self._state.error_state = ErrorState.from_proto(dp.errorState)
        if dp.HasField("motorFaultFlag"):
            self._state.motor_fault = bool(dp.motorFaultFlag)

        # Infer low water level: error state active with no motor RPM
        if dp.HasField("errorState") and dp.errorState != joule_pb2.NO_ERROR:
            if dp.HasField("motorRPM") and dp.motorRPM == 0:
                self._state.low_water = True
        elif dp.HasField("errorState") and dp.errorState == joule_pb2.NO_ERROR:
            self._state.low_water = False

        self._state.last_updated = time.time()

        # Dual response recognition:
        # ChefSteps firmware often begins heating and emits CirculatorDataPoint
        # with programStep=PRE_HEAT or IDLE without sending a discrete reply.
        if "startProgramReply" in self._response_futures and self._state.is_cooking:
            _LOGGER.info(
                "Circulator transitioned to cooking step %s; resolving "
                "startProgramReply",
                self._state.program_step,
            )
            dummy_msg = joule_pb2.StreamMessage()
            dummy_msg.startProgramReply.result = joule_pb2.CS_SUCCESS
            self._resolve_pending_reply("startProgramReply", dummy_msg)

        if (
            "stopCirculatorReply" in self._response_futures
            and not self._state.is_cooking
        ):
            _LOGGER.info(
                "Circulator transitioned to idle step %s; resolving "
                "stopCirculatorReply",
                self._state.program_step,
            )
            dummy_msg = joule_pb2.StreamMessage()
            dummy_msg.stopCirculatorReply.result = joule_pb2.CS_SUCCESS
            self._resolve_pending_reply("stopCirculatorReply", dummy_msg)

        self._notify_listeners()

    def _resolve_pending_reply(
        self, reply_field: str, msg: joule_pb2.StreamMessage
    ) -> None:
        """Fulfill waiting future for a reply message."""
        fut = self._response_futures.pop(reply_field, None)
        if fut and not fut.done():
            fut.set_result(msg)

    async def _send_message(
        self,
        msg: joule_pb2.StreamMessage,
        expected_reply: str | None = None,
        timeout: float = DEFAULT_COMMAND_TIMEOUT,
    ) -> joule_pb2.StreamMessage | None:
        """Serialize, fragment, and send a StreamMessage.

        Optionally waits for a reply message.
        """
        if not self.is_connected or not self._client or not self._write_char:
            raise JouleConnectionError("Not connected to Joule")

        # Ensure required stream envelope headers are set
        if not msg.HasField("handle"):
            msg.handle = self._stream_handle
        if not msg.HasField("senderAddress"):
            msg.senderAddress = self._sender_address
        if not msg.HasField("recipientAddress"):
            msg.recipientAddress = self._recipient_address

        payload = msg.SerializeToString()

        write_with_response = (
            "write" in self._write_char.properties
            if self._write_char.properties
            else True
        )

        client = self._client
        write_char = self._write_char
        assert client is not None
        assert write_char is not None

        async def _do_write() -> None:
            _LOGGER.debug(
                "Sending StreamMessage (%d B, handle=%r, sender=%r, "
                "recipient=%r, response=%s)",
                len(payload),
                msg.handle,
                msg.senderAddress,
                msg.recipientAddress,
                write_with_response,
            )
            async with self._write_lock:
                try:
                    await client.write_gatt_char(
                        write_char,
                        payload,
                        response=write_with_response,
                    )
                except BleakError as err:
                    raise JouleConnectionError(
                        f"Failed to write BLE stream message: {err}"
                    ) from err

        if expected_reply is None:
            # Fire-and-forget message (KeepAlive or unacknowledged feed requests)
            await _do_write()
            return None

        # Request-reply command: serialize across other commands under stream_lock
        async with self._stream_lock:
            loop = asyncio.get_running_loop()
            reply_future: asyncio.Future[joule_pb2.StreamMessage] = loop.create_future()
            self._response_futures[expected_reply] = reply_future

            try:
                await _do_write()
            except Exception:
                self._response_futures.pop(expected_reply, None)
                raise

            try:
                return await asyncio.wait_for(
                    asyncio.shield(reply_future), timeout=timeout
                )
            except TimeoutError as err:
                # Fallback for ChefSteps: direct read on read characteristic
                if not self._is_breville_profile and self._read_char:
                    try:
                        await self._read_chefsteps_stream()
                        if reply_future.done() and not reply_future.cancelled():
                            return reply_future.result()
                    except Exception:
                        pass

                self._response_futures.pop(expected_reply, None)
                raise JouleTimeoutError(
                    f"Timed out waiting for {expected_reply} after {timeout}s"
                ) from err

    def _start_keepalive_task(self) -> None:
        """Start periodic KeepAlive background loop for ChefSteps Original Joule."""
        self._stop_keepalive_task()
        self._keepalive_task = asyncio.create_task(self._keepalive_loop())

    def _stop_keepalive_task(self) -> None:
        """Stop periodic KeepAlive background loop."""
        if self._keepalive_task and not self._keepalive_task.done():
            self._keepalive_task.cancel()
        self._keepalive_task = None

    async def _keepalive_loop(self) -> None:
        """Periodically send KeepAlive to ChefSteps Joule to maintain connection."""
        while self.is_connected:
            try:
                await asyncio.sleep(CHEFSTEPS_KEEPALIVE_INTERVAL)
                if not self.is_connected:
                    break
                await self.send_keep_alive()
            except asyncio.CancelledError:
                break
            except Exception as err:
                _LOGGER.debug("KeepAlive send error: %s", err)

    async def send_keep_alive(self) -> None:
        """Send a KeepAlive message to ChefSteps Original Joule."""
        if not self.is_connected or self._is_breville_profile:
            return
        msg = joule_pb2.StreamMessage()
        msg.keepAlive.CopyFrom(joule_pb2.KeepAlive())
        try:
            await self._send_message(msg, expected_reply=None)
        except Exception as err:
            _LOGGER.debug("Failed to send KeepAlive: %s", err)

    async def _start_live_feed(self) -> None:
        """Send BeginLiveFeed request to start streaming cook telemetry."""
        if not self._is_breville_profile:
            # ChefSteps Original Joule: mobile app issues describeFeedRequest
            # then beginLiveFeed
            desc_msg = joule_pb2.StreamMessage()
            desc_msg.describeFeedRequest.feedId = joule_pb2.COOK_DATA
            await self._send_message(desc_msg, expected_reply=None)

            msg = joule_pb2.StreamMessage()
            msg.beginLiveFeed.feedType = joule_pb2.COOK_DATA
            await self._send_message(msg, expected_reply=None)
            _LOGGER.debug(
                "Sent describeFeedRequest and beginLiveFeed (COOK_DATA) to "
                "ChefSteps Joule"
            )
            return

        req = joule_pb2.BeginLiveFeed()
        req.feedType = joule_pb2.COOK_DATA

        msg = joule_pb2.StreamMessage()
        msg.beginLiveFeed.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="beginLiveFeedReply", timeout=5.0
        )
        if reply and reply.beginLiveFeedReply.result != joule_pb2.CS_SUCCESS:
            _LOGGER.warning(
                "BeginLiveFeed returned error result: %d",
                reply.beginLiveFeedReply.result,
            )

    def _get_recipient_candidates(self) -> list[bytes]:
        """Generate candidate recipient addresses for ChefSteps Original Joule."""
        candidates: list[bytes] = []

        def _add(cand: bytes) -> None:
            if cand is not None and cand not in candidates:
                candidates.append(cand)

        # 1. Primary candidate: explicit or advertisement recipient address
        # (MakeRecipientAddress in official APK: raw bytes of mfg[1:])
        if (
            self._recipient_address
            and self._recipient_address != DEFAULT_RECIPIENT_ADDRESS
        ):
            _add(self._recipient_address)

        # 2. Universal broadcast address ("0")
        _add(DEFAULT_RECIPIENT_ADDRESS)

        clean_mac = self._ble_device.address.replace(":", "").replace("-", "")
        # 3. 6 raw binary MAC bytes (legacyJouleRecipientAddressBytes in Android APK)
        if len(clean_mac) == 12:
            try:
                _add(bytes.fromhex(clean_mac))
            except ValueError:
                pass

        # 4. ASCII hex representations (lowercase and uppercase)
        if len(clean_mac) == 12:
            _add(clean_mac.lower().encode("ascii"))
            _add(clean_mac.upper().encode("ascii"))

        # 5. Empty address (used by official iOS app)
        _add(b"")

        return candidates

    async def identify(self) -> JouleDeviceInfo:
        """Send IdentifyCirculatorRequest to query device metadata."""
        if self._is_breville_profile:
            msg = joule_pb2.StreamMessage()
            msg.identifyCirculatorRequest.CopyFrom(
                joule_pb2.IdentifyCirculatorRequest()
            )
            msg.recipientAddress = self._recipient_address or DEFAULT_RECIPIENT_ADDRESS
            await self._send_message(
                msg, expected_reply="identifyCirculatorReply", timeout=5.0
            )
            return self._device_info

        # ChefSteps Original Joule: negotiate recipient address across candidates
        candidates = self._get_recipient_candidates()
        last_error: Exception | None = None
        for cand in candidates:
            _LOGGER.debug(
                "Attempting identify query with recipient=%r (%d candidates total)",
                cand,
                len(candidates),
            )
            msg = joule_pb2.StreamMessage()
            msg.identifyCirculatorRequest.CopyFrom(
                joule_pb2.IdentifyCirculatorRequest()
            )
            msg.recipientAddress = cand
            try:
                reply = await self._send_message(
                    msg, expected_reply="identifyCirculatorReply", timeout=2.5
                )
                if reply:
                    _LOGGER.info(
                        "Identify query succeeded with recipientAddress=%r",
                        cand,
                    )
                    self._recipient_address = cand
                    self._device_info.recipient_address = cand
                    return self._device_info
            except JouleTimeoutError as err:
                _LOGGER.debug(
                    "Identify query timed out with recipientAddress=%r: %s",
                    cand,
                    err,
                )
                last_error = err
            except Exception as err:
                _LOGGER.debug(
                    "Identify query error with recipientAddress=%r: %s",
                    cand,
                    err,
                )
                last_error = err

        if last_error:
            raise last_error
        return self._device_info

    async def start_cook(
        self,
        target_temp_c: float,
        cook_time_seconds: int = 0,
        delayed_start_seconds: int = 0,
        holding_temp_c: float = 0.0,
    ) -> None:
        """Start cooking at target temperature in Celsius with optional timer."""
        if not (MIN_TEMP_C <= target_temp_c <= MAX_TEMP_C):
            raise ValueError(
                f"Target temperature {target_temp_c}°C must be between "
                f"{MIN_TEMP_C}°C and {MAX_TEMP_C}°C"
            )

        # On ChefSteps, ensure live feed has emitted at least one data point
        # for concurrency headers
        if not self._is_breville_profile and not self._latest_feed_id:
            _LOGGER.debug("Waiting for live feed data point before starting cook...")
            await self._start_live_feed()
            for _ in range(10):
                await asyncio.sleep(0.2)
                if self._latest_feed_id:
                    break

        prog = joule_pb2.CirculatorProgram()
        prog.setPoint = float(target_temp_c)
        if not self._is_breville_profile:
            # ChefSteps Original Joule:
            # The firmware requires programType=MANUAL (0) and NO cookTime.
            # Local control manages timers in software.
            prog.programType = joule_pb2.MANUAL

            # Pre-flight state hygiene: ChefSteps firmware rejects StartProgramRequest
            # with CS_ERROR_INVALID_STATE (code 8) if the circulator is non-idle
            # (e.g. already cooking or halted in CookState.ERROR). Stop & clear.
            had_error = self._state.has_error
            was_non_idle = self._state.program_step != CookState.IDLE

            if was_non_idle:
                _LOGGER.debug(
                    "Circulator in step %s before start_cook; stopping prior program",
                    self._state.program_step.value,
                )
                try:
                    await self.stop_cook()
                except Exception as err:
                    _LOGGER.debug("Pre-start stop_cook ignored: %s", err)

            if had_error:
                _LOGGER.debug(
                    "Active error condition (%s) before start_cook; clearing errors",
                    self._state.error_state.value,
                )
                try:
                    await self.clear_errors()
                except Exception as err:
                    _LOGGER.debug("Pre-start clear_errors ignored: %s", err)

            if not self._latest_feed_id or not self._latest_seq_num:
                _LOGGER.debug(
                    "Waiting up to 1.5s for initial live CirculatorDataPoint "
                    "to acquire feed session..."
                )
                try:
                    await asyncio.wait_for(self._feed_ready_event.wait(), timeout=1.5)
                except TimeoutError:
                    _LOGGER.debug(
                        "Timed out waiting for initial CirculatorDataPoint; continuing"
                    )
        else:
            if cook_time_seconds > 0:
                prog.cookTime = int(cook_time_seconds)
                prog.programType = joule_pb2.AUTOMATIC
            else:
                prog.programType = joule_pb2.MANUAL
            if delayed_start_seconds > 0:
                prog.delayedStart = int(delayed_start_seconds)
            if holding_temp_c >= MIN_TEMP_C:
                prog.holdingTemperature = float(holding_temp_c)

        req = joule_pb2.StartProgramRequest()
        req.circulatorProgram.CopyFrom(prog)
        if not self._is_breville_profile:
            req.feedId = (
                self._latest_feed_id if self._latest_feed_id else joule_pb2.COOK_DATA
            )
            if self._latest_seq_num:
                req.sequenceNumber = self._latest_seq_num

        msg = joule_pb2.StreamMessage()
        if not self._is_breville_profile:
            msg.handle = random.randint(1, 2**31 - 1)
            msg.senderAddress = b""
            msg.recipientAddress = b""
        msg.startProgramRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="startProgramReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.startProgramReply.result
            if (
                res == joule_pb2.CS_ERROR_INVALID_STATE
                and not self._is_breville_profile
            ):
                _LOGGER.warning(
                    "Start cook returned CS_ERROR_INVALID_STATE; attempting recovery "
                    "by stopping circulator"
                )
                try:
                    await self.stop_cook()
                    if self._latest_seq_num:
                        req.sequenceNumber = self._latest_seq_num
                    msg.handle = random.randint(1, 2**31 - 1)
                    retry_reply = await self._send_message(
                        msg,
                        expected_reply="startProgramReply",
                        timeout=DEFAULT_COMMAND_TIMEOUT,
                    )
                    if retry_reply:
                        res = retry_reply.startProgramReply.result
                except Exception as err:
                    _LOGGER.debug("Start cook recovery retry failed: %s", err)

            if res != joule_pb2.CS_SUCCESS:
                raise JouleCommandError(
                    f"Start cook failed with code {res}", result_code=res
                )

        self._state.target_temp_c = round(target_temp_c, 2)
        self._state.cook_time_seconds = (
            cook_time_seconds if cook_time_seconds > 0 else None
        )
        self._state.program_step = CookState.PRE_HEATING
        self._notify_listeners()

    async def set_temperature(self, target_temp_c: float) -> None:
        """Update target temperature setpoint for a currently cooking bath."""
        if not (MIN_TEMP_C <= target_temp_c <= MAX_TEMP_C):
            raise ValueError(
                f"Target temperature {target_temp_c}°C must be between "
                f"{MIN_TEMP_C}°C and {MAX_TEMP_C}°C"
            )

        # If already set to this target temperature while cooking, avoid redundant write
        if self._state.is_cooking and self._state.target_temp_c == round(
            target_temp_c, 2
        ):
            return

        # If not active, use start_cook
        if not self._state.is_cooking:
            await self.start_cook(target_temp_c)
            return

        req = joule_pb2.UpdateProgramRequest()
        req.setPoint = float(target_temp_c)
        req.updateProgramType = joule_pb2.REGULAR

        msg = joule_pb2.StreamMessage()
        if not self._is_breville_profile:
            msg.handle = random.randint(1, 2**31 - 1)
            msg.senderAddress = b""
            msg.recipientAddress = b""
        msg.updateProgramRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="updateProgramReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.updateProgramReply.result
            if res != joule_pb2.CS_SUCCESS:
                raise JouleCommandError(
                    f"Set temperature failed with code {res}", result_code=res
                )

        self._state.target_temp_c = round(target_temp_c, 2)
        self._notify_listeners()

    async def stop_cook(self) -> None:
        """Stop heating and circulating."""
        req = joule_pb2.StopCirculatorRequest()
        if not self._is_breville_profile:
            if self._latest_feed_id:
                req.feedId = self._latest_feed_id
            if self._latest_seq_num:
                req.sequenceNumber = self._latest_seq_num

        msg = joule_pb2.StreamMessage()
        if not self._is_breville_profile:
            msg.handle = random.randint(1, 2**31 - 1)
            msg.senderAddress = b""
            msg.recipientAddress = b""
        msg.stopCirculatorRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="stopCirculatorReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.stopCirculatorReply.result
            # Code 8 (CS_ERROR_INVALID_STATE) indicates circulator is already stopped
            if res not in (joule_pb2.CS_SUCCESS, joule_pb2.CS_ERROR_INVALID_STATE):
                raise JouleCommandError(
                    f"Stop circulator failed with code {res}", result_code=res
                )

        self._state.program_step = CookState.IDLE
        self._state.target_temp_c = None
        self._state.cook_time_seconds = None
        self._state.time_remaining_seconds = None
        self._notify_listeners()

    async def clear_errors(self) -> None:
        """Clear software error condition on the Joule."""
        req = joule_pb2.ClearErrorRequest()

        msg = joule_pb2.StreamMessage()
        if not self._is_breville_profile:
            msg.handle = random.randint(1, 2**31 - 1)
            msg.senderAddress = b""
            msg.recipientAddress = b""
        msg.clearErrorRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="clearErrorReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.clearErrorReply.result
            # Code 8 (CS_ERROR_INVALID_STATE), 3 (CS_ERROR_INTERNAL),
            # or 5 (CS_ERROR_NOT_FOUND) indicates no active error to clear
            if res not in (
                joule_pb2.CS_SUCCESS,
                joule_pb2.CS_ERROR_INVALID_STATE,
                joule_pb2.CS_ERROR_INTERNAL,
                joule_pb2.CS_ERROR_NOT_FOUND,
            ):
                raise JouleCommandError(
                    f"Clear error failed with code {res}", result_code=res
                )

        self._state.error_state = ErrorState.NO_ERROR
        self._state.low_water = False
        self._state.motor_fault = False
        if self._state.program_step == CookState.ERROR:
            self._state.program_step = CookState.IDLE
        self._notify_listeners()

    async def drop_food(self) -> None:
        """Confirm food has been added and transition from waiting to active cooking."""
        req = joule_pb2.DropFoodRequest()

        msg = joule_pb2.StreamMessage()
        if not self._is_breville_profile:
            msg.handle = random.randint(1, 2**31 - 1)
            msg.senderAddress = b""
            msg.recipientAddress = b""
        msg.dropFoodRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="dropFoodReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.dropFoodReply.result
            if res != joule_pb2.CS_SUCCESS:
                raise JouleCommandError(
                    f"Drop food failed with code {res}", result_code=res
                )

        if self._state.program_step == CookState.WAITING_FOR_FOOD:
            self._state.program_step = CookState.COOKING
            self._notify_listeners()

    async def request_button_press(
        self,
        duration_ms: int = 30000,
        led_color: int = joule_pb2.LED_COLOR_WHITE,
        led_pattern: int = joule_pb2.LED_PATTERN_BLINK,
        timeout: float = 35.0,
    ) -> bool:
        """Request user to press the physical button on Joule with blinking LED."""
        req = joule_pb2.ButtonPressRequest(
            ledColor=cast(Any, led_color),
            ledPattern=cast(Any, led_pattern),
            durationMilliseconds=duration_ms,
        )
        msg = joule_pb2.StreamMessage()
        msg.buttonPressRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="buttonPressReply", timeout=timeout
        )
        if reply and reply.buttonPressReply.result == joule_pb2.CS_SUCCESS:
            return True
        return False

    async def cancel_button_press(self) -> None:
        """Cancel an in-progress button press request."""
        req = joule_pb2.CancelButtonPressRequest()
        msg = joule_pb2.StreamMessage()
        msg.cancelButtonPressRequest.CopyFrom(req)
        await self._send_message(
            msg, expected_reply="cancelButtonPressReply", timeout=5.0
        )

    async def authenticate(
        self,
        secret_key: bytes | str | None = None,
        timeout: float = DEFAULT_COMMAND_TIMEOUT,
    ) -> bool:
        """Authenticate with the Joule using an existing secret key."""
        key = secret_key or (self._auth_data.secret_key if self._auth_data else None)
        if not key:
            raise JouleAuthenticationError("No secret key available for authentication")
        secret_bytes: bytes
        if isinstance(key, str):
            try:
                secret_bytes = bytes.fromhex(key)
            except ValueError:
                secret_bytes = key.encode("utf-8")
        else:
            secret_bytes = key

        req = joule_pb2.SubmitKeyRequest(secretKey=secret_bytes)
        msg = joule_pb2.StreamMessage()
        msg.submitKeyRequest.CopyFrom(req)
        msg.recipientAddress = self._recipient_address or DEFAULT_RECIPIENT_ADDRESS

        reply = await self._send_message(
            msg, expected_reply="submitKeyReply", timeout=timeout
        )
        if reply and reply.submitKeyReply.result == joule_pb2.CS_SUCCESS:
            return True
        res = reply.submitKeyReply.result if reply else None
        raise JouleAuthenticationError(f"Authentication failed with result code {res}")

    async def start_key_exchange(
        self, timeout: float = DEFAULT_PAIR_TIMEOUT
    ) -> JouleAuthData:
        """Initiate key exchange to pair with the Joule and obtain a secret key."""
        req = joule_pb2.StartKeyExchangeRequest()
        msg = joule_pb2.StreamMessage()
        msg.startKeyExchangeRequest.CopyFrom(req)
        msg.recipientAddress = self._recipient_address or DEFAULT_RECIPIENT_ADDRESS

        reply = await self._send_message(
            msg, expected_reply="startKeyExchangeReply", timeout=timeout
        )
        if not reply:
            raise JouleAuthenticationError("No reply to key exchange request")

        res = reply.startKeyExchangeReply.result
        if res != joule_pb2.CS_SUCCESS:
            raise JouleAuthenticationError(
                f"Start key exchange failed with result code {res}"
            )

        secret = reply.startKeyExchangeReply.secretKey
        self._auth_data = JouleAuthData(secret_key=secret, secret=secret)
        # Immediately submit received key to transition proximity state to verified
        try:
            await self.authenticate(secret_key=secret, timeout=5.0)
            _LOGGER.debug("Proximity verified with circulator following key exchange")
        except Exception as auth_err:
            _LOGGER.debug(
                "Immediate key submission post-exchange skipped or failed: %s",
                auth_err,
            )
        return self._auth_data

    async def pair_or_authenticate(
        self, timeout: float = DEFAULT_PAIR_TIMEOUT
    ) -> JouleAuthData:
        """Perform authenticated pairing / key exchange if required by firmware."""
        if self._auth_data and (self._auth_data.secret_key or self._auth_data.secret):
            try:
                await self.authenticate(timeout=timeout)
                return self._auth_data
            except JouleAuthenticationError:
                _LOGGER.debug(
                    "Existing secret key rejected; falling back to key exchange"
                )

        return await self.start_key_exchange(timeout=timeout)

    async def disconnect(self) -> None:
        """Cleanly disconnect from the Joule."""
        self._stop_keepalive_task()
        if self._client:
            try:
                if self._notify_char:
                    await self._client.stop_notify(self._notify_char)
            except Exception:
                pass
            try:
                await self._client.disconnect()
            except Exception:
                pass
            finally:
                self._client = None
                self._write_char = None
                self._notify_char = None
                self._read_char = None

        self._state.connected = False
        self._feed_ready_event.clear()
        self._latest_feed_id = 0
        self._latest_seq_num = 0
        self._cleanup_pending_futures(JouleConnectionError("Client disconnected"))
        self._notify_listeners()
