"""
Dataset Import Script
Import phone data from CSV into the database
"""
import sys
import os
import pandas as pd
import re
from datetime import datetime

# Add the app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

def parse_price(price_str):
    """Parse price string to float"""
    if pd.isna(price_str) or not price_str:
        return None

    # Remove 'MYR' and commas
    price_str = str(price_str).replace('MYR', '').replace(',', '').strip()

    try:
        return float(price_str)
    except (ValueError, AttributeError):
        return None

def parse_date(date_str):
    """Parse date string to date object"""
    if pd.isna(date_str) or not date_str:
        return None

    try:
        return datetime.strptime(str(date_str).strip(), '%Y-%m-%d').date()
    except (ValueError, AttributeError):
        return None

def extract_main_camera_mp(camera_str):
    """Extract main camera MP from camera string"""
    if pd.isna(camera_str) or not camera_str:
        return None

    # Look for first number followed by MP
    match = re.search(r'(\d+)\s*MP', str(camera_str), re.IGNORECASE)
    if match:
        return int(match.group(1))

    return None

def extract_battery_capacity(battery_str):
    """Extract battery capacity in mAh"""
    if pd.isna(battery_str) or not battery_str:
        return None

    # Look for number followed by mAh or just the number
    match = re.search(r'(\d+)\s*mAh', str(battery_str), re.IGNORECASE)
    if match:
        return int(match.group(1))

    # Try just a number
    try:
        return int(str(battery_str).strip())
    except (ValueError, AttributeError):
        return None

def extract_screen_size(screen_str):
    """Extract screen size in inches"""
    if pd.isna(screen_str) or not screen_str:
        return None

    # Look for decimal number followed by inches
    match = re.search(r'(\d+\.?\d*)\s*inch', str(screen_str), re.IGNORECASE)
    if match:
        return float(match.group(1))

    return None

