#!/usr/bin/env python3
from createReport import CreateReport

report = CreateReport('sensehat.db','report.csv','config.json')
report.GenerateReport()