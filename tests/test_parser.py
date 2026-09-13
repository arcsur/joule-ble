"""Tests for Joule advertisement parser."""

from bleak.backends.device import BLEDevice
from bleak.backends.scanner import AdvertisementData

from joule_ble.const import (
    UUID_BREVILLE_SERVICE,
    UUID_CHEFSTEP_STREAM_SERVICE,
)
from joule_ble.models import JouleModel
from joule_ble.parser import JouleBluetoothDeviceData


def test_parser_unsupported_device():
    """Test that unrelated BLE advertisements are ignored."""
    parser = JouleBluetoothDeviceData()
    ble_device = BLEDevice("AA:BB:CC:DD:EE:FF", "Random Sensor", {})
    adv_data = AdvertisementData(
        local_name="Random Sensor",
        manufacturer_data={},
        service_data={},
        service_uuids=["0000180f-0000-1000-8000-00805f9b34fb"],
        tx_power=0,
        rssi=-60,
        platform_data=(),
    )
    assert not parser.supported(adv_data)
    assert parser.update(ble_device, adv_data) is None


def test_parser_chefsteps_joule():
    """Test discovering an Original ChefSteps Joule by service UUID."""
    parser = JouleBluetoothDeviceData()
    ble_device = BLEDevice("11:22:33:44:55:66", "Joule 1234", {})
    adv_data = AdvertisementData(
        local_name="Joule 1234",
        manufacturer_data={},
        service_data={},
        service_uuids=[UUID_CHEFSTEP_STREAM_SERVICE],
        tx_power=0,
        rssi=-55,
        platform_data=(),
    )
    assert parser.supported(adv_data)
    info = parser.update(ble_device, adv_data)
    assert info is not None
    assert info.name == "Joule 1234"
    assert info.model == JouleModel.ORIGINAL_JOULE
    assert info.mac_address == "11:22:33:44:55:66"


def test_parser_breville_joule_turbo():
    """Test discovering a Breville Joule Turbo by service UUID."""
    parser = JouleBluetoothDeviceData()
    ble_device = BLEDevice("66:55:44:33:22:11", "Joule Turbo Kitchen", {})
    adv_data = AdvertisementData(
        local_name="Joule Turbo Kitchen",
        manufacturer_data={},
        service_data={},
        service_uuids=[UUID_BREVILLE_SERVICE],
        tx_power=0,
        rssi=-48,
        platform_data=(),
    )
    assert parser.supported(adv_data)
    info = parser.update(ble_device, adv_data)
    assert info is not None
    assert info.name == "Joule Turbo Kitchen"
    assert info.model == JouleModel.JOULE_TURBO


def test_parser_manufacturer_data():
    """Test extracting serial number from advertisement manufacturer data."""
    parser = JouleBluetoothDeviceData()
    ble_device = BLEDevice("11:22:33:44:55:66", "Joule", {})
    adv_data = AdvertisementData(
        local_name="Joule",
        manufacturer_data={0x03E0: b"CS100010099"},
        service_data={},
        service_uuids=[UUID_CHEFSTEP_STREAM_SERVICE],
        tx_power=0,
        rssi=-50,
        platform_data=(),
    )
    info = parser.update(ble_device, adv_data)
    assert info is not None
    assert info.serial_number == "CS100010099"
