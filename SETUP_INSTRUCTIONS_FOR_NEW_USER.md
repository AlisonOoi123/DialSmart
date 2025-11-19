# DialSmart Setup Instructions for New Users

## Prerequisites
✅ Oracle SQL*Plus database installed and running
✅ Python 3.8+ installed
✅ Git installed

---

## Step-by-Step Setup Guide

### 1. Clone the Project

```bash
cd C:\Users\User\OneDrive\Documents\GitHub\
git clone https://github.com/AlisonOoi123/DialSmart.git
cd DialSmart
```

---

### 2. Checkout the Correct Branch

```bash
# Fetch all branches from remote
git fetch --all

# Checkout the branch with all features
git checkout claude/dialsmart-python-system-01Qv2n5kr4dUSV8HUagf8ueS
git pull origin claude/dialsmart-python-system-01Qv2n5kr4dUSV8HUagf8ueS
```

---

### 3. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

---

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**If installation fails, try installing cx_Oracle separately:**
```bash
pip install cx_Oracle==8.3.0
pip install -r requirements.txt
```

---

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Copy the example
copy env.example .env

# Edit .env with your details
```

**Required `.env` configuration:**

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this
FLASK_ENV=development
DEBUG=True

# Oracle Database Configuration
DATABASE_TYPE=oracle
ORACLE_USER=your_oracle_username
ORACLE_PASSWORD=your_oracle_password
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=your_service_name
# OR use SID instead:
# ORACLE_SID=your_sid

# Full connection string (Oracle will use this)
DATABASE_URL=oracle+cx_oracle://your_oracle_username:your_oracle_password@localhost:1521/?service_name=your_service_name

# Admin Passkey (for first admin registration)
ADMIN_PASSKEY=DialSmart2024Admin!

# Email Configuration (Optional - for password reset)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
```

**Example with actual values:**
```env
SECRET_KEY=my-super-secret-key-12345
FLASK_ENV=development
DEBUG=True

DATABASE_TYPE=oracle
ORACLE_USER=dialsmart
ORACLE_PASSWORD=password123
ORACLE_HOST=localhost
ORACLE_PORT=1521
ORACLE_SERVICE_NAME=XEPDB1

DATABASE_URL=oracle+cx_oracle://dialsmart:password123@localhost:1521/?service_name=XEPDB1

ADMIN_PASSKEY=DialSmart2024Admin!
```

---

### 6. Set Up Oracle Database

#### 6.1 Create Oracle User (if not exists)

Open SQL*Plus as SYSDBA:
```bash
sqlplus / as sysdba
```

Run:
```sql
-- Connect to your PDB (if using multitenant)
ALTER SESSION SET CONTAINER = XEPDB1;

-- Create user
CREATE USER dialsmart IDENTIFIED BY password123;

-- Grant privileges
GRANT CONNECT, RESOURCE, CREATE TABLE, CREATE SEQUENCE, CREATE VIEW TO dialsmart;
GRANT UNLIMITED TABLESPACE TO dialsmart;

-- Exit
EXIT;
```

#### 6.2 Create Database Tables

```bash
# Activate virtual environment first
.\venv\Scripts\activate

# Run the application once to create tables
python run.py
```

Press `Ctrl+C` after you see "Running on http://..." to stop it.

#### 6.3 Run Database Migrations

```bash
# Navigate to migrations folder
cd migrations

# Connect to Oracle and run migrations
sqlplus dialsmart/password123@localhost:1521/XEPDB1

# In SQL*Plus, run each migration:
@001_add_admin_management_columns.sql
@002_create_audit_logs_table.sql
@004_allow_guest_chatbot_users.sql

# Exit SQL*Plus
EXIT;

# Go back to project root
cd ..
```

---

### 7. Import Phone Data

```bash
# Make sure you're in the project root with venv activated

# Import phones from CSV
python import_phones_from_csv.py

# OR use the more comprehensive import script:
python scripts/import/update_missing_specs_from_csv.py
```

**Expected output:**
```
Connecting to database...
Reading CSV file: data/fyp_phoneDataset.csv
Found XXX phones in CSV
Importing phones...
✓ Successfully imported XXX phones
```

---

### 8. Train Chatbot Model

```bash
# Clear any existing cache first (Windows)
FOR /d /r . %d IN (__pycache__) DO @IF EXIST "%d" rd /s /q "%d"

# Linux/Mac:
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null

# Train the chatbot model
python train_chatbot_model.py
```

**Expected output:**
```
Loading training data...
Training model...
Model accuracy: XX%
Model saved successfully!
```

**Note:** Training may take 2-5 minutes depending on your computer.

---

### 9. Create Admin Account

```bash
python create_admin.py
```

**You'll be prompted for:**
- Full Name
- Email
- Password (must be strong: 8+ chars, uppercase, lowercase, number, special char)
- Confirm Password

