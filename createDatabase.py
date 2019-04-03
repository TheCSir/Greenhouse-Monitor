import sqlite3

# Remember to install SQLite, create a directory and then create a database
conn = sqlite3.connect('sensehat.db')

with conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_Data(date DATETIME, timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")

    