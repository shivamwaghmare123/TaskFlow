# Task Management System

A beginner-friendly Django project for managing projects and tasks.

## Features
- User registration, login and logout
- Dashboard with task statistics
- Create, edit and delete projects
- Create, edit and delete tasks
- Assign tasks to users
- Priority and status management
- Due dates and overdue highlighting
- Search and filtering
- Task comments
- Bootstrap-based responsive UI
- SQLite database (easy to run locally)

## Run
```bash
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Open http://127.0.0.1:8000/

Optional admin:
```bash
python manage.py createsuperuser
python manage.py runserver
```
