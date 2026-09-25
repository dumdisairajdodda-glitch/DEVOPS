from datetime import datetime, timezone
from app import db

class Department(db.Model):
    """Department model for organizational structuring."""
    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    code = db.Column(db.String(20), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationship to employees
    employees = db.relationship('Employee', backref='department', lazy='select', cascade='all')

    @property
    def employee_count(self):
        return len(self.employees)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'code': self.code,
            'description': self.description or '',
            'employee_count': self.employee_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }

    def __repr__(self):
        return f"<Department {self.name} ({self.code})>"
