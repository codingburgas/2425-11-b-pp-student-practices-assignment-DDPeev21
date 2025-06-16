# SQLAlchemy models will go here 
from app import db
from flask_login import UserMixin

class Role(db.Model):
    """Role model: represents a user role (e.g., admin, user)."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)  # One-to-many relationship

class User(UserMixin, db.Model):
    """User model: stores user credentials and profile info."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  # Foreign key to Role
    # Add more fields as needed (profile, etc.) 

    def is_admin(self):
        """Check if the user has admin role."""
        return self.role and self.role.name == 'admin'

class ClassifiedPoint(db.Model):
    """ClassifiedPoint model: stores classified 2D points for each user."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Foreign key to User
    x = db.Column(db.Float, nullable=False)
    y = db.Column(db.Float, nullable=False)
    label = db.Column(db.Integer, nullable=False)
    result = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, server_default=db.func.now())  # Creation time 