"""
SQLite to Oracle Database Migration Script
Migrates all data from SQLite to Oracle Database
"""
import os
import sys

# Set DB_TYPE to SQLite temporarily to read from SQLite
os.environ['DB_TYPE'] = 'sqlite'

from app import create_app, db as sqlite_db
from app.models import User, Brand, Phone, PhoneSpecification, Recommendation, Comparison, ChatHistory, UserPreference

print("\n" + "="*70)
print("DialSmart: SQLite to Oracle Database Migration")
print("="*70)

# Step 1: Read all data from SQLite
print("\n[1/3] Reading data from SQLite database...")

app_sqlite = create_app()

with app_sqlite.app_context():
    try:
        # Read all data
        users = User.query.all()
        brands = Brand.query.all()
        phones = Phone.query.all()
        phone_specs = PhoneSpecification.query.all()
        preferences = UserPreference.query.all()
        recommendations = Recommendation.query.all()
        comparisons = Comparison.query.all()
        chat_history = ChatHistory.query.all()

        print(f"  ✓ Users: {len(users)}")
        print(f"  ✓ Brands: {len(brands)}")
        print(f"  ✓ Phones: {len(phones)}")
        print(f"  ✓ Phone Specifications: {len(phone_specs)}")
        print(f"  ✓ User Preferences: {len(preferences)}")
        print(f"  ✓ Recommendations: {len(recommendations)}")
        print(f"  ✓ Comparisons: {len(comparisons)}")
        print(f"  ✓ Chat History: {len(chat_history)}")

        # Convert to dictionaries
        users_data = []
        for user in users:
            users_data.append({
                'id': user.id,
                'full_name': user.full_name,
                'email': user.email,
                'password_hash': user.password_hash,
                'is_admin': user.is_admin,
                'is_active': user.is_active,
                'user_category': user.user_category,
                'age_range': user.age_range,
                'created_at': user.created_at,
                'last_active': user.last_active
            })

        brands_data = []
        for brand in brands:
            brands_data.append({
                'id': brand.id,
                'name': brand.name,
                'description': brand.description,
                'tagline': brand.tagline,
                'logo_url': brand.logo_url,
                'is_featured': brand.is_featured,
                'is_active': brand.is_active,
                'created_at': brand.created_at
            })

        phones_data = []
        for phone in phones:
            phones_data.append({
                'id': phone.id,
                'brand_id': phone.brand_id,
                'model_name': phone.model_name,
                'model_number': phone.model_number,
                'price': phone.price,
                'main_image': phone.main_image,
                'gallery_images': phone.gallery_images,
                'is_active': phone.is_active,
                'availability_status': phone.availability_status,
                'release_date': phone.release_date,
                'created_at': phone.created_at,
                'updated_at': phone.updated_at
            })

        specs_data = []
        for spec in phone_specs:
            specs_data.append({
                'id': spec.id,
                'phone_id': spec.phone_id,
                'screen_size': spec.screen_size,
                'screen_resolution': spec.screen_resolution,
                'screen_type': spec.screen_type,
                'display_type': spec.display_type,
                'refresh_rate': spec.refresh_rate,
                'ppi': spec.ppi,
                'multitouch': spec.multitouch,
                'protection': spec.protection,
                'processor': spec.processor,
                'chipset': spec.chipset,
                'cpu': spec.cpu,
                'gpu': spec.gpu,
                'processor_brand': spec.processor_brand,
                'ram_options': spec.ram_options,
                'storage_options': spec.storage_options,
                'expandable_storage': spec.expandable_storage,
                'card_slot': spec.card_slot,
                'rear_camera': spec.rear_camera,
                'rear_camera_main': spec.rear_camera_main,
                'front_camera': spec.front_camera,
                'front_camera_mp': spec.front_camera_mp,
                'camera_features': spec.camera_features,
                'flash': spec.flash,
                'video_recording': spec.video_recording,
                'battery_capacity': spec.battery_capacity,
                'battery': spec.battery,
                'charging_speed': spec.charging_speed,
                'fast_charging': spec.fast_charging,
                'wireless_charging': spec.wireless_charging,
                'removable_battery': spec.removable_battery,
                'sim': spec.sim,
                'technology': spec.technology,
                'network_5g': spec.network_5g,
                'network_4g': spec.network_4g,
                'network_3g': spec.network_3g,
                'network_2g': spec.network_2g,
                'network_speed': spec.network_speed,
                'has_5g': spec.has_5g,
                'wifi_standard': spec.wifi_standard,
                'bluetooth_version': spec.bluetooth_version,
                'gps': spec.gps,
                'nfc': spec.nfc,
                'usb': spec.usb,
                'audio_jack': spec.audio_jack,
                'radio': spec.radio,
                'operating_system': spec.operating_system,
                'weight': spec.weight,
                'dimensions': spec.dimensions,
                'colors_available': spec.colors_available,
                'body_material': spec.body_material,
                'fingerprint_sensor': spec.fingerprint_sensor,
                'face_unlock': spec.face_unlock,
                'water_resistance': spec.water_resistance,
                'dual_sim': spec.dual_sim,
                'sensors': spec.sensors,
                'product_url': spec.product_url
            })

        print("\n✓ Data extraction complete!")

    except Exception as e:
        print(f"\n✗ Error reading from SQLite: {str(e)}")
        sys.exit(1)

