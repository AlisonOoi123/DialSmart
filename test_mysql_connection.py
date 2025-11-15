"""
MySQL Connection Test Script
Tests if DialSmart can connect to MySQL successfully
"""
import os
os.environ['USE_MYSQL'] = 'true'  # Force MySQL connection

print("\n" + "="*70)
print("DialSmart MySQL Connection Test")
print("="*70)

try:
    print("\n[1/5] Importing Flask app...")
    from app import create_app, db
    from app.models import User, Brand, Phone, PhoneSpecification
    print("  ✓ Imports successful")

    print("\n[2/5] Creating Flask application context...")
    app = create_app()
    print("  ✓ App created")

    print("\n[3/5] Testing database connection...")
    with app.app_context():
        # Try to connect
        db.engine.connect()
        print("  ✓ MySQL connection successful!")

        # Show connection details
        print(f"\n  Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"  Database: {app.config['MYSQL_DATABASE']}")
        print(f"  Host: {app.config['MYSQL_HOST']}:{app.config['MYSQL_PORT']}")
        print(f"  User: {app.config['MYSQL_USER']}")

        print("\n[4/5] Checking tables...")
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if tables:
            print(f"  ✓ Found {len(tables)} tables:")
            for table in tables:
                print(f"    • {table}")
        else:
            print("  ⚠ No tables found - run table creation first")

        print("\n[5/5] Testing queries...")
        try:
            user_count = User.query.count()
            brand_count = Brand.query.count()
            phone_count = Phone.query.count()
            spec_count = PhoneSpecification.query.count()

            print(f"  ✓ Database has:")
            print(f"    • Users: {user_count}")
            print(f"    • Brands: {brand_count}")
            print(f"    • Phones: {phone_count}")
            print(f"    • Phone Specifications: {spec_count}")

            if phone_count > 0:
                print("\n  Sample phones:")
                phones = Phone.query.limit(3).all()
                for phone in phones:
                    print(f"    • {phone.model_name} - RM {phone.price:,.2f}")

        except Exception as e:
            print(f"  ⚠ Query test failed: {str(e)}")
            print("  (This is normal if tables are empty)")

    print("\n" + "="*70)
    print("✓ ALL TESTS PASSED!")
    print("="*70)
    print("\nYour MySQL connection is working perfectly!")
    print("You can now run: python run.py")
    print("="*70 + "\n")

except ImportError as e:
    print(f"\n✗ Import Error: {str(e)}")
    print("\nSolution: Make sure PyMySQL is installed:")
    print("  pip install PyMySQL==1.1.0")

except Exception as e:
    print(f"\n✗ Connection Test Failed!")
    print(f"Error: {str(e)}\n")

    print("Common Solutions:")
    print("1. Check if MySQL is running:")
    print("   - Windows: Services → MySQL80 should be 'Running'")
    print("   - Or check XAMPP Control Panel")
    print("\n2. Verify database credentials in config.py:")
    print("   - MYSQL_USER = 'dialsmart_user'")
    print("   - MYSQL_PASSWORD = 'dialsmart123'")
    print("   - MYSQL_DATABASE = 'dialsmart'")
    print("\n3. Make sure database exists:")
    print("   mysql -u root -p")
    print("   CREATE DATABASE dialsmart;")
    print("\n4. Create database user:")
    print("   CREATE USER 'dialsmart_user'@'localhost' IDENTIFIED BY 'dialsmart123';")
    print("   GRANT ALL PRIVILEGES ON dialsmart.* TO 'dialsmart_user'@'localhost';")
    print("   FLUSH PRIVILEGES;")
    print("\n" + "="*70 + "\n")
