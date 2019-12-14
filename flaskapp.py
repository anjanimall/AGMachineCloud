from flask import Flask, session
from flask import render_template, request, redirect, url_for, session, make_response
import sqlite3
from flask_mysqldb import MySQL
import MySQLdb
import MySQLdb.cursors
import re

app = Flask(__name__)


mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

usernameglobal = None
useridglobal = None

@app.route('/loginfarmer', methods = ['POST', 'GET'])
def loginfarmer():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
            cursor = myDB.cursor()
            statement = cursor.execute("SELECT username FROM farmers;")
            allusernames = cursor.fetchall()
            count = -1
            firstname = None
            lastname = None
            resp = make_response(render_template('index-farmer.html', firstname=firstname, lastname=lastname))
            for row in allusernames:
                count = count + 1
                if username in row:
                    fnstatement = cursor.execute("SELECT firstname FROM farmers WHERE username=username")
                    firstname = cursor.fetchall()[count][0]
                    lnstatement = cursor.execute("SELECT lastname FROM farmers WHERE username=username")
                    lastname = cursor.fetchall()[count][0]
                    #return render_template('index-farmer.html', firstname=firstname, lastname=lastname)
                    resp.set_cookie('username', username)
                    idstatement = cursor.execute("SELECT userid FROM farmers;")
                    userid = cursor.fetchall()[count][0] #id of the farmer logged in
                    resp.set_cookie('userID', str(userid))
                    return resp
        except:
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            myDB.close()

@app.route('/cookies')
def cookies():
    name = request.cookies.get('username')
    return name

@app.route('/farmer-register')
def farmer_register():
    return render_template('farmer-register.html')

@app.route('/addfarmer', methods = ['POST', 'GET'])
def addfarmer():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            username = request.form['username']
            email = request.form['email']
            password = request.form['inputpassword']
            usertype = 'farmer'
            data = (firstname, lastname, username, email, password, usertype)
            myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
            cursor = myDB.cursor()
            msg = ""
            statement = """INSERT INTO farmers(userid, firstname, lastname, username, email, password, usertype) VALUES (NULL, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(statement, data)
            myDB.commit()
            msg = "SUCCESS"
        except:
            myDB.rollback()
            msg = "ERROR"
        finally:
            return render_template('message.html', msg=msg)
            myDB.close()

@app.route('/loginstaff', methods = ['POST', 'GET'])
def loginstaff():
    if request.method == 'POST':
        try:
            employeeID = request.form['employeeID']
            password = request.form['password']
            myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
            cursor = myDB.cursor()
            statement = cursor.execute("SELECT employeeID FROM staff;")
            allIDs = cursor.fetchall()
            count = -1
            for row in allIDs:
                count = count + 1
                if employeeID in row:
                    fnstatement = cursor.execute("SELECT firstname FROM staff WHERE employeeID=employeeID")
                    firstname = cursor.fetchall()[count][0]
                    lnstatement = cursor.execute("SELECT lastname FROM staff WHERE employeeID=employeeID")
                    lastname = cursor.fetchall()[count][0]
                    if (int(employeeID[0])) == 0:
                        return render_template('index-staff.html', firstname=firstname, lastname=lastname)
                    else:
                        return render_template('index-controller.html', firstname=firstname, lastname=lastname)
            myDB.close()
        except:
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            myDB.close()

@app.route('/staff-register')
def staff_register():
    return render_template('staff-register.html')

@app.route('/addstaff', methods = ['POST', 'GET'])
def addstaff():
    if request.method == 'POST':
        try:
            firstname = request.form['firstname']
            lastname = request.form['lastname']
            employeeID = request.form['employeeID']
            username = request.form['username']
            email = request.form['email']
            password = request.form['inputpassword']
            usertype = 'staff'
            data = (firstname, lastname, employeeID, username, email, password, usertype)
            myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
            cursor = myDB.cursor()
            statement = """INSERT INTO staff(firstname, lastname, employeeID, username, email, password, usertype) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(statement, data)
            myDB.commit()
            msg = "SUCCESS"
        except:
            myDB.rollback()
            msg = "ERROR"
        finally:
            return render_template('message.html', msg=msg)
            myDB.close()

# dashboard pages
@app.route('/farmer')
def farmer():
    return render_template('index-farmer.html')

@app.route('/cookies2')
def cookies2():
    name = request.cookies.get('userID')
    print('what the fck', name)
    return name

