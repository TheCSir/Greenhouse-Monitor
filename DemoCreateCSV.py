#!/usr/bin/env python3
from createCSV import createCsv

report = createCsv('sensehat.db','Analytics/temp.csv')
report.GenerateReport()