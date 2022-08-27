from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.display import DisplayDevice
from mqtt.homeassistant.display_entity import DisplayEntity

class StandingChargeEntity(DisplayEntity):
    _update_interval = 600 # 10m
    _entity_mqtt_name = "standing_charge"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, display: DisplayDevice):
        self.device_class = "monetary"
        self.name = "onzo.display.standing_charge"
        self.unique_id = f"{display.identifiers[0]}_standing_charge"
        self.state_topic = self.construct_onzo_mqtt_topic("standing_charge")
        self.value_template = "{{ value_json['pence'] }}"
        self.unit_of_measurement = "p"

        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler, display)
    
    def get(self):
        reading = self._display_device._display.get_register(self._display_device._display.registers.STANDING_CHARGE)
        # Example reading: "4123" -> "41.23p"
        return {
            "pence": int(reading) / 100
        }