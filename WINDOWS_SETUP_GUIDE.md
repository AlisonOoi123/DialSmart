# DialSmart - Windows Setup Guide

## ✅ All Issues Fixed!

### Issues Resolved:
1. ✅ CSV import path fixed for Windows
2. ✅ CSV column names fixed to match your dataset
3. ✅ Admin account system with passkey protection
4. ✅ Python 3.13+ compatibility

---

## 📋 Step-by-Step Setup on Windows

### 1. Pull Latest Code

```bash
git pull origin claude/debug-dialsmart-python-01WkQ1my54pjH8LUncF3nRzv
```

### 2. Update Python Packages

Make sure you're in your virtual environment:

```bash
# Activate venv (you should see (venv) in your prompt)
venv\Scripts\activate

# Upgrade pip
python -m pip install --upgrade pip

# Install/update all packages
pip install --upgrade -r requirements.txt
```

### 3. Import Phone Data

Your CSV file should be at: `C:\Users\User\OneDrive\Documents\GitHub\DialSmart\data\fyp_phoneDataset.csv`

```bash
python import_phones_from_csv.py
```

**Expected output:**
```
Found CSV file at: C:\Users\User\OneDrive\...\data\fyp_phoneDataset.csv
Importing phones from CSV dataset...
✓ Created brand: Apple
✓ Created brand: Samsung
...
✅ Import completed!
   Total phones imported: 689
   Total brands created: 13
```

### 4. Create Admin Accounts

**Option A: Create Two Default Admins (Quick)**

```bash
python create_admin.py --default
```

This creates:
- **admin@dialsmart.my** / password: `admin123`
- **superadmin@dialsmart.my** / password: `super123`

**Option B: Create Custom Admin (Secure)**

```bash
python create_admin.py
```

You'll be prompted for:
1. **Admin Passkey:** `DialSmart2024Admin!`
2. Email
3. Password
4. Full name

### 5. Run the Application

```bash
python run.py
```

The application will start on: **http://localhost:5000**

---

## 🔐 Admin Access

### Login as Admin

1. Go to: **http://localhost:5000/auth/login**
2. Use admin credentials:
   - Email: `admin@dialsmart.my`
   - Password: `admin123`

### Register New Admin (Web Interface)

1. Go to: **http://localhost:5000/auth/register-admin**
2. Enter the admin passkey: `DialSmart2024Admin!`
3. Fill in admin details
4. Click Register

**Note:** Regular users CANNOT register as admin without the passkey!

---

## 📱 Phone Images

The import script now correctly reads the `ImageURL` column from your CSV.

**If images still don't show:**
1. Check if the URLs in your CSV are valid
2. Make sure your internet connection is working
3. The images are loaded from external URLs in your dataset

To verify images were imported:

```bash
python -c "from app import create_app, db; from app.models import Phone; app = create_app(); app.app_context().push(); phone = Phone.query.first(); print(f'Sample image URL: {phone.main_image}')"
```

---

## 🔍 Find Phone Wizard (Recommendation)

The recommendation wizard route is at: `/recommendation/wizard`

**If results don't show after filtering:**
1. Make sure you imported the phone data first
2. Check that filters match available phones in database
3. Try broader filter criteria

To test if phones can be queried:

```bash
python -c "from app import create_app, db; from app.models import Phone, PhoneSpecification; app = create_app(); app.app_context().push(); phones = db.session.query(Phone).join(PhoneSpecification).filter(PhoneSpecification.has_5g == True).limit(5).all(); print(f'Found {len(phones)} 5G phones'); [print(f'  - {p.brand.name} {p.model_name}') for p in phones]"
```

---

## 🛠️ Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'flask'"

```bash
# Make sure venv is activated
venv\Scripts\activate

# Reinstall packages
pip install -r requirements.txt
```

### Issue: "FileNotFoundError" when importing CSV

Make sure your CSV is at:
```
C:\Users\User\OneDrive\Documents\GitHub\DialSmart\data\fyp_phoneDataset.csv
```

Or move it to the root folder:
```
C:\Users\User\OneDrive\Documents\GitHub\DialSmart\fyp_phoneDataset.csv
```

### Issue: Images not displaying

1. Check one phone's image URL:
   ```bash
   python -c "from app import create_app, db; from app.models import Phone; app = create_app(); app.app_context().push(); phone = Phone.query.first(); print(phone.main_image)"
   ```

2. Test the URL in your browser
3. If URLs are empty, check your CSV file's `ImageURL` column

### Issue: No phones showing after filter

```bash
# Check total phones in database
python -c "from app import create_app; from app.models import Phone; app = create_app(); app.app_context().push(); print(f'Total phones: {Phone.query.count()}')"

# Check if specifications exist
python -c "from app import create_app; from app.models import PhoneSpecification; app = create_app(); app.app_context().push(); print(f'Total specs: {PhoneSpecification.query.count()}')"
```

---

## 📊 Database Info

After import, you should have:
- **13 Brands:** Apple, Asus, Google, Honor, Huawei, Infinix, Oppo, Poco, Realme, Redmi, Samsung, Vivo, Xiaomi
- **689 Phones** with full specifications
- **514 5G Phones**
- **Price range:** MYR 248 - MYR 12,188

---

## 🔑 Important Security Notes

### Change Admin Passkey in Production!

**File:** `app/routes/auth.py` (line 111)
**File:** `create_admin.py` (line 11)

Change from:
```python
ADMIN_PASSKEY = "DialSmart2024Admin!"
```

To your own secure passkey!

---

## 📝 Summary

**Your CSV structure:**
- Columns use **no spaces**: `ImageURL`, `ScreenSize`, `DisplayType`, `RearCamera`, etc.
- The import script is now fixed to match this format

**Admin system:**
- Cannot register as admin without passkey
- Use `create_admin.py` to create admins
- Web registration at `/auth/register-admin` requires passkey

**Everything should now work!** 🎉

---

## Next Steps

1. ✅ Pull latest code
2. ✅ Update packages
3. ✅ Import phone data
4. ✅ Create admin accounts
5. ✅ Run application
6. ✅ Test login and browse phones

**Application URL:** http://localhost:5000
**Admin Login:** http://localhost:5000/auth/login
