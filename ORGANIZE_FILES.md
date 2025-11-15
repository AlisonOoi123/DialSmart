# DialSmart File Organization Plan

## New Folder Structure

```
/home/user/DialSmart/
├── app/                        # Application code (no changes)
├── docs/                       # 📚 Documentation files
│   ├── CSV_DATASET_GUIDE.md
│   ├── FIXES_SUMMARY.md
│   ├── ORACLE_SETUP_GUIDE.md
│   ├── README_IMAGE_FIX.md
│   └── SETUP_GUIDE.md
├── data/                       # 📊 Data files
│   └── fyp_phoneDataset.csv
├── sql/                        # 🗄️ SQL scripts
│   ├── setup_oracle_sequences.sql
│   ├── setup_oracle_user.sql
│   ├── update_oracle_columns.sql
│   └── update_phone_images.sql
├── scripts/                    # 🔧 Utility scripts
│   ├── database/              # Database utilities
│   │   ├── check_oracle_service.py
│   │   ├── clear_phone_data.py
│   │   ├── init_database.py
│   │   ├── initialize_oracle.py
│   │   └── initialize_system.py
│   ├── import/                # Import scripts
│   │   ├── import_csv_dataset.py
│   │   ├── import_csv_to_oracle.py
│   │   ├── fix_missing_images.py
│   │   ├── generate_update_images.py
│   │   └── generate_image_update_sql.sh
│   ├── migration/             # Migration scripts
│   │   ├── migrate_all_columns_350.py
│   │   ├── migrate_column_sizes.py
│   │   ├── migrate_sqlite_to_mysql.py
│   │   └── migrate_sqlite_to_oracle.py
│   └── testing/               # Testing tools
│       ├── check_csv.py
│       ├── find_missing_phone.py
│       ├── test_mysql_connection.py
│       └── test_oracle_connection.py
├── config.py                   # Configuration (stays at root)
├── run.py                      # Application entry point (stays at root)
├── scheduler.py                # Scheduler (stays at root)
├── requirements.txt            # Dependencies (stays at root)
└── README.md                   # Main documentation (stays at root)
```

## Files to Move

### Documentation → `docs/`
- CSV_DATASET_GUIDE.md
- FIXES_SUMMARY.md
- ORACLE_SETUP_GUIDE.md
- README_IMAGE_FIX.md
- SETUP_GUIDE.md

### Data Files → `data/`
- fyp_phoneDataset.csv

### SQL Scripts → `sql/`
- setup_oracle_sequences.sql
- setup_oracle_user.sql
- update_oracle_columns.sql
- update_phone_images.sql

### Database Scripts → `scripts/database/`
- check_oracle_service.py
- clear_phone_data.py
- init_database.py
- initialize_oracle.py
- initialize_system.py

### Import Scripts → `scripts/import/`
- import_csv_dataset.py
- import_csv_to_oracle.py
- fix_missing_images.py
- generate_update_images.py
- generate_image_update_sql.sh

### Migration Scripts → `scripts/migration/`
- migrate_all_columns_350.py
- migrate_column_sizes.py
- migrate_sqlite_to_mysql.py
- migrate_sqlite_to_oracle.py

### Testing Scripts → `scripts/testing/`
- check_csv.py
- find_missing_phone.py
- test_mysql_connection.py
- test_oracle_connection.py

## Files to DELETE (No Longer Needed)

### Obsolete/Duplicate Files:
1. **checkImageURL** - Binary file, functionality replaced by fix_missing_images.py
2. **rescrapeImage** - Binary file, functionality replaced by generate_update_images.py
3. **phone_data_updater.py** - Replaced by import_csv_to_oracle.py
4. **migrate_column_sizes.py** - Superseded by migrate_all_columns_350.py
5. **reset_admin.py** - Should use proper admin user management instead

### Keep for Now (May be needed):
- config.py - KEEP (configuration file)
- run.py - KEEP (application entry point)
- scheduler.py - KEEP (background scheduler)
- requirements.txt - KEEP (dependencies)
- README.md - KEEP (main documentation)

## Files That Stay at Root

These files are essential and should remain at the root level:
- `config.py` - Configuration
- `run.py` - Application entry point
- `scheduler.py` - Background scheduler
- `requirements.txt` - Python dependencies
- `README.md` - Main documentation
- `.gitignore` - Git configuration
- `app/` - Application directory

## Implementation Steps

1. Run the organization script: `python organize_files.py`
2. Verify all imports still work
3. Update documentation references
4. Delete obsolete files after confirmation
5. Commit changes to git

## After Organization

Update any scripts that reference these files:
- Update README.md to point to docs/ folder
- Update any import paths if needed
- Test all scripts to ensure they still work
