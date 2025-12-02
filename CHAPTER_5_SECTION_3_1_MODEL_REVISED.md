### 5.3.1 Model - Module-Based Organization

The Model in MVC architecture acts as the backbone of the DialSmart application, encapsulating the application's data and business logic across multiple functional modules. It serves as the foundational component responsible for interfacing with the database, managing vital information through well-defined entities and relationships. The Model manages the storage, processing, and integrity of data, defining the rules that govern the application. Acting as the authoritative source of information, the Model communicates with both the View and Controller, ensuring data consistency and facilitating seamless updates in response to changes in the underlying data.

The DialSmart system implements database models using SQLAlchemy ORM (Object-Relational Mapping), which provides an abstraction layer between Python objects and database tables. The models are organized based on functional modules, each addressing specific business requirements:

```python
"""
Database Models Package
Contains all database models for DialSmart
"""
from app.models.user import User, UserPreference
from app.models.phone import Phone, PhoneSpecification
from app.models.brand import Brand
from app.models.recommendation import Recommendation, Comparison, ChatHistory

__all__ = [
    'User',
    'UserPreference',
    'Phone',
    'PhoneSpecification',
    'Brand',
    'Recommendation',
    'Comparison',
    'ChatHistory'
]
```

---

#### 5.3.1.1 Admin Management Module Models

The Admin Management Module encompasses models and functionality for system administration, including admin authentication, dashboard statistics, CRUD operations for phone brands and models, user category management, and system logging. The primary model supporting this module is the User model with administrative privileges.

**Admin User Model**

The User model includes administrative capabilities through the `is_admin` flag, enabling administrative access control throughout the system:

```python
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

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    preferences = db.relationship('UserPreference', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    comparisons = db.relationship('Comparison', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    chat_history = db.relationship('ChatHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')
```

The `is_admin` boolean field distinguishes administrative users from regular users, enabling role-based access control. Administrative users can access specialized routes protected by the `admin_required` decorator. The `user_category` field supports the categorization of users into different demographic groups (Student, Working Professional, Senior Citizen), which is crucial for generating targeted recommendations and system analytics.

**Admin Controller Implementation**

The admin module implements comprehensive CRUD operations through controller methods:

```python
@bp.route('/phones/add', methods=['GET', 'POST'])
@login_required
@admin_required
def add_phone():
    """Add new phone"""
    if request.method == 'POST':
        # Basic information
        model_name = request.form.get('model_name')
        brand_id = request.form.get('brand_id', type=int)
        price = request.form.get('price', type=float)

        # Create phone
        phone = Phone(
            model_name=model_name,
            brand_id=brand_id,
            price=price,
            model_number=model_number,
            availability_status=availability_status
        )

        db.session.add(phone)
        db.session.flush()  # Get phone ID

        # Create specifications
        specs = PhoneSpecification(
            phone_id=phone.id,
            screen_size=request.form.get('screen_size', type=float),
            processor=request.form.get('processor'),
            ram_options=request.form.get('ram_options'),
            storage_options=request.form.get('storage_options'),
            rear_camera_main=request.form.get('rear_camera_main', type=int),
            battery_capacity=request.form.get('battery_capacity', type=int),
            has_5g=bool(request.form.get('has_5g'))
        )

        db.session.add(specs)
        db.session.commit()

        flash(f'Phone "{model_name}" added successfully.', 'success')
        return redirect(url_for('admin.phones'))
```

This implementation demonstrates the transactional approach to database operations, where both the Phone and PhoneSpecification records are created in a single transaction. The `db.session.flush()` method ensures the phone ID is available before creating associated specifications, maintaining referential integrity.

**Admin Dashboard Analytics**

The admin dashboard aggregates system-wide statistics through database queries:

```python
@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard"""
    # Get statistics
    total_users = User.query.filter_by(is_admin=False).count()
    total_phones = Phone.query.filter_by(is_active=True).count()
    total_brands = Brand.query.filter_by(is_active=True).count()

    # Today's recommendations
    today = datetime.utcnow().date()
    today_recommendations = Recommendation.query.filter(
        db.func.date(Recommendation.created_at) == today
    ).count()

    # Get popular phones (most recommended)
    popular_phones = db.session.query(
        Phone,
        db.func.count(Recommendation.id).label('recommendation_count')
    ).join(Recommendation).group_by(Phone.id)\
     .order_by(db.func.count(Recommendation.id).desc())\
     .limit(5)\
     .all()
```

