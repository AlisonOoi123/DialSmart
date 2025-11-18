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
    email = db.Column(db.String(150), nullable=False)  # Match Oracle VARCHAR2(150)

    # Message content
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)

    # Status and tracking
    is_read = db.Column(db.Integer)  # Oracle uses NUMBER instead of Boolean
    is_replied = db.Column(db.Integer)  # Oracle uses NUMBER instead of Boolean

    # Reply information - match actual Oracle table structure
    admin_notes = db.Column(db.Text)  # Oracle table has admin_notes, not admin_reply

    # Timestamps - match actual Oracle table structure
    created_at = db.Column(db.DateTime, nullable=False)
    read_at = db.Column(db.DateTime)  # Oracle table has read_at
    replied_at = db.Column(db.DateTime)

    # User ID - Oracle table has user_id, not replied_by_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    user = db.relationship('User', backref='contact_messages', lazy=True)

    def __repr__(self):
        return f'<ContactMessage {self.id} from {self.email}>'

    def mark_as_read(self):
        """Mark message as read"""
        self.is_read = 1
        self.read_at = datetime.utcnow()
        db.session.commit()

    def mark_as_replied(self, admin_user, reply_text):
        """Mark message as replied with reply details"""
        self.is_replied = 1
        self.admin_notes = reply_text
        self.user_id = admin_user.id
        self.replied_at = datetime.utcnow()
        db.session.commit()

    # Property for backward compatibility
    @property
    def admin_reply(self):
        """Backward compatibility - admin_notes is called admin_reply in code"""
        return self.admin_notes

    @admin_reply.setter
    def admin_reply(self, value):
        """Backward compatibility setter"""
        self.admin_notes = value

    @property
    def replied_by(self):
        """Backward compatibility - user is called replied_by in code"""
        return self.user

    @property
    def replied_by_id(self):
        """Backward compatibility - user_id is called replied_by_id in code"""
        return self.user_id

