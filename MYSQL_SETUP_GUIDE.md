# MySQL Database Setup Guide for DialSmart

This guide will help you set up MySQL as your database for DialSmart instead of SQLite.

## Why MySQL?

✅ **Better Performance**: Handles large datasets efficiently
✅ **Multi-user Support**: Multiple users can access simultaneously
✅ **Production Ready**: Industry-standard for web applications
✅ **Better Data Integrity**: ACID compliance and transactions
✅ **Scalable**: Can grow with your application

---

## Part 1: Install MySQL Server

### Option A: Install MySQL on Windows (Recommended for You)

1. **Download MySQL Installer**:
   - Go to: https://dev.mysql.com/downloads/installer/
   - Download: `mysql-installer-community-8.0.xx.msi` (Web or Full installer)

2. **Run the Installer**:
   - Choose "Custom" or "Developer Default"
   - Select at minimum:
     - MySQL Server 8.0
     - MySQL Workbench (optional, but recommended for visual management)
   - Click "Execute" to install

3. **Configure MySQL Server**:
   - **Type and Networking**: Keep defaults (Port 3306)
   - **Authentication Method**: Use Strong Password Encryption (Recommended)
   - **Root Password**: Set a strong password (remember this!)
   - **Windows Service**: ✓ Configure MySQL Server as Windows Service
   - **Start at System Startup**: ✓ Enabled
   - Click "Execute" to apply configuration

4. **Verify Installation**:
   ```powershell
   # Open Command Prompt or PowerShell
   mysql --version
   ```
   You should see: `mysql  Ver 8.0.xx...`

### Option B: Install Using XAMPP (Easier Alternative)

If you already have XAMPP or want an easier option:

1. Download XAMPP from: https://www.apachefriends.org/
2. Install XAMPP
3. Open XAMPP Control Panel
4. Start "MySQL" service
5. MySQL is now running on port 3306

---

## Part 2: Create DialSmart Database

### Using MySQL Command Line:

1. **Open MySQL Command Line**:
   ```powershell
   # Login as root
   mysql -u root -p
   # Enter your MySQL root password
   ```

2. **Create Database and User**:
   ```sql
   -- Create the database
   CREATE DATABASE dialsmart CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   -- Create a dedicated user for DialSmart
   CREATE USER 'dialsmart_user'@'localhost' IDENTIFIED BY 'dialsmart123';

   -- Grant all privileges on the database to the user
   GRANT ALL PRIVILEGES ON dialsmart.* TO 'dialsmart_user'@'localhost';

   -- Apply the changes
   FLUSH PRIVILEGES;

   -- Verify the database was created
   SHOW DATABASES;

   -- Exit MySQL
   EXIT;
   ```

### Using MySQL Workbench (Visual Tool):

1. Open MySQL Workbench
2. Connect to your MySQL server (root user)
3. Click "Create New Schema" button
4. Name: `dialsmart`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

---

## Part 3: Install Python MySQL Driver

1. **Install PyMySQL**:
   ```powershell
   pip install PyMySQL==1.1.0
   ```

   Or install all requirements:
   ```powershell
   pip install -r requirements.txt
   ```

2. **Verify Installation**:
   ```powershell
   python -c "import pymysql; print('PyMySQL installed successfully!')"
   ```

---

## Part 4: Configure DialSmart to Use MySQL

### Method 1: Environment Variable (Recommended)

Create a `.env` file in your project root:

```bash
# .env file
USE_MYSQL=true
MYSQL_USER=dialsmart_user
MYSQL_PASSWORD=dialsmart123
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DATABASE=dialsmart
```

### Method 2: Direct Configuration (Simpler)

Edit `config.py` and change line 31:

```python
# Change from:
USE_MYSQL = os.environ.get('USE_MYSQL', 'false').lower() == 'true'

# To:
USE_MYSQL = True  # Forces MySQL connection
```

Also update the credentials (lines 24-28) if different:

```python
MYSQL_USER = 'dialsmart_user'
MYSQL_PASSWORD = 'dialsmart123'  # Use your actual password
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DATABASE = 'dialsmart'
```

---

## Part 5: Create Database Tables

Run this command to create all tables in MySQL:

```powershell
python -c "from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('✓ MySQL tables created successfully!')"
```

You should see: `✓ MySQL tables created successfully!`

