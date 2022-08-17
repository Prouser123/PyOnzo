import datetime
import time
import math


import onzo.internal.connection
import onzo.devices.clamp
import onzo.devices.display

conn = onzo.internal.connection.Connection()
try:
    conn.connect()
    disp = onzo.devices.display.Display(conn)
    clamp = onzo.devices.clamp.Clamp(conn)

    p_reactive = None
    counter = 0
    print("Timestamp,P_real,P_reactive,P_apparent,kWh,Battery_Voltage")
    while True:
        p_real = clamp.get_power()

        # reactive power only updates onces every 15s, so there is no use
        # querying more often, this just wastes clamp battery
        if counter % 15 == 0:
            p_reactive = clamp.get_powervars()
        # Only update battery once every 10mins
        if counter % (60 * 10) == 0:
            battery = clamp.get_batteryvolts()

        p_apparent = int(math.sqrt(p_real**2 + p_reactive**2))
        ear = clamp.get_cumulative_kwh()

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print("{},{},{},{},{},{}".format(timestamp, p_real, p_reactive, p_apparent, ear, battery))

        counter += 1
        time.sleep(1)

finally:
    conn.disconnect()
