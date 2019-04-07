#!/usr/bin/env python3
import sqlite3
from Utility.utility_methods import Utility

util = Utility()
# Remember to install SQLite, create a directory and then create a database
conn = sqlite3.connect(util.getDbName())

with conn:
    try:
        cur = conn.cursor()

        #table for data reads
        cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
        cur.execute("CREATE TABLE SENSEHAT_Data(date DATETIME, timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")

        #table for daily notifications
        cur.execute("DROP TABLE IF EXISTS SENSEHAT_DailyNotification")
        cur.execute("CREATE TABLE SENSEHAT_DailyNotification(date DATETIME)")

        #table for bluetooth devices
        cur.execute("DROP TABLE IF EXISTS SENSEHAT_BTDevices")
        cur.execute("CREATE TABLE SENSEHAT_BTDevices(mac_address)")

        #table for bluetooth notification
        cur.execute("DROP TABLE IF EXISTS SENSEHAT_BTDailyNotification")
        cur.execute("CREATE TABLE SENSEHAT_BTDailyNotification(date DATETIME)")
    except Exception as err:
        print('Query Failed: %s\nError: %s' % (query, str(err)))
