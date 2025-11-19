@echo off
REM DialSmart Quick Setup Script for Windows
REM Run this after cloning the repository and setting up Oracle database

echo ========================================
echo   DialSmart Quick Setup Script
echo ========================================
echo.

REM Step 1: Check if we're in the right directory
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Please run this script from the DialSmart project root directory.
    pause
    exit /b 1
)

echo [1/9] Checking out the correct branch...
git fetch --all
git checkout claude/dialsmart-python-system-01Qv2n5kr4dUSV8HUagf8ueS
git pull origin claude/dialsmart-python-system-01Qv2n5kr4dUSV8HUagf8ueS
echo.

echo [2/9] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

echo [3/9] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [4/9] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
echo.

echo [5/9] Checking for .env file...
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please create .env file with your Oracle database credentials.
    echo See env.example for reference.
    echo.
    echo After creating .env, run this script again.
    pause
    exit /b 1
) else (
    echo .env file found.
)
echo.

echo [6/9] Clearing Python cache...
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
echo Cache cleared.
echo.

echo [7/9] Setting up database tables...
echo Starting application to create tables (will auto-stop in 10 seconds)...
start /b python run.py
timeout /t 10 /nobreak >nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *run.py*" 2>nul
echo Database tables should be created.
echo.

echo [8/9] Running database migrations...
echo Please run the following commands in SQL*Plus:
echo.
echo sqlplus your_username/your_password@localhost:1521/your_service_name
echo @migrations/001_add_admin_management_columns.sql
echo @migrations/002_create_audit_logs_table.sql
echo @migrations/004_allow_guest_chatbot_users.sql
echo EXIT;
echo.
echo Press any key after running migrations in SQL*Plus...
pause >nul
echo.

echo [9/9] Importing phone data...
if exist "import_phones_from_csv.py" (
    python import_phones_from_csv.py
) else if exist "scripts\import\update_missing_specs_from_csv.py" (
    python scripts\import\update_missing_specs_from_csv.py
) else (
    echo WARNING: Import script not found. Please import data manually.
)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Train chatbot model:  python train_chatbot_model.py
echo 2. Create admin account:  python create_admin.py
echo 3. Run application:       python run.py
echo 4. Open browser:          http://localhost:5000
echo.
echo See SETUP_INSTRUCTIONS_FOR_NEW_USER.md for detailed instructions.
echo.
pause
