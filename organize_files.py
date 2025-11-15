#!/usr/bin/env python3
"""
Organize DialSmart Files
Moves files into organized folder structure
"""
import os
import shutil
from pathlib import Path

# Define the organization plan
ORGANIZATION_PLAN = {
    'docs/': [
        'CSV_DATASET_GUIDE.md',
        'FIXES_SUMMARY.md',
        'ORACLE_SETUP_GUIDE.md',
        'README_IMAGE_FIX.md',
        'SETUP_GUIDE.md',
    ],
    'data/': [
        'fyp_phoneDataset.csv',
    ],
    'sql/': [
        'setup_oracle_sequences.sql',
        'setup_oracle_user.sql',
        'update_oracle_columns.sql',
        'update_phone_images.sql',
    ],
    'scripts/database/': [
        'check_oracle_service.py',
        'clear_phone_data.py',
        'init_database.py',
        'initialize_oracle.py',
        'initialize_system.py',
    ],
    'scripts/import/': [
        'import_csv_dataset.py',
        'import_csv_to_oracle.py',
        'fix_missing_images.py',
        'generate_update_images.py',
        'generate_image_update_sql.sh',
    ],
    'scripts/migration/': [
        'migrate_all_columns_350.py',
        'migrate_column_sizes.py',
        'migrate_sqlite_to_mysql.py',
        'migrate_sqlite_to_oracle.py',
    ],
    'scripts/testing/': [
        'check_csv.py',
        'find_missing_phone.py',
        'test_mysql_connection.py',
        'test_oracle_connection.py',
    ],
}

# Files to delete (obsolete)
FILES_TO_DELETE = [
    'checkImageURL',
    'rescrapeImage',
    'phone_data_updater.py',
]

def main():
    print("="*70)
    print("DialSmart File Organization")
    print("="*70)
    print()

    # Create directories
    print("[1/3] Creating directory structure...")
    for directory in ORGANIZATION_PLAN.keys():
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {directory}")

    print()

    # Move files
    print("[2/3] Moving files to organized locations...")
    moved_count = 0
    skipped_count = 0

    for destination, files in ORGANIZATION_PLAN.items():
        for filename in files:
            source_path = Path(filename)
            dest_path = Path(destination) / filename

            if source_path.exists():
                shutil.move(str(source_path), str(dest_path))
                print(f"  ✓ Moved {filename} → {destination}")
                moved_count += 1
            else:
                print(f"  ⚠ Skipped {filename} (not found)")
                skipped_count += 1

    print()
    print(f"Moved {moved_count} files, skipped {skipped_count}")
    print()

    # List files to delete
    print("[3/3] Files recommended for deletion:")
    print()
    print("The following files are obsolete and can be deleted:")
    for filename in FILES_TO_DELETE:
        if Path(filename).exists():
            print(f"  - {filename}")
        else:
            print(f"  - {filename} (already deleted)")

    print()
    print("To delete these files, run:")
    print("  rm " + " ".join(FILES_TO_DELETE))
    print()

    print("="*70)
    print("✓ Organization complete!")
    print("="*70)
    print()
    print("Next steps:")
    print("  1. Review the changes")
    print("  2. Update any scripts that reference moved files")
    print("  3. Test the application: python run.py")
    print("  4. Delete obsolete files if confirmed")
    print("  5. Commit changes: git add -A && git commit -m 'Organize files into folders'")
    print()

if __name__ == '__main__':
    main()
