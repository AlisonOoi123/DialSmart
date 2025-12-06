# Appendix B: System Document

## B.1 Hardware Requirements

### B.1.1 Minimum Hardware Requirements

| Component | Specification |
|-----------|--------------|
| **Processor** | Intel Core i3 or AMD equivalent (2.0 GHz or higher) |
| **RAM** | 4 GB |
| **Storage** | 2 GB available disk space |
| **Display** | 1024 x 768 resolution or higher |
| **Network** | Broadband internet connection (1 Mbps minimum) |

### B.1.2 Recommended Hardware Requirements

| Component | Specification |
|-----------|--------------|
| **Processor** | Intel Core i5 or AMD equivalent (2.5 GHz or higher) |
| **RAM** | 8 GB or higher |
| **Storage** | 5 GB available disk space (SSD recommended) |
| **Display** | 1920 x 1080 resolution or higher |
| **Network** | Broadband internet connection (5 Mbps or higher) |

### B.1.3 Server Hardware Requirements (Production)

| Component | Specification |
|-----------|--------------|
| **Processor** | Intel Xeon or AMD EPYC (4 cores minimum) |
| **RAM** | 16 GB or higher |
| **Storage** | 50 GB SSD storage |
| **Network** | 100 Mbps dedicated bandwidth |
| **Backup** | Redundant storage with daily backups |

---

## B.2 Software Requirements

### B.2.1 Operating System

**Supported Operating Systems:**
- **Windows**: Windows 10, Windows 11, Windows Server 2019/2022
- **macOS**: macOS 10.15 (Catalina) or later
- **Linux**: Ubuntu 20.04 LTS or later, CentOS 8+, Debian 10+

### B.2.2 Core Software Dependencies

| Software | Version | Purpose |
|----------|---------|---------|
| **Python** | 3.8 or higher | Primary programming language |
| **pip** | Latest version | Python package manager |
| **Virtual Environment** | venv/virtualenv | Isolated Python environment |
| **Git** | 2.0+ | Version control (optional for deployment) |

### B.2.3 Python Framework and Libraries

#### Core Framework
```
Flask==3.0.0
Flask-SQLAlchemy==3.1.1
Flask-Login==0.6.3
```

#### Database
```
SQLAlchemy==2.0.23
```

#### Security
```
Werkzeug==3.0.1
```

#### Forms and Validation
```
email-validator==2.1.0
```

#### Date and Time
```
python-dateutil==2.8.2
```

#### Utilities
```
python-dotenv==1.0.0
```

#### Development Tools
```
flask-shell-ipython==0.4.1
```

### B.2.4 Web Browser Requirements

**Supported Browsers:**
- Google Chrome 90+
- Mozilla Firefox 88+
- Microsoft Edge 90+
- Safari 14+

**Browser Features Required:**
- JavaScript enabled
- Cookies enabled
- LocalStorage support
- CSS3 support

### B.2.5 Database Software

**Development:**
- SQLite 3.x (bundled with Python)

**Production (Recommended):**
- PostgreSQL 13+ or MySQL 8.0+

---

## B.3 Installation Guide

### B.3.1 Prerequisites Installation

#### Step 1: Install Python

**Windows:**
1. Download Python 3.8+ from https://www.python.org/downloads/
2. Run the installer
3. Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
   ```bash
   python --version
   ```

**macOS:**
```bash
# Using Homebrew
brew install python@3.8
python3 --version
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
python3 --version
```

#### Step 2: Install Git (Optional)

**Windows:**
- Download from https://git-scm.com/download/win
- Run installer with default settings

**macOS:**
```bash
brew install git
```

**Linux:**
```bash
sudo apt install git
```

### B.3.2 DialSmart Application Installation

#### Step 1: Clone or Extract Repository
```bash
cd /path/to/installation/directory
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

**Verification:** Your terminal prompt should show `(venv)` prefix.

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed Flask-3.0.0 Flask-SQLAlchemy-3.1.1 Flask-Login-0.6.3 ...
```

#### Step 4: Initialize Database
```bash
flask init-db
```

**Expected Output:**
```
Database initialized successfully!
```

#### Step 5: Seed Sample Data (Optional)
```bash
flask seed-data
```

