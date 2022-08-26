from enum import Enum
from onzo.internal.connection import Connection
from onzo.internal.enums import NetworkID
from onzo.internal.device import Device
from onzo.internal.register import Register

class Registers(Register):
    TYPE = 0
    FIRMWARE_VERSION = 1

    SERIAL_LOW = 2
    SERIAL_HIGH = 3
    SERIAL = [SERIAL_LOW, SERIAL_HIGH]

    STATUS = 4
    POWER = 5
    READING_INTERVAL = 6
    SENDING_INTERVAL = 7

    TIMESTAMP_LOW = 8
    TIMESTAMP_HIGH = 9
    TIMESTAMP = [TIMESTAMP_LOW, TIMESTAMP_HIGH]

    VOLTAGE = 10
    CAL_PHASE_0 = 11
    CAL_GAIN_0 = 12
    TEMPERATURE = 13
    POWER_VARS = 14
    RSSI = 15
    
    # TODO: What does EAR stand for?
    EAR_LOW = 16
    EAR_HIGH = 17
    EAR = [EAR_LOW, EAR_HIGH]

    BATTERY_VOLTAGE = 18
    TX_POWER = 19
    INST_WATT = 23
    INST_VAR = 24
    CAL_GAIN_1 = 25
    CAL_GAIN_2 = 26
    TX_PERIOD_LIMITS = 27
    CAL_GAIN_3 = 28
    CAL_GAIN_4 = 29




class Clamp(Device):
    registers = Registers
    network_id = NetworkID.CLAMP

    # Static variables (reg. values will never change)
    __firmware_version: str
    __serial: str

    def __init__(self, connection: Connection):
        super().__init__(connection)

        self.__firmware_version = self.get_register(self.registers.FIRMWARE_VERSION)
        self.__serial = self.get_register(self.registers.SERIAL)

    #region Static variable getters
    def get_firmware_version(self):
        return self.__firmware_version
    
    def get_serial(self):
        return self.__serial
    #endregion

"""     
    def get_cumulative_kwh(self):
        EAR = self.get_EAR()
        return EAR/10000 
"""
