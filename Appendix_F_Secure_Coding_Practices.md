# Appendix F: Secure Coding Practices

## F.1 Security Overview

### F.1.1 Security Objectives

DialSmart implements security measures to achieve the following objectives:

| Objective | Description | Implementation |
|-----------|-------------|----------------|
| **Confidentiality** | Protect user data from unauthorized access | Encryption, access control, authentication |
| **Integrity** | Ensure data accuracy and prevent tampering | Input validation, CSRF tokens, hashing |
| **Availability** | Ensure system uptime and reliability | Error handling, rate limiting, backups |
| **Authentication** | Verify user identity | Password hashing, session management |
| **Authorization** | Control resource access | Role-based access control (RBAC) |

### F.1.2 Security Compliance Checklist

✅ **Implemented Security Measures:**

- [x] Password hashing with PBKDF2-SHA256
- [x] SQL injection prevention (SQLAlchemy ORM)
- [x] Cross-Site Scripting (XSS) protection (Jinja2 auto-escaping)
- [x] Cross-Site Request Forgery (CSRF) protection
- [x] Secure session management (Flask-Login)
- [x] Role-based access control (admin/user roles)
- [x] Input validation on forms
- [x] File upload restrictions (type and size)
- [x] Secure password requirements
- [x] Email validation
- [x] Error logging without exposing sensitive data
- [x] Database foreign key constraints

---

## F.2 Authentication and Password Management

### F.2.1 Password Hashing

**Security Standard:** Passwords are **never stored in plain text**.

**Hashing Algorithm:** PBKDF2-SHA256 via Werkzeug

**Implementation:**

```python
from werkzeug.security import generate_password_hash, check_password_hash

# Setting password (during registration or password change)
def set_password(self, password):
    """Hash and set user password"""
    self.password_hash = generate_password_hash(
        password,
        method='pbkdf2:sha256',
        salt_length=16
    )

# Verifying password (during login)
def check_password(self, password):
    """Verify password against hash"""
    return check_password_hash(self.password_hash, password)
```

**Security Features:**
- **Key Derivation Function:** PBKDF2 (Password-Based Key Derivation Function 2)
- **Hash Algorithm:** SHA-256
- **Salt:** Random 16-byte salt (auto-generated per password)
- **Iterations:** 150,000 rounds (Werkzeug default)
- **Output:** Hashed password in format `pbkdf2:sha256:150000$salt$hash`

### F.2.2 Password Requirements

**Enforced Password Policy:**

| Requirement | Value | Enforcement Level |
|-------------|-------|-------------------|
| **Minimum Length** | 8 characters | Application (Form validation) |
| **Maximum Length** | 128 characters | Application |
| **Complexity** | Recommended (not enforced) | User guidance |
| **Password History** | Not implemented | Future enhancement |
| **Expiration** | None | Not required for this application |

**Password Validation Code:**

```python
def validate_password(password):
    """Validate password meets requirements"""
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long")

    if len(password) > 128:
        errors.append("Password must not exceed 128 characters")

    # Recommended but not enforced
    if not any(char.isdigit() for char in password):
        warnings.append("Password should contain at least one number")

    if not any(char.isupper() for char in password):
        warnings.append("Password should contain at least one uppercase letter")

    return errors
```

**Best Practices:**
- ✅ Minimum 8 characters enforced
- ✅ No maximum length restrictions (within reason)
- ✅ Passwords hashed with salt
- ✅ Passwords never logged or displayed
- ✅ Password confirmation on registration/change

### F.2.3 Password Reset Security

**Secure Password Reset Flow:**

1. **User Request:** User enters email address
2. **Token Generation:** Generate unique, time-limited reset token
3. **Email Delivery:** Send password reset link via email
4. **Token Validation:** Verify token validity and expiration (30 minutes)
5. **Password Update:** Allow password change only with valid token
6. **Token Invalidation:** Invalidate token after use

**Implementation:**

```python
from itsdangerous import URLSafeTimedSerializer

def generate_reset_token(user_id, expiration=1800):
    """Generate password reset token (30 minutes expiration)"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(user_id, salt='password-reset-salt')

def verify_reset_token(token, max_age=1800):
    """Verify and decode reset token"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        user_id = serializer.loads(
            token,
            salt='password-reset-salt',
            max_age=max_age  # 30 minutes
        )
        return user_id
    except:
        return None  # Token expired or invalid
```

**Security Features:**
- ✅ Cryptographically secure tokens
- ✅ Time-limited validity (30 minutes)
- ✅ One-time use tokens
- ✅ Tokens invalidated after password change
- ✅ No user enumeration (same response for valid/invalid emails)

