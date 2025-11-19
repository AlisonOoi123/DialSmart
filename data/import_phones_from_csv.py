# import_phones_from_csv.py
import pandas as pd
import oracledb
from datetime import datetime

print("="*60)
print("IMPORTING PHONES WITH FULL SPECIFICATIONS")
print("="*60)

# Oracle connection
try:
    connection = oracledb.connect(
        user='ds_user',
        password='dsuser123',
        host='localhost',
        port=1521,
        service_name='orclpdb'
    )
    cursor = connection.cursor()
    print("✓ Connected to Oracle")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    exit()

# Read CSV
print("\n📂 Reading CSV file...")
try:
    df = pd.read_csv('data/fyp_phoneDataset.csv')
    print(f"✓ Found {len(df)} phones in CSV")
except Exception as e:
    print(f"✗ Error reading CSV: {e}")
    exit()

# Check brands
print("\n🏷️ Checking brands...")
cursor.execute("SELECT id, name FROM brands")
brands = cursor.fetchall()
brand_map = {row[1].upper(): row[0] for row in brands}
print(f"✓ Found {len(brand_map)} brands")

# Clear old data
print("\n🗑️ Clearing old data...")
cursor.execute("DELETE FROM phone_specifications")
cursor.execute("DELETE FROM phones")
connection.commit()
print("✓ Cleared")

# Import phones
print("\n📥 Importing phones...")
imported = 0
errors = 0

