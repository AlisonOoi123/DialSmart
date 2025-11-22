"""
Migration Script: Add website_url to brands table
Usage: python migrations/add_brand_website_url.py
"""
import os
import sys

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from sqlalchemy import text

def migrate():
    """Add website_url column to brands table"""
    app = create_app(os.getenv('FLASK_ENV', 'development'))

    with app.app_context():
        try:
            # Check if column already exists
            inspector = db.inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('brands')]

            if 'website_url' in columns:
                print("Column 'website_url' already exists in brands table. Skipping migration.")
                return

            # Add the column
            with db.engine.connect() as conn:
                conn.execute(text("ALTER TABLE brands ADD COLUMN website_url VARCHAR(500)"))
                conn.commit()

            print("Successfully added 'website_url' column to brands table!")

        except Exception as e:
            print(f"Error during migration: {e}")
            print("If the column already exists, you can ignore this error.")

if __name__ == '__main__':
    migrate()
