from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from model import Patient, Doctor, Appointment, MedicalRecord, Report

# Database URL (replace with your actual database URL)
DATABASE_URL = 'sqlite:///hospital.db'
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Sample data for seeding the database
patients_data = [
    {
        'first_name': 'Ten',
        'last_name': 'Hag',
        'date_of_birth': datetime(1990, 5, 15),
        'contact_number': '555-123-4567',
        'email': 'ten.hag@example.com',
        'address': '123 Manchester St, City'
    },
    {
        'first_name': 'Jordan',
        'last_name': 'Sancho',
        'date_of_birth': datetime(1985, 8, 22),
        'contact_number': '555-987-6543',
        'email': 'jordansancho@example.com',
        'address': '456 Dortmund St, Town'
    },
    # Add more patient data here...
]

doctors_data = [
    {
        'first_name': 'Dr. Shadrack',
        'last_name': 'Kibet',
        'specialization': 'Neurosurgeon'
    },
    {
        'first_name': 'Dr. Colli',
        'last_name': 'Botum',
        'specialization': 'Physiotherapy'
    },
    # Add more doctor data here...
]

# Seeding Patients
for data in patients_data:
    patient = Patient(**data)
    session.add(patient)

# Seeding Doctors
for data in doctors_data:
    doctor = Doctor(**data)
    session.add(doctor)

# Commit the changes to the database
session.commit()

# Sample data for appointments
appointments_data = [
    {
        'patient_id': 1,
        'appointment_date': datetime(2023, 9, 10),
        'doctor_id': 1,
    },
    # Add more appointment data here...
]

# Seeding Appointments
for data in appointments_data:
    appointment = Appointment(**data)
    session.add(appointment)

# Sample data for medical records
medical_records_data = [
    {
        'patient_id': 1,
        'doctor_id': 1,
        'diagnosis': 'Sample diagnosis for patient 1.',
        'treatment_plan': 'Sample treatment plan for patient 1.',
        'medications': 'Medication A, Medication B',
    },
    {
        'patient_id': 2,
        'doctor_id': 2,
        'diagnosis': 'Sample diagnosis for patient 2.',
        'treatment_plan': 'Sample treatment plan for patient 2.',
        'medications': 'Medication C, Medication D',
    },
    # Add more medical record data here...
]

# Seeding Medical Records
for data in medical_records_data:
    medical_record = MedicalRecord(**data)
    session.add(medical_record)

# Sample data for reports
reports_data = [
    {
        'patient_id': 1,
        'report_type': 'X-Ray',
        'report_date': datetime(2023, 9, 6),
        'content': 'Report content for patient 1.'
    },
    {
        'patient_id': 2,
        'report_type': 'MRI',
        'report_date': datetime(2023, 9, 7),
        'content': 'Report content for patient 2.'
    },
    # Add more report data here...
]

# Seeding Reports
for data in reports_data:
    report = Report(**data)
    session.add(report)

# Commit the changes to the database
session.commit()

# Close the session
session.close()

print("Database seeding completed.")
