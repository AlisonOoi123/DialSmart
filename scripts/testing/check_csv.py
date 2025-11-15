"""
Check CSV file structure and first few rows
"""
import csv

csv_file = 'fyp_phoneDataset.csv'

print("\n" + "="*70)
print("CSV File Diagnostic")
print("="*70)

with open(csv_file, 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)

    # Show column names
    print("\nColumn Names Found:")
    for i, col in enumerate(reader.fieldnames, 1):
        print(f"  {i}. '{col}'")

    # Show first 3 rows
    print("\nFirst 3 Rows:")
    for idx, row in enumerate(reader, 1):
        if idx <= 3:
            print(f"\nRow {idx}:")
            print(f"  Model: '{row.get('Model', 'NOT FOUND')}'")
            print(f"  Brand: '{row.get('Brand', 'NOT FOUND')}'")
            print(f"  Price: '{row.get('Price', 'NOT FOUND')}'")
        else:
            break

print("\n" + "="*70 + "\n")
