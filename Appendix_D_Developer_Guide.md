# Appendix D: Developer Guide

## D.1 Development Environment Setup

### D.1.1 Required Tools and Software

| Tool | Version | Purpose |
|------|---------|---------|
| **Python** | 3.8+ | Primary programming language |
| **pip** | Latest | Python package manager |
| **Git** | 2.0+ | Version control |
| **Code Editor** | Any | VS Code, PyCharm, Sublime Text |
| **Browser** | Latest | Chrome/Firefox with DevTools |
| **SQLite Browser** | Optional | Database inspection tool |

### D.1.2 Setting Up Development Environment

#### Step 1: Clone Repository

```bash
git clone <repository-url>
cd DialSmart
```

#### Step 2: Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verification:**
```bash
which python  # Should point to venv/bin/python
pip list      # Should show minimal packages
```

#### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Packages:**
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
SQLAlchemy==2.0.23
Werkzeug==3.0.1
email-validator==2.1.0
python-dateutil==2.8.2
python-dotenv==1.0.0
flask-shell-ipython==0.4.1
```

#### Step 4: Install Development Dependencies (Optional)

```bash
pip install pytest pytest-cov black flake8 pylint
```

- **pytest**: Unit testing framework
- **pytest-cov**: Code coverage reports
- **black**: Code formatter
- **flake8**: Linting tool
- **pylint**: Static code analysis

#### Step 5: Initialize Database

```bash
flask init-db
flask seed-data
```

#### Step 6: Create Admin Account

```bash
flask create-admin
# Follow prompts to create admin user
```

#### Step 7: Configure Environment Variables

Create `.env` file:
```bash
touch .env
```

Add configuration:
```env
SECRET_KEY=your-secret-development-key
FLASK_ENV=development
FLASK_APP=run.py
DEBUG=True
DATABASE_URL=sqlite:///dialsmart.db
```

#### Step 8: Run Development Server

```bash
python run.py
```

Or:
```bash
flask run --debug
```

**Server runs at:** `http://localhost:5000`

### D.1.3 IDE Configuration

#### Visual Studio Code

**Recommended Extensions:**
- Python (Microsoft)
- Pylance
- Flask Snippets
- SQLite Viewer
- GitLens
- Jinja2 Snippet Kit

**Settings (`.vscode/settings.json`):**
```json
{
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.terminal.activateEnvironment": true,
    "editor.formatOnSave": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true,
        "**/.pytest_cache": true
    }
}
```

#### PyCharm

1. **Open Project** → Select DialSmart folder
2. **Configure Interpreter** → Add Python Interpreter → Existing environment → Select `venv/bin/python`
3. **Enable Flask Support** → Settings → Languages & Frameworks → Flask
   - Check "Enable Flask support"
   - Templates folder: `app/templates`
   - Static folder: `app/static`

### D.1.4 Database Development Tools

#### SQLite Browser

**Installation:**
```bash
# Ubuntu/Debian
sudo apt install sqlitebrowser

# macOS
brew install --cask db-browser-for-sqlite

# Windows
Download from: https://sqlitebrowser.org/
```

**Usage:**
1. Open SQLite Browser
2. File → Open Database
3. Select `dialsmart.db`
4. Browse tables, execute queries, inspect schema

#### Flask Shell

**Access database in interactive shell:**
```bash
flask shell
```

**Example operations:**
```python
# Query users
>>> users = User.query.all()
>>> print(users)

# Query phones
>>> phones = Phone.query.filter_by(brand_id=1).all()

# Create new brand
>>> brand = Brand(name='OnePlus', description='Chinese smartphone manufacturer')
>>> db.session.add(brand)
>>> db.session.commit()

# Update phone price
>>> phone = Phone.query.get(1)
>>> phone.price = 1999.00
>>> db.session.commit()

# Delete record
>>> phone = Phone.query.get(5)
>>> db.session.delete(phone)
>>> db.session.commit()
```

---

## D.2 Application Architecture

### D.2.1 Application Factory Pattern

**File:** `app/__init__.py`

```python
def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    from app.routes import auth, user, admin, phone, api
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(phone.bp)
    app.register_blueprint(api.bp)

    return app
```

**Benefits:**
- Multiple app instances (testing, production)
- Cleaner extension initialization
- Blueprint modularization
- Easier testing with different configurations

