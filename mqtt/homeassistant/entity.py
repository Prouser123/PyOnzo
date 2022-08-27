import json

from paho.mqtt.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.base import MQTTDevice
from onzo.internal.device import Device

class Entity:
    # Filter these types when we serialize our entity classes
    __filter_types = (Client, MQTTDevice, Device)
    

    _device_type: str = "unknown"
    _entity_mqtt_name: str = "unknown"
    _update_interval: int

    device: None
    device_class: str
    name: str
    unique_id: str
    state_topic: str
    value_template: str

    def __init__(self, client: Client, scheduler: BackgroundScheduler):
        self.__client = client

        # Child classes' inits have already set the variables they want to serialize.
        # Now we can publish the homeassistant config topic!

        # Publish entity information to home assistant.
        self.__client.publish(
            self.construct_hass_mqtt_topic(f"{self._entity_mqtt_name}/config"),
            self.serialize(),
            retain=True
        )

        # If an update interval was configured, setup a scheduled job.
        if (self._update_interval):
            # Define a scheduled job to retrieve and publish sensor data
            @scheduler.scheduled_job("interval", seconds=self._update_interval)
            def publish():
                self.__client.publish(
                    self.construct_onzo_mqtt_topic(self._entity_mqtt_name),
                    json.dumps(self.get()) # Serialize the dict to JSON
                )
            # Run the job now (to get data immediately)
            publish()

    def construct_hass_mqtt_topic(self, suffix: str):
        return f"homeassistant/sensor/onzo_{self._device_type}/{suffix}"

    def construct_onzo_mqtt_topic(self, suffix: str):
        return f"onzo/{self._device_type}/{suffix}"

    def serialize(self):
        # The serialize handler returns None for any objects we don't want serialized.
        # Unfortunately, json.dumps includes Non values in it's response.
        data = json.dumps(self.__dict__, default=self.__serialize_handler)
        # To fix this, we will load the data (creating a copy), filter it, and export it again.
        # We cannot simply deep copy self.__dict__ itself as some objects in it cannot be picked, resulting in a TypeError.
        data = json.dumps(self.__dict_filter_remove_none(json.loads(data)))
        # Return the filtered and re-dumped data.
        return data
    
    def __serialize_handler(self, obj):
        if isinstance(obj, self.__filter_types):
            # Return none as these are unserializable
            # Unfortunately json.dumps will still show these
            return None
        else:
            return obj.value

    # Based on https://stackoverflow.com/a/66127889
    def __dict_filter_remove_none(self, _dict):
        """Delete values that are "None" recursively from all of the dictionaries"""
        for key, value in list(_dict.items()):
            if isinstance(value, dict):
                self.__dict_filter_remove_none(value)
            elif value is None:
                del _dict[key]
            elif isinstance(value, list):
                for v_i in value:
                    if isinstance(v_i, dict):
                        self.__dict_filter_remove_none(v_i)
        return _dict
    
    def get(self) -> dict:
        raise NotImplementedError("Implemented in subclass.")