# Email Verification & Admin Features Guide

This document describes the new email verification system and admin features implemented in DialSmart.

---

## 🔧 Fixed Issues

### 1. Missing `local_time` Filter Error

**Error:** `jinja2.exceptions.TemplateAssertionError: No filter named 'local_time'`

**Fix:** Added custom Jinja2 filters to `app/__init__.py`

**Filters Added:**
- `local_time` - Converts UTC datetime to Malaysia time (UTC+8)
- `format_date` - Formats dates with custom format strings

**Usage in Templates:**
```html
<!-- Display datetime in local time -->
{{ message.created_at|local_time('%Y-%m-%d %H:%M') }}

<!-- Display date only -->
{{ user.created_at|format_date('%d %b %Y') }}
```

---

## 📧 Email Verification System

### Overview

Users can now register with real email addresses, and the system will send verification emails automatically.

### Features

✅ **Email Verification on Registration**
- Verification emails sent automatically after registration
- Secure token-based verification
- 24-hour token expiry
- Resend verification option

✅ **Email Sending Capabilities**
- Send verification emails
- Send admin replies via email
- Send password reset emails (ready for implementation)

### Configuration

**Environment Variables (.env file):**

```bash
# Email Server Settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@dialsmart.my

# Enable/Disable Email Verification
EMAIL_VERIFICATION_REQUIRED=false  # Set to true to enable
```

**Important Notes:**

1. **Gmail Users:** Use App Password instead of regular password
   - Go to Google Account → Security → 2-Step Verification → App passwords
   - Generate an app password for "Mail"
   - Use this password in `MAIL_PASSWORD`

2. **Outlook/Hotmail:**
   ```
   MAIL_SERVER=smtp.office365.com
   MAIL_PORT=587
   ```

3. **Other Email Providers:**
   - Check your provider's SMTP settings
   - Update `MAIL_SERVER` and `MAIL_PORT` accordingly

### Database Changes

**New User Model Fields:**

```python
class User(UserMixin, db.Model):
    # ... existing fields ...

    # Email verification
    email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(100), unique=True, nullable=True)
    email_verification_sent_at = db.Column(db.DateTime, nullable=True)
```

**Migration Required:**

After pulling these changes, run:

```bash
# Option 1: Drop and recreate (WARNING: Loses all data)
# Delete dialsmart.db and restart the app

# Option 2: Manual migration (Recommended for production)
# Add columns to existing database
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     # Add the new columns manually or use Alembic migrations
```

### User Flow

#### Registration Flow (Email Verification Enabled)

1. User fills registration form
2. System validates password strength
3. User account created (email_verified=False)
4. Verification email sent to user
5. User receives email with verification link
6. User clicks link → email verified
7. User can now login

#### Registration Flow (Email Verification Disabled - Default)

1. User fills registration form
2. System validates password strength
3. User account created (email_verified=True automatically)
4. User can login immediately

### New Routes

**Email Verification:**
```
GET  /auth/verify-email/<token>     - Verify email with token
GET  /auth/resend-verification      - Show resend form
POST /auth/resend-verification      - Resend verification email
```

### Testing Email Verification

**1. Enable Email Verification:**

Create `.env` file in project root:
```bash
EMAIL_VERIFICATION_REQUIRED=true
MAIL_USERNAME=your-test-email@gmail.com
MAIL_PASSWORD=your-app-password
```

**2. Register New User:**
```bash
# Visit: http://localhost:5000/auth/register
# Fill in details with real email
# Submit form
```

**3. Check Email:**
- Look for verification email
- Click verification link
- Should redirect to login with success message

**4. Test Resend:**
```bash
# Visit: http://localhost:5000/auth/resend-verification
# Enter your email
# Submit - should receive new verification email
```

---

## 👨‍💼 Admin Features

### 1. Admin Registration Workflow

**Current Feature:** Default admin can register new admins via web interface

**How It Works:**

1. **Create First Admin:**
   ```bash
   python create_admin_account.py
   ```
   - Prompts for admin details
   - Validates password strength
   - Creates admin account

2. **Register Additional Admins (via Web):**
   - Visit: `/auth/register-admin`
   - Enter admin passkey: `DialSmart2024Admin!`
   - Fill in admin details
   - Submit to create new admin

3. **New Admin Changes Password:**
   - New admin logs in
   - Goes to profile page
   - Changes password using secure form
   - Password validation enforced

**Security Notes:**
- ⚠️ Change `ADMIN_PASSKEY` in `app/routes/auth.py:143` for production
- ✅ All passwords must meet security requirements
- ✅ Only admins can access admin panel

