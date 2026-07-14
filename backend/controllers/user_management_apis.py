from flask_restful import Resource
from flask import request
from flask_security import auth_token_required, roles_required, current_user
from controllers.database import db
from controllers.models import User, Student, Company, Application, PlacementDrive
from sqlalchemy import or_


class AdminStatsAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        return {
            "total_students": Student.query.count(),
            "total_companies": Company.query.count(),
            "total_drives": PlacementDrive.query.count()
        }, 200


class AdminUserManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        companies = Company.query.all()
        
        output = []
        for c in companies:
            drive_count = len(c.drives)
            selected_count = 0
            for drive in c.drives:
                selected_count += Application.query.filter_by(
                    drive_id=drive.id, 
                    status='Selected'
                ).count()

            output.append({
                "id": c.id, 
                "name": c.company_name, 
                "status": c.status, 
                "user_id": c.user_id,
                "email": c.user.email,
                "is_active": c.user.active,
                "drive_count": drive_count,       
                "selected_count": selected_count   
            })
            
        return output, 200
    @auth_token_required
    @roles_required('admin')
    def put(self, company_id): 
        company = Company.query.get_or_404(company_id)
        data = request.get_json()
        new_status = data.get('status')
        
        company.status = new_status
        user = User.query.get(company.user_id)
        user.active = False if new_status == 'Rejected' else True
            
        db.session.commit()
        return {"message": f"Company {company.company_name} is now {new_status}"}, 200

class AdminStudentManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        students = Student.query.all()
        return [{
            "id": s.id,
            "full_name": s.full_name,
            "roll_number": s.roll_number,
            "email": s.user.email,
            "user_id": s.user_id,
            "is_active": s.user.active
        } for s in students], 200

    @auth_token_required
    @roles_required('admin')
    def put(self, student_id):
        print(f"--- DEBUG: Received Student ID: {student_id} ---")
        student = Student.query.get_or_404(student_id)
        print(f"--- DEBUG: Found Student: {student.full_name} linked to User ID: {student.user_id} ---")
        user = User.query.get(student.user_id)
        if not user:
            print("--- DEBUG: FAILED - User account not found! ---")
            return {"message": "User not found"}, 404
        old_status = user.active
        user.active = not user.active 
        print(f"--- DEBUG: Changing active from {old_status} to {user.active} ---")
        db.session.commit()
        status_text = "Active" if user.active else "Blacklisted"
        return {"message": f"Student status updated to {status_text}"}, 200

    @auth_token_required
    @roles_required('admin')
    def delete(self, student_id):
        student = Student.query.get_or_404(student_id)
        user = User.query.get(student.user_id)
        db.session.delete(student)
        db.session.delete(user)
        db.session.commit()
        return {"message": "Student deleted permanently"}, 200

class AdminDriveManagementAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        drives = PlacementDrive.query.all()
        return [{
            "id": d.id,
            "title": d.title,
            "company_name": d.company.company_name if d.company else "Unknown",
            "status": d.status,
            "min_cgpa": d.min_cgpa_required,
            "deadline": d.deadline_date.strftime('%Y-%m-%d')
        } for d in drives], 200

    @auth_token_required
    @roles_required('admin')
    def put(self, drive_id):
        drive = PlacementDrive.query.get_or_404(drive_id)
        drive.status = "Approved"
        db.session.commit()
        return {"message": "Placement drive approved"}, 200