**Expected Output:**
```
Sample data seeded successfully!
Created 10 brands, 50 phones, and test users.
```

#### Step 6: Create Admin User
```bash
flask create-admin
```

**Follow the prompts:**
```
Enter admin name: Admin User
Enter admin email: admin@dialsmart.my
Enter admin password: ********
Confirm admin password: ********
Admin user created successfully!
```

#### Step 7: Run Application
```bash
python run.py
```

**Expected Output:**
```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

#### Step 8: Access Application

Open web browser and navigate to:
```
http://localhost:5000
```

---

## B.4 File Structure

### B.4.1 Complete Project Structure

```
DialSmart/
│
├── app/                                    # Main application package
│   ├── __init__.py                        # Application factory
│   │
│   ├── models/                            # Database models
│   │   ├── __init__.py                   # Models package initialization
│   │   ├── user.py                       # User and UserPreference models
│   │   ├── phone.py                      # Phone and PhoneSpecification models
│   │   ├── brand.py                      # Brand model
│   │   └── recommendation.py             # Recommendation, Comparison, ChatHistory
│   │
│   ├── routes/                            # Route blueprints
│   │   ├── __init__.py                   # Routes package initialization
│   │   ├── auth.py                       # Authentication routes (/login, /register)
│   │   ├── user.py                       # User-facing routes (/dashboard, /profile)
│   │   ├── admin.py                      # Admin panel routes (/admin/*)
│   │   ├── phone.py                      # Phone routes (/phones/*, /compare)
│   │   └── api.py                        # API endpoints (/api/*)
│   │
│   ├── modules/                           # Business logic modules
│   │   ├── __init__.py                   # Modules package initialization
│   │   ├── ai_engine.py                  # AI recommendation engine
│   │   ├── chatbot.py                    # Chatbot NLP engine
│   │   └── comparison.py                 # Phone comparison module
│   │
│   ├── templates/                         # Jinja2 HTML templates
│   │   ├── base.html                     # Base template with navigation
│   │   │
│   │   ├── auth/                         # Authentication templates
│   │   │   ├── login.html               # Login page
│   │   │   ├── register.html            # Registration page
│   │   │   └── forgot_password.html     # Password reset page
│   │   │
│   │   ├── user/                         # User interface templates
│   │   │   ├── dashboard.html           # User dashboard
│   │   │   ├── profile.html             # User profile
│   │   │   ├── preferences.html         # User preferences
│   │   │   ├── recommendation.html      # AI recommendation wizard
│   │   │   ├── chatbot.html             # Chatbot interface
│   │   │   └── history.html             # Recommendation history
│   │   │
│   │   ├── phone/                        # Phone-related templates
│   │   │   ├── browse.html              # Browse phones page
│   │   │   ├── details.html             # Phone details page
│   │   │   ├── compare.html             # Phone comparison page
│   │   │   └── search_results.html      # Search results page
│   │   │
│   │   ├── admin/                        # Admin panel templates
│   │   │   ├── dashboard.html           # Admin dashboard
│   │   │   ├── phones.html              # Phone management
│   │   │   ├── brands.html              # Brand management
│   │   │   ├── users.html               # User management
│   │   │   ├── logs.html                # System logs
│   │   │   └── analytics.html           # Analytics dashboard
│   │   │
│   │   ├── contact/                      # Contact and support
│   │   │   ├── contact.html             # Contact form
│   │   │   └── admin_replies.html       # Admin reply interface
│   │   │
│   │   └── index.html                    # Landing page
│   │
│   ├── static/                            # Static files
│   │   ├── css/                          # Stylesheets
│   │   │   ├── main.css                 # Main stylesheet
│   │   │   ├── admin.css                # Admin panel styles
│   │   │   └── chatbot.css              # Chatbot styles
│   │   │
│   │   ├── js/                           # JavaScript files
│   │   │   ├── main.js                  # Main JavaScript
│   │   │   ├── recommendation.js        # Recommendation wizard logic
│   │   │   ├── chatbot.js               # Chatbot interface logic
│   │   │   ├── comparison.js            # Phone comparison logic
│   │   │   └── admin.js                 # Admin panel scripts
│   │   │
│   │   ├── images/                       # Image assets
│   │   │   ├── logo.png                 # DialSmart logo
│   │   │   └── default-phone.png        # Default phone image
│   │   │
│   │   └── uploads/                      # User uploaded files
│   │       └── phones/                   # Phone images
│   │
│   └── utils/                             # Utility functions
│       ├── __init__.py                   # Utils package initialization
│       └── helpers.py                    # Helper functions
│
├── models/                                # AI/ML models (optional)
│   └── recommendation_model.pkl          # Trained recommendation model
│
├── migrations/                            # Database migrations (if using Flask-Migrate)
│
├── tests/                                 # Test files (optional)
│
├── config.py                              # Configuration settings
├── run.py                                 # Application entry point
├── requirements.txt                       # Python dependencies
├── .env                                   # Environment variables (not in git)
├── .gitignore                            # Git ignore file
├── README.md                             # Project documentation
│
├── dialsmart.db                          # SQLite database file (created after init-db)
│
├── Chapter_6_Testing.md                  # Testing documentation
├── Appendix_A_User_Guide.md             # User guide
└── Appendix_B_System_Document.md        # This document
```

### B.4.2 Key File Descriptions

| File/Directory | Purpose |
|----------------|---------|
| `app/__init__.py` | Application factory, creates Flask app instance |
| `config.py` | Configuration classes (Development, Production, Testing) |
| `run.py` | Entry point to start the application |
| `requirements.txt` | Lists all Python package dependencies |
| `dialsmart.db` | SQLite database file (created during initialization) |
| `app/models/` | Database models using SQLAlchemy ORM |
| `app/routes/` | Flask blueprints for routing requests |
| `app/modules/` | Core business logic (AI engine, chatbot) |
| `app/templates/` | HTML templates using Jinja2 |
| `app/static/` | Static assets (CSS, JavaScript, images) |
| `app/static/uploads/` | User-uploaded phone images |

---

## B.5 Database Location and Configuration

### B.5.1 Database Location

#### Development Database
**File Path:**
```
/home/user/DialSmart/dialsmart.db
```

**Relative Path:**
```
DialSmart/dialsmart.db
```

**Database Type:** SQLite 3.x

**Created By:**
- Command: `flask init-db`
- Automatic creation on first run if not exists

#### Database File Size
- **Initial Size:** ~100 KB (empty database)
- **With Sample Data:** ~500 KB - 2 MB
- **Production Estimate:** 50-100 MB (depends on number of phones and users)

### B.5.2 Upload Folder Location

**Phone Images Upload Path:**
```
/home/user/DialSmart/app/static/uploads/
```

**Subdirectories:**
```
app/static/uploads/
├── phones/          # Phone product images
└── temp/            # Temporary uploads
```

**Access URL:**
```
http://localhost:5000/static/uploads/phones/image.jpg
```

### B.5.3 Database Configuration

#### Configuration File: `config.py`

**Base Configuration Settings:**

```python
class Config:
    """Base configuration"""
    # Application settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dialsmart-secret-key-2024'

    # Database settings
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'dialsmart.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    # Upload settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

    # Pagination
    ITEMS_PER_PAGE = 12
    ADMIN_ITEMS_PER_PAGE = 20

    # AI Model settings
    AI_MODEL_PATH = os.path.join(BASE_DIR, 'models', 'recommendation_model.pkl')

    # Malaysian Ringgit price ranges
    PRICE_RANGES = {
        'budget': (0, 1000),
        'mid_range': (1000, 2000),
        'upper_mid': (2000, 3000),
        'premium': (3000, 10000)
    }

    # Feature brands
    FEATURED_BRANDS = [
        'Samsung', 'Apple', 'Huawei', 'XIAOMI', 'Nokia',
        'Lenovo', 'Honor', 'Oppo', 'Realme', 'Vivo'
    ]
