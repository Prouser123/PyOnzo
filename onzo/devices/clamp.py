from onzo.internal.enums import NetworkID
from onzo.internal.device import Device

class Clamp(Device):
    network_id = NetworkID.CLAMP
    registers = {
        'type': [0],
        'version': [1],
        'serial': [2, 3],
        'status': [4],
        'power': [5],
        'readinginterval': [6],
        'sendinginterval': [7],
        'timestamp': [8, 9],
        'voltage': [10],
        'calphase0': [11],
        'calgain0': [12],
        'temperature': [13],
        'powervars': [14],
        'RSSI': [15],
        'EAR': [16, 17],
        'batteryvolts': [18],
        'txpower': [19],
        'instwatt': [23],
        'instvar': [24],
        'calgain1': [25],
        'calgain2': [26],
        'txperiodlimits': [27],
        'calgain3': [28],
        'calgain4': [29]
    }

    def get_cumulative_kwh(self):
        EAR = self.get_EAR()
        return EAR/10000
