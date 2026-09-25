from flask import Flask, render_template, session, g
from flask_sqlalchemy import SQLAlchemy
from config import config_by_name

db = SQLAlchemy()

def create_app(config_name='development'):
    """Application factory for EmployeeHub."""
    app = Flask(__name__)
    
    # Load configuration
    cfg = config_by_name.get(config_name or 'development', config_by_name['default'])
    app.config.from_object(cfg)
    
    # Initialize extensions
    db.init_app(app)
    
    # Import models
    from app.models.user import User
    from app.models.department import Department
    from app.models.employee import Employee
    
    # Context processor to inject user into all templates
    @app.before_request
    def load_logged_in_user():
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = db.session.get(User, user_id)
            
    @app.context_processor
    def inject_app_globals():
        return {
            'app_name': 'EmployeeHub',
            'app_tagline': 'Smart Employee Management',
            'current_user': g.user
        }
    
    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.employees import employees_bp
    from app.routes.departments import departments_bp
    from app.routes.api import api_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(employees_bp, url_prefix='/employees')
    app.register_blueprint(departments_bp, url_prefix='/departments')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Custom Error Pages
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
        
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500
        
    return app