The dashboard analytics utilize SQLAlchemy's advanced querying capabilities, including aggregate functions (`count`), joins, and grouping operations to provide real-time insights into system usage and popular smartphones.

---

#### 5.3.1.2 User Management Module Models

The User Management Module handles regular user operations including registration, authentication, profile management, preferences configuration, and viewing past recommendations and comparisons. This module is built on two primary models: User and UserPreference.

**User Authentication Model**

The User model implements Flask-Login's UserMixin for session management and secure authentication:

```python
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'

    def set_password(self, password):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify password against hash"""
        return check_password_hash(self.password_hash, password)

    def update_last_active(self):
        """Update last active timestamp"""
        self.last_active = datetime.utcnow()
        db.session.commit()
```

The model implements secure password handling through Werkzeug's `generate_password_hash` and `check_password_hash` functions, which use the pbkdf2:sha256 algorithm. Passwords are never stored in plain text, ensuring security compliance. The `user_loader` decorator enables Flask-Login to retrieve user objects from user IDs stored in session cookies.

**User Registration and Login Implementation**

The authentication controller handles user registration with comprehensive validation:

```python
@bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        user_category = request.form.get('user_category')
        age_range = request.form.get('age_range')

        # Validation
        if not all([full_name, email, password, confirm_password]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth/register.html')

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered. Please login.', 'warning')
            return redirect(url_for('auth.login'))

        # Create new user
        user = User(
            full_name=full_name,
            email=email,
            user_category=user_category,
            age_range=age_range
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
```

**UserPreference Model for Personalization**

The UserPreference model stores detailed user preferences for AI-powered recommendations:

```python
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
```

The UserPreference model enables personalized recommendations by storing user-specific criteria including budget range, technical specifications (RAM, storage, camera, battery), 5G requirements, and screen size preferences. JSON fields store complex data structures for usage patterns, important features, and brand preferences, providing flexibility for multi-value selections.

**User Profile and Preferences Management**

The user controller implements profile editing with password change functionality:

```python
@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page"""
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.user_category = request.form.get('user_category', current_user.user_category)
        current_user.age_range = request.form.get('age_range', current_user.age_range)

        # Update password if provided
        new_password = request.form.get('new_password')
        if new_password:
            current_password = request.form.get('current_password')
            if current_user.check_password(current_password):
                current_user.set_password(new_password)
                flash('Password updated successfully.', 'success')
            else:
                flash('Current password is incorrect.', 'danger')
                return render_template('user/profile.html')

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile'))
```

---

#### 5.3.1.3 Brand & Phone Details Module Models

The Brand & Phone Details Module manages smartphone brands, phone models, detailed specifications, and product categorization. This module implements two primary models: Brand and Phone, along with the PhoneSpecification model for detailed technical attributes.

**Brand Model**

The Brand model represents smartphone manufacturers and their attributes:

```python
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
```

The Brand model includes utility methods `get_phone_count()` and `get_price_range()` that provide aggregated information about associated phones. The `is_featured` flag enables prioritizing certain brands on the homepage. The one-to-many relationship with Phone models uses `lazy='dynamic'` loading, which returns a query object rather than loading all phones immediately, improving performance for brands with many phone models.

**Phone Model with Price Categorization**

The Phone model represents individual smartphone products:

```python
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
```

The Phone model implements database indexing on `model_name`, `price`, and `is_active` columns to optimize query performance for common search and filter operations. The `get_price_category()` method provides automatic categorization based on Malaysian Ringgit price ranges (Budget: <RM1000, Mid-range: RM1000-2000, Upper-mid: RM2000-3000, Premium: >RM3000). The one-to-one relationship with PhoneSpecification uses `cascade='all, delete-orphan'` to ensure specification records are automatically deleted when the parent phone is removed.

**PhoneSpecification Model for Technical Details**

The PhoneSpecification model stores comprehensive technical attributes:

```python
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
```

