# Database Migrations

This directory contains database migration scripts for DialSmart.

## Migration: Add Brand Website URL

**Date:** 2025-11-22
**Description:** Adds a `website_url` field to the brands table to store official brand website URLs.

### Running the Migration

#### Option 1: Using Python Script
```bash
python migrations/add_brand_website_url.py
```

#### Option 2: Using SQL Directly
If you're using SQLite:
```bash
sqlite3 dialsmart.db < migrations/add_brand_website_url.sql
```

For other databases, execute the SQL file using your database client.

### Manual Migration (Alternative)
If automated migration fails, you can manually add the column using SQL:

```sql
ALTER TABLE brands ADD COLUMN website_url VARCHAR(500);
```

### Verification
After running the migration, verify the column was added:
```sql
PRAGMA table_info(brands);  -- For SQLite
-- or
DESCRIBE brands;  -- For MySQL
-- or
\d brands  -- For PostgreSQL
```

### Rollback
To remove the column (if needed):
```sql
-- Note: SQLite doesn't support DROP COLUMN easily
-- For other databases:
ALTER TABLE brands DROP COLUMN website_url;
```
