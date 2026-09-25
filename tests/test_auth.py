def test_login_page_renders(client):
    """Test that login page loads successfully."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Sign In to Dashboard" in response.data

def test_login_success(client):
    """Test login with valid credentials sets session and redirects."""
    response = client.post('/login', data={
        'identifier': 'admin',
        'password': 'adminpass'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Analytics &amp; Overview" in response.data or b"Analytics & Overview" in response.data
    assert b"Welcome back, Admin User!" in response.data

def test_login_invalid_password(client):
    """Test login failure with bad password."""
    response = client.post('/login', data={
        'identifier': 'admin',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username/email or password" in response.data

def test_logout(authenticated_client):
    """Test that logout clears session and redirects to login."""
    response = authenticated_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b"You have been signed out successfully" in response.data

def test_protected_route_requires_login(client):
    """Test that protected pages redirect unauthenticated users to login."""
    response = client.get('/dashboard')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
