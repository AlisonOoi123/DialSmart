"""
Phone Data Updater for Malaysian Market
Automatically updates phone prices and new launches
"""
from app import create_app, db
from app.models import Phone, PhoneSpecification, Brand
from datetime import datetime
import json
import time

class PhoneDataUpdater:
    """
    Manages phone data updates for Malaysian market

    NOTE: This is a template for web scraping.
    In production, you would integrate with APIs from:
    - Lazada Malaysia
    - Shopee Malaysia
    - PriceSpy Malaysia
    - GSMArena

    Or use official retailer APIs where available.
    """

    def __init__(self):
        self.app = create_app()
        self.updated_count = 0
        self.new_phones_count = 0

    def update_all_prices(self):
        """Update prices for all existing phones"""
        with self.app.app_context():
            print("=" * 60)
            print("DIALSMART PRICE UPDATER")
            print("=" * 60)
            print("\n[INFO] Starting price update process...")

            phones = Phone.query.filter_by(is_active=True).all()
            print(f"[INFO] Found {len(phones)} active phones to check")

            for phone in phones:
                try:
                    # Get latest price from Malaysian retailers
                    new_price = self._fetch_latest_price(phone)

                    if new_price and new_price != phone.price:
                        old_price = phone.price
                        phone.price = new_price
                        phone.updated_at = datetime.utcnow()

                        self.updated_count += 1
                        price_change = ((new_price - old_price) / old_price) * 100

                        print(f"  ✓ Updated: {phone.model_name}")
                        print(f"    Old: RM {old_price:,.2f} → New: RM {new_price:,.2f} ({price_change:+.1f}%)")

                    time.sleep(0.5)  # Rate limiting

                except Exception as e:
                    print(f"  ✗ Error updating {phone.model_name}: {str(e)}")

            db.session.commit()

            print(f"\n[COMPLETE] Updated {self.updated_count} phone prices")

    def check_new_launches(self):
        """Check for new phone launches in Malaysian market"""
        with self.app.app_context():
            print("\n[INFO] Checking for new phone launches...")

            # This would fetch from Malaysian tech news, retailer APIs, etc.
            new_phones = self._fetch_new_launches()

            for phone_data in new_phones:
                existing = Phone.query.filter_by(
                    model_name=phone_data['model_name']
                ).first()

                if not existing:
                    self._add_new_phone(phone_data)
                    self.new_phones_count += 1

            print(f"[COMPLETE] Added {self.new_phones_count} new phones")

    def _fetch_latest_price(self, phone):
        """
        Fetch latest price from Malaysian retailers

        In production, integrate with:
        1. Lazada Malaysia API
        2. Shopee Malaysia API
        3. Price comparison websites
        4. Official brand stores

        Returns price in MYR
        """
        # TEMPLATE: Replace with actual API calls

        # Example: Lazada Malaysia
        # lazada_price = self._get_lazada_price(phone.model_name)

        # Example: Shopee Malaysia
        # shopee_price = self._get_shopee_price(phone.model_name)

        # Example: Price aggregation
        # prices = [p for p in [lazada_price, shopee_price] if p]
        # return min(prices) if prices else None

        # For now, return current price (no change)
        return phone.price

    def _fetch_new_launches(self):
        """
        Fetch new phone launches

        In production, scrape from:
        1. GSMArena Malaysia
        2. SoyaCincau (Malaysian tech news)
        3. Lowyat.NET
        4. Amanz
        5. Brand official websites
        """
        # TEMPLATE: Return empty list
        # In production, this would return newly launched phones
        return []

    def _add_new_phone(self, phone_data):
        """Add a new phone to database"""
        try:
            brand = Brand.query.filter_by(name=phone_data['brand']).first()
            if not brand:
                print(f"  ✗ Brand not found: {phone_data['brand']}")
                return

            phone = Phone(
                brand_id=brand.id,
                model_name=phone_data['model_name'],
                price=phone_data['price'],
                availability_status=phone_data.get('availability_status', 'Available'),
                release_date=phone_data.get('release_date')
            )
            db.session.add(phone)
            db.session.flush()

            if 'specs' in phone_data:
                specs = PhoneSpecification(
                    phone_id=phone.id,
                    **phone_data['specs']
                )
                db.session.add(specs)

            db.session.commit()
            print(f"  ✓ Added new phone: {phone.model_name} - RM {phone.price:,.2f}")

        except Exception as e:
            print(f"  ✗ Error adding phone: {str(e)}")
            db.session.rollback()

    def generate_price_report(self):
        """Generate price comparison report"""
        with self.app.app_context():
            print("\n" + "=" * 60)
            print("PRICE ANALYSIS REPORT")
            print("=" * 60)

            # Price by brand
            brands = Brand.query.filter_by(is_active=True).all()

            print("\nAverage Price by Brand (MYR):")
            print("-" * 60)

            for brand in brands:
                phones = Phone.query.filter_by(
                    brand_id=brand.id,
                    is_active=True
                ).all()

                if phones:
                    avg_price = sum(p.price for p in phones) / len(phones)
                    min_price = min(p.price for p in phones)
                    max_price = max(p.price for p in phones)

                    print(f"{brand.name:15} | Avg: RM {avg_price:7,.0f} | "
                          f"Range: RM {min_price:6,.0f} - RM {max_price:6,.0f} | "
                          f"Models: {len(phones)}")

            # Price segments
            print("\n\nPrice Segments:")
            print("-" * 60)

            segments = {
                'Budget (Under RM1000)': (0, 1000),
                'Mid-Range (RM1000-2000)': (1000, 2000),
                'Upper Mid (RM2000-3000)': (2000, 3000),
                'Premium (RM3000-4500)': (3000, 4500),
                'Flagship (Above RM4500)': (4500, 999999)
            }

            for segment_name, (min_p, max_p) in segments.items():
                count = Phone.query.filter(
                    Phone.is_active == True,
                    Phone.price >= min_p,
                    Phone.price < max_p
                ).count()

                print(f"{segment_name:30} | {count:3} phones")

            print("\n" + "=" * 60)


