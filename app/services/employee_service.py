from datetime import datetime, date
from sqlalchemy import or_, func
from app import db
from app.models.employee import Employee
from app.models.department import Department

class EmployeeService:
    """Service handling employee CRUD, search, filter and metrics."""

    @staticmethod
    def get_all(search=None, department_id=None, status=None):
        query = Employee.query.join(Department)
        
        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Employee.first_name.ilike(search_term),
                    Employee.last_name.ilike(search_term),
                    Employee.email.ilike(search_term),
                    Employee.employee_id.ilike(search_term),
                    Employee.designation.ilike(search_term),
                    Employee.phone.ilike(search_term)
                )
            )

        if department_id:
            try:
                dept_id_int = int(department_id)
                if dept_id_int > 0:
                    query = query.filter(Employee.department_id == dept_id_int)
            except (ValueError, TypeError):
                pass

        if status and status.strip():
            query = query.filter(Employee.status == status.strip())

        return query.order_by(Employee.id.desc()).all()

    @staticmethod
    def get_by_id(emp_id):
        return db.session.get(Employee, emp_id)

    @staticmethod
    def get_by_employee_id(employee_id_code):
        return Employee.query.filter_by(employee_id=employee_id_code.strip()).first()

    @staticmethod
    def create(data):
        # Validate required fields
        required = ['employee_id', 'first_name', 'last_name', 'email', 'phone', 
                    'gender', 'department_id', 'designation', 'salary', 'joining_date']
        for field in required:
            if not data.get(field):
                raise ValueError(f"Field '{field.replace('_', ' ').capitalize()}' is required.")

        emp_id_code = str(data['employee_id']).strip().upper()
        email = str(data['email']).strip().lower()

        # Check unique constraints
        if Employee.query.filter_by(employee_id=emp_id_code).first():
            raise ValueError(f"Employee ID '{emp_id_code}' is already assigned.")
        if Employee.query.filter_by(email=email).first():
            raise ValueError(f"Email '{email}' is already in use.")

        # Check department
        dept = db.session.get(Department, int(data['department_id']))
        if not dept:
            raise ValueError("Selected department does not exist.")

        # Parse joining date
        joining_date_val = data['joining_date']
        if isinstance(joining_date_val, str):
            try:
                joining_date_val = datetime.strptime(joining_date_val, '%Y-%m-%d').date()
            except ValueError:
                joining_date_val = date.today()

        # Parse salary
        try:
            salary_val = float(data['salary'])
            if salary_val < 0:
                raise ValueError("Salary cannot be negative.")
        except (ValueError, TypeError):
            raise ValueError("Salary must be a valid positive number.")

        employee = Employee(
            employee_id=emp_id_code,
            first_name=str(data['first_name']).strip(),
            last_name=str(data['last_name']).strip(),
            email=email,
            phone=str(data['phone']).strip(),
            gender=str(data['gender']).strip(),
            department_id=dept.id,
            designation=str(data['designation']).strip(),
            salary=salary_val,
            joining_date=joining_date_val,
            status=str(data.get('status', 'Active')).strip(),
            address=str(data.get('address', '')).strip()
        )
        db.session.add(employee)
        db.session.commit()
        return employee

    @staticmethod
    def update(emp_id, data):
        employee = db.session.get(Employee, emp_id)
        if not employee:
            raise ValueError("Employee not found.")

        emp_id_code = str(data.get('employee_id', employee.employee_id)).strip().upper()
        email = str(data.get('email', employee.email)).strip().lower()

        # Check unique constraint collisions
        existing_emp_id = Employee.query.filter(Employee.employee_id == emp_id_code, Employee.id != emp_id).first()
        if existing_emp_id:
            raise ValueError(f"Employee ID '{emp_id_code}' is already assigned to another employee.")

        existing_email = Employee.query.filter(Employee.email == email, Employee.id != emp_id).first()
        if existing_email:
            raise ValueError(f"Email '{email}' is already in use by another employee.")

        if 'department_id' in data:
            dept = db.session.get(Department, int(data['department_id']))
            if not dept:
                raise ValueError("Selected department does not exist.")
            employee.department_id = dept.id

        if 'joining_date' in data:
            joining_date_val = data['joining_date']
            if isinstance(joining_date_val, str):
                try:
                    employee.joining_date = datetime.strptime(joining_date_val, '%Y-%m-%d').date()
                except ValueError:
                    pass
            elif isinstance(joining_date_val, date):
                employee.joining_date = joining_date_val

        if 'salary' in data:
            try:
                salary_val = float(data['salary'])
                if salary_val < 0:
                    raise ValueError("Salary cannot be negative.")
                employee.salary = salary_val
            except (ValueError, TypeError):
                raise ValueError("Salary must be a valid number.")

        if 'first_name' in data:
            employee.first_name = str(data['first_name']).strip()
        if 'last_name' in data:
            employee.last_name = str(data['last_name']).strip()
        if 'phone' in data:
            employee.phone = str(data['phone']).strip()
        if 'gender' in data:
            employee.gender = str(data['gender']).strip()
        if 'designation' in data:
            employee.designation = str(data['designation']).strip()
        if 'status' in data:
            employee.status = str(data['status']).strip()
        if 'address' in data:
            employee.address = str(data['address']).strip()

        employee.employee_id = emp_id_code
        employee.email = email
        db.session.commit()
        return employee

    @staticmethod
    def delete(emp_id):
        employee = db.session.get(Employee, emp_id)
        if not employee:
            return False, "Employee not found."
        name = employee.full_name
        db.session.delete(employee)
        db.session.commit()
        return True, f"Employee '{name}' deleted successfully."

    @staticmethod
    def get_dashboard_stats():
        """Retrieve real database metrics for the analytics dashboard."""
        total_employees = Employee.query.count()
        active_employees = Employee.query.filter_by(status='Active').count()
        inactive_employees = Employee.query.filter_by(status='Inactive').count()
        on_leave_employees = Employee.query.filter_by(status='On Leave').count()
        total_departments = Department.query.count()

        # Monthly payroll calculation
        payroll_result = db.session.query(func.sum(Employee.salary)).filter(Employee.status == 'Active').scalar()
        total_payroll = float(payroll_result) if payroll_result else 0.0

        # Employees count per department
        departments = Department.query.all()
        department_distribution = []
        for d in departments:
            count = Employee.query.filter_by(department_id=d.id).count()
            department_distribution.append({
                'id': d.id,
                'name': d.name,
                'code': d.code,
                'count': count
            })

        # Recent 5 employees
        recent_employees = Employee.query.order_by(Employee.id.desc()).limit(5).all()

        return {
            'total_employees': total_employees,
            'active_employees': active_employees,
            'inactive_employees': inactive_employees,
            'on_leave_employees': on_leave_employees,
            'total_departments': total_departments,
            'total_monthly_payroll': total_payroll,
            'department_distribution': department_distribution,
            'status_distribution': {
                'Active': active_employees,
                'Inactive': inactive_employees,
                'On Leave': on_leave_employees
            },
            'recent_employees': [emp.to_dict() for emp in recent_employees]
        }