---

## Part 6: Import Your Phone Data

### If You Have SQLite Data (Migration):

Run the migration script:

```powershell
python migrate_sqlite_to_mysql.py
```

This will copy all data from your SQLite database to MySQL.

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

## Part 7: Verify MySQL Connection

Test that everything works:

```powershell
python test_mysql_connection.py
```

Or start your application:

```powershell
python run.py
```

If you see the Flask startup message without errors, MySQL is connected!

---

## Verify Data in MySQL

### Using MySQL Command Line:

```powershell
mysql -u dialsmart_user -p
```

```sql
USE dialsmart;

-- Show all tables
SHOW TABLES;

-- Count phones
SELECT COUNT(*) FROM phones;

-- Count brands
SELECT COUNT(*) FROM brands;

-- Show sample phones
SELECT id, model_name, price FROM phones LIMIT 5;

-- Exit
EXIT;
```

### Using MySQL Workbench:

1. Connect to localhost
2. Double-click `dialsmart` database
3. Click "Tables" to see all tables
4. Right-click any table → "Select Rows" to view data

---

## Troubleshooting

### Error: "Access denied for user"

**Solution**: Check username and password in `config.py`

```powershell
# Test MySQL login
mysql -u dialsmart_user -p
# Enter: dialsmart123
```

### Error: "Can't connect to MySQL server"

**Solutions**:
1. Check if MySQL service is running:
   - Windows Services → MySQL80 → Should be "Running"
   - Or use XAMPP Control Panel
2. Check port 3306 is not blocked by firewall
3. Verify MySQL is listening on localhost:
   ```powershell
   netstat -an | findstr 3306
   ```

### Error: "Unknown database 'dialsmart'"

**Solution**: Create the database:

```sql
mysql -u root -p
CREATE DATABASE dialsmart;
EXIT;
```

### Error: "No module named 'pymysql'"

**Solution**: Install PyMySQL:

```powershell
pip install PyMySQL==1.1.0
```

### Error: "Table already exists"

**Solution**: Tables already created. Skip table creation and import data directly.

---

## MySQL Configuration Tips

### Increase Max Connections (Optional):

Edit MySQL config file (`my.ini` or `my.cnf`):

```ini
[mysqld]
max_connections = 200
max_allowed_packet = 64M
```

Restart MySQL service after changes.

### Enable Query Logging (For Debugging):

```sql
SET GLOBAL general_log = 'ON';
SET GLOBAL log_output = 'TABLE';

-- View queries
SELECT * FROM mysql.general_log ORDER BY event_time DESC LIMIT 100;
```

---

## Benefits You'll See

After switching to MySQL:

✅ **Faster Queries**: Especially with 100+ phones
✅ **Better Concurrency**: Multiple users can browse simultaneously
✅ **Data Safety**: Built-in backup and recovery
✅ **Professional**: Industry-standard database
✅ **Scalable**: Can handle thousands of phones

---

## Quick Reference

### Start MySQL (Windows Service):
```powershell
net start MySQL80
```

### Stop MySQL:
```powershell
net stop MySQL80
```

### Backup Database:
```powershell
mysqldump -u dialsmart_user -p dialsmart > backup.sql
```

### Restore Database:
```powershell
mysql -u dialsmart_user -p dialsmart < backup.sql
```

### Access MySQL:
```powershell
mysql -u dialsmart_user -p
# Password: dialsmart123
```

---

## Summary: Complete Setup Steps

1. ✅ Install MySQL Server (Download from MySQL.com or use XAMPP)
2. ✅ Create `dialsmart` database and `dialsmart_user`
3. ✅ Install PyMySQL: `pip install PyMySQL`
4. ✅ Update `config.py`: Set `USE_MYSQL = True`
5. ✅ Create tables: Run Python command to create tables
6. ✅ Import data: Run `import_csv_dataset.py` or migration script
7. ✅ Test: Run `python run.py` and verify connection

Your DialSmart system is now running on MySQL! 🎉

---

## Contact Support

If you encounter issues not covered here, check:
- MySQL Documentation: https://dev.mysql.com/doc/
- Flask-SQLAlchemy MySQL Guide: https://flask-sqlalchemy.palletsprojects.com/

For DialSmart-specific MySQL issues, refer to the project documentation.