**Example:**
```
Full Name: Admin User
Email: admin@dialsmart.com
Password: Admin@123
Confirm Password: Admin@123

✓ Admin user created successfully!
```

---

### 10. Run the Application

```bash
python run.py
```

**You should see:**
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000
Press CTRL+C to quit
```

---

### 11. Access the Application

Open your browser and go to:
- **Homepage:** http://localhost:5000
- **Admin Login:** http://localhost:5000/auth/login

**Test Accounts:**
- **Admin:** Use the account you created in Step 9
- **User:** Register a new user account at http://localhost:5000/auth/register

---

## 🎯 Quick Start (After Initial Setup)

Every time you want to run the project:

```bash
# 1. Navigate to project
cd C:\Users\User\OneDrive\Documents\GitHub\DialSmart

# 2. Activate virtual environment
.\venv\Scripts\activate

# 3. Run the application
python run.py
```

---

## 🔧 Troubleshooting

### Issue 1: `cx_Oracle.DatabaseError: DPI-1047: Cannot locate a 64-bit Oracle Client library`

**Solution:**
1. Download Oracle Instant Client from: https://www.oracle.com/database/technologies/instant-client/downloads.html
2. Extract to `C:\oracle\instantclient_21_X`
3. Add to PATH environment variable
4. Restart your terminal

### Issue 2: `Cannot connect to Oracle database`

**Solution:**
```bash
# Test Oracle connection
sqlplus dialsmart/password123@localhost:1521/XEPDB1

# If successful, check your .env file DATABASE_URL
```

### Issue 3: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 4: `No phones found in database`

**Solution:**
```bash
# Re-import phone data
python import_phones_from_csv.py

# Verify import
python
>>> from app import db, create_app
>>> app = create_app()
>>> with app.app_context():
...     from app.models.phone import Phone
...     print(Phone.query.count())
>>> # Should show number of phones
```

### Issue 5: Chatbot not responding properly

**Solution:**
```bash
# Retrain chatbot model
python train_chatbot_model.py

# Clear cache
FOR /d /r . %d IN (__pycache__) DO @IF EXIST "%d" rd /s /q "%d"

# Restart application
python run.py
```

### Issue 6: Port 5000 already in use

**Solution:**

Edit `run.py` and change port:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # Changed to 5001
```

---

## 📁 Important Files/Folders

| Path | Purpose |
|------|---------|
| `app/` | Main application code |
| `data/fyp_phoneDataset.csv` | Phone dataset (350+ phones) |
| `config.py` | Application configuration |
| `run.py` | Application entry point |
| `.env` | Environment variables (CREATE THIS) |
| `requirements.txt` | Python dependencies |
| `migrations/` | Database migration scripts |
| `train_chatbot_model.py` | Chatbot ML training |

---

## 🔐 Security Notes

1. **Never commit `.env` file** to Git (it's in .gitignore)
2. **Change SECRET_KEY** in production
3. **Change ADMIN_PASSKEY** if deploying publicly
4. **Use strong passwords** for admin accounts
5. **Keep Oracle credentials secure**

---

## 📚 Additional Resources

- **README.md** - Project overview
- **SETUP_GUIDE.md** (if exists in docs/) - Detailed setup guide
- **QUICK_START.md** (if exists in docs/) - Quick reference
- **ORACLE_SETUP_GUIDE.md** (if exists in docs/) - Oracle-specific setup

---

## ✅ Verification Checklist

After setup, verify everything works:

- [ ] Virtual environment activated
- [ ] Dependencies installed (`pip list` shows flask, cx_Oracle, etc.)
- [ ] `.env` file created with correct Oracle credentials
- [ ] Database tables created (Users, Phones, Brands, etc.)
- [ ] Migrations run successfully
- [ ] Phone data imported (350+ phones)
- [ ] Chatbot model trained
- [ ] Admin account created
- [ ] Application runs without errors
- [ ] Can access homepage (http://localhost:5000)
- [ ] Can login as admin
- [ ] Can register as new user
- [ ] Chatbot responds to questions
- [ ] Can browse phones
- [ ] Can search phones
- [ ] Can compare phones

---

## 🆘 Need Help?

If you encounter issues not covered here:

1. Check the Flask logs in the terminal
2. Check Oracle SQL*Plus connection
3. Verify all environment variables in `.env`
4. Make sure virtual environment is activated
5. Try clearing Python cache and restarting

**Common commands:**
```bash
# Check Python version
python --version

# Check installed packages
pip list

# Check Oracle connection
sqlplus dialsmart/password123@localhost:1521/XEPDB1

# View Flask logs
python run.py  # Watch the terminal output
```

---

## 🎉 Success!

If you can access http://localhost:5000 and see the DialSmart homepage, you're all set!

**Next steps:**
1. Explore the application as a user
2. Login as admin to manage phones and brands
3. Test the chatbot recommendations
4. Try the phone comparison feature
5. Use the wizard for guided recommendations

Enjoy using DialSmart! 📱✨
