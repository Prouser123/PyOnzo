from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.clamp import ClampDevice
from mqtt.homeassistant.entity import Entity


class ClampEntity(Entity):
    _device_type = "clamp"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, clamp: ClampDevice):
        self._clamp_device = clamp
        self.device = self._clamp_device.__dict__
        
        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler)
    
