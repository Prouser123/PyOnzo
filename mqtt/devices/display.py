from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp
from onzo.devices.display import Display

import json

class DisplayDevice:
    def __init__(self, display: Display):
        self.__display = display
        self.connections = [["usb-hid", "onzo0"]]
        self.identifiers = [f"onzo_display-v{self.__display.get_hardware_version()}_{self.__display.get_serial()}"]
        self.manufacturer = "Onzo"
        self.model = f"Smart Energy Kit - Display (v{self.__display.get_hardware_version()})"
        self.name = "onzo.display"
        self.sw_version = str(self.__display.get_firmware_version())
    
    def get_json(self):
        return json.dumps(self.__dict__)