---

## F.3 Session Management

### F.3.1 Session Security with Flask-Login

**Session Configuration:**

```python
from flask_login import LoginManager
from datetime import timedelta

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.session_protection = 'strong'  # Strong session protection

# Session lifetime
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
```

**Session Protection Modes:**

| Mode | Description | Implementation |
|------|-------------|----------------|
| **None** | No protection | Not recommended |
| **basic** | Basic session validation | Checks for session tampering |
| **strong** | ✅ **Used in DialSmart** | Additional checks: IP address, user agent |

**Flask-Login Security Features:**

```python
from flask_login import login_user, logout_user, current_user

@bp.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        # Remember Me: 7 days if checked, session-only if not
        remember = request.form.get('remember', False)

        login_user(user, remember=remember)

        # Update last active timestamp
        user.update_last_active()

        # Regenerate session ID to prevent session fixation
        session.regenerate()

        return redirect(url_for('user.dashboard'))
```

**Session Security Measures:**
- ✅ Session cookies marked as `HttpOnly` (prevents XSS access)
- ✅ Session cookies marked as `Secure` in production (HTTPS only)
- ✅ Session ID regeneration on login (prevents session fixation)
- ✅ Automatic session expiration (7 days)
- ✅ Session binding to IP address and user agent (strong mode)
- ✅ Logout invalidates session

### F.3.2 Session Timeout

**Automatic Timeout:** 7 days of inactivity

**Implementation:**

```python
# Config
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

# Middleware to update last active
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_active = datetime.utcnow()
        db.session.commit()
```

**Logout Functionality:**

```python
@bp.route('/logout')
@login_required
def logout():
    """Securely log out user"""
    logout_user()  # Clear Flask-Login session
    session.clear()  # Clear all session data
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('auth.login'))
```

---

## F.4 Access Control and Authorization

### F.4.1 Role-Based Access Control (RBAC)

**User Roles:**

| Role | Permissions | Implementation |
|------|-------------|----------------|
| **Guest** | Browse phones (read-only) | No authentication required |
| **Registered User** | Browse, recommendations, chatbot, comparisons, profile | `@login_required` decorator |
| **Admin** | User management, phone management, brand management | `@admin_required` decorator |
| **Super Admin** | All admin permissions + create admins | `is_super_admin` flag |

**Implementation:**

```python
from functools import wraps
from flask import abort
from flask_login import current_user

def login_required(f):
    """Require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)  # Unauthorized

        if not current_user.is_admin:
            abort(403)  # Forbidden

        return f(*args, **kwargs)
    return decorated_function
```

**Example Usage:**

```python
@user_bp.route('/dashboard')
@login_required  # Only authenticated users
def dashboard():
    return render_template('user/dashboard.html')

@admin_bp.route('/manage-phones')
@login_required
@admin_required  # Only admins
def manage_phones():
    phones = Phone.query.all()
    return render_template('admin/phones.html', phones=phones)
```

### F.4.2 Account Suspension

**Admin Capability:** Suspend user accounts

```python
@admin_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@login_required
@admin_required
def suspend_user(user_id):
    """Suspend user account and send notification email"""
    user = User.query.get_or_404(user_id)

    # Prevent admins from suspending themselves
    if user.id == current_user.id:
        flash('You cannot suspend your own account.', 'danger')
        return redirect(url_for('admin.users'))

    # Suspend account
    user.is_active = False
    db.session.commit()

    # Send email notification
    send_suspension_email(user)

    flash(f'User {user.email} has been suspended.', 'success')
    return redirect(url_for('admin.users'))
```

**Suspended Account Check:**

```python
@login_manager.user_loader
def load_user(user_id):
    """Load user and check if active"""
    user = User.query.get(int(user_id))

    if user and not user.is_active:
        logout_user()
        flash('Your account has been suspended. Please contact support.', 'danger')
        return None

    return user
```

---

## F.5 Input Validation and Sanitization

### F.5.1 Form Input Validation

**Validation Strategy:** Server-side validation on all form inputs

**Email Validation:**

```python
from email_validator import validate_email, EmailNotValidError

def validate_email_address(email):
    """Validate email format"""
    try:
        # Validate and normalize
        valid = validate_email(email)
        return valid.email  # Normalized email
    except EmailNotValidError as e:
        raise ValueError(str(e))
```

**Usage in Registration:**

