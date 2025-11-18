# Oracle Database Setup Guide for DialSmart

This guide will help you set up Oracle Database as your database for DialSmart instead of SQLite.

## Why Oracle Database?

✅ **Enterprise Grade**: Industry-leading database for critical applications
✅ **High Performance**: Optimized for large datasets and complex queries
✅ **Advanced Security**: Built-in encryption, auditing, and access control
✅ **Scalability**: Handles millions of records efficiently
✅ **ACID Compliance**: Ensures data integrity and reliability
✅ **Professional**: Used by major corporations worldwide

---

## Part 1: Install Oracle Database

### Option A: Oracle Database XE (Express Edition) - FREE & Recommended

Oracle XE is free, lightweight, and perfect for development and small applications.

1. **Download Oracle Database XE**:
   - Go to: https://www.oracle.com/database/technologies/xe-downloads.html
   - Download: Oracle Database 21c Express Edition for Windows (64-bit)
   - You may need to create a free Oracle account

2. **Install Oracle Database XE**:
   - Run the installer: `OracleXE213_Win64.zip`
   - Extract and run `setup.exe`
   - **Password**: Set a strong password for SYS and SYSTEM accounts (remember this!)
   - Accept default settings (Port 1521, Service Name: XE)
   - Installation takes 5-10 minutes

3. **Verify Installation**:
   ```powershell
   # Check if Oracle services are running
   # Look for "OracleServiceXE" and "OracleXETNSListener"
   services.msc
   ```

4. **Test SQL*Plus Connection**:
   ```powershell
   # Open Command Prompt
   sqlplus system/your_password@localhost:1521/XE
   ```

   You should see:
   ```
   SQL*Plus: Release 21.0.0.0.0 - Production
   Connected to:
   Oracle Database 21c Express Edition Release 21.0.0.0.0 - Production
   ```

### Option B: Oracle Database Standard/Enterprise Edition

If you have Oracle Database Standard or Enterprise Edition installed:
- Default port: 1521
- Service name varies (e.g., ORCL, ORCLPDB1)
- Connect as SYSDBA or user with CREATE USER privileges

---

## Part 2: Create DialSmart User and Tablespace

### Using SQL*Plus:

1. **Connect as SYSTEM**:
   ```powershell
   sqlplus system/your_password@localhost:1521/XE
   ```

2. **For Oracle XE (Pluggable Database)**:
   ```sql
   -- Switch to the pluggable database
   ALTER SESSION SET CONTAINER = XEPDB1;

   -- Create tablespace for DialSmart
   CREATE TABLESPACE dialsmart_ts
   DATAFILE 'dialsmart_data.dbf' SIZE 100M
   AUTOEXTEND ON NEXT 10M MAXSIZE 500M;

   -- Create user
   CREATE USER dialsmart_user IDENTIFIED BY dialsmart123
   DEFAULT TABLESPACE dialsmart_ts
   QUOTA UNLIMITED ON dialsmart_ts;

   -- Grant privileges
   GRANT CONNECT, RESOURCE TO dialsmart_user;
   GRANT CREATE SESSION TO dialsmart_user;
   GRANT CREATE TABLE TO dialsmart_user;
   GRANT CREATE VIEW TO dialsmart_user;
   GRANT CREATE SEQUENCE TO dialsmart_user;

   -- Verify user was created
   SELECT username FROM dba_users WHERE username = 'DIALSMART_USER';

   -- Exit
   EXIT;
   ```

3. **For Oracle Standard/Enterprise (Non-CDB)**:
   ```sql
   -- Create tablespace
   CREATE TABLESPACE dialsmart_ts
   DATAFILE 'dialsmart_data.dbf' SIZE 100M
   AUTOEXTEND ON NEXT 10M MAXSIZE 500M;

   -- Create user
   CREATE USER dialsmart_user IDENTIFIED BY dialsmart123
   DEFAULT TABLESPACE dialsmart_ts
   QUOTA UNLIMITED ON dialsmart_ts;

   -- Grant privileges
   GRANT CONNECT, RESOURCE TO dialsmart_user;
   GRANT CREATE SESSION TO dialsmart_user;
   GRANT CREATE TABLE TO dialsmart_user;
   GRANT CREATE VIEW TO dialsmart_user;
   GRANT CREATE SEQUENCE TO dialsmart_user;

   -- Exit
   EXIT;
   ```

4. **Test User Connection**:
   ```powershell
   # For Oracle XE (Pluggable Database)
   sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1

   # For Non-CDB Oracle
   sqlplus dialsmart_user/dialsmart123@localhost:1521/XE
   ```

---

## Part 3: Install Python Oracle Driver

1. **Install oracledb (Modern Python Driver)**:
   ```powershell
   pip install oracledb
   ```

   Or install all requirements:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```powershell
   python -c "import oracledb; print('Oracle driver installed successfully! Version:', oracledb.__version__)"
   ```

**Note**: The new `oracledb` driver works in "Thin mode" by default, which means **you don't need Oracle Client libraries installed**! This makes setup much easier.

