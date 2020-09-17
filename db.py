import sqlite3
from sqlite3 import Error

def dbconnection():
    conn = None
    try:
        conn = sqlite3.connect(r"C:\DevApps\sqlite\testDB.db")
    except Error as e:
        print(e)
    return conn

if __name__ == '__main__':
    main()
