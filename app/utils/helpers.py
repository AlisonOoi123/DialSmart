"""
Helper Utilities
Common utility functions used across the application
"""
import os
import json
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
    Priority: Budget (HARD FILTER) > Brand > Features > Specs
    """
    # CRITICAL: Budget is a HARD REQUIREMENT
    # Phones outside budget range get ZERO score immediately
    if phone.price < user_prefs.min_budget or phone.price > user_prefs.max_budget:
        return 0  # Immediately disqualify phones outside budget

    score = 0
    max_score = 0

    # Brand preference (weight: 50 - HIGHEST PRIORITY after budget)
    max_score += 50
    preferred_brands = []

    # Handle both list and JSON string formats
    if hasattr(user_prefs, 'preferred_brands'):
        if isinstance(user_prefs.preferred_brands, list):
            preferred_brands = user_prefs.preferred_brands
        elif isinstance(user_prefs.preferred_brands, str) and user_prefs.preferred_brands:
            try:
                preferred_brands = json.loads(user_prefs.preferred_brands)
            except (json.JSONDecodeError, ValueError):
                preferred_brands = []

    # Convert brand IDs to integers if they're strings
    try:
        preferred_brands = [int(b) for b in preferred_brands if b]
    except (ValueError, TypeError):
        preferred_brands = []

    # If user selected specific brands, heavily prioritize them
    if preferred_brands:
        if phone.brand_id in preferred_brands:
            score += 50  # Full points for matching brand
        else:
            # Brand doesn't match preference - give partial points
            score += 10  # Small points for being within budget but wrong brand
    else:
        score += 50  # No brand preference, give full points to all

    # Budget match (weight: 25) - Already within budget, give bonus for being optimal
    max_score += 25
    budget_midpoint = (user_prefs.min_budget + user_prefs.max_budget) / 2
    budget_range = user_prefs.max_budget - user_prefs.min_budget

    # Give more points for phones near the budget midpoint
    if budget_range > 0:
        distance_from_midpoint = abs(phone.price - budget_midpoint)
        # Phones at midpoint get full 25 points, phones at edges get 15 points
        budget_score = 25 - (distance_from_midpoint / budget_range) * 10
        score += max(15, budget_score)
    else:
        score += 25  # Exact budget match

    if phone_specs:
        # RAM match (weight: 10)
        max_score += 10
        if phone_specs.ram_options:
            import re
            ram_values = [int(r) for r in re.findall(r'\d+', phone_specs.ram_options) if r]
            if ram_values and max(ram_values) >= user_prefs.min_ram:
                score += 10

        # Storage match (weight: 10)
        max_score += 10
        if phone_specs.storage_options:
            import re
            storage_values = [int(s) for s in re.findall(r'\d+', phone_specs.storage_options) if s]
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

    # Brand preference (HIGHEST PRIORITY)
    preferred_brands = []
    if hasattr(user_prefs, 'preferred_brands'):
        if isinstance(user_prefs.preferred_brands, list):
            preferred_brands = user_prefs.preferred_brands
        elif isinstance(user_prefs.preferred_brands, str) and user_prefs.preferred_brands:
            try:
                preferred_brands = json.loads(user_prefs.preferred_brands)
            except (json.JSONDecodeError, ValueError):
                preferred_brands = []

    # Convert to integers
    try:
        preferred_brands = [int(b) for b in preferred_brands if b]
    except (ValueError, TypeError):
        preferred_brands = []

    # Mention brand match if user selected specific brands
    if preferred_brands and phone.brand_id in preferred_brands:
        reasons.append(f"✓ From your preferred brand: {phone.brand.name}")

    # Budget
    if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
        reasons.append(f"Within your budget of {format_price(user_prefs.min_budget)} - {format_price(user_prefs.max_budget)}")

    if phone_specs:
        # Performance
        if phone_specs.ram_options:
            import re
            ram_values = [int(r) for r in re.findall(r'\d+', phone_specs.ram_options) if r]
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
