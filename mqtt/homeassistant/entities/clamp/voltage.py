from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.clamp import ClampDevice
from mqtt.homeassistant.clamp_entity import ClampEntity

class BatteryVoltageEntity(ClampEntity):
    _update_interval = 600 # Update every 10 minutes
    _entity_mqtt_name = "battery_voltage"

    def __init__(self, client: Client, scheduler: BackgroundScheduler, clamp: ClampDevice):
        self.device_class = "voltage"
        self.name = "onzo.clamp.battery_voltage"
        self.unique_id = f"{clamp.identifiers[0]}_battery_voltage"
        self.state_topic = self.construct_onzo_mqtt_topic("battery_voltage")
        self.value_template = "{{ value_json['battery_volts'] }}"

        # Call init after we define the data we want to be serialized / published in Entity init
        super().__init__(client, scheduler, clamp)
    
    def get(self):
        reading = self._clamp_device._clamp.get_register(self._clamp_device._clamp.registers.BATTERY_VOLTAGE)
        # Example reading: "4123" -> "4.123V"
        return {
            "battery_volts": int(reading) / 1000
        }