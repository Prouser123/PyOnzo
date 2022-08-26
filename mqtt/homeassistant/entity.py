from sre_constants import NOT_LITERAL
from paho.mqtt.client import Client

import json

from mqtt.devices.display import DisplayDevice
from onzo.devices.display import Display
from onzo.internal.device import Device

class Entity:

    _device_type: str = "unknown"
    _entity_mqtt_name: str = "unknown"
    _update_interval: int

    device: None
    device_class: str
    name: str
    unique_id: str
    state_topic: str
    value_template: str

    def __init__(self, client: Client):
        self.__client = client

        # Publish entity information to home assistant.
        #self.__client.publish(
        #    self.construct_hass_mqtt_topic(f"{self.__entity_mqtt_name}/config"),
        #    self.serialize(),
        #    retain=True
        #)
        print(self.construct_hass_mqtt_topic(f"{self._entity_mqtt_name}/config"))
        #print(self.serialize())


    def construct_hass_mqtt_topic(self, suffix: str):
        return f"testing2/homeassistant/sensor/onzo_{self._device_type}/{suffix}"

    def construct_onzo_mqtt_topic(self, suffix: str):
        return f"testing2/onzo/{self._device_type}/{suffix}"

    def serialize(self):
        # Unfortunately json.dumps() includes values that are "null", so we need to remove these next!
        data = json.dumps(self.__dict__, default=self.__serialize_handler)
        return data


    def __serialize_handler(self, obj):
        if isinstance(obj, (Client, DisplayDevice, Device)):
            # Return none as these are unserializable 
            return None
        else:
            return obj.value
    
    def get(self) -> dict:
        raise NotImplementedError("Implemented in subclass.")