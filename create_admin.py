"""
Create Admin Account Script
Simple script to create a new admin user for DialSmart
"""

import sys
import os
import getpass

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User
from app.utils.helpers import validate_password

def create_admin():
    """Create a new admin user"""

    app = create_app()

    with app.app_context():
        print()
        print("=" * 60)
        print("  DialSmart - Create Admin Account")
        print("=" * 60)
        print()

        # Get admin details
        full_name = input("Enter Full Name: ").strip()
        if not full_name:
            print("❌ Full name is required!")
            return False

        email = input("Enter Email: ").strip()
        if not email:
            print("❌ Email is required!")
            return False

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"❌ Error: Email '{email}' is already registered!")
            print()

            # Ask if they want to make this user an admin
            if not existing_user.is_admin:
                make_admin = input(f"Do you want to make '{existing_user.full_name}' an admin? (yes/no): ").strip().lower()
                if make_admin in ['yes', 'y']:
                    existing_user.is_admin = True
                    db.session.commit()
                    print()
                    print("✅ User successfully upgraded to admin!")
                    print(f"   Name: {existing_user.full_name}")
                    print(f"   Email: {existing_user.email}")
                    return True
                else:
                    print("Operation cancelled.")
                    return False
            else:
                print(f"This user is already an admin.")
                return False

        # Get password
        while True:
            password = getpass.getpass("Enter Password: ")
            if not password:
                print("❌ Password is required!")
                continue

            # Validate password strength
            is_valid, error_message = validate_password(password)
            if not is_valid:
                print(f"❌ {error_message}")
                continue

            confirm_password = getpass.getpass("Confirm Password: ")
            if password != confirm_password:
                print("❌ Passwords do not match!")
                continue

            break

        # Create admin user
        try:
            admin_user = User(
                full_name=full_name,
                email=email,
                user_category='Admin',
                is_admin=True,
                is_active=True,
                email_verified=True  # Auto-verify admin accounts
            )
            admin_user.set_password(password)

            db.session.add(admin_user)
            db.session.commit()

            print()
            print("=" * 60)
            print("✅ Admin account created successfully!")
            print("=" * 60)
            print(f"Name:  {admin_user.full_name}")
            print(f"Email: {admin_user.email}")
            print(f"Admin: Yes")
            print()
            print("You can now login at: http://localhost:5000/auth/login")
            print("=" * 60)
            print()

            return True

        except Exception as e:
            db.session.rollback()
            print()
            print(f"❌ Error creating admin account: {str(e)}")
            return False

if __name__ == '__main__':
    success = create_admin()
    sys.exit(0 if success else 1)
