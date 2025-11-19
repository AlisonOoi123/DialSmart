"""
DialSmart: Phone Data Import Script
Matches YOUR exact database structure (12 tables)
Date: 2025-11-19
"""

import pandas as pd
import oracledb
import re

print("="*80)
print("DialSmart: Importing 692 Phones from CSV")
print("="*80)

# ============================================================================
# 1. CONNECT TO DATABASE
# ============================================================================
print("\n[1/5] Connecting to Oracle...")
try:
    connection = oracledb.connect(
        user='ds_user',
        password='dsuser123',
        host='localhost',
        port=1521,
        service_name='orclpdb'
    )
    cursor = connection.cursor()
    print("✓ Connected successfully")
except Exception as e:
    print(f"✗ Failed: {e}")
    exit(1)

# ============================================================================
# 2. READ CSV
# ============================================================================
print("\n[2/5] Reading CSV...")
try:
    df = pd.read_csv('data/fyp_phoneDataset.csv')
    print(f"✓ Found {len(df)} phones")
except Exception as e:
    print(f"✗ Failed: {e}")
    exit(1)

# ============================================================================
# 3. GET BRANDS
# ============================================================================
print("\n[3/5] Loading brands...")
cursor.execute("SELECT id, name FROM brands")
brand_map = {row[1].upper(): row[0] for row in cursor.fetchall()}
print(f"✓ Found {len(brand_map)} brands")

# ============================================================================
# 4. CLEAR OLD DATA
# ============================================================================
print("\n[4/5] Clearing old data...")
cursor.execute("DELETE FROM phone_specifications")
cursor.execute("DELETE FROM phones")
connection.commit()
print("✓ Cleared")

# ============================================================================
# 5. IMPORT
# ============================================================================
print("\n[5/5] Importing phones...")

def safe_str(val, max_len=None):
    if pd.isna(val): return None
    s = str(val).strip()
    return s[:max_len] if max_len and len(s) > max_len else s if s else None

def safe_num(val):
    if pd.isna(val): return None
    m = re.search(r'(\d+(?:\.\d+)?)', str(val))
    return float(m.group(1)) if m else None

imported = 0
errors = 0

