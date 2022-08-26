from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp
from onzo.devices.display import Display

import json

class DisplayDevice:
    def __init__(self, display: Display):
        self.connections = [["usb-hid", "onzo0"]]
        self.identifiers = [f"onzo_display-v{display.get_hardware_version()}_{display.get_serial()}"]
        self.manufacturer = "Onzo"
        self.model = f"Smart Energy Kit - Display (v{display.get_hardware_version()})"
        self.name = "onzo.display"
        self.sw_version = str(display.get_firmware_version())
    
    def get_json(self):
        return json.dumps(self.__dict__)