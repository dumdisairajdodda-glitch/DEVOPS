import os
from app import create_app, db
from app.models.user import User
from app.models.department import Department
from app.models.employee import Employee

env_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(env_name)

# Ensure database tables and initial seed data exist upon startup (crucial for Render / Gunicorn)
with app.app_context():
    try:
        db.create_all()
        if User.query.first() is None:
            from seed import seed_all
            seed_all()
    except Exception as e:
        print(f"Startup database check: {e}")

@app.cli.command("init-db")
def init_db_command():
    """Clear existing data and create new database tables."""
    with app.app_context():
        db.create_all()
        print("Initialized database tables successfully!")

@app.cli.command("seed-db")
def seed_db_command():
    """Populate database with default Admin, HR and sample data."""
    from seed import seed_all
    with app.app_context():
        seed_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(env_name == 'development'))
