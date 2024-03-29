#!/usr/bin/env python3
import sqlite3
import time
import requests
import sys
import json
from Utility.utility_methods import Utility


class SendNotification:

	def __init__(self,tableName,date,configFile="config.json"):
		self.tableName = tableName
		self.date = date
		self.configFile = configFile


	    #check bounds and send necessary notifications 
	def check_data_bounds(self,temperature,humidity,bluetooth=False):

		bluetooth_msg = ""
        
		#get data from jason
		with open(self.configFile, "r") as file:
			data = json.load(file)

		#add this message if a bluetooth device is connected
		if(bluetooth == True):
			bluetooth_msg = "Bluetooth Device Connected!\n"

        #check boundaries        
		if temperature < data["min_temperature"] or humidity < data["min_humidity"]:
			self.send_notification(bluetooth_msg + "Raspberry Pi Data Update", "Recorded temperature: " + str(temperature) +"\nRecorded humidity: "+ str(humidity)+"\n\n"+
				"Temperature and/or Humidity is less than the configured parameters.")
		elif temperature > data["max_temperature"] or humidity > data["max_humidity"]:
			self.send_notification(bluetooth_msg + "Raspberry Pi Data Update", "Recorded temperature: "+ str(temperature)+"\nRecorded humidity: "+ str(humidity)+"\n\n"+
				"Temperature and/or Humidity is greater than the configured parameters.")

	def send_notification(self,title,body):

		utility = Utility()
		
		try:
		#check if notification is send already
			conn = sqlite3.connect(utility.get_db_name())
			cur = conn.cursor()
			cur.execute("SELECT count(date) FROM " + self.tableName + " where date = (?)",(self.date,))
			result= cur.fetchall()
			for row in result:
				count = row[0]
		except Exception as err:
			print(err)
			sys.exit(1)
        #count is not 0 if notification is alrady sent for the day
		if count == 0:

			data_send = {"type": "note", "title": title, "body": body}
			response = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + utility.get_access_token(), 'Content-Type': 'application/json'})
            
			#check if sending fails
			if response.status_code != 200:
				raise Exception('Message not sent.')

			#if not update database
			else:
				try:
					cur.execute("INSERT INTO " + self.tableName + " (date) VALUES (?)",(self.date,))
					conn.commit()        
					conn.close()
				except Exception as err:
					print(err)
					sys.exit(1)



