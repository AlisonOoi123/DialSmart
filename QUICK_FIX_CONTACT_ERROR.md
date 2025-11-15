# Fix Contact Form Error - ORA-01400

## Error You're Seeing

```
ORA-01400: cannot insert NULL into ("DS_USER"."CONTACT_MESSAGES"."ID")
```

## What Happened

The `contact_messages` table was created, but Oracle needs a **sequence** and **trigger** to auto-generate the ID field (Oracle doesn't support AUTO_INCREMENT like MySQL).

## Quick Fix (30 seconds)

### Option 1: Run the Quick Fix SQL

In SQL*Plus or SQL Developer:

```sql
SQL> @sql/create_contact_messages_sequence.sql
```

**OR** copy and paste this directly:

```sql
CREATE SEQUENCE contact_messages_seq
    START WITH 1
    INCREMENT BY 1
    NOCACHE
    NOCYCLE;

CREATE OR REPLACE TRIGGER contact_messages_id_trigger
BEFORE INSERT ON contact_messages
FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        SELECT contact_messages_seq.NEXTVAL INTO :NEW.id FROM DUAL;
    END IF;
END;
/
```

### Option 2: Re-run the Complete Setup

If you want to ensure ALL tables have sequences (recommended):

```sql
SQL> @sql/setup_oracle_sequences.sql
```

This will create sequences for ALL tables including the new `contact_messages` table.

## After Running the Fix

1. The error will be gone
2. Try submitting the contact form again
3. You should see a success message
4. Admin can view the message at: `/admin/messages`

## Verification

Check if the sequence was created:

```sql
SELECT sequence_name FROM user_sequences WHERE sequence_name = 'CONTACT_MESSAGES_SEQ';
```

Check if the trigger was created:

```sql
SELECT trigger_name, status FROM user_triggers WHERE trigger_name = 'CONTACT_MESSAGES_ID_TRIGGER';
```

Both should return results.

## Why This Happened

- The `ContactMessage` model was added recently
- SQLAlchemy created the table structure
- But Oracle 11g requires manual sequence/trigger setup for auto-increment
- This is different from MySQL/PostgreSQL which have built-in AUTO_INCREMENT

## Preventing Future Issues

Whenever you add a new model with an auto-incrementing ID in Oracle:

1. Update `sql/setup_oracle_sequences.sql` to include it (✅ already done!)
2. Run the sequence setup script
3. Or use the quick fix script for just that table

---

**TL;DR:** Run `@sql/create_contact_messages_sequence.sql` in SQL*Plus and you're good to go! 🚀