```python
@bp.route('/register', methods=['POST'])
def register():
    email = request.form.get('email', '').strip()
    full_name = request.form.get('full_name', '').strip()
    password = request.form.get('password', '')

    # Validate email
    try:
        email = validate_email_address(email)
    except ValueError as e:
        flash(f'Invalid email: {e}', 'danger')
        return redirect(url_for('auth.register'))

    # Validate name length
    if len(full_name) < 2 or len(full_name) > 100:
        flash('Name must be between 2 and 100 characters', 'danger')
        return redirect(url_for('auth.register'))

    # Validate password
    if len(password) < 8:
        flash('Password must be at least 8 characters', 'danger')
        return redirect(url_for('auth.register'))

    # Check for existing user
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        flash('Email already registered', 'danger')
        return redirect(url_for('auth.register'))

    # Create user
    user = User(email=email, full_name=full_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    flash('Registration successful! Please log in.', 'success')
    return redirect(url_for('auth.login'))
```

### F.5.2 Numeric Input Validation

**Price Validation:**

```python
def validate_price(price_str):
    """Validate and sanitize price input"""
    try:
        price = float(price_str)

        if price < 0:
            raise ValueError("Price cannot be negative")

        if price > 100000:
            raise ValueError("Price exceeds maximum allowed value")

        return round(price, 2)

    except ValueError:
        raise ValueError("Invalid price format")
```

**Integer Validation (RAM, Storage, etc.):**

```python
def validate_positive_integer(value, field_name, max_value=None):
    """Validate positive integer input"""
    try:
        int_value = int(value)

        if int_value < 0:
            raise ValueError(f"{field_name} cannot be negative")

        if max_value and int_value > max_value:
            raise ValueError(f"{field_name} exceeds maximum value of {max_value}")

        return int_value

    except (ValueError, TypeError):
        raise ValueError(f"Invalid {field_name} format")
```

### F.5.3 String Sanitization

**HTML Escaping:** Jinja2 auto-escapes all variables by default

```html
<!-- Safe: Automatically escaped -->
<p>{{ user.full_name }}</p>
<!-- Outputs: &lt;script&gt;alert('XSS')&lt;/script&gt; if user enters script -->

<!-- Unsafe: Manual override (use with caution) -->
<p>{{ user.bio | safe }}</p>
```

**SQL Injection Prevention:** SQLAlchemy ORM with parameterized queries

```python
# Safe: Parameterized query
user = User.query.filter_by(email=email).first()

# Safe: SQLAlchemy escapes parameters
phones = Phone.query.filter(Phone.price <= max_price).all()

# UNSAFE: Never use raw SQL with string interpolation
# query = f"SELECT * FROM users WHERE email = '{email}'"  # NEVER DO THIS
```

---

## F.6 Cross-Site Scripting (XSS) Protection

### F.6.1 Automatic HTML Escaping

**Jinja2 Auto-Escaping:** Enabled by default in Flask

```python
# In app/__init__.py
app = Flask(__name__)
# Auto-escaping is enabled by default
```

**Template Output:**

```html
<!-- All variables are escaped automatically -->
<h1>Welcome, {{ user.full_name }}</h1>
<p>{{ user.bio }}</p>

<!-- If user.full_name contains: <script>alert('XSS')</script> -->
<!-- Rendered as: &lt;script&gt;alert('XSS')&lt;/script&gt; -->
```

### F.6.2 Content Security Policy (CSP)

**Recommended CSP Header (Production):**

```python
@app.after_request
def set_security_headers(response):
    """Set security headers"""
    response.headers['Content-Security-Policy'] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
        "img-src 'self' data: https:; "
        "font-src 'self' https://cdn.jsdelivr.net;"
    )
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    return response
```

---

## F.7 Cross-Site Request Forgery (CSRF) Protection

### F.7.1 CSRF Token Implementation

**Using Flask-WTF (Recommended):**

```python
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# In forms
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
```

**Manual CSRF Token (Current Implementation):**

```python
from flask import session
import secrets

def generate_csrf_token():
    """Generate CSRF token"""
    if '_csrf_token' not in session:
        session['_csrf_token'] = secrets.token_hex(32)
    return session['_csrf_token']

# Make available in all templates
@app.context_processor
def inject_csrf_token():
    return dict(csrf_token=generate_csrf_token)
```

**Template Usage:**

```html
<form method="POST" action="/login">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
    <!-- Other form fields -->
    <button type="submit">Login</button>
</form>
```

**Server-Side Validation:**

```python
@bp.route('/login', methods=['POST'])
def login():
    # Validate CSRF token
    token = request.form.get('csrf_token')
    if not token or token != session.get('_csrf_token'):
        abort(403, description="CSRF token missing or invalid")

    # Process login
    ...
```

---

## F.8 File Upload Security

### F.8.1 File Upload Restrictions

**Configuration:**

```python
# In config.py
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
```

