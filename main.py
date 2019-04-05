#!/usr/bin/env python3
from monitorAndNotify import MonitorAndNotify



#init MoniMonitorAndNotify class with user inputs
main = MonitorAndNotify(11,'sensehat.db','config.json',"o.ZJwli1lhTH9nH1pKrSisFfMivfGO3SP4")

#call getSenseHatData method
main.getSenseHatData()