import sqlite3

# Remember to install SQLite, create a directory and then create a database
conn = sqlite3.connect('sensehat.db')

with conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS SENSEHAT_data")
    cur.execute("CREATE TABLE SENSEHAT_Data(date DATETIME, timestamp DATETIME, temp NUMERIC, humidity NUMERIC)")

    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('03/04/2019', '10:30', 10, 100 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('03/04/2019', '11:30', 10, 10 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('04/04/2019', '10:30', 40, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('04/04/2019', '10:30', 25, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('05/04/2019', '10:30', 25, 10 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('05/04/2019', '10:30', 25, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('06/04/2019', '10:30', 25, 70 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('06/04/2019', '10:30', 25, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('07/04/2019', '10:30', 25, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('07/04/2019', '10:30', 25, 55 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('08/04/2019', '10:30', 10, 10 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('08/04/2019', '10:30', 10, 10 ))
    cur.execute("INSERT INTO SENSEHAT_data values(?,?,?,?)", ('08/04/2019', '10:30', 10, 10 ))
    
    conn.commit()
