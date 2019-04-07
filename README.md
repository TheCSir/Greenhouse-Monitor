# Greenhouse-Monitor

## Task A | monitorAndNotify.py
- Run createDatabase.py (ensure that sensehat.db is in the same directory/change the database filename if needed)
- Run main.py (this creates an instance of monitorAndNotify)

## Task B | createReport.py
- All function methods are in createReport.py
- function can be called by <br>
 CreateReport( arg1, arg2, arg3 ) where <br>
      arg1 = (string) database name <br>
      arg2 = (string) report.csv name <br>
      arg3 = (string) configuration.json file name <br>
## Task C | ghBluetooth.py
- Get the mac address of the device and pair it via [bluetoothctl](https://docs.ubuntu.com/core/en/stacks/bluetooth/bluez/docs/reference/pairing/outbound)
- Add the mac address of the device in the database:<br>
      call the addNewDevice(arg1) where arg1 = (string) mac address of the device
- Run ghBluetooth.py

## Task D | analytics.py
- Run analytics.py
- To create a new data visualisation please extend AbstractAnalytics
