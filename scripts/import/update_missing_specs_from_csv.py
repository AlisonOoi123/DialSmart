#!/usr/bin/env python
"""
Update Missing Phone Specifications from CSV
Fixes the issue where screen_size, ram_options, storage_options,
rear_camera, and battery_capacity are NULL in database for certain brands
"""
import sys
import os
import csv
import re

# Add the app directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models import Phone, PhoneSpecification, Brand

app = create_app()

def parse_battery_capacity(battery_str):
    """Extract battery capacity as integer from string like '4383 mAh'"""
    if not battery_str:
        return None
    match = re.search(r'(\d+)\s*mAh', str(battery_str))
    if match:
        return int(match.group(1))
    return None

def parse_screen_size(screen_str):
    """Extract screen size as float from string like '6.7 inches'"""
    if not screen_str:
        return None
    match = re.search(r'([\d.]+)\s*inch', str(screen_str), re.IGNORECASE)
    if match:
        return float(match.group(1))
    return None

def clean_text(text):
    """Clean text field"""
    if not text or text.strip() == '':
        return None
    return text.strip()

def update_specs_from_csv(csv_path):
    """Read CSV and update missing specifications"""

    with app.app_context():
        updated_count = 0
        skipped_count = 0
        error_count = 0

        with open(csv_path, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)

            for row in reader:
                try:
                    # Check if required fields exist
                    if 'Brand' not in row or 'Model' not in row:
                        print(f"⚠️  Row missing Brand or Model columns, skipping")
                        skipped_count += 1
                        continue

                    brand_name = row['Brand'].strip()
                    model_name = row['Model'].strip()

                    # Skip rows with empty brand or model
                    if not brand_name or not model_name:
                        skipped_count += 1
                        continue

                    # Find the brand
                    brand = Brand.query.filter_by(name=brand_name).first()
                    if not brand:
                        print(f"⚠️  Brand not found: {brand_name}")
                        skipped_count += 1
                        continue

                    # Find the phone
                    phone = Phone.query.filter_by(
                        model_name=model_name,
                        brand_id=brand.id
                    ).first()

                    if not phone:
                        print(f"⚠️  Phone not found: {brand_name} {model_name}")
                        skipped_count += 1
                        continue

                    # Get or create specs
                    specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
                    if not specs:
                        specs = PhoneSpecification(phone_id=phone.id)
                        db.session.add(specs)

                    # Track if anything was updated
                    updated = False

                    # Update screen_size if NULL
                    if not specs.screen_size:
                        screen_size = parse_screen_size(row.get('ScreenSize'))
                        if screen_size:
                            specs.screen_size = screen_size
                            updated = True

                    # Update ram_options if NULL
                    if not specs.ram_options:
                        ram = clean_text(row.get('RAM'))
                        if ram:
                            specs.ram_options = ram
                            updated = True

                    # Update storage_options if NULL
                    if not specs.storage_options:
                        storage = clean_text(row.get('Storage'))
                        if storage:
                            specs.storage_options = storage
                            updated = True

                    # Update rear_camera if NULL
                    if not specs.rear_camera:
                        rear_camera = clean_text(row.get('RearCamera'))
                        if rear_camera:
                            specs.rear_camera = rear_camera
                            updated = True

                    # Update front_camera if NULL
                    if not specs.front_camera:
                        front_camera = clean_text(row.get('FrontCamera'))
                        if front_camera:
                            specs.front_camera = front_camera
                            updated = True

                    # Update battery_capacity if NULL
                    if not specs.battery_capacity:
                        battery = parse_battery_capacity(row.get('BatteryCapacity'))
                        if battery:
                            specs.battery_capacity = battery
                            updated = True

                    # Update other fields if NULL
                    if not specs.screen_resolution:
                        resolution = clean_text(row.get('Resolution'))
                        if resolution:
                            specs.screen_resolution = resolution
                            updated = True

                    if not specs.screen_type:
                        display_type = clean_text(row.get('DisplayType'))
                        if display_type:
                            specs.screen_type = display_type
                            updated = True

                    if not specs.processor:
                        chipset = clean_text(row.get('Chipset'))
                        if chipset:
                            specs.processor = chipset
                            updated = True

                    if updated:
                        print(f"✓ Updated: {brand_name} {model_name}")
                        updated_count += 1
                    else:
                        # print(f"  Skipped (already has data): {brand_name} {model_name}")
                        skipped_count += 1

                except Exception as e:
                    print(f"❌ Error processing {row.get('Brand', 'Unknown')} {row.get('Model', 'Unknown')}: {e}")
                    error_count += 1

            # Commit all changes
            if updated_count > 0:
                db.session.commit()
                print(f"\n✅ Successfully updated {updated_count} phones")
            else:
                print(f"\n⚠️  No phones needed updating")

            print(f"📊 Summary: Updated: {updated_count}, Skipped: {skipped_count}, Errors: {error_count}")

if __name__ == '__main__':
    csv_path = 'data/fyp_phoneDataset.csv'

    if not os.path.exists(csv_path):
        print(f"❌ CSV file not found: {csv_path}")
        print("Please ensure the CSV file is in the data/ directory")
        sys.exit(1)

    print(f"📁 Reading from: {csv_path}")
    print("🔄 Updating missing specifications...")
    print("-" * 60)

    update_specs_from_csv(csv_path)

    print("-" * 60)
    print("✅ Done!")