```

#### Development Configuration

```python
class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
```

- **Debug Mode:** Enabled
- **Auto-reload:** Enabled on code changes
- **Database:** SQLite (`dialsmart.db`)

#### Production Configuration

```python
class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
```

**Recommended Production Settings:**
- **Database:** PostgreSQL or MySQL
- **Example PostgreSQL URI:**
  ```
  postgresql://username:password@localhost/dialsmart_db
  ```
- **Environment Variable:**
  ```bash
  export DATABASE_URL="postgresql://user:pass@localhost/dialsmart_db"
  ```

#### Testing Configuration

```python
class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
```

- **Database:** In-memory SQLite (temporary, deleted after tests)
- **Purpose:** Unit testing and integration testing

### B.5.4 Environment Variables

**Optional Environment Variables:**

| Variable | Purpose | Example |
|----------|---------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `your-secret-key-here` |
| `DATABASE_URL` | Database connection string | `postgresql://user:pass@host/db` |
| `FLASK_ENV` | Flask environment | `development` or `production` |
| `FLASK_APP` | Flask application entry | `run.py` |

**Creating `.env` File:**

```bash
# .env file
SECRET_KEY=your-super-secret-key-change-this
DATABASE_URL=sqlite:///dialsmart.db
FLASK_ENV=development
FLASK_APP=run.py
```

