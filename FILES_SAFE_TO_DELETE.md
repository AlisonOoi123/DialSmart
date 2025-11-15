# Files Safe to Delete - DialSmart

This document lists files and folders that can be safely deleted from the DialSmart project.

---

## ✅ SAFE TO DELETE (Recommended)

### 1. Python Cache Files (Auto-generated)
These are automatically recreated when you run the app:

```bash
# Delete all __pycache__ folders
/home/user/DialSmart/app/models/__pycache__/
/home/user/DialSmart/app/routes/__pycache__/
/home/user/DialSmart/app/modules/__pycache__/
/home/user/DialSmart/app/utils/__pycache__/
/home/user/DialSmart/app/__pycache__/
/home/user/DialSmart/__pycache__/

# All .pyc files (compiled Python)
*.pyc
*.pyo
```

**How to delete:**
```bash
# From project root
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

---

### 2. Old Documentation Files (Debugging/Development)

These were created during development and are no longer needed:

```
❌ FILES_TO_DELETE.md              (Old file listing, outdated)
❌ MISSING_SPECS_FIX.md             (Debugging doc, issue is fixed)
❌ ORGANIZE_FILES.md                (Development notes, no longer needed)
❌ QUICK_FIX_CONTACT_ERROR.md       (Debugging doc, issue is fixed)
```

**Keep these docs:**
```
✅ README.md                        (Main project overview)
✅ SETUP_GUIDE.md                   (Complete setup instructions)
✅ QUICK_START.md                   (Quick reference)
✅ SETUP_CHECKLIST.md               (Setup progress tracker)
```

---

### 3. Testing/Debug Scripts

Located in `scripts/testing/`:

```
❌ scripts/testing/check_csv.py                    (Debug script)
❌ scripts/testing/find_missing_phone.py           (Debug script)
❌ scripts/testing/test_oracle_connection.py       (Test script, not needed after setup)
❌ scripts/testing/test_mysql_connection.py        (MySQL not used)
```

---

### 4. Migration Scripts (If Already on Oracle)

Located in `scripts/migration/`:

```
❌ scripts/migration/migrate_sqlite_to_oracle.py   (Only needed for SQLite migration)
❌ scripts/migration/migrate_sqlite_to_mysql.py    (Not used - project uses Oracle)
❌ scripts/migration/migrate_all_columns_350.py    (Old migration script)
❌ scripts/migration/migrate_column_sizes.py       (Old migration script)
```

**Note:** Only delete these if you're already using Oracle and don't need to migrate from SQLite.

---

### 5. Redundant Database Scripts

Located in `scripts/database/`:

```
❌ scripts/database/initialize_system.py           (Redundant - db.create_all() in run.py)
❌ scripts/database/initialize_oracle.py           (Redundant)
❌ scripts/database/init_database.py               (Redundant)
```

**Keep these:**
```
✅ scripts/database/clear_phone_data.py            (Useful for resetting data)
✅ scripts/database/check_oracle_service.py        (Useful for debugging)
```

---

### 6. Redundant Import Scripts

Located in `scripts/import/`:

```
❌ scripts/import/import_csv_dataset.py            (Old version)
❌ scripts/import/import_csv_to_oracle.py          (Old version)
❌ scripts/import/generate_update_images.py        (Image update script, probably not needed)
❌ scripts/import/fix_missing_images.py            (Debug script)
```

**Keep this:**
```
✅ scripts/import/update_missing_specs_from_csv.py (Main import script - KEEP!)
```

---

### 7. Large SQL Data Files

Located in `sql/`:

```
❌ sql/update_phone_images.sql                     (284KB - large data file, only needed once)
❌ sql/check_missing_specs.sql                     (Debug query, issue is fixed)
```

**Keep these:**
```
✅ sql/create_contact_messages_sequence.sql        (Needed for setup)
✅ sql/setup_oracle_sequences.sql                  (Needed for setup)
✅ sql/setup_oracle_user.sql                       (Needed for setup)
✅ sql/update_oracle_columns.sql                   (May be needed for updates)
```

---

### 8. Root Level Utility Scripts

```
❌ organize_files.py                               (Development utility, no longer needed)
```

**Keep these:**
```
✅ run.py                                          (Main application entry point)
✅ config.py                                       (Configuration file)
✅ scheduler.py                                    (Background task scheduler)
✅ requirements.txt                                (Python dependencies)
```

---

## ⚠️ CHECK BEFORE DELETING

These might be useful depending on your needs:

### Log Files (if any)
```
*.log                                              (Application logs - check if needed)
```

### Environment Files
```
.env                                               (Contains sensitive data - NEVER commit to Git!)
.env.example                                       (Template for .env - keep if sharing project)
```

### Git Files
```
.gitignore                                         (KEEP - tells Git what to ignore)
.git/                                              (KEEP - Git repository data)
```

---

## 🔴 NEVER DELETE

These are essential for the application:

### Core Application Files
```
✅ app/                                            (Main application code)
✅ app/models/                                     (Database models)
✅ app/routes/                                     (URL routes)
✅ app/modules/                                    (Core logic - AI, chatbot, comparison)
✅ app/templates/                                  (HTML templates)
✅ app/static/                                     (CSS, JavaScript, images)
✅ app/utils/                                      (Helper functions)
```

### Data Files
```
✅ data/fyp_phoneDataset.csv                       (Main phone dataset)
```

### Configuration & Setup
```
✅ config.py                                       (Application configuration)
✅ run.py                                          (Application entry point)
✅ requirements.txt                                (Python dependencies)
```

### Documentation
```
✅ README.md                                       (Project overview)
✅ SETUP_GUIDE.md                                  (Setup instructions)
✅ QUICK_START.md                                  (Quick reference)
✅ SETUP_CHECKLIST.md                              (Setup checklist)
```

---

## 📋 Quick Delete Commands

### Option 1: Delete Everything Safe (Recommended)

Run these commands from the project root:

```bash
# 1. Delete Python cache files
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
find . -type f -name "*.pyo" -delete

