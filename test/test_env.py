"""
Test script to verify .env file loading
Run this to check if your .env file is properly configured
"""
import os
from dotenv import load_dotenv

print("\n" + "="*70)
print("TESTING .ENV FILE LOADING")
print("="*70)

# Check if .env file exists
env_file = os.path.join(os.path.dirname(__file__), '.env')
print(f"\n1. Looking for .env file at: {env_file}")
print(f"   File exists: {os.path.exists(env_file)}")

if not os.path.exists(env_file):
    print("\n   ERROR: .env file not found!")
    print("   Please create a .env file in the project root directory")
    print("   (same directory as run.py)")
    print("\n" + "="*70 + "\n")
    exit(1)

# Try to load .env file
print("\n2. Loading environment variables from .env file...")
load_dotenv()
print("   load_dotenv() completed")

# Check email configuration
print("\n3. Email Configuration:")
print(f"   MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
print(f"   MAIL_PORT: {os.getenv('MAIL_PORT')}")
print(f"   MAIL_USE_TLS: {os.getenv('MAIL_USE_TLS')}")
print(f"   MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
password = os.getenv('MAIL_PASSWORD')
print(f"   MAIL_PASSWORD: {'***' + password[-4:] if password else 'NOT SET'}")
print(f"   MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")

# Check database configuration
print("\n4. Database Configuration:")
print(f"   ORACLE_USER: {os.getenv('ORACLE_USER')}")
print(f"   ORACLE_HOST: {os.getenv('ORACLE_HOST')}")
print(f"   ORACLE_PORT: {os.getenv('ORACLE_PORT')}")
print(f"   ORACLE_SERVICE: {os.getenv('ORACLE_SERVICE')}")

# Validation
print("\n5. Validation:")
errors = []

if not os.getenv('MAIL_USERNAME'):
    errors.append("   ✗ MAIL_USERNAME is not set")
else:
    print("   ✓ MAIL_USERNAME is set")

if not os.getenv('MAIL_PASSWORD'):
    errors.append("   ✗ MAIL_PASSWORD is not set")
else:
    print("   ✓ MAIL_PASSWORD is set")

if not os.getenv('MAIL_DEFAULT_SENDER'):
    errors.append("   ✗ MAIL_DEFAULT_SENDER is not set")
else:
    print("   ✓ MAIL_DEFAULT_SENDER is set")

if errors:
    print("\n   ERRORS FOUND:")
    for error in errors:
        print(error)
    print("\n   Please check your .env file configuration")
else:
    print("\n   ✓ All required email settings are configured!")

print("\n" + "="*70 + "\n")
