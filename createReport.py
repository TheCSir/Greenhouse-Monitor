#!/usr/bin/env python3
import csv
import sqlite3
import json
import sys

class CreateReport:

    # Initializer / Instance Attributes
    def __init__(self, dbName,flename,configs):
        self.dbName = dbName
        self.filename = flename
        self.configurations=configs

    #get datafromDatabase
    def generate_report(self):

        #create report CSV file
        self.create_CSV()

        try:
            #open sql connection
            conn = sqlite3.connect(self.dbName)
            cur = conn.cursor()

            #get all diffrent days
            cur.execute("SELECT date FROM `SENSEHAT_Data` GROUP BY SENSEHAT_Data.date;")
            result= cur.fetchall()

            #loop throught days
            for row in result:
                date = row[0]
                currentline = self.analyse_data(self.get_daily_data(date)[0],self.get_daily_data(date)[1],
                                self.get_daily_data(date)[2],self.get_daily_data(date)[3])
                
                #append data to csv
                self.write_to_CSV(date,currentline)
        except Exception as err:
            print(err)
            sys.exit(1)

    #get the min max data for the selected date
    def get_daily_data(self,date):

        try:
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
        except Exception as err:
            print(err)
            sys.exit(1)


        #return format is (Min,Max)/(Temprature,Humidity)
        return(MinTemp,MaxTemp,MinHumidity,MaxHumidity)

    #analyze data and genarate message
    def analyse_data(self,minTemp,maxTemp,minHum,maxHum):

        isGood = True
        Message = ''

        #load data from json
        try:
            with open(self.configurations, "r") as file:
                data = json.load(file)
        except IOError as e:
            print("I/O error opening config file ({0}): {1}".format(e.errno, e.strerror))
        
        
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
    def create_CSV(self):

        try:
            with open(self.filename , 'w') as file:

                #append initial row
                writer = csv.writer(file)
                writer.writerow(['Date','Status'])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    #append the data to csv
    def write_to_CSV(self,date,status):

        try:
            with open(self.filename , 'a' ,newline='') as file:

                #append data
                writer = csv.writer(file,escapechar='', quoting=csv.QUOTE_NONE)
                writer.writerow([date,status])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
            
report = CreateReport('sensehat.db','report.csv','config.json')
report.generate_report()