"""
DialSmart - Fresh Database Import Script
Import brands and phones from fyp_phoneDataset.csv into empty database
"""

import csv
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import create_app, db
from app.models.brand import Brand
from app.models.phone import Phone
from app.models import PhoneSpecification

def import_from_csv():
    """Import brands and phones from CSV file"""

    app = create_app()

    with app.app_context():
        csv_file = 'fyp_phoneDataset.csv'

        if not os.path.exists(csv_file):
            csv_file = 'data/fyp_phoneDataset.csv'

        if not os.path.exists(csv_file):
            print(f"❌ Error: CSV file not found!")
            print(f"   Looking for: fyp_phoneDataset.csv or data/fyp_phoneDataset.csv")
            return False

        print(f"📁 Reading CSV file: {csv_file}")
        print()

        # Read CSV
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        print(f"✓ Found {len(rows)} phones in CSV")
        print()

        # Extract unique brands
        brand_names = set()
        for row in rows:
            brand = row.get('Brand', '').strip()
            if brand:
                brand_names.add(brand)

        print(f"📋 Found {len(brand_names)} unique brands: {', '.join(sorted(brand_names))}")
        print()

        # Step 1: Import Brands
        print("=" * 80)
        print("STEP 1: Importing Brands")
        print("=" * 80)
        print()

        brand_map = {}
        for brand_name in sorted(brand_names):
            # Check if brand exists
            existing_brand = Brand.query.filter_by(name=brand_name).first()

            if existing_brand:
                print(f"   → Brand '{brand_name}' already exists (ID: {existing_brand.id})")
                brand_map[brand_name] = existing_brand
            else:
                # Create new brand
                new_brand = Brand(
                    name=brand_name,
                    description=f"{brand_name} smartphones and mobile devices",
                    is_active=True,
                    is_featured=brand_name in ['Apple', 'Samsung', 'Xiaomi', 'Oppo', 'Vivo']
                )
                db.session.add(new_brand)
                db.session.flush()  # Get the ID
                brand_map[brand_name] = new_brand
                print(f"   ✓ Created brand '{brand_name}' (ID: {new_brand.id})")

        db.session.commit()
        print()
        print(f"✓ {len(brand_map)} brands in database")
        print()

        # Step 2: Import Phones
        print("=" * 80)
        print("STEP 2: Importing Phones and Specifications")
        print("=" * 80)
        print()

        imported_count = 0
        skipped_count = 0
        error_count = 0

        for idx, row in enumerate(rows, 1):
            try:
                brand_name = row.get('Brand', '').strip()
                model_name = row.get('Model', '').strip()

                if not brand_name or not model_name:
                    print(f"   ⚠ Row {idx}: Missing brand or model, skipping")
                    skipped_count += 1
                    continue

                # Get brand
                brand = brand_map.get(brand_name)
                if not brand:
                    print(f"   ⚠ Row {idx}: Brand '{brand_name}' not found, skipping")
                    skipped_count += 1
                    continue

                # Check if phone already exists
                existing_phone = Phone.query.filter_by(
                    brand_id=brand.id,
                    model_name=model_name
                ).first()

                if existing_phone:
                    print(f"   → Row {idx}: {brand_name} {model_name} already exists")
                    skipped_count += 1
                    continue

                # Parse price
                price_str = row.get('Price', '').replace('RM', '').replace(',', '').strip()
                try:
                    price = float(price_str) if price_str else 0.0
                except:
                    price = 0.0

                # Create phone
                phone = Phone(
                    brand_id=brand.id,
                    model_name=model_name,
                    price=price,
                    is_active=True,
                    availability_status='In Stock'
                )
                db.session.add(phone)
                db.session.flush()  # Get phone ID

                # Helper function to convert string to number
                def to_number(value, default=None):
                    if not value or value == '-' or value == 'N/A':
                        return default
                    try:
                        # Remove common suffixes
                        value = str(value).replace('GB', '').replace('MP', '').replace('mAh', '')
                        value = value.replace('GHz', '').replace('Hz', '').replace('"', '')
                        value = value.strip()
                        if not value:
                            return default
                        return float(value)
                    except:
                        return default

                def to_int(value, default=None):
                    result = to_number(value, default)
                    return int(result) if result is not None else default

                def clean_value(value):
                    if value in ['-', 'N/A', '', None]:
                        return None
                    return str(value).strip()

                # Create specifications
                spec = PhoneSpecification(
                    phone_id=phone.id,

                    # Display
                    screen_size=to_number(row.get('Screen Size')),
                    screen_resolution=clean_value(row.get('Resolution')),
                    display_type=clean_value(row.get('Display Type')),
                    refresh_rate=to_int(row.get('Refresh Rate')),

                    # Processor
                    processor=clean_value(row.get('Processor')),
                    chipset=clean_value(row.get('Chipset')),

                    # Memory
                    ram_options=clean_value(row.get('RAM')),
                    storage_options=clean_value(row.get('Storage')),

                    # Camera
                    rear_camera=clean_value(row.get('Rear Camera')),
                    rear_camera_main=to_int(row.get('Rear Camera MP')),
                    front_camera=clean_value(row.get('Front Camera')),
                    front_camera_mp=to_int(row.get('Front Camera MP')),

                    # Battery
                    battery_capacity=to_int(row.get('Battery')),
                    fast_charging=clean_value(row.get('Fast Charging')),

                    # Network
                    has_5g=1 if row.get('5G Support', '').lower() == 'yes' else 0,
                    network_5g=clean_value(row.get('5G Bands')),

                    # Connectivity
                    wifi_standard=clean_value(row.get('Wi-Fi')),
                    bluetooth_version=clean_value(row.get('Bluetooth')),
                    nfc=clean_value(row.get('NFC')),

                    # Software
                    operating_system=clean_value(row.get('OS')),

                    # Build
                    weight=clean_value(row.get('Weight')),
                    dimensions=clean_value(row.get('Dimensions')),

                    # Security
                    fingerprint_sensor=1 if 'fingerprint' in str(row.get('Security', '')).lower() else 0,
                    water_resistance=clean_value(row.get('Water Resistance')),

                    # URL
                    product_url=clean_value(row.get('URL'))
                )
                db.session.add(spec)

                imported_count += 1

                if imported_count % 50 == 0:
                    print(f"   ✓ Imported {imported_count} phones...")
                    db.session.commit()  # Commit in batches

            except Exception as e:
                error_count += 1
                print(f"   ❌ Row {idx}: Error - {str(e)}")
                db.session.rollback()
                continue

        # Final commit
        db.session.commit()

        print()
        print("=" * 80)
        print("IMPORT SUMMARY")
        print("=" * 80)
        print(f"✓ Successfully imported: {imported_count} phones")
        print(f"→ Skipped (duplicates):  {skipped_count} phones")
        print(f"❌ Errors:               {error_count} phones")
        print(f"📋 Total in CSV:         {len(rows)} phones")
        print()

        # Verify counts
        total_brands = Brand.query.count()
        total_phones = Phone.query.count()
        total_specs = PhoneSpecification.query.count()

        print("=" * 80)
        print("DATABASE STATUS")
        print("=" * 80)
        print(f"Brands in database:       {total_brands}")
        print(f"Phones in database:       {total_phones}")
        print(f"Specifications:           {total_specs}")
        print()

        return True

if __name__ == '__main__':
    print()
    print("=" * 80)
    print("  DialSmart - Fresh Database Import")
    print("=" * 80)
    print()
    print("This will import brands and phones from fyp_phoneDataset.csv")
    print()

    success = import_from_csv()

    if success:
        print("✅ Import completed successfully!")
        print()
        print("Next steps:")
        print("1. Train chatbot model: python train_chatbot_model.py")
        print("2. Create admin account: python create_admin.py")
        print("3. Run application: python run.py")
    else:
        print("❌ Import failed!")
        sys.exit(1)
