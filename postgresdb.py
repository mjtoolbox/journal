import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL'] = 'postgresql://postgres:docker@localhost/postgres'


def dbconnection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(e)
    return conn


if __name__ == '__main__':
    dbconnection()
