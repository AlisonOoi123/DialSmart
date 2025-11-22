# Brand Website URL Feature - Setup Instructions for Oracle Database

## You're using Oracle Database with SQL*Plus - Follow these steps:

### Step 1: Connect to Your Oracle Database

```bash
sqlplus username/password@your_database
```

Or if you're using a connection string:
```bash
sqlplus username/password@//host:port/service_name
```

### Step 2: Run the Migration

Once connected to SQL*Plus, run the migration script:

```sql
@migrations/add_brand_website_url_oracle.sql
```

This will:
- Add the `website_url` column to your brands table
- Show the table structure to verify the column was added

### Step 3: Populate Brand URLs (Optional but Recommended)

To add website URLs for common brands:

```sql
@migrations/populate_brand_urls_oracle.sql
```

This will populate URLs for brands like Apple, Samsung, Realme, etc.

### Step 4: Verify the Changes

Check if the column was added:
```sql
DESC brands;
```

Check which brands now have URLs:
```sql
SELECT name, website_url FROM brands WHERE website_url IS NOT NULL;
```

### Step 5: Restart Your Flask Application

Stop and restart your Flask application:

```bash
# Stop the current application (Ctrl+C)
# Then restart it
python run.py
```

### Step 6: Test the Feature

1. Visit any phone details page, e.g., http://192.168.0.178:5000/phone/4786
2. The brand name (e.g., "Apple") should now be clickable
3. Clicking it will open the brand's official website in a new tab

---

## Alternative: Manual SQL Commands

If you prefer to run commands manually in SQL*Plus:

```sql
-- Add the column
ALTER TABLE brands ADD website_url VARCHAR2(500);
COMMIT;

-- Add a website URL for a specific brand
UPDATE brands SET website_url = 'https://www.apple.com' WHERE name = 'Apple';
COMMIT;

-- Verify
SELECT name, website_url FROM brands WHERE name = 'Apple';
```

---

## Adding More Brands via Admin Panel

After the migration, you can also add/edit brand URLs via the web interface:

1. Go to http://192.168.0.178:5000/admin/brands
2. Click "Edit" on any brand
3. Enter the official website URL in the "Official Website URL" field
4. Click "Update Brand"

---

## Troubleshooting

**Q: Brand names still not clickable?**
- Verify the column exists: `DESC brands;`
- Check if the brand has a URL: `SELECT name, website_url FROM brands WHERE name = 'Apple';`
- Make sure you restarted the Flask application
- Clear your browser cache (Ctrl+Shift+R)

**Q: "Column already exists" error?**
- The migration was already run. Skip to Step 3 to populate URLs.

**Q: How to check my Oracle database connection info?**
- Check your `config.py` or environment variables for `DATABASE_URL`
- It should look like: `oracle://user:pass@host:port/service_name`

**Q: Permission denied errors?**
- Make sure your Oracle user has ALTER TABLE privileges
- Contact your DBA if needed
