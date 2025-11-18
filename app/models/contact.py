"""
Contact Message Model
Stores user contact form submissions and admin replies
"""
from datetime import datetime
from app import db


class ContactMessage(db.Model):
    """Model for storing contact form messages"""
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)

    # Sender information
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)

    # Message content
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

    # Status and tracking
    is_read = db.Column(db.Boolean, default=False)
    is_replied = db.Column(db.Boolean, default=False)

    # Reply information
    admin_reply = db.Column(db.Text)
    replied_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    replied_at = db.Column(db.DateTime)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    replied_by = db.relationship('User', backref='message_replies', lazy=True)

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.email}>'

    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = True
        db.session.commit()

    def mark_as_replied(self, admin_user, reply_text):
        """Mark message as replied with reply details"""
        self.is_replied = True
        self.admin_reply = reply_text
        self.replied_by_id = admin_user.id
        self.replied_at = datetime.utcnow()
        db.session.commit()