The comprehensive specification model stores over 25 different attributes covering display, performance, camera, battery, connectivity, and physical characteristics. The `has_5g` field is indexed to support efficient filtering for 5G-capable devices, a key feature for users seeking future-proof smartphones. String fields for options (ram_options, storage_options) allow flexible storage of multiple variants without requiring separate tables.

---

#### 5.3.1.4 Phone Comparison Module Models

The Phone Comparison Module enables users to compare up to two phones side-by-side with detailed specification comparisons. This module utilizes the Comparison model for storing comparison history and implements the PhoneComparison class for comparison logic.

**Comparison Model for History Tracking**

```python
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
```

The Comparison model implements dual foreign key relationships to the Phone model, enabling storage of comparison pairs. The `is_saved` flag allows users to bookmark important comparisons for future reference. The model uses `foreign_keys` parameter in relationships to explicitly specify which foreign key column corresponds to each relationship, resolving the ambiguity of having two references to the same table.

**Phone Comparison Logic Implementation**

The PhoneComparison class implements comprehensive comparison functionality:

```python
"""
Phone Comparison Module
Handles side-by-side phone comparisons
"""
from app import db
from app.models import Phone, PhoneSpecification, Comparison

class PhoneComparison:
    """Phone comparison functionality"""

    def __init__(self):
        self.comparison_categories = [
            'price',
            'display',
            'performance',
            'camera',
            'battery',
            'connectivity',
            'features'
        ]

    def compare_phones(self, phone1_id, phone2_id, user_id=None):
        """
        Compare two phones side-by-side

        Args:
            phone1_id: ID of first phone
            phone2_id: ID of second phone
            user_id: Optional user ID to save comparison

        Returns:
            Dictionary with comparison data
        """
        phone1 = Phone.query.get(phone1_id)
        phone2 = Phone.query.get(phone2_id)

        if not phone1 or not phone2:
            return None

        specs1 = PhoneSpecification.query.filter_by(phone_id=phone1_id).first()
        specs2 = PhoneSpecification.query.filter_by(phone_id=phone2_id).first()

        # Build comparison data
        comparison_data = {
            'phone1': {
                'info': phone1,
                'specs': specs1
            },
            'phone2': {
                'info': phone2,
                'specs': specs2
            },
            'comparison': self._build_comparison_table(phone1, specs1, phone2, specs2),
            'winner': self._determine_winner(phone1, specs1, phone2, specs2)
        }

        # Save comparison if user_id provided
        if user_id:
            self._save_comparison(user_id, phone1_id, phone2_id)

        return comparison_data
```

**Comparison Table Building**

The comparison module creates structured comparison data across multiple categories:

```python
def _build_comparison_table(self, phone1, specs1, phone2, specs2):
    """Build detailed comparison table"""
    comparison = {
        'price': {
            'label': 'Price',
            'phone1': f"RM {phone1.price:,.2f}",
            'phone2': f"RM {phone2.price:,.2f}",
            'winner': 1 if phone1.price < phone2.price else 2,
            'difference': abs(phone1.price - phone2.price)
        }
    }

    if specs1 and specs2:
        # Camera comparisons
        comparison['rear_camera'] = {
            'label': 'Rear Camera',
            'phone1': specs1.rear_camera or 'N/A',
            'phone2': specs2.rear_camera or 'N/A',
            'winner': 1 if (specs1.rear_camera_main or 0) > (specs2.rear_camera_main or 0) else 2
        }

        # Battery comparisons
        comparison['battery'] = {
            'label': 'Battery Capacity',
            'phone1': f"{specs1.battery_capacity}mAh" if specs1.battery_capacity else 'N/A',
            'phone2': f"{specs2.battery_capacity}mAh" if specs2.battery_capacity else 'N/A',
            'winner': 1 if (specs1.battery_capacity or 0) > (specs2.battery_capacity or 0) else 2
        }

        # 5G Support
        comparison['5g'] = {
            'label': '5G Support',
            'phone1': '✓ Yes' if specs1.has_5g else '✗ No',
            'phone2': '✓ Yes' if specs2.has_5g else '✗ No',
            'winner': 1 if specs1.has_5g else 2 if specs2.has_5g else None
        }

    return comparison
```

The comparison table structure provides human-readable formatted values alongside raw data for winner determination. Each comparison item includes label, values for both phones, winner indication, and optional difference calculation. The system uses conditional expressions to handle missing data gracefully, displaying 'N/A' when specifications are unavailable.

