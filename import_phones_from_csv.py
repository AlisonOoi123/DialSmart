"""
Import phones from CSV dataset into the database
"""
import csv
import re
from datetime import datetime
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

def clean_price(price_str):
    """Extract numeric price from string like 'MYR 3,899'"""
    if not price_str or price_str.strip() == '':
        return 0.0
    # Remove MYR, currency symbols, commas, and spaces
    price_str = re.sub(r'[MYR,\s]', '', price_str)
    try:
        return float(price_str)
    except:
        return 0.0

def extract_number(text, default=None):
    """Extract first number from text"""
    if not text or text.strip() == '':
        return default
    match = re.search(r'(\d+\.?\d*)', str(text))
    if match:
        try:
            return float(match.group(1)) if '.' in match.group(1) else int(match.group(1))
        except:
            return default
    return default

def extract_screen_size(text):
    """Extract screen size in inches from text like '6.7 inches'"""
    if not text:
        return None
    match = re.search(r'(\d+\.?\d*)\s*inch', str(text))
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None

def parse_date(date_str):
    """Parse date from string"""
    if not date_str or date_str.strip() == '':
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except:
        return None

def extract_main_camera_mp(camera_str):
    """Extract main camera MP from string like '48 MP, f/1.6, ...'"""
    if not camera_str:
        return None
    match = re.search(r'(\d+)\s*MP', str(camera_str))
    if match:
        return int(match.group(1))
    return None

def has_5g(networks_str):
    """Check if phone supports 5G"""
    if not networks_str:
        return False
    return len(str(networks_str).strip()) > 0 and str(networks_str).strip() != ''

def parse_yes_no(text):
    """Convert Yes/No to boolean"""
    if not text:
        return False
    text = str(text).strip().lower()
    return text in ['yes', 'true', '1']

def clean_text(text):
    """Clean text field"""
    if not text or str(text).strip() == '':
        return None
    return str(text).strip()

# Create application instance
app = create_app()

with app.app_context():
    print("Importing phones from CSV dataset...")
    print("=" * 80)

    # Clear existing data (optional - comment out if you want to keep sample data)
    print("Clearing existing phone data...")
    PhoneSpecification.query.delete()
    Phone.query.delete()
    Brand.query.delete()
    db.session.commit()
    print("✓ Existing data cleared\n")

    # Track brands
    brands_cache = {}

    # Read CSV file
    csv_file = '/home/user/DialSmart/fyp_phoneDataset.csv'

    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        total_phones = 0
        skipped_phones = 0

        for row in reader:
            try:
                brand_name = clean_text(row.get('Brand'))
                model_name = clean_text(row.get('Model'))

                if not brand_name or not model_name:
                    print(f"✗ Skipping row with missing brand/model")
                    skipped_phones += 1
                    continue

                # Get or create brand
                if brand_name not in brands_cache:
                    brand = Brand.query.filter_by(name=brand_name).first()
                    if not brand:
                        brand = Brand(
                            name=brand_name,
                            is_featured=brand_name in ['Samsung', 'Apple', 'Xiaomi', 'Huawei', 'Oppo', 'Vivo', 'Realme', 'OnePlus', 'Google'],
                            is_active=True
                        )
                        db.session.add(brand)
                        db.session.flush()
                        print(f"✓ Created brand: {brand_name}")
                    brands_cache[brand_name] = brand

                brand = brands_cache[brand_name]

                # Check if phone already exists
                existing_phone = Phone.query.filter_by(
                    brand_id=brand.id,
                    model_name=model_name
                ).first()

                if existing_phone:
                    print(f"  Skipping duplicate: {brand_name} {model_name}")
                    skipped_phones += 1
                    continue

                # Create phone
                phone = Phone(
                    brand_id=brand.id,
                    model_name=model_name,
                    price=clean_price(row.get('Price', '0')),
                    main_image=clean_text(row.get('Image URL')),
                    availability_status=clean_text(row.get('Status', 'Available')),
                    release_date=parse_date(row.get('Date')),
                    is_active=True
                )

                db.session.add(phone)
                db.session.flush()

                # Create specifications
                screen_size = extract_screen_size(row.get('Screen Size'))
                ram_str = clean_text(row.get('RAM'))
                storage_str = clean_text(row.get('Storage'))
                rear_camera = clean_text(row.get('Rear Camera'))
                front_camera = clean_text(row.get('Front Camera'))
                battery_capacity = extract_number(row.get('Battery Capacity'))

                specs = PhoneSpecification(
                    phone_id=phone.id,
                    # Display
                    screen_size=screen_size,
                    screen_resolution=clean_text(row.get('Resolution')),
                    screen_type=clean_text(row.get('Display Type')),
                    refresh_rate=extract_number(row.get('Display Type')) if 'Hz' in str(row.get('Display Type', '')) else 60,

                    # Performance
                    processor=clean_text(row.get('Chipset')),
                    processor_brand=clean_text(row.get('Chipset', '').split()[0]) if row.get('Chipset') else None,
                    ram_options=ram_str,
                    storage_options=storage_str,
                    expandable_storage=parse_yes_no(row.get('Card Slot')),

                    # Camera
                    rear_camera=rear_camera,
                    rear_camera_main=extract_main_camera_mp(rear_camera),
                    front_camera=front_camera,
                    front_camera_mp=extract_main_camera_mp(front_camera),
                    camera_features=clean_text(row.get('Camera Features')),

                    # Battery
                    battery_capacity=battery_capacity,
                    charging_speed=clean_text(row.get('Fast Charging')),
                    wireless_charging=parse_yes_no(row.get('Wireless Charging')),

                    # Connectivity
                    has_5g=has_5g(row.get('5G Networks')),
                    wifi_standard=clean_text(row.get('Wi-Fi')),
                    bluetooth_version=clean_text(row.get('Bluetooth')),
                    nfc=parse_yes_no(row.get('NFC')),

                    # Additional
                    operating_system=clean_text(row.get('OS')),
                    fingerprint_sensor='fingerprint' in str(row.get('Sensors', '')).lower(),
                    face_unlock='face' in str(row.get('Sensors', '')).lower(),
                    water_resistance=clean_text(row.get('Protection')) if 'IP' in str(row.get('Protection', '')) else None,
                    dual_sim='Dual' in str(row.get('SIM', '')),
                    weight=extract_number(row.get('Weight')),
                    dimensions=clean_text(row.get('Dimensions')),
                    colors_available=clean_text(row.get('Color'))
                )

                db.session.add(specs)

                total_phones += 1

                if total_phones % 50 == 0:
                    db.session.commit()
                    print(f"  Imported {total_phones} phones...")

            except Exception as e:
                print(f"✗ Error importing {brand_name} {model_name}: {str(e)}")
                skipped_phones += 1
                continue

        # Final commit
        db.session.commit()

        print("\n" + "=" * 80)
        print(f"✅ Import completed!")
        print(f"   Total phones imported: {total_phones}")
        print(f"   Total phones skipped: {skipped_phones}")
        print(f"   Total brands created: {len(brands_cache)}")
        print("=" * 80)

        # Show brand summary
        print("\nBrand Summary:")
        for brand_name in sorted(brands_cache.keys()):
            brand = brands_cache[brand_name]
            count = Phone.query.filter_by(brand_id=brand.id).count()
            featured = "⭐" if brand.is_featured else "  "
            print(f"  {featured} {brand_name}: {count} phones")
