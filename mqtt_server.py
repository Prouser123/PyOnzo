import os

import paho.mqtt.client as mqtt
from mqtt.devices.clamp import ClampDevice
from mqtt.devices.display import DisplayDevice
from mqtt.entities.display.temperature import TemperatureEntity

from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp
from onzo.devices.display import Display

username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
host = os.environ["HOST"]
port = int(os.environ["PORT"])

conn = Connection()
client = mqtt.Client()
try:
    # Connect to the display over USB
    conn.connect()
    display = Display(conn)
    clamp = Clamp(conn)

    # Connect to mqtt
    client.username_pw_set(username, password)
    client.connect(host, port, 60)

    # Start the mqtt loop in the background
    client.loop_start()

    display_device = DisplayDevice(display)
    clamp_device = ClampDevice(clamp, display_device)

    temp_entity = TemperatureEntity(display_device)

    client.publish("homeassistant/sensor/onzo_display/temperature/config", temp_entity.get_json(), retain=True)
    client.publish("onzo/display/temperature", display.get_register(display.registers.TEMPERATURE))


finally:
    conn.disconnect()
    client.disconnect()