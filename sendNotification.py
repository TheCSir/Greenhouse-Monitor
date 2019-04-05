#!/usr/bin/env python3
import sqlite3
import time
import requests
import json


class SendNotification:

	def __init__(self,dbname,tableName,date,accessToken):
		self.dbname = dbname
		self.tableName = tableName
		self.accessToken = accessToken
		self.date = date

	def send_notification(self,title,body):

		conn = sqlite3.connect(self.dbname)
		cur = conn.cursor()

        		#check if notification is send already
		cur.execute("SELECT count(date) FROM " + self.tableName + " where date = (?)",(self.date,))
		result= cur.fetchall()
		for row in result:
			count = row[0]
		print(count)

        #count is not 0 if notification is alrady sent for the day
		if count == 0:

			data_send = {"type": "note", "title": title, "body": body}
			response = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send), headers={'Authorization': 'Bearer ' + self.accessToken, 'Content-Type': 'application/json'})
            
            #check if sending fails
			if response.status_code != 200:
				raise Exception('Message not sent.')

            #if not update database
			else:
				cur.execute("INSERT INTO " + self.tableName + " (date) VALUES (?)",(self.date,))
				conn.commit()        
				conn.close()



