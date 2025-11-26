"""
Create Admin User with Secure Passkey
Run this script to create admin accounts for DialSmart
"""
from app import create_app, db
from app.models import User
import sys

# IMPORTANT: Change this secret admin passkey for production!
ADMIN_PASSKEY = "DialSmart2024Admin!"

def create_admin_user():
    """Create an admin user with passkey verification"""
    app = create_app()

    with app.app_context():
        print("=" * 70)
        print("DialSmart Admin Account Creator")
        print("=" * 70)

        # Verify admin passkey
        print("\nTo create an admin account, you must enter the admin passkey.")
        print("(Default passkey: DialSmart2024Admin!)")

        passkey = input("\nEnter admin passkey: ").strip()

        if passkey != ADMIN_PASSKEY:
            print("\n❌ ERROR: Invalid admin passkey!")
            print("Admin account creation cancelled.")
            sys.exit(1)

        print("\n✓ Passkey verified!\n")

        # Get admin details
        email = input("Enter admin email: ").strip()

        if not email:
            print("❌ ERROR: Email cannot be empty!")
            sys.exit(1)

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"\n❌ ERROR: User with email '{email}' already exists!")
            if existing_user.is_admin:
                print(f"   This user is already an admin.")
            else:
                print(f"   Converting existing user to admin...")
                existing_user.is_admin = True
                db.session.commit()
                print(f"\n✅ SUCCESS: '{email}' is now an admin!")
            sys.exit(0)

        password = input("Enter admin password: ").strip()

        if len(password) < 6:
            print("❌ ERROR: Password must be at least 6 characters!")
            sys.exit(1)

        full_name = input("Enter admin full name: ").strip()

        if not full_name:
            full_name = "Administrator"

        # Ask if this should be a super admin
        is_super = input("Make this a SUPER ADMIN? (y/n): ").strip().lower() == 'y'


        # Create admin user
        admin = User(
            email=email,
            full_name=full_name,
            is_admin=True,
            is_super_admin=is_super,
            is_active=True,
            user_category='Admin'
        )
        admin.set_password(password)

        db.session.add(admin)
        db.session.commit()

        print("\n" + "=" * 70)
        print("✅ SUCCESS: Admin account created successfully!")
        print("=" * 70)
        print(f"Email: {email}")
        print(f"Name: {full_name}")
        print(f"Admin: Yes")
        print("=" * 70)
        print("\nYou can now login at: http://localhost:5000/auth/login")
        print("=" * 70)

def create_default_admins():
    """Create two default admin accounts"""
    app = create_app()

    with app.app_context():
        print("=" * 70)
        print("Creating Default Admin Accounts")
        print("=" * 70)

        admins_data = [
            {
                'email': 'admin@dialsmart.my',
                'password': 'abcD1234#',
                'full_name': 'System Administrator',
                'is_super_admin': False  # Regular admin
            },
            {
                'email': 'superadmin@dialsmart.my',
                'password': 'super123#',
                'full_name': 'Super Administrator',
                'is_super_admin': True  # Super admin
            }
        ]

        created = 0
        for admin_data in admins_data:
            existing = User.query.filter_by(email=admin_data['email']).first()

            if existing:
                print(f"⚠  Admin already exists: {admin_data['email']}")
                if not existing.is_admin:
                    existing.is_admin = True
                    existing.is_super_admin = admin_data['is_super_admin']
                    db.session.commit()
                    print(f"   ✓ Converted to {'super admin' if admin_data['is_super_admin'] else 'admin'}")
                else:
                    # Update super admin status if needed
                    if admin_data['is_super_admin'] and not existing.is_super_admin:
                        existing.is_super_admin = True
                        db.session.commit()
                        print(f"   ✓ Upgraded to super admin")
                continue

            admin = User(
                email=admin_data['email'],
                full_name=admin_data['full_name'],
                is_admin=True,
                is_super_admin=admin_data['is_super_admin'],
                is_active=True,
                user_category='Admin'
            )
            admin.set_password(admin_data['password'])

            db.session.add(admin)
            created += 1
            print(f"✓ Created admin: {admin_data['email']}")

        db.session.commit()

        print("\n" + "=" * 70)
        print(f"✅ Created {created} new admin account(s)")
        print("=" * 70)
        print("\nDefault Admin Accounts:")
        print("  1. admin@dialsmart.my / abcD1234# (Regular Admin)")
        print("  2. superadmin@dialsmart.my / super123# (SUPER ADMIN)")
        print("\nLogin at: http://localhost:5000/auth/login")
        print("=" * 70)
        print("\n⚠  IMPORTANT: Only the SUPER ADMIN can create new admin accounts!")
        print("=" * 70)

if __name__ == '__main__':
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == '--default':
        # Create default admins
        create_default_admins()
    else:
        # Interactive mode with passkey
        create_admin_user()
