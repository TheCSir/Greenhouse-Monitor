#!/usr/bin/env python3
import bluetooth
import os
import sys
import time
import sqlite3
from sendNotification import SendNotification
from monitorAndNotify import MonitorAndNotify
from Utility.utility_methods import Utility


class GreenHouseBluetooth:

    def __init__(self):
        utility = Utility()
        self.dbname = utility.getDbName()

    #check if the mac address passed in is in the database (i.e. paired with)
    def isDeviceInDb(self, mac_address):

        try:
            conn = sqlite3.connect(self.dbname)
            cur = conn.cursor()

            
            cur.execute("SELECT count(SENSEHAT_BTDevices.mac_address) FROM SENSEHAT_BTDevices WHERE SENSEHAT_BTDEvices.mac_address = (?)",(mac_address,))
            result = cur.fetchall()
            for row in result:
                count = row[0]

            if count > 0:
                return True
            else:
                return False
        except Exception as err:
            print(error)
            sys.exit(1)

    #scans the area to see the bluetooth-enabled devices
    def search(self):
        while True:

            nearby_devices = bluetooth.discover_devices()

            #loop through the mac address found by the pi
            for mac_address in nearby_devices:
                if self.isDeviceInDb(mac_address) == True:
                    #create utility class to get the date
                    utility = Utility()
                    
                    #checks the current temperature and humidity
                    man = MonitorAndNotify()
                    man.getSenseHatData()
                    
                    #check if notification is needed to be sent
                    alert = SendNotification('SENSEHAT_BTDailyNotification',utility.getDate())
                    alert.checkDataBounds(man.temperature,man.humidity,True)
                    break

    #Add the mac address of the device you want to be found
    def addNewDevice(self, mac_address):
        try:
            conn = sqlite3.connect(self.dbname)
            curs = conn.cursor()
            curs.execute("INSERT INTO SENSEHAT_BTDevices VALUES(?)",(mac_address,))
            conn.commit()
            conn.close()
        except Exception as err:
            print(error)
            sys.exit(1)

#execute
ghBluetooth = GreenHouseBluetooth()
ghBluetooth.search()
