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
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)

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
    """Detailed phone specifications - Enhanced for comprehensive CSV dataset"""
    __tablename__ = 'phone_specifications'

    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False, unique=True)

    # Display specifications
    screen_size = db.Column(db.Float)  # in inches
    screen_resolution = db.Column(db.String(150))  # e.g., "1080x2400" (increased for detailed resolutions)
    screen_type = db.Column(db.String(200))  # AMOLED, IPS LCD, etc. (increased for detailed descriptions)
    display_type = db.Column(db.String(200))  # Full display description
    refresh_rate = db.Column(db.Integer, default=60)  # Hz
    ppi = db.Column(db.Integer)  # Pixels per inch
    multitouch = db.Column(db.String(50))  # Yes/No or specific info
    protection = db.Column(db.String(200))  # Corning Gorilla Glass, etc. (increased for detailed protection specs)

    # Performance specifications
    processor = db.Column(db.String(100))  # Chipset name
    chipset = db.Column(db.String(150))  # Full chipset details
    cpu = db.Column(db.String(200))  # CPU architecture and cores
    gpu = db.Column(db.String(100))  # GPU model
    processor_brand = db.Column(db.String(50))  # Qualcomm, MediaTek, Apple, etc.
    ram_options = db.Column(db.String(50))  # "4GB, 6GB, 8GB"
    storage_options = db.Column(db.String(50))  # "64GB, 128GB, 256GB"
    expandable_storage = db.Column(db.Boolean, default=False)
    card_slot = db.Column(db.String(100))  # microSD details

    # Camera specifications
    rear_camera = db.Column(db.String(500))  # Full rear camera specs (increased for multi-camera setups)
    rear_camera_main = db.Column(db.Integer)  # Main camera MP
    front_camera = db.Column(db.String(200))  # Front camera specs
    front_camera_mp = db.Column(db.Integer)  # Front camera MP
    camera_features = db.Column(db.Text)  # Camera features
    flash = db.Column(db.String(100))  # Flash type
    video_recording = db.Column(db.String(200))  # Video capabilities

    # Battery specifications
    battery_capacity = db.Column(db.Integer)  # in mAh
    battery = db.Column(db.String(100))  # Full battery description
    charging_speed = db.Column(db.String(100))  # "33W Fast Charging"
    fast_charging = db.Column(db.String(200))  # Detailed fast charging info
    wireless_charging = db.Column(db.String(100))  # Wireless charging details
    removable_battery = db.Column(db.String(50))  # Removable/Non-Removable

    # Network and Connectivity
    sim = db.Column(db.String(150))  # SIM type details (increased for dual/eSIM descriptions)
    technology = db.Column(db.String(100))  # GSM / HSPA / LTE / 5G
    network_5g = db.Column(db.String(200))  # 5G bands
    network_4g = db.Column(db.String(250))  # 4G bands (increased for multiple band listings)
    network_3g = db.Column(db.String(200))  # 3G bands
    network_2g = db.Column(db.String(200))  # 2G bands
    network_speed = db.Column(db.String(100))  # Network speed capabilities
    has_5g = db.Column(db.Boolean, default=False, index=True)
    wifi_standard = db.Column(db.String(100))  # "WiFi 6", "WiFi 5"
    bluetooth_version = db.Column(db.String(100))  # Bluetooth version (increased for CSV data alignment issues)
    gps = db.Column(db.String(100))  # GPS capabilities
    nfc = db.Column(db.String(100))  # NFC support (increased for CSV data alignment issues)
    usb = db.Column(db.String(100))  # USB type and version
    audio_jack = db.Column(db.String(100))  # 3.5mm jack presence (increased for CSV data alignment issues)
    radio = db.Column(db.String(100))  # FM radio support (increased for CSV data alignment issues)

    # Operating System
    operating_system = db.Column(db.String(200))  # "Android 13", "iOS 16", full OS details

    # Physical characteristics
    weight = db.Column(db.String(50))  # Weight with unit
    dimensions = db.Column(db.String(100))  # "160.5 x 74.8 x 8.4 mm"
    colors_available = db.Column(db.String(200))  # "Black, White, Blue"
    body_material = db.Column(db.String(300))  # Body material description (increased for detailed material specs)

    # Additional features
    fingerprint_sensor = db.Column(db.Boolean, default=True)
    face_unlock = db.Column(db.Boolean, default=False)
    water_resistance = db.Column(db.String(20))  # "IP68"
    dual_sim = db.Column(db.Boolean, default=True)
    sensors = db.Column(db.Text)  # All sensors

    # Reference
    product_url = db.Column(db.String(500))  # Original product page URL

    def __repr__(self):
        return f'<PhoneSpecification for Phone {self.phone_id}>'
