# DialSmart - New Features Implementation Guide

## Overview
This document describes the newly implemented features in DialSmart, including admin registration, automated phone data collection, email notifications, and search improvements.

---

## 1. Admin Registration with Validation

### Access
- URL: `/admin/register`
- Requires a special registration code to prevent unauthorized admin creation

### Features
- ✅ Username validation (minimum 3 characters)
- ✅ Email validation
- ✅ Password strength check (minimum 6 characters)
- ✅ Password confirmation
- ✅ Registration code verification
- ✅ Duplicate check for username and email

### Registration Code
- Default code: `DIALSMART_ADMIN_2025`
- **Important**: Change this in production by setting `ADMIN_REGISTRATION_CODE` in your `.env` file

### Usage
1. Navigate to `/admin/register`
2. Fill in the registration form:
   - Username
   - Email
   - Full Name (optional)
   - Password
   - Confirm Password
   - Registration Code
3. Submit the form
4. Upon success, you'll be redirected to the login page

---

## 2. Contact Message Management System

### Admin Interface
- URL: `/admin/messages`

### Features
- ✅ View all contact messages
- ✅ Filter by status (All, Unread, Replied, Unreplied)
- ✅ Mark messages as read
- ✅ Reply to messages via email
- ✅ Add admin notes
- ✅ Delete messages
- ✅ Dashboard integration (shows unread message count)

### Message Workflow
1. **User submits contact form** → Message saved to database
2. **Admin views messages** → Message automatically marked as read
3. **Admin replies** → Email sent to user + message marked as replied
4. **User receives email** → Professional HTML email with reply

### Email Templates
- Professional HTML templates with DialSmart branding
- Plain text fallback for email clients that don't support HTML
- Includes original message context

---

## 3. Email Notification System (Flask-Mail)

### Configuration
Edit `.env` file with your email settings:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=noreply@dialsmart.com
```

### Gmail Setup Instructions
1. Enable 2-Factor Authentication on your Google account
2. Go to https://myaccount.google.com/apppasswords
3. Create an App Password for "Mail"
4. Use the generated 16-character password in `.env`

### Email Functions
Located in `app/utils/email.py`:

- **`send_contact_reply()`** - Send reply to contact form message
- **`send_welcome_email()`** - Send welcome email to new users
- **`send_email()`** - General email sending function

### Testing Email
```python
from app.utils.email import send_email

send_email(
    to='test@example.com',
    subject='Test Email',
    body='This is a test email from DialSmart'
)
```

---

## 4. Automated Phone Data Collection API

### File: `phone_data_updater.py`

### Features
- ✅ Update phone prices from APIs
- ✅ Check for new phone launches
- ✅ Import phone data from CSV files
- ✅ Generate price reports
- ✅ Automatic logging

### Usage

#### Manual Mode
```bash
python phone_data_updater.py
```

Then select:
1. Update all prices
2. Check for new launches
3. Import from CSV
4. Generate price report

#### Automated Mode (Scheduler)
```bash
python scheduler.py
```

The scheduler runs:
- **Price updates**: Every 6 hours
- **New phone check**: Daily at 9:00 AM
- **Price report**: Daily at 6:00 PM

### CSV Import Format
```csv
brand,model_name,price,main_image,ram_options,internal_storage,battery_capacity,rear_camera_main,display_size,display_type,chipset,network_5g
Samsung,Galaxy S24,3999,https://example.com/image.jpg,8GB,256GB,5000mAh,50MP,6.2",AMOLED,Snapdragon 8 Gen 3,Yes
```

### API Integration (To be implemented)
The updater has placeholder methods for integrating with:
- GSMArena API
- PhoneDB API
- Retailer APIs (Amazon, Shopee, Lazada, etc.)

Add your API keys in `.env`:
```env
GSMARENA_API_KEY=your-key
PHONE_API_KEY=your-key
```

---

## 5. Search Results Image Display Fix

### Issue Fixed
Phone images were not displaying properly in search results.

### Solution
Updated `/app/templates/phone/search_results.html` with:
- Better image error handling
- Fallback placeholder images
- Proper image styling (`object-fit: cover`)
- Checks for empty/null image values

### Template Code
```html
{% if phone.main_image and phone.main_image != 'None' and phone.main_image != '' %}
<img src="{{ phone.main_image }}"
     class="card-img-top"
     alt="{{ phone.model_name }}"
     style="height: 200px; object-fit: cover;"
     onerror="this.src='https://via.placeholder.com/300x200/e0e0e0/666666?text={{ phone.model_name | urlencode }}'">
{% else %}
<img src="https://via.placeholder.com/300x200/e0e0e0/666666?text={{ phone.model_name | urlencode }}"
     class="card-img-top"
     alt="{{ phone.model_name }}"
     style="height: 200px; object-fit: cover;">
{% endif %}
```

---

## 6. Database Model: ContactMessage

### Schema
```python
class ContactMessage(db.Model):
    id              # Primary key
    name            # Sender name
    email           # Sender email
    subject         # Message subject
    message         # Message content
    is_read         # Read status (boolean)
    is_replied      # Reply status (boolean)
    admin_notes     # Admin's internal notes
    created_at      # Timestamp
    read_at         # When message was read
    replied_at      # When reply was sent
    user_id         # Foreign key (optional)
