#!/bin/bash
# DialSmart Cleanup Script
# Safely removes unnecessary files from the project

echo "================================================"
echo "DialSmart Project Cleanup Script"
echo "================================================"
echo ""

# Ask for confirmation
read -p "This will delete cache files and old documentation. Continue? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Cleanup cancelled."
    exit 1
fi

echo ""
echo "Starting cleanup..."
echo ""

# 1. Delete Python cache files
echo "1. Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
find . -type f -name "*.pyo" -delete 2>/dev/null
echo "   ✓ Python cache files removed"

# 2. Delete old documentation
echo "2. Removing old documentation..."
rm -f FILES_TO_DELETE.md 2>/dev/null
rm -f MISSING_SPECS_FIX.md 2>/dev/null
rm -f ORGANIZE_FILES.md 2>/dev/null
rm -f QUICK_FIX_CONTACT_ERROR.md 2>/dev/null
echo "   ✓ Old documentation removed"

# 3. Delete testing scripts
echo "3. Removing testing scripts..."
rm -rf scripts/testing/ 2>/dev/null
echo "   ✓ Testing scripts removed"

# 4. Delete migration scripts
echo "4. Removing migration scripts..."
rm -rf scripts/migration/ 2>/dev/null
echo "   ✓ Migration scripts removed"

# 5. Delete redundant database scripts
echo "5. Removing redundant database scripts..."
rm -f scripts/database/initialize_system.py 2>/dev/null
rm -f scripts/database/initialize_oracle.py 2>/dev/null
rm -f scripts/database/init_database.py 2>/dev/null
echo "   ✓ Redundant database scripts removed"

# 6. Delete redundant import scripts
echo "6. Removing redundant import scripts..."
rm -f scripts/import/import_csv_dataset.py 2>/dev/null
rm -f scripts/import/import_csv_to_oracle.py 2>/dev/null
rm -f scripts/import/generate_update_images.py 2>/dev/null
rm -f scripts/import/fix_missing_images.py 2>/dev/null
echo "   ✓ Redundant import scripts removed"

# 7. Delete large SQL data files
echo "7. Removing large SQL data files..."
rm -f sql/update_phone_images.sql 2>/dev/null
rm -f sql/check_missing_specs.sql 2>/dev/null
echo "   ✓ SQL data files removed"

# 8. Delete root utility scripts
echo "8. Removing root utility scripts..."
rm -f organize_files.py 2>/dev/null
echo "   ✓ Utility scripts removed"

# 9. Delete log files (optional)
echo "9. Removing log files (if any)..."
find . -type f -name "*.log" -delete 2>/dev/null
echo "   ✓ Log files removed"

echo ""
echo "================================================"
echo "Cleanup completed successfully!"
echo "================================================"
echo ""
echo "You can now share this cleaner project."
echo ""
