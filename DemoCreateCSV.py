#!/usr/bin/env python3
from createCsv import createCsv

report = createCsv('sensehat.db','Analytics/temp.csv')
report.GenerateReport()