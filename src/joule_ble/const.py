"""Constants for Joule Bluetooth Low Energy communication."""

from __future__ import annotations

# ==============================================================================
# Original ChefSteps Joule (CS10001 / CS20001) GATT UUIDs
# ==============================================================================
UUID_CHEFSTEP_STREAM_SERVICE = "700b4321-9836-4383-a2b2-31a9098d1473"
UUID_CHEFSTEP_STREAM_WRITE = "700b4322-9836-4383-a2b2-31a9098d1473"
UUID_CHEFSTEP_STREAM_READ = "700b4323-9836-4383-a2b2-31a9098d1473"
UUID_CHEFSTEP_STREAM_SUBSCRIBE = "700b4325-9836-4383-a2b2-31a9098d1473"
UUID_CHEFSTEP_STREAM_FILE = "700b4326-9836-4383-a2b2-31a9098d1473"

# ==============================================================================
# Breville Joule Turbo (CS30001) FreeRTOS GATT UUIDs
# ==============================================================================
UUID_BREVILLE_SERVICE = "c6f2d9e3-49e7-4125-9014-bfc6d669ff00"
UUID_BREVILLE_SERIAL_NUMBER = "c6f2d9e3-49e7-4125-9014-bfc6d669ff01"
UUID_BREVILLE_WIFI_MAC_ADDRESS = "c6f2d9e3-49e7-4125-9014-bfc6d669ff02"
UUID_BREVILLE_PROXIMITY_STATE = "c6f2d9e3-49e7-4125-9014-bfc6d669ff05"
UUID_BREVILLE_ENDPOINT_INDEX = "c6f2d9e3-49e7-4125-9014-bfc6d669ff07"
UUID_BREVILLE_APPLIANCE_MESSAGE = "c6f2d9e3-49e7-4125-9014-bfc6d669ff08"
UUID_BREVILLE_APP_MESSAGE = "c6f2d9e3-49e7-4125-9014-bfc6d669ff09"
UUID_BREVILLE_LARGE_DATA_FROM_APPLIANCE = "c6f2d9e3-49e7-4125-9014-bfc6d669ff0a"
UUID_BREVILLE_LARGE_DATA_FROM_APP = "c6f2d9e3-49e7-4125-9014-bfc6d669ff0b"
UUID_BREVILLE_WIFI_CONNECTION_STATUS = "c6f2d9e3-49e7-4125-9014-bfc6d669ff0c"

# ==============================================================================
# Amazon FreeRTOS Device Information Service UUIDs
# ==============================================================================
UUID_DEVICE_INFORMATION_SERVICE = "8a7f1168-48af-4efb-83b5-e679f932ff00"
UUID_DEVICE_VERSION = "8a7f1168-48af-4efb-83b5-e679f932ff01"
UUID_IOT_ENDPOINT = "8a7f1168-48af-4efb-83b5-e679f932ff02"
UUID_DEVICE_MTU = "8a7f1168-48af-4efb-83b5-e679f932ff03"
UUID_DEVICE_PLATFORM = "8a7f1168-48af-4efb-83b5-e679f932ff04"
UUID_DEVICE_ID = "8a7f1168-48af-4efb-83b5-e679f932ff05"

# All recognized service UUIDs for scanning / detection
JOULE_SERVICE_UUIDS = {
    UUID_CHEFSTEP_STREAM_SERVICE,
    UUID_BREVILLE_SERVICE,
}

# Temperature limits in Celsius
MIN_TEMP_C = 20.0
MAX_TEMP_C = 99.0

# Timeouts in seconds
DEFAULT_COMMAND_TIMEOUT = 10.0
DEFAULT_CONNECT_TIMEOUT = 15.0
DEFAULT_PAIR_TIMEOUT = 30.0

# Default chunk MTU (fallback for ATT MTU 23 - 3 byte header)
DEFAULT_ATT_PAYLOAD_SIZE = 20
