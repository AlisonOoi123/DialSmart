"""
Contact Message Model
Handles contact form submissions from users
"""
from app import db
from datetime import datetime

class ContactMessage(db.Model):
    """Contact form messages"""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)

    # Sender information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    # Message content
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

    # Status tracking
    is_read = db.Column(db.Boolean, default=False, index=True)
    is_replied = db.Column(db.Boolean, default=False)
    admin_notes = db.Column(db.Text)  # Notes from admin

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    read_at = db.Column(db.DateTime)
    replied_at = db.Column(db.DateTime)

    # User reference (if logged in)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()

    def mark_as_replied(self):
        """Mark message as replied"""
        if not self.is_replied:
            self.is_replied = True
            self.replied_at = datetime.utcnow()

    def __repr__(self):
        return f'<ContactMessage from {self.name} ({self.email})>'
