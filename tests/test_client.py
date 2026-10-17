"""Tests for JouleClient."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from bleak.backends.characteristic import BleakGATTCharacteristic
from bleak.backends.device import BLEDevice
from bleak.backends.service import BleakGATTService, BleakGATTServiceCollection

from joule_ble import (
    MAX_TEMP_C,
    MIN_TEMP_C,
    CookState,
    ErrorState,
    JouleClient,
    JouleCommandError,
    JouleModel,
    JouleTimeoutError,
)
from joule_ble.const import (
    DEFAULT_RECIPIENT_ADDRESS,
    UUID_BREVILLE_APP_MESSAGE,
    UUID_BREVILLE_APPLIANCE_MESSAGE,
    UUID_BREVILLE_SERIAL_NUMBER,
    UUID_BREVILLE_SERVICE,
    UUID_CHEFSTEP_STREAM_READ,
    UUID_CHEFSTEP_STREAM_SERVICE,
    UUID_CHEFSTEP_STREAM_SUBSCRIBE,
    UUID_CHEFSTEP_STREAM_WRITE,
)
from joule_ble.proto import joule_pb2


def create_mock_bleak_client(profile: str = "chefsteps"):
    """Create a configured mock BleakClient with GATT services."""
    mock_client = MagicMock()
    mock_client.is_connected = True
    mock_client.mtu_size = 247
    mock_client.connect = AsyncMock(return_value=True)
    mock_client.disconnect = AsyncMock()
    mock_client.start_notify = AsyncMock()
    mock_client.stop_notify = AsyncMock()
    mock_client.write_gatt_char = AsyncMock()
    mock_client.read_gatt_char = AsyncMock(return_value=b"")

    services = BleakGATTServiceCollection()

    if profile == "chefsteps":
        write_char = MagicMock(spec=BleakGATTCharacteristic)
        write_char.uuid = UUID_CHEFSTEP_STREAM_WRITE
        write_char.properties = ["write", "write-without-response"]

        notify_char = MagicMock(spec=BleakGATTCharacteristic)
        notify_char.uuid = UUID_CHEFSTEP_STREAM_SUBSCRIBE
        notify_char.properties = ["notify", "write"]

        read_char = MagicMock(spec=BleakGATTCharacteristic)
        read_char.uuid = UUID_CHEFSTEP_STREAM_READ
        read_char.properties = ["read"]

        svc = MagicMock(spec=BleakGATTService)
        svc.uuid = UUID_CHEFSTEP_STREAM_SERVICE

        def get_service(uuid):
            if uuid == UUID_CHEFSTEP_STREAM_SERVICE:
                return svc
            return None

        def get_char(uuid):
            if uuid == UUID_CHEFSTEP_STREAM_WRITE:
                return write_char
            if uuid == UUID_CHEFSTEP_STREAM_SUBSCRIBE:
                return notify_char
            if uuid == UUID_CHEFSTEP_STREAM_READ:
                return read_char
            return None

    else:
        app_write = MagicMock(spec=BleakGATTCharacteristic)
        app_write.uuid = UUID_BREVILLE_APP_MESSAGE
        app_write.properties = ["write"]

        appliance_notify = MagicMock(spec=BleakGATTCharacteristic)
        appliance_notify.uuid = UUID_BREVILLE_APPLIANCE_MESSAGE
        appliance_notify.properties = ["notify"]

        svc = MagicMock(spec=BleakGATTService)
        svc.uuid = UUID_BREVILLE_SERVICE

        def get_service(uuid):
            if uuid == UUID_BREVILLE_SERVICE:
                return svc
            return None

        def get_char(uuid):
            if uuid == UUID_BREVILLE_APP_MESSAGE:
                return app_write
            if uuid == UUID_BREVILLE_APPLIANCE_MESSAGE:
                return appliance_notify
            if uuid == UUID_BREVILLE_SERIAL_NUMBER:
                return MagicMock()
            return None

    services.get_service = MagicMock(side_effect=get_service)
    services.get_characteristic = MagicMock(side_effect=get_char)
    mock_client.services = services

    return mock_client


@pytest.mark.asyncio
async def test_client_connect_chefsteps_profile():
    """Test connecting to a ChefSteps Original Joule."""
    device = BLEDevice("11:22:33:44:55:66", "Joule CS100", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)
        assert client.is_connected
        assert client.device_info.model == JouleModel.ORIGINAL_JOULE
        assert client.state.connected


@pytest.mark.asyncio
async def test_client_connect_breville_profile():
    """Test connecting to a Breville Joule Turbo."""
    device = BLEDevice("66:55:44:33:22:11", "Joule Turbo", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("breville")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)
        assert client.is_connected
        assert client.device_info.model == JouleModel.JOULE_TURBO


@pytest.mark.asyncio
async def test_client_notification_updates_state():
    """Test receiving CirculatorDataPoint notifications."""
    device = BLEDevice("11:22:33:44:55:66", "Joule Turbo", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("breville")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    updates = []
    client.register_callback(lambda s: updates.append(s.bath_temp_c))

    # Simulate incoming CirculatorDataPoint notification
    dp_msg = joule_pb2.StreamMessage()
    dp = dp_msg.circulatorDataPoint
    dp.bathTemp = 57.25
    dp.heaterTemp = 59.0
    dp.motorRPM = 1250
    dp.programStep = joule_pb2.COOK
    dp.errorState = joule_pb2.NO_ERROR
    dp.timeRemaining = 1800

    raw_data = bytearray(dp_msg.SerializeToString())
    client._handle_notification(MagicMock(), raw_data)

    assert client.state.bath_temp_c == 57.25
    assert client.state.heater_temp_c == 59.0
    assert client.state.motor_rpm == 1250
    assert client.state.program_step == CookState.COOKING
    assert client.state.time_remaining_seconds == 1800
    assert client.state.low_water is False
    assert 57.25 in updates


@pytest.mark.asyncio
async def test_client_start_cook_success():
    """Test start_cook command with successful reply."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    # Intercept write_gatt_char to automatically simulate startProgramReply
    async def fake_write(char, data, response=False):
        if data == bytearray([1]):
            return
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.startProgramReply.result = joule_pb2.CS_SUCCESS
        mock_bleak.read_gatt_char.return_value = reply_msg.SerializeToString()
        client._handle_notification(MagicMock(), bytearray([1]))

    mock_bleak.write_gatt_char.side_effect = fake_write

    await client.start_cook(target_temp_c=54.5, cook_time_seconds=3600)
    assert client.state.target_temp_c == 54.5
    assert client.state.cook_time_seconds == 3600
    assert client.state.program_step == CookState.PRE_HEATING


