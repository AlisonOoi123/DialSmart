"""
Complete System Initialization for DialSmart
Creates database, user accounts, and imports CSV data
"""
from app import create_app, db
from app.models import User, Brand, Phone, PhoneSpecification
from werkzeug.security import generate_password_hash
from datetime import datetime
import sys

def initialize_database():
    """Create all database tables"""
    app = create_app()

    with app.app_context():
        print("\n" + "="*70)
        print("DialSmart System Initialization")
        print("="*70)

        # Step 1: Create database tables
        print("\n[1/3] Creating database tables with enhanced schema...")
        db.create_all()
        print("✓ Database tables created successfully!")

        # Step 2: Create default users
        print("\n[2/3] Creating default user accounts...")

        # Create admin user
        admin = User.query.filter_by(email='admin@dialsmart.my').first()
        if not admin:
            admin = User(
                full_name='Admin User',
                email='admin@dialsmart.my',
                password_hash=generate_password_hash('admin123'),
                is_admin=True,
                is_active=True,
                user_category='Working Professional',
                age_range='26-35'
            )
            db.session.add(admin)
            print("  ✓ Created admin account: admin@dialsmart.my / admin123")
        else:
            print("  ⊘ Admin account already exists")

        # Create regular user
        user = User.query.filter_by(email='user@dialsmart.my').first()
        if not user:
            user = User(
                full_name='Test User',
                email='user@dialsmart.my',
                password_hash=generate_password_hash('user123'),
                is_admin=False,
                is_active=True,
                user_category='Student',
                age_range='18-25'
            )
            db.session.add(user)
            print("  ✓ Created user account: user@dialsmart.my / user123")
        else:
            print("  ⊘ User account already exists")

        db.session.commit()
        print("\n✓ User accounts created successfully!")

        # Step 3: Import CSV data
        print("\n[3/3] Importing phone data from CSV...")
        print("-" * 70)

        # Import the CSV data
        from import_csv_dataset import CSVDatasetImporter
        importer = CSVDatasetImporter('fyp_phoneDataset.csv')

        # The import_csv creates its own app context, so we exit ours first
        return importer

def main():
    print("\n🚀 Starting DialSmart System Initialization...\n")

    importer = initialize_database()

    # Run CSV import
    print("\nNow importing CSV data...")
    importer.import_csv()

    print("\n" + "="*70)
    print("✅ SYSTEM INITIALIZATION COMPLETE!")
    print("="*70)
    print("\nYour DialSmart system is ready to use!")
    print("\nLogin Credentials:")
    print("  👤 Admin: admin@dialsmart.my / admin123")
    print("  👤 User:  user@dialsmart.my / user123")
    print("\nNext steps:")
    print("  1. Run the application: python run.py")
    print("  2. Open browser: http://127.0.0.1:5000")
    print("  3. Login and explore!")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
