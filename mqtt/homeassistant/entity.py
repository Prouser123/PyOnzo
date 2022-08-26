from sre_constants import NOT_LITERAL
from paho.mqtt.client import Client

import json

from mqtt.devices.display import DisplayDevice
from onzo.devices.display import Display
from onzo.internal.device import Device

class Entity:
    # Filter these types when we serialize our entity classes
    __filter_types = (Client, DisplayDevice, Device)
    

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
        return json.dumps(self.__serialize_filter_dict(self.__dict__))

    # Based on https://stackoverflow.com/a/66127889
    def __serialize_filter_dict(self, _dict):
        """Delete values of a certain type recursively from all of the dictionaries"""
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                self.__serialize_filter_dict(value)
            elif isinstance(value, self.__filter_types):
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        self.__serialize_filter_dict(v_i)
        return _dict
    
    def get(self) -> dict:
        raise NotImplementedError("Implemented in subclass.")