# 2. Delete old documentation
rm -f FILES_TO_DELETE.md MISSING_SPECS_FIX.md ORGANIZE_FILES.md QUICK_FIX_CONTACT_ERROR.md

# 3. Delete testing scripts (optional)
rm -rf scripts/testing/

# 4. Delete migration scripts (if already on Oracle)
rm -rf scripts/migration/

# 5. Delete redundant scripts
rm -f scripts/database/initialize_system.py
rm -f scripts/database/initialize_oracle.py
rm -f scripts/database/init_database.py

# 6. Delete redundant import scripts
rm -f scripts/import/import_csv_dataset.py
rm -f scripts/import/import_csv_to_oracle.py
rm -f scripts/import/generate_update_images.py
rm -f scripts/import/fix_missing_images.py

# 7. Delete large SQL data files (after data is imported)
rm -f sql/update_phone_images.sql
rm -f sql/check_missing_specs.sql

# 8. Delete root utility scripts
rm -f organize_files.py
```

### Option 2: Conservative Delete (Just Cache)

If you're unsure, just delete cache files:

```bash
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete
```

---

## 📊 Space Saved

Approximate space you'll save:

- Python cache files: ~5-10 MB
- Old documentation: ~20 KB
- Testing/migration scripts: ~100 KB
- Large SQL files: ~300 KB
- Total: **~5-10 MB**

---

## ⚙️ After Deleting

1. **Test the application** to ensure everything still works:
   ```bash
   python run.py
   ```

2. **Commit changes to Git** (if using version control):
   ```bash
   git status
   git add .
   git commit -m "Clean up unnecessary files and cache"
   ```

3. **Cache files will regenerate** automatically when you run the app again

---

## 🔍 How to Check If a File is Used

Before deleting any file you're unsure about:

```bash
# Search for imports of the file
grep -r "import filename" .

# Search for any references to the file
grep -r "filename" . --include="*.py"
```

---

## ✅ Final Recommendation

**For most users, safe to delete:**
1. All `__pycache__` folders and `.pyc` files
2. Old documentation files (FILES_TO_DELETE.md, MISSING_SPECS_FIX.md, etc.)
3. Testing and migration scripts
4. organize_files.py

**This will clean up your project without affecting functionality!**
