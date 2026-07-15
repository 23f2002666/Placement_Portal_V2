# Placement Portal Application - V2 (MAD-II)

A centralized web application for managing campus recruitment, allowing Admin (Institute), Companies, and Students to interact seamlessly.

## 🚀 Features
- **Role-Based Access:** Admin, Student, and Company dashboards.
- **Job Management:** Companies can post, edit, and close job drives.
- **Application Tracking:** Students can apply and track status (Shortlisted/Selected/Rejected) in real-time.
- **Admin Analytics:** Global search, student/company management, and weekly analytics summary.
- **Automated Tasks:** 
    - Daily reminders for upcoming job deadlines.
    - Monthly HTML performance reports.
    - Asynchronous CSV export for student application history.
- **Performance:** Optimized API responses using Redis Caching.

## 🛠️ Tech Stack
- **Backend:** Flask (Python), Flask-RESTful, Flask-Security, SQLAlchemy.
- **Frontend:** Vue.js 3, Bootstrap 5,CSS
- **Database:** SQLAlchemy.
- **Task Queue:** Celery + Redis.
- **Caching:** Redis.

## 🛠️ Setup Instructions

### 1. Prerequisites
- Python 3.x
- Node.js & npm
- Redis Server

### 2. Backend Setup

```bash
cd backend
python app.py
```

### 3. Frontend Setup

```bash
npm install
npm run dev
```
### 4. Redis and Celety Setup

```bash
 python3 -m venv venv
source venv/bin/activate
pip install
pip install -r requirements.txt
ctrl +c 
cd backend
celery -A controllers.tasks.celery_app worker --beat --loglevel=info
```


