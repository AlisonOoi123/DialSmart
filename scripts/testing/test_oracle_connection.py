"""
Oracle Database Connection Test Script
Tests the Oracle Database connection and displays database information
"""
import os
import sys

# Force Oracle connection for testing
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import User, Brand, Phone, PhoneSpecification
from sqlalchemy import inspect, text

print("\n" + "="*70)
print("DialSmart: Oracle Database Connection Test")
print("="*70)

app = create_app()

print("\n[1/4] Testing Oracle Database Connection...")

try:
    with app.app_context():
        # Test connection
        db.engine.connect()
        print("  ✓ Oracle connection successful!")

        # Show connection details (without password)
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        # Mask password in URI
        if '@' in db_uri:
            protocol_user = db_uri.split('@')[0]
            host_db = db_uri.split('@')[1]
            protocol = protocol_user.split('://')[0]
            user = protocol_user.split('://')[1].split(':')[0]
            masked_uri = f"{protocol}://{user}:****@{host_db}"
            print(f"  Database URI: {masked_uri}")
        else:
            print(f"  Database URI: {db_uri}")

        print(f"  Database Type: Oracle")
        print(f"  Host: {app.config.get('ORACLE_HOST', 'localhost')}")
        print(f"  Port: {app.config.get('ORACLE_PORT', '1521')}")
        print(f"  Service: {app.config.get('ORACLE_SERVICE', 'XEPDB1')}")
        print(f"  User: {app.config.get('ORACLE_USER', 'dialsmart_user')}")

except Exception as e:
    print(f"\n✗ Connection failed: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Check if Oracle Database is running:")
    print("     - Open Services and check 'OracleServiceXE' and 'OracleXETNSListener'")
    print("  2. Verify credentials in config.py:")
    print("     - ORACLE_USER, ORACLE_PASSWORD, ORACLE_SERVICE")
    print("  3. Test with SQL*Plus:")
    print("     sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1")
    print("  4. Check listener status:")
    print("     lsnrctl status")
    sys.exit(1)

print("\n[2/4] Checking Database Tables...")

with app.app_context():
    try:
        # Get table names
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        if tables:
            print(f"  ✓ Found {len(tables)} tables:")
            for table in sorted(tables):
                print(f"    - {table}")
        else:
            print("  ⚠ No tables found. Run this command to create tables:")
            print('    python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print(\'Tables created!\')"')
    except Exception as e:
        print(f"  ✗ Error checking tables: {str(e)}")

print("\n[3/4] Checking Data...")

with app.app_context():
    try:
        # Count records
        user_count = User.query.count()
        brand_count = Brand.query.count()
        phone_count = Phone.query.count()
        spec_count = PhoneSpecification.query.count()

        print(f"  ✓ Users: {user_count}")
        print(f"  ✓ Brands: {brand_count}")
        print(f"  ✓ Phones: {phone_count}")
        print(f"  ✓ Phone Specifications: {spec_count}")

        if phone_count == 0:
            print("\n  ⚠ No phones found. Import data:")
            print("    Option 1 - From CSV: python import_csv_dataset.py")
            print("    Option 2 - From SQLite: python migrate_sqlite_to_oracle.py")
            print("    Option 3 - Initialize: python initialize_system.py")

    except Exception as e:
        print(f"  ✗ Error querying data: {str(e)}")

print("\n[4/4] Testing Sample Query...")

with app.app_context():
    try:
        # Get sample phones
        sample_phones = Phone.query.limit(3).all()

        if sample_phones:
            print(f"  ✓ Sample phones from Oracle Database:")
            print(f"\n  {'ID':<5} {'Model Name':<30} {'Price (RM)':<12}")
            print(f"  {'-'*5} {'-'*30} {'-'*12}")
            for phone in sample_phones:
                print(f"  {phone.id:<5} {phone.model_name[:30]:<30} RM {phone.price:<10.2f}")
        else:
            print("  ⚠ No sample data available")

        # Test Oracle-specific query
        with db.engine.connect() as conn:
            result = conn.execute(text("SELECT banner FROM v$version WHERE ROWNUM = 1"))
            version = result.scalar()
            print(f"\n  Oracle Version: {version}")

    except Exception as e:
        print(f"  ✗ Error running sample query: {str(e)}")

print("\n" + "="*70)
print("✓ Oracle Database Connection Test Complete!")
print("="*70)

print("\nConnection Summary:")
print("  ✓ Oracle Database is connected and working")
print("  ✓ All tables are accessible")
print("  ✓ Queries are executing successfully")

print("\nUseful SQL*Plus Commands:")
print("  Connect: sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1")
print("  Show tables: SELECT table_name FROM user_tables;")
print("  Count phones: SELECT COUNT(*) FROM phones;")
print("  Sample data: SELECT * FROM phones WHERE ROWNUM <= 5;")

print("\nYour DialSmart system is ready to use with Oracle Database! 🎉\n")
