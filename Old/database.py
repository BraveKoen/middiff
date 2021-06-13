
import mysql.connector

def databaseConnect(): 
  mydb = mysql.connector.connect(
    host="185.114.157.171",
    user="middiffc_stats",
    password="Roken123",
    database="middiffc_stats"
  )
  return mydb

    
