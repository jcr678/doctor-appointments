from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
import pandas as pd
import ast
import sqlite3

app = Flask(__name__)
api = Api(app) #api takes in app

def get_doctors():
    toReturn =[]
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_query = """SELECT * from doctor"""
    cursor.execute(sqlite_select_query)
    records = cursor.fetchall()
    for row in records:
        user = {}
        user["id"]=row[0]
        user["firstName"]=row[1]
        user["lastName"] = row[2]
        toReturn.append(user)
    cursor.close()
    return jsonify(toReturn)  # return data and 200 OK (successful api)

def get_doctor_id(doctorFirstName, doctorLastName):
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()
    sqlite_select_query = "SELECT * from doctor where firstName =? and lastName =?"
    print(sqlite_select_query)
    cursor.execute(sqlite_select_query, (doctorFirstName,doctorLastName))
    records = cursor.fetchall()
    cursor.close()
    return records
def get_appointments(doctorFirstName, doctorLastName,date):
    records=get_doctor_id(doctorFirstName, doctorLastName)
    sqliteConnection = sqlite3.connect('database.db')
    if len(records)==0:
        return {
            'message': f"Doctor '{doctorLastName}','{doctorFirstName}' not found."
        }, 404
    elif len(records)==1:
        toReturn =[]
        cursor = sqliteConnection.cursor()
        doctorId= records[0][0]
        sqlite_select_query = "SELECT * from appointment where doctorId=? and dateAppointment=?"
        cursor.execute(sqlite_select_query, (doctorId,date))
        records = cursor.fetchall()
        for row in records:
            user = {}
            user["id"]=row[0]
            user["patientFirstName"]=row[1]
            user["patientLastName"] = row[2]
            user["dateAppointment"]=row[3]
            user["timeAppointment"]=row[4]
            user["kind"]=row[5]
            user["doctorId"]=row[6]
            toReturn.append(user)
        cursor.close()
        return jsonify(toReturn)  # return data and 200 OK (successful api)
