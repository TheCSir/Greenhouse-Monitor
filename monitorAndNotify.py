from datetime import datetime, timedelta
from sense_hat import SenseHat
import time
import sqlite3

class MonitorAndNotify():

# timezone = Offset in GMT e.g Melbourne timezone is GMT+11
# dbname = name of the database

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
        currentTime = datetime.now()
        currentTime = currentTime - timedelta(hours=self.timezone)
        return(currentTime.strftime("%H:%M"))

    def logData(self):
        conn = sqlite3.connect(self.dbname)
        curs = conn.cursor()
        curs.execute("INSERT INTO SENSEHAT_data values(?,?,?)", (self.getTime(), self.temperature, self.humidity))
        conn.commit()
        conn.close()


	




