from enum import Enum
from onzo.internal.enums import NetworkID
from onzo.internal.device import Device
from onzo.internal.register import Register

class Registers(Register):
    DATE_MINUTE = 1
    DATE_HOUR = 2
    DATE_DAY = 3
    DATE_MONTH = 4
    DATE_YEAR = 5

    # Temperature register (src: https://bruce33.github.io/onzo_dumper/docs/www.navitron.org.uk-forum-topic-12168.html#:~:text=(Temperature%20is%20register%206%20by%20the%20way).)
    TEMPERATURE = 6

    SYNCHED = 33
    FIRMWARE_VERSION = 45
    HARDWARE_VERSION = 46
    CONFIGURED = 83

    STANDING_CHARGE_LOW = 129
    STANDING_CHARGE_HIGH = 130
    # response: 1234 (12.34p)
    STANDING_CHARGE = [STANDING_CHARGE_LOW, STANDING_CHARGE_HIGH]

    UNIT_COST_LOW = 131
    UNIT_COST_HIGH = 132
    # response: 1234 (12.34p)
    UNIT_COST = [UNIT_COST_LOW, UNIT_COST_HIGH]

    ESTIMATED_ANNUAL_CONSUPTION_LOW = 133
    ESTIMATED_ANNUAL_CONSUPTION_HIGH = 134
    ESTIMATED_ANNUAL_CONSUPTION = [ESTIMATED_ANNUAL_CONSUPTION_LOW, ESTIMATED_ANNUAL_CONSUPTION_HIGH]

    GRIDWATCH_WEEK_START = 176
    GRIDWATCH_WEEK_STOP = 177

    GRIDWATCH_WEEKEND_START = 178
    GRIDWATCH_WEEKEND_STOP = 179

    SERIAL_LOW = 185
    SERIAL_HIGH = 186
    SERIAL = [SERIAL_LOW, SERIAL_HIGH]

    # 2 possible values (will make enums for later)
    COUNTRY_CODE = 187

    TEMPERATURE_OFFSET = 192
    TEMPERATURE_GAIN = 193

    TARGET_LOW = 222
    TARGET_HIGH = 223
    TARGET = [TARGET_LOW, TARGET_HIGH]

    COST_0 = 224
    COST_1 = 225
    COST_2 = 226
    COST_3 = 227

    START_0 = 228
    START_1 = 229
    START_2 = 230
    START_3 = 231

class Display(Device):
    registers = Registers
    network_id = NetworkID.DISPLAY
    
    def set_spend_rates(self, standing_charge, rate):
        standing_charge = max(min(int(standing_charge * 10000 + 0.5), 65534), 0)
        rate = max(min(int(rate * 10000 + 0.5), 65534), 0)
        return [
            self.set_register(self.registers["standingcharge"][0], standing_charge),
            self.set_register(self.registers["standingcharge"][1], 0),
            self.set_register(self.registers["unitcost"][0], rate),
            self.set_register(self.registers["unitcost"][1], 0)
        ]

    def get_spend_rates(self):
        standing_charge = self.get_register(self.registers["standingcharge"][0])
        standing_charge /= 10000
        rate = self.get_register(self.registers["unitcost"][0])
        rate /= 10000
        return (standing_charge, rate)

    def set_estimated_annual_consumption(self, eac_value):
        eac_value = int(eac_value / 3600000)
        eac_hi = eac_value >> 16
        eac_lo = eac_value & 65535
        return [
            self.set_register(self.registers["EAC"][0], eac_lo),
            self.set_register(self.registers["EAC"][1], eac_hi),
            self.set_register(self.CONFIGURED, 1)
        ]

    def get_estimated_annual_consumption(self):
        eac_lo = self.get_register(self.registers["EAC"][0])
        eac_hi = self.get_register(self.registers["EAC"][1])
        eac_value = (eac_hi << 16 + eac_lo)
        return eac_value