@app.route('/controller')
def controller():
    return render_template('index-controller.html')

@app.route('/staff')
def staff():
    return render_template('index-staff.html')


# farmer tabs
@app.route('/farmer-services')
def farmer_services():
    try:
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        statement = cursor.execute("SELECT username FROM farmers;")
        allusernames = cursor.fetchall()
        count = -1
        listofmachines = []
        listofsensors = []
        resp = make_response(render_template('farmer-services.html', listofmachines=listofmachines, listofsensors=listofsensors))
        username = request.cookies.get('username')
        print('YOOOOOOOOOO USERNAME', username)
        userid = request.cookies.get('userID')
        userid = int(userid)
        print('YOOOOOOOOOO PT 2 ID', userid)
        for row in allusernames:
            print('YES IN ROW')
            count = count + 1
            #if usernameglobal in row:
            if username in row:
                print('IN IF USERNAME IN ROW')
                #idstatement = cursor.execute("SELECT userid FROM farmers;")
                #userid = cursor.fetchall()[count][0] #id of the farmer logged in
                #global useridglobal
                #useridglobal = userid
                #msg = userid
                statement2 = cursor.execute("SELECT * FROM machines;")
                allmachines = cursor.fetchall()
                for machine in allmachines:
                    if userid in machine:
                        listofmachines.append(machine)
                statement3 = cursor.execute("SELECT * FROM sensors;")
                allsensors = cursor.fetchall()
                for sensor in allsensors:
                    if userid in sensor:
                        listofsensors.append(sensor)
        print('LIST OF MACHINES', listofmachines)
        print('LIST OF SENSORS', listofsensors)
        msg = "SUCCESS"
        return render_template('farmer-services.html', listofmachines=listofmachines, listofsensors=listofsensors)
        #return resp
    except:
        msg = "ERROR"
        return render_template('message.html', msg=msg)
    finally:
        myDB.close()
        #return render_template('message.html', msg=msg)


@app.route('/farmer-payments')
def farmer_payments():
    try:
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        statement = cursor.execute("SELECT username FROM farmers;")
        allusernames = cursor.fetchall()
        count = -1
        listofcontracts = []
        for row in allusernames:
            count = count + 1
            username = request.cookies.get('username')
            #if usernameglobal in row:
            if username in row:
                #idstatement = cursor.execute("SELECT userid FROM farmers;")
                #userid = cursor.fetchall()[count][0] #id of the farmer logged in
                #global useridglobal
                #useridglobal = userid
                #msg = userid
                userid = request.cookies.get('userID')
                statement2 = cursor.execute("SELECT * FROM contracts;")
                allcontracts = cursor.fetchall()
                for contract in allcontracts:
                    userid = int(userid)
                    if userid in contract:
                        print('IF ID STATEMENT')
                        listofcontracts.append(contract)
        paymentdue = 0
        for c in listofcontracts:
            if c[5] == 'incomplete':
                paymentdue = paymentdue + int(c[1])
        msg = "SUCCESS"
        return render_template('farmer-payments.html', paymentdue=paymentdue)
    except:
        msg = "ERROR"
        return render_template('message.html', msg=msg)
    finally:
        myDB.close()
        #return render_template('message.html', msg=msg)

@app.route('/farmer-catalog')
def farmer_catalog():
    return render_template('farmer-catalog.html')

@app.route('/farmer-map')
def farmer_map():
    return render_template('farmer-map.html')

@app.route('/addmachine')
def addmachine():
    return render_template('addmachine.html')

@app.route('/addsensor')
def addsensor():
    return render_template('addsensor.html')

@app.route('/dbaddmachine', methods = ['POST', 'GET'])
def dbaddmachine():
    if request.method == 'POST':
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        try:
            machinetype = request.form['type']
            quantity = request.form['quantity']
            location = request.form['location']
            dateadded = request.form['date']
            print('DATE ADDED', dateadded)
            userid = request.cookies.get('userID')
            data = (machinetype, location, dateadded, userid)
            statement = """INSERT INTO machines(machineid, type, location, dateadded, userid) VALUES (NULL, %s, %s, %s, %s);"""
            cursor.execute(statement, data)
            myDB.commit()
            msg = "SUCCESS"
            return redirect('farmer-services')
        except:
            myDB.rollback()
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            #return render_template('message.html', msg=msg)
            myDB.close()

