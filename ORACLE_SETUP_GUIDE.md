# Oracle Database Setup Guide for DialSmart

Complete guide for configuring DialSmart with Oracle Database.

---

## ✅ Current Status

You have:
- ✅ Oracle Database 21c running
- ✅ 692 phones in database
- ✅ User: `ds_user` with password: `dsuser123`
- ✅ Service: `orclpdb` on `localhost:1521`

---

## 🚀 Quick Setup (5 Steps)

### Step 1: Install Oracle Driver

```bash
pip install cx-Oracle
```

**Or install all requirements:**
```bash
pip install -r requirements.txt
```

### Step 2: Run Oracle Migration

```bash
python migrate_oracle_database.py
```

**You'll be prompted for:**
- Username: `ds_user` (press Enter for default)
- Password: `dsuser123`
- Host: `localhost` (press Enter for default)
- Port: `1521` (press Enter for default)
- Service Name: `orclpdb` (press Enter for default)

**Expected Output:**
```
======================================================================
DialSmart Oracle Database Migration
Adding Email Verification & Password Reset Columns
======================================================================

Enter Oracle Database Connection Details:
Username (default: ds_user):
Password:
Host (default: localhost):
Port (default: 1521):
Service Name (default: orclpdb):

Connecting to Oracle at localhost:1521/orclpdb...
✅ Connected successfully!

Checking existing columns in users table...
Found X existing columns

Adding missing columns...
  Adding: email_verified (NUMBER(1) DEFAULT 0)
  Adding: email_verification_token (VARCHAR2(100))
  Adding: email_verification_sent_at (TIMESTAMP)
  Adding: password_reset_token (VARCHAR2(100))
  Adding: password_reset_sent_at (TIMESTAMP)

Auto-verifying existing users...
✅ Updated X users

======================================================================
✅ Oracle Database Migration Completed Successfully!
======================================================================
```

### Step 3: Verify Migration

Connect to Oracle and check:

```bash
sqlplus ds_user/dsuser123@localhost:1521/orclpdb
```

```sql
-- Check new columns
DESCRIBE users;

-- Verify email_verified column exists
SELECT email_verified FROM users WHERE ROWNUM = 1;

-- Should return 1 for existing users
```

### Step 4: Configure Application

The application is already configured for Oracle with your credentials:
- `config.py` has Oracle connection settings
- Defaults match your setup (ds_user, dsuser123, localhost:1521/orclpdb)

**No changes needed unless you want to use environment variables.**

### Step 5: Run Application

```bash
python run.py
```

Visit: http://localhost:5000

---

## 📋 Configuration Details

### Option A: Use Default Configuration (Recommended)

The `config.py` already has your Oracle credentials:

```python
ORACLE_USER = 'ds_user'
ORACLE_PASSWORD = 'dsuser123'
ORACLE_HOST = 'localhost'
ORACLE_PORT = '1521'
ORACLE_SERVICE = 'orclpdb'
```

**No additional setup needed!**

### Option B: Use Environment Variables (Production)

Create `.env` file:

```bash
# Oracle Database
ORACLE_USER=ds_user
ORACLE_PASSWORD=dsuser123
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=orclpdb

# Or use full connection string
# DATABASE_URL=oracle+cx_oracle://ds_user:dsuser123@localhost:1521/?service_name=orclpdb
```

---

## 🔧 Database Schema Changes

### Columns Added to USERS Table

```sql
-- Email verification
email_verified NUMBER(1) DEFAULT 0
email_verification_token VARCHAR2(100)
email_verification_sent_at TIMESTAMP

-- Password reset
password_reset_token VARCHAR2(100)
password_reset_sent_at TIMESTAMP
```

### Manual Migration (Alternative)

If you prefer to run SQL manually:

```sql
-- Connect to Oracle
sqlplus ds_user/dsuser123@localhost:1521/orclpdb

-- Add email verification columns
ALTER TABLE users ADD email_verified NUMBER(1) DEFAULT 0;
ALTER TABLE users ADD email_verification_token VARCHAR2(100);
ALTER TABLE users ADD email_verification_sent_at TIMESTAMP;

-- Add password reset columns
ALTER TABLE users ADD password_reset_token VARCHAR2(100);
ALTER TABLE users ADD password_reset_sent_at TIMESTAMP;

-- Auto-verify existing users
UPDATE users SET email_verified = 1;
COMMIT;

-- Verify changes
DESCRIBE users;
SELECT COUNT(*) FROM users WHERE email_verified = 1;
```

