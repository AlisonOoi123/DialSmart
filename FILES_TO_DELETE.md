# Files to Delete

## ✅ Safe to Delete Immediately

These files are obsolete and have been replaced by better alternatives:

### 1. **checkImageURL** (Binary file)
- **Reason**: Functionality replaced by `scripts/import/fix_missing_images.py`
- **What it did**: Checked image URLs in the CSV
- **Replacement**: Use `python scripts/import/generate_update_images.py` instead

### 2. **rescrapeImage** (Binary file)
- **Reason**: Functionality replaced by `scripts/import/generate_update_images.py`
- **What it did**: Re-scraping phone images
- **Replacement**: SQL script `sql/update_phone_images.sql` does this better

### 3. **phone_data_updater.py**
- **Reason**: Superseded by `scripts/import/import_csv_to_oracle.py`
- **What it did**: Old version of CSV import
- **Replacement**: Use `python scripts/import/import_csv_to_oracle.py`

### 4. **migrate_column_sizes.py** (Already moved to scripts/migration/)
- **Reason**: Superseded by `scripts/migration/migrate_all_columns_350.py`
- **What it did**: Incremental column size increases
- **Replacement**: Use the comprehensive migration instead
- **Location**: `scripts/migration/migrate_column_sizes.py` (can delete after confirming)

### 5. **reset_admin.py**
- **Reason**: Should use proper admin user management in the app
- **What it did**: Reset admin password
- **Replacement**: Use the admin panel or database directly
- **⚠️ Warning**: Keep this if you frequently need to reset admin access

## 🔧 Command to Delete

```bash
# Delete the obsolete files
rm checkImageURL rescrapeImage phone_data_updater.py

# Optional: Delete the old migration script after confirming the new one works
rm scripts/migration/migrate_column_sizes.py

# Optional: Delete reset_admin.py if not needed
rm reset_admin.py
```

## ⚠️ DO NOT DELETE

The following files must be kept:

- **config.py** - Application configuration
- **run.py** - Application entry point
- **scheduler.py** - Background scheduler
- **requirements.txt** - Python dependencies
- **README.md** - Main documentation
- **ORGANIZE_FILES.md** - Organization documentation
- **organize_files.py** - Organization script (useful for reference)
- **.gitignore** - Git configuration
- **app/** - Application directory
- **docs/** - Documentation folder (newly organized)
- **data/** - Data files folder
- **sql/** - SQL scripts folder
- **scripts/** - All organized scripts

## 📊 Summary

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Ready to Delete | 3-5 files | Obsolete binaries and old scripts |
| 📁 Organized | 28 files | Moved to categorized folders |
| 🔒 Protected | 6+ files | Essential files at root level |

## 🎯 After Deletion

1. The project will be cleaner and more organized
2. All functionality is preserved in better scripts
3. Easier to find and maintain code
4. Clear separation of concerns (docs, scripts, data, SQL)

## 📝 Verification Steps

Before deleting, verify:
```bash
# 1. Check if import still works
python scripts/import/import_csv_to_oracle.py --help

# 2. Check if migration works
python scripts/migration/migrate_all_columns_350.py --help

# 3. Check if image fix works
python scripts/import/generate_update_images.py > test.sql
head test.sql
rm test.sql
```

If all three work, it's safe to delete the old files.