### D.2.2 Blueprint Architecture

**Blueprints organize routes into modules:**

| Blueprint | Prefix | File | Purpose |
|-----------|--------|------|---------|
| `auth` | `/` | `app/routes/auth.py` | Authentication (login, register, logout) |
| `user` | `/` | `app/routes/user.py` | User-facing features (dashboard, profile) |
| `admin` | `/admin` | `app/routes/admin.py` | Admin panel |
| `phone` | `/phones` | `app/routes/phone.py` | Phone browsing and comparison |
| `api` | `/api` | `app/routes/api.py` | REST API endpoints |

**Example Blueprint Registration:**
```python
from flask import Blueprint

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Login logic
    pass

@bp.route('/register', methods=['GET', 'POST'])
def register():
    # Registration logic
    pass
```

### D.2.3 MVC Architecture

**Model-View-Controller Pattern:**

```
User Request
    ↓
Routes (Controller) → Process request
    ↓
Models (Model) → Database operations
    ↓
Templates (View) → Render HTML
    ↓
Response to User
```

**Components:**

1. **Models** (`app/models/`)
   - Define database schema
   - Business logic methods
   - Relationships between entities

2. **Controllers** (`app/routes/`)
   - Handle HTTP requests
   - Process form data
   - Call model methods
   - Return responses

3. **Views** (`app/templates/`)
   - Jinja2 templates
   - Render dynamic HTML
   - Display data from models

---

## D.3 Database Models and Relationships

### D.3.1 User Model

**File:** `app/models/user.py`

```python
class User(UserMixin, db.Model):
    """User model for authentication and profile"""
    __tablename__ = 'users'

    # Primary key
    id = db.Column(db.Integer, primary_key=True)

    # User information
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)

    # Categorization
    user_category = db.Column(db.String(50))  # Student, Working Professional, etc.
    age_range = db.Column(db.String(20))  # 18-25, 26-35, etc.

    # Account settings
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_active = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    preferences = db.relationship('UserPreference', backref='user', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', backref='user', cascade='all, delete-orphan')
```

**Key Methods:**

```python
def set_password(self, password):
    """Hash and set user password"""
    self.password_hash = generate_password_hash(password)

def check_password(self, password):
    """Verify password against hash"""
    return check_password_hash(self.password_hash, password)
```

### D.3.2 Brand Model

**File:** `app/models/brand.py`

```python
class Brand(db.Model):
    """Smartphone brand model"""
    __tablename__ = 'brands'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    tagline = db.Column(db.String(200))
    is_featured = db.Column(db.Boolean, default=False)
    logo_url = db.Column(db.String(255))

    # Relationships
    phones = db.relationship('Phone', backref='brand', lazy='dynamic')
```

### D.3.3 Phone Model

**File:** `app/models/phone.py`

```python
class Phone(db.Model):
    """Smartphone model"""
    __tablename__ = 'phones'

    id = db.Column(db.Integer, primary_key=True)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)
    model_name = db.Column(db.String(200), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    availability_status = db.Column(db.String(50), default='Available')
    release_date = db.Column(db.Date)
    image_url = db.Column(db.String(255))

    # Relationships
    specifications = db.relationship('PhoneSpecification', backref='phone',
                                    uselist=False, cascade='all, delete-orphan')
```

### D.3.4 PhoneSpecification Model

**File:** `app/models/phone.py`

```python
class PhoneSpecification(db.Model):
    """Detailed phone specifications"""
    __tablename__ = 'phone_specifications'

    id = db.Column(db.Integer, primary_key=True)
    phone_id = db.Column(db.Integer, db.ForeignKey('phones.id'), nullable=False)

    # Display
    screen_size = db.Column(db.Float)
    screen_resolution = db.Column(db.String(50))
    screen_type = db.Column(db.String(100))
    refresh_rate = db.Column(db.Integer)

    # Performance
    processor = db.Column(db.String(100))
    processor_brand = db.Column(db.String(50))
    ram_options = db.Column(db.String(100))
    storage_options = db.Column(db.String(100))

    # Camera
    rear_camera = db.Column(db.String(200))
    rear_camera_main = db.Column(db.Integer)
    front_camera = db.Column(db.String(100))
    front_camera_mp = db.Column(db.Integer)

    # Battery
    battery_capacity = db.Column(db.Integer)
    charging_speed = db.Column(db.String(100))
    wireless_charging = db.Column(db.Boolean, default=False)

    # Connectivity
    has_5g = db.Column(db.Boolean, default=False)
    wifi = db.Column(db.String(50))
    bluetooth = db.Column(db.String(50))
    nfc = db.Column(db.Boolean, default=False)

    # Other features
    operating_system = db.Column(db.String(100))
    fingerprint_sensor = db.Column(db.Boolean, default=False)
    face_unlock = db.Column(db.Boolean, default=False)
    water_resistance = db.Column(db.String(50))
    weight = db.Column(db.Integer)
```

