import json


class MQTTDevice:
    def get_json(self):
        return json.dumps(self.__dict__)