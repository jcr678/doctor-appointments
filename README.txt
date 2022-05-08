Flask API with the following rest request types:
  GET
  POST
  DELETE

# To create the table and initialize the doctor table with initial values.
# Note that this will also delete the old tables data.
python3 createtable.py
# To set up the server to enable REST requests
python3 flask_api_db.py
# To check that the rest requests return the correct value in postman
  # Get a list of all doctors
    get http://127.0.0.1:5000/calendar
  # Get a list of all appointments for a particular doctor and particular day
  get http://127.0.0.1:5000/calendar?doctorFirstName=Julius&doctorLastName=Hibbert&date=8-17-2021
  get http://127.0.0.1:5000/calendar?doctorFirstName=Algernop&doctorLastName=Krieger&date=8-17-2021
  # Add a new appointment to a doctor's calendar
  post http://127.0.0.1:5000/calendar?doctorFirstName=Julius&doctorLastName=Hibbert&date=8-17-2021&time=8:15AM&patientFirstName=john&patientLastName=Green&kind=New Patient
  post http://127.0.0.1:5000/calendar?doctorFirstName=Algernop&doctorLastName=Krieger&date=8-17-2021&time=8:15AM&patientFirstName=jane&patientLastName=Green&kind=New Patient
  # Delete an existing appointment from a doctor's calendar
  delete http://127.0.0.1:5000/calendar?doctorFirstName=Julius&doctorLastName=Hibbert&date=8-17-2021&time=8:15AM&patientFirstName=john&patientLastName=Green&kind=New Patient
  delete http://127.0.0.1:5000/calendar?doctorFirstName=Algernop&doctorLastName=Krieger&date=8-17-2021&time=8:15AM&patientFirstName=jane&patientLastName=Green&kind=New Patient
#Assume no two doctors have the same firstname and lastname, if two doctors had the same first name and lastname,
# the calendar app would take in the doctor id rather than firstname and lastname for all the requests.

#Also assume no two patients have the same first and lastname.
# If this assumption was incorrect, the patient id could be passed instead of the patients first and lastname as input to the delete request.

Here is the versions of the libraries that I used.
Python 3.6.8
>>> import flask
>>> flask.__version__
'1.1.2'
>>> import sqlite3
>>> sqlite3.version
'2.6.0'
>>> sqlite3.sqlite_version
'3.22.0'
