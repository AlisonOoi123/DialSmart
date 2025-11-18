# Quick Fix: Database Column Error

## Error Message

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such column: users.email_verified
```

## ⚡ Quick Fix (Recommended)

Run the migration script to add the missing columns to your existing database:

```bash
python migrate_database.py
```

This will:
- ✅ Add the new email verification columns
- ✅ Keep all your existing data (689 phones, users, etc.)
- ✅ Auto-verify all existing users
- ✅ Take only a few seconds

After migration, restart your app:
```bash
python run.py
```

---

## Alternative Solutions

### Option A: Delete and Recreate Database (⚠️ LOSES ALL DATA)

If you don't mind losing your existing data:

```bash
# Windows
del dialsmart.db
python run.py

# Linux/Mac
rm dialsmart.db
python run.py
```

Then re-import your data:
```bash
python import_phones_from_csv.py
python create_test_user.py
python create_admin_account.py
```

### Option B: Manual SQLite Migration

If you prefer to do it manually:

```bash
sqlite3 dialsmart.db
```

```sql
-- Add the new columns
ALTER TABLE users ADD COLUMN email_verified INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN email_verification_token VARCHAR(100);
ALTER TABLE users ADD COLUMN email_verification_sent_at DATETIME;

-- Auto-verify existing users
UPDATE users SET email_verified = 1;

-- Exit
.exit
```

---

## What Changed?

New columns added to the `users` table:

| Column | Type | Description |
|--------|------|-------------|
| `email_verified` | Boolean | Whether user verified their email |
| `email_verification_token` | String(100) | Unique token for email verification |
| `email_verification_sent_at` | DateTime | When verification email was sent |

---

## Why This Happened

The User model was updated to support email verification, but your existing database doesn't have these columns yet. This is a normal part of database schema evolution.

---

## Prevention for Future Updates

For production, consider using proper database migration tools:

```bash
# Install Flask-Migrate (optional)
pip install Flask-Migrate

# Initialize migrations
flask db init
flask db migrate -m "Add email verification"
flask db upgrade
```

This will track all database schema changes automatically.

---

## Verification

After running the migration, verify it worked:

```bash
sqlite3 dialsmart.db "PRAGMA table_info(users);"
```

You should see `email_verified`, `email_verification_token`, and `email_verification_sent_at` in the list.

---

## Need Help?

1. **Migration Failed?**
   - Check if `dialsmart.db` exists
   - Make sure no other process is using the database
   - Close the Flask app before migrating

2. **Still Getting Errors?**
   - Try Option A (delete and recreate)
   - Check file permissions
   - Verify Python has write access to the directory

3. **Want to Keep Data?**
   - Use the migration script (Option 1)
   - Or manually export/import data

---

**Quick Command Summary:**

```bash
# Recommended fix
python migrate_database.py
python run.py

# Check if it worked
sqlite3 dialsmart.db "SELECT email_verified FROM users LIMIT 1;"
```

If you see a result without errors, you're good to go! ✅
