from app import db
from app.models.department import Department
from app.models.employee import Employee

class DepartmentService:
    """Service handling department CRUD and safety constraints."""

    @staticmethod
    def get_all():
        return Department.query.order_by(Department.name.asc()).all()

    @staticmethod
    def get_by_id(dept_id):
        return db.session.get(Department, dept_id)

    @staticmethod
    def create(name, code, description=None):
        name = name.strip()
        code = code.strip().upper()
        if Department.query.filter_by(name=name).first():
            raise ValueError(f"Department with name '{name}' already exists.")
        if Department.query.filter_by(code=code).first():
            raise ValueError(f"Department with code '{code}' already exists.")

        dept = Department(
            name=name,
            code=code,
            description=description.strip() if description else None
        )
        db.session.add(dept)
        db.session.commit()
        return dept

    @staticmethod
    def update(dept_id, name, code, description=None):
        dept = db.session.get(Department, dept_id)
        if not dept:
            raise ValueError("Department not found.")

        name = name.strip()
        code = code.strip().upper()

        # Check for unique conflicts
        existing_name = Department.query.filter(Department.name == name, Department.id != dept_id).first()
        if existing_name:
            raise ValueError(f"Department with name '{name}' already exists.")

        existing_code = Department.query.filter(Department.code == code, Department.id != dept_id).first()
        if existing_code:
            raise ValueError(f"Department with code '{code}' already exists.")

        dept.name = name
        dept.code = code
        dept.description = description.strip() if description else None
        db.session.commit()
        return dept

    @staticmethod
    def delete(dept_id):
        """Safe deletion check: prevent deleting if employees exist."""
        dept = db.session.get(Department, dept_id)
        if not dept:
            return False, "Department not found."

        assigned_count = Employee.query.filter_by(department_id=dept.id).count()
        if assigned_count > 0:
            return False, f"Cannot delete '{dept.name}' because {assigned_count} employee(s) are assigned to it. Please reassign them first."

        db.session.delete(dept)
        db.session.commit()
        return True, f"Department '{dept.name}' deleted successfully."
