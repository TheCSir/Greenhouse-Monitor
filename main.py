#!/usr/bin/env python3
from monitorAndNotify import MonitorAndNotify

#init MoniMonitorAndNotify class with user inputs
main = MonitorAndNotify()

#get the temperature and humidity
main.getSenseHatData()

#insert into the database
main.logData()