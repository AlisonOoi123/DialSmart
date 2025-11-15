"""
Fix Missing Phone Images
Updates phones in database with image URLs from CSV file
"""
import os
import sys
import csv

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import Brand, Phone

print("\n" + "="*70)
print("DialSmart: Fix Missing Phone Images from CSV")
print("="*70)

app = create_app()

with app.app_context():
    try:
        # Path to CSV file
        csv_file = 'fyp_phoneDataset.csv'

        if not os.path.exists(csv_file):
            print(f"\n✗ Error: CSV file '{csv_file}' not found!")
            sys.exit(1)

        print(f"\n[1/3] Reading CSV file: {csv_file}")

        # Read CSV and build a mapping of (brand, model) -> image_url
        image_mapping = {}
        with open(csv_file, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            for row in reader:
                brand_name = row.get('Brand', '').strip()
                model_name = row.get('Model', '').strip()
                image_url = row.get('Image URL', '').strip()

                if brand_name and model_name and image_url and image_url.startswith('http'):
                    key = (brand_name, model_name)
                    image_mapping[key] = image_url

        print(f"  ✓ Found {len(image_mapping)} phones with image URLs in CSV")

        print(f"\n[2/3] Checking database for phones with missing images...")

        # Find all phones with NULL or 'N/A' images
        phones_missing_images = Phone.query.filter(
            db.or_(
                Phone.main_image.is_(None),
                Phone.main_image == '',
                Phone.main_image == 'N/A'
            )
        ).all()

        print(f"  ✓ Found {len(phones_missing_images)} phones with missing images")

        print(f"\n[3/3] Updating phone images...")
        updated_count = 0
        not_found_count = 0

        for phone in phones_missing_images:
            brand = Brand.query.get(phone.brand_id)
            if not brand:
                continue

            # Look up image URL from CSV mapping
            key = (brand.name, phone.model_name)
            if key in image_mapping:
                phone.main_image = image_mapping[key]
                updated_count += 1
                if updated_count <= 10:  # Show first 10 updates
                    print(f"  ✓ Updated: {brand.name} {phone.model_name}")
            else:
                not_found_count += 1
                if not_found_count <= 5:  # Show first 5 not found
                    print(f"  ⚠ Not found in CSV: {brand.name} {phone.model_name}")

        # Commit all updates
        db.session.commit()

        print(f"\n{'='*70}")
        print(f"✓ Successfully updated {updated_count} phone images")
        if not_found_count > 0:
            print(f"⚠ {not_found_count} phones not found in CSV (may have different model names)")
        print(f"{'='*70}\n")

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
