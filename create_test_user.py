"""
Create a test user for chatbot testing
"""
from app import create_app, db
from app.models import User

# Create application instance
app = create_app()

with app.app_context():
    print("Creating test user...")

    # Check if test user already exists
    test_user = User.query.filter_by(email='user@dialsmart.my').first()

    if test_user:
        print("✓ Test user already exists: user@dialsmart.my")
    else:
        test_user = User(
            email='user@dialsmart.my',
            full_name='Test User',
            user_category='Working Professional',
            age_range='26-35'
        )
        test_user.set_password('password123')
        db.session.add(test_user)
        db.session.commit()
        print("✓ Test user created successfully!")

    print("\n✅ You can now login with:")
    print("Email: user@dialsmart.my")
    print("Password: password123")
