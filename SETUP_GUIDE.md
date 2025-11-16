# DialSmart - Complete Setup Guide

This guide will help you set up and run the DialSmart Phone Recommendation Platform on your local machine.

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Project Setup](#project-setup)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Importing Data](#importing-data)
7. [Testing Features](#testing-features)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.11 or higher**
   - Download from: https://www.python.org/downloads/
   - During installation, **check "Add Python to PATH"**
   - Verify installation: Open Command Prompt and run:
     ```bash
     python --version
     ```

2. **Oracle Database 11g or higher**
   - You should already have Oracle installed
   - Ensure Oracle service is running
   - Know your Oracle connection details:
     - Username (e.g., `ds_user`)
     - Password (e.g., `dsuser123`)
     - Host (usually `localhost`)
     - Port (usually `1521`)
     - Service name (e.g., `ORCLPDB` or `XE`)

3. **Git**
   - Download from: https://git-scm.com/downloads
   - Verify installation:
     ```bash
     git --version
     ```

---

## Project Setup

### Step 1: Clone the Repository

Open Command Prompt and navigate to where you want the project:

```bash
cd C:\Users\YourName\Documents
git clone https://github.com/AlisonOoi123/DialSmart.git
cd DialSmart
```

### Step 2: Create Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
```

Activate the virtual environment:
- **Windows:**
  ```bash
  venv\Scripts\activate
  ```
- **Mac/Linux:**
  ```bash
  source venv/bin/activate
  ```

You should see `(venv)` at the start of your command prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Flask (web framework)
- SQLAlchemy (database ORM)
- cx_Oracle (Oracle database driver)
- And more...

---

## Database Setup

### Step 1: Start Oracle Database

1. Open **Services** (Windows key + R, type `services.msc`)
2. Find services starting with **"Oracle"**
3. Make sure these are **Running**:
   - OracleServiceORCL (or similar)
   - OracleOraDB21Home1TNSListener (or similar)

Alternatively, use SQL*Plus or SQL Developer to verify connection.

### Step 2: Create Database User (if not exists)

Open SQL*Plus or SQL Developer and run:

```sql
-- Connect as SYSDBA first
sqlplus / as sysdba

-- Create user
CREATE USER ds_user IDENTIFIED BY dsuser123;

-- Grant privileges
GRANT CONNECT, RESOURCE, DBA TO ds_user;
GRANT CREATE SESSION TO ds_user;
GRANT CREATE TABLE TO ds_user;
GRANT CREATE SEQUENCE TO ds_user;
GRANT CREATE TRIGGER TO ds_user;
GRANT UNLIMITED TABLESPACE TO ds_user;

-- Verify user created
SELECT username FROM dba_users WHERE username = 'DS_USER';
```

### Step 3: Verify Database Connection

From the DialSmart project folder:

```bash
python
```

Then in Python:

```python
import cx_Oracle
try:
    conn = cx_Oracle.connect('ds_user/dsuser123@localhost:1521/ORCLPDB')
    print("✓ Database connection successful!")
    conn.close()
except Exception as e:
    print(f"✗ Connection failed: {e}")
exit()
```

If you see "✓ Database connection successful!", you're good to go!

---

## Configuration

### Step 1: Update Database Configuration

Open `config.py` in a text editor and verify these settings:

```python
# Oracle Database connection
ORACLE_USER = 'ds_user'           # Your Oracle username
ORACLE_PASSWORD = 'dsuser123'      # Your Oracle password
ORACLE_HOST = 'localhost'          # Usually localhost
ORACLE_PORT = '1521'               # Usually 1521
ORACLE_SERVICE = 'ORCLPDB'         # Your Oracle service name

# Database type
DB_TYPE = 'oracle'                 # Keep as 'oracle'
```

**Important:** Change these values to match YOUR Oracle setup!

### Step 2: Create Environment File (Optional)

Create a `.env` file in the project root (optional, for sensitive data):

```
SECRET_KEY=your-secret-key-here
ORACLE_USER=ds_user
ORACLE_PASSWORD=dsuser123
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE=ORCLPDB
```

---

## Running the Application

### Step 1: Initialize Database Tables

The first time you run the application, it will automatically create all tables.

```bash
python run.py
```

Wait for the message:
```
* Running on http://127.0.0.1:5000
```

**Important:** Let it run for 30-60 seconds on first launch to create all tables.

Press `CTRL+C` to stop, then check if tables were created:

```sql
-- In SQL*Plus or SQL Developer
SELECT table_name FROM user_tables WHERE table_name LIKE 'USERS' OR table_name LIKE 'PHONES';
```

You should see tables like: `USERS`, `PHONES`, `BRANDS`, `PHONE_SPECIFICATIONS`, etc.

### Step 2: Run the Application

```bash
python run.py
```

You should see:
```
* Serving Flask app 'app'
* Debug mode: on
* Running on http://127.0.0.1:5000
```

### Step 3: Access the Application

Open your web browser and go to:
```
http://127.0.0.1:5000
```

You should see the DialSmart homepage!

---

## Importing Data

The database needs phone data to work properly. If you don't have data yet:

### Step 1: Import Phone Data from CSV

Make sure your CSV file is in the `data/` folder:
- File name: `fyp_phoneDataset.csv`
- Location: `C:\...\DialSmart\data\fyp_phoneDataset.csv`

Run the import script:

```bash
python scripts/import/update_missing_specs_from_csv.py
```

You should see:
```
✓ Updated: Apple iPhone 15 Plus
✓ Updated: Samsung Galaxy S24
...
✅ Successfully updated X phones
```

### Step 2: Create Admin Account

To access the admin panel, you need to create an admin user.

**Option A: Via Web Interface**
1. Go to http://127.0.0.1:5000/register
2. Create an account
3. Then manually update the database:

```sql
UPDATE users SET role = 'admin' WHERE email = 'your-email@example.com';
COMMIT;
```

**Option B: Via SQL Directly**

```sql
INSERT INTO users (id, username, email, password_hash, role, is_active, created_at)
VALUES (
    users_seq.NEXTVAL,
    'admin',
    'admin@dialsmart.com',
    'scrypt:32768:8:1$...',  -- You'll need to generate this
    'admin',
    1,
    SYSDATE
);
COMMIT;
```

---

## Testing Features

### Test User Features

1. **Homepage** - http://127.0.0.1:5000
2. **Find Phone (Wizard)** - Click "Find Your Phone" → Answer questions
3. **Chatbot** - Click chatbot icon (bottom right) → Try:
   - "I want a gaming phone"
   - "Show me phones with good camera"
   - "Phones under RM3000"
4. **Compare Phones** - Navigation → Compare → Select 2 phones
5. **Browse Phones** - Navigation → All Phones

### Test Admin Features

Login as admin, then access:

1. **Admin Dashboard** - http://127.0.0.1:5000/admin/dashboard
2. **Manage Phones** - Add/Edit/Delete phones
3. **Manage Brands** - Add/Edit brands
4. **Contact Messages** - View messages from contact form
5. **User Management** - View registered users

---

## Troubleshooting

### Common Issues

#### 1. ModuleNotFoundError: No module named 'flask'

**Solution:** Install dependencies
```bash
pip install -r requirements.txt
```

#### 2. Oracle connection refused / DPY-6005 error

**Solution:**
- Check Oracle service is running (Services → OracleServiceORCL)
- Verify connection details in `config.py`
- Test with SQL*Plus: `sqlplus ds_user/dsuser123@localhost:1521/ORCLPDB`

#### 3. ORA-01017: invalid username/password

**Solution:**
- Verify username and password in `config.py`
- Create user if it doesn't exist (see Database Setup Step 2)

#### 4. ORA-12899: value too large for column

**Solution:**
- This happens during CSV import if data is too long
- The import script automatically truncates long values
- Make sure you're using the latest version: `git pull`

#### 5. Port 5000 already in use

**Solution:**
- Another application is using port 5000
- Kill the process or change port in `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001
```

#### 6. Static files not loading (CSS/images missing)

**Solution:**
- Check `static/` folder exists
- Clear browser cache (CTRL+F5)
- Check browser console for errors (F12)

#### 7. Database tables not created

**Solution:**
```bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
...     print("Tables created!")
>>> exit()
```

#### 8. Chatbot not responding

**Solution:**
- Check browser console (F12) for errors
- Verify `/api/chat` endpoint is working
- Check `static/js/chatbot.js` exists
- Ensure you're logged in (chatbot requires login)

---

## Project Structure

```
DialSmart/
├── app/
│   ├── __init__.py           # App initialization
│   ├── models/               # Database models
│   ├── routes/               # URL routes
│   ├── modules/              # Core logic (AI, chatbot, comparison)
│   ├── templates/            # HTML templates
│   ├── static/               # CSS, JS, images
│   └── utils/                # Helper functions
├── data/
│   └── fyp_phoneDataset.csv  # Phone data CSV
├── scripts/
│   └── import/               # Data import scripts
├── sql/                      # SQL scripts
├── config.py                 # Configuration
├── run.py                    # Main application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project README
```

---

## Important URLs

Once running, access these URLs:

- **Homepage:** http://127.0.0.1:5000
- **Find Phone:** http://127.0.0.1:5000/phone/find
- **Compare:** http://127.0.0.1:5000/phone/compare
- **Admin Dashboard:** http://127.0.0.1:5000/admin/dashboard
- **Login:** http://127.0.0.1:5000/login
- **Register:** http://127.0.0.1:5000/register

---

## Getting Help

If you encounter issues:

1. **Check this guide** - Most common issues are covered above
2. **Check terminal output** - Error messages often explain the problem
3. **Check browser console** - Press F12 → Console tab
4. **Check database connection** - Verify Oracle is running
5. **Check file permissions** - Make sure you can read/write in the project folder

---

## Next Steps

After successful setup:

1. ✅ Import phone data from CSV
2. ✅ Create admin account
3. ✅ Test all features (wizard, chatbot, comparison)
4. ✅ Add your own phone data via admin panel
5. ✅ Customize branding in `templates/base.html`
6. ✅ Deploy to production server (if needed)

---

## Security Notes

**Before deploying to production:**

1. Change `SECRET_KEY` in `config.py` to a random string
2. Set `DEBUG = False` in `run.py`
3. Use environment variables for sensitive data (`.env` file)
4. Update Oracle password to something secure
5. Enable HTTPS if deploying online
6. Regular database backups

---

## Contact

For questions or issues:
- Project Repository: https://github.com/AlisonOoi123/DialSmart
- Create an issue on GitHub with error details

---

**Good luck! 🚀**

If everything is set up correctly, you should see the DialSmart homepage and be able to use all features including the intelligent chatbot, phone comparison, and recommendation wizard!
