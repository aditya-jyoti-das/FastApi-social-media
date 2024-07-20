import mysql.connector
# import asyncio
import time
import os 

def connect_to_sqldatabase():
    MYSQL_HOST='localhost'
    MYSQL_USER=os.environ.get('MYSQL_USERNAME')
    MYSQL_PASSWORD=os.environ.get( 'MYSQL_PASSKEY')
    MYSQL_DB='Fastapiapp'
    global conn
    while True:
        try:
            conn= mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
            )
            print('sucessfully connected to the database')
            return conn
            
        except Exception as e:
            print('Error occuar during database connectivity:  ',e)
            print('tring to connect again in 2 seconds')
            time.sleep(2)

'''
def initialize_db():
    conn = connect()
    cursor = conn.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255),
        age INT
    )
    """
    cursor.execute(query)
    conn.close()
'''

# @app.on_event("startup")
# async def startup_event():
#     initialize_db()