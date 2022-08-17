from onzo.internal.enums import NetworkID
from onzo.internal.device import Device

class Display(Device):
    network_id = NetworkID.DISPLAY
    registers = {
         'min': [1],
         'hour': [2],
         'day': [3],
         'month': [4],
         'year': [5],
         # BULK DATA LIVES HERE
         'synched': [33],
         'version': [45],
         'hardware': [46],
         'configured': [83],
         'standingcharge': [129, 130],
         'unitcost': [131, 132],
         'EAC': [133, 134],
         'gridweekstart': [176],
         'gridweekstop': [177],
         'gridweekendstart': [178],
         'gridweekendstop': [179],
         'serial': [185, 186],
         'country': [187],
         'temp-offset': [192],
         'temp-gain': [193],
         'target': [222, 223],
         'cost0': [224],
         'cost1': [225],
         'cost2': [226],
         'cost3': [227],
         'start0': [228],
         'start1': [229],
         'start2': [230],
         'start3': [231],
    }

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
