from mqtt.devices.display import DisplayDevice

import json


class TemperatureEntity:
    def __init__(self, display: DisplayDevice):
        self.device = display.__dict__
        self.device_class = "temperature"
        self.name = "onzo.display.temperature"
        self.unique_id = f"{display.identifiers[0]}_temperature"
        self.state_topic = "onzo/display/temperature"
        self.value_template = "{{ value_json['state'] }}"

    def get_json(self):
        return json.dumps(self.__dict__)