# CSV Dataset Integration Guide

This guide explains how to integrate your `fyp_phoneDataset.csv` with DialSmart's database system.

## Overview

Your CSV dataset contains **comprehensive phone specifications** from 13 brands:
- Infinix, Poco, Redmi, Google, Honor, Asus, Huawei, Vivo, Oppo, Xiaomi, Apple, Realme, Samsung

The database has been **enhanced to store ALL 50+ attributes** from your CSV, including:
- Basic info (model, brand, price, images, status, release date)
- Display (screen size, type, resolution, PPI, refresh rate, protection)
- Performance (chipset, CPU, GPU, RAM, storage)
- Camera (rear, front, flash, features, video recording)
- Battery (capacity, fast charging, wireless charging)
- Network (5G/4G/3G/2G bands, SIM, technology)
- Connectivity (Wi-Fi, Bluetooth, GPS, NFC, USB, audio jack, radio)
- Physical (dimensions, weight, colors, body material)
- Features (OS, sensors, and more)

## Database Architecture

### Database Choice

**Development (Current)**: SQLite
- ✓ Simple, no setup required
- ✓ File-based database (dialsmart.db)
- ✓ Perfect for development and testing
- ✓ Works on any platform

**Production (Recommended for large datasets)**: PostgreSQL
- ✓ Better performance with large datasets
- ✓ Advanced features and indexing
- ✓ Better concurrent access
- ✓ Industry standard for production apps

### Database Models

**Brand Model**:
- Stores phone manufacturers
- Auto-created during import

**Phone Model**:
- Basic phone information
- Links to Brand via brand_id
- Stores: model name, price, images, status, release date

**PhoneSpecification Model**:
- **50+ detailed specifications**
- One-to-one relationship with Phone
- Stores ALL CSV attributes

## CSV Import Process

### Prerequisites

1. **Place your CSV file** in the project root directory:
   ```
   DialSmart/
   ├── fyp_phoneDataset.csv  ← Your CSV file here
   ├── import_csv_dataset.py
   └── ...
   ```

2. **Ensure database is initialized**:
   ```bash
   # This creates the database tables
   python run.py
   # Press Ctrl+C after it starts
   ```

### Import Your Dataset

#### Basic Import

```bash
# Import from default file (fyp_phoneDataset.csv)
python import_csv_dataset.py
```

#### Custom CSV File

```bash
# Import from a different CSV file
python import_csv_dataset.py path/to/your/custom_dataset.csv
```

### What Happens During Import

The import script will:

1. **Read the CSV file** and parse all rows
2. **Create brands automatically** if they don't exist
3. **Parse and extract data**:
   - Extract numeric values (price, battery mAh, camera MP, PPI)
   - Parse dates (release date)
   - Detect features (5G support, NFC, dual SIM)
   - Clean and format text
4. **Check for duplicates** (same brand + model name)
5. **Create Phone records** with basic info
6. **Create PhoneSpecification records** with all detailed specs
7. **Save to database** and commit

### Expected Output

```
======================================================================
DialSmart CSV Dataset Importer
======================================================================

Reading CSV file: fyp_phoneDataset.csv
Found 150 phones in CSV file

Starting import...

  [+] Created brand: Infinix
  [1/150] ✓ Imported: Infinix Note 50s - RM 741.00
  [2/150] ✓ Imported: Samsung Galaxy S24 Ultra - RM 5,999.00
  [3/150] ⊘ Skipped (duplicate): iPhone 15 Pro Max
  [4/150] ✓ Imported: Xiaomi 14 Pro - RM 3,299.00
  ...

======================================================================
Import Summary
======================================================================
Total phones in CSV: 150
Successfully imported: 145
Skipped (duplicates): 5
Errors: 0
======================================================================

✓ Success! Your database has been populated with the CSV dataset.
```

## CSV Format Requirements

Your CSV must have these columns (exact names):

### Required Columns
- `Model` - Phone model name
- `Brand` - Manufacturer name
- `Price` - Price in MYR format (e.g., "MYR 741")

### Optional but Recommended Columns
All other columns are optional but will be imported if present:

**Display**: Screen Size, Type, Display Type, Resolution, PPI, Multi-touch, Protection

**Performance**: RAM, Storage, Card Slot, Chipset, CPU, GPU

**Camera**: Rear Camera, Front Camera, Flash, Camera Features, Video Recording

**Battery**: Battery, Battery Capacity, Fast Charging, Wireless Charging, Removable Battery

**Network**: SIM, Technology, 5G Networks, 4G Networks, 3G Networks, 2G Networks, Network Speed

**Connectivity**: Wi-Fi, Bluetooth, GPS, NFC, USB, Audio Jack, Radio

**Physical**: Dimensions, Weight, Color, Body Material

**Other**: Image URL, Status, Release Date, OS, Sensors, URL

## Data Parsing Features

The import script intelligently parses data:

### Price Extraction
- Handles: "MYR 741", "RM 1,999", "RM1500"
- Extracts numeric value automatically

### Screen Size
- Extracts from: "6.78 inches", "6.5-inch display"
- Stores as float (6.78)

### Battery Capacity
- Extracts from: "5500 mAh", "5000mAh battery"
- Stores as integer (5500)

### Camera MP
- Extracts from: "64 MP, f/1.8", "48MP main camera"
- Takes first MP value (usually main camera)

### 5G Detection
- Checks Technology field for "5G"
- Checks 5G Networks field for band data
- Sets has_5g boolean automatically

### Release Date
- Parses: "Released 2025, April"
- Extracts year and creates date

## Admin Panel Integration

After importing, you can manage phones via Admin Panel:

1. **Login as admin**:
   - Email: admin@dialsmart.my
   - Password: admin123

