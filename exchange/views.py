from django.shortcuts import render
import mysql.connector, os
from rest_framework.views import APIView



#connect to database
mydb = mysql.connector.connect(
  host=os.getenv('DATABASE_HOST'),
  port=os.getenv('DATABASE_PORT'),
  user=os.getenv('DATABASE_USER_NAME'),
  password=os.getenv('DATABASE_USER_PASSWORD'),
  database=os.getenv('DATABASE_NAME'),
)


class save_candles(APIView):
    def post(self, req):
        sql_command = req.POST['sql_commands']
        mycursor = mydb.cursor()
        mycursor.execute(sql_command)
        mydb.commit()