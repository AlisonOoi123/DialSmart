@echo off
REM ===============================================================================
REM DialSmart - Fresh Setup (After SQL*Plus Steps)
REM Run this AFTER you have completed the SQL*Plus steps:
REM   1. Dropped all tables
REM   2. Created all tables
REM   3. Ran migrations
REM ===============================================================================

echo.
echo ================================================================================
echo   DialSmart Fresh Setup - Part 2 (After SQL*Plus)
echo ================================================================================
echo.
echo This script will:
echo   1. Import phone data from CSV
echo   2. Train chatbot model
echo   3. Create admin account
echo   4. Run the application
echo.
echo IMPORTANT: Make sure you have completed these SQL*Plus steps first:
echo   - Dropped all existing tables
echo   - Created all tables
echo   - Ran all migrations
echo.
pause
echo.

REM Check if we're in the right directory
if not exist "fyp_phoneDataset.csv" (
    if not exist "data\fyp_phoneDataset.csv" (
        echo ERROR: CSV file not found!
        echo Please make sure fyp_phoneDataset.csv exists in the project root or data folder.
        pause
        exit /b 1
    )
)

REM Check virtual environment
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please create virtual environment first:
    echo   python -m venv venv
    pause
    exit /b 1
)

echo [Step 1/5] Activating virtual environment...
call venv\Scripts\activate
echo.

echo [Step 2/5] Importing phone data from CSV...
echo This may take 2-5 minutes depending on CSV size.
echo.
python scripts\import\import_fresh_database.py
if errorlevel 1 (
    echo.
    echo ERROR: Import failed!
    echo Please check:
    echo   1. CSV file exists (fyp_phoneDataset.csv or data\fyp_phoneDataset.csv)
    echo   2. Database tables were created
    echo   3. .env file has correct Oracle credentials
    pause
    exit /b 1
)
echo.
echo ✓ Phone data imported successfully!
echo.
pause

echo [Step 3/5] Clearing Python cache...
FOR /d /r . %%d IN (__pycache__) DO @IF EXIST "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
echo ✓ Cache cleared.
echo.

echo [Step 4/5] Training chatbot model...
echo This will take 2-5 minutes. Please wait...
echo.
python train_chatbot_model.py
if errorlevel 1 (
    echo.
    echo WARNING: Chatbot training failed!
    echo The application will still work, but chatbot may not respond correctly.
    echo You can train it later by running: python train_chatbot_model.py
    echo.
    pause
) else (
    echo.
    echo ✓ Chatbot model trained successfully!
    echo.
)
pause

echo [Step 5/5] Creating admin account...
echo.
echo Please enter admin account details:
echo.
python create_admin.py
if errorlevel 1 (
    echo.
    echo WARNING: Admin account creation failed!
    echo You can create it later by running: python create_admin.py
    echo.
    pause
) else (
    echo.
    echo ✓ Admin account created successfully!
    echo.
)
pause

echo.
echo ================================================================================
echo   Setup Complete!
echo ================================================================================
echo.
echo ✓ Phone data imported
echo ✓ Chatbot model trained
echo ✓ Admin account created
echo.
echo Ready to run DialSmart!
echo.
echo To start the application:
echo   python run.py
echo.
echo Then open in browser:
echo   http://localhost:5000
echo.
echo ================================================================================
echo.

choice /C YN /M "Do you want to start the application now"
if errorlevel 2 goto :end
if errorlevel 1 goto :run

:run
echo.
echo Starting DialSmart...
echo Press Ctrl+C to stop the application.
echo.
python run.py

:end
echo.
echo To run DialSmart later, use:
echo   venv\Scripts\activate
echo   python run.py
echo.
pause
