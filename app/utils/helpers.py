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

def validate_password(password):
    """
    Validate password strength
    Requirements:
    - 8-12 characters long
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character

    Returns: (is_valid, error_message)
    """
    if not password:
        return False, "Password is required"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if len(password) > 12:
        return False, "Password must not exceed 12 characters"

    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"

    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"

    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)"

    return True, ""

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
    Only considers criteria explicitly set by user (None values are ignored)
    """
    score = 0
    max_score = 0

    # Budget match (weight: 30) - only if user specified budget
    if user_prefs.min_budget is not None or user_prefs.max_budget is not None:
        max_score += 30
        min_budget = user_prefs.min_budget if user_prefs.min_budget is not None else 0
        max_budget = user_prefs.max_budget if user_prefs.max_budget is not None else float('inf')

        if min_budget <= phone.price <= max_budget:
            score += 30
        elif phone.price < min_budget:
            # Slight bonus for cheaper phones (under budget)
            score += 20
        else:
            # Penalty for over-budget phones
            if max_budget != float('inf'):
                over_budget = phone.price - max_budget
                penalty = min(30, (over_budget / max_budget) * 30)
                score += max(0, 30 - penalty)

    if phone_specs:
        # RAM match (weight: 10) - only if user specified RAM requirement
        if user_prefs.min_ram is not None:
            max_score += 10
            if phone_specs.ram_options:
                try:
                    # Extract all numbers from RAM string (handles "8GB / 12GB", "4GB / 6GB (Expandable...)", etc.)
                    ram_values = re.findall(r'(\d+)\s*GB', phone_specs.ram_options, re.IGNORECASE)
                    ram_values = [int(r) for r in ram_values]
                    if ram_values and max(ram_values) >= user_prefs.min_ram:
                        score += 10
                    elif ram_values:
                        # Partial credit for some RAM (better than nothing)
                        score += 5
                except:
                    pass

        # Storage match (weight: 10) - only if user specified storage requirement
        if user_prefs.min_storage is not None:
            max_score += 10
            if phone_specs.storage_options:
                try:
                    # Extract all numbers from storage string (handles "256GB / 512GB / 1TBUFS 4.0", etc.)
                    storage_values = re.findall(r'(\d+)\s*GB', phone_specs.storage_options, re.IGNORECASE)
                    storage_values = [int(s) for s in storage_values]

                    # Also check for TB (terabytes)
                    tb_values = re.findall(r'(\d+)\s*TB', phone_specs.storage_options, re.IGNORECASE)
                    if tb_values:
                        storage_values.extend([int(t) * 1024 for t in tb_values])

                    if storage_values and max(storage_values) >= user_prefs.min_storage:
                        score += 10
                    elif storage_values:
                        # Partial credit for some storage
                        score += 5
                except:
                    pass

        # Camera match (weight: 15) - only if user specified camera requirement
        if user_prefs.min_camera is not None:
            max_score += 15
            if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
                score += 15

        # Battery match (weight: 15) - only if user specified battery requirement
        if user_prefs.min_battery is not None:
            max_score += 15
            if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
                score += 15

        # 5G requirement (weight: 10)
        max_score += 10
        if user_prefs.requires_5g:
            if phone_specs.has_5g:
                score += 10
            # If user requires 5G but phone doesn't have it, give 0 points
        else:
            score += 10  # No 5G requirement, so full points

        # Screen size match (weight: 10) - only if user specified screen size range
        if user_prefs.min_screen_size is not None or user_prefs.max_screen_size is not None:
            max_score += 10
            if phone_specs.screen_size:
                min_screen = user_prefs.min_screen_size if user_prefs.min_screen_size is not None else 0
                max_screen = user_prefs.max_screen_size if user_prefs.max_screen_size is not None else float('inf')
                if min_screen <= phone_specs.screen_size <= max_screen:
                    score += 10

    # Calculate final percentage
    if max_score > 0:
        return round((score / max_score) * 100, 2)
    return 0

def parse_memory_values(memory_string):
    """
    Parse memory values from strings like '8GB', '3 / 4', '6GB / 8GB', '128, 256'
    Returns list of integer values
    """
    if not memory_string:
        return []

    import re
    # Extract all numbers from the string (handles "3 / 4", "8GB", "6GB / 8GB", etc.)
    numbers = re.findall(r'\d+', str(memory_string))

    values = []
    for num in numbers:
        try:
            values.append(int(num))
        except ValueError:
            continue

    return values

def generate_recommendation_reasoning(match_score, user_prefs, phone, phone_specs):
    """Generate human-readable reasoning for recommendation"""
    reasons = []

    # Budget
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        reasons.append(f"Within your budget of {format_price(user_prefs.min_budget)} - {format_price(user_prefs.max_budget)}")

    if phone_specs:
        # Performance
        if phone_specs.ram_options:
            ram_values = parse_memory_values(phone_specs.ram_options)
            if ram_values:
                max_ram = max(ram_values)
                if user_prefs.min_ram and max_ram >= user_prefs.min_ram:
                    reasons.append(f"Excellent performance with up to {max_ram}GB RAM")

        # Camera
        if phone_specs.rear_camera_main and user_prefs.min_camera and phone_specs.rear_camera_main >= user_prefs.min_camera:
            reasons.append(f"Great {phone_specs.rear_camera_main}MP camera for photography")

        # Battery
        if phone_specs.battery_capacity and user_prefs.min_battery and phone_specs.battery_capacity >= user_prefs.min_battery:
            reasons.append(f"Long-lasting {phone_specs.battery_capacity}mAh battery")

        # 5G
        if phone_specs.has_5g:
            reasons.append("Future-ready with 5G connectivity")

    if not reasons:
        reasons.append("Good overall specifications for the price")

    return " • ".join(reasons)
