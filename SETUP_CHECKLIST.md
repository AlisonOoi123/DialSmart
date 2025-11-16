# DialSmart Setup Checklist

Use this checklist to track your setup progress. Check off each item as you complete it.

---

## Pre-Setup Checklist

- [ ] Python 3.11+ installed
  - [ ] Verified with `python --version`
  - [ ] Added to PATH
- [ ] Oracle Database 11g+ installed and running
  - [ ] Oracle service running in Windows Services
  - [ ] Know connection details (user, password, service name)
- [ ] Git installed
  - [ ] Verified with `git --version`

---

## Project Setup

- [ ] Repository cloned
  ```bash
  git clone https://github.com/AlisonOoi123/DialSmart.git
  ```
- [ ] Navigated to project folder
  ```bash
  cd DialSmart
  ```
- [ ] Virtual environment created (optional)
  ```bash
  python -m venv venv
  ```
- [ ] Virtual environment activated (if created)
  ```bash
  venv\Scripts\activate  # Windows
  source venv/bin/activate  # Mac/Linux
  ```
- [ ] Dependencies installed
  ```bash
  pip install -r requirements.txt
  ```

---

## Database Setup

- [ ] Oracle database user created (if not exists)
  ```sql
  CREATE USER ds_user IDENTIFIED BY dsuser123;
  GRANT CONNECT, RESOURCE, DBA TO ds_user;
  ```
- [ ] Database connection verified
  ```python
  import cx_Oracle
  conn = cx_Oracle.connect('ds_user/dsuser123@localhost:1521/ORCLPDB')
  ```
- [ ] Connection details updated in `config.py`
  - [ ] ORACLE_USER set correctly
  - [ ] ORACLE_PASSWORD set correctly
  - [ ] ORACLE_SERVICE set correctly

---

## First Run

- [ ] Application started for first time
  ```bash
  python run.py
  ```
- [ ] Database tables created automatically
  - [ ] Waited 30-60 seconds for tables to create
  - [ ] No errors in terminal
- [ ] Application stopped (CTRL+C)
- [ ] Tables verified in database
  ```sql
  SELECT table_name FROM user_tables;
  ```

---

## Data Import

- [ ] CSV file in correct location
  - [ ] File: `data/fyp_phoneDataset.csv`
  - [ ] File exists and readable
- [ ] Import script run successfully
  ```bash
  python scripts/import/update_missing_specs_from_csv.py
  ```
- [ ] Data verified in database
  ```sql
  SELECT COUNT(*) FROM phones;
  SELECT COUNT(*) FROM brands;
  ```

---

## Application Testing

### Basic Access
- [ ] Application started successfully
  ```bash
  python run.py
  ```
- [ ] Homepage loads at http://127.0.0.1:5000
- [ ] No errors in terminal
- [ ] CSS/images loading correctly

### User Registration
- [ ] Register page accessible: http://127.0.0.1:5000/register
- [ ] User account created successfully
- [ ] Login works: http://127.0.0.1:5000/login
- [ ] Dashboard accessible after login

### Core Features
- [ ] **Find Phone (Wizard)** working
  - [ ] Wizard loads correctly
  - [ ] Can answer all questions
  - [ ] Recommendations display
- [ ] **Chatbot** working
  - [ ] Chatbot icon visible (bottom right)
  - [ ] Can send messages
  - [ ] Receives intelligent responses
  - [ ] Tested queries:
    - [ ] "I want a gaming phone"
    - [ ] "Show me phones with good camera"
    - [ ] "Phones under RM3000"
- [ ] **Phone Comparison** working
  - [ ] Compare page loads
  - [ ] Brand filters work
  - [ ] Can select two phones
  - [ ] Comparison displays correctly
- [ ] **Browse Phones** working
  - [ ] All phones page loads
  - [ ] Can filter by brand
  - [ ] Can filter by price
  - [ ] Phone details page works

---

## Admin Setup (if needed)

- [ ] Admin account created
  - [ ] Via registration + SQL update, OR
  - [ ] Via SQL insert directly
- [ ] Admin login works
- [ ] Admin dashboard accessible: http://127.0.0.1:5000/admin/dashboard
- [ ] Admin features tested:
  - [ ] View dashboard statistics
  - [ ] Manage phones (add/edit/delete)
  - [ ] Manage brands
  - [ ] View contact messages
  - [ ] View users

---

## Final Verification

- [ ] All features tested and working
- [ ] No errors in terminal during use
- [ ] No errors in browser console (F12)
- [ ] Phone data displaying correctly
- [ ] Images loading (if available)
- [ ] Forms submitting correctly
- [ ] Database updating correctly

---

## Documentation Review

- [ ] Read **SETUP_GUIDE.md** (detailed instructions)
- [ ] Read **QUICK_START.md** (quick reference)
- [ ] Understand project structure
- [ ] Know where to find:
  - [ ] Configuration (`config.py`)
  - [ ] Templates (`app/templates/`)
  - [ ] Static files (`app/static/`)
  - [ ] Database models (`app/models/`)

---

## Troubleshooting (if needed)

If you encountered issues, check these:

- [ ] Oracle service running
- [ ] Correct Oracle credentials in `config.py`
- [ ] Python dependencies installed
- [ ] No port conflicts (port 5000)
- [ ] Database tables created
- [ ] CSV data imported
- [ ] Checked terminal for errors
- [ ] Checked browser console for errors

---

## Success Criteria

**Setup is complete when ALL of these work:**

✅ Application starts without errors
✅ Homepage loads correctly
✅ User can register and login
✅ Find Phone wizard returns recommendations
✅ Chatbot responds intelligently
✅ Phone comparison shows detailed specs
✅ Browse phones displays all phones with filters
✅ Admin dashboard accessible (if admin user created)

---

## Next Steps After Setup

- [ ] Explore all features
- [ ] Test with different queries
- [ ] Add custom phone data (if needed)
- [ ] Customize branding (optional)
- [ ] Read code to understand structure
- [ ] Plan deployment (if needed)

---

## Notes / Issues Encountered

Use this space to note any issues or important information:

```
_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

_________________________________________________________________

```

---

## Setup Completed! 🎉

Date: _______________
Time taken: _______________
Completed by: _______________

**Congratulations! DialSmart is now ready to use!**

For questions, refer to:
- **SETUP_GUIDE.md** - Detailed setup instructions
- **QUICK_START.md** - Quick reference
- **README.md** - Project overview
