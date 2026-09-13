"""Data models and enums for Joule Bluetooth library."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from enum import Enum, StrEnum

from .proto import joule_pb2


class JouleModel(StrEnum):
    """Joule device hardware generation."""

    ORIGINAL_JOULE = "Original Joule"
    JOULE_TURBO = "Joule Turbo"
    UNKNOWN = "Unknown Joule"


class CookState(StrEnum):
    """Cooking lifecycle states mapped from ProgramStep."""

    IDLE = "idle"
    PRE_HEATING = "pre_heating"
    WAITING_FOR_FOOD = "waiting_for_food"
    COOKING = "cooking"
    WAITING_FOR_REMOVE_FOOD = "waiting_for_remove_food"
    ERROR = "error"
    WAIT_FOR_UPDATE = "wait_for_update"
    UNKNOWN = "unknown"

    @classmethod
    def from_proto(cls, step: int) -> CookState:
        """Convert a protobuf ProgramStep integer to CookState."""
        mapping: dict[int, CookState] = {
            int(joule_pb2.UNKNOWN): cls.UNKNOWN,
            int(joule_pb2.PRE_HEAT): cls.PRE_HEATING,
            int(joule_pb2.WAIT_FOR_FOOD): cls.WAITING_FOR_FOOD,
            int(joule_pb2.COOK): cls.COOKING,
            int(joule_pb2.WAIT_FOR_REMOVE_FOOD): cls.WAITING_FOR_REMOVE_FOOD,
            int(joule_pb2.ERROR): cls.ERROR,
            int(joule_pb2.WAIT_FOR_UPDATE): cls.WAIT_FOR_UPDATE,
        }
        return mapping.get(step, cls.UNKNOWN)


class ProgramType(StrEnum):
    """Program type."""

    MANUAL = "manual"
    AUTOMATIC = "automatic"

    @classmethod
    def from_proto(cls, val: int) -> ProgramType:
        """Convert proto ProgramType."""
        if val == joule_pb2.AUTOMATIC:
            return cls.AUTOMATIC
        return cls.MANUAL


class ErrorState(StrEnum):
    """Device error severity state."""

    NO_ERROR = "no_error"
    SOFT_ERROR = "soft_error"
    HARD_ERROR = "hard_error"

    @classmethod
    def from_proto(cls, val: int) -> ErrorState:
        """Convert proto ErrorState."""
        mapping: dict[int, ErrorState] = {
            int(joule_pb2.NO_ERROR): cls.NO_ERROR,
            int(joule_pb2.SOFT_ERROR): cls.SOFT_ERROR,
            int(joule_pb2.HARD_ERROR): cls.HARD_ERROR,
        }
        return mapping.get(val, cls.NO_ERROR)


class EventReason(Enum):
    """Event / fault reasons from Joule."""

    NO_REASON = joule_pb2.NO_REASON
    BUTTON_PRESSED = joule_pb2.BUTTON_PRESSED
    LOW_WATER_LEVEL = joule_pb2.LOW_WATER_LEVEL
    TIPPED_OVER = joule_pb2.TIPPED_OVER
    OVERHEATING = joule_pb2.OVERHEATING
    POWER_LOSS = joule_pb2.POWER_LOSS
    STUCK_MOTOR = joule_pb2.STUCK_MOTOR
    FIRMWARE_CRASH = joule_pb2.FIRMWARE_CRASH
    HEATER_THERMISTOR = joule_pb2.HEATER_THERMISTOR
    BATH_THERMISTOR = joule_pb2.BATH_THERMISTOR
    PRESSURE_SENSOR = joule_pb2.PRESSURE_SENSOR
    ACCELEROMETER = joule_pb2.ACCELEROMETER
    BAD_MOTOR = joule_pb2.BAD_MOTOR
    BAD_HEATER = joule_pb2.BAD_HEATER
    HARDWARE_FAILURE = joule_pb2.HARDWARE_FAILURE


class TurboCookState(StrEnum):
    """Turbo cooking mode state."""

    NO_TURBO = "no_turbo"
    TURBO_ENABLED = "turbo_enabled"
    TURBO_TIMED_OUT = "turbo_timed_out"

    @classmethod
    def from_proto(cls, val: int) -> TurboCookState:
        """Convert proto TurboCookState."""
        mapping: dict[int, TurboCookState] = {
            int(joule_pb2.NO_TURBO): cls.NO_TURBO,
            int(joule_pb2.TURBO_ENABLED): cls.TURBO_ENABLED,
            int(joule_pb2.TURBO_TIMED_OUT): cls.TURBO_TIMED_OUT,
        }
        return mapping.get(val, cls.NO_TURBO)


@dataclass
class JouleDeviceInfo:
    """Device identification information."""

    name: str = "Joule Sous Vide"
    model: JouleModel = JouleModel.UNKNOWN
    serial_number: str | None = None
    hardware_version: str | None = None
    firmware_version: str | None = None
    mac_address: str | None = None
    model_number: str | None = None


@dataclass
class JouleAuthData:
    """Authentication and pairing keys for Joule."""

    token: str | None = None
    secret: str | bytes | None = None


@dataclass
class JouleState:
    """Current live telemetry and operational state of the Joule."""

    connected: bool = False
    bath_temp_c: float | None = None
    target_temp_c: float | None = None
    heater_temp_c: float | None = None
    upper_board_temp_c: float | None = None
    lower_board_temp_c: float | None = None
    motor_rpm: int | None = None
    heater_pwm: float | None = None
    time_remaining_seconds: int | None = None
    cook_time_seconds: int | None = None
    program_step: CookState = CookState.IDLE
    error_state: ErrorState = ErrorState.NO_ERROR
    low_water: bool = False
    motor_fault: bool = False
    turbo_cook_state: TurboCookState = TurboCookState.NO_TURBO
    last_updated: float = field(default_factory=time.time)

    @property
    def is_cooking(self) -> bool:
        """Return True if currently active (heating, cooking, or waiting)."""
        return self.program_step in (
            CookState.PRE_HEATING,
            CookState.WAITING_FOR_FOOD,
            CookState.COOKING,
            CookState.WAITING_FOR_REMOVE_FOOD,
        )

    @property
    def is_heating(self) -> bool:
        """Return True if heater is actively warming water."""
        return self.program_step == CookState.PRE_HEATING

    @property
    def has_error(self) -> bool:
        """Return True if device is in an error condition."""
        return (
            self.error_state != ErrorState.NO_ERROR
            or self.low_water
            or self.motor_fault
            or self.program_step == CookState.ERROR
        )
