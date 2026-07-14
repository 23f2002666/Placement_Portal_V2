import os
import csv
from datetime import datetime, timedelta
from celery.schedules import crontab
from app import celery_app
from controllers.database import db
from controllers.models import PlacementDrive, Application, Student, User,Company

@celery_app.task
def export_applications_csv(user_id):
 
    student_profile = Student.query.filter_by(user_id=user_id).first()
    
    if not student_profile:
        return f"FAILED: No student profile found for User ID {user_id}"

    # 2. Now query using the actual student_profile.id
    results = db.session.query(Application, PlacementDrive, Company).join(
        PlacementDrive, Application.drive_id == PlacementDrive.id
    ).join(
        Company, PlacementDrive.company_id == Company.id
    ).filter(Application.student_id == student_profile.id).all()

    export_dir = 'exports'
    if not os.path.exists(export_dir):
        os.makedirs(export_dir)

    filename = f'{export_dir}/student_{user_id}_report.csv'

    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        
        writer.writerow([
            'Full Name', 
            'Roll Number', 
            'Branch', 
            'CGPA', 
            'Company Name', 
            'Drive Title', 
            'Status', 
            'Applied Date'
        ])
        
        for app, drive, company in results:
            writer.writerow([
                student_profile.full_name,
                student_profile.roll_number,
                student_profile.branch,
                student_profile.cgpa,
                company.company_name,
                drive.title,
                app.status,
                app.application_date.strftime('%Y-%m-%d')
            ])
            
    return f"COMPLETED: Exported {len(results)} rows for {student_profile.full_name}"


@celery_app.task
def export_applications_csv(user_id):
    from controllers.models import Student, Application, PlacementDrive, Company
    from controllers.database import db

    
    all_students = Student.query.all()
    print(f"DEBUG: You are searching for User ID: {user_id}")
    print(f"DEBUG: Currently in Student Table: ")
    for s in all_students:
        print(f"   -> Student ID: {s.id} | Linked to User ID: {s.user_id} | Name: {s.full_name}")
 

    student_profile = Student.query.filter_by(user_id=user_id).first()
    
    if not student_profile:
        return f"FAILED: User ID {user_id} has no Student Profile row."

   
    results = db.session.query(Application, PlacementDrive, Company).join(
        PlacementDrive, Application.drive_id == PlacementDrive.id
    ).join(
        Company, PlacementDrive.company_id == Company.id
    ).filter(Application.student_id == student_profile.id).all()

   
    filename = f'exports/student_{user_id}_report.csv'
    if not os.path.exists('exports'): os.makedirs('exports')
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Full Name', 'Roll Number', 'Branch', 'CGPA', 'Company', 'Drive', 'Status', 'Date'])
        for app, drive, company in results:
            writer.writerow([student_profile.full_name, student_profile.roll_number, student_profile.branch, 
                             student_profile.cgpa, company.company_name, drive.title, app.status, 
                             app.application_date.strftime('%Y-%m-%d')])
            
    return f"COMPLETED: Exported {len(results)} rows for {student_profile.full_name}"

@celery_app.task
def daily_reminders():
    """
    Checks for drives ending tomorrow.
    Requirement: Runs daily at a chosen time.
    """
    from sqlalchemy import func
    from controllers.models import PlacementDrive
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    

    upcoming_drives = PlacementDrive.query.filter(func.date(PlacementDrive.deadline_date) == tomorrow).all()
    
    for drive in upcoming_drives:
        
        print(f"--- [EXTERNAL NOTIFICATION SENT] ---")
        print(f"TO: All Students")
        print(f"VIA: Google Chat Webhook / Email")
        print(f"MESSAGE: Reminder! {drive.title} deadline is {drive.deadline_date}")
        print(f"-------------------------------------")
    
    return f"Processed {len(upcoming_drives)} reminders for {tomorrow}."





@celery_app.task
def monthly_activity_report():
    from controllers.models import Student, Company, Application, PlacementDrive
    from controllers.database import db
    from datetime import datetime

    
    students = Student.query.all()
    student_rows_html = ""
    for s in students:
       
        selection = Application.query.filter_by(student_id=s.id, status='Selected').first()
        placed_at = selection.drive.company.company_name if selection else "Pending"
        status_color = "#198754" if placed_at != "Pending" else "#6c757d"
        
        student_rows_html += f"""
            <tr>
                <td>{s.full_name}</td>
                <td>{s.roll_number}</td>
                <td>{s.branch}</td>
                <td>{s.cgpa}</td>
                <td style="color: {status_color}; font-weight: bold;">{placed_at}</td>
            </tr>
        """

  
    companies = Company.query.all()
    company_cards_html = ""
    for c in companies:
        drive_list_html = ""
        total_hired = 0
        for drive in c.drives:
            hired_count = Application.query.filter_by(drive_id=drive.id, status='Selected').count()
            total_hired += hired_count
            drive_list_html += f"<li>{drive.title}: <strong>{hired_count} Hired</strong></li>"
        
        company_cards_html += f"""
            <div class="company-card">
                <h3>{c.company_name}</h3>
                <p>Total Drives: {len(c.drives)}</p>
                <ul>{drive_list_html}</ul>
                <div class="total">Total Hired: {total_hired}</div>
            </div>
        """


    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', sans-serif; padding: 40px; background-color: #f8f9fa; color: #333; }}
            h1, h2 {{ color: #2c3e50; border-bottom: 2px solid #0d6efd; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; background: white; }}
            th, td {{ padding: 12px; border: 1px solid #dee2e6; text-align: left; }}
            th {{ background-color: #0d6efd; color: white; }}
            .company-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px; }}
            .company-card {{ background: white; padding: 20px; border-radius: 10px; border: 1px solid #ddd; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
            .total {{ font-size: 1.2rem; font-weight: bold; color: #198754; margin-top: 10px; text-align: right; }}
            ul {{ font-size: 0.9rem; color: #555; }}
        </style>
    </head>
    <body>
        <h1>Monthly Placement Activity Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>

        <h2>Part 1: Student Placement Tracking</h2>
        <table>
            <thead>
                <tr>
                    <th>Name</th><th>Roll No</th><th>Branch</th><th>CGPA</th><th>Placed At</th>
                </tr>
            </thead>
            <tbody>
                {student_rows_html}
            </tbody>
        </table>

        <h2 style="margin-top: 50px;">Part 2: Recruiter Performance Breakdown</h2>
        <div class="company-grid">
            {company_cards_html}
        </div>
    </body>
    </html>
    """

  
    with open('monthly_report.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return "Detailed Monthly Report Generated."


celery_app.conf.beat_schedule = {
    'daily-deadline-reminders': {
        'task': 'controllers.tasks.daily_reminders',
        'schedule': crontab(hour=8, minute=0),
    },
    'monthly-admin-activity-report': {
        'task': 'controllers.tasks.monthly_activity_report',
        'schedule': crontab(day_of_month=1, hour=0, minute=0),
    },
}