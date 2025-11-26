"""
Create an admin account for DialSmart
This script creates a secure admin account with proper password validation
"""
from app import create_app, db
from app.models import User
from app.utils.helpers import validate_password
import getpass

# Create application instance
app = create_app()

def create_admin():
    """Create admin account with secure password"""
    print("=" * 70)
    print("DialSmart Admin Account Creation")
    print("=" * 70)
    print()

    # Get admin details
    print("Enter admin details:")
    full_name = input("Full Name: ").strip()
    email = input("Email: ").strip()

    if not full_name or not email:
        print("\n❌ Error: Full name and email are required!")
        return

    # Check if email already exists
    with app.app_context():
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            print(f"\n❌ Error: Email '{email}' is already registered!")
            if existing_user.is_admin:
                print("   This account is already an admin.")
            else:
                print("   This account exists but is not an admin.")
            return

    print("\n" + "=" * 70)
    print("Password Requirements:")
    print("  • At least 8 characters long")
    print("  • Contains uppercase letter (A-Z)")
    print("  • Contains lowercase letter (a-z)")
    print("  • Contains number (0-9)")
    print("  • Contains special character (!@#$%^&*()_+-=[]{}|;:,.<>?)")
    print("=" * 70)
    print()

    # Get password with validation
    while True:
        password = getpass.getpass("Password: ")
        confirm_password = getpass.getpass("Confirm Password: ")

        if password != confirm_password:
            print("\n❌ Error: Passwords do not match! Please try again.\n")
            continue

        # Validate password strength
        is_valid, error_message = validate_password(password)
        if not is_valid:
            print(f"\n❌ Error: {error_message}")
            print("Please try again with a stronger password.\n")
            continue

        break

    # Create admin account
    with app.app_context():
        admin_user = User(
            full_name=full_name,
            email=email,
            user_category='Admin',
            is_admin=True,
            is_active=True
        )
        admin_user.set_password(password)

        try:
            db.session.add(admin_user)
            db.session.commit()

            print("\n" + "=" * 70)
            print("✅ Admin account created successfully!")
            print("=" * 70)
            print(f"\nAdmin Details:")
            print(f"  Name: {full_name}")
            print(f"  Email: {email}")
            print(f"  Role: Administrator")
            print("\nYou can now login at: /auth/login")
            print("=" * 70)

        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Error creating admin account: {str(e)}")

if __name__ == '__main__':
    try:
        create_admin()
    except KeyboardInterrupt:
        print("\n\n❌ Admin account creation cancelled.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
