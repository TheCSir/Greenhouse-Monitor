#!/usr/bin/env python3
import csv
import sys
import sqlite3
from Utility.utility_methods import Utility

class CreateCSV:

    # Initializer / Instance Attributes
    def __init__(self,filename):
        util = Utility()
        self.dbName = util.get_db_name()
        self.outputFileName = filename

    #get datafromDatabase
    def generate_report(self):

        try:
            #open sql connection
            conn = sqlite3.connect(self.dbName)
            cur = conn.cursor()

            #call init csv
            self.init_CSV()

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
                self.write_to_CSV(date,time,temperature,humidity)
        except Exception as err:
            print(err)
            sys.exit(1)

        

    #append the data to csv
    def write_to_CSV(self,date,time,temperature,humidity):

        try:
            with open(self.outputFileName , 'a', newline='') as file:
                #append data
                writer = csv.writer(file,escapechar='', quoting=csv.QUOTE_NONE)
                writer.writerow([date,time,temperature,humidity])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

    #init csv header
    def init_CSV(self):

        try:
            with open(self.outputFileName , 'w',newline='') as file:
                #append initial row
                writer = csv.writer(file)
                writer.writerow(['Date','Time','Temperature','Humidity'])
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))

report = CreateCSV('Analytics/data.csv')
report.generate_report()