**Winner Determination Algorithm**

```python
def _determine_winner(self, phone1, specs1, phone2, specs2):
    """Determine overall winner based on multiple factors"""
    phone1_score = 0
    phone2_score = 0

    # Price (lower is better)
    if phone1.price < phone2.price:
        phone1_score += 1
    else:
        phone2_score += 1

    if specs1 and specs2:
        # Camera
        if (specs1.rear_camera_main or 0) > (specs2.rear_camera_main or 0):
            phone1_score += 1
        elif (specs2.rear_camera_main or 0) > (specs1.rear_camera_main or 0):
            phone2_score += 1

        # Battery
        if (specs1.battery_capacity or 0) > (specs2.battery_capacity or 0):
            phone1_score += 1
        elif (specs2.battery_capacity or 0) > (specs1.battery_capacity or 0):
            phone2_score += 1

        # 5G
        if specs1.has_5g and not specs2.has_5g:
            phone1_score += 1
        elif specs2.has_5g and not specs1.has_5g:
            phone2_score += 1

    if phone1_score > phone2_score:
        return {'phone': 1, 'name': phone1.model_name, 'score': phone1_score}
    elif phone2_score > phone1_score:
        return {'phone': 2, 'name': phone2.model_name, 'score': phone2_score}
    else:
        return {'phone': None, 'name': 'Tie', 'score': phone1_score}
```

The winner determination algorithm assigns points across multiple categories including price (lower is better), camera quality, battery capacity, 5G support, and screen refresh rate. The scoring system provides an objective comparison while allowing for ties when phones are evenly matched.

---

#### 5.3.1.5 AI Chatbot Module Models

The AI Chatbot Module implements natural language processing capabilities for conversational phone recommendations. The ChatHistory model stores all chat interactions for context maintenance and conversation analysis.

**ChatHistory Model**

```python
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

    # Metadata (JSON stored as string)
    metadata = db.Column(db.Text)  # Additional context like recommended phone IDs

    # Timestamp
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
```

The ChatHistory model stores complete conversation turns including user messages and bot responses. The `session_id` field groups related conversations, enabling context-aware responses across multiple message exchanges. The `intent` field records the detected user intention (greeting, budget_query, recommendation, comparison, etc.), which is crucial for improving the chatbot's natural language understanding over time through analysis of historical data.

**Chatbot Message Processing**

The chatbot engine implements intent detection and response generation:

```python
class ChatbotEngine:
    """Conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better'],
            'specification': ['specs', 'specification', 'camera', 'battery', 'ram', 'storage', 'screen'],
            'brand_query': ['brand', 'samsung', 'apple', 'iphone', 'xiaomi', 'huawei'],
            'help': ['help', 'how', 'what can you do'],
            'usage_type': ['gaming', 'photography', 'camera', 'business', 'work', 'social media', 'entertainment']
        }

    def process_message(self, user_id, message, session_id=None):
        """Process user message and generate response"""
        # Detect intent
        intent = self._detect_intent(message.lower())

        # Generate response based on intent
        response_data = self._generate_response(user_id, message, intent)

        # Save to chat history
        self._save_chat_history(
            user_id=user_id,
            message=message,
            response=response_data['response'],
            intent=intent,
            session_id=session_id,
            metadata=response_data.get('metadata', {})
        )

        return response_data
```

**Natural Language Processing for Budget Extraction**

The chatbot implements pattern matching for extracting structured data from natural language:

```python
def _extract_budget(self, message):
    """Extract budget range from message"""
    # Look for patterns like "RM1000", "1000", "under 2000", "between 1000 and 2000"
    patterns = [
        r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
        r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000
        r'under\s*rm?\s*(\d+)',  # under RM2000
        r'below\s*rm?\s*(\d+)',  # below 2000
        r'rm\s*(\d+)',  # RM2000
    ]

    for pattern in patterns:
        match = re.search(pattern, message.lower())
        if match:
            if 'under' in message.lower() or 'below' in message.lower():
                max_budget = int(match.group(1))
                return (500, max_budget)
            elif len(match.groups()) == 2:
                return (int(match.group(1)), int(match.group(2)))
            else:
                value = int(match.group(1))
                return (500, value)

    return None
```

