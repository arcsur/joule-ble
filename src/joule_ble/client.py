"""Bluetooth Low Energy client for Joule sous vide devices."""

from __future__ import annotations

import asyncio
import logging
import time
from collections.abc import Callable

from bleak import BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.exc import BleakError
from bleak_retry_connector import establish_connection
from google.protobuf.message import DecodeError

from .const import (
    DEFAULT_ATT_PAYLOAD_SIZE,
    DEFAULT_COMMAND_TIMEOUT,
    DEFAULT_CONNECT_TIMEOUT,
    MAX_TEMP_C,
    MIN_TEMP_C,
    UUID_BREVILLE_APP_MESSAGE,
    UUID_BREVILLE_APPLIANCE_MESSAGE,
    UUID_BREVILLE_SERIAL_NUMBER,
    UUID_BREVILLE_SERVICE,
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
    ) -> None:
        """Initialize the Joule client."""
        self._ble_device = ble_device
        self._auth_data = auth_data or JouleAuthData()
        self._model = model

        self._client: BleakClient | None = None
        self._write_char: BleakGATTCharacteristic | None = None
        self._notify_char: BleakGATTCharacteristic | None = None
        self._is_breville_profile: bool = False

        self._device_info: JouleDeviceInfo = JouleDeviceInfo(
            name=ble_device.name or "Joule",
            model=model,
            mac_address=ble_device.address,
        )
        self._state: JouleState = JouleState()
        self._callbacks: list[Callable[[JouleState], None]] = []

        self._write_lock = asyncio.Lock()
        self._response_futures: dict[str, asyncio.Future[joule_pb2.StreamMessage]] = {}
        self._rx_buffer = bytearray()
        self._max_payload_size = DEFAULT_ATT_PAYLOAD_SIZE

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

    async def connect(self, timeout: float = DEFAULT_CONNECT_TIMEOUT) -> None:
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
            await self._setup_services()
        except Exception as err:
            await self.disconnect()
            raise JouleConnectionError(f"Failed to setup GATT services: {err}") from err

    def _handle_disconnect(self, client: BleakClient) -> None:
        """Handle unexpected BLE disconnection."""
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

    async def _setup_services(self) -> None:
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
            _LOGGER.debug("Detected ChefSteps Original Joule profile")
        else:
            raise JouleConnectionError(
                "Neither ChefSteps nor Breville GATT service found on device"
            )

        if not self._write_char or not self._notify_char:
            raise JouleConnectionError(
                f"Missing write or notify characteristic on {self._device_info.model}"
            )

        # Read static device info if available
        await self._read_static_device_info()

        # Subscribe to notifications
        await self._client.start_notify(self._notify_char, self._handle_notification)

        self._state.connected = True
        self._notify_listeners()

        # Request identification and start live feed
        try:
            await self.identify()
        except Exception as err:
            _LOGGER.debug("Identify query failed or skipped: %s", err)

        try:
            await self._start_live_feed()
        except Exception as err:
            _LOGGER.warning("Could not automatically start live cook feed: %s", err)

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
        """Handle raw notification chunks received from Joule."""
        self._rx_buffer.extend(data)

        # Try parsing message from accumulated buffer
        try:
            msg = joule_pb2.StreamMessage()
            msg.ParseFromString(bytes(self._rx_buffer))
            # Successfully parsed full message
            self._rx_buffer.clear()
            self._process_stream_message(msg)
        except DecodeError:
            # Buffer contains partial message or corrupted stream
            # If buffer gets unreasonably large, discard to avoid memory bloat
            if len(self._rx_buffer) > 4096:
                _LOGGER.warning(
                    "Discarding corrupted RX buffer (%d bytes)",
                    len(self._rx_buffer),
                )
                self._rx_buffer.clear()

    def _process_stream_message(self, msg: joule_pb2.StreamMessage) -> None:
        """Process a fully reassembled StreamMessage."""
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
            "startKeyExchangeReply",
            "submitBearerAuthTokenReply",
        ]
        for f in reply_fields:
            if msg.HasField(f):
                self._resolve_pending_reply(f, msg)

    def _handle_circulator_data_point(self, dp: joule_pb2.CirculatorDataPoint) -> None:
        """Update internal state from incoming CirculatorDataPoint."""
        self._state.connected = True
        self._state.bath_temp_c = round(dp.bathTemp, 2)
        self._state.heater_temp_c = round(dp.heaterTemp, 2)
        self._state.upper_board_temp_c = round(dp.upperBoardTemp, 2)
        self._state.lower_board_temp_c = round(dp.lowerBoardTemp, 2)
        self._state.motor_rpm = dp.motorRPM
        self._state.heater_pwm = dp.heaterPWM
        self._state.time_remaining_seconds = int(dp.timeRemaining)
        self._state.program_step = CookState.from_proto(dp.programStep)
        self._state.error_state = ErrorState.from_proto(dp.errorState)
        self._state.motor_fault = bool(dp.motorFaultFlag)

        # Infer low water level: error state active with no motor RPM
        if dp.errorState != joule_pb2.NO_ERROR and dp.motorRPM == 0:
            self._state.low_water = True
        elif dp.errorState == joule_pb2.NO_ERROR:
            self._state.low_water = False

        self._state.last_updated = time.time()
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

        payload = msg.SerializeToString()
        reply_future: asyncio.Future[joule_pb2.StreamMessage] | None = None

        if expected_reply:
            loop = asyncio.get_running_loop()
            reply_future = loop.create_future()
            self._response_futures[expected_reply] = reply_future

        async with self._write_lock:
            # Fragment payload into MTU chunks
            total_len = len(payload)
            chunk_size = self._max_payload_size
            offset = 0

            while offset < total_len:
                chunk = payload[offset : offset + chunk_size]
                offset += len(chunk)
                try:
                    # Write with response if supported, otherwise without response
                    can_write_with_response = "write" in self._write_char.properties
                    await self._client.write_gatt_char(
                        self._write_char,
                        chunk,
                        response=can_write_with_response,
                    )
                except BleakError as err:
                    if reply_future and expected_reply:
                        self._response_futures.pop(expected_reply, None)
                    raise JouleConnectionError(
                        f"Failed to write BLE chunk: {err}"
                    ) from err

        if not reply_future:
            return None

        try:
            return await asyncio.wait_for(reply_future, timeout=timeout)
        except TimeoutError as err:
            if expected_reply is not None:
                self._response_futures.pop(expected_reply, None)
            raise JouleTimeoutError(
                f"Timed out waiting for {expected_reply} after {timeout}s"
            ) from err

    async def _start_live_feed(self) -> None:
        """Send BeginLiveFeed request to start streaming cook telemetry."""
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

    async def identify(self) -> JouleDeviceInfo:
        """Send IdentifyCirculatorRequest to query device metadata."""
        msg = joule_pb2.StreamMessage()
        msg.identifyCirculatorRequest.CopyFrom(joule_pb2.IdentifyCirculatorRequest())

        await self._send_message(
            msg, expected_reply="identifyCirculatorReply", timeout=5.0
        )
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

        prog = joule_pb2.CirculatorProgram()
        prog.setPoint = float(target_temp_c)
        prog.cookTime = int(cook_time_seconds)
        prog.delayedStart = int(delayed_start_seconds)
        prog.holdingTemperature = float(holding_temp_c)
        prog.programType = joule_pb2.MANUAL

        req = joule_pb2.StartProgramRequest()
        req.circulatorProgram.CopyFrom(prog)

        msg = joule_pb2.StreamMessage()
        msg.startProgramRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="startProgramReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.startProgramReply.result
            if res != joule_pb2.CS_SUCCESS:
                raise JouleCommandError(
                    f"Start cook failed with code {res}", result_code=res
                )

        self._state.target_temp_c = round(target_temp_c, 2)
        self._state.cook_time_seconds = cook_time_seconds
        self._state.program_step = CookState.PRE_HEATING
        self._notify_listeners()

    async def set_temperature(self, target_temp_c: float) -> None:
        """Update target temperature setpoint for a currently cooking bath."""
        if not (MIN_TEMP_C <= target_temp_c <= MAX_TEMP_C):
            raise ValueError(
                f"Target temperature {target_temp_c}°C must be between "
                f"{MIN_TEMP_C}°C and {MAX_TEMP_C}°C"
            )

        # If not active, use start_cook
        if not self._state.is_cooking:
            await self.start_cook(target_temp_c)
            return

        req = joule_pb2.UpdateProgramRequest()
        req.setPoint = float(target_temp_c)
        req.updateProgramType = joule_pb2.REGULAR

        msg = joule_pb2.StreamMessage()
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

        msg = joule_pb2.StreamMessage()
        msg.stopCirculatorRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="stopCirculatorReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.stopCirculatorReply.result
            if res != joule_pb2.CS_SUCCESS:
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
        msg.clearErrorRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="clearErrorReply", timeout=DEFAULT_COMMAND_TIMEOUT
        )
        if reply:
            res = reply.clearErrorReply.result
            if res != joule_pb2.CS_SUCCESS:
                raise JouleCommandError(
                    f"Clear error failed with code {res}", result_code=res
                )

        self._state.error_state = ErrorState.NO_ERROR
        self._state.low_water = False
        self._state.motor_fault = False
        self._notify_listeners()

    async def drop_food(self) -> None:
        """Confirm food has been added and transition from waiting to active cooking."""
        req = joule_pb2.DropFoodRequest()

        msg = joule_pb2.StreamMessage()
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

    async def pair_or_authenticate(self, timeout: float = 30.0) -> JouleAuthData:
        """Perform authenticated pairing / key exchange if required by firmware."""
        # 1. Start key exchange request
        req = joule_pb2.StartKeyExchangeRequest()
        msg = joule_pb2.StreamMessage()
        msg.startKeyExchangeRequest.CopyFrom(req)

        reply = await self._send_message(
            msg, expected_reply="startKeyExchangeReply", timeout=timeout
        )
        if not reply:
            raise JouleAuthenticationError("No reply to key exchange request")

        token = reply.startKeyExchangeReply.token
        secret = reply.startKeyExchangeReply.secretKey
        self._auth_data = JouleAuthData(token=token, secret=secret)
        return self._auth_data

    async def disconnect(self) -> None:
        """Cleanly disconnect from the Joule."""
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

        self._state.connected = False
        self._cleanup_pending_futures(JouleConnectionError("Client disconnected"))
        self._notify_listeners()
