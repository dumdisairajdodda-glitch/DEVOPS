from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.employees import employees_bp
from app.routes.departments import departments_bp
from app.routes.api import api_bp

__all__ = ['auth_bp', 'dashboard_bp', 'employees_bp', 'departments_bp', 'api_bp']