@pytest.mark.asyncio
async def test_client_start_cook_invalid_temp():
    """Test that start_cook rejects temperatures outside safe limits."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)

    with pytest.raises(ValueError):
        await client.start_cook(target_temp_c=MIN_TEMP_C - 1.0)

    with pytest.raises(ValueError):
        await client.start_cook(target_temp_c=MAX_TEMP_C + 1.0)


@pytest.mark.asyncio
async def test_client_start_cook_error_reply():
    """Test start_cook raising JouleCommandError on error reply."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    async def fake_write(char, data, response=False):
        if data == bytearray([1]):
            return
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.startProgramReply.result = joule_pb2.CS_ERROR_INVALID_STATE
        mock_bleak.read_gatt_char.return_value = reply_msg.SerializeToString()
        client._handle_notification(MagicMock(), bytearray([1]))

    mock_bleak.write_gatt_char.side_effect = fake_write

    with pytest.raises(JouleCommandError) as exc_info:
        await client.start_cook(target_temp_c=55.0)
    assert exc_info.value.result_code == joule_pb2.CS_ERROR_INVALID_STATE


@pytest.mark.asyncio
async def test_client_stop_cook():
    """Test stop_cook command."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    async def fake_write(char, data, response=False):
        if data == bytearray([1]):
            return
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.stopCirculatorReply.result = joule_pb2.CS_SUCCESS
        mock_bleak.read_gatt_char.return_value = reply_msg.SerializeToString()
        client._handle_notification(MagicMock(), bytearray([1]))

    mock_bleak.write_gatt_char.side_effect = fake_write

    await client.stop_cook()
    assert client.state.program_step == CookState.IDLE
    assert client.state.target_temp_c is None


@pytest.mark.asyncio
async def test_client_clear_errors():
    """Test clear_errors command."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    client._state.error_state = ErrorState.SOFT_ERROR
    client._state.low_water = True

    async def fake_write(char, data, response=False):
        if data == bytearray([1]):
            return
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.clearErrorReply.result = joule_pb2.CS_SUCCESS
        mock_bleak.read_gatt_char.return_value = reply_msg.SerializeToString()
        client._handle_notification(MagicMock(), bytearray([1]))

    mock_bleak.write_gatt_char.side_effect = fake_write

    await client.clear_errors()
    assert client.state.error_state == ErrorState.NO_ERROR
    assert client.state.low_water is False


