"""
Database Migration Script for Oracle - Add Email Verification Columns
Adds new email verification and password reset fields to users table
"""
import oracledb
import os
from getpass import getpass

def migrate_oracle_database():
    """Add email verification and password reset columns to Oracle users table"""

    print("=" * 70)
    print("DialSmart Oracle Database Migration")
    print("Adding Email Verification & Password Reset Columns")
    print("=" * 70)
    print()

    # Get Oracle connection details
    print("Enter Oracle Database Connection Details:")
    username = input("Username (default: ds_user): ").strip() or "ds_user"
    password = getpass("Password: ")
    host = input("Host (default: localhost): ").strip() or "localhost"
    port = input("Port (default: 1521): ").strip() or "1521"
    service_name = input("Service Name (default: orclpdb): ").strip() or "orclpdb"

    # Build connection string (DSN)
    dsn = f"{host}:{port}/{service_name}"

    try:
        # Connect to Oracle
        print(f"\nConnecting to Oracle at {host}:{port}/{service_name}...")
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        cursor = connection.cursor()
        print("✅ Connected successfully!")
        print()

        # Check existing columns
        print("Checking existing columns in users table...")
        cursor.execute("""
            SELECT column_name
            FROM user_tab_columns
            WHERE table_name = 'USERS'
        """)

        existing_columns = [row[0].lower() for row in cursor.fetchall()]
        print(f"Found {len(existing_columns)} existing columns")
        print()

        columns_to_add = []

        # Email verification columns
        if 'email_verified' not in existing_columns:
            columns_to_add.append(('email_verified', 'NUMBER(1) DEFAULT 0'))

        if 'email_verification_token' not in existing_columns:
            columns_to_add.append(('email_verification_token', 'VARCHAR2(100)'))

        if 'email_verification_sent_at' not in existing_columns:
            columns_to_add.append(('email_verification_sent_at', 'TIMESTAMP'))

        # Password reset columns
        if 'password_reset_token' not in existing_columns:
            columns_to_add.append(('password_reset_token', 'VARCHAR2(100)'))

        if 'password_reset_sent_at' not in existing_columns:
            columns_to_add.append(('password_reset_sent_at', 'TIMESTAMP'))

        if not columns_to_add:
            print("✅ All columns already exist!")
            print("No migration needed.")
            cursor.close()
            connection.close()
            return True

        # Add missing columns
        print("Adding missing columns...")
        print()

        for column_name, column_type in columns_to_add:
            sql = f"ALTER TABLE users ADD {column_name} {column_type}"
            print(f"  Adding: {column_name} ({column_type})")
            cursor.execute(sql)

        # Auto-verify existing users
        if 'email_verified' in [col[0] for col in columns_to_add]:
            print()
            print("Auto-verifying existing users...")
            cursor.execute("UPDATE users SET email_verified = 1 WHERE email_verified IS NULL OR email_verified = 0")
            connection.commit()
            print(f"✅ Updated {cursor.rowcount} users")

        # Commit changes
        connection.commit()

        print()
        print("=" * 70)
        print("✅ Oracle Database Migration Completed Successfully!")
        print("=" * 70)
        print()
        print("Columns added:")
        for column_name, column_type in columns_to_add:
            print(f"  ✅ {column_name} ({column_type})")

        print()
        print("📝 Notes:")
        print("  - All existing users have been auto-verified")
        print("  - New users will require email verification if enabled")
        print("  - Password reset functionality is now available")

        cursor.close()
        connection.close()

        return True

    except oracledb.Error as e:
        print()
        print(f"❌ Oracle Error: {e}")
        print()
        return False
    except Exception as e:
        print()
        print(f"❌ Error: {str(e)}")
        print()
        return False


if __name__ == '__main__':
    try:
        success = migrate_oracle_database()

        if success:
            print()
            print("✅ Migration successful!")
            print()
            print("Next steps:")
            print("1. Update config.py with Oracle connection string")
            print("2. Install cx_Oracle: pip install cx-Oracle")
            print("3. Run: python run.py")
        else:
            print()
            print("❌ Migration failed! Please check the errors above.")

    except KeyboardInterrupt:
        print("\n\n❌ Migration cancelled by user.")
    except ImportError:
        print()
        print("❌ oracledb not installed!")
        print()
        print("Please install it:")
        print("  pip install oracledb")
        print()
    except Exception as e:
        print()
        print(f"❌ Unexpected error: {str(e)}")
        print()