### B.5.5 Database Schema Tables

**Main Tables:**

| Table Name | Purpose | Estimated Rows |
|------------|---------|----------------|
| `user` | User accounts and authentication | 100-1000 |
| `user_preference` | User preferences for recommendations | 100-1000 |
| `brand` | Smartphone brands | 10-50 |
| `phone` | Smartphone models | 50-500 |
| `phone_specification` | Detailed phone specifications | 50-500 |
| `recommendation` | Recommendation history | 1000-10000 |
| `comparison` | Phone comparison history | 500-5000 |
| `chat_history` | Chatbot conversation logs | 1000-10000 |

**Total Estimated Size:** 50-100 MB for production with 500 phones and 1000 users

### B.5.6 Backup and Maintenance

**Development Backup:**
```bash
# Backup database file
cp dialsmart.db dialsmart_backup_$(date +%Y%m%d).db
```

**Production Backup (PostgreSQL):**
```bash
pg_dump dialsmart_db > backup_$(date +%Y%m%d).sql
```

**Database Maintenance Commands:**
```bash
# Initialize new database
flask init-db

# Clear all data and reinitialize
rm dialsmart.db
flask init-db

# Seed sample data
flask seed-data
```

---

## B.6 Network and Port Configuration

### B.6.1 Default Configuration

| Setting | Value |
|---------|-------|
| **Host** | 127.0.0.1 (localhost) |
| **Port** | 5000 |
| **Protocol** | HTTP |
| **URL** | http://localhost:5000 |

### B.6.2 Production Deployment

**Recommended Production Setup:**
- **Web Server:** Nginx or Apache
- **WSGI Server:** Gunicorn or uWSGI
- **Protocol:** HTTPS with SSL/TLS certificate
- **Port:** 443 (HTTPS), 80 (HTTP redirect)

**Example Gunicorn Command:**
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## B.7 System Performance Specifications

### B.7.1 Response Time Requirements

| Operation | Target Response Time |
|-----------|---------------------|
| **Page Load** | < 2 seconds |
| **AI Recommendation** | < 3 seconds |
| **Chatbot Response** | < 1 second |
| **Phone Search** | < 1 second |
| **Comparison Generation** | < 2 seconds |
| **Database Query** | < 500ms |

### B.7.2 Capacity Specifications

| Metric | Specification |
|--------|--------------|
| **Concurrent Users** | 100 users (development), 1000+ (production) |
| **Database Records** | 500 phones, 1000 users |
| **Upload Size** | 16 MB per file |
| **Session Duration** | 7 days |
| **API Rate Limit** | 100 requests/minute per user |

---

## B.8 Security Configurations

### B.8.1 Password Requirements

- Minimum length: 8 characters
- Hashing algorithm: Werkzeug PBKDF2-SHA256
- Password storage: Hashed, never plain text

### B.8.2 Session Security

- Session timeout: 7 days
- Session storage: Server-side (Flask-Login)
- CSRF protection: Enabled for forms

### B.8.3 Access Control

- Role-based access control (RBAC)
- User roles: Regular User, Admin, Super Admin
- Protected routes: Require authentication
- Admin routes: Require admin role

---

**End of Appendix B**
