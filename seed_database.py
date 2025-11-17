"""
Seed the database with brand and phone data
"""
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification, User
from datetime import datetime, date

# Create application instance
app = create_app()

with app.app_context():
    print("Seeding database with sample data...")

    # Create sample brands
    brands_data = [
        {'name': 'Samsung', 'description': 'South Korean multinational conglomerate', 'tagline': 'Inspire the World, Create the Future', 'is_featured': True},
        {'name': 'Apple', 'description': 'American technology company', 'tagline': 'Think Different', 'is_featured': True},
        {'name': 'Xiaomi', 'description': 'Chinese electronics company', 'tagline': 'Just for fans', 'is_featured': True},
        {'name': 'Huawei', 'description': 'Chinese technology company', 'tagline': 'Make It Possible', 'is_featured': True},
        {'name': 'Oppo', 'description': 'Chinese consumer electronics company', 'tagline': 'Camera Phone', 'is_featured': True},
        {'name': 'Vivo', 'description': 'Chinese technology company', 'tagline': 'Camera & Music', 'is_featured': True},
        {'name': 'Realme', 'description': 'Chinese smartphone manufacturer', 'tagline': 'Dare to Leap', 'is_featured': True},
    ]

    for brand_data in brands_data:
        existing_brand = Brand.query.filter_by(name=brand_data['name']).first()
        if not existing_brand:
            brand = Brand(**brand_data)
            db.session.add(brand)

    db.session.commit()
    print("✓ Brands created successfully!")

    # Create sample phones
    samsung = Brand.query.filter_by(name='Samsung').first()
    apple = Brand.query.filter_by(name='Apple').first()
    xiaomi = Brand.query.filter_by(name='Xiaomi').first()

    if samsung:
        phones_data = [
            {
                'brand_id': samsung.id,
                'model_name': 'Samsung Galaxy S23 Ultra',
                'price': 5299.00,
                'availability_status': 'Available',
                'release_date': date(2023, 2, 1),
                'specs': {
                    'screen_size': 6.8,
                    'screen_resolution': '1440x3088',
                    'screen_type': 'Dynamic AMOLED 2X',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 2',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '256GB, 512GB, 1TB',
                    'rear_camera': '200MP + 10MP + 10MP + 12MP',
                    'rear_camera_main': 200,
                    'front_camera': '12MP',
                    'front_camera_mp': 12,
                    'battery_capacity': 5000,
                    'charging_speed': '45W Fast Charging',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 234,
                    'dimensions': '163.4 x 78.1 x 8.9 mm'
                }
            },
            {
                'brand_id': samsung.id,
                'model_name': 'Samsung Galaxy A54',
                'price': 1899.00,
                'availability_status': 'Available',
                'release_date': date(2023, 3, 15),
                'specs': {
                    'screen_size': 6.4,
                    'screen_resolution': '1080x2340',
                    'screen_type': 'Super AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Exynos 1380',
                    'processor_brand': 'Samsung',
                    'ram_options': '8GB',
                    'storage_options': '128GB, 256GB',
                    'rear_camera': '50MP + 12MP + 5MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 5000,
                    'charging_speed': '25W Fast Charging',
                    'wireless_charging': False,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP67',
                    'dual_sim': True,
                    'weight': 202,
                    'dimensions': '158.2 x 76.7 x 8.2 mm'
                }
            }
        ]

        for phone_data in phones_data:
            existing_phone = Phone.query.filter_by(model_name=phone_data['model_name']).first()
            if not existing_phone:
                specs_data = phone_data.pop('specs')
                phone = Phone(**phone_data)
                db.session.add(phone)
                db.session.flush()

                specs = PhoneSpecification(phone_id=phone.id, **specs_data)
                db.session.add(specs)

    if apple:
        phones_data = [
            {
                'brand_id': apple.id,
                'model_name': 'iPhone 15 Pro Max',
                'price': 5999.00,
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
                    'charging_speed': '27W Fast Charging',
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
            }
        ]

        for phone_data in phones_data:
            existing_phone = Phone.query.filter_by(model_name=phone_data['model_name']).first()
            if not existing_phone:
                specs_data = phone_data.pop('specs')
                phone = Phone(**phone_data)
                db.session.add(phone)
                db.session.flush()

                specs = PhoneSpecification(phone_id=phone.id, **specs_data)
                db.session.add(specs)

    if xiaomi:
        phones_data = [
            {
                'brand_id': xiaomi.id,
                'model_name': 'Xiaomi 13 Pro',
                'price': 3499.00,
                'availability_status': 'Available',
                'release_date': date(2023, 2, 26),
                'specs': {
                    'screen_size': 6.73,
                    'screen_resolution': '1440x3200',
                    'screen_type': 'LTPO AMOLED',
                    'refresh_rate': 120,
                    'processor': 'Snapdragon 8 Gen 2',
                    'processor_brand': 'Qualcomm',
                    'ram_options': '8GB, 12GB',
                    'storage_options': '128GB, 256GB, 512GB',
                    'rear_camera': '50MP + 50MP + 50MP',
                    'rear_camera_main': 50,
                    'front_camera': '32MP',
                    'front_camera_mp': 32,
                    'battery_capacity': 4820,
                    'charging_speed': '120W Fast Charging',
                    'wireless_charging': True,
                    'has_5g': True,
                    'operating_system': 'Android 13',
                    'fingerprint_sensor': True,
                    'face_unlock': True,
                    'water_resistance': 'IP68',
                    'dual_sim': True,
                    'weight': 229,
                    'dimensions': '162.9 x 74.6 x 8.4 mm'
                }
            }
        ]

        for phone_data in phones_data:
            existing_phone = Phone.query.filter_by(model_name=phone_data['model_name']).first()
            if not existing_phone:
                specs_data = phone_data.pop('specs')
                phone = Phone(**phone_data)
                db.session.add(phone)
                db.session.flush()

                specs = PhoneSpecification(phone_id=phone.id, **specs_data)
                db.session.add(specs)

    db.session.commit()
    print("✓ Sample phones created successfully!")

    # Create a test user
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
        db.session.commit()
        print("✓ Test user created: user@dialsmart.my / password123")

    print("\n✅ Database seeded successfully!")
    print("\nYou can now login with:")
    print("Email: user@dialsmart.my")
    print("Password: password123")