### Troubleshooting Installation Issues (Python 3.14+)

If you get an error about "Microsoft Visual C++ 14.0 or greater is required":

**Option 1: Install Latest Version (Recommended)**
```powershell
# Install the latest version which has better compatibility
pip install --upgrade oracledb
```

**Option 2: Install Microsoft C++ Build Tools**
1. Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Install "Desktop development with C++"
3. Retry: `pip install oracledb`

**Option 3: Use Pre-built Wheel (If available)**
```powershell
# Check available versions with wheels
pip install oracledb --only-binary :all:
```

---

## Part 4: Configure DialSmart to Use Oracle

### Method 1: Environment Variable (Recommended)

Create a `.env` file in your project root:

```bash
# .env file
DB_TYPE=oracle
ORACLE_USER=dialsmart_user
ORACLE_PASSWORD=dialsmart123
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=XEPDB1
```

**Important**:
- For Oracle XE Pluggable Database, use `ORACLE_SERVICE=XEPDB1`
- For Oracle XE non-pluggable, use `ORACLE_SERVICE=XE`
- For other Oracle versions, check your service name with: `lsnrctl status`

### Method 2: Direct Configuration (Simpler)

Edit `config.py` and change line 40:

```python
# Change from:
DB_TYPE = os.environ.get('DB_TYPE', 'sqlite').lower()

# To:
DB_TYPE = 'oracle'  # Forces Oracle connection
```

Also update the Oracle credentials (lines 32-36) if different:

```python
ORACLE_USER = 'dialsmart_user'
ORACLE_PASSWORD = 'dialsmart123'  # Use your actual password
ORACLE_HOST = 'localhost'
ORACLE_PORT = '1521'
ORACLE_SERVICE = 'XEPDB1'  # Change if using different service
```

---

## Part 5: Create Database Tables

Run this command to create all tables in Oracle:

```powershell
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✓ Oracle tables created successfully!')"
```

You should see: `✓ Oracle tables created successfully!`

---

## Part 6: Import Your Phone Data

### If You Have SQLite Data (Migration):

Run the Oracle migration script:

```powershell
python migrate_sqlite_to_oracle.py
```

This will copy all data from your SQLite database to Oracle.

### If Starting Fresh:

Import from CSV:

```powershell
python import_csv_dataset.py
```

Or initialize with sample data:

```powershell
python initialize_system.py
```

---

## Part 7: Verify Oracle Connection

Test that everything works:

```powershell
python test_oracle_connection.py
```

Or start your application:

```powershell
python run.py
```

If you see the Flask startup message without errors, Oracle is connected!

---

## Verify Data in Oracle

### Using SQL*Plus:

```powershell
# Connect to Oracle
sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1
```

```sql
-- Show all tables
SELECT table_name FROM user_tables;

-- Count phones
SELECT COUNT(*) FROM phones;

-- Count brands
SELECT COUNT(*) FROM brands;

-- Show sample phones
SELECT id, model_name, price FROM phones WHERE ROWNUM <= 5;

-- Show table structure
DESCRIBE phones;

-- Exit
EXIT;
```

### Using Oracle SQL Developer (Visual Tool):

1. Download SQL Developer from: https://www.oracle.com/database/sqldeveloper/
2. Create new connection:
   - Name: DialSmart
   - Username: dialsmart_user
   - Password: dialsmart123
   - Hostname: localhost
   - Port: 1521
   - Service name: XEPDB1
3. Click "Test" then "Connect"
4. Browse tables in the left panel

---

## Troubleshooting

### Error: "ORA-12154: TNS:could not resolve the connect identifier"

**Solutions**:
1. Check service name is correct (XEPDB1 for Oracle XE, or XE for older versions)
2. Verify listener is running:
   ```powershell
   lsnrctl status
   ```
3. Check `tnsnames.ora` file or use full connection string

### Error: "ORA-01017: invalid username/password"

**Solutions**:
1. Verify username and password in `config.py`
2. Test login via SQL*Plus:
   ```powershell
   sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1
   ```
3. Reset password if needed:
   ```sql
   sqlplus system/system_password@localhost:1521/XE
   ALTER SESSION SET CONTAINER = XEPDB1;
   ALTER USER dialsmart_user IDENTIFIED BY new_password;
   ```

### Error: "ORA-12541: TNS:no listener"

**Solutions**:
1. Start the Oracle listener:
   ```powershell
   lsnrctl start
   ```
2. Check Oracle services are running:
   - OracleServiceXE
   - OracleXETNSListener
3. Restart services if needed

### Error: "DPI-1047: Cannot locate a 64-bit Oracle Client library"

**Solution**: This error shouldn't occur with the new `oracledb` driver in Thin mode. If you see this:
1. Make sure you installed `oracledb` (not the old `cx_Oracle`)
2. The new driver doesn't require Oracle Client installation

### Error: "ORA-01950: no privileges on tablespace"

**Solution**: Grant quota on tablespace:
```sql
sqlplus system/system_password@localhost:1521/XE
ALTER SESSION SET CONTAINER = XEPDB1;
ALTER USER dialsmart_user QUOTA UNLIMITED ON dialsmart_ts;
EXIT;
```