def import_dataset(csv_path):
    """Import phone dataset from CSV"""
    print(f"Reading CSV file: {csv_path}")

    # Read CSV
    try:
        df = pd.read_csv(csv_path)
        print(f"Found {len(df)} rows in CSV")
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Create all brands first
    print("\nCreating brands...")
    brand_map = {}
    unique_brands = df['Brand'].unique()

    for brand_name in unique_brands:
        if pd.isna(brand_name):
            continue

        brand_name = str(brand_name).strip()

        # Check if brand exists
        brand = Brand.query.filter_by(name=brand_name).first()

        if not brand:
            brand = Brand(
                name=brand_name,
                description=f"{brand_name} smartphones",
                is_featured=brand_name in ['Apple', 'Samsung', 'Xiaomi', 'Vivo', 'Oppo', 'Realme', 'Huawei', 'Google']
            )
            db.session.add(brand)
            db.session.flush()
            print(f"  Created brand: {brand_name}")

        brand_map[brand_name] = brand.id

    db.session.commit()
    print(f"Created/verified {len(brand_map)} brands")

    # Import phones
    print("\nImporting phones...")
    imported_count = 0
    skipped_count = 0

    for index, row in df.iterrows():
        try:
            brand_name = str(row['Brand']).strip() if not pd.isna(row['Brand']) else None
            model_name = str(row['Model']).strip() if not pd.isna(row['Model']) else None

            if not brand_name or not model_name:
                skipped_count += 1
                continue

            # Get brand_id
            brand_id = brand_map.get(brand_name)
            if not brand_id:
                skipped_count += 1
                continue

            # Check if phone already exists
            existing_phone = Phone.query.filter_by(
                brand_id=brand_id,
                model_name=model_name
            ).first()

            if existing_phone:
                # Update existing phone
                phone = existing_phone
            else:
                # Create new phone
                phone = Phone(brand_id=brand_id, model_name=model_name)

            # Parse and set phone attributes
            phone.price = parse_price(row.get('Price', 0)) or 500
            phone.main_image = str(row.get('Image URL', '')).strip() if not pd.isna(row.get('Image URL')) else None
            phone.availability_status = str(row.get('Status', 'Available')).strip() if not pd.isna(row.get('Status')) else 'Available'
            phone.release_date = parse_date(row.get('Date'))
            phone.is_active = True

            if not existing_phone:
                db.session.add(phone)

            db.session.flush()

            # Create/update specifications
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            if not specs:
                specs = PhoneSpecification(phone_id=phone.id)
                db.session.add(specs)

            # Parse specifications
            specs.screen_size = extract_screen_size(row.get('Screen Size'))
            specs.screen_type = str(row.get('Display Type', '')).strip()[:50] if not pd.isna(row.get('Display Type')) else None
            specs.screen_resolution = str(row.get('Resolution', '')).strip()[:50] if not pd.isna(row.get('Resolution')) else None

            # Processor
            specs.processor = str(row.get('Chipset', '')).strip()[:100] if not pd.isna(row.get('Chipset')) else None

            # RAM and Storage
            specs.ram_options = str(row.get('RAM', '')).strip()[:50] if not pd.isna(row.get('RAM')) else None
            specs.storage_options = str(row.get('Storage', '')).strip()[:50] if not pd.isna(row.get('Storage')) else None

            # Camera
            specs.rear_camera = str(row.get('Rear Camera', '')).strip()[:100] if not pd.isna(row.get('Rear Camera')) else None
            specs.rear_camera_main = extract_main_camera_mp(row.get('Rear Camera'))
            specs.front_camera = str(row.get('Front Camera', '')).strip()[:50] if not pd.isna(row.get('Front Camera')) else None
            specs.front_camera_mp = extract_main_camera_mp(row.get('Front Camera'))

            # Battery
            specs.battery_capacity = extract_battery_capacity(row.get('Battery Capacity'))
            specs.charging_speed = str(row.get('Fast Charging', '')).strip()[:50] if not pd.isna(row.get('Fast Charging')) else None
            specs.wireless_charging = 'wireless' in str(row.get('Wireless Charging', '')).lower()

            # Connectivity
            specs.has_5g = '5G' in str(row.get('Technology', '')).upper()
            specs.wifi_standard = str(row.get('Wi-Fi', '')).strip()[:50] if not pd.isna(row.get('Wi-Fi')) else None
            specs.bluetooth_version = str(row.get('Bluetooth', '')).strip()[:20] if not pd.isna(row.get('Bluetooth')) else None
            specs.nfc = str(row.get('NFC', '')).lower() == 'yes'

            # OS
            specs.operating_system = str(row.get('OS', '')).strip()[:50] if not pd.isna(row.get('OS')) else None

            # Physical
            weight_str = str(row.get('Weight', ''))
            if not pd.isna(row.get('Weight')) and weight_str:
                weight_match = re.search(r'(\d+)\s*g', weight_str, re.IGNORECASE)
                if weight_match:
                    specs.weight = int(weight_match.group(1))

            specs.dimensions = str(row.get('Dimensions', '')).strip()[:50] if not pd.isna(row.get('Dimensions')) else None
            specs.colors_available = str(row.get('Color', '')).strip()[:200] if not pd.isna(row.get('Color')) else None

            # Protection
            protection = str(row.get('Protection', ''))
            if not pd.isna(row.get('Protection')) and protection:
                if 'IP68' in protection.upper():
                    specs.water_resistance = 'IP68'
                elif 'IP67' in protection.upper():
                    specs.water_resistance = 'IP67'

            imported_count += 1

            if imported_count % 100 == 0:
                print(f"  Imported {imported_count} phones...")
                db.session.commit()

        except Exception as e:
            print(f"  Error importing row {index}: {e}")
            skipped_count += 1
            continue

    # Final commit
    db.session.commit()

    print(f"\nImport completed!")
    print(f"  Successfully imported: {imported_count} phones")
    print(f"  Skipped: {skipped_count} rows")

def main():
    """Main function"""
    app = create_app('development')

    with app.app_context():
        print("=" * 60)
        print("DialSmart Phone Dataset Import")
        print("=" * 60)

        # Create tables if they don't exist
        print("\nCreating database tables...")
        db.create_all()
        print("Database tables ready!")

        # Import dataset
        csv_path = os.path.join(os.path.dirname(__file__), 'fyp_phoneDataset.csv')

        if not os.path.exists(csv_path):
            print(f"\nError: CSV file not found at {csv_path}")
            return

        import_dataset(csv_path)

        print("\n" + "=" * 60)
        print("Import completed successfully!")
        print("=" * 60)

if __name__ == '__main__':
    main()
