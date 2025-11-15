"""
Initialize Oracle Database with Default Data
Creates admin account, test user, and sample brands
"""
import os
import sys

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import User, Brand
from datetime import datetime

print("\n" + "="*70)
print("DialSmart: Oracle Database Initialization")
print("="*70)

app = create_app()

with app.app_context():
    try:
        print("\n[1/3] Creating Admin Account...")

        # Check if admin exists
        admin = User.query.filter_by(email='admin@dialsmart.com').first()
        if admin:
            print("  ⚠ Admin already exists. Skipping.")
        else:
            # Create admin user
            admin = User(
                full_name='DialSmart Admin',
                email='admin@dialsmart.com',
                is_admin=True,
                is_active=True,
                user_category='Working Professional',
                age_range='26-35',
                created_at=datetime.utcnow(),
                last_active=datetime.utcnow()
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("  ✓ Admin created: admin@dialsmart.com / admin123")

        print("\n[2/3] Creating Test User Account...")

        # Check if test user exists
        test_user = User.query.filter_by(email='user@dialsmart.com').first()
        if test_user:
            print("  ⚠ Test user already exists. Skipping.")
        else:
            # Create test user
            test_user = User(
                full_name='Test User',
                email='user@dialsmart.com',
                is_admin=False,
                is_active=True,
                user_category='Student',
                age_range='18-25',
                created_at=datetime.utcnow(),
                last_active=datetime.utcnow()
            )
            test_user.set_password('user123')
            db.session.add(test_user)
            db.session.commit()
            print("  ✓ Test user created: user@dialsmart.com / user123")

        print("\n[3/3] Creating Sample Brands...")

        # Sample brands from Malaysian market
        sample_brands = [
            {
                'name': 'Samsung',
                'description': 'South Korean multinational conglomerate, leader in smartphones, displays, and technology innovation.',
                'tagline': 'Together for Tomorrow',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Apple',
                'description': 'American technology company known for iPhone, innovation, and premium quality products.',
                'tagline': 'Think Different',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Xiaomi',
                'description': 'Chinese electronics company offering high-performance phones at competitive prices.',
                'tagline': 'Mi fans for life',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Oppo',
                'description': 'Chinese smartphone manufacturer known for camera technology and fast charging.',
                'tagline': 'Inspiration Ahead',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Vivo',
                'description': 'Chinese technology company specializing in smartphones with advanced camera features.',
                'tagline': 'Camera & Music',
                'is_featured': True,
                'is_active': True
            },
            {
                'name': 'Realme',
                'description': 'Fast-growing Chinese brand targeting youth with trendy, affordable smartphones.',
                'tagline': 'Dare to Leap',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Infinix',
                'description': 'Hong Kong-based brand offering budget-friendly smartphones for emerging markets.',
                'tagline': 'The Future is Now',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Poco',
                'description': 'Xiaomi sub-brand focusing on performance-oriented affordable flagship phones.',
                'tagline': 'Everything you need, nothing you don\'t',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Redmi',
                'description': 'Xiaomi sub-brand providing value-for-money smartphones for budget-conscious users.',
                'tagline': 'Reliable. Quality. Value.',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Honor',
                'description': 'Former Huawei sub-brand, now independent, offering innovative mid-range phones.',
                'tagline': 'For the Brave',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Google',
                'description': 'American tech giant offering Pixel phones with pure Android and AI features.',
                'tagline': 'Do more with AI',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Asus',
                'description': 'Taiwanese company known for ROG gaming phones and innovative ZenFone series.',
                'tagline': 'Inspiring Innovation',
                'is_featured': False,
                'is_active': True
            },
            {
                'name': 'Huawei',
                'description': 'Chinese telecommunications giant known for camera technology and premium design.',
                'tagline': 'Make it Possible',
                'is_featured': False,
                'is_active': True
            }
        ]

        brands_created = 0
        brands_skipped = 0

        for brand_data in sample_brands:
            # Check if brand exists
            existing_brand = Brand.query.filter_by(name=brand_data['name']).first()
            if existing_brand:
                brands_skipped += 1
            else:
                brand = Brand(**brand_data)
                db.session.add(brand)
                brands_created += 1

        db.session.commit()

        print(f"  ✓ Brands created: {brands_created}")
        if brands_skipped > 0:
            print(f"  ⚠ Brands skipped (already exist): {brands_skipped}")

        print("\n" + "="*70)
        print("✓ INITIALIZATION COMPLETE!")
        print("="*70)

        # Summary
        total_users = User.query.count()
        total_brands = Brand.query.count()

        print(f"\nDatabase Summary:")
        print(f"  • Total Users: {total_users}")
        print(f"  • Total Brands: {total_brands}")

        print(f"\nDefault Accounts Created:")
        print(f"  Admin:")
        print(f"    Email: admin@dialsmart.com")
        print(f"    Password: admin123")
        print(f"\n  Test User:")
        print(f"    Email: user@dialsmart.com")
        print(f"    Password: user123")

        print(f"\nNext Steps:")
        print(f"  1. Run your application: python run.py")
        print(f"  2. Login as admin: admin@dialsmart.com / admin123")
        print(f"  3. Import phones from CSV: python import_csv_dataset.py")
        print(f"  4. Or manually add phones via Admin Panel")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error initializing database: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
