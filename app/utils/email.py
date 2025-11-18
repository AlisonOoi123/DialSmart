"""
Email Utilities
Functions for sending emails and managing email verification
"""
from flask import current_app, url_for, render_template_string
from flask_mail import Message
from app import mail
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
        current_app.logger.error(f"Failed to send verification email: {str(e)}")
        return False, f"Failed to send verification email: {str(e)}"


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
        current_app.logger.error(f"Failed to send admin reply email: {str(e)}")
        return False, f"Failed to send email: {str(e)}"


def send_password_reset_email(user, reset_url):
    """Send password reset email to user"""
    try:
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
        current_app.logger.error(f"Failed to send password reset email: {str(e)}")
        return False, f"Failed to send email: {str(e)}"


def is_token_expired(sent_at, expiry_seconds):
    """Check if a token has expired"""
    if not sent_at:
        return True

    expiry_time = sent_at + timedelta(seconds=expiry_seconds)
    return datetime.utcnow() > expiry_time

send_contact_reply = send_admin_reply_email
