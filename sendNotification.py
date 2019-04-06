#!/usr/bin/env python3
import sqlite3
import time
import requests
import json
from usefulMethods import Utility


class SendNotification:

	def __init__(self,tableName,date,configFile="config.json"):
		self.tableName = tableName
		self.date = date
		self.configFile = configFile


	    #check bounds and send necessary notifications 
	def checkDataBounds(self,temperature,humidity,bluetooth=False):

		bluetooth_msg = ""
        
		#get data from jason
		with open(self.configFile, "r") as file:
			data = json.load(file)

		if(bluetooth == True):
			bluetooth_msg = "Bluetooth Device Connected!\n\n"

        #check boundaries        
		if temperature < data["min_temperature"] or humidity < data["min_humidity"]:
			self.send_notification(bluetooth_msg + "Raspberry Pi Data Update", "Recorded temperature: " + str(temperature) +"\nRecorded humidity: "+ str(humidity)+"\n\n"+
				"Temperature and/or Humidity is less than the configured parameters.")
		elif temperature > data["max_temperature"] or humidity > data["max_humidity"]:
			self.send_notification(bluetooth_msg + "Raspberry Pi Data Update", "Recorded temperature: "+ str(temperature)+"\nRecorded humidity: "+ str(humidity)+"\n\n"+
				"Temperature and/or Humidity is greater than the configured parameters.")

	def send_notification(self,title,body):

		utility = Utility()
		conn = sqlite3.connect(utility.getDbName())
		cur = conn.cursor()

        #check if notification is send already
		cur.execute("SELECT count(date) FROM " + self.tableName + " where date = (?)",(self.date,))
		result= cur.fetchall()
		for row in result:
			count = row[0]

        #count is not 0 if notification is alrady sent for the day
		if count == 0:

			data_send = {"type": "note", "title": title, "body": body}
			response = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + utility.getAccessToken(), 'Content-Type': 'application/json'})
            
            #check if sending fails
			if response.status_code != 200:
				raise Exception('Message not sent.')

            #if not update database
			else:
				cur.execute("INSERT INTO " + self.tableName + " (date) VALUES (?)",(self.date,))
				conn.commit()        
				conn.close()



