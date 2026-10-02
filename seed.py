"""
Database Seeder for EmployeeHub.
Creates initial Admin, HR users, Departments, and realistic sample Employees.
Credentials are automatically loaded from .env.
"""
import os
from datetime import date, timedelta
from app import create_app, db
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee

def seed_all():
    print("Beginning database seeding...")

    # Create tables if not existing
    db.create_all()

    # Load credentials from environment
    admin_name = os.environ.get('DEFAULT_ADMIN_NAME', 'System Administrator')
    admin_username = os.environ.get('DEFAULT_ADMIN_USERNAME', 'admin')
    admin_email = os.environ.get('DEFAULT_ADMIN_EMAIL', 'admin@employeehub.com')
    admin_password = os.environ.get('DEFAULT_ADMIN_PASSWORD', 'admin123')

    hr_name = os.environ.get('DEFAULT_HR_NAME', 'Sarah Jenkins')
    hr_username = os.environ.get('DEFAULT_HR_USERNAME', 'hr_manager')
    hr_email = os.environ.get('DEFAULT_HR_EMAIL', 'hr@employeehub.com')
    hr_password = os.environ.get('DEFAULT_HR_PASSWORD', 'hr123')

    # 1. Seed or Update Admin User
    admin = User.query.filter((User.username == admin_username) | (User.email == admin_email)).first()
    if not admin:
        admin = User(
            username=admin_username,
            email=admin_email,
            full_name=admin_name,
            role='Admin'
        )
        admin.set_password(admin_password)
        db.session.add(admin)
        print(f"-> Created Admin user from .env: {admin_email} / {admin_password}")
    else:
        admin.email = admin_email
        admin.set_password(admin_password)
        print(f"-> Updated Admin password from .env for: {admin_email}")

    # 2. Seed or Update HR User
    hr = User.query.filter((User.username == hr_username) | (User.email == hr_email)).first()
    if not hr:
        hr = User(
            username=hr_username,
            email=hr_email,
            full_name=hr_name,
            role='HR'
        )
        hr.set_password(hr_password)
        db.session.add(hr)
        print(f"-> Created HR user from .env: {hr_email} / {hr_password}")
    else:
        hr.email = hr_email
        hr.set_password(hr_password)
        print(f"-> Updated HR password from .env for: {hr_email}")

    db.session.commit()

    # 3. Seed Departments
    dept_data = [
        {'name': 'Engineering', 'code': 'ENG', 'description': 'Cloud infrastructure, backend microservices, and software engineering.'},
        {'name': 'Human Resources', 'code': 'HR', 'description': 'Talent management, organizational development, and employee success.'},
        {'name': 'Product & Design', 'code': 'PRD', 'description': 'Product management, user research, and modern SaaS UI/UX.'},
        {'name': 'Finance & Accounting', 'code': 'FIN', 'description': 'Financial reporting, audit compliance, and corporate payroll.'},
        {'name': 'Marketing & Sales', 'code': 'MKT', 'description': 'Growth marketing, brand outreach, and corporate client partnerships.'}
    ]

    dept_map = {}
    for d in dept_data:
        existing = Department.query.filter_by(code=d['code']).first()
        if not existing:
            dept_obj = Department(name=d['name'], code=d['code'], description=d['description'])
            db.session.add(dept_obj)
            db.session.flush()
            dept_map[d['code']] = dept_obj
        else:
            dept_map[d['code']] = existing

    db.session.commit()
    print("-> Departments seeded successfully.")

    # 4. Seed Sample Employees
    if Employee.query.count() == 0:
        sample_employees = [
            {
                'employee_id': 'EMP-1001',
                'first_name': 'Alexander',
                'last_name': 'Wright',
                'email': 'alexander.wright@employeehub.com',
                'phone': '+1 (555) 234-5678',
                'gender': 'Male',
                'department_id': dept_map['ENG'].id,
                'designation': 'Lead DevOps Architect',
                'salary': 9500.00,
                'joining_date': date.today() - timedelta(days=720),
                'status': 'Active',
                'address': '742 Evergreen Terrace, Springfield, OR'
            },
            {
                'employee_id': 'EMP-1002',
                'first_name': 'Sophia',
                'last_name': 'Martinez',
                'email': 'sophia.martinez@employeehub.com',
                'phone': '+1 (555) 345-6789',
                'gender': 'Female',
                'department_id': dept_map['PRD'].id,
                'designation': 'Principal UI/UX Designer',
                'salary': 8200.00,
                'joining_date': date.today() - timedelta(days=450),
                'status': 'Active',
                'address': '124 Conch Street, Bikini Bottom, WA'
            },
            {
                'employee_id': 'EMP-1003',
                'first_name': 'Liam',
                'last_name': 'Chen',
                'email': 'liam.chen@employeehub.com',
                'phone': '+1 (555) 456-7890',
                'gender': 'Male',
                'department_id': dept_map['ENG'].id,
                'designation': 'Senior Backend Engineer',
                'salary': 8800.00,
                'joining_date': date.today() - timedelta(days=320),
                'status': 'Active',
                'address': '221B Baker Street, London, CA'
            },
            {
                'employee_id': 'EMP-1004',
                'first_name': 'Emily',
                'last_name': 'Watson',
                'email': 'emily.watson@employeehub.com',
                'phone': '+1 (555) 567-8901',
                'gender': 'Female',
                'department_id': dept_map['HR'].id,
                'designation': 'HR Operations Specialist',
                'salary': 5600.00,
                'joining_date': date.today() - timedelta(days=180),
                'status': 'Active',
                'address': '350 Fifth Avenue, New York, NY'
            },
            {
                'employee_id': 'EMP-1005',
                'first_name': 'Marcus',
                'last_name': 'Vance',
                'email': 'marcus.vance@employeehub.com',
                'phone': '+1 (555) 678-9012',
                'gender': 'Male',
                'department_id': dept_map['FIN'].id,
                'designation': 'Senior Financial Analyst',
                'salary': 7400.00,
                'joining_date': date.today() - timedelta(days=600),
                'status': 'On Leave',
                'address': '42 Wallaby Way, Sydney, TX'
            },
            {
                'employee_id': 'EMP-1006',
                'first_name': 'Olivia',
                'last_name': 'Taylor',
                'email': 'olivia.taylor@employeehub.com',
                'phone': '+1 (555) 789-0123',
                'gender': 'Female',
                'department_id': dept_map['MKT'].id,
                'designation': 'Brand Strategy Director',
                'salary': 7900.00,
                'joining_date': date.today() - timedelta(days=120),
                'status': 'Inactive',
                'address': '100 Universal City Plaza, Universal City, CA'
            }
        ]

        for emp in sample_employees:
            employee_obj = Employee(**emp)
            db.session.add(employee_obj)

        db.session.commit()
        print(f"-> Seeded {len(sample_employees)} sample employees.")
    else:
        print("-> Existing employees found; skipping sample employee population.")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    env_name = os.environ.get('FLASK_ENV', 'development')
    app = create_app(env_name)
    with app.app_context():
        seed_all()