### Error: "No module named 'oracledb'"

**Solution**: Install the Oracle driver:
```powershell
pip install oracledb==2.0.1
```

---

## Oracle Configuration Tips

### Check Oracle Version:

```sql
SELECT * FROM v$version;
```

### Check Service Name:

```powershell
lsnrctl status
```

Look for "Service" entries like `XEPDB1` or `XE`.

### Increase Tablespace Size (if needed):

```sql
ALTER DATABASE DATAFILE 'dialsmart_data.dbf' RESIZE 500M;
```

### Enable Query Logging (For Debugging):

```sql
-- Enable SQL trace for session
ALTER SESSION SET SQL_TRACE = TRUE;

-- Or enable auditing
AUDIT SELECT TABLE, INSERT TABLE, UPDATE TABLE, DELETE TABLE BY dialsmart_user;
```

### View Active Sessions:

```sql
SELECT username, status, machine, program
FROM v$session
WHERE username = 'DIALSMART_USER';
```

---

## Performance Optimization

### Create Indexes (After Data Import):

```sql
-- Login as dialsmart_user
sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1

-- Create indexes on frequently queried columns
CREATE INDEX idx_phones_brand ON phones(brand_id);
CREATE INDEX idx_phones_price ON phones(price);
CREATE INDEX idx_phones_active ON phones(is_active);
CREATE INDEX idx_specs_5g ON phone_specifications(has_5g);

-- Exit
EXIT;
```

### Gather Statistics:

```sql
EXEC DBMS_STATS.GATHER_SCHEMA_STATS('DIALSMART_USER');
```

---

## Benefits of Oracle Database

After switching to Oracle:

✅ **Enterprise Performance**: Optimized query execution and caching
✅ **Advanced Security**: Row-level security, encryption, auditing
✅ **High Availability**: Built-in backup, recovery, and replication
✅ **Scalability**: Handles millions of records with ease
✅ **Professional Tools**: SQL Developer, Enterprise Manager, SQL*Plus
✅ **Data Integrity**: Advanced constraints and triggers
✅ **Industry Standard**: Used by Fortune 500 companies

---

## Quick Reference

### Start Oracle Services (Windows):
```powershell
net start OracleServiceXE
net start OracleXETNSListener
```

### Stop Oracle Services:
```powershell
net stop OracleXETNSListener
net stop OracleServiceXE
```

### Connect with SQL*Plus:
```powershell
# As SYSTEM
sqlplus system/password@localhost:1521/XE

# As DialSmart user (Pluggable DB)
sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1

# As DialSmart user (Non-CDB)
sqlplus dialsmart_user/dialsmart123@localhost:1521/XE
```

### Export Data (Backup):
```powershell
# Using Data Pump
expdp dialsmart_user/dialsmart123@localhost:1521/XEPDB1 directory=DATA_PUMP_DIR dumpfile=dialsmart_backup.dmp

# Using SQL*Plus
sqlplus dialsmart_user/dialsmart123@localhost:1521/XEPDB1
SPOOL dialsmart_backup.sql
-- Run your SELECT statements
SPOOL OFF
EXIT
```

### Import Data (Restore):
```powershell
# Using Data Pump
impdp dialsmart_user/dialsmart123@localhost:1521/XEPDB1 directory=DATA_PUMP_DIR dumpfile=dialsmart_backup.dmp
```

---

## Summary: Complete Setup Steps

1. ✅ Install Oracle Database XE (Free download from Oracle.com)
2. ✅ Create `dialsmart_user` and tablespace using SQL*Plus
3. ✅ Install oracledb: `pip install oracledb`
4. ✅ Update `config.py`: Set `DB_TYPE = 'oracle'`
5. ✅ Update Oracle service name (XEPDB1 for XE Pluggable DB)
6. ✅ Create tables: Run Python command to create tables
7. ✅ Import data: Run `import_csv_dataset.py` or migration script
8. ✅ Test: Run `python run.py` and verify connection

Your DialSmart system is now running on Oracle Database! 🎉

---

## Important Notes for Oracle XE

**Pluggable Database (PDB)**:
- Oracle XE 18c and later use Pluggable Databases
- Default PDB name: `XEPDB1`
- Always use `XEPDB1` as the service name in your connection
- To switch containers in SQL*Plus: `ALTER SESSION SET CONTAINER = XEPDB1;`

**Resource Limits (Oracle XE)**:
- Max 2 CPU threads
- Max 2 GB RAM
- Max 12 GB user data
- Perfect for development and small applications
- For larger deployments, consider Oracle Standard or Enterprise Edition

---

## Contact Support

If you encounter issues not covered here, check:
- Oracle Documentation: https://docs.oracle.com/en/database/
- Oracle Community: https://community.oracle.com/
- SQLAlchemy Oracle Guide: https://docs.sqlalchemy.org/en/20/dialects/oracle.html

For DialSmart-specific Oracle issues, refer to the project documentation.