2. **View all phones**:
   - Go to Admin Dashboard → Phones
   - See all imported phones with full specs

3. **Add new phones manually**:
   - Click "Add New Phone"
   - Fill in the form with all specifications
   - **New phones are automatically saved to the database**

4. **Edit existing phones**:
   - Click "Edit" next to any phone
   - Update specifications
   - Changes are saved to database

5. **Delete phones**:
   - Click "Delete" to remove phones
   - Specifications are automatically deleted too (cascade)

## Automatic Database Updates

When admin adds/edits phones through the Admin Panel:

1. **Form submission** → Saves to Phone table
2. **Specifications** → Saved to PhoneSpecification table
3. **Relationships** → Automatically linked via phone_id
4. **Validation** → Price must be positive, required fields checked
5. **Persistence** → All data stored in database file (SQLite) or server (PostgreSQL)

## AI Recommendation Integration

The enhanced database powers your AI recommendations:

### Current AI Engine
Uses these fields for matching:
- Price (budget fit)
- RAM (performance needs)
- Storage (capacity needs)
- Battery (usage patterns)
- 5G support (connectivity)
- Camera MP (photography needs)
- Screen size (viewing preferences)

### Enhanced AI Engine
Uses demographic data + all specs:
- Age-based preferences
- Occupation-based priorities
- Comprehensive spec matching
- Usage pattern alignment

### Chatbot Integration
Can access all phone data:
- "Show me phones with 5G under RM 2000"
- "Recommend gaming phones with good battery"
- "Find phones with wireless charging"

## Updating Your Dataset

### Re-importing (Duplicate Prevention)

If you update your CSV and re-import:

```bash
python import_csv_dataset.py
```

The script will:
- ✓ Skip existing phones (same brand + model)
- ✓ Only import new phones
- ✓ Show count of duplicates skipped

### Adding New Phones to CSV

1. **Edit your CSV file** with new phone data
2. **Run import script** again
3. **Only new phones** will be added

### Manual Addition via Admin Panel

1. Login as admin
2. Go to Phones → Add New Phone
3. Fill in all fields
4. Submit → **Automatically saved to database**

## Database Flexibility

### Switching from SQLite to PostgreSQL

For production or large datasets (1000+ phones), switch to PostgreSQL:

1. **Install PostgreSQL**:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib

   # macOS
   brew install postgresql

   # Windows
   # Download from postgresql.org
   ```

2. **Create database**:
   ```sql
   CREATE DATABASE dialsmart;
   CREATE USER dialsmart_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE dialsmart TO dialsmart_user;
   ```

3. **Update config.py**:
   ```python
   # Change from:
   SQLALCHEMY_DATABASE_URI = 'sqlite:///dialsmart.db'

   # To:
   SQLALCHEMY_DATABASE_URI = 'postgresql://dialsmart_user:your_password@localhost/dialsmart'
   ```

4. **Install PostgreSQL driver**:
   ```bash
   pip install psycopg2-binary
   ```

5. **Re-import your data**:
   ```bash
   python import_csv_dataset.py
   ```

### Database Backup

**SQLite** (current):
```bash
# Backup is just copying the file
cp dialsmart.db dialsmart_backup.db
```

**PostgreSQL** (if you switch):
```bash
pg_dump dialsmart > dialsmart_backup.sql
```

## Verifying Your Import

After importing, verify the data:

### 1. Check Database
```bash
python run.py
# Go to http://127.0.0.1:5000
# Login as admin
# Go to Admin → Phones
```

### 2. Test Recommendations
```bash
# Login as user: user@dialsmart.my / user123
# Go to Dashboard → Get Recommendations
# Try different budgets and preferences
```

### 3. Test Chatbot
```bash
# Click chatbot icon
# Try: "Recommend phones under RM 1500 with 5G"
# Should show phones from your CSV data
```

### 4. Check Phone Details
```bash
# Browse phones
# Click any phone to see details
# Verify all specs are displayed correctly
```

## Troubleshooting

### CSV file not found
```
✗ Error: CSV file not found at 'fyp_phoneDataset.csv'
```

**Solution**: Place CSV file in project root directory (same level as run.py)

### No phones imported
```
Successfully imported: 0
```

**Possible causes**:
1. All phones already in database (duplicates)
2. CSV missing required columns (Model, Brand)
3. CSV format issues

**Solution**: Check CSV has Model and Brand columns, try with fresh database

### Import errors
```
✗ Error: Invalid price format
```

**Solution**: Check price column format, should be like "MYR 741" or "RM 1999"

### Database locked (SQLite)
```
database is locked
```

**Solution**: Close all database connections, stop the Flask app, then import

## Best Practices

### For Development
1. Use SQLite (default) - simple and fast
2. Import CSV once to populate database
3. Add new phones via Admin Panel
4. Backup database file regularly

### For Production
1. Switch to PostgreSQL for better performance
2. Import CSV to production database
3. Set up regular database backups
4. Use environment variables for database credentials

### Data Maintenance
1. **Don't re-import CSV repeatedly** (causes duplicates)
2. **Use Admin Panel** for adding new phones after initial import
3. **Backup before** major changes
4. **Test on development database** first

## Summary

### Quick Start
```bash
# 1. Place CSV in project root
# 2. Import data
python import_csv_dataset.py

# 3. Run app
python run.py

# 4. Verify
# Login as admin and check phones
```

### Key Features
- ✓ **50+ specifications per phone** stored
- ✓ **Automatic brand creation**
- ✓ **Duplicate prevention**
- ✓ **Intelligent data parsing**
- ✓ **Admin panel integration**
- ✓ **AI recommendation ready**
- ✓ **Flexible database** (SQLite → PostgreSQL)

Your CSV dataset is now fully integrated with DialSmart! 🚀
