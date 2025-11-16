"""
Clear All Phone Data from Oracle Database
Drops all phones, specifications, recommendations, comparisons, and user preferences
"""
import os
import sys

# Set DB_TYPE to Oracle
os.environ['DB_TYPE'] = 'oracle'

from app import create_app, db
from app.models import Phone, PhoneSpecification, Brand, Recommendation, Comparison, UserPreference, ChatHistory

print("\n" + "="*70)
print("DialSmart: Clear All Phone Data")
print("="*70)
print("\n⚠️  WARNING: This will delete ALL phone data from the database!")
print("   - All phones and specifications")
print("   - All brands")
print("   - All recommendations")
print("   - All comparisons")
print("   - All user preferences")
print("   - All chat history")
print("\n" + "="*70)

response = input("\nAre you sure you want to continue? (yes/no): ")

if response.lower() != 'yes':
    print("\n✗ Operation cancelled.")
    sys.exit(0)

app = create_app()

with app.app_context():
    try:
        print("\n[1/6] Deleting chat history...")
        deleted_chat = ChatHistory.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_chat} chat records")

        print("\n[2/6] Deleting user preferences...")
        deleted_prefs = UserPreference.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_prefs} user preferences")

        print("\n[3/6] Deleting comparisons...")
        deleted_comparisons = Comparison.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_comparisons} comparisons")

        print("\n[4/6] Deleting recommendations...")
        deleted_recommendations = Recommendation.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_recommendations} recommendations")

        print("\n[5/6] Deleting phone specifications...")
        deleted_specs = PhoneSpecification.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_specs} specifications")

        print("\n[6/6] Deleting phones and brands...")
        deleted_phones = Phone.query.delete()
        deleted_brands = Brand.query.delete()
        db.session.commit()
        print(f"  ✓ Deleted {deleted_phones} phones")
        print(f"  ✓ Deleted {deleted_brands} brands")

        print("\n" + "="*70)
        print("✓ ALL PHONE DATA CLEARED SUCCESSFULLY!")
        print("="*70)

        print(f"\nDatabase is now empty and ready for fresh import.")
        print(f"\nNext Step:")
        print(f"  1. Update fyp_phoneDataset.csv with your new data")
        print(f"  2. Run: python import_csv_to_oracle.py")

        print("\n" + "="*70 + "\n")

    except Exception as e:
        db.session.rollback()
        print(f"\n✗ Error clearing data: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
