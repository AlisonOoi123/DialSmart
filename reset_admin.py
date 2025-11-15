"""
Reset Admin Account - Delete existing and create fresh admin
"""
from app import create_app, db
from app.models import User
from datetime import datetime

app = create_app()

with app.app_context():
    print("\n" + "="*70)
    print("Resetting Admin Account")
    print("="*70)

    # Delete existing admin accounts
    existing_admins = User.query.filter_by(is_admin=True).all()
    if existing_admins:
        print(f"\n✓ Found {len(existing_admins)} existing admin account(s)")
        for admin in existing_admins:
            print(f"  • Deleting: {admin.email}")
            db.session.delete(admin)
        db.session.commit()
        print("✓ Existing admin accounts deleted")
    else:
        print("\n• No existing admin accounts found")

    # Create fresh admin account
    print("\nCreating new admin account...")
    admin = User(
        full_name='DialSmart Admin',
        email='admin@dialsmart.com',
        is_admin=True,
        is_active=True,
        user_category='Working Professional',
        age_range='26-35',
        created_at=datetime.utcnow(),
        last_active=datetime.utcnow()
    )
    admin.set_password('admin123')

    db.session.add(admin)
    db.session.commit()

    print("\n✓ New admin account created successfully!")
    print("\n" + "="*70)
    print("Admin Login Credentials:")
    print("="*70)
    print(f"  Email: admin@dialsmart.com")
    print(f"  Password: admin123")
    print("="*70)
    print("\nYou can now login at: http://localhost:5000/auth/login")
    print("="*70 + "\n")
