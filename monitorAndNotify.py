from datetime import datetime, timedelta
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

    def send_notification(self,title,body):

        conn = sqlite3.connect(self.dbname)
        cur = conn.cursor()

        #check if notification is send already
        cur.execute("SELECT count(SENSEHAT_DailyNotification.date) FROM `SENSEHAT_DailyNotification` where SENSEHAT_DailyNotification.date = (?)",(self.getDate(),))
        result= cur.fetchall()
        for row in result:
            count = row[0]

        #count is not 0 if notification is alrady sent for the day
        if count == 0:

            data_send = {"type": "note", "title": title, "body": body}
            response = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + self.ACCESS_TOKEN, 'Content-Type': 'application/json'})
            
            #check if sending fails
            if response.status_code != 200:
                raise Exception('Message not sent.')

            #if not update database
            else:
                cur.execute("INSERT INTO `SENSEHAT_DailyNotification` (date) VALUES (?)",(self.getDate(),))
                conn.commit()
        
        conn.close()
        
    def checkDataBounds(self):

        #get data from jason
        with open(self.configuration, "r") as file:
            data = json.load(file)

        #check boundries        
        if self.temperature < data["min_temperature"] or self.humidity < data["min_humidity"]:
            self.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is less than the configured parameters.")
        elif self.temperature > data["max_temperature"] or self.humidity > data["max_humidity"]:
            self.send_notification("Raspberry Pi Data Update", "Temperature and/or Humidity is greater than configured parameters.")

            