### D.3.5 Database Relationships Diagram

```
User (1) ──< (M) UserPreference
User (1) ──< (M) Recommendation
User (1) ──< (M) Comparison
User (1) ──< (M) ChatHistory

Brand (1) ──< (M) Phone
Phone (1) ─── (1) PhoneSpecification

Recommendation (M) ──> (1) Phone
Comparison (M) ──> (1) Phone (phone1_id)
Comparison (M) ──> (1) Phone (phone2_id)
```

**Legend:**
- (1) = One
- (M) = Many
- ─── = One-to-One
- ──< = One-to-Many
- ──> = Many-to-One

---

## D.4 Key Modules and Functions

### D.4.1 AI Recommendation Engine

**File:** `app/modules/ai_engine.py`

**Purpose:** Generate personalized phone recommendations using AI algorithms

**Key Class:**
```python
class AIRecommendationEngine:
    """AI-powered phone recommendation system"""

    def __init__(self):
        self.weights = {
            'price': 0.25,
            'camera': 0.20,
            'battery': 0.15,
            'performance': 0.20,
            'brand': 0.10,
            'features': 0.10
        }
```

**Main Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `get_recommendations()` | `user_criteria: dict` | `list[dict]` | Generate top phone recommendations |
| `calculate_match_score()` | `phone: Phone, criteria: dict` | `float` | Calculate match score (0-100) |
| `filter_by_criteria()` | `phones: list, criteria: dict` | `list` | Filter phones by user criteria |
| `rank_recommendations()` | `scored_phones: list` | `list` | Sort by match score |
| `generate_reasoning()` | `phone: Phone, score: float` | `str` | Explain why phone recommended |

**Example Usage:**
```python
from app.modules.ai_engine import AIRecommendationEngine

engine = AIRecommendationEngine()

criteria = {
    'budget': {'min': 1000, 'max': 3000},
    'primary_usage': ['Photography', 'Social Media'],
    'important_features': ['Camera', 'Battery'],
    'technical': {
        'min_ram': 6,
        'min_storage': 128,
        'requires_5g': True
    }
}

recommendations = engine.get_recommendations(criteria)
# Returns top 5 phones with match scores and reasoning
```

**Algorithm Overview:**
1. **Filter Stage:** Remove phones outside budget and minimum specs
2. **Scoring Stage:** Calculate weighted score based on criteria
3. **Ranking Stage:** Sort phones by match score
4. **Reasoning Stage:** Generate explanation for each recommendation

### D.4.2 Chatbot Module

**File:** `app/modules/chatbot.py`

**Purpose:** Natural language processing for conversational recommendations

**Key Class:**
```python
class ChatbotEngine:
    """NLP-powered chatbot for phone recommendations"""

    def __init__(self):
        self.intent_patterns = {
            'budget_query': [r'under\s+RM?\s*(\d+)', r'below\s+(\d+)', r'less than\s+(\d+)'],
            'feature_query': [r'(good|best)\s+(camera|battery|performance)'],
            'comparison': [r'compare\s+(.+)\s+(vs|and)\s+(.+)'],
            'recommendation': [r'recommend|suggest|show me'],
        }
```

**Main Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `process_message()` | `user_message: str, user_id: int` | `dict` | Process user message and generate response |
| `detect_intent()` | `message: str` | `str` | Identify user's intent |
| `extract_criteria()` | `message: str` | `dict` | Extract budget, features from text |
| `generate_response()` | `intent: str, criteria: dict` | `str` | Create chatbot response |
| `save_conversation()` | `user_id: int, message: str, response: str` | `None` | Save chat history |

