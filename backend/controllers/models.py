from controllers.database import db
from datetime import datetime
from flask_security import UserMixin, RoleMixin

roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True) 
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    fs_token_uniquifier = db.Column(db.String(255), unique=True, nullable=False)

    roles = db.relationship('Role', secondary=roles_users, 
                            backref=db.backref('users', lazy='dynamic'))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True) 
    description = db.Column(db.String(255))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    roll_number = db.Column(db.String(20), unique=True, nullable=False)
    branch = db.Column(db.String(50))
    cgpa = db.Column(db.Float, default=0.0) 
    resume = db.Column(db.String(255)) 
    skills = db.Column(db.Text) 
    
    user = db.relationship('User', backref=db.backref('student_profile', uselist=False))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    hr_name= db.Column(db.String(50))
    mobile = db.Column(db.String(20))
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending') 
    user = db.relationship('User', backref=db.backref('company_profile', uselist=False))

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    company = db.relationship('Company', backref='drives') 
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_cgpa_required = db.Column(db.Float, default=0.0) 
    package_details = db.Column(db.String(100)) 
    status = db.Column(db.String(20), default='Pending') 
    deadline_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    applications = db.relationship('Application', backref='drive', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company_name": self.company.company_name if self.company else "Unknown",
            "status": self.status,
            "deadline_date": self.deadline_date.strftime('%Y-%m-%d'),
            "min_cgpa": self.min_cgpa_required,
            "description": self.description
        }

class Application(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    status = db.Column(db.String(50), default='Applied')
    application_date = db.Column(db.DateTime, default=datetime.utcnow)
    offer_letter_path = db.Column(db.String(255), nullable=True)
    __table_args__ = (db.UniqueConstraint('student_id', 'drive_id', name='_student_drive_uc'),)
    student = db.relationship('Student', backref=db.backref('my_applications', lazy=True))