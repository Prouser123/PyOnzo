from mqtt.devices.base import MQTTDevice
from mqtt.devices.display import DisplayDevice
from onzo.devices.clamp import Clamp

class ClampDevice(MQTTDevice):
    def __init__(self, clamp: Clamp, dispDevice: DisplayDevice):
        self._clamp = clamp
        self.connections = [["onzo-rf", dispDevice.identifiers[0]]]
        self.identifiers = [f"onzo_clamp_{clamp.get_serial()}"]
        self.manufacturer = "Onzo"
        self.model = f"Smart Energy Kit - Clamp"
        self.name = "onzo.clamp"
        self.sw_version = str(clamp.get_firmware_version())
        self.via_device = dispDevice.identifiers[0]