for index, row in df.iterrows():
    try:
        # Get brand
        brand_name = str(row['Brand']).strip().upper()
        if brand_name not in brand_map:
            errors += 1
            continue
        
        brand_id = brand_map[brand_name]
        
        # Clean price
        price_str = str(row.get('Price', '0')).replace('MYR', '').replace('RM', '').replace(',', '').strip()
        try:
            price = float(price_str) if price_str else 0.0
        except:
            price = 0.0
        
        model_name = str(row.get('Model', 'Unknown'))[:150]
        image_url = str(row.get('ImageURL', ''))[:500] if pd.notna(row.get('ImageURL')) else None
        status = str(row.get('Status', 'Available'))[:50]
        
        try:
            release_date = pd.to_datetime(row.get('Date')).date() if pd.notna(row.get('Date')) else None
        except:
            release_date = None
        
        # Insert phone
        cursor.execute("""
            INSERT INTO phones (
                id, brand_id, model_name, price, main_image,
                release_date, availability_status, is_active, created_at
            ) VALUES (
                phones_seq.NEXTVAL, :brand_id, :model, :price, :image,
                :release_date, :status, 1, SYSDATE
            )
        """, {
            'brand_id': brand_id,
            'model': model_name,
            'price': price,
            'image': image_url,
            'release_date': release_date,
            'status': status
        })
        
        # Get phone_id
        cursor.execute("SELECT phones_seq.CURRVAL FROM dual")
        phone_id = cursor.fetchone()[0]
        
        # Helper function to safely get string value
        def get_str(col, max_len=None):
            val = row.get(col)
            if pd.isna(val):
                return None
            val_str = str(val).strip()
            if max_len and len(val_str) > max_len:
                return val_str[:max_len]
            return val_str if val_str else None
        
        # Helper to extract numeric values
        def extract_number(text):
            if pd.isna(text):
                return None
            import re
            match = re.search(r'(\d+(?:\.\d+)?)', str(text))
            return float(match.group(1)) if match else None
        
        # Insert specifications - matching YOUR database columns
        cursor.execute("""
            INSERT INTO phone_specifications (
                id, phone_id,
                screen_size, screen_resolution, screen_type, display_type,
                ppi, multitouch, protection,
                processor, chipset, cpu, gpu,
                ram_options, storage_options, card_slot,
                rear_camera, front_camera, camera_features,
                flash, video_recording,
                battery_capacity, battery, charging_speed, fast_charging, wireless_charging, removable_battery,
                sim, technology,
                network_5g, network_4g, network_3g, network_2g, network_speed,
                wifi_standard, bluetooth_version, gps, nfc, usb, audio_jack, radio,
                operating_system,
                weight, dimensions, colors_available, body_material,
                sensors, product_url
            ) VALUES (
                phone_specifications_seq.NEXTVAL, :phone_id,
                :screen_size, :screen_resolution, :screen_type, :display_type,
                :ppi, :multitouch, :protection,
                :processor, :chipset, :cpu, :gpu,
                :ram_options, :storage_options, :card_slot,
                :rear_camera, :front_camera, :camera_features,
                :flash, :video_recording,
                :battery_capacity, :battery, :charging_speed, :fast_charging, :wireless_charging, :removable_battery,
                :sim, :technology,
                :network_5g, :network_4g, :network_3g, :network_2g, :network_speed,
                :wifi_standard, :bluetooth_version, :gps, :nfc, :usb, :audio_jack, :radio,
                :operating_system,
                :weight, :dimensions, :colors_available, :body_material,
                :sensors, :product_url
            )
        """, {
            'phone_id': phone_id,
            # Display
            'screen_size': extract_number(row.get('ScreenSize')),
            'screen_resolution': get_str('Resolution', 350),
            'screen_type': get_str('DisplayType', 350),
            'display_type': get_str('DisplayType', 350),
            'ppi': extract_number(row.get('PPI')),
            'multitouch': get_str('Multi-touch', 350),
            'protection': get_str('Protection', 350),
            # Performance
            'processor': get_str('Chipset', 350),
            'chipset': get_str('Chipset', 350),
            'cpu': get_str('CPU', 350),
            'gpu': get_str('GPU', 350),
            # Memory
            'ram_options': get_str('RAM', 350),
            'storage_options': get_str('Storage', 350),
            'card_slot': get_str('Card Slot', 350),
            # Camera
            'rear_camera': get_str('RearCamera', 500),
            'front_camera': get_str('FrontCamera', 200),
            'camera_features': get_str('Camera Features', 4000),  # CLOB
            'flash': get_str('Flash', 350),
            'video_recording': get_str('VideoRecording', 350),
            # Battery
            'battery_capacity': extract_number(row.get('BatteryCapacity')),
            'battery': get_str('Battery', 350),
            'charging_speed': get_str('FastCharging', 350),
            'fast_charging': get_str('FastCharging', 350),
            'wireless_charging': get_str('WirelessCharging', 350),
            'removable_battery': get_str('RemovableBattery', 350),
            # Network
            'sim': get_str('SIM', 350),
            'technology': get_str('Technology', 350),
            'network_5g': get_str('5GNetworks', 500),
            'network_4g': get_str('4GNetworks', 500),
            'network_3g': get_str('3GNetworks', 300),
            'network_2g': get_str('2GNetworks', 300),
            'network_speed': get_str('NetworkSpeed', 350),
            # Connectivity
            'wifi_standard': get_str('Wi-Fi', 350),
            'bluetooth_version': get_str('Bluetooth', 350),
            'gps': get_str('GPS', 350),
            'nfc': get_str('NFC', 350),
            'usb': get_str('USB', 350),
            'audio_jack': None,  # Not in CSV
            'radio': get_str('Radio', 350),
            # Software
            'operating_system': get_str('OS', 350),
            # Physical
            'weight': get_str('Weight', 350),
            'dimensions': get_str('Dimensions', 350),
            'colors_available': get_str('Color', 350),
            'body_material': get_str('BodyMaterial', 300),
            # Other
            'sensors': get_str('Sensors', 4000),  # CLOB
            'product_url': get_str('URL', 500)
        })
        
        imported += 1
        
        if imported % 50 == 0:
            connection.commit()
            print(f"  ... {imported} phones imported")
        
    except Exception as e:
        errors += 1
        print(f"✗ Error importing {row.get('Model', 'Unknown')}: {str(e)}")
        continue

# Final commit
connection.commit()

print(f"\n{'='*60}")
print(f"✅ IMPORT COMPLETE!")
print(f"{'='*60}")
print(f"   Imported: {imported} phones")
print(f"   Errors: {errors}")
print(f"{'='*60}")

# Verify
cursor.execute("SELECT COUNT(*) FROM phones")
print(f"\n📊 Total phones: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM phone_specifications")
print(f"📊 Total specs: {cursor.fetchone()[0]}")

# Sample
cursor.execute("""
    SELECT p.model_name, ps.ram_options, ps.battery_capacity
    FROM phones p
    LEFT JOIN phone_specifications ps ON p.id = ps.phone_id
    WHERE ROWNUM <= 3
""")
print(f"\n📱 Sample:")
for row in cursor.fetchall():
    print(f"   {row[0]} - RAM: {row[1]} - Battery: {row[2]}")

cursor.close()
connection.close()

print(f"\n✓ Done! Check your website at http://localhost:5000/browse")