"""
Import Phone Dataset from CSV to Oracle Database
Reads fyp_phoneDataset.csv and imports phones with all specifications
"""
import os
import sys
import csv
import re
from datetime import datetime

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

print("\n" + "="*70)
print("DialSmart: Import CSV Dataset to Oracle")
print("="*70)

def parse_price(price_str):
    """Parse price string to float: 'MYR  2,687' -> 2687.0"""
    if not price_str or price_str.strip() == '':
        return 0.0
    # Remove 'MYR', spaces, and commas
    price_cleaned = re.sub(r'[MYR\s,]', '', price_str)
    try:
        return float(price_cleaned)
    except:
        return 0.0

def parse_screen_size(screen_str):
    """Parse screen size: '6.7 inches' -> 6.7"""
    if not screen_str:
        return None
    match = re.search(r'(\d+\.?\d*)', screen_str)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None

def parse_ppi(ppi_str):
    """Parse PPI: '385 ppi density' -> 385"""
    if not ppi_str:
        return None
    match = re.search(r'(\d+)', ppi_str)
    if match:
        try:
            return int(match.group(1))
        except:
            return None
    return None

def parse_battery(battery_str):
    """Parse battery: '4500 mAh' -> 4500"""
    if not battery_str:
        return None
    match = re.search(r'(\d+)', battery_str)
    if match:
        try:
            return int(match.group(1))
        except:
            return None
    return None

def parse_camera_mp(camera_str):
    """Parse main camera MP: '50 MP, f/1.8...' -> 50"""
    if not camera_str:
        return None
    match = re.search(r'(\d+)\s*MP', camera_str)
    if match:
        try:
            return int(match.group(1))
        except:
            return None
    return None

