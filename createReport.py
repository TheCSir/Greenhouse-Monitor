#!/usr/bin/env python3
import csv
import sqlite3
import json

class CreateReport:

    # Initializer / Instance Attributes
    def __init__(self, dbName,flename,configs):
        self.dbName = dbName
        self.filename = flename
        self.configurations=configs

    #get datafromDatabase
    def GenerateReport(self):

        #open sql connection
        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        #create report CSV file
        self.createCSV()

        #get all diffrent days
        cur.execute("SELECT date FROM `SENSEHAT_Data` GROUP BY SENSEHAT_Data.date;")

        #loop throught days
        result= cur.fetchall()
        for row in result:
            date = row[0]
            currentline = self.AnalyzeData(self.GetDailyData(date)[0],self.GetDailyData(date)[1],
                            self.GetDailyData(date)[2],self.GetDailyData(date)[3])
            
            #append data to csv
            self.writeToCSV(date,currentline)



    #get the min max data for the selected date
    def GetDailyData(self,date):

        conn = sqlite3.connect(self.dbName)
        cur = conn.cursor()

        #get values for the day
        #max temprature
        cur.execute("SELECT max(SENSEHAT_Data.temp) FROM `SENSEHAT_Data` WHERE SENSEHAT_Data.date= (?)",(date,))
        result= cur.fetchall()
        for row in result:
            MaxTemp = row[0]

        #min temprature
        cur.execute("SELECT min(SENSEHAT_Data.temp) FROM `SENSEHAT_Data` WHERE SENSEHAT_Data.date= (?)",(date,))
        result= cur.fetchall()
        for row in result:
            MinTemp = row[0]

        #max humidity
        cur.execute("SELECT max(SENSEHAT_Data.humidity) FROM `SENSEHAT_Data` WHERE SENSEHAT_Data.date= (?)",(date,))
        result= cur.fetchall()
        for row in result:
            MaxHumidity = row[0]

        #min humidity
        cur.execute("SELECT min(SENSEHAT_Data.humidity) FROM `SENSEHAT_Data` WHERE SENSEHAT_Data.date= (?)",(date,))
        result= cur.fetchall()
        for row in result:
            MinHumidity = row[0]


        #return format is (Min,Max)/(Temprature,Humidity)
        return(MinTemp,MaxTemp,MinHumidity,MaxHumidity)

    #analyze data and genarate message
    def AnalyzeData(self,minTemp,maxTemp,minHum,maxHum):

        isGood = True
        Message = ''

        #load data from json
        with open(self.configurations, "r") as file:
            data = json.load(file)
        
        #analyze daily scores
        if minTemp < data["min_temperature"]:
            isGood = False
            tempData=round(data["min_temperature"]-minTemp, 1)
            Message += str(tempData) +'*C below Minimum temprature '
        if maxTemp > data["max_temperature"]:
            isGood = False
            tempData=round(maxTemp-data["min_temperature"], 1)
            Message += str(tempData) +'*C above Maximum temprature '
        if minHum < data["min_humidity"]:
            isGood = False
            tempData=round(data["min_humidity"]-minHum, 1)
            Message += str(tempData) +'% below Minimum humidity '
        if maxHum > data["max_humidity"]:
            isGood = False
            tempData=round(maxHum-data["max_humidity"], 1)
            Message += str(tempData) +'% above Maximum humidity '

        if isGood:
            return ' OK'
        else:
            return ' BAD :' + Message

    #create filenamed 'report.csv'
    def createCSV(self):
        
        with open(self.filename , 'w') as file:

            #append initial row
            writer = csv.writer(file)
            writer.writerow(['Date','Status'])

    #append the data to csv
    def writeToCSV(self,date,status):

        with open(self.filename , 'a' ,newline='') as file:

            #append data
            writer = csv.writer(file,escapechar='', quoting=csv.QUOTE_NONE)
            writer.writerow([date,status])
            
