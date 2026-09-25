from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from app.routes.auth import login_required, admin_required
from app.services.employee_service import EmployeeService
from app.services.department_service import DepartmentService

employees_bp = Blueprint('employees', __name__)

@employees_bp.route('', methods=['GET'])
@employees_bp.route('/', methods=['GET'])
@login_required
def index():
    search = request.args.get('search', '').strip()
    department_id = request.args.get('department_id', '')
    status = request.args.get('status', '').strip()

    employees = EmployeeService.get_all(search=search, department_id=department_id, status=status)
    departments = DepartmentService.get_all()

    return render_template(
        'employees/index.html',
        employees=employees,
        departments=departments,
        current_search=search,
        current_dept=department_id,
        current_status=status
    )

@employees_bp.route('/new', methods=['GET', 'POST'])
@login_required
def create():
    departments = DepartmentService.get_all()
    if not departments:
        flash('Please create at least one department before adding employees.', 'warning')
        return redirect(url_for('departments.index'))

    if request.method == 'POST':
        data = {
            'employee_id': request.form.get('employee_id'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'gender': request.form.get('gender'),
            'department_id': request.form.get('department_id'),
            'designation': request.form.get('designation'),
            'salary': request.form.get('salary'),
            'joining_date': request.form.get('joining_date'),
            'status': request.form.get('status', 'Active'),
            'address': request.form.get('address')
        }
        try:
            employee = EmployeeService.create(data)
            flash(f"Employee {employee.full_name} ({employee.employee_id}) created successfully!", 'success')
            return redirect(url_for('employees.detail', id=employee.id))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('employees/form.html', departments=departments, form_data=data, is_edit=False)

    return render_template('employees/form.html', departments=departments, form_data={}, is_edit=False)

@employees_bp.route('/<int:id>', methods=['GET'])
@login_required
def detail(id):
    employee = EmployeeService.get_by_id(id)
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employees.index'))
    return render_template('employees/detail.html', employee=employee)

@employees_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    employee = EmployeeService.get_by_id(id)
    if not employee:
        flash('Employee not found.', 'danger')
        return redirect(url_for('employees.index'))

    departments = DepartmentService.get_all()

    if request.method == 'POST':
        data = {
            'employee_id': request.form.get('employee_id'),
            'first_name': request.form.get('first_name'),
            'last_name': request.form.get('last_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'gender': request.form.get('gender'),
            'department_id': request.form.get('department_id'),
            'designation': request.form.get('designation'),
            'salary': request.form.get('salary'),
            'joining_date': request.form.get('joining_date'),
            'status': request.form.get('status'),
            'address': request.form.get('address')
        }
        try:
            EmployeeService.update(id, data)
            flash(f"Employee {employee.full_name} updated successfully!", 'success')
            return redirect(url_for('employees.detail', id=employee.id))
        except ValueError as e:
            flash(str(e), 'danger')
            return render_template('employees/form.html', departments=departments, form_data=data, employee=employee, is_edit=True)

    form_data = {
        'employee_id': employee.employee_id,
        'first_name': employee.first_name,
        'last_name': employee.last_name,
        'email': employee.email,
        'phone': employee.phone,
        'gender': employee.gender,
        'department_id': employee.department_id,
        'designation': employee.designation,
        'salary': employee.salary,
        'joining_date': employee.joining_date.strftime('%Y-%m-%d') if employee.joining_date else '',
        'status': employee.status,
        'address': employee.address
    }
    return render_template('employees/form.html', departments=departments, form_data=form_data, employee=employee, is_edit=True)

@employees_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    success, message = EmployeeService.delete(id)
    if success:
        flash(message, 'success')
    else:
        flash(message, 'danger')
    return redirect(url_for('employees.index'))
