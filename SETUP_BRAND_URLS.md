# Brand Website URL Feature - Setup Instructions

## The feature is now installed, but you need to activate it:

### Step 1: Run the Migration

**On your local machine** where the DialSmart app is running, navigate to the project directory and run:

```bash
python migrate_add_website_url.py
```

This will:
- Add the `website_url` column to your brands table
- Optionally populate website URLs for common brands (Apple, Samsung, Realme, etc.)

### Step 2: Verify the Migration

After running the migration, you can verify it worked:

```bash
sqlite3 dialsmart.db "SELECT name, website_url FROM brands LIMIT 5;"
```

### Step 3: Restart Your Flask Application

Stop and restart your Flask application:

```bash
# Stop the current application (Ctrl+C)
# Then restart it
python run.py
```

### Step 4: Test the Feature

1. Visit any phone details page, e.g., http://192.168.0.178:5000/phone/4786
2. The brand name (e.g., "Apple") should now be clickable
3. Clicking it will open the brand's official website in a new tab

### Step 5: Add More Brand URLs (Optional)

Via the admin panel:
1. Go to http://192.168.0.178:5000/admin/brands
2. Click "Edit" on any brand
3. Enter the official website URL in the "Official Website URL" field
4. Save

## Troubleshooting

**Q: Brand names still not clickable?**
- Check if the migration ran successfully
- Check if the brand has a website_url set in the database
- Try running: `sqlite3 dialsmart.db "SELECT name, website_url FROM brands WHERE name='Apple';"`
- Make sure you restarted the Flask application

**Q: Migration script can't find database?**
- Make sure you're in the DialSmart project root directory
- The database file should be named `dialsmart.db`
- Check if your DATABASE_URL environment variable points to a different location

**Q: How do I add website URLs manually?**
You can use SQL:
```sql
sqlite3 dialsmart.db
UPDATE brands SET website_url = 'https://www.apple.com' WHERE name = 'Apple';
```

Or use the admin panel at http://192.168.0.178:5000/admin/brands
