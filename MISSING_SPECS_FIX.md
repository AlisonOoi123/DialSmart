# Missing Phone Specifications Issue

## Problem
Apple, Honor, Google, and Asus phones have specification records in the database, but key fields are NULL:
- screen_size
- ram_options
- storage_options
- rear_camera
- battery_capacity

This causes the comparison table to show "N/A" for these fields.

## Diagnosis
Run this SQL query to see which phones are affected:
```sql
sqlplus DS_USER/password@XE @sql/check_missing_specs.sql
```

## Solution Options

### Option 1: Check Your CSV Data
If your original CSV file (`data/phones_dataset.csv`) has this data:
1. Verify the CSV has columns: screen_size, ram_options, storage_options, rear_camera, battery_capacity
2. Check if data exists for Apple, Honor, Google, Asus rows
3. If CSV has data, you may need to re-import

### Option 2: Manual Database Update (Quick Fix for Testing)
Update a few phones manually to test:

```sql
-- Example: Update iPhone 15 Plus (adjust phone_id as needed)
UPDATE phone_specifications
SET screen_size = 6.7,
    ram_options = '6GB',
    storage_options = '128GB / 256GB / 512GB',
    rear_camera = '48 MP + 12 MP',
    battery_capacity = 4383
WHERE phone_id = (SELECT id FROM phones WHERE model_name = 'iPhone 15 Plus' AND ROWNUM = 1);

-- Example: Update iPhone 16 Plus
UPDATE phone_specifications
SET screen_size = 6.7,
    ram_options = '8GB',
    storage_options = '128GB / 256GB / 512GB',
    rear_camera = '48 MP + 12 MP',
    battery_capacity = 4674
WHERE phone_id = (SELECT id FROM phones WHERE model_name = 'iPhone 16 Plus' AND ROWNUM = 1);

COMMIT;
```

### Option 3: Check Import Script
The issue might be in how data was imported. Check:
- Did the import script skip these fields for certain brands?
- Are there any brand-specific import rules?
- Was the CSV column mapping correct?

## Quick Test
After updating a couple of phones, try comparing them again. You should see:
- Screen Size: actual values instead of N/A
- RAM: actual values instead of N/A
- Storage: actual values instead of N/A
- Camera: actual values instead of N/A
- Battery: actual values instead of N/A

## Next Steps
1. Run `sql/check_missing_specs.sql` to see the full scope
2. Check if your CSV has the data
3. If CSV has data, I can help create an update script
4. If CSV doesn't have data, you'll need to source it from elsewhere (e.g., manufacturer websites)