### 2. User Password Change

**User Profile:**
Users can change their password from their profile page.

**Location:** `/profile` (user dashboard)

**Features:**
- Requires current password verification
- New password must meet security requirements
- Success/error messages displayed

**Already Implemented in:** `app/routes/user.py:64-79`

---

## 📨 Admin Message Reply with Email

### How to Implement in Your Admin Messages Page

The system is ready to send admin replies via email. Here's how to integrate it into your admin panel:

**1. Import Email Function:**

In your `app/routes/admin.py`:

```python
from app.utils.email import send_admin_reply_email
```

**2. Add Reply Route:**

```python
@bp.route('/messages/<int:message_id>/reply', methods=['POST'])
@login_required
@admin_required
def reply_to_message(message_id):
    """Reply to user message via email"""
    message = ContactMessage.query.get_or_404(message_id)

    reply_text = request.form.get('reply')
    if not reply_text:
        flash('Reply message cannot be empty.', 'danger')
        return redirect(url_for('admin.messages'))

    # Send email to user
    success, result = send_admin_reply_email(
        user_email=message.email,
        user_name=message.name,
        reply_message=reply_text,
        original_message=message.message
    )

    if success:
        # Mark message as replied
        message.replied = True
        message.reply_text = reply_text
        message.replied_at = datetime.utcnow()
        db.session.commit()

        flash('Reply sent successfully via email!', 'success')
    else:
        flash(f'Failed to send reply: {result}', 'danger')

    return redirect(url_for('admin.messages'))
```

**3. Update Messages Template:**

In your `app/templates/admin/messages.html`:

```html
<div class="message-card">
    <h5>{{ msg.name }} ({{ msg.email }})</h5>
    <p>{{ msg.message }}</p>
    <small>{{ msg.created_at|local_time('%Y-%m-%d %H:%M') }}</small>

    {% if not msg.replied %}
    <!-- Reply Form -->
    <form method="POST" action="{{ url_for('admin.reply_to_message', message_id=msg.id) }}">
        <div class="form-group">
            <label>Reply:</label>
            <textarea name="reply" class="form-control" rows="3" required></textarea>
        </div>
        <button type="submit" class="btn btn-primary">Send Reply via Email</button>
    </form>
    {% else %}
    <div class="alert alert-success">
        <strong>Replied:</strong> {{ msg.reply_text }}
        <br>
        <small>Sent at: {{ msg.replied_at|local_time('%Y-%m-%d %H:%M') }}</small>
    </div>
    {% endif %}
</div>
```

**4. Update Contact Message Model:**

Add these fields to your ContactMessage model (if not already present):

```python
class ContactMessage(db.Model):
    # ... existing fields ...

    replied = db.Column(db.Boolean, default=False)
    reply_text = db.Column(db.Text)
    replied_at = db.Column(db.DateTime)
    replied_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
```

### Email Templates

The system uses beautiful HTML email templates with:
- Professional styling
- Responsive design
- Company branding (DialSmart header)
- Original message included in replies
- Clear call-to-action buttons

**Available Email Functions:**

```python
# Send verification email
send_verification_email(user)

# Send admin reply to user
send_admin_reply_email(user_email, user_name, reply_message, original_message=None)

# Send password reset (ready to use)
send_password_reset_email(user, reset_url)
```

---

## 🧪 Testing Email Features

### Test Email Sending

**1. Create Test Script: `test_email.py`**

```python
from app import create_app, db
from app.models import User
from app.utils.email import send_verification_email, send_admin_reply_email

app = create_app()

with app.app_context():
    # Test 1: Send verification email
    user = User.query.first()
    if user:
        success, message = send_verification_email(user)
        print(f"Verification Email: {message}")

    # Test 2: Send admin reply
    success, message = send_admin_reply_email(
        user_email="test@example.com",
        user_name="Test User",
        reply_message="Thank you for contacting us!",
        original_message="I have a question..."
    )
    print(f"Admin Reply: {message}")
```

**2. Run Test:**
```bash
python test_email.py
```

**3. Check Email:**
- Check inbox for test emails
- Verify styling and content
- Test verification link clicks

### Common Issues & Solutions

**Issue: Email not sending**
- ✅ Check `.env` file exists with correct settings
- ✅ Verify `MAIL_USERNAME` and `MAIL_PASSWORD` are correct
- ✅ For Gmail, use App Password, not regular password
- ✅ Check firewall/antivirus not blocking SMTP

**Issue: Emails go to spam**
- ✅ Use a proper sender email (not example.com)
- ✅ Set up SPF/DKIM records (production)
- ✅ Use authenticated SMTP server

