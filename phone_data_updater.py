"""
Phone Data Updater
Automated system for collecting and updating phone data from various sources
"""
import requests
import json
import csv
from datetime import datetime
from app import create_app, db
from app.models import Phone, PhoneSpecification, Brand
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PhoneDataUpdater:
    """Handles automated phone data collection and updates"""

    def __init__(self):
        """Initialize the updater with Flask app context"""
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def __del__(self):
        """Cleanup app context"""
        if hasattr(self, 'app_context'):
            self.app_context.pop()

    def update_all_prices(self):
        """
        Update prices for all phones from various sources
        You can integrate with real price APIs here
        """
        logger.info("Starting price update for all phones...")

        try:
            phones = Phone.query.filter_by(is_active=True).all()
            updated_count = 0

            for phone in phones:
                try:
                    # TODO: Integrate with real price API
                    # For now, this is a placeholder
                    # Example: new_price = self.fetch_price_from_api(phone.model_name)

                    # Simulate price update (for demonstration)
                    # In production, replace this with actual API calls
                    logger.info(f"Checking price for: {phone.model_name}")

                    # You can add your API integration here
                    # Examples of APIs you might use:
                    # 1. GSMArena API
                    # 2. PhoneDB API
                    # 3. Retailer APIs (Amazon, Shopee, Lazada, etc.)

                    updated_count += 1

                except Exception as e:
                    logger.error(f"Error updating price for {phone.model_name}: {str(e)}")
                    continue

            db.session.commit()
            logger.info(f"Price update completed. Checked {updated_count} phones.")
            return updated_count

        except Exception as e:
            logger.error(f"Price update failed: {str(e)}")
            db.session.rollback()
            return 0

    def check_new_launches(self):
        """
        Check for new phone launches and add them to database
        """
        logger.info("Checking for new phone launches...")

        try:
            # TODO: Integrate with phone launch announcement APIs
            # Examples:
            # 1. GSMArena newest phones
            # 2. PhoneArena API
            # 3. Brand official APIs (Samsung, Apple, etc.)

            # Placeholder for new phone detection
            new_phones_count = 0

            # Example implementation structure:
            # new_phones = self.fetch_new_phones_from_api()
            # for phone_data in new_phones:
            #     if not self.phone_exists(phone_data['model_name']):
            #         self.add_new_phone(phone_data)
            #         new_phones_count += 1

            logger.info(f"New phone check completed. Found {new_phones_count} new phones.")
            return new_phones_count

        except Exception as e:
            logger.error(f"New phone check failed: {str(e)}")
            return 0

    def fetch_price_from_api(self, model_name):
        """
        Fetch price from external API

        Args:
            model_name: Phone model name

        Returns:
            float: Updated price or None if not found
        """
        # TODO: Implement actual API integration
        # Example structure for price API:

        # try:
        #     # Example: E-commerce API
        #     api_url = f"https://api.example.com/prices?q={model_name}"
        #     response = requests.get(api_url, timeout=10)
        #
        #     if response.status_code == 200:
        #         data = response.json()
        #         return data.get('price')
        #
        # except requests.RequestException as e:
        #     logger.error(f"API request failed: {str(e)}")

        return None

    def import_from_csv(self, csv_file_path):
        """
        Import phone data from CSV file

        Args:
            csv_file_path: Path to CSV file with phone data

        Returns:
            dict: Import statistics
        """
        logger.info(f"Importing phones from CSV: {csv_file_path}")

        stats = {
            'total': 0,
            'added': 0,
            'updated': 0,
            'skipped': 0,
            'errors': 0
        }

        try:
            with open(csv_file_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    stats['total'] += 1

                    try:
                        # Get or create brand
                        brand_name = row.get('brand', '').strip()
                        if not brand_name:
                            stats['skipped'] += 1
                            continue

                        brand = Brand.query.filter(
                            Brand.name.ilike(f"%{brand_name}%")
                        ).first()

                        if not brand:
                            brand = Brand(name=brand_name, is_active=True)
                            db.session.add(brand)
                            db.session.flush()

                        # Check if phone exists
                        model_name = row.get('model_name', '').strip()
                        existing_phone = Phone.query.filter_by(
                            model_name=model_name,
                            brand_id=brand.id
                        ).first()

                        if existing_phone:
                            # Update existing phone
                            existing_phone.price = float(row.get('price', 0))
                            existing_phone.main_image = row.get('main_image', '')
                            stats['updated'] += 1
                        else:
                            # Add new phone
                            new_phone = Phone(
                                model_name=model_name,
                                brand_id=brand.id,
                                price=float(row.get('price', 0)),
                                main_image=row.get('main_image', ''),
                                is_active=True
                            )
                            db.session.add(new_phone)
                            db.session.flush()

                            # Add specifications if available
                            if row.get('ram_options') or row.get('internal_storage'):
                                specs = PhoneSpecification(
                                    phone_id=new_phone.id,
                                    ram_options=row.get('ram_options'),
                                    internal_storage=row.get('internal_storage'),
                                    battery_capacity=row.get('battery_capacity'),
                                    rear_camera_main=row.get('rear_camera_main'),
                                    display_size=row.get('display_size'),
                                    display_type=row.get('display_type'),
                                    chipset=row.get('chipset'),
                                    network_5g=row.get('network_5g')
                                )
                                db.session.add(specs)

                            stats['added'] += 1

                    except Exception as e:
                        logger.error(f"Error processing row {stats['total']}: {str(e)}")
                        stats['errors'] += 1
                        continue

                db.session.commit()
                logger.info(f"CSV import completed: {stats}")

        except FileNotFoundError:
            logger.error(f"CSV file not found: {csv_file_path}")
            stats['errors'] += 1
        except Exception as e:
            logger.error(f"CSV import failed: {str(e)}")
            db.session.rollback()
            stats['errors'] += 1

        return stats

    def generate_price_report(self):
        """
        Generate daily price change report
        """
        logger.info("Generating price report...")

        try:
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'total_phones': Phone.query.filter_by(is_active=True).count(),
                'total_brands': Brand.query.filter_by(is_active=True).count(),
                'timestamp': datetime.now().isoformat()
            }

            # Save report to file
            report_file = f"reports/price_report_{report['date']}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)

            logger.info(f"Report generated: {report_file}")
            return report

        except Exception as e:
            logger.error(f"Report generation failed: {str(e)}")
            return None

    def phone_exists(self, model_name):
        """Check if phone already exists in database"""
        return Phone.query.filter(
            Phone.model_name.ilike(f"%{model_name}%")
        ).first() is not None


def main():
    """Main function for manual testing"""
    updater = PhoneDataUpdater()

    print("=" * 60)
    print("Phone Data Updater - Manual Mode")
    print("=" * 60)
    print()
    print("1. Update all prices")
    print("2. Check for new launches")
    print("3. Import from CSV")
    print("4. Generate price report")
    print()

    choice = input("Enter your choice (1-4): ")

    if choice == '1':
        updater.update_all_prices()
    elif choice == '2':
        updater.check_new_launches()
    elif choice == '3':
        csv_path = input("Enter CSV file path: ")
        stats = updater.import_from_csv(csv_path)
        print(f"\nImport Statistics: {stats}")
    elif choice == '4':
        updater.generate_price_report()
    else:
        print("Invalid choice")


if __name__ == '__main__':
    main()
