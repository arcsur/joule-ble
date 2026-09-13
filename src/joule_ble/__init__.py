"""Joule Bluetooth Low Energy integration library."""

from __future__ import annotations

__version__ = "0.1.0a1"

from .client import JouleClient
from .const import (
    MAX_TEMP_C,
    MIN_TEMP_C,
    UUID_BREVILLE_SERVICE,
    UUID_CHEFSTEP_STREAM_SERVICE,
)
from .exceptions import (
    JouleAuthenticationError,
    JouleCommandError,
    JouleConnectionError,
    JouleError,
    JouleTimeoutError,
)
from .models import (
    CookState,
    ErrorState,
    EventReason,
    JouleAuthData,
    JouleDeviceInfo,
    JouleModel,
    JouleState,
    ProgramType,
    TurboCookState,
)
from .parser import JouleBluetoothDeviceData

__all__ = [
    "__version__",
    "JouleClient",
    "JouleBluetoothDeviceData",
    "JouleDeviceInfo",
    "JouleState",
    "JouleAuthData",
    "JouleModel",
    "CookState",
    "ProgramType",
    "ErrorState",
    "EventReason",
    "TurboCookState",
    "JouleError",
    "JouleConnectionError",
    "JouleAuthenticationError",
    "JouleCommandError",
    "JouleTimeoutError",
    "MIN_TEMP_C",
    "MAX_TEMP_C",
    "UUID_CHEFSTEP_STREAM_SERVICE",
    "UUID_BREVILLE_SERVICE",
]
