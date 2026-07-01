from controllers.database import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin

# 1. Association table for Flask-Security (Standard)
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

# 2. THE UNIFIED USER MODEL (Admin, Company, and Student all live here)
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True) # Used for Blacklisting
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False) # For Flask-Security Token Management
    
    # Relationship to Roles
    roles = db.relationship('Role', secondary=roles_users, 
                            backref=db.backref('users', lazy='dynamic'))

# 3. ROLE MODEL
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True) # 'admin', 'student', 'company'
    description = db.Column(db.String(255))

# 4. STUDENT PROFILE (Details unique to students)
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100))
    roll_number = db.Column(db.String(20), unique=True)
    branch = db.Column(db.String(50))
    resume = db.Column(db.String(255)) # Path to file
    # Relationship
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

# 5. COMPANY PROFILE (Details unique to companies)
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100))
    hr_contact = db.Column(db.String(50))
    website = db.Column(db.String(100))
    is_approved = db.Column(db.Boolean(), default=False) # For Admin Approval (Page 6)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))

# 6. PLACEMENT DRIVE MODEL
class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text)  # Eligibility criteria (e.g., Min CGPA)
    package_details = db.Column(db.String(100)) # Salary info
    
    # Requirement 1c (Page 2): Admin must approve these
    is_approved = db.Column(db.Boolean(), default=False) 
    
    deadline_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='drive', lazy=True)

# 7. APPLICATION MODEL (The link between Student and Drive)
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    
    # Requirement 5m (Page 4): Status tracking
    # Possible values: 'Applied', 'Shortlisted', 'Selected', 'Rejected'
    status = db.Column(db.String(50), default='Applied')
    
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Page 8: Requirement to prevent multiple applications to same drive
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='_student_drive_uc'),)

    # Relationship to get student details easily from an application
    student = db.relationship('Student', backref=db.backref('my_applications', lazy=True))    