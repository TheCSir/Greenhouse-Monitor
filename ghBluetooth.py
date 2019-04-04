#!/usr/bin/env python3
import bluetooth
import os
import time
import sqlite3

class GreenHouseBluetooth:

    def __init__(self,dbname):
        self.dbname = dbname

    def isDeviceInDb(self, mac_address):
        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        #check if the mac address passed in is in the database (i.e. paired with)
        cur.execute("SELECT count(SENSEHAT_BTDevices.mac_address) FROM SENSEHAT_BTDevices WHERE SENSEHAT_BTDEvices.mac_address = (?)",(mac_address,))
        result = cur.fetchall()
        for row in result:
            count = row[0]

        if count > 0:
            return True
        else:
            return False           

    #scans the area to see the bluetooth-enabled devices
    def search(self):
        while True:
            nearby_devices = bluetooth.discover_devices()

            #loop through the mac address found by the pi
            for mac_address in nearby_devices:
                if self.isDeviceInDb(mac_address) == True:
                   #TODO SEND NOTIFICATION
                    break

    #Add the mac address of the device you want to be found
    def addNewDevice(self, mac_address):
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        curs.execute("INSERT INTO SENSEHAT_BTDevices VALUES(?)",(mac_address,))
        conn.commit()
        conn.close()

#TEST: a = GreenHouseBluetooth('/home/pi/GreenHouseMonitor/sensehat.db')
#TEST: a.search()
