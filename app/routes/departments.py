from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required, admin_required
from app.services.department_service import DepartmentService

departments_bp = Blueprint('departments', __name__)

@departments_bp.route('', methods=['GET'])
@departments_bp.route('/', methods=['GET'])
@login_required
def index():
    departments = DepartmentService.get_all()
    return render_template('departments/index.html', departments=departments)

@departments_bp.route('/new', methods=['POST'])
@login_required
def create():
    name = request.form.get('name')
    code = request.form.get('code')
    description = request.form.get('description')

    try:
        dept = DepartmentService.create(name=name, code=code, description=description)
        flash(f"Department '{dept.name}' ({dept.code}) created successfully!", 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('departments.index'))

@departments_bp.route('/<int:id>/edit', methods=['POST'])
@login_required
def edit(id):
    name = request.form.get('name')
    code = request.form.get('code')
    description = request.form.get('description')

    try:
        dept = DepartmentService.update(id, name=name, code=code, description=description)
        flash(f"Department '{dept.name}' updated successfully!", 'success')
    except ValueError as e:
        flash(str(e), 'danger')

    return redirect(url_for('departments.index'))

@departments_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    success, message = DepartmentService.delete(id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('departments.index'))
