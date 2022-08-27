from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.clamp import ClampDevice
from mqtt.homeassistant.clamp_entity import ClampEntity

class RealPowerEntity(ClampEntity):
    _update_interval = 5 # every 5s
    _entity_mqtt_name = "real_power"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, clamp: ClampDevice):
        self.device_class = "power"
        self.name = "onzo.clamp.real_power"
        self.unique_id = f"{clamp.identifiers[0]}_real_power"
        self.state_topic = self.construct_onzo_mqtt_topic("real_power")
        self.value_template = "{{ value_json['watts'] }}"

        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler, clamp)
    
    def get(self):
        return {
            "watts": self._clamp_device._clamp.get_register(self._clamp_device._clamp.registers.POWER)
        }