for idx, row in df.iterrows():
    try:
        brand = str(row.get('Brand', '')).strip().upper()
        if brand not in brand_map:
            errors += 1
            continue
        
        # Parse price (YOUR database uses FLOAT, not NUMBER(10,2))
        price_str = str(row.get('Price', '0')).replace('MYR','').replace('RM','').replace(',','').strip()
        price = float(price_str) if price_str and price_str != 'nan' else 0.0
        
        model = safe_str(row.get('Model', 'Unknown'), 150) or 'Unknown'
        
        # Insert phone
        cursor.execute("""
            INSERT INTO phones (
                id, brand_id, model_name, price, main_image,
                release_date, availability_status, is_active, created_at
            ) VALUES (
                phones_seq.NEXTVAL, :brand, :model, :price, :img,
                :date, :status, 1, SYSDATE
            )
        """, {
            'brand': brand_map[brand],
            'model': model,
            'price': price,
            'img': safe_str(row.get('ImageURL'), 255),
            'date': pd.to_datetime(row.get('Date')).date() if pd.notna(row.get('Date')) else None,
            'status': safe_str(row.get('Status', 'Available'), 50) or 'Available'
        })
        
        # Get phone ID
        cursor.execute("SELECT phones_seq.CURRVAL FROM dual")
        phone_id = cursor.fetchone()[0]
        
        # Insert specifications
        cursor.execute("""
            INSERT INTO phone_specifications (
                id, phone_id, screen_size, screen_resolution, display_type,
                ppi, multitouch, protection, chipset, cpu, gpu,
                ram_options, storage_options, card_slot,
                rear_camera, front_camera, camera_features, flash, video_recording,
                battery_capacity, battery, fast_charging, wireless_charging,
                removable_battery, sim, technology,
                network_5g, network_4g, network_3g, network_2g, network_speed,
                wifi_standard, bluetooth_version, gps, nfc, usb, radio,
                operating_system, weight, dimensions, colors_available,
                body_material, sensors, product_url
            ) VALUES (
                phone_specifications_seq.NEXTVAL, :phone_id,
                :screen_size, :resolution, :display, :ppi, :touch, :protect,
                :chip, :cpu, :gpu, :ram, :storage, :card,
                :rcam, :fcam, :camfeat, :flash, :video,
                :batcap, :bat, :fast, :wireless, :removable,
                :sim, :tech, :net5g, :net4g, :net3g, :net2g, :speed,
                :wifi, :bt, :gps, :nfc, :usb, :radio,
                :os, :weight, :dim, :color, :material, :sensors, :url
            )
        """, {
            'phone_id': phone_id,
            'screen_size': safe_num(row.get('ScreenSize')),
            'resolution': safe_str(row.get('Resolution'), 350),
            'display': safe_str(row.get('DisplayType'), 350),
            'ppi': safe_num(row.get('PPI')),
            'touch': safe_str(row.get('Multi-touch'), 350),
            'protect': safe_str(row.get('Protection'), 350),
            'chip': safe_str(row.get('Chipset'), 350),
            'cpu': safe_str(row.get('CPU'), 350),
            'gpu': safe_str(row.get('GPU'), 350),
            'ram': safe_str(row.get('RAM'), 350),
            'storage': safe_str(row.get('Storage'), 350),
            'card': safe_str(row.get('Card Slot'), 350),
            'rcam': safe_str(row.get('RearCamera'), 500),
            'fcam': safe_str(row.get('FrontCamera'), 200),
            'camfeat': safe_str(row.get('Camera Features'), 4000),
            'flash': safe_str(row.get('Flash'), 350),
            'video': safe_str(row.get('VideoRecording'), 350),
            'batcap': safe_num(row.get('BatteryCapacity')),
            'bat': safe_str(row.get('Battery'), 350),
            'fast': safe_str(row.get('FastCharging'), 350),
            'wireless': safe_str(row.get('WirelessCharging'), 350),
            'removable': safe_str(row.get('RemovableBattery'), 350),
            'sim': safe_str(row.get('SIM'), 350),
            'tech': safe_str(row.get('Technology'), 350),
            'net5g': safe_str(row.get('5GNetworks'), 500),
            'net4g': safe_str(row.get('4GNetworks'), 500),
            'net3g': safe_str(row.get('3GNetworks'), 300),
            'net2g': safe_str(row.get('2GNetworks'), 300),
            'speed': safe_str(row.get('NetworkSpeed'), 350),
            'wifi': safe_str(row.get('Wi-Fi'), 350),
            'bt': safe_str(row.get('Bluetooth'), 350),
            'gps': safe_str(row.get('GPS'), 350),
            'nfc': safe_str(row.get('NFC'), 350),
            'usb': safe_str(row.get('USB'), 350),
            'radio': safe_str(row.get('Radio'), 350),
            'os': safe_str(row.get('OS'), 350),
            'weight': safe_str(row.get('Weight'), 350),
            'dim': safe_str(row.get('Dimensions'), 350),
            'color': safe_str(row.get('Color'), 350),
            'material': safe_str(row.get('BodyMaterial'), 300),
            'sensors': safe_str(row.get('Sensors'), 4000),
            'url': safe_str(row.get('URL'), 500)
        })
        
        imported += 1
        if imported % 50 == 0:
            connection.commit()
            print(f"  ✓ {imported} phones...")
            
    except Exception as e:
        errors += 1
        if errors <= 3:
            print(f"  ✗ Error: {row.get('Model', 'Unknown')}: {e}")

connection.commit()

# Verify
cursor.execute("SELECT COUNT(*) FROM phones")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM phone_specifications")
specs = cursor.fetchone()[0]

print("\n" + "="*80)
print(f"✅ COMPLETE!")
print("="*80)
print(f"Imported: {imported}")
print(f"Errors: {errors}")
print(f"Database phones: {total}")
print(f"Database specs: {specs}")
print("="*80)

# Sample
print("\n📱 Sample phones:")
cursor.execute("""
    SELECT p.model_name, b.name, p.price, ps.ram_options
    FROM phones p
    JOIN brands b ON p.brand_id = b.id
    LEFT JOIN phone_specifications ps ON p.id = ps.phone_id
    WHERE ROWNUM <= 5
""")
for r in cursor.fetchall():
    print(f"  • {r[0]} ({r[1]}) - RM{r[2]:.0f} - {r[3] or 'N/A'}")

cursor.close()
connection.close()

print("\n✓ Done! Start Flask: python run.py")
print("="*80)