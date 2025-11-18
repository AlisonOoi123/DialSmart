# Contact Message System Documentation

## Overview

The Contact Message System allows users to send messages through the contact form, and enables administrators to view and reply to these messages via email directly from the admin panel.

## Features

✅ User can submit contact form with name, email, subject, and message
✅ Messages are stored in Oracle database
✅ Admin can view all messages in `/admin/messages`
✅ Filter messages by: All, Unread, Pending Reply, Replied
✅ Admin can reply to messages with email integration
✅ Automatic email notification to user when admin replies
✅ Track message read/unread status
✅ Track reply status
✅ Delete unwanted messages

## Database Setup

### 1. Run the Migration Script

The contact messages table needs to be created in your Oracle database:

```bash
python migrate_contact_messages.py
```

This will create:
- `contact_messages` table
- Indexes for better performance
- Trigger for automatic timestamp updates

### 2. Table Structure

```sql
contact_messages (
    id                  NUMBER (auto-increment)
    name                VARCHAR2(100)
    email               VARCHAR2(120)
    subject             VARCHAR2(200)
    message             CLOB
    is_read             NUMBER(1) default 0
    is_replied          NUMBER(1) default 0
    admin_reply         CLOB
    replied_by_id       NUMBER (FK to users.id)
    replied_at          TIMESTAMP
    created_at          TIMESTAMP
    updated_at          TIMESTAMP
)
```

## User Flow

### Sending a Message

1. User visits `/contact` page
2. Fills in the contact form:
   - Name (required)
   - Email (required)
   - Subject (optional)
   - Message (required)
3. Submits the form
4. Message is saved to database
5. User sees success message

### Contact Form Fields

```html
<form method="POST">
    <input type="text" name="name" required>
    <input type="email" name="email" required>
    <input type="text" name="subject">
    <textarea name="message" required></textarea>
    <button type="submit">Send Message</button>
</form>
```

## Admin Flow

### Viewing Messages

1. Admin logs in and navigates to `/admin/messages`
2. Sees list of all contact messages with:
   - ID, Name, Email, Subject, Date, Status
   - Badges showing: New, Replied/Pending status
   - Filter tabs: All, Unread, Pending, Replied
3. Unread messages are highlighted in blue

### Replying to a Message

1. Click "View/Reply" button on a message
2. Message is automatically marked as read
3. View full message details
4. Type reply in the text area
5. Click "Send Reply via Email"
6. Reply is sent to user's email address
7. Reply is saved in database with timestamp and admin info
8. Message is marked as replied

### Email Template

When admin replies, user receives a professional HTML email containing:
- Admin's reply message
- Original message for reference
- DialSmart branding
- Professional formatting

## Code Structure

### Models

**File:** `app/models/contact.py`

```python
class ContactMessage(db.Model):
    # Fields
    id, name, email, subject, message
    is_read, is_replied
    admin_reply, replied_by_id, replied_at
    created_at, updated_at

    # Methods
    mark_as_read()
    mark_as_replied(admin_user, reply_text)
```

### Routes

**File:** `app/routes/user.py`

- `GET/POST /contact` - Contact form submission

**File:** `app/routes/admin.py`

- `GET /admin/messages` - List all messages (with filters)
- `GET /admin/messages/<id>` - View message details
- `POST /admin/messages/<id>/reply` - Send email reply
- `POST /admin/messages/<id>/delete` - Delete message

### Email Integration

**File:** `app/utils/email.py`

```python
send_admin_reply_email(user_email, user_name, reply_message, original_message)
```

Sends professional HTML email with:
- Admin reply in highlighted box
- Original message for context
- Professional styling
- DialSmart branding

### Templates

**Files:**
- `app/templates/admin/messages.html` - Message list view
- `app/templates/admin/message_details.html` - Individual message with reply form

## Testing the System

### 1. Test User Submission

```bash
# Start the application
python run.py

# Open browser to: http://localhost:5000/contact
# Fill in the form and submit
```

### 2. Test Admin View

```bash
# Login as admin
# Navigate to: http://localhost:5000/admin/messages
# You should see the submitted message
```

### 3. Test Email Reply

**Prerequisites:**
- Email settings configured in `.env`
- SMTP server accessible

```bash
# Click "View/Reply" on a message
# Type a reply message
# Click "Send Reply via Email"
# Check that user receives the email
```

## Email Configuration

Ensure your `.env` file has email settings:

```bash
# Email Server Settings
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-gmail-app-password
MAIL_DEFAULT_SENDER=noreply@dialsmart.my
```

### Gmail App Password

If using Gmail, you need an App Password:

1. Go to Google Account Settings
2. Security → 2-Step Verification
3. App Passwords
4. Generate password for "Mail"
5. Use this password in MAIL_PASSWORD

## Error Handling

### Common Issues

1. **ImportError: send_contact_reply**
   - Fixed! Function alias added to `email.py`

2. **Database connection lost**
   - Run migration script first
   - Check Oracle connection settings

3. **Email not sending**
   - Check SMTP settings in `.env`
   - Verify email credentials
   - Check firewall/network settings

4. **Messages not appearing in admin panel**
   - Verify database migration completed
   - Check if contact form submission succeeded
   - Look for errors in Flask logs

## Database Queries

### Get unread messages count
```sql
SELECT COUNT(*) FROM contact_messages WHERE is_read = 0;
```

### Get pending replies
```sql
SELECT * FROM contact_messages WHERE is_replied = 0 ORDER BY created_at DESC;
```

### Get messages from specific email
```sql
SELECT * FROM contact_messages WHERE email = 'user@example.com';
```

## Security Considerations

✅ Form validation (required fields)
✅ Email validation
✅ Admin authentication required
✅ SQL injection protection (SQLAlchemy ORM)
✅ XSS protection (Jinja2 auto-escaping)
✅ CSRF protection (Flask forms)

## Performance Optimizations

The migration script creates indexes on:
- `email` - Fast lookups by email
- `is_read` - Filter unread messages
- `is_replied` - Filter pending replies
- `created_at` - Sort by date

## Troubleshooting

### Migration Script Issues

If migration fails:

1. Check Oracle connection:
   ```bash
   sqlplus ds_user/dsuser123@localhost:1521/orclpdb
   ```

2. Verify user permissions:
   ```sql
   GRANT CREATE TABLE TO ds_user;
   GRANT CREATE INDEX TO ds_user;
   GRANT CREATE TRIGGER TO ds_user;
   ```

3. Check if table already exists:
   ```sql
   SELECT * FROM user_tables WHERE table_name = 'CONTACT_MESSAGES';
   ```

### Runtime Issues

Check Flask logs:
```bash
python run.py
# Watch console for errors
```

Enable debug mode in `config.py`:
```python
DEBUG = True
```

## Next Steps

After implementing the contact message system:

1. ✅ Run database migration
2. ✅ Configure email settings
3. ✅ Test contact form submission
4. ✅ Test admin message viewing
5. ✅ Test email reply functionality

## API Reference

### ContactMessage Model Methods

```python
# Mark as read
message.mark_as_read()

# Mark as replied
message.mark_as_replied(admin_user, reply_text)
```

### Email Function

```python
from app.utils.email import send_admin_reply_email

success, message = send_admin_reply_email(
    user_email="user@example.com",
    user_name="John Doe",
    reply_message="Thank you for contacting us...",
    original_message="Original message text..."
)
```

Returns:
- `success` (bool): True if email sent successfully
- `message` (str): Success or error message

## Support

For issues or questions:
1. Check this documentation
2. Review error logs
3. Verify database and email configurations
4. Check the code in `app/models/contact.py` and `app/routes/admin.py`
