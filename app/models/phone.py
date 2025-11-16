"""
Phone Model
Handles smartphone data and specifications
"""
from app import db
from datetime import datetime

class Phone(db.Model):
    """Main phone model"""
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id', ondelete='CASCADE'), nullable=False)

    # Basic information
    model_name = db.Column(db.String(150), nullable=False, index=True)
    model_number = db.Column(db.String(100))
    price = db.Column(db.Float, nullable=False, index=True)  # Price in MYR

    # Media
    main_image = db.Column(db.String(255))
    gallery_images = db.Column(db.Text)  # JSON string of image URLs

    # Status and availability
    is_active = db.Column(db.Boolean, default=True, index=True)
    availability_status = db.Column(db.String(50), default='Available')  # Available, Out of Stock, Pre-order
    release_date = db.Column(db.Date)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    specifications = db.relationship('PhoneSpecification', backref='phone', uselist=False, cascade='all, delete-orphan')

    def get_price_category(self):
        """Categorize phone by price"""
        if self.price < 1000:
            return 'budget'
        elif self.price < 2000:
            return 'mid_range'
        elif self.price < 3000:
            return 'upper_mid'
        else:
            return 'premium'

    def __repr__(self):
        return f'<Phone {self.model_name}>'


class PhoneSpecification(db.Model):
    """Detailed phone specifications"""
    __tablename__ = 'phone_specifications'

    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False, unique=True)

    # Display specifications
    screen_size = db.Column(db.Float)  # in inches
    screen_resolution = db.Column(db.String(50))  # e.g., "1080x2400"
    screen_type = db.Column(db.String(50))  # AMOLED, IPS LCD, etc.
    refresh_rate = db.Column(db.Integer, default=60)  # Hz

    # Performance specifications
    processor = db.Column(db.String(100))
    processor_brand = db.Column(db.String(50))  # Qualcomm, MediaTek, Apple, etc.
    ram_options = db.Column(db.String(50))  # "4GB, 6GB, 8GB"
    storage_options = db.Column(db.String(50))  # "64GB, 128GB, 256GB"
    expandable_storage = db.Column(db.Boolean, default=False)

    # Camera specifications
    rear_camera = db.Column(db.String(100))  # "48MP + 8MP + 2MP"
    rear_camera_main = db.Column(db.Integer)  # Main camera MP
    front_camera = db.Column(db.String(50))  # "16MP"
    front_camera_mp = db.Column(db.Integer)  # Front camera MP
    camera_features = db.Column(db.Text)  # JSON string of features

    # Battery specifications
    battery_capacity = db.Column(db.Integer)  # in mAh
    charging_speed = db.Column(db.String(50))  # "33W Fast Charging"
    wireless_charging = db.Column(db.Boolean, default=False)

    # Connectivity
    has_5g = db.Column(db.Boolean, default=False, index=True)
    wifi_standard = db.Column(db.String(50))  # "WiFi 6", "WiFi 5"
    bluetooth_version = db.Column(db.String(20))  # "5.2"
    nfc = db.Column(db.Boolean, default=False)

    # Additional features
    operating_system = db.Column(db.String(50))  # "Android 13", "iOS 16"
    fingerprint_sensor = db.Column(db.Boolean, default=True)
    face_unlock = db.Column(db.Boolean, default=False)
    water_resistance = db.Column(db.String(20))  # "IP68"
    dual_sim = db.Column(db.Boolean, default=True)

    # Physical characteristics
    weight = db.Column(db.Integer)  # in grams
    dimensions = db.Column(db.String(50))  # "160.5 x 74.8 x 8.4 mm"
    colors_available = db.Column(db.String(200))  # "Black, White, Blue"

    def __repr__(self):
        return f'<PhoneSpecification for Phone {self.phone_id}>'
