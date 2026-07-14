from flask import Flask, jsonify, request
from flask_login import current_user
from flask_security import Security
from flask_restful import Api
from flask_cors import CORS
from controllers.database import db
from controllers.config import config
from controllers.user_datastore import user_datastore
from flask_caching import Cache  
from celery import Celery 
from controllers.models import PlacementDrive

cache = Cache()

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['result_backend'],
        broker=app.config['broker_url']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery


def create_app():
    app= Flask(__name__)

    app.config.from_object(config)
    app.config['broker_url'] = 'redis://localhost:6379/0'
    app.config['result_backend'] = 'redis://localhost:6379/0'
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'

    db.init_app(app)
    cache.init_app(app)
    security = Security(app, user_datastore)


    api = Api(app, prefix='/api')

    with app.app_context():
        db.create_all()

        admin_role = user_datastore.find_or_create_role(name='admin', description='Placement Cell')
        company_role = user_datastore.find_or_create_role(name='company', description='Recruiters')
        student_role = user_datastore.find_or_create_role(name='student', description='Applicants')

        if not user_datastore.find_user(email='admin@gmail.com'):
            user_datastore.create_user(
                email='admin@gmail.com',
                password='admin123',
                roles=[admin_role]
            )
        db.session.commit()    

    return app,api

app,api=create_app()
CORS(
    app,
    resources={r"/api/*": {"origins": [
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]}}
)

celery_app = make_celery(app) 
@app.route('/')
def index():
    return{
        'message': 'Welcome to the Placement Management System API!'
    },200


@app.route('/api/all-drives', methods=['GET'])
@cache.cached(timeout=10) 
def get_drives():
    drives = PlacementDrive.query.filter_by(status='Approved').all()
    return jsonify([{
        "id": d.id,
        "title": d.title,
        "company_name": d.company.company_name if d.company else "Unknown",
        "status": d.status,
        "deadline_date": d.deadline_date.strftime('%Y-%m-%d'),
        "min_cgpa": d.min_cgpa_required,
        "description": d.description,
        "package": d.package_details
    } for d in drives])


from controllers.auth_apis import LoginAPI, LogoutAPI, RegisterAPI
api.add_resource(LoginAPI, '/login')
api.add_resource(LogoutAPI, '/logout')
api.add_resource(RegisterAPI, '/register')


from controllers.placement_apis import (
    PlacementDriveAPI, AdminDriveActionAPI, 
    ApplyDriveAPI, CompanyApplicationActionAPI,StudentSearchAPI 
)

from controllers.user_management_apis import AdminGlobalSearchAPI

from controllers.user_management_apis import (
    AdminStatsAPI, 
    AdminUserManagementAPI, 
    AdminStudentManagementAPI, 
    AdminDriveManagementAPI, 
    StudentProfileAPI,
    CompanyProfileAPI,AdminAnalyticsAPI
)

api.add_resource(AdminGlobalSearchAPI, '/admin/search')
api.add_resource(PlacementDriveAPI, '/drives')
api.add_resource(AdminDriveActionAPI, '/admin/drive/<int:drive_id>')
api.add_resource(StudentSearchAPI, '/student/search')


api.add_resource(ApplyDriveAPI, '/apply/<int:drive_id>')

api.add_resource(CompanyApplicationActionAPI, 
                 '/company/applications/<int:drive_id>', 
                 '/company/application/update/<int:application_id>')

api.add_resource(AdminStatsAPI, '/admin/stats')

api.add_resource(AdminAnalyticsAPI, '/admin/analytics-report')

api.add_resource(AdminUserManagementAPI, 
                 '/admin/companies', 
                 '/admin/company/<int:company_id>')

api.add_resource(AdminStudentManagementAPI, 
                 '/admin/students', 
                 '/admin/student/<int:student_id>')

api.add_resource(AdminDriveManagementAPI, 
                 '/admin/drives', 
                 '/admin/drive/<int:drive_id>')


api.add_resource(StudentProfileAPI, '/student/profile')


api.add_resource(CompanyProfileAPI, '/company/profile')


@app.route('/test-celery')
def test_celery():
    from controllers.tasks import export_applications_csv
    task = export_applications_csv.delay(1) 
    return f"Success! Task ID {task.id} has been sent to the Assistant."


@app.route('/api/admin/add-drive', methods=['POST'])
def add_drive():
    cache.delete('view//api/all-drives') 
    return {"message": "Drive added and cache updated"}

@app.route('/api/test-monthly-report')
def test_monthly_report():
    from controllers.tasks import monthly_activity_report
    monthly_activity_report.delay()
    return {"message": "Monthly HTML Report generation started!"}

@app.route('/api/test-export', methods=['GET']) 
def trigger_export():
    from controllers.tasks import export_applications_csv
    task = export_applications_csv.delay(current_user.id)
    return {"message": "Export started", "task_id": task.id}, 200

@app.route('/api/test-reminders')
def test_reminders():
    from controllers.tasks import daily_reminders
    daily_reminders.delay()
    return {"message": "Daily Reminder logic triggered in Celery!"}

if __name__ == '__main__':
    app.run(debug=True)