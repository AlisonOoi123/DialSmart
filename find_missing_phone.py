"""
Find which phone from CSV is missing in Oracle database
"""
import csv
import sys
from app import create_app, db
from app.models import Phone, Brand

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("Checking for missing phones...")
    print("="*70)

    # Read CSV
    csv_file = 'fyp_phoneDataset.csv'
    csv_phones = []

    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            brand_name = row.get('Brand', '').strip()
            model_name = row.get('Model', '').strip()
            if brand_name and model_name:
                csv_phones.append({
                    'brand': brand_name,
                    'model': model_name,
                    'price': row.get('Price', '')
                })

    print(f"\nCSV has {len(csv_phones)} phones")
    print(f"Database has {Phone.query.count()} phones")

    # Find missing phones
    missing = []
    for phone_data in csv_phones:
        brand = Brand.query.filter_by(name=phone_data['brand']).first()
        if not brand:
            missing.append(phone_data)
            continue

        phone = Phone.query.filter_by(
            brand_id=brand.id,
            model_name=phone_data['model']
        ).first()

        if not phone:
            missing.append(phone_data)

    if missing:
        print(f"\n⚠ Found {len(missing)} missing phone(s):")
        for phone in missing:
            print(f"  • {phone['brand']} {phone['model']} - {phone['price']}")
    else:
        print("\n✓ All phones from CSV are in the database!")

    print("\n" + "="*70)
