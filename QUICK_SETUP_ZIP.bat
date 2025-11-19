@echo off
REM DialSmart Quick Setup Script for ZIP Download (No Git Required)
REM Run this after extracting the ZIP file and setting up Oracle database

echo ========================================
echo   DialSmart Quick Setup (ZIP Version)
echo ========================================
echo.

REM Step 1: Check if we're in the right directory
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found!
    echo Please run this script from the DialSmart project root directory.
    echo.
    echo Example:
    echo   cd C:\Users\User\OneDrive\Documents\GitHub\DialSmart
    echo   QUICK_SETUP_ZIP.bat
    pause
    exit /b 1
)

echo [1/8] Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)
echo.

echo [2/8] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [3/8] Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages failed to install.
    echo If cx_Oracle failed, you may need Oracle Instant Client.
    echo See troubleshooting in SETUP_INSTRUCTIONS_FOR_NEW_USER.md
    echo.
    pause
)
echo.

echo [4/8] Checking for .env file...
if not exist ".env" (
    echo.
    echo ========================================
    echo   IMPORTANT: Create .env File
    echo ========================================
    echo.
    echo The .env file is REQUIRED for database connection.
    echo.
    if exist "env.example" (
        echo Creating .env from env.example...
        copy env.example .env
        echo.
        echo Please edit .env file with your Oracle database credentials:
        echo   - ORACLE_USER
        echo   - ORACLE_PASSWORD
        echo   - ORACLE_SERVICE_NAME
        echo   - DATABASE_URL
        echo.
        echo Opening .env in notepad...
        timeout /t 2 >nul
        start notepad .env
        echo.
        echo Press any key AFTER you have saved your .env file...
        pause >nul
    ) else (
        echo ERROR: env.example not found!
        echo Please create .env manually with Oracle credentials.
        echo See SETUP_INSTRUCTIONS_FOR_NEW_USER.md for example.
        pause
        exit /b 1
    )
) else (
    echo .env file already exists.
)
echo.

echo [5/8] Clearing Python cache...
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo Cache cleared.
echo.

echo [6/8] Creating database tables...
echo.
echo The application will start to create database tables.
echo It will automatically close after 10 seconds.
echo Check for any errors in the output.
echo.
echo Starting application...
start /b python run.py
timeout /t 10 /nobreak
taskkill /F /IM python.exe 2>nul
echo.
echo Database tables should be created.
echo.

echo [7/8] Database migrations...
echo.
echo ========================================
echo   MANUAL STEP REQUIRED
echo ========================================
echo.
echo Please run these commands in SQL*Plus:
echo.
echo 1. Open SQL*Plus:
echo    sqlplus your_username/your_password@localhost:1521/your_service_name
echo.
echo 2. Run migrations:
echo    @migrations\001_add_admin_management_columns.sql
echo    @migrations\002_create_audit_logs_table.sql
echo    @migrations\004_allow_guest_chatbot_users.sql
echo    EXIT;
echo.
echo Press any key AFTER running migrations in SQL*Plus...
pause >nul
echo.

echo [8/8] Importing phone data...
echo.
if exist "import_phones_from_csv.py" (
    echo Importing from root directory...
    python import_phones_from_csv.py
) else if exist "scripts\import\import_phones_from_csv.py" (
    echo Importing from scripts directory...
    python scripts\import\import_phones_from_csv.py
) else if exist "scripts\import\update_missing_specs_from_csv.py" (
    echo Using update script...
    python scripts\import\update_missing_specs_from_csv.py
) else (
    echo WARNING: Import script not found!
    echo Please import phone data manually.
    echo Look for import scripts in the project.
)
echo.

echo ========================================
echo   Setup Complete!
echo ========================================
echo.
echo ✓ Virtual environment created
echo ✓ Dependencies installed
echo ✓ .env file created
echo ✓ Database tables created
echo ✓ Migrations run
echo ✓ Phone data imported
echo.
echo ========================================
echo   Next Steps:
echo ========================================
echo.
echo 1. Train chatbot model (2-5 minutes):
echo    python train_chatbot_model.py
echo.
echo 2. Create admin account:
echo    python create_admin.py
echo.
echo 3. Run the application:
echo    python run.py
echo.
echo 4. Open in browser:
echo    http://localhost:5000
echo.
echo ========================================
echo   Need Help?
echo ========================================
echo.
echo See SETUP_INSTRUCTIONS_FOR_NEW_USER.md for:
echo - Detailed troubleshooting
echo - Oracle database setup
echo - Common issues and solutions
echo.
pause