---

## 🔍 Troubleshooting

### Error: "cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library"

**Solution:** Install Oracle Instant Client

**For Windows:**
1. Download Oracle Instant Client from Oracle website
2. Extract to `C:\oracle\instantclient_21_3`
3. Add to PATH: `C:\oracle\instantclient_21_3`
4. Restart terminal

**For Linux:**
```bash
# Download and install Instant Client
sudo yum install oracle-instantclient-basic

# Or for Ubuntu
sudo apt-get install libaio1
wget https://download.oracle.com/otn_software/linux/instantclient/instantclient-basic-linux.x64-21.1.0.0.0.zip
unzip instantclient-basic-linux.x64-21.1.0.0.0.zip
export LD_LIBRARY_PATH=/path/to/instantclient_21_1:$LD_LIBRARY_PATH
```

### Error: "ORA-12541: TNS:no listener"

**Solution:** Oracle listener not running

```bash
# Check listener status
lsnrctl status

# Start listener
lsnrctl start
```

### Error: "ORA-01017: invalid username/password"

**Solution:** Verify credentials

```bash
# Test connection
sqlplus ds_user/dsuser123@localhost:1521/orclpdb

# If fails, reset password
sqlplus / as sysdba
ALTER USER ds_user IDENTIFIED BY dsuser123;
```

### Error: "ModuleNotFoundError: No module named 'cx_Oracle'"

**Solution:** Install cx_Oracle

```bash
pip install cx-Oracle
```

---

## 🧪 Testing Oracle Connection

### Test Script: `test_oracle_connection.py`

```python
import cx_Oracle

# Connection details
username = "ds_user"
password = "dsuser123"
dsn = cx_Oracle.makedsn("localhost", "1521", service_name="orclpdb")

try:
    # Connect
    connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
    print("✅ Connection successful!")

    # Execute query
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM phones")
    count = cursor.fetchone()[0]
    print(f"✅ Found {count} phones in database")

    # Check users table
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]
    print(f"✅ Found {user_count} users in database")

    cursor.close()
    connection.close()

except cx_Oracle.Error as e:
    print(f"❌ Error: {e}")
```

**Run:**
```bash
python test_oracle_connection.py
```

---

## 📊 SQLAlchemy Connection String Format

### Oracle with cx_Oracle

```
oracle+cx_oracle://username:password@host:port/?service_name=service_name
```

### Examples:

```python
# Local development
oracle+cx_oracle://ds_user:dsuser123@localhost:1521/?service_name=orclpdb

# Remote server
oracle+cx_oracle://ds_user:dsuser123@192.168.1.100:1521/?service_name=orclpdb

# With SID instead of service name
oracle+cx_oracle://ds_user:dsuser123@localhost:1521/ORCL
```

---

## 🔐 Security Best Practices

### For Production:

1. **Use Environment Variables:**
   ```bash
   # .env
   ORACLE_USER=ds_user
   ORACLE_PASSWORD=your_secure_password
   ```

2. **Change Default Password:**
   ```sql
   ALTER USER ds_user IDENTIFIED BY "NewSecurePassword123!";
   ```

3. **Use Oracle Wallet:**
   - Store credentials securely
   - No hardcoded passwords

4. **Limit Permissions:**
   ```sql
   -- Grant only necessary privileges
   GRANT SELECT, INSERT, UPDATE, DELETE ON phones TO ds_user;
   GRANT SELECT, INSERT, UPDATE, DELETE ON users TO ds_user;
   ```

5. **Use Connection Pool:**
   Already configured in SQLAlchemy:
   ```python
   SQLALCHEMY_POOL_SIZE = 10
   SQLALCHEMY_MAX_OVERFLOW = 20
   ```

---

## 📈 Performance Optimization

### Oracle-Specific Settings

Add to `config.py`:

```python
# Oracle performance settings
SQLALCHEMY_POOL_SIZE = 10
SQLALCHEMY_POOL_TIMEOUT = 30
SQLALCHEMY_POOL_RECYCLE = 3600
SQLALCHEMY_MAX_OVERFLOW = 20

# Oracle echo SQL (development only)
SQLALCHEMY_ECHO = False  # Set True to see SQL queries
```

### Create Indexes

```sql
-- Index on email for faster lookups
CREATE INDEX idx_users_email ON users(email);

-- Index on email verification token
CREATE INDEX idx_users_email_token ON users(email_verification_token);

-- Index on password reset token
CREATE INDEX idx_users_reset_token ON users(password_reset_token);

-- Index on phone brand for filtering
CREATE INDEX idx_phones_brand ON phones(brand_id);

-- Index on phone price for sorting
CREATE INDEX idx_phones_price ON phones(price);
```

---

## 🎯 Differences from SQLite

### Data Types

| SQLite | Oracle | Notes |
|--------|--------|-------|
| `INTEGER` | `NUMBER` | Integers |
| `REAL` | `NUMBER` | Floating point |
| `TEXT` | `VARCHAR2` or `CLOB` | Strings |
| `BLOB` | `BLOB` | Binary data |
| `BOOLEAN` | `NUMBER(1)` | 0=False, 1=True |
| `DATETIME` | `TIMESTAMP` | Date and time |

### Auto-increment

**SQLite:**
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```

**Oracle:**
```sql
id NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
```

Or use sequences:
```sql
CREATE SEQUENCE user_seq START WITH 1;
CREATE TRIGGER user_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    :NEW.id := user_seq.NEXTVAL;
END;
```

### Case Sensitivity

- **Oracle:** Table/column names are UPPERCASE by default
- **SQLite:** Case-insensitive

**In SQLAlchemy:** Works transparently, but be aware when writing raw SQL.

---

## 📝 Common SQL Conversions

### Limit Results

**SQLite:**
```sql
SELECT * FROM phones LIMIT 10;
```

**Oracle:**
```sql
SELECT * FROM phones WHERE ROWNUM <= 10;

-- Or in Oracle 12c+
SELECT * FROM phones FETCH FIRST 10 ROWS ONLY;
```

### Date/Time Functions

**SQLite:**
```sql
SELECT datetime('now');
```

**Oracle:**
```sql
SELECT SYSDATE FROM DUAL;
SELECT SYSTIMESTAMP FROM DUAL;
```

### String Concatenation

**SQLite:**
```sql
SELECT first_name || ' ' || last_name FROM users;
```

**Oracle:**
```sql
SELECT first_name || ' ' || last_name FROM users;
-- Same syntax works!
```

---

## 🔄 Backup and Restore

### Backup Oracle Database

```bash
# Export schema
expdp ds_user/dsuser123@orclpdb \
    schemas=DS_USER \
    directory=DATA_PUMP_DIR \
    dumpfile=dialsmart_backup.dmp \
    logfile=dialsmart_backup.log
```

### Restore

```bash
impdp ds_user/dsuser123@orclpdb \
    schemas=DS_USER \
    directory=DATA_PUMP_DIR \
    dumpfile=dialsmart_backup.dmp \
    logfile=dialsmart_restore.log
```

---

## ✅ Verification Checklist

After migration, verify:

- [ ] cx_Oracle installed: `pip list | grep cx-Oracle`
- [ ] Migration completed successfully
- [ ] New columns exist: `DESCRIBE users`
- [ ] Existing users auto-verified: `SELECT COUNT(*) FROM users WHERE email_verified = 1`
- [ ] Application starts: `python run.py`
- [ ] Can login at http://localhost:5000
- [ ] All 692 phones visible
- [ ] Password reset works
- [ ] Email verification ready (when configured)

---

## 🚀 Summary

**To Complete Setup:**

```bash
# 1. Install Oracle driver
pip install cx-Oracle

# 2. Run migration
python migrate_oracle_database.py

# 3. Start application
python run.py

# 4. Test at http://localhost:5000
```

**Your configuration is ready!** The app will connect to:
- **User:** ds_user
- **Password:** dsuser123
- **Host:** localhost:1521
- **Service:** orclpdb
- **Phones:** 692 ✅

---

**Modified by:** Claude AI Assistant
**Date:** 2025-11-18
**Version:** 1.0 - Oracle Support