@app.route('/dbaddsensor', methods = ['POST', 'GET'])
def dbaddsensor():
    if request.method == 'POST':
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        try:
            sensortype = request.form['type']
            machineid = request.form['machineid']
            location = request.form['location']
            dateadded = request.form['date']
            #data = (sensortype, machineid, location, dateadded, useridglobal)
            userid = request.cookies.get('userID')
            data = (sensortype, machineid, location, dateadded, userid)
            statement = """INSERT INTO sensors(sensorid, type, machineid, location, dateadded, userid) VALUES (NULL, %s, %s, %s, %s, %s);"""
            cursor.execute(statement, data)
            myDB.commit()
            msg = "SUCCESS"
            return redirect('farmer-services')
        except:
            myDB.rollback()
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            #return render_template('message.html', msg=msg)
            myDB.close()


# machine controller tabs
@app.route('/controller-tasks')
def controller_tasks():
    try:
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        listofmachines = []
        listofsensors = []
        machinestatement = cursor.execute("SELECT * FROM machines;")
        allmachines = cursor.fetchall()
        for machine in allmachines:
            listofmachines.append(machine)
        sensorstatement = cursor.execute("SELECT * FROM sensors;")
        allsensors = cursor.fetchall()
        for sensor in allsensors:
            listofsensors.append(sensor)
        msg = "SUCCESS"
        return render_template('controller-tasks.html', listofmachines=listofmachines, listofsensors=listofsensors)
    except:
        msg = "ERROR"
        return render_template('message.html', msg=msg)
    finally:
        myDB.close()


# service carrier staff tabs
@app.route('/staff-resources')
def staff_resources():
    return render_template('staff-resources.html')

@app.route('/staff-servicerequests')
def staff_servicerequests():
    return render_template('staff-servicerequests.html')

@app.route('/staff-billing')
def staff_billing():
    myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
    try:
        cursor = myDB.cursor()
        statement = cursor.execute("SELECT * FROM contracts;")
        allcontracts = cursor.fetchall()
        incompletecontracts = []
        completecontracts = []
        for contract in allcontracts:
            if contract[5] == 'incomplete':
                incompletecontracts.append(contract)
            else:
                completecontracts.append(contract)
        msg = "SUCCESS"
        return render_template('staff-billing.html', incompletecontracts=incompletecontracts, completecontracts=completecontracts)
    except:
        msg = "ERROR"
        return render_template('message.html', msg=msg)
    finally:
        myDB.close()

@app.route('/dbaddcontract', methods = ['POST', 'GET'])
def dbaddcontract():
    if request.method == 'POST':
        myDB = MySQLdb.connect(host="database-2.c7yxtf52qncx.us-east-2.rds.amazonaws.com",port=3306,user="admin",passwd="281project",db="281APP")
        cursor = myDB.cursor()
        try:
            userid = request.form['userid']
            amount = request.form['amount']
            description = request.form['description']
            dateadded = request.form['dateadded']
            status = request.form['status']
            data = (amount, description, dateadded, userid, status)
            statement = """INSERT INTO contracts(contractid, amount, description, dateadded, userid, status) VALUES (NULL, %s, %s, %s, %s, %s);"""
            cursor.execute(statement, data)
            myDB.commit()
            msg = "SUCCESS"
            return redirect('staff-billing')
        except:
            myDB.rollback()
            msg = "ERROR"
            return render_template('message.html', msg=msg)
        finally:
            #return render_template('message.html', msg=msg)
            myDB.close()

@app.route('/staff-customers')
def staff_customers():
    return render_template('staff-customers.html')

@app.route('/staff-team')
def staff_team():
    return render_template('staff-team.html')


# random
@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/machine-data')
def machine_data():
    return render_template('machine-data.html')

@app.route('/sensor-data')
def sensor_data():
    return render_template('sensor-data.html')


# extras
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/charts')
def charts():
    return render_template('charts.html')

@app.route('/cards')
def cards():
    return render_template('cards.html')

@app.route('/tables')
def tables():
    return render_template('tables.html')

@app.route('/buttons')
def buttons():
    return render_template('buttons.html')

@app.route('/utilities-color')
def utilities_color():
    return render_template('utilities-color.html')

@app.route('/utilities-border')
def utilities_border():
    return render_template('utilities-border.html')

@app.route('/utilities-animation')
def utilities_animation():
    return render_template('utilities-animation.html')

@app.route('/utilities-other')
def utilities_other():
    return render_template('utilities-other.html')


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=80)\
    app.run()

