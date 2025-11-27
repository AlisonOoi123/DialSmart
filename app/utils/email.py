"""
Email Utilities
Functions for sending emails and managing email verification
"""
from flask import current_app, url_for, render_template_string
from flask_mail import Message
from app import mail
import threading
import secrets
from datetime import datetime, timedelta



def generate_verification_token():
    """Generate a secure random token for email verification"""
    return secrets.token_urlsafe(32)


def send_verification_email(user):
    """Send email verification link to user"""
    try:
        # Generate verification token
        token = generate_verification_token()
        user.email_verification_token = token
        user.email_verification_sent_at = datetime.utcnow()

        # Generate verification URL
        verification_url = url_for('auth.verify_email', token=token, _external=True)

        # Email content
        subject = "DialSmart - Verify Your Email Address"
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #28a745; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>DialSmart</h1>
                </div>
                <div class="content">
                    <h2>Welcome to DialSmart!</h2>
                    <p>Hello {user.full_name},</p>
                    <p>Thank you for registering with DialSmart. To complete your registration, please verify your email address by clicking the button below:</p>
                    <div style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </div>
                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #007bff;">{verification_url}</p>
                    <p>This verification link will expire in 24 hours.</p>
                    <p>If you didn't create an account with DialSmart, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 DialSmart. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create message
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email],
            html=html_body
        )

        # Send email
        mail.send(msg)
        return True, "Verification email sent successfully"

    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Failed to send verification email: {error_msg}")

        # Provide helpful error messages
        if "530" in error_msg or "Authentication Required" in error_msg:
            return False, f"Failed to send email: Gmail authentication failed. You need to use a Gmail App Password (not your regular password). Visit https://myaccount.google.com/apppasswords to generate one, then update MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        elif "MAIL_USERNAME" in error_msg or "MAIL_PASSWORD" in error_msg:
            return False, f"Failed to send email: Email not configured. Please set MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        else:
            return False, f"Failed to send verification email: {error_msg}"


def send_admin_reply_email(user_email, user_name, reply_message, original_message=None):
    """Send admin reply to user via email"""
    try:
        subject = "DialSmart - Response to Your Message"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background-color: #f9f9f9; }}
                .message-box {{ background-color: white; padding: 15px; border-left: 4px solid #007bff; margin: 15px 0; }}
                .original-message {{ background-color: #f0f0f0; padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>DialSmart</h1>
                </div>
                <div class="content">
                    <h2>Response to Your Message</h2>
                    <p>Hello {user_name},</p>
                    <p>We have received your message and here is our response:</p>

                    <div class="message-box">
                        <h3>Admin Reply:</h3>
                        <p>{reply_message}</p>
                    </div>
        """

        if original_message:
            html_body += f"""
                    <div class="original-message">
                        <h4>Your Original Message:</h4>
                        <p>{original_message}</p>
                    </div>
            """

        html_body += """
                    <p>If you have any further questions, please feel free to contact us again.</p>
                    <p>Thank you for using DialSmart!</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 DialSmart. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create message
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user_email],
            html=html_body
        )

        # Send email
        mail.send(msg)
        return True, "Reply sent successfully via email"

    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Failed to send admin reply email: {error_msg}")

        # Provide helpful error messages
        if "530" in error_msg or "Authentication Required" in error_msg:
            return False, f"Failed to send email: Gmail authentication failed. You need to use a Gmail App Password (not your regular password). Visit https://myaccount.google.com/apppasswords to generate one, then update MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        elif "MAIL_USERNAME" in error_msg or "MAIL_PASSWORD" in error_msg:
            return False, f"Failed to send email: Email not configured. Please set MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        else:
            return False, f"Failed to send email: {error_msg}"


# Alias for backward compatibility
def send_contact_reply(user_email, user_name, reply_message, original_message=None):
    """
    Alias for send_admin_reply_email for backward compatibility
    Send admin reply to user contact message via email
    """
    return send_admin_reply_email(user_email, user_name, reply_message, original_message)


def send_password_reset_email(user):
    """Send password reset email to user with token generation"""
    try:
        from datetime import datetime

        # Generate reset token
        token = generate_verification_token()
        user.password_reset_token = token
        user.password_reset_sent_at = datetime.utcnow()

        # Generate reset URL
        reset_url = url_for('auth.reset_password', token=token, _external=True)

        subject = "DialSmart - Password Reset Request"

        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #007bff; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 30px; background-color: #f9f9f9; }}
                .button {{ display: inline-block; padding: 12px 30px; background-color: #dc3545; color: white; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                .footer {{ padding: 20px; text-align: center; font-size: 12px; color: #666; }}
                .warning {{ background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 15px; margin: 15px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>DialSmart</h1>
                </div>
                <div class="content">
                    <h2>Password Reset Request</h2>
                    <p>Hello {user.full_name},</p>
                    <p>We received a request to reset your password. Click the button below to reset it:</p>

                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </div>

                    <p>Or copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #007bff;">{reset_url}</p>

                    <div class="warning">
                        <strong>Security Notice:</strong>
                        <p>This link will expire in 1 hour. If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                    </div>
                </div>
                <div class="footer">
                    <p>&copy; 2024 DialSmart. All rights reserved.</p>
                    <p>This is an automated email. Please do not reply to this message.</p>
                </div>
            </div>
        </body>
        </html>
        """

        # Create message
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[user.email],
            html=html_body
        )

        # Send email
        mail.send(msg)
        return True, "Password reset email sent successfully"

    except Exception as e:
        error_msg = str(e)
        current_app.logger.error(f"Failed to send password reset email: {error_msg}")

        # Provide helpful error messages
        if "530" in error_msg or "Authentication Required" in error_msg:
            return False, f"Failed to send email: Gmail authentication failed. You need to use a Gmail App Password (not your regular password). Visit https://myaccount.google.com/apppasswords to generate one, then update MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        elif "MAIL_USERNAME" in error_msg or "MAIL_PASSWORD" in error_msg:
            return False, f"Failed to send email: Email not configured. Please set MAIL_USERNAME and MAIL_PASSWORD in your .env file."
        else:
            return False, f"Failed to send password reset email: {error_msg}"


def is_token_expired(sent_at, expiry_seconds):
    """Check if a token has expired"""
    if not sent_at:
        return True

    expiry_time = sent_at + timedelta(seconds=expiry_seconds)
    return datetime.utcnow() > expiry_time

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