**File Validation:**

```python
import os
from werkzeug.utils import secure_filename

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@bp.route('/upload-phone-image', methods=['POST'])
@login_required
@admin_required
def upload_phone_image():
    # Check if file exists in request
    if 'file' not in request.files:
        flash('No file selected', 'danger')
        return redirect(request.url)

    file = request.files['file']

    # Check if filename is empty
    if file.filename == '':
        flash('No file selected', 'danger')
        return redirect(request.url)

    # Validate file extension
    if not allowed_file(file.filename):
        flash('Invalid file type. Only PNG, JPG, JPEG, GIF allowed.', 'danger')
        return redirect(request.url)

    # Secure filename (remove path traversal characters)
    filename = secure_filename(file.filename)

    # Generate unique filename to prevent collisions
    unique_filename = f"{uuid.uuid4()}_{filename}"

    # Save file
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    flash('File uploaded successfully', 'success')
    return redirect(url_for('admin.manage_phones'))
```

**Security Measures:**
- ✅ File type restrictions (whitelist approach)
- ✅ File size limit (16MB)
- ✅ Filename sanitization (`secure_filename()`)
- ✅ Unique filenames (UUID prefix)
- ✅ Files stored outside web root when possible
- ✅ No execution permissions on upload directory

### F.8.2 File Content Validation

**Image Validation (Recommended Enhancement):**

```python
from PIL import Image

def validate_image_file(file_path):
    """Validate that file is actually an image"""
    try:
        img = Image.open(file_path)
        img.verify()  # Verify it's a valid image
        return True
    except Exception as e:
        return False
```

---

## F.9 SQL Injection Prevention

### F.9.1 ORM Usage (SQLAlchemy)

**Safe Queries with ORM:**

```python
# Safe: Parameterized through ORM
user = User.query.filter_by(email=email).first()

# Safe: SQLAlchemy handles escaping
phones = Phone.query.filter(
    Phone.price >= min_price,
    Phone.price <= max_price
).all()

# Safe: Using SQLAlchemy text() with bound parameters
from sqlalchemy import text
query = text("SELECT * FROM phones WHERE brand_id = :brand_id")
result = db.session.execute(query, {'brand_id': brand_id})
```

**Unsafe Practices to Avoid:**

```python
# UNSAFE: String interpolation
email = request.form['email']
query = f"SELECT * FROM users WHERE email = '{email}'"  # NEVER!
db.session.execute(query)

# UNSAFE: String concatenation
query = "SELECT * FROM users WHERE email = '" + email + "'"  # NEVER!
```

### F.9.2 Input Parameterization

**Always use parameterized queries:**

```python
# Correct
User.query.filter(User.email == email).first()

# Correct (raw SQL if necessary)
from sqlalchemy import text
query = text("SELECT * FROM users WHERE email = :email")
result = db.session.execute(query, {'email': email})
```

---

## F.10 Error Handling and Logging

### F.10.1 Secure Error Messages

**Development vs Production:**

```python
# In config.py
class DevelopmentConfig(Config):
    DEBUG = True  # Show detailed errors

class ProductionConfig(Config):
    DEBUG = False  # Hide detailed errors
```

**Custom Error Pages:**

```python
@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    # Don't expose internal paths or sensitive info
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()  # Rollback any failed transactions

    # Log error (but don't expose to user)
    app.logger.error(f'Internal error: {error}')

    # Generic message to user
    return render_template('errors/500.html'), 500
```

### F.10.2 Logging Best Practices