class Calendar(Resource): #inherit Resource library
    def get(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('doctorFirstName', required=False)  # add args
        parser.add_argument('doctorLastName', required=False)  # add args
        parser.add_argument('date', required=False)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        #doctor and day were not provided, therefore return list of all doctors
        #http://127.0.0.1:5000/calendar
        if((not args['doctorFirstName']) and (not args['doctorLastName']) and (not args['date'])):
            return get_doctors()
        #doctor and date were provided, return appointments for the given doctor and date
        #http://127.0.0.1:5000/calendar?doctorFirstName=Juliu&doctorLastName=Hibbert&date=123
        elif(args['doctorFirstName'] and args['doctorLastName'] and args['date']):
            return get_appointments(args['doctorFirstName'], args['doctorLastName'],args['date'])
        else:
            return {
                'message': "Please either either provide no parameters, \n or provide parameters for doctor First name, Last name, and date."
            }, 404
    #http://127.0.0.1:5000/calendar?doctorFirstName=Julius&doctorLastName=Hibbert&date=8-17-2021&time=8:15AM&patientFirstName=john&patientLastName=Green&kind=New Patient
    def post(self):
        parser = reqparse.RequestParser()  # initialize
        #rows of the data frame
        #required=true, nonoptional
        #type defaults to str, type=str
        parser.add_argument('doctorFirstName', required=True)  # add args
        parser.add_argument('doctorLastName', required=True)  # add args
        parser.add_argument('date', required=True)  # add args
        parser.add_argument('time', required=True)  # add args
        parser.add_argument('patientFirstName', required=True)  # add args
        parser.add_argument('patientLastName', required=True)  # add args
        parser.add_argument('kind', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        records_id=get_doctor_id(args['doctorFirstName'], args['doctorLastName'])
        doctorId= records_id[0][0]
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        interval = args['time'].split(":")[1][0:2]
        #New appointments can only start at 15 minute intervals
        possible_intervals=["00","15","30","45"]
        if(interval not in possible_intervals):
            return {
                'message': "Time must be in 15 minute intervals"
                }, 404
        #kind can only be New Patient or Follow-up).
        possible_patients = ["New Patient", "Follow-up"]
        if(args['kind'] not in possible_patients):
            return {
                'message': "Kind must be " + possible_patients[0] +" or " + possible_patients[1]
                }, 404
        #A doctor can have multiple appointments with the same time, but no more than 3
        # appointments can be added with the same time for a given doctor
        sqlite_select_query = "SELECT * from appointment where doctorId=? and " + \
                "dateAppointment=? and timeAppointment=?"
        cursor.execute(sqlite_select_query, (doctorId,
                                            args['date'],
                                            args['time']
                                            ))
        records = cursor.fetchall()
        cursor.close()
        if(len(records)>=3):
            return {
                'message': "The given doctor already has three appointments on this day"
                }, 404
        insert_sql="INSERT INTO appointment (doctorId,dateAppointment,timeAppointment,patientFirstName,patientLastName,kind) VALUES (?, ?, ?, ?, ?, ?)"
        sqliteConnection.execute(insert_sql,
        (doctorId,args['date'], args['time'], args['patientFirstName'],args['patientLastName'],args['kind'])
        )
        sqliteConnection.commit()
        sqliteConnection.close()
        return get_appointments(args['doctorFirstName'], args['doctorLastName'],args['date'])

    #http://127.0.0.1:5000/calendar?doctorFirstName=Julius&doctorLastName=Hibbert&date=8-17-2021&time=8:15AM&patientFirstName=john&patientLastName=Green&kind=new
    def delete(self):
        parser = reqparse.RequestParser()  # initialize
        parser.add_argument('doctorFirstName', required=True)  # add args
        parser.add_argument('doctorLastName', required=True)  # add args
        parser.add_argument('date', required=True)  # add args
        parser.add_argument('time', required=True)  # add args
        parser.add_argument('patientFirstName', required=True)  # add args
        parser.add_argument('patientLastName', required=True)  # add args
        parser.add_argument('kind', required=True)  # add args
        args = parser.parse_args()  # parse arguments to dictionary
        toReturn =[]
        records_id=get_doctor_id(args['doctorFirstName'], args['doctorLastName'])
        doctorId= records_id[0][0]
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        sqlite_select_query = "SELECT * from appointment where doctorId=? and " + \
                "dateAppointment=? and timeAppointment=? and patientFirstName=? and patientLastName=? and kind=?"
        cursor.execute(sqlite_select_query, (doctorId,
                                            args['date'],
                                            args['time'],
                                            args['patientFirstName'],
                                            args['patientLastName'],
                                            args['kind']
                                            ))
        records = cursor.fetchall()
        #id not already in db
        if len(records)==0:
            cursor.close()
            return {
                'message': "No appointments were found."
            }, 404
        #id in db
        #get the row to return
        for row in records:
            user = {}
            print(row)

            user["id"]=row[0]
            user["patientFirstName"]=row[1]
            user["patientLastName"] = row[2]
            user["dateAppointment"] = row[3],
            user["timeAppointment"] = row[4],
            user["kind"] = row[5],
            user["doctorId"] = row[6],
            toReturn.append(user)

        cursor.close()
        #delete from db
        sqliteConnection = sqlite3.connect('database.db')
        sqlite_delete_query ="DELETE from appointment where doctorId=? and "+ \
                "dateAppointment=? and timeAppointment=? and patientFirstName=? and patientLastName=? and kind=?"
        sqliteConnection.execute(sqlite_delete_query, (doctorId,
                                            args['date'],
                                            args['time'],
                                            args['patientFirstName'],
                                            args['patientLastName'],
                                            args['kind']
                                            ))
        sqliteConnection.commit()
        sqliteConnection.close()
        return jsonify(toReturn)  # return data and 200 OK (successful api)

api.add_resource(Calendar, '/calendar')  # add endpoint

if __name__ == '__main__':
    app.run()  # run our Flask app
