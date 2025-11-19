# DialSmart - Fresh Database Setup Guide

## 🎯 Purpose
Complete step-by-step guide to set up DialSmart database from scratch for your friend.

---

## Prerequisites

✅ Oracle SQL*Plus installed and running
✅ Oracle user created (e.g., `ds_user`)
✅ Python virtual environment activated
✅ DialSmart project downloaded/extracted

**Your friend's Oracle credentials:**
- Username: `ds_user`
- Password: `dsuser123`
- Host: `localhost:1521`
- Service: `orclpdb`

---

## 📋 Complete Setup Process

### STEP 1: Connect to Oracle SQL*Plus

Open Command Prompt and connect:

```bash
sqlplus ds_user/dsuser123@localhost:1521/orclpdb
```

You should see:
```
Connected to:
Oracle Database 21c Enterprise Edition Release 21.0.0.0.0 - Production
SQL>
```

---

### STEP 2: Drop All Existing Tables

This will completely clean the database.

**In SQL*Plus, run:**

```sql
@sql/01_drop_all_tables.sql
```

**OR manually copy and paste:**

```sql
-- Drop all tables in correct order
DROP TABLE user_preferences CASCADE CONSTRAINTS;
DROP TABLE recommendations CASCADE CONSTRAINTS;
DROP TABLE phone_specifications CASCADE CONSTRAINTS;
DROP TABLE phones CASCADE CONSTRAINTS;
DROP TABLE comparisons CASCADE CONSTRAINTS;
DROP TABLE chat_history CASCADE CONSTRAINTS;
DROP TABLE chat_history_backup CASCADE CONSTRAINTS;
DROP TABLE contact_messages CASCADE CONSTRAINTS;
DROP TABLE audit_logs CASCADE CONSTRAINTS;
DROP TABLE brands CASCADE CONSTRAINTS;
DROP TABLE users CASCADE CONSTRAINTS;
DROP TABLE admins CASCADE CONSTRAINTS;

-- Drop all sequences
DROP SEQUENCE user_preferences_seq;
DROP SEQUENCE recommendations_seq;
DROP SEQUENCE phone_specifications_seq;
DROP SEQUENCE phones_seq;
DROP SEQUENCE comparisons_seq;
DROP SEQUENCE chat_history_seq;
DROP SEQUENCE contact_messages_seq;
DROP SEQUENCE audit_logs_seq;
DROP SEQUENCE brands_seq;
DROP SEQUENCE users_seq;
```

**Expected output:**
```
Table dropped.
Table dropped.
... (for each table)
Sequence dropped.
... (for each sequence)
```

**Verify tables are dropped:**
```sql
SELECT COUNT(*) FROM user_tables;
```

Should return **0**.

---

### STEP 3: Create All Tables

**In SQL*Plus, run:**

```sql
@sql/02_create_all_tables.sql
```

This will create:
- ✅ 11 tables (users, brands, phones, phone_specifications, etc.)
- ✅ 10 sequences
- ✅ All foreign key relationships
- ✅ Performance indexes

**Expected output:**
```
Creating USERS table...
Users table created.

Creating BRANDS table...
Brands table created.

... (for each table)

All tables created successfully!
```

**Verify tables created:**
```sql
SELECT table_name FROM user_tables ORDER BY table_name;
```

Should show **11-12 tables**.

---

### STEP 4: Run Database Migrations

These add extra columns needed by the application.

**In SQL*Plus, run each migration:**

```sql
@migrations/001_add_admin_management_columns.sql
@migrations/002_create_audit_logs_table.sql
@migrations/004_allow_guest_chatbot_users.sql
```

**Expected output for each:**
```
Table altered.
-- OR --
Table created.
```

**Note:** Some migrations may show errors if columns already exist - that's okay!

---

### STEP 5: Exit SQL*Plus

```sql
EXIT;
```

---

### STEP 6: Import Phone Data from CSV

Back in Command Prompt (with virtual environment activated):

**Navigate to project root:**
```bash
cd C:\Users\User\OneDrive\Documents\GitHub\DialSmart
```

**Activate virtual environment if not already:**
```bash
venv\Scripts\activate
```

**Run the import script:**
```bash
python scripts\import\import_fresh_database.py
```

**Expected output:**
```
================================================================================
  DialSmart - Fresh Database Import
================================================================================

Reading CSV file: fyp_phoneDataset.csv
✓ Found XXX phones in CSV

Found XX unique brands: Apple, Oppo, Samsung, Vivo, Xiaomi, ...

================================================================================
STEP 1: Importing Brands
================================================================================

   ✓ Created brand 'Apple' (ID: 1)
   ✓ Created brand 'Samsung' (ID: 2)
   ... (for each brand)

================================================================================
STEP 2: Importing Phones and Specifications
================================================================================

   ✓ Imported 50 phones...
   ✓ Imported 100 phones...
   ... (progress updates)

================================================================================
IMPORT SUMMARY
================================================================================
✓ Successfully imported: XXX phones
→ Skipped (duplicates):  0 phones
❌ Errors:               0 phones

================================================================================
DATABASE STATUS
================================================================================
Brands in database:       XX
Phones in database:       XXX
Specifications:           XXX

✅ Import completed successfully!
```

**If import fails:**
- Make sure CSV file exists: `fyp_phoneDataset.csv` or `data/fyp_phoneDataset.csv`
- Check Oracle connection in `.env` file
- Verify tables were created in Step 3

---

### STEP 7: Verify Data Imported

**Connect to SQL*Plus again:**
```bash
sqlplus ds_user/dsuser123@localhost:1521/orclpdb
```

