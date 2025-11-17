"""
Email Utility Module
Handles sending emails for contact form replies and notifications
"""
from flask_mail import Message
from app import mail
from flask import current_app, render_template_string
import logging

logger = logging.getLogger(__name__)


def send_email(to, subject, body, html_body=None):
    """
    Send an email

    Args:
        to: Recipient email address (string or list)
        subject: Email subject
        body: Plain text body
        html_body: HTML body (optional)

    Returns:
        bool: True if sent successfully, False otherwise
    """
    try:
        msg = Message(
            subject=subject,
            sender=current_app.config['MAIL_DEFAULT_SENDER'],
            recipients=[to] if isinstance(to, str) else to
        )

        msg.body = body

        if html_body:
            msg.html = html_body

        mail.send(msg)
        logger.info(f"Email sent successfully to {to}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {to}: {str(e)}")
        return False


def send_contact_reply(user_email, user_name, original_subject, reply_text, admin_name="DialSmart Admin"):
    """
    Send a reply to a contact form message

    Args:
        user_email: User's email address
        user_name: User's name
        original_subject: Subject of original message
        reply_text: Admin's reply text
        admin_name: Name of admin sending reply

    Returns:
        bool: True if sent successfully
    """
    subject = f"Re: {original_subject}" if original_subject else "Reply from DialSmart"

    # Plain text version
    body = f"""
Dear {user_name},

Thank you for contacting DialSmart. Here is our response to your message:

{reply_text}

---

Best regards,
{admin_name}
DialSmart Customer Support

---
This is an automated reply from DialSmart phone recommendation system.
If you have further questions, please reply to this email.
"""

    # HTML version
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #007bff;
                color: white;
                padding: 20px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                background-color: #f8f9fa;
                padding: 30px;
                border: 1px solid #dee2e6;
            }}
            .reply-box {{
                background-color: white;
                padding: 20px;
                margin: 20px 0;
                border-left: 4px solid #007bff;
                border-radius: 4px;
            }}
            .footer {{
                background-color: #e9ecef;
                padding: 15px;
                text-align: center;
                font-size: 12px;
                color: #6c757d;
                border-radius: 0 0 5px 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>📱 DialSmart</h2>
            <p>Phone Recommendation System</p>
        </div>

        <div class="content">
            <p>Dear <strong>{user_name}</strong>,</p>

            <p>Thank you for contacting DialSmart. Here is our response to your message:</p>

            <div class="reply-box">
                {reply_text.replace(chr(10), '<br>')}
            </div>

            <p>If you have any further questions, please don't hesitate to reply to this email.</p>

            <p>Best regards,<br>
            <strong>{admin_name}</strong><br>
            DialSmart Customer Support</p>
        </div>

        <div class="footer">
            <p>This is an automated message from DialSmart.<br>
            © 2025 DialSmart - Your Smart Phone Recommendation System</p>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, body, html_body)


def send_welcome_email(user_email, user_name):
    """
    Send welcome email to new user

    Args:
        user_email: User's email address
        user_name: User's name

    Returns:
        bool: True if sent successfully
    """
    subject = "Welcome to DialSmart!"

    body = f"""
Dear {user_name},

Welcome to DialSmart - Your intelligent phone recommendation system!

We're excited to help you find the perfect smartphone that matches your needs and budget.

What you can do with DialSmart:
• Get personalized phone recommendations
• Compare different phone models
• Browse phones by brand and price range
• Chat with our AI-powered chatbot for instant suggestions
• Save your favorite phones for later

Start exploring now: http://localhost:5000

If you have any questions, feel free to contact us through the contact form.

Best regards,
The DialSmart Team

---
This is an automated welcome message.
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
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #28a745;
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 5px 5px 0 0;
            }}
            .content {{
                background-color: #f8f9fa;
                padding: 30px;
                border: 1px solid #dee2e6;
            }}
            .features {{
                background-color: white;
                padding: 20px;
                margin: 20px 0;
                border-radius: 4px;
            }}
            .features ul {{
                list-style-type: none;
                padding-left: 0;
            }}
            .features li {{
                padding: 8px 0;
                border-bottom: 1px solid #e9ecef;
            }}
            .features li:before {{
                content: "✓ ";
                color: #28a745;
                font-weight: bold;
                margin-right: 10px;
            }}
            .footer {{
                background-color: #e9ecef;
                padding: 15px;
                text-align: center;
                font-size: 12px;
                color: #6c757d;
                border-radius: 0 0 5px 5px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📱 Welcome to DialSmart!</h1>
        </div>

        <div class="content">
            <p>Dear <strong>{user_name}</strong>,</p>

            <p>Welcome to <strong>DialSmart</strong> - Your intelligent phone recommendation system!</p>

            <p>We're excited to help you find the perfect smartphone that matches your needs and budget.</p>

            <div class="features">
                <h3>What you can do with DialSmart:</h3>
                <ul>
                    <li>Get personalized phone recommendations</li>
                    <li>Compare different phone models side-by-side</li>
                    <li>Browse phones by brand and price range</li>
                    <li>Chat with our AI-powered chatbot for instant suggestions</li>
                    <li>Save your favorite phones for later</li>
                </ul>
            </div>

            <p style="text-align: center; margin: 30px 0;">
                <a href="http://localhost:5000" style="background-color: #28a745; color: white; padding: 12px 30px; text-decoration: none; border-radius: 4px; display: inline-block;">
                    Start Exploring Now
                </a>
            </p>

            <p>If you have any questions, feel free to contact us through our contact form.</p>

            <p>Best regards,<br>
            <strong>The DialSmart Team</strong></p>
        </div>

        <div class="footer">
            <p>© 2025 DialSmart - Your Smart Phone Recommendation System<br>
            This is an automated welcome message.</p>
        </div>
    </body>
    </html>
    """

    return send_email(user_email, subject, body, html_body)
