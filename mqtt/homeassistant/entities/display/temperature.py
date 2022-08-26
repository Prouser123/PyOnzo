from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.display import DisplayDevice
from mqtt.homeassistant.display_entity import DisplayEntity

class TemperatureEntity(DisplayEntity):
    _update_interval = 60
    _entity_mqtt_name = "temperature"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, display: DisplayDevice):
        self.device_class = "temperature"
        self.name = "onzo.display.temperature"
        self.unique_id = f"{display.identifiers[0]}_temperature"
        self.state_topic = self.construct_onzo_mqtt_topic("temperature")
        self.value_template = "{{ value_json['state'] }}"

        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler, display)
    
    def get(self):
        return {
            "state": self._display_device._display.get_register(self._display_device._display.registers.TEMPERATURE)
        }