The budget extraction function uses regular expressions to parse various natural language formats including "RM1000 to RM2000", "under 2000", "between 1000 and 2000", enabling flexible user input while maintaining structured data for database queries.

**Chatbot Response Generation**

```python
def _generate_response(self, user_id, message, intent):
    """Generate appropriate response based on intent"""

    if intent == 'budget_query':
        # Extract budget from message
        budget = self._extract_budget(message)
        if budget:
            min_budget, max_budget = budget
            phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=3)

            if phones:
                response = f"Here are the top phones within RM{min_budget} - RM{max_budget}:\n\n"
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price
                    })

                return {
                    'response': response,
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }
```

---

#### 5.3.1.6 Recommendation System Core Logic Models

The Recommendation System Core Logic implements AI-powered phone recommendations based on user preferences, usage patterns, and technical requirements. The Recommendation model stores historical recommendations with match scores and reasoning.

**Recommendation Model**

```python
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
```

The Recommendation model stores not only the recommendation result but also the match percentage (0-100) and human-readable reasoning explaining why the phone was recommended. The `user_criteria` field stores the original search parameters as JSON, enabling analysis of recommendation accuracy and system improvement over time. User feedback fields (`is_viewed`, `is_saved`, `user_rating`) facilitate recommendation quality assessment and algorithm refinement.

**AI Recommendation Engine Implementation**

```python
from app import db
from app.models import Phone, PhoneSpecification, UserPreference, Recommendation
from app.utils.helpers import calculate_match_score, generate_recommendation_reasoning
import json

class AIRecommendationEngine:
    """AI-powered recommendation engine for smartphones"""

    def __init__(self):
        self.min_match_threshold = 50  # Minimum match percentage to recommend

    def get_recommendations(self, user_id, criteria=None, top_n=3):
        """
        Get top N phone recommendations for a user

        Args:
            user_id: User ID to get recommendations for
            criteria: Optional dictionary of criteria to override user preferences
            top_n: Number of recommendations to return

        Returns:
            List of recommended phones with match scores
        """
        from app.models import User

        user = User.query.get(user_id)
        if not user:
            return []

        # Get or create user preferences
        user_prefs = UserPreference.query.filter_by(user_id=user_id).first()

        # If criteria provided, create temporary preference object
        if criteria:
            user_prefs = self._create_temp_preferences(criteria)
        elif not user_prefs:
            user_prefs = self._create_default_preferences(user_id)

        # Get all active phones with their specifications
        phones = Phone.query.filter_by(is_active=True).all()

        # Calculate match scores for each phone
        recommendations = []
        for phone in phones:
            phone_specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            # Calculate match score
            match_score = calculate_match_score(user_prefs, phone, phone_specs)

            # Only include if above threshold
            if match_score >= self.min_match_threshold:
                reasoning = generate_recommendation_reasoning(
                    match_score, user_prefs, phone, phone_specs
                )

                recommendations.append({
                    'phone': phone,
                    'specifications': phone_specs,
                    'match_score': match_score,
                    'reasoning': reasoning
                })

        # Sort by match score (descending)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Save recommendations to database
        if not criteria and user_prefs and hasattr(user_prefs, 'user_id'):
            self._save_recommendations(user_id, recommendations[:top_n], user_prefs)

        return recommendations[:top_n]
```

The recommendation engine implements a filtering approach where all active phones are evaluated against user preferences, with only matches exceeding the 50% threshold being returned. This ensures recommendation quality while maintaining sufficient result diversity.

**Match Score Calculation Algorithm**

```python
def calculate_match_score(user_prefs, phone, phone_specs):
    """
    Calculate how well a phone matches user preferences
    Returns a score from 0-100
    """
    score = 0
    max_score = 0

    # Budget match (weight: 30)
    max_score += 30
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        score += 30
    elif phone.price < user_prefs.min_budget:
        score += 20
    else:
        over_budget = phone.price - user_prefs.max_budget
        penalty = min(30, (over_budget / user_prefs.max_budget) * 30)
        score += max(0, 30 - penalty)

    if phone_specs:
        # RAM match (weight: 10)
        max_score += 10
        if phone_specs.ram_options:
            ram_values = [int(r.replace('GB', '')) for r in phone_specs.ram_options.split(',') if 'GB' in r]
            if ram_values and max(ram_values) >= user_prefs.min_ram:
                score += 10

        # Camera match (weight: 15)
        max_score += 15
        if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
            score += 15

        # Battery match (weight: 15)
        max_score += 15
        if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
            score += 15

        # 5G requirement (weight: 10)
        max_score += 10
        if user_prefs.requires_5g:
            if phone_specs.has_5g:
                score += 10
        else:
            score += 10  # No requirement, so full points

    # Calculate final percentage
    if max_score > 0:
        return round((score / max_score) * 100, 2)
    return 0
```

