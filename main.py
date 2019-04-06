#!/usr/bin/env python3
from monitorAndNotify import MonitorAndNotify



#init MoniMonitorAndNotify class with user inputs
main = MonitorAndNotify()

#call getSenseHatData method
main.getSenseHatData()
main.logData()