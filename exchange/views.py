from django.shortcuts import render
import mysql.connector, os
from rest_framework.views import APIView
from accounts.models import *

################ contact   #######################
def index(req):
  return render(req, 'index.html')

def contact(req):
  if req.method == 'GET':
    return render(req, 'contact.html')
  


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