The match score algorithm implements weighted scoring across six key factors: Budget (30%), Camera (15%), Battery (15%), RAM (10%), 5G Support (10%), and Screen Size (10%). The budget component implements graduated scoring: full points for within-budget phones, partial credit for cheaper phones, and proportional penalties for over-budget options. This nuanced approach prevents artificial boundary effects where a phone RM1 over budget would score dramatically worse than one at the exact budget limit.

**Recommendation Reasoning Generation**

```python
def generate_recommendation_reasoning(match_score, user_prefs, phone, phone_specs):
    """Generate human-readable reasoning for recommendation"""
    reasons = []

    # Budget
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        reasons.append(f"Within your budget of {format_price(user_prefs.min_budget)} - {format_price(user_prefs.max_budget)}")

    if phone_specs:
        # Performance
        if phone_specs.ram_options:
            ram_values = [int(r.replace('GB', '')) for r in phone_specs.ram_options.split(',') if 'GB' in r]
            if ram_values:
                max_ram = max(ram_values)
                if max_ram >= user_prefs.min_ram:
                    reasons.append(f"Excellent performance with up to {max_ram}GB RAM")

        # Camera
        if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
            reasons.append(f"Great {phone_specs.rear_camera_main}MP camera for photography")

        # Battery
        if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
            reasons.append(f"Long-lasting {phone_specs.battery_capacity}mAh battery")

        # 5G
        if phone_specs.has_5g:
            reasons.append("Future-ready with 5G connectivity")

    if not reasons:
        reasons.append("Good overall specifications for the price")

    return " • ".join(reasons)
```

The reasoning generation function creates human-readable explanations for why each phone was recommended, highlighting the specific features that match user preferences. This transparency builds user trust in the recommendation system and helps users understand the trade-offs between different options.

---

#### 5.3.1.7 Model Relationships and Database Integrity

The DialSmart database schema implements comprehensive relationships between models ensuring referential integrity and cascade operations:

```python
# User relationships
preferences = db.relationship('UserPreference', backref='user', lazy='dynamic', cascade='all, delete-orphan')
recommendations = db.relationship('Recommendation', backref='user', lazy='dynamic', cascade='all, delete-orphan')
comparisons = db.relationship('Comparison', backref='user', lazy='dynamic', cascade='all, delete-orphan')
chat_history = db.relationship('ChatHistory', backref='user', lazy='dynamic', cascade='all, delete-orphan')

# Brand relationships
phones = db.relationship('Phone', backref='brand', lazy='dynamic')

# Phone relationships
specifications = db.relationship('PhoneSpecification', backref='phone', uselist=False, cascade='all, delete-orphan')
```

The cascade options (`cascade='all, delete-orphan'`) ensure that when a user is deleted, all associated preferences, recommendations, comparisons, and chat history are automatically removed, maintaining database consistency. The `lazy='dynamic'` loading strategy optimizes performance by returning query objects rather than loading related records immediately, particularly beneficial for users with extensive recommendation or comparison histories.

---

### Conclusion

The Model layer of the DialSmart system demonstrates comprehensive implementation of database-driven application architecture across six major functional modules. Each model is carefully designed with appropriate data types, indexes, relationships, and business logic methods. The module-based organization (Admin Management, User Management, Brand & Phone Details, Phone Comparison, AI Chatbot, and Recommendation System) provides clear separation of concerns while maintaining strong inter-module relationships through foreign keys and SQLAlchemy relationships. The implementation leverages SQLAlchemy ORM capabilities including lazy loading, cascade operations, and complex queries to deliver efficient, maintainable, and scalable data management for the DialSmart AI-powered smartphone recommendation system.