def parse_release_date(date_str):
    """Parse release date: '2023-09-22' or 'Released 2025, October' -> date object"""
    if not date_str:
        return None

    # Try ISO format first (YYYY-MM-DD)
    if re.match(r'\d{4}-\d{2}-\d{2}', date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            pass

    # Extract year
    year_match = re.search(r'(\d{4})', date_str)
    if not year_match:
        return None

    year = int(year_match.group(1))

    # Extract month
    months = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4,
        'may': 5, 'june': 6, 'july': 7, 'august': 8,
        'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    month = 1  # Default to January
    for month_name, month_num in months.items():
        if month_name in date_str.lower():
            month = month_num
            break

    try:
        return datetime(year, month, 1).date()
    except:
        return None

def parse_ram_storage(ram_storage_str):
    """Parse combined RAM/Storage: '8GB' or '6GB / 8GB' or '128GB / 256GB / 512GB'
    Returns tuple: (ram_options, storage_options)"""
    if not ram_storage_str or not ram_storage_str.strip():
        return (None, None)

    # Clean the string
    ram_storage_str = ram_storage_str.strip()

    # Look for GB values
    gb_values = re.findall(r'(\d+)\s*GB', ram_storage_str)

    if not gb_values:
        return (None, None)

    # Convert to integers
    values = [int(v) for v in gb_values]

    # RAM is typically 2-16GB, Storage is typically 32GB+
    ram_values = [v for v in values if v <= 32]  # Assume RAM <= 32GB
    storage_values = [v for v in values if v >= 32]  # Assume Storage >= 32GB

    # If all values are in the RAM range but look like storage (e.g., 128, 256)
    if not storage_values and ram_values and min(ram_values) >= 64:
        storage_values = ram_values
        ram_values = []

    # Format the options
    ram_options = ' / '.join([f'{v}GB' for v in ram_values]) if ram_values else None
    storage_options = ' / '.join([f'{v}GB' for v in storage_values]) if storage_values else None

    return (ram_options, storage_options)

def extract_processor_brand(chipset):
    """Extract processor brand from chipset"""
    if not chipset:
        return None
    chipset_lower = chipset.lower()
    if 'qualcomm' in chipset_lower or 'snapdragon' in chipset_lower:
        return 'Qualcomm'
    elif 'mediatek' in chipset_lower or 'helio' in chipset_lower or 'dimensity' in chipset_lower:
        return 'MediaTek'
    elif 'exynos' in chipset_lower:
        return 'Samsung'
    elif 'apple' in chipset_lower or 'bionic' in chipset_lower:
        return 'Apple'
    elif 'kirin' in chipset_lower:
        return 'Huawei'
    elif 'unisoc' in chipset_lower:
        return 'Unisoc'
    return None

def check_5g(network_5g, technology):
    """Check if phone supports 5G"""
    if network_5g and network_5g.strip():
        return True
    if technology and '5G' in technology:
        return True
    return False

app = create_app()

with app.app_context():
    try:
        # Path to CSV file
        csv_file = 'fyp_phoneDataset.csv'

        if not os.path.exists(csv_file):
            print(f"\n✗ Error: CSV file '{csv_file}' not found!")
            print(f"  Please ensure the file is in the project root directory.")
            print(f"  Current directory: {os.getcwd()}")
            sys.exit(1)

        print(f"\n[1/3] Reading CSV file: {csv_file}")

        # Read CSV (utf-8-sig strips BOM character automatically)
        phones_data = []
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                phones_data.append(row)

        print(f"  ✓ Found {len(phones_data)} phones in CSV")

        print(f"\n[2/3] Processing brands and phones...")

        phones_created = 0
        phones_skipped = 0
        brands_created = 0

        for idx, row in enumerate(phones_data, 1):
            brand_name = row.get('Brand', '').strip()
            model_name = row.get('Model', '').strip()

            if not brand_name or not model_name:
                print(f"  ⚠ Skipping row {idx}: Missing brand or model name")
                phones_skipped += 1
                continue

            # Get or create brand
            brand = Brand.query.filter_by(name=brand_name).first()
            if not brand:
                brand = Brand(
                    name=brand_name,
                    is_active=True,
                    is_featured=brand_name in ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo']
                )
                db.session.add(brand)
                db.session.flush()  # Get brand ID
                brands_created += 1

            # Check if phone already exists
            existing_phone = Phone.query.filter_by(
                brand_id=brand.id,
                model_name=model_name
            ).first()

            if existing_phone:
                phones_skipped += 1
                continue

            # Parse price
            price = parse_price(row.get('Price', '0'))

            # Parse RAM and Storage from combined field
            ram_options, storage_options = parse_ram_storage(row.get('RAMStorage', ''))

            # Create phone
            phone = Phone(
                brand_id=brand.id,
                model_name=model_name,
                price=price,
                main_image=row.get('ImageURL', '').strip() or None,
                availability_status=row.get('Status', 'Available').strip(),
                release_date=parse_release_date(row.get('Date', '')),
                is_active=True
            )
            db.session.add(phone)
            db.session.flush()  # Get phone ID

            # Create specifications
            spec = PhoneSpecification(
                phone_id=phone.id,
                # Display
                screen_size=parse_screen_size(row.get('ScreenSize', '')),
                screen_resolution=row.get('Resolution', '').strip() or None,
                screen_type=row.get('DisplayType', '').strip() or None,
                display_type=row.get('DisplayType', '').strip() or None,
                ppi=parse_ppi(row.get('PPI', '')),
                multitouch=row.get('Multi-touch', '').strip() or None,
                protection=row.get('Protection', '').strip() or None,

                # Performance
                processor=row.get('Chipset', '').strip() or None,
                chipset=row.get('Chipset', '').strip() or None,
                cpu=row.get('CPU', '').strip() or None,
                gpu=row.get('GPU', '').strip() or None,
                processor_brand=extract_processor_brand(row.get('Chipset', '')),
                ram_options=ram_options,
                storage_options=storage_options,
                card_slot=row.get('CardSlot', '').strip() or None,
                expandable_storage='microSD' in row.get('CardSlot', '') if row.get('CardSlot') else False,

                # Camera
                rear_camera=row.get('RearCamera', '').strip() or None,
                rear_camera_main=parse_camera_mp(row.get('RearCamera', '')),
                front_camera=row.get('FrontCamera', '').strip() or None,
                front_camera_mp=parse_camera_mp(row.get('FrontCamera', '')),
                camera_features=row.get('CameraFeatures', '').strip() or None,
                flash=row.get('Flash', '').strip() or None,
                video_recording=row.get('VideoRecording', '').strip() or None,

                # Battery
                battery_capacity=parse_battery(row.get('BatteryCapacity', '')),
                battery=row.get('Battery', '').strip() or None,
                charging_speed=row.get('FastCharging', '').strip() or None,
                fast_charging=row.get('FastCharging', '').strip() or None,
                wireless_charging=row.get('WirelessCharging', '').strip() or None,
                removable_battery=row.get('RemovableBattery', '').strip() or None,

                # Network
                sim=row.get('SIM', '').strip() or None,
                technology=row.get('Technology', '').strip() or None,
                network_5g=row.get('5GNetworks', '').strip() or None,
                network_4g=row.get('4GNetworks', '').strip() or None,
                network_3g=row.get('3GNetworks', '').strip() or None,
                network_2g=row.get('2GNetworks', '').strip() or None,
                network_speed=row.get('NetworkSpeed', '').strip() or None,
                has_5g=check_5g(row.get('5GNetworks', ''), row.get('Technology', '')),
                wifi_standard=row.get('Wi-Fi', '').strip() or None,
                bluetooth_version=row.get('Bluetooth', '').strip() or None,
                gps=row.get('GPS', '').strip() or None,
                nfc=row.get('NFC', '').strip() or None,
                usb=row.get('USB', '').strip() or None,
                audio_jack=None,  # Not in new CSV format
                radio=row.get('Radio', '').strip() or None,

                # OS
                operating_system=row.get('OS', '').strip() or None,

                # Physical
                weight=row.get('Weight', '').strip() or None,
                dimensions=row.get('Dimensions', '').strip() or None,
                colors_available=row.get('Color', '').strip() or None,
                body_material=row.get('BodyMaterial', '').strip() or None,

                # Features
                sensors=row.get('Sensors', '').strip() or None,

                # Reference
                product_url=row.get('URL', '').strip() or None
            )
            db.session.add(spec)

            phones_created += 1

            # Commit every 10 phones
            if phones_created % 10 == 0:
                db.session.commit()
                print(f"  • Imported {phones_created} phones...")

        # Final commit
        db.session.commit()

        print(f"\n[3/3] Import Summary:")
        print(f"  ✓ Brands created: {brands_created}")
        print(f"  ✓ Phones imported: {phones_created}")
        if phones_skipped > 0:
            print(f"  ⚠ Phones skipped (already exist): {phones_skipped}")

        print("\n" + "="*70)
        print("✓ CSV IMPORT COMPLETE!")
        print("="*70)

        # Show database summary
        total_brands = Brand.query.count()
        total_phones = Phone.query.count()

        print(f"\nDatabase Summary:")
        print(f"  • Total Brands: {total_brands}")
        print(f"  • Total Phones: {total_phones}")

        print(f"\nNext Steps:")
        print(f"  1. Run your application: python run.py")
        print(f"  2. Login as admin: admin@dialsmart.com / admin123")
        print(f"  3. Browse phones and test recommendations")

        print("\n" + "="*70 + "\n")

    except FileNotFoundError:
        print(f"\n✗ Error: CSV file 'fyp_phoneDataset.csv' not found!")
        print(f"  Please place the CSV file in the project root directory.")
        sys.exit(1)
    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error importing CSV: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
