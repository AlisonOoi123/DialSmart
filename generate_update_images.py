#!/usr/bin/env python3
"""
Generate SQL UPDATE statements to fix missing phone images
This script reads the CSV and generates SQL that can be run in SQL*Plus
"""
import csv
import sys

def escape_sql(text):
    """Escape single quotes for SQL"""
    if not text:
        return ''
    return text.replace("'", "''")

try:
    print("-- SQL Script to Update Missing Phone Images")
    print("-- Generated from fyp_phoneDataset.csv")
    print("-- Run this in SQL*Plus")
    print("")
    print("SET SERVEROUTPUT ON;")
    print("SET FEEDBACK ON;")
    print("")

    csv_file = 'fyp_phoneDataset.csv'

    with open(csv_file, 'r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        update_count = 0

        for row in reader:
            brand = row.get('Brand', '').strip()
            model = row.get('Model', '').strip()
            image_url = row.get('Image URL', '').strip()

            # Only generate UPDATE if we have all required data
            if brand and model and image_url and image_url.startswith('http'):
                # Escape single quotes
                brand_esc = escape_sql(brand)
                model_esc = escape_sql(model)
                image_esc = escape_sql(image_url)

                # Generate UPDATE statement
                # Match on brand name and model name, only update if image is missing
                print(f"""UPDATE phones p
SET p.main_image = '{image_esc}'
WHERE p.id IN (
    SELECT p2.id
    FROM phones p2
    JOIN brands b ON p2.brand_id = b.id
    WHERE UPPER(b.name) = UPPER('{brand_esc}')
      AND UPPER(p2.model_name) = UPPER('{model_esc}')
      AND (p2.main_image IS NULL OR p2.main_image = 'N/A' OR p2.main_image = '')
      AND ROWNUM = 1
);
""")
                update_count += 1

    print("COMMIT;")
    print("")
    print(f"-- Total updates attempted: {update_count}")
    print("")
    print("-- Verify the results:")
    print("SELECT b.name, COUNT(p.id) as phones_without_images")
    print("FROM phones p")
    print("JOIN brands b ON p.brand_id = b.id")
    print("WHERE (p.main_image IS NULL OR p.main_image = 'N/A' OR p.main_image = '')")
    print("GROUP BY b.name")
    print("ORDER BY phones_without_images DESC;")

except FileNotFoundError:
    print(f"Error: Could not find {csv_file}", file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"Error: {str(e)}", file=sys.stderr)
    sys.exit(1)
