# Database Migrations

This folder contains SQL migration scripts for the Oracle database.

## How to Run Migrations

Connect to your Oracle database using SQL*Plus or SQL Developer and execute the scripts in order:

### Using SQL*Plus:
```bash
sqlplus username/password@database
@migrations/001_add_admin_management_columns.sql
@migrations/002_create_audit_logs_table.sql
```

### Using SQL Developer:
1. Connect to your Oracle database
2. Open each .sql file
3. Execute them in numerical order

## Migration History

| Script | Description | Date |
|--------|-------------|------|
| 001_add_admin_management_columns.sql | Add admin management columns (force_password_change, created_by_admin_id, last_password_change) | 2025-11-19 |
| 002_create_audit_logs_table.sql | Create audit_logs table for tracking admin actions | 2025-11-19 |

## Verification

After running the migrations, verify the changes:

```sql
-- Check if new columns exist
SELECT column_name, data_type, nullable
FROM user_tab_columns
WHERE table_name = 'USERS'
AND column_name IN ('FORCE_PASSWORD_CHANGE', 'CREATED_BY_ADMIN_ID', 'LAST_PASSWORD_CHANGE');

-- Check if audit_logs table was created
SELECT table_name FROM user_tables WHERE table_name = 'AUDIT_LOGS';

-- Check audit_logs structure
DESC audit_logs;
```

## Rollback (if needed)

If you need to rollback these changes:

```sql
-- Rollback 002_create_audit_logs_table.sql
DROP TRIGGER audit_logs_bir;
DROP SEQUENCE audit_logs_seq;
DROP TABLE audit_logs CASCADE CONSTRAINTS;

-- Rollback 001_add_admin_management_columns.sql
ALTER TABLE users DROP CONSTRAINT fk_users_created_by_admin;
ALTER TABLE users DROP COLUMN force_password_change;
ALTER TABLE users DROP COLUMN created_by_admin_id;
ALTER TABLE users DROP COLUMN last_password_change;

COMMIT;
```