**Check data counts:**
```sql
SELECT 'BRANDS' as table_name, COUNT(*) FROM brands
UNION ALL
SELECT 'PHONES', COUNT(*) FROM phones
UNION ALL
SELECT 'SPECIFICATIONS', COUNT(*) FROM phone_specifications;
```

**Expected output:**
```
BRANDS          XX
PHONES          XXX
SPECIFICATIONS  XXX
```

**Sample a few phones:**
```sql
SELECT b.name, p.model_name, p.price
FROM phones p
JOIN brands b ON p.brand_id = b.id
WHERE ROWNUM <= 10
ORDER BY b.name, p.model_name;
```

**Exit SQL*Plus:**
```sql
EXIT;
```

---

### STEP 8: Train Chatbot Model

**In Command Prompt (with venv activated):**

```bash
python train_chatbot_model.py
```

**Expected output:**
```
Loading training data...
Training chatbot model...
Model accuracy: XX%
Model saved successfully!
```

**Note:** This takes 2-5 minutes.

---

### STEP 9: Create Admin Account

```bash
python create_admin.py
```

**You'll be prompted for:**
```
Full Name: [Enter name, e.g., "Admin User"]
Email: [Enter email, e.g., "admin@dialsmart.com"]
Password: [Enter strong password, e.g., "Admin@123"]
Confirm Password: [Re-enter password]
```

**Expected output:**
```
✓ Admin user created successfully!
You can now login with: admin@dialsmart.com
```

---

### STEP 10: Run the Application

```bash
python run.py
```

**Expected output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000
Press CTRL+C to quit
```

---

### STEP 11: Test the Application

**Open browser and go to:**
- Homepage: http://localhost:5000
- Login: http://localhost:5000/auth/login

**Test:**
1. ✅ Can see homepage
2. ✅ Can browse phones (should see hundreds of phones)
3. ✅ Can search for phones
4. ✅ Login as admin (use credentials from Step 9)
5. ✅ Admin dashboard shows statistics
6. ✅ Chatbot responds to questions
7. ✅ Can compare phones

---

## 🎉 Success!

Your database is now fully set up with:
- ✅ All tables created
- ✅ Brands imported
- ✅ XXX+ phones imported with full specifications
- ✅ Chatbot model trained
- ✅ Admin account created
- ✅ Application running

---

## 📝 Quick Reference Commands

### Every Time You Want to Run DialSmart:

```bash
# 1. Navigate to project
cd C:\Users\User\OneDrive\Documents\GitHub\DialSmart

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Run application
python run.py

# 4. Open browser
# http://localhost:5000
```

---

## 🔧 Troubleshooting

### Problem: "Table or view does not exist"

**Solution:**
- Go back to Step 3 and recreate tables
- Verify with: `SELECT table_name FROM user_tables;`

### Problem: "No phones found in database"

**Solution:**
- Re-run Step 6 (import script)
- Check CSV file exists
- Verify brand and phone counts in SQL*Plus

### Problem: "ORA-00001: unique constraint violated"

**Solution:**
- Data already exists
- Either skip import or go to Step 2 and drop all tables first

### Problem: Import script shows "CSV file not found"

**Solution:**
```bash
# Make sure you're in the project root
cd C:\Users\User\OneDrive\Documents\GitHub\DialSmart

# Check if CSV exists
dir fyp_phoneDataset.csv
# OR
dir data\fyp_phoneDataset.csv
```

### Problem: Chatbot not responding

**Solution:**
- Re-run Step 8 (train chatbot)
- Clear Python cache:
  ```bash
  FOR /d /r . %d IN (__pycache__) DO @IF EXIST "%d" rd /s /q "%d"
  ```
- Restart application

---

## 📊 Database Schema Summary

**Tables Created:**
1. `users` - User accounts (admin and regular users)
2. `brands` - Phone brands (Apple, Samsung, etc.)
3. `phones` - Phone models
4. `phone_specifications` - Detailed phone specs
5. `user_preferences` - User preferences for recommendations
6. `recommendations` - AI-generated recommendations
7. `comparisons` - Phone comparison history
8. `chat_history` - Chatbot conversation history
9. `contact_messages` - Contact form messages
10. `audit_logs` - Admin action logs
11. `admins` - (Legacy table, may not be used)

**Relationships:**
- Brands → Phones (one-to-many)
- Phones → Phone Specifications (one-to-one)
- Users → Preferences (one-to-one)
- Users → Recommendations (one-to-many)
- Users → Comparisons (one-to-many)
- Users → Chat History (one-to-many)

---

## 🆘 Need Help?

1. **Check Flask logs** in the terminal where you ran `python run.py`
2. **Check SQL*Plus** for database errors
3. **Verify `.env` file** has correct Oracle credentials
4. **Re-run specific steps** if something failed

**All scripts are located in:**
- SQL scripts: `sql/`
- Import scripts: `scripts/import/`
- Migrations: `migrations/`

---

## ✅ Final Checklist

After completing all steps, verify:

- [ ] Can connect to Oracle SQL*Plus
- [ ] All tables exist (11-12 tables)
- [ ] Brands imported (check count > 0)
- [ ] Phones imported (check count > 300)
- [ ] Chatbot model trained
- [ ] Admin account created
- [ ] Application runs without errors
- [ ] Can access http://localhost:5000
- [ ] Can browse phones
- [ ] Can login as admin
- [ ] Chatbot responds to questions

**If all checked - SUCCESS! 🎉**

---

## 📚 Additional Resources

- **Main README**: `README.md`
- **Setup Instructions**: `SETUP_INSTRUCTIONS_FOR_NEW_USER.md`
- **ZIP Download Guide**: `SETUP_FROM_ZIP.txt`
- **Browser History Testing**: `TESTING_BROWSER_HISTORY.md`

---

**Last Updated:** 2025-11-19
**For:** DialSmart Fresh Database Setup
