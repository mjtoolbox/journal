import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL'] = 'postgres://ofbhuqifsdukbk:0000fb45e23c541e1a93a544ef00e38f81528c742de3d1b65bad6baa36b8ec98@ec2-18-210-90-1.compute-1.amazonaws.com:5432/d2ift4156h369'


def dbconnection():
    conn = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    except Exception as e:
        print(e)
    return conn


if __name__ == '__main__':
    main()
