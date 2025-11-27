"""
Migration Script: Add is_super_admin column to users table
Run this script to add the is_super_admin column to existing databases
"""
import sqlite3
import os
import sys

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import User

def migrate_add_is_super_admin():
    """Add is_super_admin column to users table"""
    app = create_app()

    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('users')]

            if 'is_super_admin' in columns:
                print("✓ Column 'is_super_admin' already exists in users table.")
                return

            # Add the column using raw SQL
            with db.engine.connect() as conn:
                # For SQLite
                if 'sqlite' in str(db.engine.url):
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT 0"))
                    conn.commit()
                    print("✓ Added 'is_super_admin' column to users table (SQLite)")

                # For other databases (PostgreSQL, MySQL, etc.)
                else:
                    conn.execute(db.text("ALTER TABLE users ADD COLUMN is_super_admin BOOLEAN DEFAULT FALSE"))
                    conn.commit()
                    print("✓ Added 'is_super_admin' column to users table")

            # Update existing admins - make the first admin a super admin
            first_admin = User.query.filter_by(is_admin=True).order_by(User.created_at).first()
            if first_admin:
                first_admin.is_super_admin = True
                db.session.commit()
                print(f"✓ Set {first_admin.email} as super admin (first admin account)")
            else:
                print("⚠ No admin users found. Please create a super admin manually.")

            print("\n✅ Migration completed successfully!")
            print("\nIMPORTANT:")
            print("- The first admin account has been promoted to super admin")
            print("- Only super admins can suspend/activate users")
            print("- To promote other admins to super admin, update them in the database:")
            print("  UPDATE users SET is_super_admin = 1 WHERE email = 'admin@example.com';")

        except Exception as e:
            print(f"❌ Migration failed: {str(e)}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("="*60)
    print("Migration: Add is_super_admin column")
    print("="*60)
    migrate_add_is_super_admin()
