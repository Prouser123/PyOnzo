from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.display import DisplayDevice
from mqtt.homeassistant.entity import Entity


class DisplayEntity(Entity):
    _device_type = "display"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, display: DisplayDevice):
        self._display_device = display
        self.device = self._display_device.__dict__
        
        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler)
    
