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

if not brands:
    print("⚠️ Creating brands...")
    unique_brands = df['Brand'].unique()
    for brand in unique_brands:
        brand_name = str(brand).strip()
        cursor.execute(
            "INSERT INTO brands (id, name, is_active) VALUES (brands_seq.NEXTVAL, :name, 1)",
            {'name': brand_name}
        )
    connection.commit()
    cursor.execute("SELECT id, name FROM brands")
    brand_map = {row[1].upper(): row[0] for row in cursor.fetchall()}
    print(f"✓ Created {len(brand_map)} brands")

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
        
        # Insert phone - Use sequence to get ID
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
        
        # Get the phone_id that was just inserted
        cursor.execute("SELECT phones_seq.CURRVAL FROM dual")
        phone_id = cursor.fetchone()[0]
        
        # Insert specifications
        cursor.execute("""
            INSERT INTO phone_specifications (
                id, phone_id, 
                dimensions, weight, colors, body_material,
                screen_size, display_type, resolution, ppi,
                network_technology, os, chipset, cpu, gpu,
                ram_options, storage_options, card_slot,
                rear_camera, front_camera, camera_features, video_recording,
                battery_capacity, fast_charging, wireless_charging,
                wifi, bluetooth, gps, nfc, usb_type, radio,
                sensors, product_url
            ) VALUES (
                phone_specifications_seq.NEXTVAL, :phone_id,
                :dimensions, :weight, :colors, :body_material,
                :screen_size, :display_type, :resolution, :ppi,
                :technology, :os, :chipset, :cpu, :gpu,
                :ram, :storage, :card_slot,
                :rear_camera, :front_camera, :camera_features, :video,
                :battery, :fast_charging, :wireless_charging,
                :wifi, :bluetooth, :gps, :nfc, :usb, :radio,
                :sensors, :url
            )
        """, {
            'phone_id': phone_id,
            'dimensions': str(row.get('Dimensions', ''))[:100] if pd.notna(row.get('Dimensions')) else None,
            'weight': str(row.get('Weight', ''))[:50] if pd.notna(row.get('Weight')) else None,
            'colors': str(row.get('Color', ''))[:200] if pd.notna(row.get('Color')) else None,
            'body_material': str(row.get('BodyMaterial', ''))[:200] if pd.notna(row.get('BodyMaterial')) else None,
            'screen_size': str(row.get('ScreenSize', ''))[:50] if pd.notna(row.get('ScreenSize')) else None,
            'display_type': str(row.get('DisplayType', ''))[:200] if pd.notna(row.get('DisplayType')) else None,
            'resolution': str(row.get('Resolution', ''))[:100] if pd.notna(row.get('Resolution')) else None,
            'ppi': str(row.get('PPI', ''))[:50] if pd.notna(row.get('PPI')) else None,
            'technology': str(row.get('Technology', ''))[:200] if pd.notna(row.get('Technology')) else None,
            'os': str(row.get('OS', ''))[:100] if pd.notna(row.get('OS')) else None,
            'chipset': str(row.get('Chipset', ''))[:100] if pd.notna(row.get('Chipset')) else None,
            'cpu': str(row.get('CPU', ''))[:200] if pd.notna(row.get('CPU')) else None,
            'gpu': str(row.get('GPU', ''))[:100] if pd.notna(row.get('GPU')) else None,
            'ram': str(row.get('RAM', ''))[:100] if pd.notna(row.get('RAM')) else None,
            'storage': str(row.get('Storage', ''))[:200] if pd.notna(row.get('Storage')) else None,
            'card_slot': str(row.get('Card Slot', ''))[:100] if pd.notna(row.get('Card Slot')) else None,
            'rear_camera': str(row.get('RearCamera', ''))[:500] if pd.notna(row.get('RearCamera')) else None,
            'front_camera': str(row.get('FrontCamera', ''))[:200] if pd.notna(row.get('FrontCamera')) else None,
            'camera_features': str(row.get('Camera Features', ''))[:300] if pd.notna(row.get('Camera Features')) else None,
            'video': str(row.get('VideoRecording', ''))[:300] if pd.notna(row.get('VideoRecording')) else None,
            'battery': str(row.get('BatteryCapacity', ''))[:50] if pd.notna(row.get('BatteryCapacity')) else None,
            'fast_charging': str(row.get('FastCharging', ''))[:200] if pd.notna(row.get('FastCharging')) else None,
            'wireless_charging': str(row.get('WirelessCharging', ''))[:100] if pd.notna(row.get('WirelessCharging')) else None,
            'wifi': str(row.get('Wi-Fi', ''))[:100] if pd.notna(row.get('Wi-Fi')) else None,
            'bluetooth': str(row.get('Bluetooth', ''))[:50] if pd.notna(row.get('Bluetooth')) else None,
            'gps': str(row.get('GPS', ''))[:100] if pd.notna(row.get('GPS')) else None,
            'nfc': str(row.get('NFC', ''))[:50] if pd.notna(row.get('NFC')) else None,
            'usb': str(row.get('USB', ''))[:100] if pd.notna(row.get('USB')) else None,
            'radio': str(row.get('Radio', ''))[:50] if pd.notna(row.get('Radio')) else None,
            'sensors': str(row.get('Sensors', ''))[:300] if pd.notna(row.get('Sensors')) else None,
            'url': str(row.get('URL', ''))[:500] if pd.notna(row.get('URL')) else None
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