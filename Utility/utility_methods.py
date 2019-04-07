from datetime import datetime, timedelta
import time
import json
import sys


class Utility:

    def __init__(self,configFile="/home/pi/GreenHouseMonitor/Utility/setup.json"):
        self.configFile = configFile

    #get current timestamp
    def getTime(self):
        #get the timezone
        with open(self.configFile, "r") as file:
            data = json.load(file)
        
        currentTime = datetime.utcnow()

        timezone = data["timezone"]

        #validating UTC offset given
        try:
            if(timezone[0] == "+"):
                currentTime = currentTime + timedelta(hours=int(int(timezone[1:3])))
            elif(timezone[0] == "-"):
                currentTime = currentTime - timedelta(hours=int(timezone[1:3]))
            else:
                raise Exception("Invalid timezone. Please double check setup.json")
        except Exception as error:
            print(error)
            sys.exit(1)
                      
 

        return(currentTime.strftime("%H:%M"))

    #get current date
    def getDate(self):
        currentDate = time.strftime("%d/%m/%Y")
        return(currentDate)

    #get the database name
    def getDbName(self):
        with open(self.configFile, "r") as file:
            data = json.load(file)
        return data["dbName"]
    
    #get the access token
    def getAccessToken(self):
        with open(self.configFile, "r") as file:
            data = json.load(file)
        return data["accessToken"]