def update_manual_phone(model_name, new_price):
    """Manually update a specific phone's price"""
    app = create_app()

    with app.app_context():
        phone = Phone.query.filter_by(model_name=model_name).first()

        if phone:
            old_price = phone.price
            phone.price = new_price
            phone.updated_at = datetime.utcnow()
            db.session.commit()

            print(f"✓ Updated {model_name}")
            print(f"  Old: RM {old_price:,.2f} → New: RM {new_price:,.2f}")
        else:
            print(f"✗ Phone not found: {model_name}")


def main():
    """Main updater function"""
    import sys

    updater = PhoneDataUpdater()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == 'prices':
            updater.update_all_prices()

        elif command == 'new':
            updater.check_new_launches()

        elif command == 'report':
            updater.generate_price_report()

        elif command == 'all':
            updater.update_all_prices()
            updater.check_new_launches()
            updater.generate_price_report()

        elif command == 'manual' and len(sys.argv) == 4:
            model = sys.argv[2]
            price = float(sys.argv[3])
            update_manual_phone(model, price)

        else:
            print("Unknown command!")
            print_usage()
    else:
        print_usage()


def print_usage():
    """Print usage instructions"""
    print("""
DialSmart Phone Data Updater
============================

Usage:
  python phone_data_updater.py [command]

Commands:
  prices          Update all phone prices
  new             Check for new phone launches
  report          Generate price analysis report
  all             Run all update tasks
  manual <model> <price>  Manually update a phone's price

Examples:
  python phone_data_updater.py prices
  python phone_data_updater.py report
  python phone_data_updater.py manual "iPhone 15 Pro" 5299.00

Note: To enable automatic updates, configure the web scraping
      functions in _fetch_latest_price() and _fetch_new_launches()
      with Malaysian retailer APIs or web scraping logic.
    """)


if __name__ == '__main__':
    main()
