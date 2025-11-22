"""
Quick Migration Script - Add website_url to brands table
Run this script to add the website_url column to your database
"""
import sqlite3
import os

# Database path
db_path = 'dialsmart.db'

if not os.path.exists(db_path):
    print(f"Error: Database file '{db_path}' not found!")
    print("Make sure you're running this from the DialSmart project root directory.")
    exit(1)

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if column already exists
    cursor.execute("PRAGMA table_info(brands)")
    columns = [column[1] for column in cursor.fetchall()]

    if 'website_url' in columns:
        print("✓ Column 'website_url' already exists in brands table!")
    else:
        # Add the column
        cursor.execute("ALTER TABLE brands ADD COLUMN website_url VARCHAR(500)")
        conn.commit()
        print("✓ Successfully added 'website_url' column to brands table!")

    # Optional: Add sample website URLs for common brands
    print("\nWould you like to add sample website URLs for common brands? (y/n)")
    response = input().strip().lower()

    if response == 'y':
        # Sample brand websites
        brand_websites = {
            'Apple': 'https://www.apple.com',
            'Samsung': 'https://www.samsung.com',
            'Huawei': 'https://www.huawei.com',
            'XIAOMI': 'https://www.mi.com',
            'Xiaomi': 'https://www.mi.com',
            'Nokia': 'https://www.nokia.com',
            'Oppo': 'https://www.oppo.com',
            'Vivo': 'https://www.vivo.com',
            'Realme': 'https://www.realme.com',
            'realme': 'https://www.realme.com',
            'OnePlus': 'https://www.oneplus.com',
            'Google': 'https://store.google.com',
            'Motorola': 'https://www.motorola.com',
            'Sony': 'https://www.sony.com',
            'LG': 'https://www.lg.com',
            'Honor': 'https://www.hihonor.com',
            'Lenovo': 'https://www.lenovo.com',
            'Asus': 'https://www.asus.com',
            'HTC': 'https://www.htc.com',
            'BlackBerry': 'https://www.blackberry.com',
        }

        updated_count = 0
        for brand_name, website in brand_websites.items():
            cursor.execute(
                "UPDATE brands SET website_url = ? WHERE name = ? AND (website_url IS NULL OR website_url = '')",
                (website, brand_name)
            )
            if cursor.rowcount > 0:
                updated_count += cursor.rowcount
                print(f"  ✓ Updated {brand_name}: {website}")

        conn.commit()
        print(f"\n✓ Updated {updated_count} brand(s) with website URLs!")

    conn.close()
    print("\n✅ Migration completed successfully!")
    print("\nNext steps:")
    print("1. Restart your Flask application")
    print("2. Visit a phone details page to see the clickable brand name")
    print("3. Add/edit more brand URLs via the admin panel at /admin/brands")

except sqlite3.Error as e:
    print(f"❌ Database error: {e}")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)
