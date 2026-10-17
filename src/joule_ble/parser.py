"""BLE advertisement parser for Joule devices."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from .const import (
    CHEFSTEPS_MANUFACTURER_ID,
    DEFAULT_RECIPIENT_ADDRESS,
    JOULE_SERVICE_UUIDS,
    UUID_BREVILLE_SERVICE,
    UUID_CHEFSTEP_STREAM_SERVICE,
)
from .models import JouleDeviceInfo, JouleModel

if TYPE_CHECKING:
    from bleak.backends.device import BLEDevice
    from bleak.backends.scanner import AdvertisementData

_LOGGER = logging.getLogger(__name__)


class JouleBluetoothDeviceData:
    """Parser for Joule BLE advertisements."""

    def __init__(self) -> None:
        """Initialize parser."""
        self._device_info: JouleDeviceInfo | None = None

    def supported(self, advertisement_data: AdvertisementData) -> bool:
        """Return True if the advertisement matches a known Joule device."""
        service_uuids = set(advertisement_data.service_uuids or [])
        if service_uuids.intersection(JOULE_SERVICE_UUIDS):
            return True

        if (
            advertisement_data.manufacturer_data
            and CHEFSTEPS_MANUFACTURER_ID in advertisement_data.manufacturer_data
        ):
            return True

        local_name = advertisement_data.local_name or ""
        return local_name.lower().startswith("joule")

    def update(
        self,
        ble_device: BLEDevice,
        advertisement_data: AdvertisementData,
    ) -> JouleDeviceInfo | None:
        """Parse advertisement data and update device info."""
        if not self.supported(advertisement_data):
            return None

        service_uuids = set(advertisement_data.service_uuids or [])
        local_name = advertisement_data.local_name or ble_device.name or "Joule"

        if UUID_BREVILLE_SERVICE in service_uuids or "turbo" in local_name.lower():
            model = JouleModel.JOULE_TURBO
        elif UUID_CHEFSTEP_STREAM_SERVICE in service_uuids:
            model = JouleModel.ORIGINAL_JOULE
        else:
            model = JouleModel.ORIGINAL_JOULE

        serial_number: str | None = None
        recipient_address: bytes | None = DEFAULT_RECIPIENT_ADDRESS
        # Check manufacturer data if available
        if advertisement_data.manufacturer_data:
            if CHEFSTEPS_MANUFACTURER_ID in advertisement_data.manufacturer_data:
                mfg = advertisement_data.manufacturer_data[CHEFSTEPS_MANUFACTURER_ID]
                if len(mfg) > 1:
                    # MakeRecipientAddress in official APK: raw bytes of mfg[1:]
                    recipient_address = bytes(mfg[1:])

            for _, data in advertisement_data.manufacturer_data.items():
                if len(data) >= 8:
                    try:
                        decoded = data.decode("utf-8", errors="ignore").strip()
                        if decoded.isprintable() and len(decoded) >= 8:
                            serial_number = decoded
                    except Exception:
                        pass

        self._device_info = JouleDeviceInfo(
            name=local_name,
            model=model,
            serial_number=serial_number,
            mac_address=ble_device.address,
            recipient_address=recipient_address,
        )
        return self._device_info

    @property
    def device_info(self) -> JouleDeviceInfo | None:
        """Return the current device info."""
        return self._device_info
