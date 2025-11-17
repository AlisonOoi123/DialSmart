# reimport_data.py
import pandas as pd
import oracledb  # ✅ Changed from cx_Oracle
from datetime import datetime

print("="*60)
print("RE-IMPORTING PHONE DATA TO ORACLE")
print("="*60)

# Oracle connection (using oracledb)
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
    df = pd.read_csv('fyp_phoneDataset.csv')
    print(f"✓ Found {len(df)} phones in CSV")
    print(f"✓ Columns: {list(df.columns)}")
except Exception as e:
    print(f"✗ Error reading CSV: {e}")
    exit()

# Check brands exist
print("\n🏷️ Checking brands...")
cursor.execute("SELECT id, name FROM brands")
brands = cursor.fetchall()
brand_map = {row[1].upper(): row[0] for row in brands}
print(f"✓ Found {len(brand_map)} brands in database")

if not brands:
    print("⚠️ No brands found! Creating brands first...")
    # Get unique brands from CSV
    unique_brands = df['Brand'].unique()
    for brand in unique_brands:
        brand_name = str(brand).strip()
        cursor.execute(
            "INSERT INTO brands (id, name, is_active) VALUES (brands_seq.NEXTVAL, :name, 1)",
            {'name': brand_name}
        )
        connection.commit()
    
    # Reload brand map
    cursor.execute("SELECT id, name FROM brands")
    brand_map = {row[1].upper(): row[0] for row in cursor.fetchall()}
    print(f"✓ Created {len(brand_map)} brands")

# Clear old phone data
print("\n🗑️ Clearing old phone data...")
cursor.execute("DELETE FROM phones")
connection.commit()
print("✓ Old data cleared")

# Import phones
print("\n📥 Importing phones...")
imported = 0
errors = 0

for index, row in df.iterrows():
    try:
        # Get brand
        brand_name = str(row['Brand']).strip().upper()
        if brand_name not in brand_map:
            print(f"⚠️ Unknown brand: {brand_name}, skipping...")
            errors += 1
            continue
        
        brand_id = brand_map[brand_name]
        
        # Clean price
        price_str = str(row.get('Price', '0'))
        price_str = price_str.replace('MYR', '').replace('RM', '').replace(',', '').strip()
        try:
            price = float(price_str) if price_str else 0.0
        except:
            price = 0.0
        
        # Get model name
        model_name = str(row.get('Model', 'Unknown'))[:150]
        
        # Get image URL
        image_url = str(row.get('ImageURL', ''))[:255] if pd.notna(row.get('ImageURL')) else None
        
        # Get status
        status = str(row.get('Status', 'Available'))[:50] if pd.notna(row.get('Status')) else 'Available'
        status = status.strip()
        
        # Parse release date
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
        
        imported += 1
        
        # Commit every 50 records
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

# Verify import
print(f"\n📊 Verification:")
cursor.execute("SELECT COUNT(*) FROM phones")
total = cursor.fetchone()[0]
print(f"   Total phones in database: {total}")

cursor.execute("""
    SELECT b.name, COUNT(p.id) as cnt
    FROM brands b
    LEFT JOIN phones p ON b.id = p.brand_id
    GROUP BY b.name
    ORDER BY cnt DESC
""")

print(f"\n📱 Phones by brand:")
for brand, count in cursor.fetchall():
    print(f"   {brand}: {count} phones")

# Close connection
cursor.close()
connection.close()

print(f"\n✓ Done! Refresh your website to see phones.")
print(f"  Open: http://localhost:5000/browse")