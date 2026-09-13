from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UnavailableReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    RECIPIENT_OFFLINE: _ClassVar[UnavailableReason]
    UNAUTHORIZED_RECIPIENT: _ClassVar[UnavailableReason]

class Result(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    CS_SUCCESS: _ClassVar[Result]
    CS_ERROR_SVC_HANDLER_MISSING: _ClassVar[Result]
    CS_ERROR_SOFTDEVICE_NOT_ENABLED: _ClassVar[Result]
    CS_ERROR_INTERNAL: _ClassVar[Result]
    CS_ERROR_NO_MEM: _ClassVar[Result]
    CS_ERROR_NOT_FOUND: _ClassVar[Result]
    CS_ERROR_NOT_SUPPORTED: _ClassVar[Result]
    CS_ERROR_INVALID_PARAM: _ClassVar[Result]
    CS_ERROR_INVALID_STATE: _ClassVar[Result]
    CS_ERROR_INVALID_LENGTH: _ClassVar[Result]
    CS_ERROR_INVALID_FLAGS: _ClassVar[Result]
    CS_ERROR_INVALID_DATA: _ClassVar[Result]
    CS_ERROR_DATA_SIZE: _ClassVar[Result]
    CS_ERROR_TIMEOUT: _ClassVar[Result]
    CS_ERROR_NULL: _ClassVar[Result]
    CS_ERROR_FORBIDDEN: _ClassVar[Result]
    CS_ERROR_INVALID_ADDR: _ClassVar[Result]
    CS_ERROR_BUSY: _ClassVar[Result]
    CS_ERROR_IO_FAILED: _ClassVar[Result]
    CS_ERROR_ALREADY_EXISTS: _ClassVar[Result]
    CS_ERROR_END_OF_FILE: _ClassVar[Result]
    CS_ERROR_NOT_CONNECTED: _ClassVar[Result]
    CS_ERROR_UNKNOWN_RPC_MSG: _ClassVar[Result]
    CS_ERROR_WIFI_DUPLICATE_SCAN_RESULT: _ClassVar[Result]
    CS_ERROR_WIFI_KEY_ERROR: _ClassVar[Result]
    CS_ERROR_WIFI_INVALID_ROLE: _ClassVar[Result]
    CS_ERROR_WIFI_INVALID_SEC_TYPE: _ClassVar[Result]
    CS_ERROR_WIFI_INVALID_WEP_IND: _ClassVar[Result]
    CS_ERROR_WIFI_ALREADY_DISCONN: _ClassVar[Result]
    CS_ERROR_WIFI_NOT_CONN: _ClassVar[Result]
    CS_ERROR_WIFI_DISCONNECT: _ClassVar[Result]
    CS_ERROR_WIFI_INVALID_PWD: _ClassVar[Result]
    CS_ERROR_WIFI_RX_BUFF: _ClassVar[Result]
    CS_ERROR_WIFI_AP_TERM_CONN: _ClassVar[Result]
    CS_ERROR_INVALID_SOCKET: _ClassVar[Result]
    CS_ERROR_IO_IN_PROGRESS: _ClassVar[Result]
    CS_ERROR_GEN_SOCK_FAILURE: _ClassVar[Result]
    CS_ERROR_PLACEHOLDER_37: _ClassVar[Result]
    CS_ERROR_DNS_FAILURE: _ClassVar[Result]
    CS_ERROR_CONNECT_FAILURE: _ClassVar[Result]
    CS_ERROR_NO_DATA: _ClassVar[Result]
    CS_ERROR_EINVAL: _ClassVar[Result]
    CS_ERROR_SOCK_EWOULDBLOCK: _ClassVar[Result]
    CS_ERROR_SOCK_GEN_FAILURE: _ClassVar[Result]
    CS_ERROR_SOCK_ECLOSE: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_NOT_AUTHORIZED: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_UPGRADE_FAILURE: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_DATA_SIZE: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_PARSE_ERROR: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_BUFF_TOO_SMALL: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_NO_DATA: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_CONNECTION_CLOSING: _ClassVar[Result]
    CS_ERROR_WEB_SOCKET_UNHANDLED_OPCODE: _ClassVar[Result]
    CS_ERROR_SPI_INVALID_FRAME: _ClassVar[Result]
    CS_ERROR_SPI_NO_DATA: _ClassVar[Result]
    CS_ERROR_SPI_BUSY: _ClassVar[Result]
    CS_ERROR_SPI_QUEUE_FULL: _ClassVar[Result]
    CS_ERROR_QUEUE_WOULDBLOCK: _ClassVar[Result]
    CS_ERROR_STREAM_MESSAGE_DECODE: _ClassVar[Result]
    CS_ERROR_WIFI_IN_PROGRESS: _ClassVar[Result]
    CS_ERROR_TLS_FAILURE: _ClassVar[Result]
    CS_ERROR_TLS_INVALID_CERT: _ClassVar[Result]

class TurboCookState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_TURBO: _ClassVar[TurboCookState]
    TURBO_ENABLED: _ClassVar[TurboCookState]
    TURBO_TIMED_OUT: _ClassVar[TurboCookState]

class ProgramType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MANUAL: _ClassVar[ProgramType]
    AUTOMATIC: _ClassVar[ProgramType]

class ProgramStep(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    UNKNOWN: _ClassVar[ProgramStep]
    PRE_HEAT: _ClassVar[ProgramStep]
    WAIT_FOR_FOOD: _ClassVar[ProgramStep]
    COOK: _ClassVar[ProgramStep]
    WAIT_FOR_REMOVE_FOOD: _ClassVar[ProgramStep]
    ERROR: _ClassVar[ProgramStep]
    WAIT_FOR_UPDATE: _ClassVar[ProgramStep]

class ErrorState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_ERROR: _ClassVar[ErrorState]
    SOFT_ERROR: _ClassVar[ErrorState]
    HARD_ERROR: _ClassVar[ErrorState]

class LedColor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LED_COLOR_RED: _ClassVar[LedColor]
    LED_COLOR_GREEN: _ClassVar[LedColor]
    LED_COLOR_BLUE: _ClassVar[LedColor]
    LED_COLOR_WHITE: _ClassVar[LedColor]
    LED_COLOR_ORANGE: _ClassVar[LedColor]
    LED_COLOR_YELLOW: _ClassVar[LedColor]
    LED_COLOR_BLACK: _ClassVar[LedColor]
    LED_COLOR_PURPLE: _ClassVar[LedColor]

class LedPattern(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LED_PATTERN_BLINK: _ClassVar[LedPattern]
    LED_PATTERN_BREATHE: _ClassVar[LedPattern]
    LED_PATTERN_DOUBLE_BLINK: _ClassVar[LedPattern]
    LED_PATTERN_DOUBLE_PULSE: _ClassVar[LedPattern]
    LED_PATTERN_SOLID: _ClassVar[LedPattern]

class UpdateProgramType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    REGULAR: _ClassVar[UpdateProgramType]
    TURBO: _ClassVar[UpdateProgramType]

class EventType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_EVENT: _ClassVar[EventType]
    HW_FAILURE: _ClassVar[EventType]
    STOP_PROGRAM: _ClassVar[EventType]

class EventReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    NO_REASON: _ClassVar[EventReason]
    BUTTON_PRESSED: _ClassVar[EventReason]
    LOW_WATER_LEVEL: _ClassVar[EventReason]
    TIPPED_OVER: _ClassVar[EventReason]
    OVERHEATING: _ClassVar[EventReason]
    POWER_LOSS: _ClassVar[EventReason]
    STUCK_MOTOR: _ClassVar[EventReason]
    FIRMWARE_CRASH: _ClassVar[EventReason]
    HEATER_THERMISTOR: _ClassVar[EventReason]
    BATH_THERMISTOR: _ClassVar[EventReason]
    PRESSURE_SENSOR: _ClassVar[EventReason]
    ACCELEROMETER: _ClassVar[EventReason]
    BAD_MOTOR: _ClassVar[EventReason]
    BAD_HEATER: _ClassVar[EventReason]
    HARDWARE_FAILURE: _ClassVar[EventReason]

class FaultReason(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    HW_FAULT_TYPE_NONE: _ClassVar[FaultReason]
    HW_FAULT_TYPE_UNKNOWN: _ClassVar[FaultReason]
    HW_FAULT_TYPE_OFF: _ClassVar[FaultReason]
    HW_FAULT_TYPE_ARM_DOUBLE: _ClassVar[FaultReason]
    HW_FAULT_TYPE_NRF_WDT: _ClassVar[FaultReason]
    HW_FAULT_TYPE_NRF_PIN_RESET: _ClassVar[FaultReason]
    HW_FAULT_TYPE_ARM_HARD: _ClassVar[FaultReason]
    HW_FAULT_TYPE_NRF_WDT_TRAP: _ClassVar[FaultReason]
    HW_FAULT_TYPE_NRF_SD: _ClassVar[FaultReason]

class SecurityType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OPEN: _ClassVar[SecurityType]
    WEP: _ClassVar[SecurityType]
    WPA: _ClassVar[SecurityType]
    WPS: _ClassVar[SecurityType]
    UNKNOWN_WIFI: _ClassVar[SecurityType]
    WPA2: _ClassVar[SecurityType]
    WPA_WPA2: _ClassVar[SecurityType]

class WifiConnectionStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    WIFI_IDLE: _ClassVar[WifiConnectionStatus]
    WIFI_CONNECTING: _ClassVar[WifiConnectionStatus]
    WIFI_WRONG_PASSWORD: _ClassVar[WifiConnectionStatus]
    WIFI_NO_AP_FOUND: _ClassVar[WifiConnectionStatus]
    WIFI_CONNECT_FAIL: _ClassVar[WifiConnectionStatus]
    WIFI_GOT_IP: _ClassVar[WifiConnectionStatus]

class WifiDFUDownloadTFTPStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    API_ERROR: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED: _ClassVar[WifiDFUDownloadTFTPStatus]
    SUCCESS: _ClassVar[WifiDFUDownloadTFTPStatus]
    ONGOING: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_TIMEOUT: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_ROUTING: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_SHASUM: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_SLOT_ACTIVE: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_SLOT_FACTORY: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_SLOT_INVALID: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_BAD_IMAGE: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_BAD_ADDRESS: _ClassVar[WifiDFUDownloadTFTPStatus]
    FAILED_BUSY: _ClassVar[WifiDFUDownloadTFTPStatus]

class FeedType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    COOK_DATA: _ClassVar[FeedType]
    DEBUG: _ClassVar[FeedType]
    NETWORK_BLUETOOTH: _ClassVar[FeedType]
    NETWORK_WIFI: _ClassVar[FeedType]

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOG_DEBUG: _ClassVar[LogLevel]
    LOG_INFO: _ClassVar[LogLevel]
    LOG_WARNING: _ClassVar[LogLevel]
    LOG_ERROR: _ClassVar[LogLevel]
    LOG_FATAL: _ClassVar[LogLevel]

class BootModeType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    SOFTDEVICE_BOOT_MODE: _ClassVar[BootModeType]
    BOOTLOADER_BOOT_MODE: _ClassVar[BootModeType]
    APPLICATION_BOOT_MODE: _ClassVar[BootModeType]

class FileType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    APPLICATION_FIRMWARE: _ClassVar[FileType]
    SOFTDEVICE_FIRMWARE: _ClassVar[FileType]
    WIFI_FIRMWARE: _ClassVar[FileType]
    CERTIFICATE_FIRMWARE: _ClassVar[FileType]
    BOOTLOADER_FIRMWARE: _ClassVar[FileType]

class UsageMetric(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    MOTOR_RUNNING_MINS_LT: _ClassVar[UsageMetric]
    TOTAL_REVOLUTIONS: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_30C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_35C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_40C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_45C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_50C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_55C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_60C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_65C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_70C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_75C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_80C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_85C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_90C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_LT_95C: _ClassVar[UsageMetric]
    MOTOR_RUNNING_MINS_GT_95C: _ClassVar[UsageMetric]
    MOTOR_RPM_MEAN: _ClassVar[UsageMetric]
    MOTOR_RPM_VARIANCE: _ClassVar[UsageMetric]
    MOTOR_CURRENT_MEAN: _ClassVar[UsageMetric]
    MOTOR_CURRENT_VARIANCE: _ClassVar[UsageMetric]
    HEATER_MEAN: _ClassVar[UsageMetric]
    HEATER_VARIANCE: _ClassVar[UsageMetric]
    PRESSURE_MEAN: _ClassVar[UsageMetric]
    PRESSURE_VARIANCE: _ClassVar[UsageMetric]
    BATH_TEMP_MEAN: _ClassVar[UsageMetric]
    BATH_TEMP_VARIANCE: _ClassVar[UsageMetric]
    NUM_BUTTON_PRESSES: _ClassVar[UsageMetric]
    NUM_COOKS_INTERRUPTED: _ClassVar[UsageMetric]
    NUM_OOW_ERRORS: _ClassVar[UsageMetric]
    NUM_OVERTEMP_ERRORS: _ClassVar[UsageMetric]
    NUM_MOTOR_OVER_CURRENT_ERRORS: _ClassVar[UsageMetric]
    NUM_ACCELEROMETER_TRIPS: _ClassVar[UsageMetric]
    NUM_MOTOR_STALLS: _ClassVar[UsageMetric]

class JouleHardwareOptions(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    JOULE_HARDWARE_OPTIONS_STAINLESS: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_WHITE: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_ROSE_GOLD: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_230_VOLT: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_TYPE_G_PLUG: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_TYPE_CEE7_PLUG: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_TYPE_J_PLUG: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_UL_CERTIFIED: _ClassVar[JouleHardwareOptions]
    JOULE_HARDWARE_OPTIONS_CE_CERTIFIED: _ClassVar[JouleHardwareOptions]
RECIPIENT_OFFLINE: UnavailableReason
UNAUTHORIZED_RECIPIENT: UnavailableReason
CS_SUCCESS: Result
CS_ERROR_SVC_HANDLER_MISSING: Result
CS_ERROR_SOFTDEVICE_NOT_ENABLED: Result
CS_ERROR_INTERNAL: Result
CS_ERROR_NO_MEM: Result
CS_ERROR_NOT_FOUND: Result
CS_ERROR_NOT_SUPPORTED: Result
CS_ERROR_INVALID_PARAM: Result
CS_ERROR_INVALID_STATE: Result
CS_ERROR_INVALID_LENGTH: Result
CS_ERROR_INVALID_FLAGS: Result
CS_ERROR_INVALID_DATA: Result
CS_ERROR_DATA_SIZE: Result
CS_ERROR_TIMEOUT: Result
CS_ERROR_NULL: Result
CS_ERROR_FORBIDDEN: Result
CS_ERROR_INVALID_ADDR: Result
CS_ERROR_BUSY: Result
CS_ERROR_IO_FAILED: Result
CS_ERROR_ALREADY_EXISTS: Result
CS_ERROR_END_OF_FILE: Result
CS_ERROR_NOT_CONNECTED: Result
CS_ERROR_UNKNOWN_RPC_MSG: Result
CS_ERROR_WIFI_DUPLICATE_SCAN_RESULT: Result
CS_ERROR_WIFI_KEY_ERROR: Result
CS_ERROR_WIFI_INVALID_ROLE: Result
CS_ERROR_WIFI_INVALID_SEC_TYPE: Result
CS_ERROR_WIFI_INVALID_WEP_IND: Result
CS_ERROR_WIFI_ALREADY_DISCONN: Result
CS_ERROR_WIFI_NOT_CONN: Result
CS_ERROR_WIFI_DISCONNECT: Result
CS_ERROR_WIFI_INVALID_PWD: Result
CS_ERROR_WIFI_RX_BUFF: Result
CS_ERROR_WIFI_AP_TERM_CONN: Result
CS_ERROR_INVALID_SOCKET: Result
CS_ERROR_IO_IN_PROGRESS: Result
CS_ERROR_GEN_SOCK_FAILURE: Result
CS_ERROR_PLACEHOLDER_37: Result
CS_ERROR_DNS_FAILURE: Result
CS_ERROR_CONNECT_FAILURE: Result
CS_ERROR_NO_DATA: Result
CS_ERROR_EINVAL: Result
CS_ERROR_SOCK_EWOULDBLOCK: Result
CS_ERROR_SOCK_GEN_FAILURE: Result
CS_ERROR_SOCK_ECLOSE: Result
CS_ERROR_WEB_SOCKET_NOT_AUTHORIZED: Result
CS_ERROR_WEB_SOCKET_UPGRADE_FAILURE: Result
CS_ERROR_WEB_SOCKET_DATA_SIZE: Result
CS_ERROR_WEB_SOCKET_PARSE_ERROR: Result
CS_ERROR_WEB_SOCKET_BUFF_TOO_SMALL: Result
CS_ERROR_WEB_SOCKET_NO_DATA: Result
CS_ERROR_WEB_SOCKET_CONNECTION_CLOSING: Result
CS_ERROR_WEB_SOCKET_UNHANDLED_OPCODE: Result
CS_ERROR_SPI_INVALID_FRAME: Result
CS_ERROR_SPI_NO_DATA: Result
CS_ERROR_SPI_BUSY: Result
CS_ERROR_SPI_QUEUE_FULL: Result
CS_ERROR_QUEUE_WOULDBLOCK: Result
CS_ERROR_STREAM_MESSAGE_DECODE: Result
CS_ERROR_WIFI_IN_PROGRESS: Result
CS_ERROR_TLS_FAILURE: Result
CS_ERROR_TLS_INVALID_CERT: Result
NO_TURBO: TurboCookState
TURBO_ENABLED: TurboCookState
TURBO_TIMED_OUT: TurboCookState
MANUAL: ProgramType
AUTOMATIC: ProgramType
UNKNOWN: ProgramStep
PRE_HEAT: ProgramStep
WAIT_FOR_FOOD: ProgramStep
COOK: ProgramStep
WAIT_FOR_REMOVE_FOOD: ProgramStep
ERROR: ProgramStep
WAIT_FOR_UPDATE: ProgramStep
NO_ERROR: ErrorState
SOFT_ERROR: ErrorState
HARD_ERROR: ErrorState
LED_COLOR_RED: LedColor
LED_COLOR_GREEN: LedColor
LED_COLOR_BLUE: LedColor
LED_COLOR_WHITE: LedColor
LED_COLOR_ORANGE: LedColor
LED_COLOR_YELLOW: LedColor
LED_COLOR_BLACK: LedColor
LED_COLOR_PURPLE: LedColor
LED_PATTERN_BLINK: LedPattern
LED_PATTERN_BREATHE: LedPattern
LED_PATTERN_DOUBLE_BLINK: LedPattern
LED_PATTERN_DOUBLE_PULSE: LedPattern
LED_PATTERN_SOLID: LedPattern
REGULAR: UpdateProgramType
TURBO: UpdateProgramType
NO_EVENT: EventType
HW_FAILURE: EventType
STOP_PROGRAM: EventType
NO_REASON: EventReason
BUTTON_PRESSED: EventReason
LOW_WATER_LEVEL: EventReason
TIPPED_OVER: EventReason
OVERHEATING: EventReason
POWER_LOSS: EventReason
STUCK_MOTOR: EventReason
FIRMWARE_CRASH: EventReason
HEATER_THERMISTOR: EventReason
BATH_THERMISTOR: EventReason
PRESSURE_SENSOR: EventReason
ACCELEROMETER: EventReason
BAD_MOTOR: EventReason
BAD_HEATER: EventReason
HARDWARE_FAILURE: EventReason
HW_FAULT_TYPE_NONE: FaultReason
HW_FAULT_TYPE_UNKNOWN: FaultReason
HW_FAULT_TYPE_OFF: FaultReason
HW_FAULT_TYPE_ARM_DOUBLE: FaultReason
HW_FAULT_TYPE_NRF_WDT: FaultReason
HW_FAULT_TYPE_NRF_PIN_RESET: FaultReason
HW_FAULT_TYPE_ARM_HARD: FaultReason
HW_FAULT_TYPE_NRF_WDT_TRAP: FaultReason
HW_FAULT_TYPE_NRF_SD: FaultReason
OPEN: SecurityType
WEP: SecurityType
WPA: SecurityType
WPS: SecurityType
UNKNOWN_WIFI: SecurityType
WPA2: SecurityType
WPA_WPA2: SecurityType
WIFI_IDLE: WifiConnectionStatus
WIFI_CONNECTING: WifiConnectionStatus
WIFI_WRONG_PASSWORD: WifiConnectionStatus
WIFI_NO_AP_FOUND: WifiConnectionStatus
WIFI_CONNECT_FAIL: WifiConnectionStatus
WIFI_GOT_IP: WifiConnectionStatus
API_ERROR: WifiDFUDownloadTFTPStatus
FAILED: WifiDFUDownloadTFTPStatus
SUCCESS: WifiDFUDownloadTFTPStatus
ONGOING: WifiDFUDownloadTFTPStatus
FAILED_TIMEOUT: WifiDFUDownloadTFTPStatus
FAILED_ROUTING: WifiDFUDownloadTFTPStatus
FAILED_SHASUM: WifiDFUDownloadTFTPStatus
FAILED_SLOT_ACTIVE: WifiDFUDownloadTFTPStatus
FAILED_SLOT_FACTORY: WifiDFUDownloadTFTPStatus
FAILED_SLOT_INVALID: WifiDFUDownloadTFTPStatus
FAILED_BAD_IMAGE: WifiDFUDownloadTFTPStatus
FAILED_BAD_ADDRESS: WifiDFUDownloadTFTPStatus
FAILED_BUSY: WifiDFUDownloadTFTPStatus
COOK_DATA: FeedType
DEBUG: FeedType
NETWORK_BLUETOOTH: FeedType
NETWORK_WIFI: FeedType
LOG_DEBUG: LogLevel
LOG_INFO: LogLevel
LOG_WARNING: LogLevel
LOG_ERROR: LogLevel
LOG_FATAL: LogLevel
SOFTDEVICE_BOOT_MODE: BootModeType
BOOTLOADER_BOOT_MODE: BootModeType
APPLICATION_BOOT_MODE: BootModeType
APPLICATION_FIRMWARE: FileType
SOFTDEVICE_FIRMWARE: FileType
WIFI_FIRMWARE: FileType
CERTIFICATE_FIRMWARE: FileType
BOOTLOADER_FIRMWARE: FileType
MOTOR_RUNNING_MINS_LT: UsageMetric
TOTAL_REVOLUTIONS: UsageMetric
MOTOR_RUNNING_MINS_LT_30C: UsageMetric
MOTOR_RUNNING_MINS_LT_35C: UsageMetric
MOTOR_RUNNING_MINS_LT_40C: UsageMetric
MOTOR_RUNNING_MINS_LT_45C: UsageMetric
MOTOR_RUNNING_MINS_LT_50C: UsageMetric
MOTOR_RUNNING_MINS_LT_55C: UsageMetric
MOTOR_RUNNING_MINS_LT_60C: UsageMetric
MOTOR_RUNNING_MINS_LT_65C: UsageMetric
MOTOR_RUNNING_MINS_LT_70C: UsageMetric
MOTOR_RUNNING_MINS_LT_75C: UsageMetric
MOTOR_RUNNING_MINS_LT_80C: UsageMetric
MOTOR_RUNNING_MINS_LT_85C: UsageMetric
MOTOR_RUNNING_MINS_LT_90C: UsageMetric
MOTOR_RUNNING_MINS_LT_95C: UsageMetric
MOTOR_RUNNING_MINS_GT_95C: UsageMetric
MOTOR_RPM_MEAN: UsageMetric
MOTOR_RPM_VARIANCE: UsageMetric
MOTOR_CURRENT_MEAN: UsageMetric
MOTOR_CURRENT_VARIANCE: UsageMetric
HEATER_MEAN: UsageMetric
HEATER_VARIANCE: UsageMetric
PRESSURE_MEAN: UsageMetric
PRESSURE_VARIANCE: UsageMetric
BATH_TEMP_MEAN: UsageMetric
BATH_TEMP_VARIANCE: UsageMetric
NUM_BUTTON_PRESSES: UsageMetric
NUM_COOKS_INTERRUPTED: UsageMetric
NUM_OOW_ERRORS: UsageMetric
NUM_OVERTEMP_ERRORS: UsageMetric
NUM_MOTOR_OVER_CURRENT_ERRORS: UsageMetric
NUM_ACCELEROMETER_TRIPS: UsageMetric
NUM_MOTOR_STALLS: UsageMetric
JOULE_HARDWARE_OPTIONS_STAINLESS: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_WHITE: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_ROSE_GOLD: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_230_VOLT: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_TYPE_G_PLUG: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_TYPE_CEE7_PLUG: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_TYPE_J_PLUG: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_UL_CERTIFIED: JouleHardwareOptions
JOULE_HARDWARE_OPTIONS_CE_CERTIFIED: JouleHardwareOptions

class StreamMessage(_message.Message):
    __slots__ = ("handle", "end", "senderAddress", "recipientAddress", "noop", "unhandledMessageReply", "connectionReadyReply", "recipientUnavailableReply", "ping", "pong", "listStreamsRequest", "listStreamsReply", "listOperationsRequest", "listOperationsReply", "startProgramRequest", "startProgramReply", "updateProgramRequest", "updateProgramReply", "getCookEventsRequest", "getCookEventsReply", "stopCirculatorRequest", "stopCirculatorReply", "dropFoodRequest", "dropFoodReply", "beginLiveFeed", "beginLiveFeedReply", "keepAlive", "retransmitFeedRequest", "retransmitFeedReply", "circulatorDataPoint", "debugMessage", "listRecentEventsRequest", "listRecentEventsReply", "describeFeedRequest", "describeFeedReply", "listFeedsRequest", "listFeedsReply", "clearErrorRequest", "clearErrorReply", "listWifiRequest", "listWifiReply", "connectWifiRequest", "connectWifiReply", "listWifiProfileRequest", "listWifiProfileReply", "forgetWifiProfileRequest", "forgetWifiProfileReply", "enterBootModeRequest", "enterBootModeReply", "startFileTransferRequest", "startFileTransferReply", "transferFileBlockRequest", "transferFileBlockReply", "transferFileComplete", "startFileReceiveRequest", "startFileReceiveReply", "startKeyExchangeRequest", "startKeyExchangeReply", "cancelKeyExchangeRequest", "cancelKeyExchangeReply", "submitKeyRequest", "submitKeyReply", "submitBearerAuthTokenRequest", "submitBearerAuthTokenReply", "renameCirculatorRequest", "renameCirculatorReply", "identifyCirculatorRequest", "identifyCirculatorReply", "setMessagingAddressRequest", "setMessagingAddressReply", "displayLedRequest", "displayLedReply", "disconnectWifiRequest", "disconnectWifiReply", "wifiDFUStatusRequest", "wifiDFUStatusReply", "wifiDFUSetFirmware", "wifiDFUDownloadTFTPRequest", "wifiDFUDownloadTFTPResponse", "getLimitsRequest", "getLimitsReply", "buttonPressRequest", "buttonPressReply", "cancelButtonPressRequest", "cancelButtonPressReply", "factoryResetRequest", "factoryResetReply", "deviceRestartRequest", "deviceRestartReply", "testResetRequest", "testResetReply", "forgetDevicePairingRequest", "forgetDevicePairingReply", "setSimulatorRequest", "setSimulatorReply", "getSimulatorRequest", "getSimulatorReply", "setHardwareCoeffsRequest", "setHardwareCoeffsReply", "getHardwareCoeffsRequest", "getHardwareCoeffsReply", "getUsageDataRequest", "getUsageDataReply", "resetUsageDataRequest", "resetUsageDataReply", "getCrashDataRequest", "getCrashDataReply", "resetCrashDataRequest", "resetCrashDataReply")
    HANDLE_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    SENDERADDRESS_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTADDRESS_FIELD_NUMBER: _ClassVar[int]
    NOOP_FIELD_NUMBER: _ClassVar[int]
    UNHANDLEDMESSAGEREPLY_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONREADYREPLY_FIELD_NUMBER: _ClassVar[int]
    RECIPIENTUNAVAILABLEREPLY_FIELD_NUMBER: _ClassVar[int]
    PING_FIELD_NUMBER: _ClassVar[int]
    PONG_FIELD_NUMBER: _ClassVar[int]
    LISTSTREAMSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTSTREAMSREPLY_FIELD_NUMBER: _ClassVar[int]
    LISTOPERATIONSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTOPERATIONSREPLY_FIELD_NUMBER: _ClassVar[int]
    STARTPROGRAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    STARTPROGRAMREPLY_FIELD_NUMBER: _ClassVar[int]
    UPDATEPROGRAMREQUEST_FIELD_NUMBER: _ClassVar[int]
    UPDATEPROGRAMREPLY_FIELD_NUMBER: _ClassVar[int]
    GETCOOKEVENTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETCOOKEVENTSREPLY_FIELD_NUMBER: _ClassVar[int]
    STOPCIRCULATORREQUEST_FIELD_NUMBER: _ClassVar[int]
    STOPCIRCULATORREPLY_FIELD_NUMBER: _ClassVar[int]
    DROPFOODREQUEST_FIELD_NUMBER: _ClassVar[int]
    DROPFOODREPLY_FIELD_NUMBER: _ClassVar[int]
    BEGINLIVEFEED_FIELD_NUMBER: _ClassVar[int]
    BEGINLIVEFEEDREPLY_FIELD_NUMBER: _ClassVar[int]
    KEEPALIVE_FIELD_NUMBER: _ClassVar[int]
    RETRANSMITFEEDREQUEST_FIELD_NUMBER: _ClassVar[int]
    RETRANSMITFEEDREPLY_FIELD_NUMBER: _ClassVar[int]
    CIRCULATORDATAPOINT_FIELD_NUMBER: _ClassVar[int]
    DEBUGMESSAGE_FIELD_NUMBER: _ClassVar[int]
    LISTRECENTEVENTSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTRECENTEVENTSREPLY_FIELD_NUMBER: _ClassVar[int]
    DESCRIBEFEEDREQUEST_FIELD_NUMBER: _ClassVar[int]
    DESCRIBEFEEDREPLY_FIELD_NUMBER: _ClassVar[int]
    LISTFEEDSREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTFEEDSREPLY_FIELD_NUMBER: _ClassVar[int]
    CLEARERRORREQUEST_FIELD_NUMBER: _ClassVar[int]
    CLEARERRORREPLY_FIELD_NUMBER: _ClassVar[int]
    LISTWIFIREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTWIFIREPLY_FIELD_NUMBER: _ClassVar[int]
    CONNECTWIFIREQUEST_FIELD_NUMBER: _ClassVar[int]
    CONNECTWIFIREPLY_FIELD_NUMBER: _ClassVar[int]
    LISTWIFIPROFILEREQUEST_FIELD_NUMBER: _ClassVar[int]
    LISTWIFIPROFILEREPLY_FIELD_NUMBER: _ClassVar[int]
    FORGETWIFIPROFILEREQUEST_FIELD_NUMBER: _ClassVar[int]
    FORGETWIFIPROFILEREPLY_FIELD_NUMBER: _ClassVar[int]
    ENTERBOOTMODEREQUEST_FIELD_NUMBER: _ClassVar[int]
    ENTERBOOTMODEREPLY_FIELD_NUMBER: _ClassVar[int]
    STARTFILETRANSFERREQUEST_FIELD_NUMBER: _ClassVar[int]
    STARTFILETRANSFERREPLY_FIELD_NUMBER: _ClassVar[int]
    TRANSFERFILEBLOCKREQUEST_FIELD_NUMBER: _ClassVar[int]
    TRANSFERFILEBLOCKREPLY_FIELD_NUMBER: _ClassVar[int]
    TRANSFERFILECOMPLETE_FIELD_NUMBER: _ClassVar[int]
    STARTFILERECEIVEREQUEST_FIELD_NUMBER: _ClassVar[int]
    STARTFILERECEIVEREPLY_FIELD_NUMBER: _ClassVar[int]
    STARTKEYEXCHANGEREQUEST_FIELD_NUMBER: _ClassVar[int]
    STARTKEYEXCHANGEREPLY_FIELD_NUMBER: _ClassVar[int]
    CANCELKEYEXCHANGEREQUEST_FIELD_NUMBER: _ClassVar[int]
    CANCELKEYEXCHANGEREPLY_FIELD_NUMBER: _ClassVar[int]
    SUBMITKEYREQUEST_FIELD_NUMBER: _ClassVar[int]
    SUBMITKEYREPLY_FIELD_NUMBER: _ClassVar[int]
    SUBMITBEARERAUTHTOKENREQUEST_FIELD_NUMBER: _ClassVar[int]
    SUBMITBEARERAUTHTOKENREPLY_FIELD_NUMBER: _ClassVar[int]
    RENAMECIRCULATORREQUEST_FIELD_NUMBER: _ClassVar[int]
    RENAMECIRCULATORREPLY_FIELD_NUMBER: _ClassVar[int]
    IDENTIFYCIRCULATORREQUEST_FIELD_NUMBER: _ClassVar[int]
    IDENTIFYCIRCULATORREPLY_FIELD_NUMBER: _ClassVar[int]
    SETMESSAGINGADDRESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETMESSAGINGADDRESSREPLY_FIELD_NUMBER: _ClassVar[int]
    DISPLAYLEDREQUEST_FIELD_NUMBER: _ClassVar[int]
    DISPLAYLEDREPLY_FIELD_NUMBER: _ClassVar[int]
    DISCONNECTWIFIREQUEST_FIELD_NUMBER: _ClassVar[int]
    DISCONNECTWIFIREPLY_FIELD_NUMBER: _ClassVar[int]
    WIFIDFUSTATUSREQUEST_FIELD_NUMBER: _ClassVar[int]
    WIFIDFUSTATUSREPLY_FIELD_NUMBER: _ClassVar[int]
    WIFIDFUSETFIRMWARE_FIELD_NUMBER: _ClassVar[int]
    WIFIDFUDOWNLOADTFTPREQUEST_FIELD_NUMBER: _ClassVar[int]
    WIFIDFUDOWNLOADTFTPRESPONSE_FIELD_NUMBER: _ClassVar[int]
    GETLIMITSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETLIMITSREPLY_FIELD_NUMBER: _ClassVar[int]
    BUTTONPRESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    BUTTONPRESSREPLY_FIELD_NUMBER: _ClassVar[int]
    CANCELBUTTONPRESSREQUEST_FIELD_NUMBER: _ClassVar[int]
    CANCELBUTTONPRESSREPLY_FIELD_NUMBER: _ClassVar[int]
    FACTORYRESETREQUEST_FIELD_NUMBER: _ClassVar[int]
    FACTORYRESETREPLY_FIELD_NUMBER: _ClassVar[int]
    DEVICERESTARTREQUEST_FIELD_NUMBER: _ClassVar[int]
    DEVICERESTARTREPLY_FIELD_NUMBER: _ClassVar[int]
    TESTRESETREQUEST_FIELD_NUMBER: _ClassVar[int]
    TESTRESETREPLY_FIELD_NUMBER: _ClassVar[int]
    FORGETDEVICEPAIRINGREQUEST_FIELD_NUMBER: _ClassVar[int]
    FORGETDEVICEPAIRINGREPLY_FIELD_NUMBER: _ClassVar[int]
    SETSIMULATORREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETSIMULATORREPLY_FIELD_NUMBER: _ClassVar[int]
    GETSIMULATORREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETSIMULATORREPLY_FIELD_NUMBER: _ClassVar[int]
    SETHARDWARECOEFFSREQUEST_FIELD_NUMBER: _ClassVar[int]
    SETHARDWARECOEFFSREPLY_FIELD_NUMBER: _ClassVar[int]
    GETHARDWARECOEFFSREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETHARDWARECOEFFSREPLY_FIELD_NUMBER: _ClassVar[int]
    GETUSAGEDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETUSAGEDATAREPLY_FIELD_NUMBER: _ClassVar[int]
    RESETUSAGEDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESETUSAGEDATAREPLY_FIELD_NUMBER: _ClassVar[int]
    GETCRASHDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    GETCRASHDATAREPLY_FIELD_NUMBER: _ClassVar[int]
    RESETCRASHDATAREQUEST_FIELD_NUMBER: _ClassVar[int]
    RESETCRASHDATAREPLY_FIELD_NUMBER: _ClassVar[int]
    handle: int
    end: bool
    senderAddress: bytes
    recipientAddress: bytes
    noop: Noop
    unhandledMessageReply: UnhandledMessageReply
    connectionReadyReply: ConnectionReadyReply
    recipientUnavailableReply: RecipientUnavailableReply
    ping: Ping
    pong: Pong
    listStreamsRequest: ListStreamsRequest
    listStreamsReply: ListStreamsReply
    listOperationsRequest: ListOperationsRequest
    listOperationsReply: ListOperationsReply
    startProgramRequest: StartProgramRequest
    startProgramReply: StartProgramReply
    updateProgramRequest: UpdateProgramRequest
    updateProgramReply: UpdateProgramReply
    getCookEventsRequest: GetCookEventsRequest
    getCookEventsReply: GetCookEventsReply
    stopCirculatorRequest: StopCirculatorRequest
    stopCirculatorReply: StopCirculatorReply
    dropFoodRequest: DropFoodRequest
    dropFoodReply: DropFoodReply
    beginLiveFeed: BeginLiveFeed
    beginLiveFeedReply: BeginLiveFeedReply
    keepAlive: KeepAlive
    retransmitFeedRequest: RetransmitFeedRequest
    retransmitFeedReply: RetransmitFeedReply
    circulatorDataPoint: CirculatorDataPoint
    debugMessage: DebugMessage
    listRecentEventsRequest: ListRecentEventsRequest
    listRecentEventsReply: ListRecentEventsReply
    describeFeedRequest: DescribeFeedRequest
    describeFeedReply: DescribeFeedReply
    listFeedsRequest: ListFeedsRequest
    listFeedsReply: ListFeedsReply
    clearErrorRequest: ClearErrorRequest
    clearErrorReply: ClearErrorReply
    listWifiRequest: ListWifiRequest
    listWifiReply: ListWifiReply
    connectWifiRequest: ConnectWifiRequest
    connectWifiReply: ConnectWifiReply
    listWifiProfileRequest: ListWifiProfileRequest
    listWifiProfileReply: ListWifiProfileReply
    forgetWifiProfileRequest: ForgetWifiProfileRequest
    forgetWifiProfileReply: ForgetWifiProfileReply
    enterBootModeRequest: EnterBootModeRequest
    enterBootModeReply: EnterBootModeReply
    startFileTransferRequest: StartFileTransferRequest
    startFileTransferReply: StartFileTransferReply
    transferFileBlockRequest: TransferFileBlockRequest
    transferFileBlockReply: TransferFileBlockReply
    transferFileComplete: TransferFileComplete
    startFileReceiveRequest: StartFileReceiveRequest
    startFileReceiveReply: StartFileReceiveReply
    startKeyExchangeRequest: StartKeyExchangeRequest
    startKeyExchangeReply: StartKeyExchangeReply
    cancelKeyExchangeRequest: CancelKeyExchangeRequest
    cancelKeyExchangeReply: CancelKeyExchangeReply
    submitKeyRequest: SubmitKeyRequest
    submitKeyReply: SubmitKeyReply
    submitBearerAuthTokenRequest: SubmitBearerAuthTokenRequest
    submitBearerAuthTokenReply: SubmitBearerAuthTokenReply
    renameCirculatorRequest: RenameCirculatorRequest
    renameCirculatorReply: RenameCirculatorReply
    identifyCirculatorRequest: IdentifyCirculatorRequest
    identifyCirculatorReply: IdentifyCirculatorReply
    setMessagingAddressRequest: SetMessagingAddressRequest
    setMessagingAddressReply: SetMessagingAddressReply
    displayLedRequest: DisplayLedRequest
    displayLedReply: DisplayLedReply
    disconnectWifiRequest: DisconnectWifiRequest
    disconnectWifiReply: DisconnectWifiReply
    wifiDFUStatusRequest: WifiDFUStatusRequest
    wifiDFUStatusReply: WifiDFUStatusReply
    wifiDFUSetFirmware: WifiDFUSetFirmware
    wifiDFUDownloadTFTPRequest: WifiDFUDownloadTFTPRequest
    wifiDFUDownloadTFTPResponse: WifiDFUDownloadTFTPResponse
    getLimitsRequest: GetLimitsRequest
    getLimitsReply: GetLimitsReply
    buttonPressRequest: ButtonPressRequest
    buttonPressReply: ButtonPressReply
    cancelButtonPressRequest: CancelButtonPressRequest
    cancelButtonPressReply: CancelButtonPressReply
    factoryResetRequest: FactoryResetRequest
    factoryResetReply: FactoryResetReply
    deviceRestartRequest: DeviceRestartRequest
    deviceRestartReply: DeviceRestartReply
    testResetRequest: TestResetRequest
    testResetReply: TestResetReply
    forgetDevicePairingRequest: ForgetDevicePairingRequest
    forgetDevicePairingReply: ForgetDevicePairingReply
    setSimulatorRequest: SetSimulatorRequest
    setSimulatorReply: SetSimulatorReply
    getSimulatorRequest: GetSimulatorRequest
    getSimulatorReply: GetSimulatorReply
    setHardwareCoeffsRequest: SetHardwareCoeffsRequest
    setHardwareCoeffsReply: SetHardwareCoeffsReply
    getHardwareCoeffsRequest: GetHardwareCoeffsRequest
    getHardwareCoeffsReply: GetHardwareCoeffsReply
    getUsageDataRequest: GetUsageDataRequest
    getUsageDataReply: GetUsageDataReply
    resetUsageDataRequest: ResetUsageDataRequest
    resetUsageDataReply: ResetUsageDataReply
    getCrashDataRequest: GetCrashDataRequest
    getCrashDataReply: GetCrashDataReply
    resetCrashDataRequest: ResetCrashDataRequest
    resetCrashDataReply: ResetCrashDataReply
    def __init__(self, handle: _Optional[int] = ..., end: _Optional[bool] = ..., senderAddress: _Optional[bytes] = ..., recipientAddress: _Optional[bytes] = ..., noop: _Optional[_Union[Noop, _Mapping]] = ..., unhandledMessageReply: _Optional[_Union[UnhandledMessageReply, _Mapping]] = ..., connectionReadyReply: _Optional[_Union[ConnectionReadyReply, _Mapping]] = ..., recipientUnavailableReply: _Optional[_Union[RecipientUnavailableReply, _Mapping]] = ..., ping: _Optional[_Union[Ping, _Mapping]] = ..., pong: _Optional[_Union[Pong, _Mapping]] = ..., listStreamsRequest: _Optional[_Union[ListStreamsRequest, _Mapping]] = ..., listStreamsReply: _Optional[_Union[ListStreamsReply, _Mapping]] = ..., listOperationsRequest: _Optional[_Union[ListOperationsRequest, _Mapping]] = ..., listOperationsReply: _Optional[_Union[ListOperationsReply, _Mapping]] = ..., startProgramRequest: _Optional[_Union[StartProgramRequest, _Mapping]] = ..., startProgramReply: _Optional[_Union[StartProgramReply, _Mapping]] = ..., updateProgramRequest: _Optional[_Union[UpdateProgramRequest, _Mapping]] = ..., updateProgramReply: _Optional[_Union[UpdateProgramReply, _Mapping]] = ..., getCookEventsRequest: _Optional[_Union[GetCookEventsRequest, _Mapping]] = ..., getCookEventsReply: _Optional[_Union[GetCookEventsReply, _Mapping]] = ..., stopCirculatorRequest: _Optional[_Union[StopCirculatorRequest, _Mapping]] = ..., stopCirculatorReply: _Optional[_Union[StopCirculatorReply, _Mapping]] = ..., dropFoodRequest: _Optional[_Union[DropFoodRequest, _Mapping]] = ..., dropFoodReply: _Optional[_Union[DropFoodReply, _Mapping]] = ..., beginLiveFeed: _Optional[_Union[BeginLiveFeed, _Mapping]] = ..., beginLiveFeedReply: _Optional[_Union[BeginLiveFeedReply, _Mapping]] = ..., keepAlive: _Optional[_Union[KeepAlive, _Mapping]] = ..., retransmitFeedRequest: _Optional[_Union[RetransmitFeedRequest, _Mapping]] = ..., retransmitFeedReply: _Optional[_Union[RetransmitFeedReply, _Mapping]] = ..., circulatorDataPoint: _Optional[_Union[CirculatorDataPoint, _Mapping]] = ..., debugMessage: _Optional[_Union[DebugMessage, _Mapping]] = ..., listRecentEventsRequest: _Optional[_Union[ListRecentEventsRequest, _Mapping]] = ..., listRecentEventsReply: _Optional[_Union[ListRecentEventsReply, _Mapping]] = ..., describeFeedRequest: _Optional[_Union[DescribeFeedRequest, _Mapping]] = ..., describeFeedReply: _Optional[_Union[DescribeFeedReply, _Mapping]] = ..., listFeedsRequest: _Optional[_Union[ListFeedsRequest, _Mapping]] = ..., listFeedsReply: _Optional[_Union[ListFeedsReply, _Mapping]] = ..., clearErrorRequest: _Optional[_Union[ClearErrorRequest, _Mapping]] = ..., clearErrorReply: _Optional[_Union[ClearErrorReply, _Mapping]] = ..., listWifiRequest: _Optional[_Union[ListWifiRequest, _Mapping]] = ..., listWifiReply: _Optional[_Union[ListWifiReply, _Mapping]] = ..., connectWifiRequest: _Optional[_Union[ConnectWifiRequest, _Mapping]] = ..., connectWifiReply: _Optional[_Union[ConnectWifiReply, _Mapping]] = ..., listWifiProfileRequest: _Optional[_Union[ListWifiProfileRequest, _Mapping]] = ..., listWifiProfileReply: _Optional[_Union[ListWifiProfileReply, _Mapping]] = ..., forgetWifiProfileRequest: _Optional[_Union[ForgetWifiProfileRequest, _Mapping]] = ..., forgetWifiProfileReply: _Optional[_Union[ForgetWifiProfileReply, _Mapping]] = ..., enterBootModeRequest: _Optional[_Union[EnterBootModeRequest, _Mapping]] = ..., enterBootModeReply: _Optional[_Union[EnterBootModeReply, _Mapping]] = ..., startFileTransferRequest: _Optional[_Union[StartFileTransferRequest, _Mapping]] = ..., startFileTransferReply: _Optional[_Union[StartFileTransferReply, _Mapping]] = ..., transferFileBlockRequest: _Optional[_Union[TransferFileBlockRequest, _Mapping]] = ..., transferFileBlockReply: _Optional[_Union[TransferFileBlockReply, _Mapping]] = ..., transferFileComplete: _Optional[_Union[TransferFileComplete, _Mapping]] = ..., startFileReceiveRequest: _Optional[_Union[StartFileReceiveRequest, _Mapping]] = ..., startFileReceiveReply: _Optional[_Union[StartFileReceiveReply, _Mapping]] = ..., startKeyExchangeRequest: _Optional[_Union[StartKeyExchangeRequest, _Mapping]] = ..., startKeyExchangeReply: _Optional[_Union[StartKeyExchangeReply, _Mapping]] = ..., cancelKeyExchangeRequest: _Optional[_Union[CancelKeyExchangeRequest, _Mapping]] = ..., cancelKeyExchangeReply: _Optional[_Union[CancelKeyExchangeReply, _Mapping]] = ..., submitKeyRequest: _Optional[_Union[SubmitKeyRequest, _Mapping]] = ..., submitKeyReply: _Optional[_Union[SubmitKeyReply, _Mapping]] = ..., submitBearerAuthTokenRequest: _Optional[_Union[SubmitBearerAuthTokenRequest, _Mapping]] = ..., submitBearerAuthTokenReply: _Optional[_Union[SubmitBearerAuthTokenReply, _Mapping]] = ..., renameCirculatorRequest: _Optional[_Union[RenameCirculatorRequest, _Mapping]] = ..., renameCirculatorReply: _Optional[_Union[RenameCirculatorReply, _Mapping]] = ..., identifyCirculatorRequest: _Optional[_Union[IdentifyCirculatorRequest, _Mapping]] = ..., identifyCirculatorReply: _Optional[_Union[IdentifyCirculatorReply, _Mapping]] = ..., setMessagingAddressRequest: _Optional[_Union[SetMessagingAddressRequest, _Mapping]] = ..., setMessagingAddressReply: _Optional[_Union[SetMessagingAddressReply, _Mapping]] = ..., displayLedRequest: _Optional[_Union[DisplayLedRequest, _Mapping]] = ..., displayLedReply: _Optional[_Union[DisplayLedReply, _Mapping]] = ..., disconnectWifiRequest: _Optional[_Union[DisconnectWifiRequest, _Mapping]] = ..., disconnectWifiReply: _Optional[_Union[DisconnectWifiReply, _Mapping]] = ..., wifiDFUStatusRequest: _Optional[_Union[WifiDFUStatusRequest, _Mapping]] = ..., wifiDFUStatusReply: _Optional[_Union[WifiDFUStatusReply, _Mapping]] = ..., wifiDFUSetFirmware: _Optional[_Union[WifiDFUSetFirmware, _Mapping]] = ..., wifiDFUDownloadTFTPRequest: _Optional[_Union[WifiDFUDownloadTFTPRequest, _Mapping]] = ..., wifiDFUDownloadTFTPResponse: _Optional[_Union[WifiDFUDownloadTFTPResponse, _Mapping]] = ..., getLimitsRequest: _Optional[_Union[GetLimitsRequest, _Mapping]] = ..., getLimitsReply: _Optional[_Union[GetLimitsReply, _Mapping]] = ..., buttonPressRequest: _Optional[_Union[ButtonPressRequest, _Mapping]] = ..., buttonPressReply: _Optional[_Union[ButtonPressReply, _Mapping]] = ..., cancelButtonPressRequest: _Optional[_Union[CancelButtonPressRequest, _Mapping]] = ..., cancelButtonPressReply: _Optional[_Union[CancelButtonPressReply, _Mapping]] = ..., factoryResetRequest: _Optional[_Union[FactoryResetRequest, _Mapping]] = ..., factoryResetReply: _Optional[_Union[FactoryResetReply, _Mapping]] = ..., deviceRestartRequest: _Optional[_Union[DeviceRestartRequest, _Mapping]] = ..., deviceRestartReply: _Optional[_Union[DeviceRestartReply, _Mapping]] = ..., testResetRequest: _Optional[_Union[TestResetRequest, _Mapping]] = ..., testResetReply: _Optional[_Union[TestResetReply, _Mapping]] = ..., forgetDevicePairingRequest: _Optional[_Union[ForgetDevicePairingRequest, _Mapping]] = ..., forgetDevicePairingReply: _Optional[_Union[ForgetDevicePairingReply, _Mapping]] = ..., setSimulatorRequest: _Optional[_Union[SetSimulatorRequest, _Mapping]] = ..., setSimulatorReply: _Optional[_Union[SetSimulatorReply, _Mapping]] = ..., getSimulatorRequest: _Optional[_Union[GetSimulatorRequest, _Mapping]] = ..., getSimulatorReply: _Optional[_Union[GetSimulatorReply, _Mapping]] = ..., setHardwareCoeffsRequest: _Optional[_Union[SetHardwareCoeffsRequest, _Mapping]] = ..., setHardwareCoeffsReply: _Optional[_Union[SetHardwareCoeffsReply, _Mapping]] = ..., getHardwareCoeffsRequest: _Optional[_Union[GetHardwareCoeffsRequest, _Mapping]] = ..., getHardwareCoeffsReply: _Optional[_Union[GetHardwareCoeffsReply, _Mapping]] = ..., getUsageDataRequest: _Optional[_Union[GetUsageDataRequest, _Mapping]] = ..., getUsageDataReply: _Optional[_Union[GetUsageDataReply, _Mapping]] = ..., resetUsageDataRequest: _Optional[_Union[ResetUsageDataRequest, _Mapping]] = ..., resetUsageDataReply: _Optional[_Union[ResetUsageDataReply, _Mapping]] = ..., getCrashDataRequest: _Optional[_Union[GetCrashDataRequest, _Mapping]] = ..., getCrashDataReply: _Optional[_Union[GetCrashDataReply, _Mapping]] = ..., resetCrashDataRequest: _Optional[_Union[ResetCrashDataRequest, _Mapping]] = ..., resetCrashDataReply: _Optional[_Union[ResetCrashDataReply, _Mapping]] = ...) -> None: ...

class UnhandledMessageReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ConnectionReadyReply(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class RecipientUnavailableReply(_message.Message):
    __slots__ = ("recipientAddress", "unavailableReason")
    RECIPIENTADDRESS_FIELD_NUMBER: _ClassVar[int]
    UNAVAILABLEREASON_FIELD_NUMBER: _ClassVar[int]
    recipientAddress: bytes
    unavailableReason: UnavailableReason
    def __init__(self, recipientAddress: _Optional[bytes] = ..., unavailableReason: _Optional[_Union[UnavailableReason, str]] = ...) -> None: ...

class ListStreamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListStreamsReply(_message.Message):
    __slots__ = ("encodedStreamMessage",)
    ENCODEDSTREAMMESSAGE_FIELD_NUMBER: _ClassVar[int]
    encodedStreamMessage: bytes
    def __init__(self, encodedStreamMessage: _Optional[bytes] = ...) -> None: ...

class ListOperationsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOperationsReply(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class IdentifyCirculatorRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class IdentifyCirculatorReply(_message.Message):
    __slots__ = ("name", "firmwareVersion", "hardwareVersion", "serialNumber", "bleMacAddress", "softdeviceVersion", "bootloaderVersion", "appFirmwareVersion", "espFirmwareVersion", "certificateVersion", "modelNumber", "apiVersion", "hardwareOptions", "buildDate", "pcbaRevision")
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREVERSION_FIELD_NUMBER: _ClassVar[int]
    HARDWAREVERSION_FIELD_NUMBER: _ClassVar[int]
    SERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    BLEMACADDRESS_FIELD_NUMBER: _ClassVar[int]
    SOFTDEVICEVERSION_FIELD_NUMBER: _ClassVar[int]
    BOOTLOADERVERSION_FIELD_NUMBER: _ClassVar[int]
    APPFIRMWAREVERSION_FIELD_NUMBER: _ClassVar[int]
    ESPFIRMWAREVERSION_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATEVERSION_FIELD_NUMBER: _ClassVar[int]
    MODELNUMBER_FIELD_NUMBER: _ClassVar[int]
    APIVERSION_FIELD_NUMBER: _ClassVar[int]
    HARDWAREOPTIONS_FIELD_NUMBER: _ClassVar[int]
    BUILDDATE_FIELD_NUMBER: _ClassVar[int]
    PCBAREVISION_FIELD_NUMBER: _ClassVar[int]
    name: str
    firmwareVersion: str
    hardwareVersion: str
    serialNumber: str
    bleMacAddress: str
    softdeviceVersion: str
    bootloaderVersion: str
    appFirmwareVersion: str
    espFirmwareVersion: str
    certificateVersion: str
    modelNumber: str
    apiVersion: int
    hardwareOptions: int
    buildDate: int
    pcbaRevision: str
    def __init__(self, name: _Optional[str] = ..., firmwareVersion: _Optional[str] = ..., hardwareVersion: _Optional[str] = ..., serialNumber: _Optional[str] = ..., bleMacAddress: _Optional[str] = ..., softdeviceVersion: _Optional[str] = ..., bootloaderVersion: _Optional[str] = ..., appFirmwareVersion: _Optional[str] = ..., espFirmwareVersion: _Optional[str] = ..., certificateVersion: _Optional[str] = ..., modelNumber: _Optional[str] = ..., apiVersion: _Optional[int] = ..., hardwareOptions: _Optional[int] = ..., buildDate: _Optional[int] = ..., pcbaRevision: _Optional[str] = ...) -> None: ...

class RenameCirculatorRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class RenameCirculatorReply(_message.Message):
    __slots__ = ("result", "name")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    result: Result
    name: str
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., name: _Optional[str] = ...) -> None: ...

class SetMessagingAddressRequest(_message.Message):
    __slots__ = ("address",)
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    def __init__(self, address: _Optional[bytes] = ...) -> None: ...

class SetMessagingAddressReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class DisplayLedRequest(_message.Message):
    __slots__ = ("ledColor", "ledPattern", "durationMilliseconds")
    LEDCOLOR_FIELD_NUMBER: _ClassVar[int]
    LEDPATTERN_FIELD_NUMBER: _ClassVar[int]
    DURATIONMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    ledColor: LedColor
    ledPattern: LedPattern
    durationMilliseconds: int
    def __init__(self, ledColor: _Optional[_Union[LedColor, str]] = ..., ledPattern: _Optional[_Union[LedPattern, str]] = ..., durationMilliseconds: _Optional[int] = ...) -> None: ...

class DisplayLedReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class ButtonPressRequest(_message.Message):
    __slots__ = ("ledColor", "ledPattern", "durationMilliseconds")
    LEDCOLOR_FIELD_NUMBER: _ClassVar[int]
    LEDPATTERN_FIELD_NUMBER: _ClassVar[int]
    DURATIONMILLISECONDS_FIELD_NUMBER: _ClassVar[int]
    ledColor: LedColor
    ledPattern: LedPattern
    durationMilliseconds: int
    def __init__(self, ledColor: _Optional[_Union[LedColor, str]] = ..., ledPattern: _Optional[_Union[LedPattern, str]] = ..., durationMilliseconds: _Optional[int] = ...) -> None: ...

class ButtonPressReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class CancelButtonPressRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelButtonPressReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class Noop(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Ping(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Pong(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class KeepAlive(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CirculatorProgram(_message.Message):
    __slots__ = ("setPoint", "cookTime", "delayedStart", "holdingTemperature", "programType", "programMetadata", "turboCookState", "thicknessMicrometers", "weightMilligrams")
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    COOKTIME_FIELD_NUMBER: _ClassVar[int]
    DELAYEDSTART_FIELD_NUMBER: _ClassVar[int]
    HOLDINGTEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    PROGRAMTYPE_FIELD_NUMBER: _ClassVar[int]
    PROGRAMMETADATA_FIELD_NUMBER: _ClassVar[int]
    TURBOCOOKSTATE_FIELD_NUMBER: _ClassVar[int]
    THICKNESSMICROMETERS_FIELD_NUMBER: _ClassVar[int]
    WEIGHTMILLIGRAMS_FIELD_NUMBER: _ClassVar[int]
    setPoint: float
    cookTime: int
    delayedStart: int
    holdingTemperature: float
    programType: ProgramType
    programMetadata: ProgramMetadata
    turboCookState: TurboCookState
    thicknessMicrometers: int
    weightMilligrams: int
    def __init__(self, setPoint: _Optional[float] = ..., cookTime: _Optional[int] = ..., delayedStart: _Optional[int] = ..., holdingTemperature: _Optional[float] = ..., programType: _Optional[_Union[ProgramType, str]] = ..., programMetadata: _Optional[_Union[ProgramMetadata, _Mapping]] = ..., turboCookState: _Optional[_Union[TurboCookState, str]] = ..., thicknessMicrometers: _Optional[int] = ..., weightMilligrams: _Optional[int] = ...) -> None: ...

class ProgramMetadata(_message.Message):
    __slots__ = ("guideId", "programId", "timerId", "cookId")
    GUIDEID_FIELD_NUMBER: _ClassVar[int]
    PROGRAMID_FIELD_NUMBER: _ClassVar[int]
    TIMERID_FIELD_NUMBER: _ClassVar[int]
    COOKID_FIELD_NUMBER: _ClassVar[int]
    guideId: str
    programId: str
    timerId: str
    cookId: str
    def __init__(self, guideId: _Optional[str] = ..., programId: _Optional[str] = ..., timerId: _Optional[str] = ..., cookId: _Optional[str] = ...) -> None: ...

class StartProgramRequest(_message.Message):
    __slots__ = ("circulatorProgram", "feedId", "sequenceNumber")
    CIRCULATORPROGRAM_FIELD_NUMBER: _ClassVar[int]
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    circulatorProgram: CirculatorProgram
    feedId: int
    sequenceNumber: int
    def __init__(self, circulatorProgram: _Optional[_Union[CirculatorProgram, _Mapping]] = ..., feedId: _Optional[int] = ..., sequenceNumber: _Optional[int] = ...) -> None: ...

class StartProgramReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class StopCirculatorRequest(_message.Message):
    __slots__ = ("feedId", "sequenceNumber")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    sequenceNumber: int
    def __init__(self, feedId: _Optional[int] = ..., sequenceNumber: _Optional[int] = ...) -> None: ...

class StopCirculatorReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class DropFoodRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DropFoodReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class UpdateProgramRequest(_message.Message):
    __slots__ = ("cookTime", "setPoint", "setPointTime", "updateProgramType")
    COOKTIME_FIELD_NUMBER: _ClassVar[int]
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    SETPOINTTIME_FIELD_NUMBER: _ClassVar[int]
    UPDATEPROGRAMTYPE_FIELD_NUMBER: _ClassVar[int]
    cookTime: int
    setPoint: float
    setPointTime: int
    updateProgramType: UpdateProgramType
    def __init__(self, cookTime: _Optional[int] = ..., setPoint: _Optional[float] = ..., setPointTime: _Optional[int] = ..., updateProgramType: _Optional[_Union[UpdateProgramType, str]] = ...) -> None: ...

class UpdateProgramReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class CookEvents(_message.Message):
    __slots__ = ("programStartedTimestamp", "dropFoodTimestamp", "setPointReachedTimestamp", "cookFinishedTimestamp")
    PROGRAMSTARTEDTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    DROPFOODTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SETPOINTREACHEDTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    COOKFINISHEDTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    programStartedTimestamp: int
    dropFoodTimestamp: int
    setPointReachedTimestamp: int
    cookFinishedTimestamp: int
    def __init__(self, programStartedTimestamp: _Optional[int] = ..., dropFoodTimestamp: _Optional[int] = ..., setPointReachedTimestamp: _Optional[int] = ..., cookFinishedTimestamp: _Optional[int] = ...) -> None: ...

class GetCookEventsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCookEventsReply(_message.Message):
    __slots__ = ("result", "cookEvents")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    COOKEVENTS_FIELD_NUMBER: _ClassVar[int]
    result: Result
    cookEvents: CookEvents
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., cookEvents: _Optional[_Union[CookEvents, _Mapping]] = ...) -> None: ...

class ListRecentEventsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListRecentEventsReply(_message.Message):
    __slots__ = ("eventType", "eventReason", "eventTimestamp", "feedId", "sequenceNumber", "faultType", "appLR", "appPC", "appSP", "nrfResetReason", "faultCount", "sdPC", "sdLn", "sdFn", "nrfGPregret")
    EVENTTYPE_FIELD_NUMBER: _ClassVar[int]
    EVENTREASON_FIELD_NUMBER: _ClassVar[int]
    EVENTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    FAULTTYPE_FIELD_NUMBER: _ClassVar[int]
    APPLR_FIELD_NUMBER: _ClassVar[int]
    APPPC_FIELD_NUMBER: _ClassVar[int]
    APPSP_FIELD_NUMBER: _ClassVar[int]
    NRFRESETREASON_FIELD_NUMBER: _ClassVar[int]
    FAULTCOUNT_FIELD_NUMBER: _ClassVar[int]
    SDPC_FIELD_NUMBER: _ClassVar[int]
    SDLN_FIELD_NUMBER: _ClassVar[int]
    SDFN_FIELD_NUMBER: _ClassVar[int]
    NRFGPREGRET_FIELD_NUMBER: _ClassVar[int]
    eventType: EventType
    eventReason: EventReason
    eventTimestamp: int
    feedId: int
    sequenceNumber: int
    faultType: FaultReason
    appLR: int
    appPC: int
    appSP: int
    nrfResetReason: int
    faultCount: int
    sdPC: int
    sdLn: int
    sdFn: str
    nrfGPregret: int
    def __init__(self, eventType: _Optional[_Union[EventType, str]] = ..., eventReason: _Optional[_Union[EventReason, str]] = ..., eventTimestamp: _Optional[int] = ..., feedId: _Optional[int] = ..., sequenceNumber: _Optional[int] = ..., faultType: _Optional[_Union[FaultReason, str]] = ..., appLR: _Optional[int] = ..., appPC: _Optional[int] = ..., appSP: _Optional[int] = ..., nrfResetReason: _Optional[int] = ..., faultCount: _Optional[int] = ..., sdPC: _Optional[int] = ..., sdLn: _Optional[int] = ..., sdFn: _Optional[str] = ..., nrfGPregret: _Optional[int] = ...) -> None: ...

class ClearErrorRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ClearErrorReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class ListWifiRequest(_message.Message):
    __slots__ = ("start",)
    START_FIELD_NUMBER: _ClassVar[int]
    start: bool
    def __init__(self, start: _Optional[bool] = ...) -> None: ...

class ListWifiReply(_message.Message):
    __slots__ = ("SSID", "securityType", "rssi")
    SSID_FIELD_NUMBER: _ClassVar[int]
    SECURITYTYPE_FIELD_NUMBER: _ClassVar[int]
    RSSI_FIELD_NUMBER: _ClassVar[int]
    SSID: str
    securityType: SecurityType
    rssi: int
    def __init__(self, SSID: _Optional[str] = ..., securityType: _Optional[_Union[SecurityType, str]] = ..., rssi: _Optional[int] = ...) -> None: ...

class ConnectWifiRequest(_message.Message):
    __slots__ = ("SSID", "passphrase", "securityType")
    SSID_FIELD_NUMBER: _ClassVar[int]
    PASSPHRASE_FIELD_NUMBER: _ClassVar[int]
    SECURITYTYPE_FIELD_NUMBER: _ClassVar[int]
    SSID: str
    passphrase: str
    securityType: SecurityType
    def __init__(self, SSID: _Optional[str] = ..., passphrase: _Optional[str] = ..., securityType: _Optional[_Union[SecurityType, str]] = ...) -> None: ...

class ConnectWifiReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class ListWifiProfileRequest(_message.Message):
    __slots__ = ("index",)
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ListWifiProfileReply(_message.Message):
    __slots__ = ("result", "SSID", "bearerTokenSet", "connectionStatus", "timeSinceLastPacketMS", "cloudStatus", "MACADDR")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SSID_FIELD_NUMBER: _ClassVar[int]
    BEARERTOKENSET_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONSTATUS_FIELD_NUMBER: _ClassVar[int]
    TIMESINCELASTPACKETMS_FIELD_NUMBER: _ClassVar[int]
    CLOUDSTATUS_FIELD_NUMBER: _ClassVar[int]
    MACADDR_FIELD_NUMBER: _ClassVar[int]
    result: Result
    SSID: str
    bearerTokenSet: bool
    connectionStatus: WifiConnectionStatus
    timeSinceLastPacketMS: int
    cloudStatus: int
    MACADDR: bytes
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., SSID: _Optional[str] = ..., bearerTokenSet: _Optional[bool] = ..., connectionStatus: _Optional[_Union[WifiConnectionStatus, str]] = ..., timeSinceLastPacketMS: _Optional[int] = ..., cloudStatus: _Optional[int] = ..., MACADDR: _Optional[bytes] = ...) -> None: ...

class ForgetWifiProfileRequest(_message.Message):
    __slots__ = ("index",)
    INDEX_FIELD_NUMBER: _ClassVar[int]
    index: int
    def __init__(self, index: _Optional[int] = ...) -> None: ...

class ForgetWifiProfileReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class DisconnectWifiRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DisconnectWifiReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class WifiDFUStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class WifiDFUSlotStatus(_message.Message):
    __slots__ = ("valid", "sha256")
    VALID_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    sha256: bytes
    def __init__(self, valid: _Optional[bool] = ..., sha256: _Optional[bytes] = ...) -> None: ...

class WifiDFUStatusReply(_message.Message):
    __slots__ = ("result", "running_slot", "slot")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    RUNNING_SLOT_FIELD_NUMBER: _ClassVar[int]
    SLOT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    running_slot: int
    slot: _containers.RepeatedCompositeFieldContainer[WifiDFUSlotStatus]
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., running_slot: _Optional[int] = ..., slot: _Optional[_Iterable[_Union[WifiDFUSlotStatus, _Mapping]]] = ...) -> None: ...

class WifiDFUSetFirmware(_message.Message):
    __slots__ = ("sha256", "doNotRestart")
    SHA256_FIELD_NUMBER: _ClassVar[int]
    DONOTRESTART_FIELD_NUMBER: _ClassVar[int]
    sha256: bytes
    doNotRestart: bool
    def __init__(self, sha256: _Optional[bytes] = ..., doNotRestart: _Optional[bool] = ...) -> None: ...

class WifiDFUDownloadTFTPRequest(_message.Message):
    __slots__ = ("host", "filename", "sha256", "useHTTP")
    HOST_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    SHA256_FIELD_NUMBER: _ClassVar[int]
    USEHTTP_FIELD_NUMBER: _ClassVar[int]
    host: str
    filename: str
    sha256: bytes
    useHTTP: bool
    def __init__(self, host: _Optional[str] = ..., filename: _Optional[str] = ..., sha256: _Optional[bytes] = ..., useHTTP: _Optional[bool] = ...) -> None: ...

class WifiDFUDownloadTFTPResponse(_message.Message):
    __slots__ = ("status", "bytes_read")
    STATUS_FIELD_NUMBER: _ClassVar[int]
    BYTES_READ_FIELD_NUMBER: _ClassVar[int]
    status: WifiDFUDownloadTFTPStatus
    bytes_read: int
    def __init__(self, status: _Optional[_Union[WifiDFUDownloadTFTPStatus, str]] = ..., bytes_read: _Optional[int] = ...) -> None: ...

class DescribeFeedRequest(_message.Message):
    __slots__ = ("feedId",)
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    def __init__(self, feedId: _Optional[int] = ...) -> None: ...

class DescribeFeedReply(_message.Message):
    __slots__ = ("feedId", "circulatorProgram", "result")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    CIRCULATORPROGRAM_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    circulatorProgram: CirculatorProgram
    result: Result
    def __init__(self, feedId: _Optional[int] = ..., circulatorProgram: _Optional[_Union[CirculatorProgram, _Mapping]] = ..., result: _Optional[_Union[Result, str]] = ...) -> None: ...

class ListFeedsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListFeedsReply(_message.Message):
    __slots__ = ("feedId", "feedType", "active", "result")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    FEEDTYPE_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    feedType: FeedType
    active: bool
    result: Result
    def __init__(self, feedId: _Optional[int] = ..., feedType: _Optional[_Union[FeedType, str]] = ..., active: _Optional[bool] = ..., result: _Optional[_Union[Result, str]] = ...) -> None: ...

class BeginLiveFeed(_message.Message):
    __slots__ = ("feedType",)
    FEEDTYPE_FIELD_NUMBER: _ClassVar[int]
    feedType: FeedType
    def __init__(self, feedType: _Optional[_Union[FeedType, str]] = ...) -> None: ...

class BeginLiveFeedReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class BeginLiveFeedError(_message.Message):
    __slots__ = ()
    class LiveFeedErrorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        NO_ACTIVE_FEED: _ClassVar[BeginLiveFeedError.LiveFeedErrorType]
    NO_ACTIVE_FEED: BeginLiveFeedError.LiveFeedErrorType
    def __init__(self) -> None: ...

class CirculatorDataPoint(_message.Message):
    __slots__ = ("feedId", "sequenceNumber", "timestamp", "errorState", "bathTemp", "programStep", "timeRemaining", "heaterTemp", "upperBoardTemp", "lowerBoardTemp", "motorRPM", "heaterPWM", "motorVoltage", "motorPWM", "motorCurrent", "pressure", "motorFaultFlag", "motorPeakCurrent", "cookStartTimestamp")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    ERRORSTATE_FIELD_NUMBER: _ClassVar[int]
    BATHTEMP_FIELD_NUMBER: _ClassVar[int]
    PROGRAMSTEP_FIELD_NUMBER: _ClassVar[int]
    TIMEREMAINING_FIELD_NUMBER: _ClassVar[int]
    HEATERTEMP_FIELD_NUMBER: _ClassVar[int]
    UPPERBOARDTEMP_FIELD_NUMBER: _ClassVar[int]
    LOWERBOARDTEMP_FIELD_NUMBER: _ClassVar[int]
    MOTORRPM_FIELD_NUMBER: _ClassVar[int]
    HEATERPWM_FIELD_NUMBER: _ClassVar[int]
    MOTORVOLTAGE_FIELD_NUMBER: _ClassVar[int]
    MOTORPWM_FIELD_NUMBER: _ClassVar[int]
    MOTORCURRENT_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_FIELD_NUMBER: _ClassVar[int]
    MOTORFAULTFLAG_FIELD_NUMBER: _ClassVar[int]
    MOTORPEAKCURRENT_FIELD_NUMBER: _ClassVar[int]
    COOKSTARTTIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    sequenceNumber: int
    timestamp: int
    errorState: ErrorState
    bathTemp: float
    programStep: ProgramStep
    timeRemaining: int
    heaterTemp: float
    upperBoardTemp: float
    lowerBoardTemp: float
    motorRPM: int
    heaterPWM: float
    motorVoltage: float
    motorPWM: float
    motorCurrent: float
    pressure: float
    motorFaultFlag: int
    motorPeakCurrent: float
    cookStartTimestamp: int
    def __init__(self, feedId: _Optional[int] = ..., sequenceNumber: _Optional[int] = ..., timestamp: _Optional[int] = ..., errorState: _Optional[_Union[ErrorState, str]] = ..., bathTemp: _Optional[float] = ..., programStep: _Optional[_Union[ProgramStep, str]] = ..., timeRemaining: _Optional[int] = ..., heaterTemp: _Optional[float] = ..., upperBoardTemp: _Optional[float] = ..., lowerBoardTemp: _Optional[float] = ..., motorRPM: _Optional[int] = ..., heaterPWM: _Optional[float] = ..., motorVoltage: _Optional[float] = ..., motorPWM: _Optional[float] = ..., motorCurrent: _Optional[float] = ..., pressure: _Optional[float] = ..., motorFaultFlag: _Optional[int] = ..., motorPeakCurrent: _Optional[float] = ..., cookStartTimestamp: _Optional[int] = ...) -> None: ...

class DebugMessage(_message.Message):
    __slots__ = ("feedId", "sequenceNumber", "timestamp", "logLevel", "source", "event", "message")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQUENCENUMBER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOGLEVEL_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    sequenceNumber: int
    timestamp: int
    logLevel: LogLevel
    source: str
    event: str
    message: str
    def __init__(self, feedId: _Optional[int] = ..., sequenceNumber: _Optional[int] = ..., timestamp: _Optional[int] = ..., logLevel: _Optional[_Union[LogLevel, str]] = ..., source: _Optional[str] = ..., event: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class RetransmitFeedRequest(_message.Message):
    __slots__ = ("feedId", "seqStart", "seqEnd")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQSTART_FIELD_NUMBER: _ClassVar[int]
    SEQEND_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    seqStart: int
    seqEnd: int
    def __init__(self, feedId: _Optional[int] = ..., seqStart: _Optional[int] = ..., seqEnd: _Optional[int] = ...) -> None: ...

class RetransmitFeedReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class StreamFeedReply(_message.Message):
    __slots__ = ("feedId", "seq", "setPoint", "bathTemp")
    FEEDID_FIELD_NUMBER: _ClassVar[int]
    SEQ_FIELD_NUMBER: _ClassVar[int]
    SETPOINT_FIELD_NUMBER: _ClassVar[int]
    BATHTEMP_FIELD_NUMBER: _ClassVar[int]
    feedId: int
    seq: int
    setPoint: float
    bathTemp: float
    def __init__(self, feedId: _Optional[int] = ..., seq: _Optional[int] = ..., setPoint: _Optional[float] = ..., bathTemp: _Optional[float] = ...) -> None: ...

class EnterBootModeRequest(_message.Message):
    __slots__ = ("bootModeType",)
    BOOTMODETYPE_FIELD_NUMBER: _ClassVar[int]
    bootModeType: BootModeType
    def __init__(self, bootModeType: _Optional[_Union[BootModeType, str]] = ...) -> None: ...

class EnterBootModeReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class StartFileTransferRequest(_message.Message):
    __slots__ = ("fileType", "blockCount", "byteCount", "checksum", "version")
    FILETYPE_FIELD_NUMBER: _ClassVar[int]
    BLOCKCOUNT_FIELD_NUMBER: _ClassVar[int]
    BYTECOUNT_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    fileType: FileType
    blockCount: int
    byteCount: int
    checksum: int
    version: str
    def __init__(self, fileType: _Optional[_Union[FileType, str]] = ..., blockCount: _Optional[int] = ..., byteCount: _Optional[int] = ..., checksum: _Optional[int] = ..., version: _Optional[str] = ...) -> None: ...

class StartFileTransferReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class StartFileReceiveRequest(_message.Message):
    __slots__ = ("fileType",)
    FILETYPE_FIELD_NUMBER: _ClassVar[int]
    fileType: FileType
    def __init__(self, fileType: _Optional[_Union[FileType, str]] = ...) -> None: ...

class StartFileReceiveReply(_message.Message):
    __slots__ = ("result", "blockCount", "byteCount", "checksum")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BLOCKCOUNT_FIELD_NUMBER: _ClassVar[int]
    BYTECOUNT_FIELD_NUMBER: _ClassVar[int]
    CHECKSUM_FIELD_NUMBER: _ClassVar[int]
    result: Result
    blockCount: int
    byteCount: int
    checksum: int
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., blockCount: _Optional[int] = ..., byteCount: _Optional[int] = ..., checksum: _Optional[int] = ...) -> None: ...

class TransferFileBlockRequest(_message.Message):
    __slots__ = ("blockIdx", "block")
    BLOCKIDX_FIELD_NUMBER: _ClassVar[int]
    BLOCK_FIELD_NUMBER: _ClassVar[int]
    blockIdx: int
    block: bytes
    def __init__(self, blockIdx: _Optional[int] = ..., block: _Optional[bytes] = ...) -> None: ...

class TransferFileBlockReply(_message.Message):
    __slots__ = ("result", "blockIdx")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    BLOCKIDX_FIELD_NUMBER: _ClassVar[int]
    result: Result
    blockIdx: int
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., blockIdx: _Optional[int] = ...) -> None: ...

class TransferFileComplete(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class StartKeyExchangeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class StartKeyExchangeReply(_message.Message):
    __slots__ = ("secretKey", "result")
    SECRETKEY_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    secretKey: bytes
    result: Result
    def __init__(self, secretKey: _Optional[bytes] = ..., result: _Optional[_Union[Result, str]] = ...) -> None: ...

class CancelKeyExchangeRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CancelKeyExchangeReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class SubmitKeyRequest(_message.Message):
    __slots__ = ("secretKey",)
    SECRETKEY_FIELD_NUMBER: _ClassVar[int]
    secretKey: bytes
    def __init__(self, secretKey: _Optional[bytes] = ...) -> None: ...

class SubmitKeyReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class SubmitBearerAuthTokenRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: str
    def __init__(self, token: _Optional[str] = ...) -> None: ...

class SubmitBearerAuthTokenReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class FactoryResetRequest(_message.Message):
    __slots__ = ("restart",)
    RESTART_FIELD_NUMBER: _ClassVar[int]
    restart: bool
    def __init__(self, restart: _Optional[bool] = ...) -> None: ...

class FactoryResetReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class DeviceRestartRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DeviceRestartReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class TestResetRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class TestResetReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class ForgetDevicePairingRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ForgetDevicePairingReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class SetSimulatorRequest(_message.Message):
    __slots__ = ("simulatorOn",)
    SIMULATORON_FIELD_NUMBER: _ClassVar[int]
    simulatorOn: bool
    def __init__(self, simulatorOn: _Optional[bool] = ...) -> None: ...

class SetSimulatorReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class GetSimulatorRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetSimulatorReply(_message.Message):
    __slots__ = ("simulatorOn",)
    SIMULATORON_FIELD_NUMBER: _ClassVar[int]
    simulatorOn: bool
    def __init__(self, simulatorOn: _Optional[bool] = ...) -> None: ...

class SetHardwareCoeffsRequest(_message.Message):
    __slots__ = ("tempAdcBias", "tempAdcScale", "tempRef", "tempCoeffA", "tempCoeffB", "tempCoeffC")
    TEMPADCBIAS_FIELD_NUMBER: _ClassVar[int]
    TEMPADCSCALE_FIELD_NUMBER: _ClassVar[int]
    TEMPREF_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFA_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFB_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFC_FIELD_NUMBER: _ClassVar[int]
    tempAdcBias: float
    tempAdcScale: float
    tempRef: float
    tempCoeffA: float
    tempCoeffB: float
    tempCoeffC: float
    def __init__(self, tempAdcBias: _Optional[float] = ..., tempAdcScale: _Optional[float] = ..., tempRef: _Optional[float] = ..., tempCoeffA: _Optional[float] = ..., tempCoeffB: _Optional[float] = ..., tempCoeffC: _Optional[float] = ...) -> None: ...

class SetHardwareCoeffsReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class GetHardwareCoeffsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetHardwareCoeffsReply(_message.Message):
    __slots__ = ("tempAdcBias", "tempAdcScale", "tempRef", "tempCoeffA", "tempCoeffB", "tempCoeffC", "result")
    TEMPADCBIAS_FIELD_NUMBER: _ClassVar[int]
    TEMPADCSCALE_FIELD_NUMBER: _ClassVar[int]
    TEMPREF_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFA_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFB_FIELD_NUMBER: _ClassVar[int]
    TEMPCOEFFC_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    tempAdcBias: float
    tempAdcScale: float
    tempRef: float
    tempCoeffA: float
    tempCoeffB: float
    tempCoeffC: float
    result: Result
    def __init__(self, tempAdcBias: _Optional[float] = ..., tempAdcScale: _Optional[float] = ..., tempRef: _Optional[float] = ..., tempCoeffA: _Optional[float] = ..., tempCoeffB: _Optional[float] = ..., tempCoeffC: _Optional[float] = ..., result: _Optional[_Union[Result, str]] = ...) -> None: ...

class UsageDataMetric(_message.Message):
    __slots__ = ("key", "value")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    key: UsageMetric
    value: MetricValue
    def __init__(self, key: _Optional[_Union[UsageMetric, str]] = ..., value: _Optional[_Union[MetricValue, _Mapping]] = ...) -> None: ...

class MetricValue(_message.Message):
    __slots__ = ("intValue", "floatValue")
    INTVALUE_FIELD_NUMBER: _ClassVar[int]
    FLOATVALUE_FIELD_NUMBER: _ClassVar[int]
    intValue: int
    floatValue: float
    def __init__(self, intValue: _Optional[int] = ..., floatValue: _Optional[float] = ...) -> None: ...

class GetUsageDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetUsageDataReply(_message.Message):
    __slots__ = ("result", "serialNumber", "metric")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    SERIALNUMBER_FIELD_NUMBER: _ClassVar[int]
    METRIC_FIELD_NUMBER: _ClassVar[int]
    result: Result
    serialNumber: str
    metric: UsageDataMetric
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., serialNumber: _Optional[str] = ..., metric: _Optional[_Union[UsageDataMetric, _Mapping]] = ...) -> None: ...

class ResetUsageDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetUsageDataReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class GetCrashDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetCrashDataReply(_message.Message):
    __slots__ = ("result", "firmwareVersion", "sameCrashCount", "data")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    FIRMWAREVERSION_FIELD_NUMBER: _ClassVar[int]
    SAMECRASHCOUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    result: Result
    firmwareVersion: str
    sameCrashCount: int
    data: bytes
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., firmwareVersion: _Optional[str] = ..., sameCrashCount: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class ResetCrashDataRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ResetCrashDataReply(_message.Message):
    __slots__ = ("result",)
    RESULT_FIELD_NUMBER: _ClassVar[int]
    result: Result
    def __init__(self, result: _Optional[_Union[Result, str]] = ...) -> None: ...

class GetLimitsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class GetLimitsReply(_message.Message):
    __slots__ = ("result", "maxTemp")
    RESULT_FIELD_NUMBER: _ClassVar[int]
    MAXTEMP_FIELD_NUMBER: _ClassVar[int]
    result: Result
    maxTemp: float
    def __init__(self, result: _Optional[_Union[Result, str]] = ..., maxTemp: _Optional[float] = ...) -> None: ...
