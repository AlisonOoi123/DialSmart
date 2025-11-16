# Fix Missing Phone Images

## Problem
Many phones in the database have `NULL` or `'N/A'` values for their `main_image` field, even though the CSV file contains valid image URLs.

**Affected phones:**
- Honor: 87 phones
- Huawei: 30 phones
- Apple: 13 phones
- Google: 12 phones
- Asus: 8 phones
- And others...

## Solution

We've generated an SQL script that will update all phones with their correct image URLs from the CSV file.

### Steps to Fix

1. **Run the SQL update script:**
   ```bash
   sqlplus username/password@database @update_phone_images.sql
   ```

   Or in SQL*Plus:
   ```sql
   SQL> @update_phone_images.sql
   ```

2. **Verify the fix:**
   After running the script, it will automatically show you a count of remaining phones without images. Ideally, this should be 0 or very close to 0.

   You can also manually check:
   ```sql
   SELECT b.name, COUNT(p.id) as phones_without_images
   FROM phones p
   JOIN brands b ON p.brand_id = b.id
   WHERE (p.main_image IS NULL OR p.main_image = 'N/A' OR p.main_image = '')
   GROUP BY b.name
   ORDER BY phones_without_images DESC;
   ```

## Files Created

- **`update_phone_images.sql`** - The SQL script to run (692 UPDATE statements)
- **`generate_update_images.py`** - Python script that generated the SQL (for future use)
- **`fix_missing_images.py`** - Alternative Python-based fix (requires Flask environment)

## How It Works

The SQL script:
1. Reads image URLs from the CSV file
2. Matches phones by brand name and model name (case-insensitive)
3. Only updates phones where `main_image` is NULL, 'N/A', or empty
4. Uses `ROWNUM = 1` to avoid duplicate updates
5. Commits all changes at the end

## Expected Results

After running the script:
- All 692 phones will have their correct image URLs
- The image proxy endpoint will work correctly
- Photos will display for Apple, Asus, Google, Honor brands
- All phone images throughout the application will be visible

## Troubleshooting

**If some phones still don't have images:**
- Check if the model name in the database exactly matches the CSV
- Verify the image URL in the CSV is valid (starts with https://)
- Check if there are multiple phones with the same brand/model combination

**If you need to regenerate the SQL:**
```bash
python3 generate_update_images.py > update_phone_images.sql
```
