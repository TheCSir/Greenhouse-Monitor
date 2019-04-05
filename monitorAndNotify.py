from datetime import datetime, timedelta
from sendNotification import SendNotification
from sense_hat import SenseHat
import time
import sqlite3
import json
import requests

class MonitorAndNotify():

# timezone = Offset in GMT e.g Melbourne timezone is GMT+11
# dbname = name of the database

    def __init__(self, timezone,dbname,cofigfile,accesstoken):
        self.temperature = None
        self.humidity = None
        self.timezone= timezone
        self.dbname = dbname
        self.configuration = cofigfile
        self.ACCESS_TOKEN=accesstoken
    
    #main method to perform task a
    def getSenseHatData(self):

        #init SenseHat and read data
        senseHat_call = SenseHat()
        temperature = senseHat_call.get_temperature()
        humidity = senseHat_call.get_humidity()

        #set global variables
        self.temperature = round(temperature, 1)
        self.humidity = round(humidity, 1)
        #store data to database and do notification if necessary
        self.logData()   
    
    #get current timestamp
    def getTime(self):
        currentTime = datetime.utcnow()
        currentTime = currentTime - timedelta(hours=self.timezone)
        return(currentTime.strftime("%H:%M"))

    #get current date
    def getDate(self):
        currentDate = time.strftime("%d/%m/%Y")
        return(currentDate)

    #add gathered data to Database
    def logData(self):
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        curs.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", (self.getDate(), self.getTime(), self.temperature, self.humidity))
        conn.commit()
        conn.close()

        #Check recorded temperature to see if needed to push notification
        self.checkDataBounds()

    #check bounds and send necessary notifications 
    def checkDataBounds(self):

        #get data from jason
        with open(self.configuration, "r") as file:
            data = json.load(file)

        #check boundries        
        if self.temperature < data["min_temperature"] or self.humidity < data["min_humidity"]:
            Allerter = SendNotification(self.dbname,'SENSEHAT_DailyNotification',self.getDate(),self.ACCESS_TOKEN)
            Allerter.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is less than the configured parameters.")
        elif self.temperature > data["max_temperature"] or self.humidity > data["max_humidity"]:
            Allerter = SendNotification(self.dbname,'SENSEHAT_DailyNotification',self.getDate(),self.ACCESS_TOKEN)
            Allerter.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is greater than configured parameters.")

            

