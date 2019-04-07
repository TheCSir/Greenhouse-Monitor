#!/usr/bin/env python3
import csv
import sqlite3
from Utility.utility_methods import Utility

class CreateCSV:

    # Initializer / Instance Attributes
    def __init__(self,filename):
        util = Utility()
        self.dbName = util.getDbName()
        self.outputFileName = filename

    #get datafromDatabase
    def GenerateReport(self):

        try:
            #open sql connection
            conn = sqlite3.connect(self.dbName)
            cur = conn.cursor()

            #call init csv
            self.InitCSV()

            #get all diffrent days
            cur.execute("SELECT * FROM `SENSEHAT_Data`;")
            result= cur.fetchall()

            #loop throught days
            for row in result:
                date = row[0]
                time = row[1]
                temperature = row[2]
                humidity = row[3]
                
                #append data to csv
                self.writeToCSV(date,time,temperature,humidity)
        except Exception as err:
            print('Query Failed: %s\nError: %s' % (query, str(err)))

        

    #append the data to csv
    def writeToCSV(self,date,time,temperature,humidity):

        try:
            with open(self.outputFileName , 'a', newline='') as file:
                #append data
                writer = csv.writer(file,escapechar='', quoting=csv.QUOTE_NONE)
                writer.writerow([date,time,temperature,humidity])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    #init csv header
    def InitCSV(self):

        try:
            with open(self.outputFileName , 'w',newline='') as file:
                #append initial row
                writer = csv.writer(file)
                writer.writerow(['Date','Time','Temperature','Humidity'])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

report = CreateCSV('Analytics/data.csv')
report.GenerateReport()