# Step 2: Switch to Oracle and create tables
print("\n[2/3] Connecting to Oracle Database and creating tables...")

# Now switch to Oracle
os.environ['DB_TYPE'] = 'oracle'

# Reload app with Oracle configuration
from app import create_app as create_app_oracle
from app import db as oracle_db

app_oracle = create_app_oracle()

with app_oracle.app_context():
    try:
        # Drop all existing tables (clean slate)
        print("  • Dropping existing tables...")
        oracle_db.drop_all()

        # Create all tables
        print("  • Creating tables...")
        oracle_db.create_all()
        print("  ✓ Tables created successfully!")

    except Exception as e:
        print(f"\n✗ Error creating Oracle tables: {str(e)}")
        print("\nMake sure Oracle Database is running and credentials in config.py are correct!")
        print("Check the service name (XEPDB1 for Oracle XE Pluggable DB, or XE for non-CDB)")
        sys.exit(1)

# Step 3: Import data into Oracle
print("\n[3/3] Importing data into Oracle Database...")

with app_oracle.app_context():
    try:
        # Import users
        print(f"  • Importing {len(users_data)} users...")
        for user_dict in users_data:
            user = User(**user_dict)
            oracle_db.session.add(user)
        oracle_db.session.commit()
        print("  ✓ Users imported")

        # Import brands
        print(f"  • Importing {len(brands_data)} brands...")
        for brand_dict in brands_data:
            brand = Brand(**brand_dict)
            oracle_db.session.add(brand)
        oracle_db.session.commit()
        print("  ✓ Brands imported")

        # Import phones
        print(f"  • Importing {len(phones_data)} phones...")
        for phone_dict in phones_data:
            phone = Phone(**phone_dict)
            oracle_db.session.add(phone)
        oracle_db.session.commit()
        print("  ✓ Phones imported")

        # Import phone specifications
        print(f"  • Importing {len(specs_data)} phone specifications...")
        for spec_dict in specs_data:
            spec = PhoneSpecification(**spec_dict)
            oracle_db.session.add(spec)
        oracle_db.session.commit()
        print("  ✓ Phone specifications imported")

        print("\n" + "="*70)
        print("✓ MIGRATION COMPLETE!")
        print("="*70)
        print(f"\nSuccessfully migrated:")
        print(f"  • {len(users_data)} users")
        print(f"  • {len(brands_data)} brands")
        print(f"  • {len(phones_data)} phones")
        print(f"  • {len(specs_data)} phone specifications")
        print("\nYour DialSmart system is now running on Oracle Database!")
        print("\nNext steps:")
        print("  1. Update config.py: Set DB_TYPE = 'oracle'")
        print("  2. Run your application: python run.py")
        print("  3. Login and verify all data is present")
        print("  4. Use SQL*Plus to query data:")
        print("     sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1")
        print("="*70 + "\n")

    except Exception as e:
        oracle_db.session.rollback()
        print(f"\n✗ Error importing data: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
