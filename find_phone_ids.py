"""
Find Phone IDs by Brand Name
Quick script to query phone IDs for specific brands
"""
import os
import sys

# Set DB_TYPE if using Oracle (comment out if using SQLite)
# os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import Phone, Brand

# List of brands to search for
BRANDS_TO_FIND = [
    'Google', 'Honor', 'Huawei', 'Infinix', 'Oppo', 'Poco',
    'Realme', 'Redmi', 'Samsung', 'Vivo', 'Xiaomi', 'Apple', 'Asus'
]

def find_phones_by_brands():
    """Find all phone IDs for specified brands"""
    app = create_app()

    with app.app_context():
        print("\n" + "="*80)
        print("PHONE IDs BY BRAND")
        print("="*80 + "\n")

        total_phones = 0
        found_brands = 0

        for brand_name in BRANDS_TO_FIND:
            # Search for brand (case-insensitive)
            brand = Brand.query.filter(Brand.name.ilike(f'%{brand_name}%')).first()

            if brand:
                found_brands += 1
                phones = Phone.query.filter_by(brand_id=brand.id).all()

                print(f"📱 {brand.name} (Brand ID: {brand.id})")
                print(f"   Total Phones: {len(phones)}")
                print(f"   {'─'*76}")

                if phones:
                    for phone in phones:
                        status_icon = "✓" if phone.is_active else "✗"
                        print(f"   {status_icon} Phone ID: {phone.id:4d} | {phone.model_name:50s} | MYR {phone.price:,.2f}")
                    total_phones += len(phones)
                else:
                    print(f"   (No phones found for this brand)")

                print()
            else:
                print(f"❌ {brand_name}: Brand not found in database\n")

        print("="*80)
        print(f"Summary: Found {found_brands}/{len(BRANDS_TO_FIND)} brands with {total_phones} total phones")
        print("="*80 + "\n")

def export_to_csv():
    """Export phone IDs to CSV file"""
    import csv

    app = create_app()

    with app.app_context():
        with open('phone_ids_by_brand.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Brand Name', 'Brand ID', 'Phone ID', 'Model Name', 'Price', 'Is Active'])

            for brand_name in BRANDS_TO_FIND:
                brand = Brand.query.filter(Brand.name.ilike(f'%{brand_name}%')).first()

                if brand:
                    phones = Phone.query.filter_by(brand_id=brand.id).all()
                    for phone in phones:
                        writer.writerow([
                            brand.name,
                            brand.id,
                            phone.id,
                            phone.model_name,
                            phone.price,
                            phone.is_active
                        ])

        print("✓ Exported to phone_ids_by_brand.csv")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--csv':
        export_to_csv()
    else:
        find_phones_by_brands()
        print("\nTip: Run with '--csv' flag to export to CSV file")
        print("     python find_phone_ids.py --csv\n")
