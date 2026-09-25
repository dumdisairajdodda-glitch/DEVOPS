from flask import Blueprint, render_template, redirect, url_for, session, g
from app.routes.auth import login_required
from app.services.employee_service import EmployeeService

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    if 'user_id' not in session or g.user is None:
        return redirect(url_for('auth.login'))
    return redirect(url_for('dashboard.index'))

@dashboard_bp.route('/dashboard')
@login_required
def index():
    stats = EmployeeService.get_dashboard_stats()
    return render_template('dashboard/index.html', stats=stats)
