"""
Comprehensive Malaysian Phone Data Seeder
Populates database with realistic Malaysian smartphone data with MYR pricing
"""
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification, User, UserPreference
from datetime import date, datetime
import sys

def init_data():
    """Initialize database with comprehensive Malaysian phone data"""
    app = create_app()

    with app.app_context():
        print("=" * 60)
        print("DialSmart Database Initialization")
        print("=" * 60)

        # Create tables
        print("\n[1/5] Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")

        # Create brands
        print("\n[2/5] Creating smartphone brands...")
        brands_data = [
            {
                'name': 'Samsung',
                'description': 'South Korean electronics giant, world leader in smartphone innovation',
                'tagline': 'Do What You Can\'t',
                'is_featured': True
            },
            {
                'name': 'Apple',
                'description': 'American technology company known for premium smartphones',
                'tagline': 'Think Different',
                'is_featured': True
            },
            {
                'name': 'Xiaomi',
                'description': 'Chinese electronics company offering value-for-money smartphones',
                'tagline': 'Just for Fans',
                'is_featured': True
            },
            {
                'name': 'Oppo',
                'description': 'Chinese brand focusing on camera technology and design',
                'tagline': 'Inspiration Ahead',
                'is_featured': True
            },
            {
                'name': 'Vivo',
                'description': 'Chinese smartphone manufacturer known for selfie cameras',
                'tagline': 'Camera & Music',
                'is_featured': True
            },
            {
                'name': 'Realme',
                'description': 'Youth-focused brand offering affordable performance phones',
                'tagline': 'Dare to Leap',
                'is_featured': True
            },
            {
                'name': 'Honor',
                'description': 'Independent smartphone brand with innovative technology',
                'tagline': 'Be Brave',
                'is_featured': True
            },
            {
                'name': 'Huawei',
                'description': 'Chinese telecommunications giant with advanced camera tech',
                'tagline': 'Make It Possible',
                'is_featured': False
            },
            {
                'name': 'Nokia',
                'description': 'Finnish brand known for durability and pure Android',
                'tagline': 'Connecting People',
                'is_featured': False
            },
            {
                'name': 'OnePlus',
                'description': 'Premium smartphone brand with flagship killer devices',
                'tagline': 'Never Settle',
                'is_featured': True
            },
        ]

        brand_objects = {}
        for brand_data in brands_data:
            existing = Brand.query.filter_by(name=brand_data['name']).first()
            if not existing:
                brand = Brand(**brand_data)
                db.session.add(brand)
                db.session.flush()
                brand_objects[brand.name] = brand
                print(f"  ✓ Created brand: {brand.name}")
            else:
                brand_objects[brand_data['name']] = existing
                print(f"  • Brand already exists: {brand_data['name']}")

        db.session.commit()
        print(f"\n✓ {len(brand_objects)} brands initialized!")

        # Create comprehensive phone data
        print("\n[3/5] Creating smartphone listings with Malaysian pricing...")

        phones_data = [
            # Samsung Phones
            {
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy S24 Ultra',
                'price': 5999.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 24),
                'specs': {
                    'screen_size': 6.8,
                    'screen_resolution': '1440x3120',
                    'screen_type': 'Dynamic AMOLED 2X',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '200MP + 50MP + 12MP + 10MP',
                    'rear_camera_main': 200,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 5000,
                    'charging_speed': '45W Super Fast Charging',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 232,
                    'dimensions': '162.3 x 79.0 x 8.6 mm'
                }
            },
            {
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy S23 FE',
                'price': 2699.00,
                'availability_status': 'Available',
                'release_date': date(2023, 12, 8),
                'specs': {
                    'screen_size': 6.4,
                    'screen_resolution': '1080x2340',
                    'screen_type': 'Dynamic AMOLED 2X',
                    'refresh_rate': 120,
                    'processor': 'Exynos 2200',
                    'processor_brand': 'Samsung',
                    'ram_options': '8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 12MP + 8MP',
                    'rear_camera_main': 50,
                    'front_camera': '10MP',
                    'front_camera_mp': 10,
                    'battery_capacity': 4500,
                    'charging_speed': '25W Fast Charging',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 209,
                    'dimensions': '158.0 x 76.5 x 8.2 mm'
                }
            },
            {
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy A55 5G',
                'price': 1899.00,
                'availability_status': 'Available',
                'release_date': date(2024, 3, 11),
                'specs': {
                    'screen_size': 6.6,
                    'screen_resolution': '1080x2340',
                    'screen_type': 'Super AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Exynos 1480',
                    'processor_brand': 'Samsung',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 12MP + 5MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5000,
                    'charging_speed': '25W Fast Charging',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP67',
                    'dual_sim': True,
                    'weight': 213,
                    'dimensions': '161.1 x 77.4 x 8.2 mm'
                }
            },
            {
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy A35 5G',
                'price': 1499.00,
                'availability_status': 'Available',
                'release_date': date(2024, 3, 11),
                'specs': {
                    'screen_size': 6.6,
                    'screen_resolution': '1080x2340',
                    'screen_type': 'Super AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Exynos 1380',
                    'processor_brand': 'Samsung',
                    'ram_options': '6GB, 8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 8MP + 5MP',
                    'rear_camera_main': 50,
                    'front_camera': '13MP',
                    'front_camera_mp': 13,
                    'battery_capacity': 5000,
                    'charging_speed': '25W Fast Charging',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP67',
                    'dual_sim': True,
                    'weight': 209,
                    'dimensions': '161.7 x 78.0 x 8.2 mm'
                }
            },
            {
                'brand': 'Samsung',
                'model_name': 'Samsung Galaxy A15 5G',
                'price': 799.00,
                'availability_status': 'Available',
                'release_date': date(2023, 12, 1),
                'specs': {
                    'screen_size': 6.5,
                    'screen_resolution': '1080x2340',
                    'screen_type': 'Super AMOLED',
                    'refresh_rate': 90,
                    'processor': 'MediaTek Dimensity 6100+',
                    'processor_brand': 'MediaTek',
                    'ram_options': '6GB, 8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 5MP + 2MP',
                    'rear_camera_main': 50,
                    'front_camera': '13MP',
                    'front_camera_mp': 13,
                    'battery_capacity': 5000,
                    'charging_speed': '25W Fast Charging',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 200,
                    'dimensions': '160.1 x 76.8 x 8.4 mm'
                }
            },

            # Apple iPhones
            {
                'brand': 'Apple',
                'model_name': 'iPhone 15 Pro Max',
                'price': 6299.00,
                'availability_status': 'Available',
                'release_date': date(2023, 9, 22),
                'specs': {
                    'screen_size': 6.7,
                    'screen_resolution': '1290x2796',
                    'screen_type': 'LTPO Super Retina XDR OLED',
                    'refresh_rate': 120,
                    'processor': 'A17 Pro',
                    'processor_brand': 'Apple',
                    'ram_options': '8GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '48MP + 12MP + 12MP',
                    'rear_camera_main': 48,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 4441,
                    'charging_speed': '27W Wired, 15W MagSafe',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'iOS 17',
                    'fingerprint_sensor': False,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 221,
                    'dimensions': '159.9 x 76.7 x 8.25 mm'
                }
            },
            {
                'brand': 'Apple',
                'model_name': 'iPhone 15 Pro',
                'price': 5499.00,
                'availability_status': 'Available',
                'release_date': date(2023, 9, 22),
                'specs': {
                    'screen_size': 6.1,
                    'screen_resolution': '1179x2556',
                    'screen_type': 'LTPO Super Retina XDR OLED',
                    'refresh_rate': 120,
                    'processor': 'A17 Pro',
                    'processor_brand': 'Apple',
                    'ram_options': '8GB',
                    'storage_options': '128GB, 256GB, 512GB, 1TB',
                    'rear_camera': '48MP + 12MP + 12MP',
                    'rear_camera_main': 48,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 3274,
                    'charging_speed': '23W Wired, 15W MagSafe',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'iOS 17',
                    'fingerprint_sensor': False,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 187,
                    'dimensions': '146.6 x 70.6 x 8.25 mm'
                }
            },
            {
                'brand': 'Apple',
                'model_name': 'iPhone 15',
                'price': 4399.00,
                'availability_status': 'Available',
                'release_date': date(2023, 9, 22),
                'specs': {
                    'screen_size': 6.1,
                    'screen_resolution': '1179x2556',
                    'screen_type': 'Super Retina XDR OLED',
                    'refresh_rate': 60,
                    'processor': 'A16 Bionic',
                    'processor_brand': 'Apple',
                    'ram_options': '6GB',
                    'storage_options': '128GB, 256GB, 512GB',
                    'rear_camera': '48MP + 12MP',
                    'rear_camera_main': 48,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 3349,
                    'charging_speed': '20W Wired, 15W MagSafe',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'iOS 17',
                    'fingerprint_sensor': False,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 171,
                    'dimensions': '147.6 x 71.6 x 7.8 mm'
                }
            },
            {
                'brand': 'Apple',
                'model_name': 'iPhone 14',
                'price': 3699.00,
                'availability_status': 'Available',
                'release_date': date(2022, 9, 16),
                'specs': {
                    'screen_size': 6.1,
                    'screen_resolution': '1170x2532',
                    'screen_type': 'Super Retina XDR OLED',
                    'refresh_rate': 60,
                    'processor': 'A15 Bionic',
                    'processor_brand': 'Apple',
                    'ram_options': '6GB',
                    'storage_options': '128GB, 256GB, 512GB',
                    'rear_camera': '12MP + 12MP',
                    'rear_camera_main': 12,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 3279,
                    'charging_speed': '20W Wired, 15W MagSafe',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'iOS 16',
                    'fingerprint_sensor': False,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 172,
                    'dimensions': '146.7 x 71.5 x 7.8 mm'
                }
            },

            # Xiaomi Phones
            {
                'brand': 'Xiaomi',
                'model_name': 'Xiaomi 14',
                'price': 3999.00,
                'availability_status': 'Available',
                'release_date': date(2024, 2, 25),
                'specs': {
                    'screen_size': 6.36,
                    'screen_resolution': '1200x2670',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 50MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 4610,
                    'charging_speed': '90W HyperCharge',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 193,
                    'dimensions': '152.8 x 71.5 x 8.2 mm'
                }
            },
            {
                'brand': 'Xiaomi',
                'model_name': 'Xiaomi 13T Pro',
                'price': 2699.00,
                'availability_status': 'Available',
                'release_date': date(2023, 9, 26),
                'specs': {
                    'screen_size': 6.67,
                    'screen_resolution': '1220x2712',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 144,
                    'processor': 'MediaTek Dimensity 9200+',
                    'processor_brand': 'MediaTek',
                    'ram_options': '12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 50MP + 12MP',
                    'rear_camera_main': 50,
                    'front_camera': '20MP',
                    'front_camera_mp': 20,
                    'battery_capacity': 5000,
                    'charging_speed': '120W HyperCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 200,
                    'dimensions': '162.2 x 75.7 x 8.5 mm'
                }
            },
            {
                'brand': 'Xiaomi',
                'model_name': 'Redmi Note 13 Pro+ 5G',
                'price': 1699.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 4),
                'specs': {
                    'screen_size': 6.67,
                    'screen_resolution': '1220x2712',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'MediaTek Dimensity 7200 Ultra',
                    'processor_brand': 'MediaTek',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '200MP + 8MP + 2MP',
                    'rear_camera_main': 200,
                    'front_camera': '16MP',
                    'front_camera_mp': 16,
                    'battery_capacity': 5000,
                    'charging_speed': '120W HyperCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 204,
                    'dimensions': '161.4 x 74.2 x 8.9 mm'
                }
            },
            {
                'brand': 'Xiaomi',
                'model_name': 'Redmi Note 13 Pro 5G',
                'price': 1299.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 4),
                'specs': {
                    'screen_size': 6.67,
                    'screen_resolution': '1080x2400',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 7s Gen 2',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '200MP + 8MP + 2MP',
                    'rear_camera_main': 200,
                    'front_camera': '16MP',
                    'front_camera_mp': 16,
                    'battery_capacity': 5100,
                    'charging_speed': '67W Turbo Charging',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP54',
                    'dual_sim': True,
                    'weight': 187,
                    'dimensions': '161.2 x 74.3 x 8.0 mm'
                }
            },

            # Oppo Phones
            {
                'brand': 'Oppo',
                'model_name': 'Oppo Find X7 Ultra',
                'price': 4999.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 8),
                'specs': {
                    'screen_size': 6.82,
                    'screen_resolution': '1440x3168',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB, 16GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 50MP + 50MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5000,
                    'charging_speed': '100W SuperVOOC',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 221,
                    'dimensions': '164.3 x 76.2 x 9.5 mm'
                }
            },
            {
                'brand': 'Oppo',
                'model_name': 'Oppo Reno 11 5G',
                'price': 1899.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 11),
                'specs': {
                    'screen_size': 6.7,
                    'screen_resolution': '1080x2412',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'MediaTek Dimensity 7050',
                    'processor_brand': 'MediaTek',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB',
                    'rear_camera': '50MP + 32MP + 8MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5000,
                    'charging_speed': '67W SuperVOOC',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP65',
                    'dual_sim': True,
                    'weight': 184,
                    'dimensions': '162.4 x 74.3 x 7.6 mm'
                }
            },
            {
                'brand': 'Oppo',
                'model_name': 'Oppo A79 5G',
                'price': 999.00,
                'availability_status': 'Available',
                'release_date': date(2023, 11, 1),
                'specs': {
                    'screen_size': 6.72,
                    'screen_resolution': '1080x2400',
                    'screen_type': 'IPS LCD',
                    'refresh_rate': 90,
                    'processor': 'MediaTek Dimensity 6020',
                    'processor_brand': 'MediaTek',
                    'ram_options': '8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 2MP',
                    'rear_camera_main': 50,
                    'front_camera': '8MP',
                    'front_camera_mp': 8,
                    'battery_capacity': 5000,
                    'charging_speed': '33W SuperVOOC',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP54',
                    'dual_sim': True,
                    'weight': 193,
                    'dimensions': '165.7 x 76.1 x 8.0 mm'
                }
            },

            # Vivo Phones
            {
                'brand': 'Vivo',
                'model_name': 'Vivo X100 Pro',
                'price': 4699.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 4),
                'specs': {
                    'screen_size': 6.78,
                    'screen_resolution': '1260x2800',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 120,
                    'processor': 'MediaTek Dimensity 9300',
                    'processor_brand': 'MediaTek',
                    'ram_options': '12GB, 16GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '50MP + 50MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5400,
                    'charging_speed': '100W FlashCharge',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 221,
                    'dimensions': '164.1 x 75.3 x 8.9 mm'
                }
            },
            {
                'brand': 'Vivo',
                'model_name': 'Vivo V30 5G',
                'price': 2099.00,
                'availability_status': 'Available',
                'release_date': date(2024, 2, 26),
                'specs': {
                    'screen_size': 6.78,
                    'screen_resolution': '1260x2800',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 7 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '50MP',
                    'front_camera_mp': 50,
                    'battery_capacity': 5000,
                    'charging_speed': '80W FlashCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP54',
                    'dual_sim': True,
                    'weight': 186,
                    'dimensions': '164.4 x 75.1 x 7.5 mm'
                }
            },
            {
                'brand': 'Vivo',
                'model_name': 'Vivo Y100 5G',
                'price': 1499.00,
                'availability_status': 'Available',
                'release_date': date(2024, 2, 15),
                'specs': {
                    'screen_size': 6.67,
                    'screen_resolution': '1080x2400',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 685',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 8MP + 2MP',
                    'rear_camera_main': 50,
                    'front_camera': '16MP',
                    'front_camera_mp': 16,
                    'battery_capacity': 5000,
                    'charging_speed': '80W FlashCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 190,
                    'dimensions': '164.6 x 75.8 x 7.7 mm'
                }
            },

            # Realme Phones
            {
                'brand': 'Realme',
                'model_name': 'Realme GT 5 Pro',
                'price': 3299.00,
                'availability_status': 'Available',
                'release_date': date(2023, 12, 7),
                'specs': {
                    'screen_size': 6.78,
                    'screen_resolution': '1264x2780',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 144,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB, 16GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '50MP + 50MP + 8MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5400,
                    'charging_speed': '100W SuperVOOC',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP64',
                    'dual_sim': True,
                    'weight': 218,
                    'dimensions': '161.7 x 75.1 x 9.2 mm'
                }
            },
            {
                'brand': 'Realme',
                'model_name': 'Realme 12 Pro+ 5G',
                'price': 1799.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 29),
                'specs': {
                    'screen_size': 6.7,
                    'screen_resolution': '1080x2412',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 7s Gen 2',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 64MP + 8MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5000,
                    'charging_speed': '67W SuperVOOC',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP65',
                    'dual_sim': True,
                    'weight': 196,
                    'dimensions': '161.5 x 74.0 x 8.8 mm'
                }
            },
            {
                'brand': 'Realme',
                'model_name': 'Realme C67 5G',
                'price': 799.00,
                'availability_status': 'Available',
                'release_date': date(2023, 12, 14),
                'specs': {
                    'screen_size': 6.72,
                    'screen_resolution': '1080x2400',
                    'screen_type': 'IPS LCD',
                    'refresh_rate': 120,
                    'processor': 'MediaTek Dimensity 6100+',
                    'processor_brand': 'MediaTek',
                    'ram_options': '6GB, 8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 2MP',
                    'rear_camera_main': 50,
                    'front_camera': '8MP',
                    'front_camera_mp': 8,
                    'battery_capacity': 5000,
                    'charging_speed': '33W SuperVOOC',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 190,
                    'dimensions': '165.7 x 76.1 x 7.9 mm'
                }
            },

            # Honor Phones
            {
                'brand': 'Honor',
                'model_name': 'Honor Magic6 Pro',
                'price': 4599.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 10),
                'specs': {
                    'screen_size': 6.8,
                    'screen_resolution': '1280x2800',
                    'screen_type': 'LTPO OLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB, 16GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '50MP + 180MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '50MP',
                    'front_camera_mp': 50,
                    'battery_capacity': 5600,
                    'charging_speed': '80W SuperCharge',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 225,
                    'dimensions': '162.5 x 75.8 x 8.9 mm'
                }
            },
            {
                'brand': 'Honor',
                'model_name': 'Honor 90 5G',
                'price': 1799.00,
                'availability_status': 'Available',
                'release_date': date(2023, 5, 29),
                'specs': {
                    'screen_size': 6.7,
                    'screen_resolution': '1200x2664',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 7 Gen 1',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '200MP + 12MP + 2MP',
                    'rear_camera_main': 200,
                    'front_camera': '50MP',
                    'front_camera_mp': 50,
                    'battery_capacity': 5000,
                    'charging_speed': '66W SuperCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 183,
                    'dimensions': '161.9 x 74.1 x 7.8 mm'
                }
            },
            {
                'brand': 'Honor',
                'model_name': 'Honor X9b 5G',
                'price': 1299.00,
                'availability_status': 'Available',
                'release_date': date(2023, 10, 12),
                'specs': {
                    'screen_size': 6.78,
                    'screen_resolution': '1200x2652',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 6 Gen 1',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB',
                    'rear_camera': '108MP + 5MP + 2MP',
                    'rear_camera_main': 108,
                    'front_camera': '16MP',
                    'front_camera_mp': 16,
                    'battery_capacity': 5800,
                    'charging_speed': '35W SuperCharge',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 185,
                    'dimensions': '163.6 x 75.5 x 7.98 mm'
                }
            },

            # OnePlus Phones
            {
                'brand': 'OnePlus',
                'model_name': 'OnePlus 12',
                'price': 4299.00,
                'availability_status': 'Available',
                'release_date': date(2024, 1, 23),
                'specs': {
                    'screen_size': 6.82,
                    'screen_resolution': '1440x3168',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 3',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '12GB, 16GB',
                    'storage_options': '256GB, 512GB',
                    'rear_camera': '50MP + 64MP + 48MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5400,
                    'charging_speed': '100W SuperVOOC',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 14',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP65',
                    'dual_sim': True,
                    'weight': 220,
                    'dimensions': '164.3 x 75.8 x 9.2 mm'
                }
            },
            {
                'brand': 'OnePlus',
                'model_name': 'OnePlus Nord CE 3',
                'price': 1299.00,
                'availability_status': 'Available',
                'release_date': date(2023, 7, 6),
                'specs': {
                    'screen_size': 6.7,
                    'screen_resolution': '1080x2412',
                    'screen_type': 'AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 782G',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 8MP + 2MP',
                    'rear_camera_main': 50,
                    'front_camera': '16MP',
                    'front_camera_mp': 16,
                    'battery_capacity': 5000,
                    'charging_speed': '80W SuperVOOC',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': None,
                    'dual_sim': True,
                    'weight': 184,
                    'dimensions': '162.7 x 75.5 x 8.2 mm'
                }
            },
        ]

        phone_count = 0
        for phone_data in phones_data:
            brand = brand_objects.get(phone_data['brand'])
            if not brand:
                print(f"  ✗ Brand not found: {phone_data['brand']}")
                continue

            existing_phone = Phone.query.filter_by(model_name=phone_data['model_name']).first()
            if existing_phone:
                print(f"  • Phone already exists: {phone_data['model_name']}")
                continue

            specs_data = phone_data.pop('specs')
            phone_data['brand_id'] = brand.id
            phone_data.pop('brand')

            phone = Phone(**phone_data)
            db.session.add(phone)
            db.session.flush()

            specs = PhoneSpecification(phone_id=phone.id, **specs_data)
            db.session.add(specs)

            phone_count += 1
            print(f"  ✓ Added: {phone.model_name} - RM {phone.price:,.0f}")

        db.session.commit()
        print(f"\n✓ {phone_count} smartphones added to database!")

        # Create test users
        print("\n[4/5] Creating test user accounts...")

        # Regular user
        test_user = User.query.filter_by(email='user@dialsmart.my').first()
        if not test_user:
            test_user = User(
                email='user@dialsmart.my',
                full_name='Test User',
                user_category='Working Professional',
                age_range='26-35'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            print("  ✓ Created test user: user@dialsmart.my")
        else:
            print("  • Test user already exists")

        # Admin user
        admin_user = User.query.filter_by(email='admin@dialsmart.my').first()
        if not admin_user:
            admin_user = User(
                email='admin@dialsmart.my',
                full_name='Admin User',
                is_admin=True,
                user_category='Admin',
                age_range='26-35'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            print("  ✓ Created admin user: admin@dialsmart.my")
        else:
            print("  • Admin user already exists")

        db.session.commit()

        # Create sample user preference
        print("\n[5/5] Creating sample user preferences...")
        if test_user:
            existing_pref = UserPreference.query.filter_by(user_id=test_user.id).first()
            if not existing_pref:
                user_pref = UserPreference(
                    user_id=test_user.id,
                    min_budget=1000,
                    max_budget=3000,
                    min_ram=8,
                    min_storage=128,
                    min_camera=48,
                    min_battery=4500,
                    requires_5g=True,
                    min_screen_size=6.4,
                    max_screen_size=6.8,
                    primary_usage='["Photography", "Social Media"]',
                    important_features='["Camera", "Battery", "5G"]',
                    preferred_brands='[]'
                )
                db.session.add(user_pref)
                db.session.commit()
                print("  ✓ Created sample user preferences")
            else:
                print("  • User preferences already exist")

        print("\n" + "=" * 60)
        print("✓ DATABASE INITIALIZATION COMPLETE!")
        print("=" * 60)
        print("\n📱 STATISTICS:")
        print(f"  • Total Brands: {Brand.query.count()}")
        print(f"  • Total Phones: {Phone.query.count()}")
        print(f"  • Total Users: {User.query.count()}")

        print("\n🔑 LOGIN CREDENTIALS:")
        print("\n  Regular User:")
        print("    Email: user@dialsmart.my")
        print("    Password: password123")
        print("\n  Admin User:")
        print("    Email: admin@dialsmart.my")
        print("    Password: admin123")

        print("\n🚀 You can now run: python run.py")
        print("   Then visit: http://localhost:5000")
        print("\n" + "=" * 60)

if __name__ == '__main__':
    try:
        init_data()
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
