# ⚠️ IMPORTANT: Run Database Migration First!

## Error You're Seeing

```
ORA-00904: "CONTACT_MESSAGES"."UPDATED_AT": invalid identifier
```

This means the `contact_messages` table doesn't exist in your Oracle database yet.

## Solution: Run the Migration Script

You need to create the `contact_messages` table in your Oracle database before the application can work.

### Step 1: Run the Migration

```bash
python migrate_contact_messages.py
```

### Step 2: Enter Your Oracle Credentials

When prompted, enter:
- **Username**: ds_user
- **Password**: dsuser123
- **Host**: localhost
- **Port**: 1521
- **Service Name**: orclpdb

### Step 3: Verify Success

You should see:
```
✅ Contact Messages Table Migration Completed Successfully!
```

### Step 4: Restart Your Application

```bash
python run.py
```

Now the admin dashboard should load without errors!

---

## What the Migration Creates

The migration script creates:

1. **contact_messages table** with all required columns:
   - id, name, email, subject, message
   - is_read, is_replied
   - admin_reply, replied_by_id, replied_at
   - created_at, updated_at

2. **Indexes** for better performance:
   - idx_contact_messages_email
   - idx_contact_messages_is_read
   - idx_contact_messages_is_replied
   - idx_contact_messages_created_at

3. **Trigger** for auto-updating updated_at timestamp

---

## Already Ran Migration But Still Getting Error?

If you already ran the migration but still see this error, the table might be missing columns.

Check your table structure:

```sql
sqlplus ds_user/dsuser123@localhost:1521/orclpdb

DESC contact_messages;
```

You should see all these columns:
- ID
- NAME
- EMAIL
- SUBJECT
- MESSAGE
- IS_READ
- IS_REPLIED
- ADMIN_REPLY
- REPLIED_BY_ID
- REPLIED_AT
- CREATED_AT
- **UPDATED_AT** ← This must be present!

If `UPDATED_AT` is missing, run the migration script again or add it manually:

```sql
ALTER TABLE contact_messages ADD updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

---

## Need Help?

Check the migration file: `migrate_contact_messages.py`
Check the documentation: `CONTACT_MESSAGE_SYSTEM.md`
