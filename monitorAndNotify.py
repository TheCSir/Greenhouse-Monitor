from datetime import datetime, timedelta
from sense_hat import SenseHat
import time
import sqlite3
import json
import requests

class MonitorAndNotify():

# timezone = Offset in GMT e.g Melbourne timezone is GMT+11
# dbname = name of the database
    
    # Put your accesstoken from Pushbullet here
    ACCESS_TOKEN = ""

    def __init__(self, timezone=11,dbname='sensehat.db',senseHat=SenseHat()):
        self.temperature = senseHat.get_temperature()
        self.humidity = senseHat.get_humidity()
        self.timezone= timezone
        self.dbname = dbname
        self.senseHat = senseHat
    
    def getSenseHatData(self):
        if self.temperature is not None and self.humidity is not None:
            self.temperature = round(self.temperature, 1)
            self.humidity = round(self.humidity, 1)
            self.logData()   
    
    def getTime(self):
        currentTime = datetime.utcnow()
        currentTime = currentTime - timedelta(hours=self.timezone)
        return(currentTime.strftime("%H:%M"))

    def logData(self):
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        curs.execute("INSERT INTO SENSEHAT_data values(?,?,?)", (self.getTime(), self.temperature, self.humidity))
        conn.commit()
        conn.close()

        #Check recorded temperature to see if needed to push notification
        self.checkDataBounds()

    def send_notification(self,title,body):
        data_send = {"type": "note", "title": title, "body": body}
        response = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + self.ACCESS_TOKEN, 'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            raise Exception('Message not sent.')
        
    def checkDataBounds(self):
        with open("config.json", "r") as file:
            data = json.load(file)
        
        if self.temperature < data["min_temperature"] or self.humidity < data["min_humidity"]:
            self.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is less than the configured parameters.")
        elif self.temperature > data["max_temperature"] or self.humidity > data["max_humidity"]:
            self.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is greater than configured parameters.")

            

