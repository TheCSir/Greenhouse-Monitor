import sqlite3

# Remember to install SQLite, create a directory and then create a database
conn = lite.connect('sensehat.db')

with conn:
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_Data(timestamp DATETIME, temp NUMERIC, humidity NUMERIC"))