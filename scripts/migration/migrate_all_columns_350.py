"""
Migrate All Oracle VARCHAR2 Columns to 350 chars
One-time comprehensive migration to avoid repeated column size errors
"""
import os
import sys

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db

print("\n" + "="*70)
print("DialSmart: Migrate All Columns to 350 chars")
print("="*70)

app = create_app()

with app.app_context():
    try:
        print("\n[1/1] Setting all major VARCHAR2 columns to 350 chars...")
        db.session.execute(db.text("""
            ALTER TABLE phone_specifications MODIFY (
                screen_resolution VARCHAR2(350),
                screen_type VARCHAR2(350),
                display_type VARCHAR2(350),
                multitouch VARCHAR2(350),
                protection VARCHAR2(350),
                processor VARCHAR2(350),
                chipset VARCHAR2(350),
                cpu VARCHAR2(350),
                gpu VARCHAR2(350),
                processor_brand VARCHAR2(350),
                ram_options VARCHAR2(350),
                storage_options VARCHAR2(350),
                card_slot VARCHAR2(350),
                flash VARCHAR2(350),
                video_recording VARCHAR2(350),
                battery VARCHAR2(350),
                charging_speed VARCHAR2(350),
                fast_charging VARCHAR2(350),
                wireless_charging VARCHAR2(350),
                removable_battery VARCHAR2(350),
                sim VARCHAR2(350),
                technology VARCHAR2(350),
                network_speed VARCHAR2(350),
                wifi_standard VARCHAR2(350),
                bluetooth_version VARCHAR2(350),
                gps VARCHAR2(350),
                nfc VARCHAR2(350),
                usb VARCHAR2(350),
                audio_jack VARCHAR2(350),
                radio VARCHAR2(350),
                operating_system VARCHAR2(350),
                weight VARCHAR2(350),
                dimensions VARCHAR2(350),
                colors_available VARCHAR2(350),
                water_resistance VARCHAR2(350)
            )
        """))
        db.session.commit()
        print("  ✓ All VARCHAR2 columns updated to 350 chars")

        print("\n" + "="*70)
        print("✓ COLUMN MIGRATION COMPLETE!")
        print("="*70)

        print(f"\nAll major string columns now support up to 350 characters.")
        print(f"\nNext Step:")
        print(f"  Run: python import_csv_to_oracle.py")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error migrating columns: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
