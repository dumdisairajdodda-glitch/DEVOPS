import pytest
from datetime import date
from app import create_app, db
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee

@pytest.fixture(scope='function')
def app():
    """Create and configure a new app instance for each test with isolated in-memory DB."""
    app = create_app('testing')

    with app.app_context():
        db.create_all()

        # Seed standard Admin and HR users
        admin = User(username='admin', email='admin@test.com', full_name='Admin User', role='Admin')
        admin.set_password('adminpass')
        db.session.add(admin)

        hr = User(username='hr_user', email='hr@test.com', full_name='HR User', role='HR')
        hr.set_password('hrpass')
        db.session.add(hr)

        # Seed standard Department
        dept = Department(name='Engineering', code='ENG', description='Software and infrastructure')
        db.session.add(dept)

        dept_mkt = Department(name='Marketing', code='MKT', description='Brand and growth')
        db.session.add(dept_mkt)

        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture(scope='function')
def authenticated_client(client):
    """Client with an active Admin login session."""
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['username'] = 'admin'
        sess['role'] = 'Admin'
    return client

@pytest.fixture(scope='function')
def sample_employee(app):
    """Fixture providing a seeded employee."""
    with app.app_context():
        emp = Employee(
            employee_id='EMP-TEST-01',
            first_name='John',
            last_name='Doe',
            email='john.doe@test.com',
            phone='1234567890',
            gender='Male',
            department_id=1,
            designation='DevOps Engineer',
            salary=7500.0,
            joining_date=date(2024, 1, 15),
            status='Active',
            address='123 Test Street'
        )
        db.session.add(emp)
        db.session.commit()
        return emp.id