@pytest.mark.asyncio
async def test_client_command_timeout():
    """Test that missing reply times out and raises JouleTimeoutError."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    # write_gatt_char succeeds, but no reply arrives
    with pytest.raises(JouleTimeoutError):
        await client._send_message(
            joule_pb2.StreamMessage(),
            expected_reply="startProgramReply",
            timeout=0.05,
        )


@pytest.mark.asyncio
async def test_client_clean_disconnect():
    """Test disconnecting cleanly."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)
        assert client.is_connected

        await client.disconnect()
        assert not client.is_connected
        assert not client.state.connected


@pytest.mark.asyncio
async def test_drop_food():
    """Test sending drop_food command transitions state."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    client.state.program_step = CookState.WAITING_FOR_FOOD

    async def reply_drop_food(char, data, response=False):
        if data == bytearray([1]):
            return
        msg = joule_pb2.StreamMessage()
        msg.dropFoodReply.result = joule_pb2.CS_SUCCESS
        mock_bleak.read_gatt_char.return_value = msg.SerializeToString()
        client._handle_notification(MagicMock(), bytearray([1]))

    mock_bleak.write_gatt_char.side_effect = reply_drop_food

    await client.drop_food()
    assert client.state.program_step == CookState.COOKING


@pytest.mark.asyncio
async def test_client_chefsteps_empty_notification_triggers_read():
    """Test ChefSteps empty notification triggers a read on 700b4323."""
    import asyncio

    device = BLEDevice("11:22:33:44:55:66", "Joule CS100", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    dp_msg = joule_pb2.StreamMessage()
    dp_msg.senderAddress = b"JOULE123"
    dp = dp_msg.circulatorDataPoint
    dp.bathTemp = 60.5
    dp.heaterTemp = 62.0
    dp.motorRPM = 1100
    dp.programStep = joule_pb2.COOK
    dp.errorState = joule_pb2.NO_ERROR
    dp.timeRemaining = 1200
    mock_bleak.read_gatt_char.return_value = dp_msg.SerializeToString()

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    # Empty notification payload arrives from Joule (alert signal)
    client._handle_notification(MagicMock(), bytearray(b""))
    await asyncio.sleep(0.01)

    assert client.state.bath_temp_c == 60.5
    assert client.device_info.recipient_address == b"JOULE123"


@pytest.mark.asyncio
async def test_client_send_message_sets_envelope_headers():
    """Test outgoing StreamMessage envelopes include required headers."""
    device = BLEDevice("11:22:33:44:55:66", "Joule CS100", {})
    client = JouleClient(device, recipient_address=b"MYJOULE1")
    mock_bleak = create_mock_bleak_client("chefsteps")

    captured_chunks = []

    async def capture_write(char, data, response=False):
        if data == bytearray([1]):
            return
        captured_chunks.append(bytes(data))
        reply = joule_pb2.StreamMessage()
        reply.clearErrorReply.result = joule_pb2.CS_SUCCESS
        client._resolve_pending_reply("clearErrorReply", reply)

    mock_bleak.write_gatt_char.side_effect = capture_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    await client.clear_errors()

    assert len(captured_chunks) > 0
    sent_msg = joule_pb2.StreamMessage()
    sent_msg.ParseFromString(captured_chunks[0])
    assert sent_msg.handle == 2389
    assert sent_msg.senderAddress == b"ABCDABCD"
    assert sent_msg.recipientAddress == b"MYJOULE1"


@pytest.mark.asyncio
async def test_client_key_exchange_and_auth():
    """Test start_key_exchange and authenticate methods."""
    device = BLEDevice("11:22:33:44:55:66", "Joule CS100", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    async def fake_write(char, data, response=False):
        sent = joule_pb2.StreamMessage()
        sent.ParseFromString(bytes(data))
        reply = joule_pb2.StreamMessage()
        if sent.HasField("startKeyExchangeRequest"):
            reply.startKeyExchangeReply.secretKey = b"MY_SECRET_KEY_12345"
            reply.startKeyExchangeReply.result = joule_pb2.CS_SUCCESS
            client._resolve_pending_reply("startKeyExchangeReply", reply)
        elif sent.HasField("submitKeyRequest"):
            if sent.submitKeyRequest.secretKey == b"MY_SECRET_KEY_12345":
                reply.submitKeyReply.result = joule_pb2.CS_SUCCESS
            else:
                reply.submitKeyReply.result = joule_pb2.CS_ERROR_FORBIDDEN
            client._resolve_pending_reply("submitKeyReply", reply)

    mock_bleak.write_gatt_char.side_effect = fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    auth_data = await client.start_key_exchange()
    assert auth_data.secret_key == b"MY_SECRET_KEY_12345"

    auth_success = await client.authenticate()
    assert auth_success is True


@pytest.mark.asyncio
async def test_client_request_button_press():
    """Test request_button_press and cancel_button_press."""
    device = BLEDevice("11:22:33:44:55:66", "Joule CS100", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    async def fake_write(char, data, response=False):
        sent = joule_pb2.StreamMessage()
        sent.ParseFromString(bytes(data))
        reply = joule_pb2.StreamMessage()
        if sent.HasField("buttonPressRequest"):
            reply.buttonPressReply.result = joule_pb2.CS_SUCCESS
            client._resolve_pending_reply("buttonPressReply", reply)
        elif sent.HasField("cancelButtonPressRequest"):
            reply.cancelButtonPressReply.result = joule_pb2.CS_SUCCESS
            client._resolve_pending_reply("cancelButtonPressReply", reply)

    mock_bleak.write_gatt_char.side_effect = fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    pressed = await client.request_button_press(duration_ms=5000)
    assert pressed is True

    await client.cancel_button_press()


@pytest.mark.asyncio
async def test_client_stream_envelope_headers():
    """Test that stream envelope headers are correctly formatted."""
    device = BLEDevice("CD:F6:E0:B4:F7:5D", "DagusJoule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    captured_messages: list[joule_pb2.StreamMessage] = []

    async def fake_write(char, data, response=False):
        sent = joule_pb2.StreamMessage()
        sent.ParseFromString(bytes(data))
        captured_messages.append(sent)
        if sent.HasField("identifyCirculatorRequest"):
            reply = joule_pb2.StreamMessage()
            reply.handle = 2389
            reply.senderAddress = b"cdf6e0b4f75d"
            reply.recipientAddress = b"ABCDABCD"
            reply.identifyCirculatorReply.name = "DagusJoule"
            client._resolve_pending_reply("identifyCirculatorReply", reply)

    mock_bleak.write_gatt_char.side_effect = fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)
        info = await client.identify()

    assert info.name == "DagusJoule"
    assert len(captured_messages) == 1
    sent_msg = captured_messages[0]
    assert sent_msg.handle == 2389
    assert sent_msg.senderAddress == b"ABCDABCD"
    assert sent_msg.recipientAddress == DEFAULT_RECIPIENT_ADDRESS


@pytest.mark.asyncio
async def test_client_connect_subscribes_chefsteps_stream():
    """Test ChefSteps connect starts notify without bogus write on subscribe char."""
    device = BLEDevice("11:22:33:44:55:66", "ChefSteps Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    # Verify start_notify was called for subscribe characteristic
    mock_bleak.start_notify.assert_called_once()
    notify_call_char = mock_bleak.start_notify.call_args[0][0]
    assert notify_call_char.uuid == UUID_CHEFSTEP_STREAM_SUBSCRIBE

    # Verify write_gatt_char was NOT called (no bogus 0x01 write on subscribe)
    mock_bleak.write_gatt_char.assert_not_called()


@pytest.mark.asyncio
async def test_client_identify_candidate_negotiation():
    """Test ChefSteps identify negotiates across candidate addresses on timeout."""
    device = BLEDevice("CD:F6:E0:B4:F7:5D", "DagusJoule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    attempted_recipients: list[bytes] = []

    async def fake_write(char, data, response=False):
        sent = joule_pb2.StreamMessage()
        sent.ParseFromString(bytes(data))
        attempted_recipients.append(sent.recipientAddress)
        # Fail candidate 1 (DEFAULT_RECIPIENT_ADDRESS b"0"), succeed on candidate 2
        if sent.recipientAddress == b"\xcd\xf6\xe0\xb4\xf7\x5d":
            reply = joule_pb2.StreamMessage()
            reply.senderAddress = b"cdf6e0b4f75d"
            reply.identifyCirculatorReply.name = "DagusJoule"
            client._resolve_pending_reply("identifyCirculatorReply", reply)

    mock_bleak.write_gatt_char.side_effect = fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)
        info = await client.identify()

    assert info.name == "DagusJoule"
    # First attempt was DEFAULT_RECIPIENT_ADDRESS (b"0"), second was raw 6 MAC bytes
    assert attempted_recipients[0] == DEFAULT_RECIPIENT_ADDRESS
    assert attempted_recipients[1] == b"\xcd\xf6\xe0\xb4\xf7\x5d"
    assert client.device_info.recipient_address == b"\xcd\xf6\xe0\xb4\xf7\x5d"


@pytest.mark.asyncio
async def test_client_chefsteps_alert_byte_triggers_read():
    """Test ChefSteps notification with alert byte (0x01) triggers stream read."""
    device = BLEDevice("11:22:33:44:55:66", "ChefSteps Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    dp_msg = joule_pb2.StreamMessage()
    dp_msg.circulatorDataPoint.bathTemp = 55.5
    dp_msg.circulatorDataPoint.programStep = joule_pb2.COOK
    mock_bleak.read_gatt_char.return_value = dp_msg.SerializeToString()

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect(auto_start_feed=False)

    # Firmware sends 1-byte alert notification payload (0x01)
    client._handle_notification(MagicMock(), bytearray([1]))
    await asyncio.sleep(0.02)

    assert client.state.bath_temp_c == 55.5
    assert client.state.program_step == CookState.COOKING


@pytest.mark.asyncio
async def test_client_write_response_modes():
    """Test ChefSteps and Breville both use response=True for stream messages."""
    # Test ChefSteps
    cs_device = BLEDevice("11:22:33:44:55:66", "ChefSteps Joule", {})
    cs_client = JouleClient(cs_device)
    cs_mock = create_mock_bleak_client("chefsteps")

    cs_writes = []

    async def cs_fake_write(char, data, response=False):
        cs_writes.append((char.uuid, response))
        if char.uuid == UUID_CHEFSTEP_STREAM_WRITE:
            reply = joule_pb2.StreamMessage()
            reply.identifyCirculatorReply.name = "ChefSteps"
            cs_client._resolve_pending_reply("identifyCirculatorReply", reply)

    cs_mock.write_gatt_char.side_effect = cs_fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=cs_mock),
    ):
        await cs_client.connect(auto_start_feed=False)
        await cs_client.identify()

    # Find the stream write call
    stream_writes = [w for w in cs_writes if w[0] == UUID_CHEFSTEP_STREAM_WRITE]
    assert len(stream_writes) == 1
    # ChefSteps uses response=True (Android WRITE_TYPE_DEFAULT on 700b4322)
    assert stream_writes[0][1] is True

    # Test Breville
    br_device = BLEDevice("66:55:44:33:22:11", "Joule Turbo", {})
    br_client = JouleClient(br_device)
    br_mock = create_mock_bleak_client("breville")

    br_writes = []

    async def br_fake_write(char, data, response=False):
        br_writes.append((char.uuid, response))
        if char.uuid == UUID_BREVILLE_APP_MESSAGE:
            reply = joule_pb2.StreamMessage()
            reply.identifyCirculatorReply.name = "Turbo"
            br_client._resolve_pending_reply("identifyCirculatorReply", reply)

    br_mock.write_gatt_char.side_effect = br_fake_write

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=br_mock),
    ):
        await br_client.connect(auto_start_feed=False)
        await br_client.identify()

    br_stream_writes = [w for w in br_writes if w[0] == UUID_BREVILLE_APP_MESSAGE]
    assert len(br_stream_writes) == 1
    # Must be response=True for Breville!
    assert br_stream_writes[0][1] is True
