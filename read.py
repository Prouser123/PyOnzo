import datetime
import time
import math

from onzo.internal.connection import Connection
from onzo.devices.clamp import Clamp
from onzo.devices.display import Display

conn = Connection()
try:
    conn.connect()
    disp = Display(conn)
    clamp = Clamp(conn)

    p_reactive = None
    counter = 0
    print("Timestamp,P_real,P_reactive,P_apparent,kWh,Battery_Voltage")
    print("disp serial: %s" % disp.get_register(disp.registers.SERIAL))
    while True:
        p_real = clamp.get_register(clamp.registers.POWER)

        # reactive power only updates onces every 15s, so there is no use
        # querying more often, this just wastes clamp battery
        if counter % 15 == 0:
            p_reactive = clamp.get_register(clamp.registers.POWER_VARS)
        # Only update battery once every 10mins
        if counter % (60 * 10) == 0:
            battery = clamp.get_register(clamp.registers.BATTERY_VOLTAGE)

        p_apparent = int(math.sqrt(p_real**2 + p_reactive**2))
        #ear = clamp.get_cumulative_kwh()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("{},{},{},{},{},{}".format(timestamp, p_real, p_reactive, p_apparent, "null", battery))

        counter += 1
        time.sleep(1)

finally:
    conn.disconnect()