**Example Usage:**
```python
from app.modules.chatbot import ChatbotEngine

chatbot = ChatbotEngine()

response = chatbot.process_message(
    user_message="I need a phone under RM2000 with good camera",
    user_id=1
)

# Returns:
# {
#     'intent': 'budget_query',
#     'criteria': {'max_budget': 2000, 'feature_priority': 'camera'},
#     'response': "I found several great options under RM2000 with excellent cameras...",
#     'recommendations': [...]
# }
```

**NLP Features:**
- Regex-based intent detection
- Budget extraction (e.g., "under RM2000" → max_budget: 2000)
- Feature identification (e.g., "good camera" → feature_priority: camera)
- Context-aware responses
- Conversation history tracking

### D.4.3 Phone Comparison Module

**File:** `app/modules/comparison.py`

**Purpose:** Side-by-side phone comparisons with winner detection

**Key Class:**
```python
class PhoneComparison:
    """Phone comparison functionality"""

    def __init__(self):
        self.comparison_categories = [
            'price', 'display', 'performance',
            'camera', 'battery', 'connectivity', 'features'
        ]
```

**Main Methods:**

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `compare_phones()` | `phone1_id: int, phone2_id: int, user_id: int` | `dict` | Generate full comparison |
| `_build_comparison_table()` | `phone1: Phone, specs1: Specs, phone2: Phone, specs2: Specs` | `dict` | Build comparison data |
| `_determine_winner()` | `phone1: Phone, specs1: Specs, phone2: Phone, specs2: Specs` | `dict` | Calculate overall winner |
| `get_user_comparisons()` | `user_id: int, limit: int` | `list` | Get comparison history |
| `save_comparison()` | `comparison_id: int` | `bool` | Mark comparison as saved |

**Example Usage:**
```python
from app.modules.comparison import PhoneComparison

comparator = PhoneComparison()

comparison = comparator.compare_phones(
    phone1_id=1,  # Samsung Galaxy S23
    phone2_id=2,  # iPhone 15 Pro
    user_id=1
)

# Returns:
# {
#     'phone1': {...},
#     'phone2': {...},
#     'comparison': {
#         'price': {'phone1': 'RM 5299', 'phone2': 'RM 5999', 'winner': 1},
#         'camera': {'phone1': '200MP', 'phone2': '48MP', 'winner': 1},
#         ...
#     },
#     'winner': {'phone': 1, 'name': 'Samsung Galaxy S23 Ultra', 'score': 6}
# }
```

**Comparison Categories:**

| Category | Metrics Compared | Winner Criteria |
|----------|------------------|-----------------|
| **Price** | Price in RM | Lower price wins |
| **Display** | Size, resolution, type, refresh rate | Larger size, higher refresh wins |
| **Performance** | Processor, RAM, storage | More RAM/storage wins |
| **Camera** | Rear MP, front MP | Higher MP wins |
| **Battery** | Capacity (mAh), charging speed | Higher capacity wins |
| **Connectivity** | 5G, NFC, wireless charging | More features win |
| **Features** | OS, fingerprint, water resistance | Feature availability |

**Winner Detection Algorithm:**
```python
def _determine_winner(phone1, specs1, phone2, specs2):
    phone1_score = 0
    phone2_score = 0

    # Price (lower is better)
    if phone1.price < phone2.price:
        phone1_score += 1

    # Screen size (larger is better)
    if specs1.screen_size > specs2.screen_size:
        phone1_score += 1

    # Camera (higher MP is better)
    if specs1.rear_camera_main > specs2.rear_camera_main:
        phone1_score += 1

    # Battery (higher capacity is better)
    if specs1.battery_capacity > specs2.battery_capacity:
        phone1_score += 1

    # 5G support
    if specs1.has_5g and not specs2.has_5g:
        phone1_score += 1

    # Refresh rate
    if specs1.refresh_rate > specs2.refresh_rate:
        phone1_score += 1

    if phone1_score > phone2_score:
        return {'phone': 1, 'name': phone1.model_name, 'score': phone1_score}
    elif phone2_score > phone1_score:
        return {'phone': 2, 'name': phone2.model_name, 'score': phone2_score}
    else:
        return {'phone': None, 'name': 'Tie', 'score': phone1_score}
```

