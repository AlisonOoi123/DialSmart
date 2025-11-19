"""
User Model
Handles user authentication and profile management
"""
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # User categorization
    user_category = db.Column(db.String(50))  # Student, Working Professional, Senior Citizen
    age_range = db.Column(db.String(20))  # 18-25, 26-35, 36-45, 46-55, 56+

    # Account settings
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    force_password_change = db.Column(db.Boolean, default=False)  # Force password change on next login
    created_by_admin_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Track who created this admin

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)
    last_password_change = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    preferences = db.relationship('UserPreference', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    comparisons = db.relationship('Comparison', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    chat_history = db.relationship('ChatHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    audit_logs = db.relationship('AuditLog', foreign_keys='AuditLog.user_id', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    created_admins = db.relationship('User', backref=db.backref('created_by_admin', remote_side=[id]), foreign_keys=[created_by_admin_id])

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)
        self.last_password_change = datetime.utcnow()
        # Clear force password change flag after setting new password
        if self.force_password_change:
            self.force_password_change = False

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def update_last_active(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f'<User {self.email}>'


class AuditLog(db.Model):
    """Audit log for tracking admin and important user actions"""
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Who performed the action
    target_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Who was affected
    action_type = db.Column(db.String(100), nullable=False)  # e.g., 'admin_created', 'admin_deleted', 'password_changed'
    description = db.Column(db.Text)  # Detailed description
    ip_address = db.Column(db.String(50))  # IP address of the user
    user_agent = db.Column(db.String(255))  # Browser/device info
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Additional data stored as JSON (using 'chat_metadata' to avoid SQLAlchemy reserved name 'metadata')
    chat_metadata = db.Column(db.Text)  # Any additional info as JSON string

    def __repr__(self):
        return f'<AuditLog {self.action_type} by User {self.user_id}>'


class UserPreference(db.Model):
    """User preferences for personalized recommendations"""
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Budget preferences
    min_budget = db.Column(db.Integer, default=500)
    max_budget = db.Column(db.Integer, default=5000)

    # Usage priorities (JSON stored as string)
    primary_usage = db.Column(db.Text)  # Photography, Gaming, Work, Social Media, Entertainment

    # Important features (JSON stored as string)
    important_features = db.Column(db.Text)  # Battery, Camera, Performance, Storage, 5G, Design

    # Brand preferences (JSON stored as string)
    preferred_brands = db.Column(db.Text)  # List of preferred brand IDs

    # Technical preferences
    min_ram = db.Column(db.Integer, default=4)
    min_storage = db.Column(db.Integer, default=64)
    min_camera = db.Column(db.Integer, default=12)
    min_battery = db.Column(db.Integer, default=3000)
    requires_5g = db.Column(db.Boolean, default=False)

    # Screen preferences
    min_screen_size = db.Column(db.Float, default=5.5)
    max_screen_size = db.Column(db.Float, default=7.0)

    # Updated timestamp
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<UserPreference for User {self.user_id}>'
