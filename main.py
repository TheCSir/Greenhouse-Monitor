#!/usr/bin/env python3
from monitorAndNotify import MonitorAndNotify

#init MoniMonitorAndNotify class with user inputs
main = MonitorAndNotify()

#get the temperature and humidity
main.get_sense_hat_data()

#insert into the database
main.log_data()