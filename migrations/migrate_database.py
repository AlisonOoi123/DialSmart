"""
Database Migration Script - Add Email Verification Columns
Adds new email verification fields to existing users table
"""
import sqlite3
import os

def migrate_database():
    """Add email verification columns to users table"""

    # Get database path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dialsmart.db')

    if not os.path.exists(db_path):
        print(f"❌ Database not found at: {db_path}")
        print("Please ensure the database file exists.")
        return False

    print(f"Migrating database: {db_path}")
    print("=" * 70)

    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if columns already exist
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]

        columns_to_add = []

        # Email verification columns
        if 'email_verified' not in columns:
            columns_to_add.append(('email_verified', 'INTEGER DEFAULT 0'))

        if 'email_verification_token' not in columns:
            columns_to_add.append(('email_verification_token', 'VARCHAR(100)'))

        if 'email_verification_sent_at' not in columns:
            columns_to_add.append(('email_verification_sent_at', 'DATETIME'))

        # Password reset columns
        if 'password_reset_token' not in columns:
            columns_to_add.append(('password_reset_token', 'VARCHAR(100)'))

        if 'password_reset_sent_at' not in columns:
            columns_to_add.append(('password_reset_sent_at', 'DATETIME'))

        if not columns_to_add:
            print("✅ All email verification columns already exist!")
            print("No migration needed.")
            conn.close()
            return True

        # Add missing columns
        for column_name, column_type in columns_to_add:
            sql = f"ALTER TABLE users ADD COLUMN {column_name} {column_type}"
            print(f"Adding column: {column_name}")
            cursor.execute(sql)

        # Auto-verify all existing users (so they can login immediately)
        if 'email_verified' in [col[0] for col in columns_to_add]:
            cursor.execute("UPDATE users SET email_verified = 1 WHERE email_verified IS NULL OR email_verified = 0")
            updated_count = cursor.rowcount
            print(f"✅ Auto-verified {updated_count} existing users")

        # Commit changes
        conn.commit()
        conn.close()

        print("\n" + "=" * 70)
        print("✅ Database migration completed successfully!")
        print("=" * 70)
        print("\nNew columns added:")
        for column_name, column_type in columns_to_add:
            print(f"  - {column_name} ({column_type})")

        print("\n📝 Notes:")
        print("  - All existing users have been auto-verified")
        print("  - New users will require email verification if enabled in .env")
        print("  - You can now start the application")

        return True

    except sqlite3.Error as e:
        print(f"\n❌ Database migration failed: {str(e)}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        return False


if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("DialSmart Database Migration")
    print("Adding Email Verification Columns")
    print("=" * 70)
    print()

    success = migrate_database()

    if success:
        print("\n✅ Migration successful! You can now run: python run.py")
    else:
        print("\n❌ Migration failed! Please check the errors above.")
        print("\nAlternative: Delete dialsmart.db and restart the app to create a fresh database.")
