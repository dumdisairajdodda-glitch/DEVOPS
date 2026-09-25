from app.models.employee import Employee
from app.services.employee_service import EmployeeService

def test_get_employees_list(authenticated_client, sample_employee):
    """Test fetching employees index page."""
    response = authenticated_client.get('/employees')
    assert response.status_code == 200
    assert b"EMP-TEST-01" in response.data
    assert b"John Doe" in response.data

def test_create_employee(authenticated_client):
    """Test employee creation via form submission."""
    response = authenticated_client.post('/employees/new', data={
        'employee_id': 'EMP-TEST-02',
        'first_name': 'Jane',
        'last_name': 'Smith',
        'email': 'jane.smith@test.com',
        'phone': '9876543210',
        'gender': 'Female',
        'department_id': '1',
        'designation': 'QA Engineer',
        'salary': '6000.00',
        'joining_date': '2024-02-01',
        'status': 'Active',
        'address': '456 Test Ave'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Jane Smith" in response.data

def test_get_employee_detail(authenticated_client, sample_employee):
    """Test viewing an individual employee profile."""
    response = authenticated_client.get(f'/employees/{sample_employee}')
    assert response.status_code == 200
    assert b"John Doe" in response.data
    assert b"EMP-TEST-01" in response.data

def test_update_employee(authenticated_client, sample_employee):
    """Test updating existing employee data."""
    response = authenticated_client.post(f'/employees/{sample_employee}/edit', data={
        'employee_id': 'EMP-TEST-01',
        'first_name': 'Johnny',
        'last_name': 'Doe',
        'email': 'johnny.doe@test.com',
        'phone': '1234567890',
        'gender': 'Male',
        'department_id': '1',
        'designation': 'Staff DevOps Engineer',
        'salary': '8500.00',
        'joining_date': '2024-01-15',
        'status': 'Active',
        'address': '123 Test Street Updated'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Johnny Doe" in response.data
    assert b"Staff DevOps Engineer" in response.data

def test_delete_employee(authenticated_client, sample_employee):
    """Test deleting an employee."""
    response = authenticated_client.post(f'/employees/{sample_employee}/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"deleted successfully" in response.data
