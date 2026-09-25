from flask import Blueprint, request, jsonify, session, g
from app.services.auth_service import AuthService
from app.services.employee_service import EmployeeService
from app.services.department_service import DepartmentService

api_bp = Blueprint('api', __name__)

def api_login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session or g.user is None:
            return jsonify({'success': False, 'error': 'Unauthorized. Please sign in.'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# Auth Endpoints
@api_bp.route('/login', methods=['POST'])
def api_login():
    data = request.get_json() or {}
    identifier = data.get('username') or data.get('email') or data.get('identifier')
    password = data.get('password')

    user = AuthService.authenticate(identifier, password)
    if not user:
        return jsonify({'success': False, 'error': 'Invalid credentials.'}), 401

    session['user_id'] = user.id
    session['username'] = user.username
    session['role'] = user.role
    return jsonify({
        'success': True,
        'message': f"Logged in as {user.username}",
        'user': user.to_dict()
    }), 200

@api_bp.route('/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully.'}), 200

# Dashboard Endpoints
@api_bp.route('/dashboard/stats', methods=['GET'])
def api_dashboard_stats():
    stats = EmployeeService.get_dashboard_stats()
    return jsonify({'success': True, 'data': stats}), 200

# Employees Endpoints
@api_bp.route('/employees', methods=['GET'])
def api_get_employees():
    search = request.args.get('search')
    department_id = request.args.get('department_id')
    status = request.args.get('status')
    employees = EmployeeService.get_all(search=search, department_id=department_id, status=status)
    return jsonify({
        'success': True,
        'count': len(employees),
        'data': [emp.to_dict() for emp in employees]
    }), 200

@api_bp.route('/employees/<int:id>', methods=['GET'])
def api_get_employee(id):
    employee = EmployeeService.get_by_id(id)
    if not employee:
        return jsonify({'success': False, 'error': 'Employee not found.'}), 404
    return jsonify({'success': True, 'data': employee.to_dict()}), 200

@api_bp.route('/employees', methods=['POST'])
def api_create_employee():
    data = request.get_json() or {}
    try:
        employee = EmployeeService.create(data)
        return jsonify({
            'success': True,
            'message': 'Employee created successfully.',
            'data': employee.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api_bp.route('/employees/<int:id>', methods=['PUT'])
def api_update_employee(id):
    data = request.get_json() or {}
    try:
        employee = EmployeeService.update(id, data)
        return jsonify({
            'success': True,
            'message': 'Employee updated successfully.',
            'data': employee.to_dict()
        }), 200
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        return jsonify({'success': False, 'error': str(e)}), status_code

@api_bp.route('/employees/<int:id>', methods=['DELETE'])
def api_delete_employee(id):
    success, message = EmployeeService.delete(id)
    if not success:
        return jsonify({'success': False, 'error': message}), 404
    return jsonify({'success': True, 'message': message}), 200

# Departments Endpoints
@api_bp.route('/departments', methods=['GET'])
def api_get_departments():
    departments = DepartmentService.get_all()
    return jsonify({
        'success': True,
        'count': len(departments),
        'data': [dept.to_dict() for dept in departments]
    }), 200

@api_bp.route('/departments', methods=['POST'])
def api_create_department():
    data = request.get_json() or {}
    name = data.get('name')
    code = data.get('code')
    description = data.get('description')
    if not name or not code:
        return jsonify({'success': False, 'error': 'Name and Code are required fields.'}), 400
    try:
        dept = DepartmentService.create(name=name, code=code, description=description)
        return jsonify({
            'success': True,
            'message': 'Department created successfully.',
            'data': dept.to_dict()
        }), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@api_bp.route('/departments/<int:id>', methods=['PUT'])
def api_update_department(id):
    data = request.get_json() or {}
    try:
        dept = DepartmentService.update(
            id,
            name=data.get('name'),
            code=data.get('code'),
            description=data.get('description')
        )
        return jsonify({
            'success': True,
            'message': 'Department updated successfully.',
            'data': dept.to_dict()
        }), 200
    except ValueError as e:
        status_code = 404 if "not found" in str(e).lower() else 400
        return jsonify({'success': False, 'error': str(e)}), status_code

@api_bp.route('/departments/<int:id>', methods=['DELETE'])
def api_delete_department(id):
    success, message = DepartmentService.delete(id)
    if not success:
        return jsonify({'success': False, 'error': message}), 400
    return jsonify({'success': True, 'message': message}), 200
