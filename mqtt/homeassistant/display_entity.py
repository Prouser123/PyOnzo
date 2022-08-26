from paho.mqtt.client import Client
from mqtt.devices.display import DisplayDevice

from mqtt.homeassistant.entity import Entity


class DisplayEntity(Entity):
    _device_type = "display"

    def __init__(self, client: Client, display: DisplayDevice):
        self.__display_device = display
        self.device = self.__display_device.__dict__
        
        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client)
    
