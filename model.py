from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime


#define the base class for declarative models
Base = declarative_base()

class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(DateTime)
    contact_number = Column(String(15))
    email = Column(String(100))
    address = Column(Text)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Doctor(Base):
    __tablename__ = 'doctors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    specialization = Column(String(100))

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"

class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    appointment_date = Column(DateTime)
    doctor_id = Column(Integer, ForeignKey('doctors.id'))

    patient = relationship('Patient', backref='appointments')
    doctor = relationship('Doctor', backref='appointments')

    def __str__(self):
        return f"Appointment for {self.patient} with Dr. {self.doctor}"

class MedicalRecord(Base):
    __tablename__ = 'medical_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    doctor_id = Column(Integer, ForeignKey('doctors.id'))
    diagnosis = Column(Text)
    treatment_plan = Column(Text)
    medications = Column(Text)
    date_created = Column(DateTime, default=datetime.utcnow)

    patient = relationship('Patient', backref='medical_records')
    doctor = relationship('Doctor', backref='medical_records')

    def __str__(self):
        return f"Medical Record for {self.patient}"

class Report(Base):
    __tablename__ = 'reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    report_type = Column(String(100))
    report_date = Column(DateTime)
    content = Column(Text)

    patient = relationship('Patient', backref='reports')

    def __str__(self):
        return f"Report for {self.patient} ({self.report_type})"


