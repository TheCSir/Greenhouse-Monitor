import sqlite3

# Remember to install SQLite, create a directory and then create a database
conn = sqlite3.connect('sensehat.db')

with conn:
    cur = conn.cursor()

    #table for data reads
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_Data(date DATETIME, timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")

    #table for daily notifications
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_DailyNotification")
    cur.execute("CREATE TABLE SENSEHAT_DailyNotification(date DATETIME)")

    #table for bluetooth devices
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_BTDevices")
    cur.execute("CREATE TABLE SENSEHAT_BTDevices(device_name,mac_address)")

    #table for bluetooth notification
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_BTDailyNotification")
    cur.execute("CREATE TABLE SENSEHAT_BTDailyNotification(date DATETIME)")