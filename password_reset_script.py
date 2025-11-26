"""
Reset Admin Passwords
This script resets passwords for specific admin accounts
"""
from app import create_app, db
from app.models import User

def reset_admin_passwords():
    """Reset passwords for the two admin accounts"""
    app = create_app()
    
    with app.app_context():
        print("=" * 70)
        print("Resetting Admin Passwords")
        print("=" * 70)
        
        # New password for both accounts
        new_password = "Abcd1234#"
        
        # Admin accounts to reset
        admin_emails = [
            'gansy-wm22@student.tarc.edu.my',
            'alison99690326@gmail.com'
        ]
        
        reset_count = 0
        
        for email in admin_emails:
            admin = User.query.filter_by(email=email).first()
            
            if admin:
                # Use the User model's set_password method to hash properly
                admin.set_password(new_password)
                admin.force_password_change = False  # Optional: remove forced change
                reset_count += 1
                print(f"✓ Password reset for: {email}")
            else:
                print(f"✗ Admin not found: {email}")
        
        # Commit all changes
        db.session.commit()
        
        print("\n" + "=" * 70)
        print(f"✅ Successfully reset {reset_count} admin password(s)")
        print("=" * 70)
        print("\nUpdated Accounts:")
        print(f"  1. gansy-wm22@student.tarc.edu.my / Abcd1234#")
        print(f"  2. alison99690326@gmail.com / Abcd1234#")
        print("\nYou can now login with these credentials.")
        print("=" * 70)

if __name__ == '__main__':
    reset_admin_passwords()