**Issue: Token expired**
- ✅ Default expiry is 24 hours
- ✅ Change in config: `EMAIL_VERIFICATION_TOKEN_EXPIRY = 24 * 3600`
- ✅ Use resend verification feature

---

## 🔒 Security Best Practices

### Password Security (Already Implemented)

✅ **Enforced Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Email Security

✅ **Implemented:**
- Secure token generation using `secrets.token_urlsafe()`
- Token expiry (24 hours)
- One-time use tokens (cleared after verification)

⚠️ **Production Recommendations:**
- Use environment variables for all credentials
- Never commit `.env` file to git
- Change `ADMIN_PASSKEY` from default
- Use proper email service (SendGrid, AWS SES, etc.)
- Enable HTTPS for all email links

---

## 📊 Summary of Changes

### Files Modified:

1. ✅ `app/__init__.py` - Added Flask-Mail, Jinja2 filters
2. ✅ `app/models/user.py` - Added email verification fields
3. ✅ `app/routes/auth.py` - Added verification routes
4. ✅ `app/utils/email.py` - Email sending functions (NEW)
5. ✅ `config.py` - Email configuration
6. ✅ `requirements.txt` - Added Flask-Mail, pytz

### New Features:

✅ **Fixed:**
- local_time Jinja2 filter error

✅ **Email System:**
- Email verification on registration
- Resend verification emails
- Admin reply via email
- Beautiful HTML email templates

✅ **Admin:**
- Admin registration workflow
- Password change for all users
- Ready for message reply system

✅ **Security:**
- Password strength validation
- Secure token generation
- Token expiry handling

---

## 🚀 Deployment Checklist

### Development Setup:

```bash
# 1. Install new dependencies
pip install -r requirements.txt

# 2. Create .env file
EMAIL_VERIFICATION_REQUIRED=false  # Set true when ready
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# 3. Run database migration (add new columns)
# See "Database Changes" section above

# 4. Create admin account
python create_admin_account.py

# 5. Test email sending
python test_email.py

# 6. Run application
python run.py
```

### Production Setup:

```bash
# 1. Set environment variables
export EMAIL_VERIFICATION_REQUIRED=true
export MAIL_SERVER=smtp.example.com
export MAIL_USERNAME=noreply@dialsmart.my
export MAIL_PASSWORD=secure-password

# 2. Change admin passkey in code
# Edit app/routes/auth.py line 143

# 3. Set up proper email service
# Consider: SendGrid, AWS SES, Mailgun, etc.

# 4. Enable HTTPS
# All email verification links use HTTPS in production

# 5. Monitor email delivery
# Set up logging for failed emails
```

---

## 📞 Usage Examples

### Example 1: User Registration with Verification

```python
# User submits registration form
POST /auth/register
{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "user_category": "Working Professional",
    "age_range": "26-35"
}

# If EMAIL_VERIFICATION_REQUIRED=true:
# → Email sent to john@example.com
# → User clicks link in email
# → GET /auth/verify-email/<token>
# → Email verified, redirect to login

# If EMAIL_VERIFICATION_REQUIRED=false:
# → Account created with email_verified=True
# → Redirect to login immediately
```

### Example 2: Admin Reply to User Message

```python
# Admin views message in admin panel
# Admin types reply and submits

POST /admin/messages/123/reply
{
    "reply": "Thank you for your inquiry. We'll get back to you soon!"
}

# System sends email to user with:
# - Admin's reply message
# - Original user message
# - Professional HTML formatting
# - DialSmart branding

# User receives email in their inbox
```

### Example 3: Resend Verification Email

```python
# User didn't receive email or link expired

GET /auth/resend-verification?email=john@example.com

# User submits form
POST /auth/resend-verification
{
    "email": "john@example.com"
}

# New verification email sent
# New token generated
# 24-hour expiry starts fresh
```

---

## 🎯 Next Steps

### Recommended Enhancements:

1. **Email Templates:**
   - Create more email templates
   - Add company logo to emails
   - Customize styling

2. **Password Reset:**
   - Implement full password reset flow
   - Use `send_password_reset_email()` function
   - Add reset token to User model

3. **Email Notifications:**
   - Order confirmations
   - Recommendation updates
   - Account activity alerts

4. **Admin Panel:**
   - Message management dashboard
   - Email sending statistics
   - Failed email retry system

5. **Production:**
   - Use professional email service
   - Set up email analytics
   - Monitor delivery rates

---

**Modified by:** Claude AI Assistant
**Date:** 2025-11-18
**Version:** 1.0
