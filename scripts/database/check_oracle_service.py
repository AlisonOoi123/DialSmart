"""
Oracle Service Name Checker
This script helps you find the correct Oracle service name for your installation
"""
import subprocess
import sys

print("\n" + "="*70)
print("Oracle Database Service Name Checker")
print("="*70)

print("\n[Step 1] Checking if Oracle is installed...")

# Check if Oracle services are running (Windows)
try:
    result = subprocess.run(
        ['sc', 'query', 'state=', 'all'],
        capture_output=True,
        text=True,
        shell=True
    )

    oracle_services = [line for line in result.stdout.split('\n') if 'Oracle' in line]

    if oracle_services:
        print("  ✓ Found Oracle services:")
        for service in oracle_services[:10]:  # Show first 10
            print(f"    {service.strip()}")
    else:
        print("  ✗ No Oracle services found")
        print("\n  Oracle Database doesn't appear to be installed.")
        print("  Please install Oracle Database XE first:")
        print("  https://www.oracle.com/database/technologies/xe-downloads.html")
        sys.exit(1)

except Exception as e:
    print(f"  ⚠ Could not check services: {e}")

print("\n[Step 2] Checking Oracle Listener...")

try:
    # Try to run lsnrctl status
    result = subprocess.run(
        ['lsnrctl', 'status'],
        capture_output=True,
        text=True,
        timeout=10
    )

    output = result.stdout

    if 'Service' in output:
        print("  ✓ Oracle Listener is running")
        print("\n  Available Services:")

        # Extract service names from lsnrctl output
        lines = output.split('\n')
        for i, line in enumerate(lines):
            if 'Service' in line and '=' not in line:
                # Look for service names in quotes
                if '"' in line:
                    start = line.find('"') + 1
                    end = line.find('"', start)
                    service_name = line[start:end]
                    print(f"    ✓ {service_name}")

        print("\n  Full lsnrctl output:")
        print("  " + "="*66)
        for line in output.split('\n'):
            if line.strip():
                print(f"  {line}")
        print("  " + "="*66)

    else:
        print("  ✗ Oracle Listener is not responding")

except FileNotFoundError:
    print("  ✗ 'lsnrctl' command not found")
    print("  This usually means Oracle is not installed or not in PATH")
    print("\n  To install Oracle Database XE:")
    print("  1. Download from: https://www.oracle.com/database/technologies/xe-downloads.html")
    print("  2. Install with default settings")
    print("  3. Restart this script")

except subprocess.TimeoutExpired:
    print("  ✗ Oracle Listener command timed out")

except Exception as e:
    print(f"  ✗ Error checking listener: {e}")

print("\n[Step 3] Common Oracle Service Names...")

print("""
  Common service names based on Oracle version:

  Oracle XE 21c (Pluggable Database):
    - Service Name: XEPDB1  ← Most common for Oracle XE 21c
    - Connection: localhost:1521/XEPDB1

  Oracle XE 18c/11g (Non-CDB):
    - Service Name: XE
    - Connection: localhost:1521/XE

  Oracle Standard/Enterprise:
    - Service Name: ORCL or ORCLPDB1
    - Connection: localhost:1521/ORCL
""")

print("\n[Step 4] Recommendations...")

print("""
  Based on your setup, update config.py with the correct service name:

  Option 1: If you found a service name above
    Edit config.py line 36:
    ORACLE_SERVICE = 'YOUR_SERVICE_NAME'  # e.g., XE, XEPDB1, or ORCL

  Option 2: If Oracle is not installed
    Install Oracle Database XE (free):
    https://www.oracle.com/database/technologies/xe-downloads.html

  Option 3: Use SQLite instead (no Oracle needed)
    Keep config.py line 40 as:
    DB_TYPE = 'sqlite'

    Then just run your app:
    python run.py
""")

print("\n" + "="*70)
print("Next Steps:")
print("="*70)
print("1. Note the service name shown above (if any)")
print("2. Update config.py with the correct ORACLE_SERVICE")
print("3. Try the migration again: python migrate_sqlite_to_oracle.py")
print("="*70 + "\n")