```

### Creating Tables
The ContactMessage table will be created automatically when you run the app:

```bash
python run.py
```

Or manually:
```python
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

---

## Setup Instructions

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Create Database Tables
```bash
python run.py
# Tables will be created automatically
```

### 4. Create First Admin (if needed)
Navigate to `/admin/register` and use the registration code.

### 5. Configure Email (Optional)
- For Gmail: Follow Gmail setup instructions above
- For other providers: Update MAIL_* variables in `.env`

### 6. Test Features
- ✅ Register admin account
- ✅ Send test contact message
- ✅ Reply to message (check email)
- ✅ Search for phones (verify images display)
- ✅ Import phone data from CSV

---

## File Structure

```
DialSmart/
├── app/
│   ├── models/
│   │   └── contact.py              # ContactMessage model
│   ├── routes/
│   │   └── admin.py                # Message mgmt + admin registration
│   ├── templates/
│   │   └── admin/
│   │       ├── register.html       # Admin registration form
│   │       ├── messages.html       # Message list view
│   │       └── message_detail.html # Message detail + reply
│   ├── utils/
│   │   └── email.py                # Email sending utilities
│   └── __init__.py                 # Flask-Mail initialization
├── phone_data_updater.py           # Phone data collection
├── scheduler.py                    # Automated task scheduler
├── .env.example                    # Environment config template
├── requirements.txt                # Updated with new dependencies
└── FEATURES_IMPLEMENTATION.md      # This file
```

---

## Troubleshooting

### Email not sending?
1. Check `.env` configuration
2. For Gmail: Ensure App Password is used (not regular password)
3. Check Flask logs for error messages
4. Test email configuration in Python shell:
   ```python
   from app import create_app, mail
   from flask_mail import Message
   app = create_app()
   with app.app_context():
       msg = Message('Test', recipients=['test@example.com'])
       msg.body = 'Test email'
       mail.send(msg)
   ```

### Images not displaying in search?
1. Verify phone records have valid `main_image` URLs
2. Check browser console for image loading errors
3. Ensure images are accessible (not behind authentication)

### Scheduler not working?
1. Check that `schedule` package is installed
2. Verify `phone_data_updater.py` is in project root
3. Run scheduler in foreground to see errors:
   ```bash
   python scheduler.py
   ```

### Admin registration not working?
1. Verify registration code matches `.env` setting
2. Check for existing username/email in database
3. Ensure password meets minimum requirements (6 characters)

---

## Security Notes

🔒 **Production Checklist:**
- [ ] Change `SECRET_KEY` in `.env`
- [ ] Change `ADMIN_REGISTRATION_CODE` to a strong, unique value
- [ ] Use HTTPS for all communications
- [ ] Never commit `.env` file to git
- [ ] Use strong passwords for email accounts
- [ ] Regularly update dependencies
- [ ] Enable database backups
- [ ] Monitor admin activity logs

---

## Future Enhancements

- [ ] Real-time phone price tracking with multiple retailer APIs
- [ ] Email verification for user registration
- [ ] Two-factor authentication for admin accounts
- [ ] Bulk email notifications
- [ ] Advanced message filtering and search
- [ ] Message templates for common replies
- [ ] Integration with GSMArena API
- [ ] Webhook support for new phone launches
- [ ] SMS notifications (optional)

---

## Support

For issues or questions:
1. Check this documentation
2. Review Flask-Mail documentation: https://pythonhosted.org/Flask-Mail/
3. Check application logs
4. Contact system administrator

---

**Last Updated**: 2025-11-17
**Version**: 2.0
