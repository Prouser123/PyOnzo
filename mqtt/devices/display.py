from mqtt.devices.base import MQTTDevice
from onzo.devices.display import Display

class DisplayDevice(MQTTDevice):
    def __init__(self, display: Display):
        self._display = display
        self.connections = [["usb-hid", "onzo0"]]
        self.identifiers = [f"onzo_display-v{self._display.get_hardware_version()}_{self._display.get_serial()}"]
        self.manufacturer = "Onzo"
        self.model = f"Smart Energy Kit - Display (v{self._display.get_hardware_version()})"
        self.name = "onzo.display"
        self.sw_version = str(self._display.get_firmware_version())