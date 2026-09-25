from app.models.department import Department
from app.services.department_service import DepartmentService

def test_departments_list(authenticated_client):
    """Test department index page."""
    response = authenticated_client.get('/departments')
    assert response.status_code == 200
    assert b"Engineering" in response.data
    assert b"ENG" in response.data

def test_create_department(authenticated_client):
    """Test creating a new department."""
    response = authenticated_client.post('/departments/new', data={
        'name': 'Finance',
        'code': 'FIN',
        'description': 'Finance and accounting'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Finance" in response.data
    assert b"FIN" in response.data

def test_safe_delete_department_with_employees(authenticated_client, sample_employee):
    """Test safe delete prevention when employees exist in department."""
    # Department 1 (ENG) has sample_employee assigned
    response = authenticated_client.post('/departments/1/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"Cannot delete" in response.data
    assert b"assigned to it" in response.data

def test_safe_delete_empty_department(authenticated_client):
    """Test deleting a department with 0 employees is permitted."""
    # Department 2 (MKT) has 0 employees
    response = authenticated_client.post('/departments/2/delete', follow_redirects=True)
    assert response.status_code == 200
    assert b"deleted successfully" in response.data