class StudentProfileAPI(Resource):
    @auth_token_required
    @roles_required('student')
    def get(self):
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student record not found"}, 404
        apps = Application.query.filter_by(student_id=student.id).all()
        return {
            "profile": {
                "name": student.full_name,
                "roll": student.roll_number,
                "dept": student.branch,  
                "cgpa": student.cgpa,
                "resume": student.resume,
                "skills": getattr(student, 'skills', ''), 
                "edu": "Not Set",        
                "address": "Not Set"     
            },
            "applications": [{
                "application_id": a.id,     
                "drive_id": a.drive_id,     
                "drive_title": a.drive.title, 
                "status": a.status,  
                "company_name": a.drive.company.company_name,         
                "date": a.application_date.strftime('%Y-%m-%d')
            } for a in apps]
        }, 200

    @auth_token_required
    @roles_required('student')
    def put(self):
        # 1. Find the student record
        student = Student.query.filter_by(user_id=current_user.id).first()
        if not student:
            return {"message": "Student not found"}, 404

        # 2. Get the new data from the Vue request
        data = request.get_json()

        # 3. Update the fields in the Database
        # We use .get('key', current_value) to ensure we don't overwrite with empty data
        student.full_name = data.get('name', student.full_name)
        student.roll_number = data.get('roll', student.roll_number)
        student.branch = data.get('dept', student.branch)
        student.cgpa = data.get('cgpa', student.cgpa)
        
        # If your model has a skills column
        if hasattr(student, 'skills'):
            student.skills = data.get('skills', student.skills)

        # 4. Save changes to placement.db
        try:
            db.session.commit()
            return {"message": "Profile updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Error saving profile: " + str(e)}, 500
        


class CompanyProfileAPI(Resource):
    @auth_token_required
    @roles_required('company')
    def get(self):
        from controllers.models import Company
        company = Company.query.filter_by(user_id=current_user.id).first()
        return {
            "company_name": company.company_name,
            "email": current_user.email,
            "hr_name": company.hr_name,
            "mobile": company.mobile, 
            "address": company.description,
            "status": company.status
        }, 200

    @auth_token_required
    @roles_required('company')
    def put(self):
        from controllers.models import Company
        data = request.get_json()
        company = Company.query.filter_by(user_id=current_user.id).first()
        
        if not company:
            return {"message": "Company not found"}, 404
        company.company_name = data.get('company_name', company.company_name)
        company.hr_name= data.get('hr_name', company.hr_name)
        company.mobile = data.get('mobile', company.mobile)
        company.description = data.get('address', company.description)
        db.session.commit()
        return {"message": "Profile updated successfully"}, 200      

class AdminAnalyticsAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        students = Student.query.all()
        student_data = []
        for s in students:
            selection = Application.query.filter_by(student_id=s.id, status='Selected').first()
            student_data.append({
                "name": s.full_name,
                "roll": s.roll_number,
                "dept": s.branch,
                "cgpa": s.cgpa,
                "placed_at": selection.drive.company.company_name if selection else "Pending"
            })
        companies = Company.query.all()
        company_data = []
        for c in companies:
            drive_details = []
            grand_total = 0
            for drive in c.drives:
                selected_count = Application.query.filter_by(drive_id=drive.id, status='Selected').count()
                grand_total += selected_count
                drive_details.append({
                    "job_title": drive.title,
                    "hired": selected_count
                })
            company_data.append({
                "company_name": c.company_name,
                "email": c.user.email,
                "total_drives": len(c.drives),
                "drive_breakdown": drive_details,
                "total_hired": grand_total
            })
        return {"students": student_data, "companies": company_data}, 200

class AdminGlobalSearchAPI(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        category = request.args.get('type') 
        query_str = request.args.get('q', '').strip()
        if category == 'student':
            results = db.session.query(Student).join(User).filter(
                or_(
                    Student.full_name.ilike(f'%{query_str}%'),
                    Student.roll_number.ilike(f'%{query_str}%'),
                    User.email.ilike(f'%{query_str}%')
                )
            ).all()
            return [{
                "id": s.id, "name": s.full_name, "roll": s.roll_number, "email": s.user.email, "status": "Active" if s.user.active else "Blacklisted"
            } for s in results]
        elif category == 'company':
            results = db.session.query(Company).join(User).filter(
                or_(
                    Company.company_name.ilike(f'%{query_str}%'),
                    User.email.ilike(f'%{query_str}%')
                )
            ).all()
            return [{
                "id": c.id, "name": c.company_name, "email": c.user.email, "status": c.status
            } for c in results]

        elif category == 'drive':
            results = db.session.query(PlacementDrive).join(Company).filter(
                or_(
                    PlacementDrive.title.ilike(f'%{query_str}%'),
                    Company.company_name.ilike(f'%{query_str}%')
                )
            ).all()
            return [{
                "id": d.id, "title": d.title, "company": d.company.company_name, "status": d.status
            } for d in results]

        return {"message": "Invalid type"}, 400    