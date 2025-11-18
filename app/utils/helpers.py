"""
Helper Utilities
Common utility functions used across the application
"""
import os
import json
import re
from werkzeug.utils import secure_filename
from flask import current_app
from datetime import datetime

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_uploaded_file(file, subfolder=''):
    """Save uploaded file and return the filename"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to filename to avoid conflicts
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        name, ext = os.path.splitext(filename)
        filename = f"{name}_{timestamp}{ext}"

        upload_path = current_app.config['UPLOAD_FOLDER']
        if subfolder:
            upload_path = os.path.join(upload_path, subfolder)
            os.makedirs(upload_path, exist_ok=True)

        filepath = os.path.join(upload_path, filename)
        file.save(filepath)
        return filename
    return None

def parse_json_field(field_value, default=None):
    """Safely parse JSON field"""
    if not field_value:
        return default if default is not None else []

    try:
        if isinstance(field_value, str):
            return json.loads(field_value)
        return field_value
    except (json.JSONDecodeError, TypeError):
        return default if default is not None else []

def format_price(price):
    """Format price in Malaysian Ringgit"""
    return f"RM {price:,.2f}"

def format_date(date):
    """Format date for display"""
    if isinstance(date, datetime):
        return date.strftime('%d %b %Y')
    return date

def calculate_match_score(user_prefs, phone, phone_specs):
    """
    Calculate how well a phone matches user preferences
    Returns a score from 0-100
    """
    score = 0
    max_score = 0

    # Budget match (weight: 30)
    max_score += 30
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        score += 30
    elif phone.price < user_prefs.min_budget:
        # Slight penalty for cheaper phones
        score += 20
    else:
        # Penalty for over-budget phones
        over_budget = phone.price - user_prefs.max_budget
        penalty = min(30, (over_budget / user_prefs.max_budget) * 30)
        score += max(0, 30 - penalty)

    if phone_specs:
        # RAM match (weight: 10)
        max_score += 10
        if phone_specs.ram_options:
            ram_values = [int(r.replace('GB', '')) for r in phone_specs.ram_options.split(',') if 'GB' in r]
            if ram_values and max(ram_values) >= user_prefs.min_ram:
                score += 10

        # Storage match (weight: 10)
        max_score += 10
        if phone_specs.storage_options:
            storage_values = [int(s.replace('GB', '')) for s in phone_specs.storage_options.split(',') if 'GB' in s]
            if storage_values and max(storage_values) >= user_prefs.min_storage:
                score += 10

        # Camera match (weight: 15)
        max_score += 15
        if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
            score += 15

        # Battery match (weight: 15)
        max_score += 15
        if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
            score += 15

        # 5G requirement (weight: 10)
        max_score += 10
        if user_prefs.requires_5g:
            if phone_specs.has_5g:
                score += 10
        else:
            score += 10  # No requirement, so full points

        # Screen size match (weight: 10)
        max_score += 10
        if phone_specs.screen_size:
            if user_prefs.min_screen_size <= phone_specs.screen_size <= user_prefs.max_screen_size:
                score += 10

    # Calculate final percentage
    if max_score > 0:
        return round((score / max_score) * 100, 2)
    return 0

def generate_recommendation_reasoning(match_score, user_prefs, phone, phone_specs):
    """Generate human-readable reasoning for recommendation"""
    reasons = []

    # Budget
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        reasons.append(f"Within your budget of {format_price(user_prefs.min_budget)} - {format_price(user_prefs.max_budget)}")

    if phone_specs:
        # Performance
        if phone_specs.ram_options:
            ram_values = [int(r.replace('GB', '')) for r in phone_specs.ram_options.split(',') if 'GB' in r]
            if ram_values:
                max_ram = max(ram_values)
                if max_ram >= user_prefs.min_ram:
                    reasons.append(f"Excellent performance with up to {max_ram}GB RAM")

        # Camera
        if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
            reasons.append(f"Great {phone_specs.rear_camera_main}MP camera for photography")

        # Battery
        if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
            reasons.append(f"Long-lasting {phone_specs.battery_capacity}mAh battery")

        # 5G
        if phone_specs.has_5g:
            reasons.append("Future-ready with 5G connectivity")

    if not reasons:
        reasons.append("Good overall specifications for the price")

    return " • ".join(reasons)

def validate_password(password):
    """
    Validate password strength according to security standards
    Requirements:
    - At least 8 characters long (maximum 12 recommended)
    - Contains at least one uppercase letter
    - Contains at least one lowercase letter
    - Contains at least one digit
    - Contains at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    if not password:
        return False, "Password is required."

    # Check minimum length
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    # Check maximum recommended length
    if len(password) > 128:
        return False, "Password is too long (maximum 128 characters)."

    # Check for uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter."

    # Check for lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter."

    # Check for digit
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number."

    # Check for special character
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)."

    return True, None
