"""Tests for JouleClient."""

from __future__ import annotations

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
    UUID_BREVILLE_APP_MESSAGE,
    UUID_BREVILLE_APPLIANCE_MESSAGE,
    UUID_BREVILLE_SERIAL_NUMBER,
    UUID_BREVILLE_SERVICE,
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
        notify_char.properties = ["notify"]

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
        await client.connect()
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
        await client.connect()
        assert client.is_connected
        assert client.device_info.model == JouleModel.JOULE_TURBO


@pytest.mark.asyncio
async def test_client_notification_updates_state():
    """Test receiving CirculatorDataPoint notifications."""
    device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    client = JouleClient(device)
    mock_bleak = create_mock_bleak_client("chefsteps")

    with patch(
        "joule_ble.client.establish_connection",
        AsyncMock(return_value=mock_bleak),
    ):
        await client.connect()

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
        await client.connect()

    # Intercept write_gatt_char to automatically simulate startProgramReply
    async def fake_write(char, data, response=False):
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.startProgramReply.result = joule_pb2.CS_SUCCESS
        # Deliver reply via notification handler
        raw = bytearray(reply_msg.SerializeToString())
        client._handle_notification(MagicMock(), raw)

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
        await client.connect()

    async def fake_write(char, data, response=False):
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.startProgramReply.result = joule_pb2.CS_ERROR_INVALID_STATE
        raw = bytearray(reply_msg.SerializeToString())
        client._handle_notification(MagicMock(), raw)

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
        await client.connect()

    async def fake_write(char, data, response=False):
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.stopCirculatorReply.result = joule_pb2.CS_SUCCESS
        raw = bytearray(reply_msg.SerializeToString())
        client._handle_notification(MagicMock(), raw)

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
        await client.connect()

    client._state.error_state = ErrorState.SOFT_ERROR
    client._state.low_water = True

    async def fake_write(char, data, response=False):
        reply_msg = joule_pb2.StreamMessage()
        reply_msg.clearErrorReply.result = joule_pb2.CS_SUCCESS
        raw = bytearray(reply_msg.SerializeToString())
        client._handle_notification(MagicMock(), raw)

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
        await client.connect()

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
        await client.connect()
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
        await client.connect()

    client.state.program_step = CookState.WAITING_FOR_FOOD

    async def reply_drop_food(char, data, response=False):
        msg = joule_pb2.StreamMessage()
        msg.dropFoodReply.result = joule_pb2.CS_SUCCESS
        raw = bytearray(msg.SerializeToString())
        client._handle_notification(MagicMock(), raw)

    mock_bleak.write_gatt_char.side_effect = reply_drop_food

    await client.drop_food()
    assert client.state.program_step == CookState.COOKING