---

## D.5 Authentication and Security

### D.5.1 Password Hashing

**Method:** Werkzeug PBKDF2-SHA256

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hash password
password_hash = generate_password_hash('user_password')

# Verify password
is_valid = check_password_hash(password_hash, 'user_password')
```

**Security Features:**
- PBKDF2 key derivation function
- SHA-256 hashing algorithm
- Salt generation (automatic)
- Multiple iterations (default: 150,000)

### D.5.2 User Login with Flask-Login

```python
from flask_login import login_user, logout_user, login_required, current_user

@bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        login_user(user, remember=request.form.get('remember', False))
        return redirect(url_for('user.dashboard'))

    flash('Invalid email or password', 'danger')
    return redirect(url_for('auth.login'))

@bp.route('/dashboard')
@login_required  # Requires authentication
def dashboard():
    return render_template('dashboard.html', user=current_user)
```

### D.5.3 Role-Based Access Control

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/manage-phones')
@login_required
@admin_required
def manage_phones():
    # Only admins can access
    return render_template('admin/phones.html')
```

---

## D.6 API Development

### D.6.1 RESTful API Endpoints

**File:** `app/routes/api.py`

**Public Endpoints:**

| Endpoint | Method | Authentication | Description |
|----------|--------|----------------|-------------|
| `/api/phones` | GET | No | Get all phones |
| `/api/phones/<id>` | GET | No | Get phone details |
| `/api/brands` | GET | No | Get all brands |
| `/api/phones/search` | GET | No | Search phones |
| `/api/chat` | POST | No | Chat with bot |

**Authenticated Endpoints:**

| Endpoint | Method | Authentication | Description |
|----------|--------|----------------|-------------|
| `/api/recommendations` | POST | Yes | Get AI recommendations |
| `/api/chat/history` | GET | Yes | Get chat history |
| `/api/comparisons` | POST | Yes | Create comparison |
| `/api/preferences` | GET/POST | Yes | Get/update preferences |

**Example API Implementation:**

```python
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/phones', methods=['GET'])
def get_phones():
    """Get all phones with optional filters"""
    brand_id = request.args.get('brand_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)

    query = Phone.query

    if brand_id:
        query = query.filter_by(brand_id=brand_id)

    if min_price:
        query = query.filter(Phone.price >= min_price)

    if max_price:
        query = query.filter(Phone.price <= max_price)

    phones = query.all()

    return jsonify({
        'success': True,
        'count': len(phones),
        'phones': [phone.to_dict() for phone in phones]
    })

@api_bp.route('/recommendations', methods=['POST'])
@login_required
def get_recommendations():
    """Get AI recommendations"""
    data = request.get_json()

    criteria = {
        'budget': data.get('budget'),
        'usage': data.get('usage'),
        'features': data.get('features')
    }

    engine = AIRecommendationEngine()
    recommendations = engine.get_recommendations(criteria)

    return jsonify({
        'success': True,
        'recommendations': recommendations
    })
```

### D.6.2 JSON Response Format

**Success Response:**
```json
{
    "success": true,
    "message": "Phone retrieved successfully",
    "data": {
        "id": 1,
        "model_name": "Samsung Galaxy S23",
        "price": 5299.00,
        "brand": "Samsung",
        "specifications": {...}
    }
}
```

**Error Response:**
```json
{
    "success": false,
    "error": "Phone not found",
    "error_code": "PHONE_NOT_FOUND",
    "status_code": 404
}
```

---

## D.7 Testing

### D.7.1 Unit Testing with pytest

**Install pytest:**
```bash
pip install pytest pytest-cov
```

**Create test file:** `tests/test_models.py`

```python
import pytest
from app import create_app, db
from app.models import User, Phone, Brand

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

def test_user_password_hashing(app):
    """Test password hashing"""
    with app.app_context():
        user = User(email='test@example.com', full_name='Test User')
        user.set_password('password123')

        assert user.password_hash != 'password123'
        assert user.check_password('password123') is True
        assert user.check_password('wrong_password') is False

def test_phone_creation(app):
    """Test phone model creation"""
    with app.app_context():
        brand = Brand(name='Samsung', description='Test')
        db.session.add(brand)
        db.session.commit()

        phone = Phone(
            brand_id=brand.id,
            model_name='Galaxy S23',
            price=5299.00
        )
        db.session.add(phone)
        db.session.commit()

        assert phone.id is not None
        assert phone.brand.name == 'Samsung'
```

