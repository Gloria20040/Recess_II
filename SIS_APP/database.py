# database.py - Database Operations
import datetime

from flask_sqlalchemy import SQLAlchemy
from models import db, Student

def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully!")
        
        if Student.query.count() == 0:
            add_sample_data()

def add_sample_data():
    sample_students = [
        Student(
            student_name='John Doe',
            registration_number='STU2024001',
            email='john.doe@university.edu',
            programme='Computer Science'
        ),
        Student(
            student_name='Jane Smith',
            registration_number='STU2024002',
            email='jane.smith@university.edu',
            programme='Information Technology'
        )
    ]
    
    for student in sample_students:
        db.session.add(student)
    db.session.commit()
    print("📚 Sample data added!")

def get_all_students():
    return Student.query.filter_by(is_active=True).all()

def get_student_by_name(name):
    return Student.query.filter(
        Student.student_name.contains(name),
        Student.is_active == True
    ).all()

def get_student_by_registration(registration_number):
    return Student.query.filter_by(registration_number=registration_number).first()

def add_student(student_data):
    try:
        existing = get_student_by_registration(student_data['registration_number'])
        if existing:
            return False, "Registration number already exists!", None
        
        existing_email = Student.query.filter_by(email=student_data['email']).first()
        if existing_email:
            return False, "Email already registered!", None
        
        new_student = Student(
            student_name=student_data['student_name'],
            registration_number=student_data['registration_number'],
            email=student_data['email'],
            programme=student_data['programme']
        )
        


        db.session.add(new_student)
        db.session.commit()
        return True, "Student registered successfully!", new_student
    
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}", None
    
def update_student(student_id, updated_data):
    '''update existing student record and confirm the change'''
    student = Student.query.get(student_id)
    if not student:
        return False, "Student not found!"

    try:
        new_registration_number = updated_data.get('registration_number')
        if new_registration_number and new_registration_number != student.registration_number:
            existing = get_student_by_registration(new_registration_number)
            if existing:
                return False, "Registration number already exists!"

        for key, value in updated_data.items():
            if hasattr(student, key) and value not in (None, ''):
                setattr(student, key, value)

        student.registration_date = datetime.datetime.utcnow()
        db.session.commit()
        return True, "Student updated successfully!"
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    
def delete_student_permanently(student_id):
    '''this permanently deletes a student record from the database'''
    student = Student.query.get(student_id)
    if not student:
        return False, "Student not found!"
    
    try:
        db.session.delete(student)
        db.session.commit()
        return True, "Student deleted successfully!"
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"
    
def soft_delete_student(student_id):
    '''this marks a student record as inactive instead of deleting it permanently'''
    student = Student.query.get(student_id)
    if not student:
        return False, "Student not found!"
    
    try:
        student.is_active = False
        db.session.commit()
        return True, "Student soft-deleted successfully!"
    except Exception as e:
        db.session.rollback()
        return False, f"Database error: {str(e)}"