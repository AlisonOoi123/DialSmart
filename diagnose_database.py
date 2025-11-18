"""
Database Diagnostic Script
Checks if phone data and relationships are properly set up
"""
import oracledb
from getpass import getpass

print("=" * 70)
print("DialSmart Database Diagnostic")
print("=" * 70)
print()

# Get Oracle connection details
print("Enter Oracle Database Connection Details:")
username = input("Username (default: ds_user): ").strip() or "ds_user"
password = getpass("Password: ")
host = input("Host (default: localhost): ").strip() or "localhost"
port = input("Port (default: 1521): ").strip() or "1521"
service_name = input("Service Name (default: orclpdb): ").strip() or "orclpdb"

dsn = f"{host}:{port}/{service_name}"

try:
    # Connect to Oracle
    print(f"\nConnecting to Oracle at {host}:{port}/{service_name}...")
    connection = oracledb.connect(user=username, password=password, dsn=dsn)
    cursor = connection.cursor()
    print("✅ Connected successfully!")
    print()

    # Check phones table
    print("📱 Checking PHONES table...")
    cursor.execute("SELECT COUNT(*) FROM phones")
    phone_count = cursor.fetchone()[0]
    print(f"   Total phones: {phone_count}")

    if phone_count > 0:
        # Check a sample phone
        cursor.execute("""
            SELECT id, brand_id, model_name, price, main_image, is_active
            FROM phones
            WHERE ROWNUM <= 3
            ORDER BY id
        """)
        print("\n   Sample phones:")
        for row in cursor.fetchall():
            phone_id, brand_id, model_name, price, main_image, is_active = row
            print(f"   - ID: {phone_id}, Name: {model_name}")
            print(f"     Brand ID: {brand_id}, Price: RM{price}")
            print(f"     Image: {main_image if main_image else 'NULL (missing!)'}")
            print(f"     Active: {is_active}")
            print()

    # Check phone_specifications table
    print("🔧 Checking PHONE_SPECIFICATIONS table...")
    cursor.execute("SELECT COUNT(*) FROM phone_specifications")
    spec_count = cursor.fetchone()[0]
    print(f"   Total specifications: {spec_count}")

    if spec_count > 0:
        # Check if specs are linked to phones
        cursor.execute("""
            SELECT ps.id, ps.phone_id, p.model_name,
                   ps.ram_options, ps.storage_options,
                   ps.rear_camera_main, ps.battery_capacity
            FROM phone_specifications ps
            LEFT JOIN phones p ON ps.phone_id = p.id
            WHERE ROWNUM <= 3
            ORDER BY ps.id
        """)
        print("\n   Sample specifications:")
        for row in cursor.fetchall():
            spec_id, phone_id, model_name, ram, storage, camera, battery = row
            print(f"   - Spec ID: {spec_id}, Phone ID: {phone_id}")
            print(f"     Phone: {model_name if model_name else 'NOT LINKED!'}")
            print(f"     RAM: {ram}, Storage: {storage}")
            print(f"     Camera: {camera}MP, Battery: {battery}mAh")
            print()

    # Check for orphaned specs
    cursor.execute("""
        SELECT COUNT(*)
        FROM phone_specifications ps
        LEFT JOIN phones p ON ps.phone_id = p.id
        WHERE p.id IS NULL
    """)
    orphaned = cursor.fetchone()[0]
    if orphaned > 0:
        print(f"   ⚠️  WARNING: {orphaned} specifications not linked to any phone!")

    # Check for phones without specs
    cursor.execute("""
        SELECT COUNT(*)
        FROM phones p
        LEFT JOIN phone_specifications ps ON p.id = ps.phone_id
        WHERE ps.id IS NULL AND p.is_active = 1
    """)
    no_specs = cursor.fetchone()[0]
    if no_specs > 0:
        print(f"   ⚠️  WARNING: {no_specs} active phones have no specifications!")

    # Check brands table
    print("\n🏷️  Checking BRANDS table...")
    cursor.execute("SELECT COUNT(*) FROM brands")
    brand_count = cursor.fetchone()[0]
    print(f"   Total brands: {brand_count}")

    if brand_count > 0:
        cursor.execute("""
            SELECT id, name, is_active
            FROM brands
            WHERE ROWNUM <= 5
            ORDER BY name
        """)
        print("\n   Sample brands:")
        for row in cursor.fetchall():
            brand_id, brand_name, is_active = row
            print(f"   - ID: {brand_id}, Name: {brand_name}, Active: {is_active}")

    # Check recommendations table
    print("\n💡 Checking RECOMMENDATIONS table...")
    cursor.execute("SELECT COUNT(*) FROM recommendations")
    rec_count = cursor.fetchone()[0]
    print(f"   Total recommendations: {rec_count}")

    # Summary
    print()
    print("=" * 70)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 70)
    print(f"✅ Phones: {phone_count}")
    print(f"✅ Specifications: {spec_count}")
    print(f"✅ Brands: {brand_count}")
    print(f"✅ Recommendations: {rec_count}")

    if phone_count == 0:
        print("\n❌ ISSUE: No phones in database!")
        print("   You need to import phone data.")
    elif spec_count == 0:
        print("\n❌ ISSUE: No specifications in database!")
        print("   Phone specs are missing - that's why details don't show!")
    elif no_specs > 0:
        print(f"\n⚠️  ISSUE: {no_specs} phones missing specifications!")
        print("   Some phones won't show full details.")

    print()

    cursor.close()
    connection.close()

except oracledb.Error as e:
    print(f"\n❌ Oracle Error: {e}")
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
