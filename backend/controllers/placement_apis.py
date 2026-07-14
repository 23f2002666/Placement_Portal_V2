from flask_restful import Resource, reqparse
from flask import request
from flask_security import auth_token_required, roles_required, current_user
from controllers.database import db
from controllers.models import PlacementDrive, Application, Student, Company
from datetime import datetime
from sqlalchemy import or_

drive_parser = reqparse.RequestParser()
drive_parser.add_argument('title', required=True, help="Title is required")
drive_parser.add_argument('description', required=True)
drive_parser.add_argument('min_cgpa_required', type=float, default=0.0)
drive_parser.add_argument('package_details', required=True)
drive_parser.add_argument('deadline_date', required=True, help="Format: YYYY-MM-DD")

class PlacementDriveAPI(Resource):
    @auth_token_required
    def get(self):
        if current_user.has_role('student'):
            drives = PlacementDrive.query.filter_by(status='Approved').all()
        
        elif current_user.has_role('company'):
            company = Company.query.filter_by(user_id=current_user.id).first()
            if not company: return [], 200
            drives = PlacementDrive.query.filter_by(company_id=company.id).all()   
        elif current_user.has_role('admin'):
            drives = PlacementDrive.query.all()
            
        return [{
            "id": d.id, 
            "title": d.title, 
            "company_name": d.company.company_name if d.company else "Unknown",
            "status": d.status, 
            "deadline_date": d.deadline_date.strftime('%Y-%m-%d'),
            "min_cgpa": d.min_cgpa_required,
            "description": d.description,
            "applicant_count": len(d.applications) 
        } for d in drives], 200

    @auth_token_required
    @roles_required('company')
    def post(self):
        company = Company.query.filter_by(user_id=current_user.id).first()
        if company.status != 'Approved':
            return {"message": "Your company profile must be approved by Admin first"}, 403

        args = drive_parser.parse_args()
        new_drive = PlacementDrive(
            company_id=company.id,
            title=args['title'],
            description=args['description'],
            min_cgpa_required=args['min_cgpa_required'],
            package_details=args['package_details'],
            deadline_date=datetime.strptime(args['deadline_date'], '%Y-%m-%d'),
            status='Pending'
        )
        db.session.add(new_drive)
        db.session.commit()
        return {"message": "Drive created and sent for Admin approval"}, 201

    @auth_token_required
    @roles_required('company')
    def put(self):
        drive_id = request.args.get('id')
        drive = PlacementDrive.query.get_or_404(drive_id)
        company = Company.query.filter_by(user_id=current_user.id).first()
        if drive.company_id != company.id:
            return {"message": "Unauthorized"}, 403

        data = request.get_json()
        if 'title' in data: drive.title = data['title']
        if 'description' in data: drive.description = data['description']
        if 'min_cgpa_required' in data: drive.min_cgpa_required = data['min_cgpa_required']
        if 'package_details' in data: drive.package_details = data['package_details']
        
        if 'status' in data: 
            new_status = data['status']
            if new_status == 'Approved':
                drive.status = 'Pending'
            else:
                drive.status = new_status    
        if 'deadline_date' in data:
            drive.deadline_date = datetime.strptime(data['deadline_date'], '%Y-%m-%d')
        db.session.commit()
        return {"message": "Updated successfully"}, 200

    @auth_token_required
    @roles_required('company')
    def delete(self):
        drive_id = request.args.get('id')
        drive = PlacementDrive.query.get_or_404(drive_id)
        company = Company.query.filter_by(user_id=current_user.id).first()
        if drive.company_id != company.id:
            return {"message": "Unauthorized"}, 403

        db.session.delete(drive)
        db.session.commit()
        return {"message": "Drive deleted successfully"}, 200

class AdminDriveActionAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def post(self, drive_id):
        drive = PlacementDrive.query.get_or_404(drive_id)
        action = request.json.get('action') 
        if action == 'Approve':
            drive.status = 'Approved'
        else:
            drive.status = 'Rejected'
        db.session.commit()
        return {"message": f"Drive {action}ed successfully"}
    
class StudentSearchAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        query_str = request.args.get('q', '').strip()
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student profile not found"}, 404
        search_results = db.session.query(PlacementDrive).join(Company).filter(
            PlacementDrive.status == 'Approved', 
             or_(
                Company.company_name.ilike(f'%{query_str}%'),
                PlacementDrive.title.ilike(f'%{query_str}%')
            )
        ).all()

        output = []
        for drive in search_results:
            existing_app = Application.query.filter_by(
                student_id=student.id, 
                drive_id=drive.id
            ).first()

            output.append({
                "id": drive.id,
                "title": drive.title,
                "company_name": drive.company.company_name,
                "deadline_date": drive.deadline_date.strftime('%Y-%m-%d'),
                "min_cgpa": drive.min_cgpa_required,
                "is_applied": True if existing_app else False,
                "status": existing_app.status if existing_app else "Not Applied"
            })

        return output, 200

class ApplyDriveAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def post(self, drive_id):
        student = Student.query.filter_by(user_id=current_user.id).first()
        drive = PlacementDrive.query.get_or_404(drive_id)
        if student.cgpa < drive.min_cgpa_required:
            return {"message": f"Ineligible. Minimum CGPA required is {drive.min_cgpa_required}"}, 400
        if datetime.utcnow() > drive.deadline_date:
            return {"message": "Application deadline has passed"}, 400
        existing = Application.query.filter_by(student_id=student.id, drive_id=drive_id).first()
        if existing:
            return {"message": "You have already applied to this drive"}, 400
        new_app = Application(student_id=student.id, drive_id=drive_id, status='Applied')
        db.session.add(new_app)
        db.session.commit()
        return {"message": "Applied successfully"}, 201

class CompanyApplicationActionAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self, drive_id):
        apps = Application.query.filter_by(drive_id=drive_id).all()
        return [{
        "application_id": a.id,
        "status": a.status,
        "student_info": {
            "name": a.student.full_name,
            "email": a.student.user.email, 
            "roll": a.student.roll_number, 
            "branch": a.student.branch,    
            "cgpa": a.student.cgpa,
            "skills": a.student.skills or "No skills listed"
        }
        } for a in apps], 200

    @auth_token_required
    @roles_required('company')
    def put(self, application_id):
        app = Application.query.get_or_404(application_id)
        new_status = request.json.get('status')
        app.status = new_status
        db.session.commit()
        return {"message": f"Application status updated to {new_status}"}