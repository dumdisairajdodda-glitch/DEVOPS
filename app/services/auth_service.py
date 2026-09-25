from app import db
from app.models.user import User

class AuthService:
    """Service handling user authentication and registration."""

    @staticmethod
    def authenticate(identifier, password):
        """Authenticate user by username or email and password."""
        if not identifier or not password:
            return None
        user = User.query.filter(
            (User.username == identifier.strip()) | (User.email == identifier.strip().lower())
        ).first()
        if user and user.check_password(password):
            return user
        return None

    @staticmethod
    def get_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def create_user(username, email, password, full_name, role='HR'):
        """Create a new user with hashed password."""
        username = username.strip()
        email = email.strip().lower()
        if User.query.filter_by(username=username).first():
            raise ValueError(f"Username '{username}' is already taken.")
        if User.query.filter_by(email=email).first():
            raise ValueError(f"Email '{email}' is already registered.")

        user = User(
            username=username,
            email=email,
            full_name=full_name.strip(),
            role=role if role in ('Admin', 'HR') else 'HR'
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
