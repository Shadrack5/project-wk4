import click
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from model import Patient, Doctor, Appointment, MedicalRecord, Report

# Database URL (replace with your actual database URL)
DATABASE_URL = 'sqlite:///hospital.db'
engine = create_engine(DATABASE_URL)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

@click.group()
def cli():
    pass

# Patients CLI commands

@cli.command()
@click.option('--first-name', prompt='First Name', help='First name of the patient')
@click.option('--last-name', prompt='Last Name', help='Last name of the patient')
@click.option('--date-of-birth', prompt='Date of Birth (YYYY-MM-DD)', type=str, help='Date of birth of the patient (YYYY-MM-DD)')
@click.option('--contact-number', prompt='Contact Number', help='Contact number of the patient')
@click.option('--email', prompt='Email', help='Email of the patient')
@click.option('--address', prompt='Address', help='Address of the patient')
def add_patient(first_name, last_name, date_of_birth, contact_number, email, address):
    """Add a new patient."""
    try:
        date_of_birth = datetime.strptime(date_of_birth, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    new_patient = Patient(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        contact_number=contact_number,
        email=email,
        address=address
    )

    session.add(new_patient)
    session.commit()
    print(f"Added new patient: {first_name} {last_name} (ID: {new_patient.id}).")


@cli.command()
@click.option('--patient-id', type=int, help='Patient ID to delete')
def delete_patient(patient_id):
    """Delete a patient by ID."""
    patient = session.query(Patient).filter_by(id=patient_id).first()
    if patient:
        session.delete(patient)
        session.commit()
        print(f"Deleted patient with ID {patient_id}.")
    else:
        print(f"Patient with ID {patient_id} not found.")

@cli.command()
@click.option('--doctor-id', type=int, help='Doctor ID to delete')
def delete_doctor(doctor_id):
    """Delete a doctor by ID."""
    doctor = session.query(Doctor).filter_by(id=doctor_id).first()
    if doctor:
        session.delete(doctor)
        session.commit()
        print(f"Deleted doctor with ID {doctor_id}.")
    else:
        print(f"Doctor with ID {doctor_id} not found.")



@cli.command()
@click.option('--patient-id', type=int, prompt='Patient ID', help='Patient ID for the appointment')
@click.option('--doctor-id', type=int, prompt='Doctor ID', help='Doctor ID for the appointment')
@click.option('--appointment-date', prompt='Appointment Date (YYYY-MM-DD)', type=str, help='Appointment date (YYYY-MM-DD)')
def add_appointment(patient_id, doctor_id, appointment_date):
    """Add a new appointment."""
    try:
        appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    new_appointment = Appointment(
        patient_id=patient_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date
    )

    session.add(new_appointment)
    session.commit()
    print(f"Added new appointment for Patient ID {patient_id} with Doctor ID {doctor_id} on {appointment_date} (ID: {new_appointment.id}).")

@cli.command()
@click.option('--appointment-id', type=int, prompt='Appointment ID', help='Appointment ID to delete')
def delete_appointment(appointment_id):
    """Delete an appointment by ID."""
    appointment = session.query(Appointment).filter_by(id=appointment_id).first()
    if appointment:
        session.delete(appointment)
        session.commit()
        print(f"Deleted appointment with ID {appointment_id}.")
    else:
        print(f"Appointment with ID {appointment_id} not found.")

@cli.command()
def view_appointments():
    """View all appointments."""
    appointments = session.query(Appointment).all()
    for appointment in appointments:
        patient_name = appointment.patient.first_name + " " + appointment.patient.last_name if appointment.patient else "[No Patient]"
        doctor_name = "Dr. " + appointment.doctor.first_name + " " + appointment.doctor.last_name if appointment.doctor else "[No Doctor]"
        print(f"ID: {appointment.id}, Patient: {patient_name}, Doctor: {doctor_name}, Date: {appointment.appointment_date}")



# Medical Records CLI commands

@cli.command()
@click.option('--patient-id', type=int, prompt='Patient ID', help='Patient ID for the medical record')
@click.option('--doctor-id', type=int, prompt='Doctor ID', help='Doctor ID for the medical record')
@click.option('--diagnosis', prompt='Diagnosis', help='Diagnosis for the medical record')
@click.option('--treatment-plan', prompt='Treatment Plan', help='Treatment plan for the medical record')
@click.option('--medications', prompt='Medications', help='Medications for the medical record')
def add_medical_record(patient_id, doctor_id, diagnosis, treatment_plan, medications):
    """Add a new medical record."""
    new_medical_record = MedicalRecord(
        patient_id=patient_id,
        doctor_id=doctor_id,
        diagnosis=diagnosis,
        treatment_plan=treatment_plan,
        medications=medications
    )

    session.add(new_medical_record)
    session.commit()
    print(f"Added new medical record for Patient ID {patient_id} with Doctor ID {doctor_id} (ID: {new_medical_record.id}).")

@cli.command()
@click.option('--medical-record-id', type=int, prompt='Medical Record ID', help='Medical Record ID to delete')
def delete_medical_record(medical_record_id):
    """Delete a medical record by ID."""
    medical_record = session.query(MedicalRecord).filter_by(id=medical_record_id).first()
    if medical_record:
        session.delete(medical_record)
        session.commit()
        print(f"Deleted medical record with ID {medical_record_id}.")
    else:
        print(f"Medical record with ID {medical_record_id} not found.")

@cli.command()
def view_medical_records():
    """View all medical records."""
    medical_records = session.query(MedicalRecord).all()
    for medical_record in medical_records:
        print(f"ID: {medical_record.id}, Patient: {medical_record.patient.first_name} {medical_record.patient.last_name}, Doctor: Dr. {medical_record.doctor.first_name} {medical_record.doctor.last_name}, Diagnosis: {medical_record.diagnosis}")




# ...

# Reports CLI commands

@cli.command()
@click.option('--patient-id', type=int, prompt='Patient ID', help='Patient ID for the report')
@click.option('--report-type', prompt='Report Type', help='Type of the report')
@click.option('--report-date', prompt='Report Date (YYYY-MM-DD)', type=str, help='Report date (YYYY-MM-DD)')
@click.option('--content', prompt='Report Content', help='Content of the report')
def add_report(patient_id, report_type, report_date, content):
    """Add a new report."""
    try:
        report_date = datetime.strptime(report_date, '%Y-%m-%d')
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD format.")
        return

    new_report = Report(
        patient_id=patient_id,
        report_type=report_type,
        report_date=report_date,
        content=content
    )

    session.add(new_report)
    session.commit()
    print(f"Added new report for Patient ID {patient_id} (ID: {new_report.id}).")

@cli.command()
@click.option('--report-id', type=int, prompt='Report ID', help='Report ID to delete')
def delete_report(report_id):
    """Delete a report by ID."""
    report = session.query(Report).filter_by(id=report_id).first()
    if report:
        session.delete(report)
        session.commit()
        print(f"Deleted report with ID {report_id}.")
    else:
        print(f"Report with ID {report_id} not found.")

@cli.command()
def view_reports():
    """View all reports."""
    reports = session.query(Report).all()
    for report in reports:
        print(f"ID: {report.id}, Patient: {report.patient.first_name} {report.patient.last_name}, Type: {report.report_type}, Date: {report.report_date}")

if __name__ == '__main__':
    cli()