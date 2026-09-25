from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g, jsonify
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    """Decorator to protect web routes that require an authenticated session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or g.user is None:
            flash('Please sign in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to restrict access to Admin-only features."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or g.user is None:
            flash('Please sign in first.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        if not g.user.is_admin:
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session and g.user:
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        identifier = request.form.get('identifier', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember'))

        user = AuthService.authenticate(identifier, password)
        if user:
            session.clear()
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session.permanent = remember

            flash(f"Welcome back, {user.full_name}! Signed in as {user.role}.", 'success')
            next_url = request.args.get('next')
            if next_url and next_url.startswith('/'):
                return redirect(next_url)
            return redirect(url_for('dashboard.index'))
        else:
            flash('Invalid username/email or password. Please try again.', 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    flash('You have been signed out successfully.', 'info')
    return redirect(url_for('auth.login'))
