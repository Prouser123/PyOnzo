from mqtt.devices.display import DisplayDevice
from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp

import json

class ClampDevice:
    def __init__(self, clamp: Clamp, dispDevice: DisplayDevice):
        self.connections = [["onzo-rf", dispDevice.identifiers[0]]]
        self.identifiers = [f"onzo_clamp_{clamp.get_serial()}"]
        self.manufacturer = "Onzo"
        self.model = f"Smart Energy Kit - Clamp"
        self.name = "onzo.clamp"
        self.sw_version = str(clamp.get_firmware_version())
        self.via_device = dispDevice.identifiers[0]
    
    def get_json(self):
        return json.dumps(self.__dict__)