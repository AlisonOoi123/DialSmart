"""
Lowyat.NET Web Scraper for Malaysian Phone Database
Scrapes phone data with MYR pricing from Lowyat.NET
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from datetime import datetime
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

class LowyatScraper:
    """
    Scraper for Lowyat.NET Malaysia
    Website: https://www.lowyat.net/
    """

    def __init__(self):
        self.base_url = "https://www.lowyat.net"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,ms;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Cache-Control': 'max-age=0',
        }
        self.app = create_app()
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_phone_specs(self, max_phones=50):
        """
        Scrape phone specifications from Lowyat phone database

        Args:
            max_phones: Maximum number of phones to scrape

        Returns:
            List of phone data dictionaries
        """
        print(f"\n[INFO] Scraping phone specifications from Lowyat.NET...")

        phones_data = []

        # Lowyat phone specs URLs - they have a searchable database
        # Format: https://www.lowyat.net/phones/[brand]/
        brands = ['samsung', 'apple', 'xiaomi', 'oppo', 'vivo', 'realme',
                  'honor', 'oneplus', 'huawei', 'nokia', 'motorola', 'asus']

        for brand in brands:
            try:
                print(f"\n[INFO] Scraping {brand.upper()} phones...")

                # Lowyat specs page format
                url = f"{self.base_url}/phones/{brand}/"

                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find phone listings (adjust selectors based on actual HTML)
                    phone_items = soup.find_all(['div', 'article'], class_=re.compile(r'phone|product|item|card'))

                    if not phone_items:
                        # Try alternative selectors
                        phone_items = soup.find_all('a', href=re.compile(rf'/phones/{brand}/'))

                    print(f"[INFO] Found {len(phone_items)} {brand} phone entries")

                    for item in phone_items[:max_phones]:
                        try:
                            phone_data = self._extract_phone_data(item, brand)
                            if phone_data:
                                phones_data.append(phone_data)

                                if len(phones_data) >= max_phones:
                                    print(f"[INFO] Reached maximum limit of {max_phones} phones")
                                    return phones_data

                        except Exception as e:
                            continue

                    time.sleep(2)  # Rate limiting

                else:
                    print(f"[WARN] Could not access {brand} page (status {response.status_code})")

            except Exception as e:
                print(f"[ERROR] Failed to scrape {brand}: {str(e)}")
                continue

        print(f"\n[INFO] Total phones scraped: {len(phones_data)}")
        return phones_data

    def _extract_phone_data(self, element, brand):
        """Extract phone data from HTML element"""
        try:
            phone_data = {
                'brand': brand.capitalize(),
                'scraped_at': datetime.utcnow()
            }

            # Extract model name
            title = element.find(['h2', 'h3', 'h4', 'a'])
            if title:
                phone_data['model_name'] = title.get_text(strip=True)
            else:
                return None

            # Extract price (look for MYR/RM patterns)
            price_text = element.get_text()
            price_match = re.search(r'RM\s*(\d+[,\d]*)', price_text, re.IGNORECASE)
            if price_match:
                price_str = price_match.group(1).replace(',', '')
                phone_data['price'] = float(price_str)

            # Extract specs from text content
            specs_text = element.get_text()

            # Screen size
            screen_match = re.search(r'(\d+\.?\d*)["\s]*inch', specs_text, re.IGNORECASE)
            if screen_match:
                phone_data['screen_size'] = float(screen_match.group(1))

            # RAM
            ram_match = re.search(r'(\d+)\s*GB\s*RAM', specs_text, re.IGNORECASE)
            if ram_match:
                phone_data['ram'] = f"{ram_match.group(1)}GB"

            # Storage
            storage_match = re.search(r'(\d+)\s*GB\s*(?:storage|ROM)', specs_text, re.IGNORECASE)
            if storage_match:
                phone_data['storage'] = f"{storage_match.group(1)}GB"

            # Camera
            camera_match = re.search(r'(\d+)\s*MP', specs_text, re.IGNORECASE)
            if camera_match:
                phone_data['camera'] = int(camera_match.group(1))

            # Battery
            battery_match = re.search(r'(\d+)\s*mAh', specs_text, re.IGNORECASE)
            if battery_match:
                phone_data['battery'] = int(battery_match.group(1))

            # 5G
            phone_data['has_5g'] = bool(re.search(r'5G', specs_text, re.IGNORECASE))

            return phone_data

        except Exception as e:
            return None

    def save_to_database(self, phones_data):
        """Save scraped phone data to database"""
        with self.app.app_context():
            saved_count = 0
            skipped_count = 0

            for phone_data in phones_data:
                try:
                    # Get or create brand
                    brand_name = phone_data.get('brand', 'Unknown')
                    brand = Brand.query.filter_by(name=brand_name).first()

                    if not brand:
                        brand = Brand(
                            name=brand_name,
                            description=f"{brand_name} smartphones",
                            is_active=True
                        )
                        db.session.add(brand)
                        db.session.flush()
                        print(f"  [+] Created brand: {brand_name}")

                    # Check if phone already exists
                    model_name = phone_data.get('model_name', '')
                    existing_phone = Phone.query.filter_by(
                        brand_id=brand.id,
                        model_name=model_name
                    ).first()

                    if existing_phone:
                        skipped_count += 1
                        continue

                    # Create phone
                    phone = Phone(
                        brand_id=brand.id,
                        model_name=model_name,
                        price=phone_data.get('price', 0.0),
                        availability_status='Available',
                        release_date=datetime.utcnow().date(),
                        is_featured=False,
                        is_active=True
                    )
                    db.session.add(phone)
                    db.session.flush()

                    # Create specifications
                    specs = PhoneSpecification(
                        phone_id=phone.id,
                        screen_size=phone_data.get('screen_size'),
                        processor=phone_data.get('processor', 'Not specified'),
                        ram_options=phone_data.get('ram', '4GB'),
                        storage_options=phone_data.get('storage', '64GB'),
                        rear_camera_main=phone_data.get('camera', 12),
                        battery_capacity=phone_data.get('battery', 4000),
                        has_5g=phone_data.get('has_5g', False)
                    )
                    db.session.add(specs)

                    db.session.commit()
                    saved_count += 1

                    price_display = f"RM {phone.price:,.2f}" if phone.price else "Price N/A"
                    print(f"  [✓] Added: {phone.model_name} - {price_display}")

                except Exception as e:
                    db.session.rollback()
                    print(f"  [✗] Failed to save {phone_data.get('model_name', 'Unknown')}: {str(e)}")
                    continue

            print(f"\n{'='*60}")
            print(f"Scraping Summary:")
            print(f"  • Total scraped: {len(phones_data)}")
            print(f"  • Successfully saved: {saved_count}")
            print(f"  • Skipped (duplicates): {skipped_count}")
            print(f"{'='*60}\n")


def main():
    import sys

    # Get limit from command line argument
    limit = 50
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Invalid limit. Using default: 50")

    print(f"\nStarting Lowyat.NET scraper (limit: {limit} phones)...")
    print("This may take several minutes...\n")

    print("="*60)
    print("Lowyat.NET Phone Scraper for DialSmart")
    print("="*60)

    scraper = LowyatScraper()

    # Scrape phones
    phones_data = scraper.scrape_phone_specs(max_phones=limit)

    if phones_data:
        print(f"\n[INFO] Scraped {len(phones_data)} phones successfully")
        print("[INFO] Saving to database...")
        scraper.save_to_database(phones_data)
    else:
        print("\n[ERROR] No phone data collected. Check website structure or network connection.")


if __name__ == "__main__":
    main()