**Run tests:**
```bash
pytest
pytest --cov=app  # With coverage report
pytest -v  # Verbose output
```

### D.7.2 Integration Testing

```python
def test_login_flow(client, app):
    """Test user login flow"""
    with app.app_context():
        # Create test user
        user = User(email='test@example.com', full_name='Test')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()

    # Test login
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Dashboard' in response.data

def test_recommendation_api(client, app):
    """Test recommendation API endpoint"""
    # Login first
    client.post('/login', data={'email': 'test@example.com', 'password': 'password123'})

    # Test API
    response = client.post('/api/recommendations', json={
        'budget': {'min': 1000, 'max': 3000},
        'usage': ['Gaming'],
        'features': ['Performance', 'Battery']
    })

    data = response.get_json()
    assert response.status_code == 200
    assert data['success'] is True
    assert 'recommendations' in data
```

---

## D.8 Code Style and Best Practices

### D.8.1 Python Style Guide (PEP 8)

**Naming Conventions:**
- Classes: `PascalCase` (e.g., `UserPreference`)
- Functions: `snake_case` (e.g., `get_recommendations`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_UPLOAD_SIZE`)
- Private methods: `_leading_underscore` (e.g., `_calculate_score`)

**Code Formatting:**
```python
# Good
def calculate_match_score(phone, criteria):
    """Calculate match score for phone based on criteria"""
    score = 0

    if phone.price <= criteria['max_budget']:
        score += 20

    return score

# Bad
def calculateMatchScore(phone,criteria):
  score=0
  if phone.price<=criteria['max_budget']:score+=20
  return score
```

**Docstrings:**
```python
def get_recommendations(criteria, limit=5):
    """
    Generate phone recommendations based on user criteria.

    Args:
        criteria (dict): User preferences and requirements
        limit (int): Maximum number of recommendations (default: 5)

    Returns:
        list: List of recommended phones with match scores

    Raises:
        ValueError: If criteria is empty or invalid
    """
    pass
```

### D.8.2 Database Query Best Practices

**Good Practices:**
```python
# Use indexes for frequently queried fields
email = db.Column(db.String(120), unique=True, nullable=False, index=True)

# Use eager loading to avoid N+1 queries
phones = Phone.query.options(db.joinedload(Phone.brand)).all()

# Use pagination for large datasets
phones = Phone.query.paginate(page=1, per_page=20)

# Filter before loading
active_phones = Phone.query.filter_by(availability_status='Available').all()
```

**Bad Practices:**
```python
# Don't load all data if you only need some
phones = Phone.query.all()  # Loads everything!
featured = [p for p in phones if p.brand.is_featured]  # Inefficient filtering

# Avoid N+1 queries
phones = Phone.query.all()
for phone in phones:
    print(phone.brand.name)  # Each iteration queries database!
```

### D.8.3 Error Handling

```python
from flask import flash, redirect, url_for

@app.route('/phone/<int:phone_id>')
def phone_details(phone_id):
    try:
        phone = Phone.query.get_or_404(phone_id)
        return render_template('phone/details.html', phone=phone)
    except Exception as e:
        app.logger.error(f"Error loading phone {phone_id}: {str(e)}")
        flash('Error loading phone details', 'danger')
        return redirect(url_for('phone.browse'))
```

---

## D.9 Deployment

### D.9.1 Production Checklist

- [ ] Set `DEBUG = False` in config
- [ ] Use strong `SECRET_KEY`
- [ ] Configure production database (PostgreSQL/MySQL)
- [ ] Set up proper logging
- [ ] Configure HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure backup strategy
- [ ] Set up monitoring and alerts
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up reverse proxy (Nginx)

### D.9.2 Gunicorn Configuration

**Install:**
```bash
pip install gunicorn
```

**Run:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

**Configuration file:** `gunicorn_config.py`
```python
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2
loglevel = "info"
accesslog = "/var/log/dialsmart/access.log"
errorlog = "/var/log/dialsmart/error.log"
```

**Run with config:**
```bash
gunicorn -c gunicorn_config.py run:app
```

---

**End of Appendix D**
