"""
Email Utility Module
Handles sending emails for notifications
"""
from flask import current_app, render_template_string
from flask_mail import Message
from app import mail
import threading


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            current_app.logger.error(f'Failed to send email: {str(e)}')


def send_email(subject, recipients, text_body, html_body=None):
    """
    Send email with both text and HTML versions

    Args:
        subject: Email subject
        recipients: List of recipient email addresses
        text_body: Plain text email body
        html_body: Optional HTML email body
    """
    # Check if mail is configured
    if not current_app.config.get('MAIL_USERNAME'):
        current_app.logger.warning('Email not configured. Email not sent.')
        return False

    try:
        msg = Message(
            subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=recipients if isinstance(recipients, list) else [recipients]
        )
        msg.body = text_body
        if html_body:
            msg.html = html_body

        # Send email asynchronously
        app = current_app._get_current_object()
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
        return True
    except Exception as e:
        current_app.logger.error(f'Error preparing email: {str(e)}')
        return False


def send_user_suspended_email(user):
    """
    Send notification email when user account is suspended

    Args:
        user: User object that was suspended
    """
    subject = 'Your DialSmart Account Has Been Suspended'

    text_body = f"""Dear {user.full_name},

We are writing to inform you that your DialSmart account has been suspended by an administrator.

Account Details:
- Email: {user.email}
- Name: {user.full_name}
- Account Type: {user.user_category or 'Standard'}

While your account is suspended, you will not be able to:
- Access your account
- Use the chatbot recommendation service
- Save phone comparisons
- View your recommendation history

If you believe this suspension was made in error or if you have any questions, please contact our support team.

Best regards,
The DialSmart Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #dc3545;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }}
        .info-box {{
            background-color: #fff;
            border-left: 4px solid #dc3545;
            padding: 15px;
            margin: 20px 0;
        }}
        .restrictions {{
            background-color: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        ul {{
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>⚠️ Account Suspended</h2>
        </div>
        <div class="content">
            <p>Dear <strong>{user.full_name}</strong>,</p>

            <p>We are writing to inform you that your DialSmart account has been suspended by an administrator.</p>

            <div class="info-box">
                <h3>Account Details</h3>
                <ul>
                    <li><strong>Email:</strong> {user.email}</li>
                    <li><strong>Name:</strong> {user.full_name}</li>
                    <li><strong>Account Type:</strong> {user.user_category or 'Standard'}</li>
                </ul>
            </div>

            <div class="restrictions">
                <h3>Account Restrictions</h3>
                <p>While your account is suspended, you will not be able to:</p>
                <ul>
                    <li>Access your account</li>
                    <li>Use the chatbot recommendation service</li>
                    <li>Save phone comparisons</li>
                    <li>View your recommendation history</li>
                </ul>
            </div>

            <p>If you believe this suspension was made in error or if you have any questions, please contact our support team.</p>

            <p>Best regards,<br>
            <strong>The DialSmart Team</strong></p>
        </div>
        <div class="footer">
            <p>This is an automated message from DialSmart. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(subject, user.email, text_body, html_body)


def send_user_activated_email(user):
    """
    Send notification email when user account is activated

    Args:
        user: User object that was activated
    """
    subject = 'Your DialSmart Account Has Been Activated'

    text_body = f"""Dear {user.full_name},

Good news! Your DialSmart account has been activated by an administrator.

Account Details:
- Email: {user.email}
- Name: {user.full_name}
- Account Type: {user.user_category or 'Standard'}

You can now:
- Access your account at http://dialsmart.com
- Use our AI-powered chatbot to get personalized phone recommendations
- Compare phones side-by-side
- Save and view your recommendation history

Thank you for being a part of DialSmart!

Best regards,
The DialSmart Team
"""

    html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        .header {{
            background-color: #28a745;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
        }}
        .content {{
            background-color: #f9f9f9;
            padding: 30px;
            border: 1px solid #ddd;
            border-top: none;
            border-radius: 0 0 5px 5px;
        }}
        .info-box {{
            background-color: #fff;
            border-left: 4px solid #28a745;
            padding: 15px;
            margin: 20px 0;
        }}
        .features {{
            background-color: #d4edda;
            border: 1px solid #28a745;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        ul {{
            margin: 10px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 20px;
            color: #666;
            font-size: 12px;
        }}
        .button {{
            display: inline-block;
            padding: 12px 30px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 20px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>✅ Account Activated!</h2>
        </div>
        <div class="content">
            <p>Dear <strong>{user.full_name}</strong>,</p>

            <p>Good news! Your DialSmart account has been activated by an administrator.</p>

            <div class="info-box">
                <h3>Account Details</h3>
                <ul>
                    <li><strong>Email:</strong> {user.email}</li>
                    <li><strong>Name:</strong> {user.full_name}</li>
                    <li><strong>Account Type:</strong> {user.user_category or 'Standard'}</li>
                </ul>
            </div>

            <div class="features">
                <h3>What You Can Do Now</h3>
                <ul>
                    <li>✨ Use our AI-powered chatbot for personalized phone recommendations</li>
                    <li>📊 Compare phones side-by-side with detailed specifications</li>
                    <li>💾 Save and view your recommendation history</li>
                    <li>🔍 Browse our extensive phone database</li>
                </ul>
            </div>

            <p style="text-align: center;">
                <a href="http://dialsmart.com" class="button">Access Your Account</a>
            </p>

            <p>Thank you for being a part of DialSmart!</p>

            <p>Best regards,<br>
            <strong>The DialSmart Team</strong></p>
        </div>
        <div class="footer">
            <p>This is an automated message from DialSmart. Please do not reply to this email.</p>
        </div>
    </div>
</body>
</html>
"""

    return send_email(subject, user.email, text_body, html_body)
