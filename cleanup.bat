@echo off
REM DialSmart Cleanup Script (Windows)
REM Safely removes unnecessary files from the project

echo ================================================
echo DialSmart Project Cleanup Script
echo ================================================
echo.

REM Ask for confirmation
set /p confirm="This will delete cache files and old documentation. Continue? (Y/N): "
if /i not "%confirm%"=="Y" (
    echo Cleanup cancelled.
    exit /b 1
)

echo.
echo Starting cleanup...
echo.

REM 1. Delete Python cache files
echo 1. Removing Python cache files...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo    [OK] Python cache files removed

REM 2. Delete old documentation
echo 2. Removing old documentation...
if exist FILES_TO_DELETE.md del /q FILES_TO_DELETE.md 2>nul
if exist MISSING_SPECS_FIX.md del /q MISSING_SPECS_FIX.md 2>nul
if exist ORGANIZE_FILES.md del /q ORGANIZE_FILES.md 2>nul
if exist QUICK_FIX_CONTACT_ERROR.md del /q QUICK_FIX_CONTACT_ERROR.md 2>nul
echo    [OK] Old documentation removed

REM 3. Delete testing scripts
echo 3. Removing testing scripts...
if exist scripts\testing rd /s /q scripts\testing 2>nul
echo    [OK] Testing scripts removed

REM 4. Delete migration scripts
echo 4. Removing migration scripts...
if exist scripts\migration rd /s /q scripts\migration 2>nul
echo    [OK] Migration scripts removed

REM 5. Delete redundant database scripts
echo 5. Removing redundant database scripts...
if exist scripts\database\initialize_system.py del /q scripts\database\initialize_system.py 2>nul
if exist scripts\database\initialize_oracle.py del /q scripts\database\initialize_oracle.py 2>nul
if exist scripts\database\init_database.py del /q scripts\database\init_database.py 2>nul
echo    [OK] Redundant database scripts removed

REM 6. Delete redundant import scripts
echo 6. Removing redundant import scripts...
if exist scripts\import\import_csv_dataset.py del /q scripts\import\import_csv_dataset.py 2>nul
if exist scripts\import\import_csv_to_oracle.py del /q scripts\import\import_csv_to_oracle.py 2>nul
if exist scripts\import\generate_update_images.py del /q scripts\import\generate_update_images.py 2>nul
if exist scripts\import\fix_missing_images.py del /q scripts\import\fix_missing_images.py 2>nul
echo    [OK] Redundant import scripts removed

REM 7. Delete large SQL data files
echo 7. Removing large SQL data files...
if exist sql\update_phone_images.sql del /q sql\update_phone_images.sql 2>nul
if exist sql\check_missing_specs.sql del /q sql\check_missing_specs.sql 2>nul
echo    [OK] SQL data files removed

REM 8. Delete root utility scripts
echo 8. Removing root utility scripts...
if exist organize_files.py del /q organize_files.py 2>nul
echo    [OK] Utility scripts removed

REM 9. Delete log files (optional)
echo 9. Removing log files (if any)...
del /s /q *.log 2>nul
echo    [OK] Log files removed

echo.
echo ================================================
echo Cleanup completed successfully!
echo ================================================
echo.
echo You can now share this cleaner project.
echo.
pause
