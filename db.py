import sqlite3

conn = sqlite3.connect('Cloud281.db')

print("Opened database successfully")

c = conn.cursor()

#c.execute('''CREATE TABLE farmers
#             (firstname text, lastname text, username text, email text, password text, usertype text) ''')


c.execute('''CREATE TABLE staffmembers
             (firstname text, lastname text, employeeID text, username text, email text, password text, usertype text) ''')

conn.commit()

conn.close()
