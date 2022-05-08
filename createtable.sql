DROP TABLE IF EXISTS doctor;

CREATE TABLE doctor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT NOT NULL,
    lastName TEXT NOT NULL
);

DROP TABLE IF EXISTS appointment;

CREATE TABLE appointment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patientFirstName TEXT NOT NULL,
    patientLastName TEXT NOT NULL,
    dateAppointment TEXT NOT NULL,
    timeAppointment TEXT NOT NULL,
    kind TEXT NOT NULL,
    doctorId INTEGER NOT NULL
);
