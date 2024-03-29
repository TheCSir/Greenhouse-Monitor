#!/usr/bin/env python3

from datetime import datetime, timedelta
from sendNotification import SendNotification
from Utility.utility_methods import Utility
from sense_hat import SenseHat
import sys
import time
import sqlite3
import json
import requests

class MonitorAndNotify():

# timezone = Offset in GMT e.g Melbourne timezone is GMT+11
# dbname = name of the database

    def __init__(self):
        self.temperature = None
        self.humidity = None

    #main method to perform task a
    def get_sense_hat_data(self):

        #init SenseHat and read data
        senseHat_call = SenseHat()
        temperature = senseHat_call.get_temperature()
        humidity = senseHat_call.get_humidity()

        #set global variables
        self.temperature = round(temperature, 1)
        self.humidity = round(humidity, 1)

    #add gathered data to Database
    def log_data(self):

        utility = Utility()
        date = utility.get_date()
        time = utility.get_time()
        
        try:
            conn = sqlite3.connect(utility.get_db_name())
            curs = conn.cursor()
            curs.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", (date, time, self.temperature, self.humidity))
            conn.commit()
            conn.close()
        except Exception as err:
            print(err)
            sys.exit(1)

        #Check recorded temperature/humidity to see if needed to push notification
        alert = SendNotification('SENSEHAT_DailyNotification',date)
        alert.check_data_bounds(self.temperature,self.humidity)



            

