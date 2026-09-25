def test_api_login(client):
    """Test REST API login endpoint."""
    response = client.post('/api/login', json={
        'identifier': 'admin',
        'password': 'adminpass'
    })
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['user']['username'] == 'admin'

def test_api_dashboard_stats(client, sample_employee):
    """Test REST API dashboard stats endpoint."""
    response = client.get('/api/dashboard/stats')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['success'] is True
    assert json_data['data']['total_employees'] >= 1
    assert json_data['data']['active_employees'] >= 1
    assert json_data['data']['total_departments'] >= 2

def test_api_employees_crud(client):
    """Test full Employee CRUD through JSON REST API."""
    # 1. Create
    create_res = client.post('/api/employees', json={
        'employee_id': 'EMP-API-01',
        'first_name': 'Rachel',
        'last_name': 'Green',
        'email': 'rachel.green@test.com',
        'phone': '1112223333',
        'gender': 'Female',
        'department_id': 1,
        'designation': 'Product Strategist',
        'salary': 7200.0,
        'joining_date': '2024-03-01',
        'status': 'Active',
        'address': 'Manhattan, NY'
    })
    assert create_res.status_code == 201
    emp_id = create_res.get_json()['data']['id']

    # 2. Retrieve List
    list_res = client.get('/api/employees')
    assert list_res.status_code == 200
    assert list_res.get_json()['count'] >= 1

    # 3. Retrieve Single
    get_res = client.get(f'/api/employees/{emp_id}')
    assert get_res.status_code == 200
    assert get_res.get_json()['data']['first_name'] == 'Rachel'

    # 4. Update
    update_res = client.put(f'/api/employees/{emp_id}', json={
        'designation': 'Senior Product Strategist',
        'salary': 7800.0
    })
    assert update_res.status_code == 200
    assert update_res.get_json()['data']['designation'] == 'Senior Product Strategist'

    # 5. Delete
    delete_res = client.delete(f'/api/employees/{emp_id}')
    assert delete_res.status_code == 200
    assert delete_res.get_json()['success'] is True
