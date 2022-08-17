from enum import Enum, IntEnum

class NetworkID(IntEnum):
    CLAMP = 1
    DISPLAY = 2


class RequestType(IntEnum):
    GET_REGISTER = 1
    SET_REGISTER = 2
    GET_BULK_DATA = 3
    GET_NETWORK_LIST = 4
    CMD_RESET = 5
    WRITE_BULK_DATA = 6
    LDM_COMMAND = 160


class ResponseType(IntEnum):
    GET_REGISTER = 1
    SET_REGISTER = 2
    GET_BULK_DATA = 3
    GET_NETWORK_LIST = 4
    LDM_COMMAND = 160
    ERROR = 240
    END_OF_TRANSFER = 241


class StreamType(Enum):
    ENERGY_HIGH_RES = 'E'
    ENERGY_LOW_RES = 'e'
    POWER_REAL_FINE = 'P'
    POWER_REAL_STANDARD = 'p'
    POWER_REACTIVE_FINE = 'Q'
    POWER_REACTIVE_STANDARD = 'q'