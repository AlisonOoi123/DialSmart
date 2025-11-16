# DialSmart - Quick Start Guide

## 🚀 5-Minute Setup

### 1. Install Prerequisites
- ✅ Python 3.11+ (https://www.python.org/downloads/)
- ✅ Oracle Database 11g+ (should already be installed)
- ✅ Git (https://git-scm.com/downloads/)

### 2. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/AlisonOoi123/DialSmart.git
cd DialSmart

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Database
Edit `config.py` with your Oracle details:
```python
ORACLE_USER = 'ds_user'        # Your username
ORACLE_PASSWORD = 'dsuser123'  # Your password
ORACLE_SERVICE = 'ORCLPDB'     # Your service name
```

### 4. Run Application
```bash
python run.py
```

### 5. Open Browser
```
http://127.0.0.1:5000
```

---

## 📋 Essential Commands

### Start Application
```bash
python run.py
```

### Import Phone Data
```bash
python scripts/import/update_missing_specs_from_csv.py
```

### Stop Application
Press `CTRL+C` in terminal

---

## 🔧 Common Issues & Quick Fixes

| Problem | Solution |
|---------|----------|
| Can't connect to Oracle | Start Oracle service in Windows Services |
| Module not found error | Run `pip install -r requirements.txt` |
| Port 5000 in use | Change port in `run.py` to 5001 |
| No data showing | Run CSV import script |

---

## 📁 Important Files

- `run.py` - Start the application
- `config.py` - Database configuration
- `requirements.txt` - Python dependencies
- `data/fyp_phoneDataset.csv` - Phone data

---

## 🌐 Important URLs

- Homepage: http://127.0.0.1:5000
- Find Phone: http://127.0.0.1:5000/phone/find
- Compare: http://127.0.0.1:5000/phone/compare
- Admin: http://127.0.0.1:5000/admin/dashboard
- Login: http://127.0.0.1:5000/login

---

## 📖 Need More Help?

See **SETUP_GUIDE.md** for detailed instructions!

---

**That's it! You're ready to go! 🎉**