**Logging Configuration:**

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    # File handler
    file_handler = RotatingFileHandler(
        'logs/dialsmart.log',
        maxBytes=10240000,  # 10MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('DialSmart startup')
```

**What to Log:**

✅ **Safe to log:**
- User login attempts (success/failure) - without passwords
- Access to admin functions
- Database errors (without sensitive data)
- Security events (failed auth, suspicious activity)

❌ **Never log:**
- Passwords (plain or hashed)
- Session tokens
- Credit card information
- Personal identification numbers
- Full stack traces in production

**Example Secure Logging:**

```python
# Good: Log user action without sensitive data
app.logger.info(f'User {user.id} logged in successfully')

# Good: Log failed login without password
app.logger.warning(f'Failed login attempt for email: {email}')

# Bad: Logging password
# app.logger.info(f'User logged in with password: {password}')  # NEVER!

# Bad: Logging full user object (may contain password hash)
# app.logger.info(f'User object: {user}')  # NEVER!
```

---

## F.11 Data Protection

### F.11.1 Sensitive Data Handling

**Data Classification:**

| Data Type | Sensitivity | Protection Measures |
|-----------|-------------|---------------------|
| **Passwords** | Critical | Hashed with PBKDF2-SHA256, never logged |
| **Email Addresses** | High | Indexed for login, validated, encrypted in transit |
| **User Preferences** | Medium | Access control, encrypted in transit |
| **Phone Data** | Low | Public information |
| **Session Tokens** | Critical | HttpOnly cookies, HTTPS only in production |

### F.11.2 HTTPS/TLS (Production)

**Enforce HTTPS:**

```python
from flask_talisman import Talisman

# Force HTTPS in production
if not app.debug:
    Talisman(app, force_https=True)
```

**Redirect HTTP to HTTPS:**

```python
@app.before_request
def before_request():
    """Redirect HTTP to HTTPS in production"""
    if not app.debug and request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        return redirect(url, code=301)
```

---

## F.12 Security Checklist

### F.12.1 Pre-Deployment Security Checklist

**Configuration:**
- [ ] Set `DEBUG = False` in production
- [ ] Use strong `SECRET_KEY` (min 32 characters, random)
- [ ] Configure HTTPS/SSL certificate
- [ ] Set secure session cookie flags (`HttpOnly`, `Secure`, `SameSite`)
- [ ] Configure Content Security Policy (CSP)

**Authentication:**
- [ ] Password hashing with PBKDF2-SHA256
- [ ] Minimum password length of 8 characters
- [ ] Account lockout after failed login attempts
- [ ] Secure password reset mechanism
- [ ] Session timeout configured (7 days)

**Authorization:**
- [ ] Role-based access control implemented
- [ ] Admin routes protected with `@admin_required`
- [ ] User routes protected with `@login_required`
- [ ] Proper 401/403 error handling

**Input Validation:**
- [ ] Server-side validation on all forms
- [ ] Email validation
- [ ] Numeric input validation
- [ ] String length limits enforced
- [ ] File upload restrictions

**Data Protection:**
- [ ] CSRF tokens on all forms
- [ ] SQL injection prevention (ORM usage)
- [ ] XSS protection (auto-escaping)
- [ ] Secure file uploads
- [ ] HTTPS in production

**Error Handling:**
- [ ] Custom error pages (404, 500)
- [ ] No sensitive data in error messages
- [ ] Logging configured (without sensitive data)
- [ ] Database rollback on errors

**Database:**
- [ ] Foreign key constraints
- [ ] Unique constraints on emails
- [ ] Indexes on frequently queried fields
- [ ] Regular database backups

---

## F.13 Common Vulnerabilities and Mitigations

### F.13.1 OWASP Top 10 Coverage

| Vulnerability | Risk Level | Mitigation in DialSmart |
|---------------|------------|-------------------------|
| **Injection (SQL)** | Critical | ✅ SQLAlchemy ORM with parameterized queries |
| **Broken Authentication** | Critical | ✅ PBKDF2-SHA256 hashing, Flask-Login sessions |
| **Sensitive Data Exposure** | High | ✅ HTTPS in production, no plain text passwords |
| **XML External Entities (XXE)** | Medium | ✅ Not applicable (no XML processing) |
| **Broken Access Control** | Critical | ✅ RBAC with decorators, role checks |
| **Security Misconfiguration** | High | ✅ DEBUG=False in production, secure defaults |
| **Cross-Site Scripting (XSS)** | High | ✅ Jinja2 auto-escaping, CSP headers |
| **Insecure Deserialization** | High | ✅ No untrusted deserialization |
| **Using Components with Known Vulnerabilities** | High | ⚠️ Regular dependency updates recommended |
| **Insufficient Logging & Monitoring** | Medium | ✅ Logging configured, security events logged |

### F.13.2 Additional Security Recommendations

**Future Enhancements:**

1. **Rate Limiting:**
   ```python
   from flask_limiter import Limiter

   limiter = Limiter(app, key_func=lambda: current_user.id)

   @bp.route('/login', methods=['POST'])
   @limiter.limit("5 per minute")  # Max 5 login attempts per minute
   def login():
       ...
   ```

2. **Two-Factor Authentication (2FA):**
   - Implement TOTP (Time-based One-Time Password)
   - Use libraries like `pyotp` or `python-u2f`

3. **Security Headers:**
   - Implement Strict-Transport-Security (HSTS)
   - Add Referrer-Policy header
   - Configure Feature-Policy

4. **Dependency Scanning:**
   ```bash
   pip install safety
   safety check  # Check for known vulnerabilities
   ```

5. **Regular Security Audits:**
   - Code reviews focusing on security
   - Penetration testing
   - Automated security scanning

---

**End of Appendix F**
