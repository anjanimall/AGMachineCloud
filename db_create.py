import mysql.connector

mydb = mysql.connector.connect(
  host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",
  user="admin",
  passwd="281project",
  database="database-2"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE customers (name VARCHAR(255), address VARCHAR(255))")

print("DB created.")
