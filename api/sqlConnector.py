import mysql.connector
from datetime import date
import pandas as pd

today = date.today().strftime("%Y-%m-%d")

mydb = mysql.connector.connect(
    host="localhost",
    user="RestDemo",
    password="demoRest",
    database="restapi"
)


def postData(sensorVal):
    mycursor = mydb.cursor()
    sql = "INSERT INTO data (Temperature) VALUES (%f)" % (sensorVal)
    mycursor.execute(sql)
    mydb.commit()


def getTodayData():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE CAST(Date AS DATE) = CAST('%s' AS DATE) ORDER BY ID" % (
        str(today))
    mycursor.execute(sql)
    return mycursor.fetchall()

def getLastData():
    mycursor = mydb.cursor()
    sql = "SELECT * FROM data WHERE CAST(Date AS DATE) = CAST('%s' AS DATE) ORDER BY ID DESC LIMIT 1" %(str(today))
    mycursor.execute(sql)
    return mycursor.fetchall()