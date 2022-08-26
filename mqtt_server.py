import os

import paho.mqtt.client as mqtt
from apscheduler.schedulers.background import BackgroundScheduler

from mqtt.devices.clamp import ClampDevice
from mqtt.devices.display import DisplayDevice

from mqtt.homeassistant.entities.entity_loader import EntityLoader

from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp
from onzo.devices.display import Display

username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]
host = os.environ["HOST"]
port = int(os.environ["PORT"])

conn = Connection()
client = mqtt.Client()

scheduler = BackgroundScheduler()
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

    # Start the scheduler
    # An entity will automatically create a job in the scheduler to pull and publish data
    scheduler.start()

    display_device = DisplayDevice(display)
    clamp_device = ClampDevice(clamp, display_device)

    # Dynamically load entities.
    EntityLoader(client, scheduler, display_device, clamp_device).load()

    # Create an infinite loop
    while True:
        pass


finally:
    conn.disconnect()
    client.disconnect()