import mysql.connector
import os

mydb = mysql.connector.connect(
  host=os.getenv('DATABASE_HOST'),
  port=os.getenv('DATABASE_PORT'),
  user=os.getenv('DATABASE_USER_NAME'),
  password=os.getenv('DATABASE_USER_PASSWORD'),
  database=os.getenv('DATABASE_NAME'),
)


def execute_sql(sql_command):
    global mydb
    mycursor = mydb.cursor()
    mycursor.execute(sql_command)
    mydb.commit()