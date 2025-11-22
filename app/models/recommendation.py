"""
Recommendation Models
Handles AI recommendations, comparisons, and chat history
"""
from app import db
from datetime import datetime

class Recommendation(db.Model):
    """User recommendation history"""
    __tablename__ = 'recommendations'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    phone_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False)

    # Recommendation details
    match_percentage = db.Column(db.Float)  # 0-100
    reasoning = db.Column(db.Text)  # Why this phone was recommended

    # User input parameters (JSON stored as string)
    user_criteria = db.Column(db.Text)  # The criteria used for this recommendation

    # User feedback
    is_viewed = db.Column(db.Boolean, default=False)
    is_saved = db.Column(db.Boolean, default=False)
    user_rating = db.Column(db.Integer)  # 1-5 stars

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    phone = db.relationship('Phone', backref='recommendations')

    def __repr__(self):
        return f'<Recommendation {self.id} for User {self.user_id}>'


class Comparison(db.Model):
    """Phone comparison history"""
    __tablename__ = 'comparisons'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Phones being compared
    phone1_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False)
    phone2_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False)

    # Comparison metadata
    is_saved = db.Column(db.Boolean, default=False)
    comparison_notes = db.Column(db.Text)

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # Relationships
    phone1 = db.relationship('Phone', foreign_keys=[phone1_id], backref='comparisons_as_phone1')
    phone2 = db.relationship('Phone', foreign_keys=[phone2_id], backref='comparisons_as_phone2')

    def __repr__(self):
        return f'<Comparison {self.id}: Phone {self.phone1_id} vs Phone {self.phone2_id}>'


class ChatHistory(db.Model):
    """Chatbot conversation history"""
    __tablename__ = 'chat_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Message details
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, recommendation, comparison

    # Context
    session_id = db.Column(db.String(100))  # To group conversations
    intent = db.Column(db.String(100))  # Detected user intent

    # Response metadata (JSON stored as string)
    response_metadata = db.Column(db.Text)  # Additional context like recommended phone IDs

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<ChatHistory {self.id} for User {self.user_id}>'
