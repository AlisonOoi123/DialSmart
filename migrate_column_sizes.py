"""
Migrate Oracle Database Column Sizes
Increases column sizes for new dataset with longer text values
"""
import os
import sys

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db

print("\n" + "="*70)
print("DialSmart: Migrate Column Sizes for Oracle")
print("="*70)

app = create_app()

with app.app_context():
    try:
        print("\n[1/5] Increasing SIM column size (150 -> 300)...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (sim VARCHAR2(300))
        """))
        db.session.commit()
        print("  ✓ SIM column updated")

        print("\n[2/5] Increasing technology column size (100 -> 200)...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (technology VARCHAR2(200))
        """))
        db.session.commit()
        print("  ✓ Technology column updated")

        print("\n[3/5] Increasing network columns size...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (
                network_5g VARCHAR2(500),
                network_4g VARCHAR2(500),
                network_3g VARCHAR2(300),
                network_2g VARCHAR2(300)
            )
        """))
        db.session.commit()
        print("  ✓ Network columns updated")

        print("\n[4/5] Increasing network_speed column size (100 -> 200)...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (network_speed VARCHAR2(200))
        """))
        db.session.commit()
        print("  ✓ Network speed column updated")

        print("\n[5/5] Increasing WiFi and Bluetooth columns...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (
                wifi_standard VARCHAR2(200),
                bluetooth_version VARCHAR2(100)
            )
        """))
        db.session.commit()
        print("  ✓ WiFi and Bluetooth columns updated")

        print("\n" + "="*70)
        print("✓ COLUMN MIGRATION COMPLETE!")
        print("="*70)

        print(f"\nDatabase schema updated successfully.")
        print(f"\nNext Step:")
        print(f"  Run: python import_csv_to_oracle.py")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error migrating columns: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
