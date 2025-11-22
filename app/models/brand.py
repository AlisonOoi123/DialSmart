"""
Brand Model
Handles smartphone brand information
"""
from app import db
from datetime import datetime

class Brand(db.Model):
    """Brand model for phone manufacturers"""
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    tagline = db.Column(db.String(200))

    # Media
    logo_url = db.Column(db.String(255))
    website_url = db.Column(db.String(500))

    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    phones = db.relationship('Phone', backref='brand', lazy='dynamic')

    def get_phone_count(self):
        """Get number of active phones for this brand"""
        return self.phones.filter_by(is_active=True).count()

    def get_price_range(self):
        """Get min and max price for brand's phones"""
        active_phones = self.phones.filter_by(is_active=True).all()
        if not active_phones:
            return (0, 0)

        prices = [phone.price for phone in active_phones]
        return (min(prices), max(prices))

    def __repr__(self):
        return f'<Brand {self.name}>'
