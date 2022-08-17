import onzo.internal.connection
import onzo.devices.clamp
import onzo.devices.display

conn = onzo.internal.connection.Connection()
try:
    conn.connect()
    disp = onzo.devices.display.Display(conn)
    clamp = onzo.devices.clamp.Clamp(conn)

    data =[
        [disp.get_min, "disp min"],
        [disp.get_hour, "disp hour"],
        [disp.get_day, "disp day"],
        [disp.get_year, "disp year"],
        [disp.get_synched, "disp synched"],
        [disp.get_version, "disp version"],
        [disp.get_hardware, "disp hardware"],
        [disp.get_configured, "disp configured"],
        [disp.get_standingcharge, "disp standingcharge"],
        [disp.get_unitcost, "disp unitcost"],
        [disp.get_EAC, "disp EAC"],
        [disp.get_gridweekstart, "disp gridweekstart"],
        [disp.get_gridweekstop, "disp gridweekstop"],
        [disp.get_gridweekendstart, "disp gridweekendstart"],
        [disp.get_gridweekendstop, "disp gridweekendstop"],
        [disp.get_serial, "disp serial"],
        [disp.get_country, "disp country"],
        #[disp.get_temp-offset, "disp temp-offset"],
        #[disp.get_temp_gain, "disp temp-gain"],
        [disp.get_target, "disp target"],
        [disp.get_cost0, "disp cost0"],
        #[disp.get_cost1, "disp cost1"],
        #[disp.get_cost2, "disp cost2"],
        #[disp.get_cost3, "disp cost3"],
        [disp.get_start0, "disp start0"],
        #[disp.get_start1, "disp start1"],
        #[disp.get_start2, "disp start2"],
        #[disp.get_start3, "disp start3"],

        [clamp.get_type, "clamp type"],
        [clamp.get_version, "clamp version"],
        [clamp.get_serial, "clamp serial"],
        [clamp.get_status, "clamp status"],
        [clamp.get_power, "clamp power"],
        [clamp.get_readinginterval, "clamp readinginterval"],
        [clamp.get_sendinginterval, "clamp sendinginterval"],
        [clamp.get_timestamp, "clamp timestamp"],
        [clamp.get_voltage, "clamp voltage"],
        [clamp.get_calphase0, "clamp calphase0"],
        [clamp.get_calgain0, "clamp calgain0"],
        [clamp.get_temperature, "clamp temperature"],
        [clamp.get_powervars, "clamp powervars"],
        [clamp.get_RSSI, "clamp RSSI"],
        [clamp.get_EAR, "clamp EAR"],
        [clamp.get_batteryvolts, "clamp batteryvolts"],
        [clamp.get_txpower, "clamp txpower"],
        [clamp.get_instwatt, "clamp instwatt"],
        [clamp.get_instvar, "clamp instvar"],
        [clamp.get_calgain1, "clamp calgain1"],
        [clamp.get_calgain2, "clamp calgain2"],
        [clamp.get_txperiodlimits, "clamp txperiodlimits"],
        [clamp.get_calgain3, "clamp calgain3"],
        [clamp.get_calgain4, "clamp calgain4"]

    ]

    for i in data:
        print("%s: %s" % (i[1], i[0]()))
finally:
    conn.disconnect()
