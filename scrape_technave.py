"""
TechNave Web Scraper for Malaysian Phone Database
Scrapes phone data with MYR pricing from TechNave Malaysia
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from datetime import datetime, date
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

class TechNaveScraper:
    """
    Scraper for TechNave Malaysia
    Website: https://www.technave.com/
    """

    def __init__(self):
        self.base_url = "https://www.technave.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
        }
        self.app = create_app()
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_phone_list(self, brand_name=None, max_pages=5):
        """
        Scrape phone listings from TechNave

        Args:
            brand_name: Optional brand filter (e.g., 'Samsung', 'Apple')
            max_pages: Maximum number of pages to scrape

        Returns:
            List of phone URLs
        """
        print(f"\n[INFO] Scraping phone list from TechNave...")

        # TechNave phone review URLs
        phone_urls = []

        # Main phone review page
        review_url = f"{self.base_url}/devices/"

        try:
            response = self.session.get(review_url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find phone listing articles
            # Adjust selectors based on actual TechNave HTML structure
            phone_links = soup.find_all('a', href=re.compile(r'/devices/.*-review'))

            for link in phone_links[:50]:  # Limit to first 50 phones
                url = link.get('href')
                if url:
                    full_url = url if url.startswith('http') else f"{self.base_url}{url}"
                    if full_url not in phone_urls:
                        phone_urls.append(full_url)

            print(f"[INFO] Found {len(phone_urls)} phone review URLs")

        except Exception as e:
            print(f"[ERROR] Failed to scrape phone list: {str(e)}")

        return phone_urls

    def scrape_phone_details(self, url):
        """
        Scrape detailed phone information from a review page

        Args:
            url: Phone review URL

        Returns:
            Dictionary with phone details
        """
        try:
            print(f"  [•] Scraping: {url}")

            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract phone data (adjust selectors based on actual HTML)
            phone_data = {
                'url': url,
                'scraped_at': datetime.utcnow()
            }

            # Extract model name from title or heading
            title = soup.find('h1', class_='entry-title')
            if title:
                phone_data['model_name'] = self._clean_text(title.text)

            # Extract specs from review content
            specs_section = soup.find('div', class_='specs') or soup.find('table', class_='specifications')

            if specs_section:
                phone_data['specs'] = self._parse_specs(specs_section)

            # Extract price - look for MYR mentions
            price_pattern = re.compile(r'RM\s*[\d,]+(?:\.\d{2})?', re.IGNORECASE)
            content = soup.get_text()
            price_matches = price_pattern.findall(content)

            if price_matches:
                # Clean and convert to float
                price_str = price_matches[0].replace('RM', '').replace(',', '').strip()
                phone_data['price'] = float(price_str)

            # Extract brand from model name
            phone_data['brand'] = self._extract_brand(phone_data.get('model_name', ''))

            return phone_data

        except Exception as e:
            print(f"  [✗] Error scraping {url}: {str(e)}")
            return None

        finally:
            time.sleep(2)  # Rate limiting

    def _parse_specs(self, specs_element):
        """Parse specifications table/section"""
        specs = {}

        # Try to find spec rows (adjust based on actual HTML)
        rows = specs_element.find_all('tr') or specs_element.find_all('div', class_='spec-row')

        for row in rows:
            # Extract label and value
            label_elem = row.find(['th', 'td', 'span'], class_=re.compile('label|name'))
            value_elem = row.find(['td', 'span'], class_=re.compile('value|spec'))

            if label_elem and value_elem:
                label = self._clean_text(label_elem.text).lower()
                value = self._clean_text(value_elem.text)

                # Map to our database fields
                if 'screen' in label or 'display' in label:
                    specs['screen'] = value
                    # Extract screen size
                    size_match = re.search(r'(\d+\.?\d*)\s*(?:inch|")', value)
                    if size_match:
                        specs['screen_size'] = float(size_match.group(1))

                elif 'processor' in label or 'chipset' in label:
                    specs['processor'] = value

                elif 'ram' in label or 'memory' in label:
                    specs['ram_options'] = value

                elif 'storage' in label or 'rom' in label:
                    specs['storage_options'] = value

                elif 'camera' in label:
                    if 'rear' in label or 'back' in label or 'main' in label:
                        specs['rear_camera'] = value
                        # Extract main camera MP
                        mp_match = re.search(r'(\d+)\s*mp', value, re.IGNORECASE)
                        if mp_match:
                            specs['rear_camera_main'] = int(mp_match.group(1))
                    elif 'front' in label or 'selfie' in label:
                        specs['front_camera'] = value
                        mp_match = re.search(r'(\d+)\s*mp', value, re.IGNORECASE)
                        if mp_match:
                            specs['front_camera_mp'] = int(mp_match.group(1))

                elif 'battery' in label:
                    specs['battery_info'] = value
                    # Extract mAh
                    mah_match = re.search(r'(\d+)\s*mah', value, re.IGNORECASE)
                    if mah_match:
                        specs['battery_capacity'] = int(mah_match.group(1))

                elif '5g' in label.lower() or 'network' in label:
                    specs['has_5g'] = '5g' in value.lower()

                elif 'os' in label or 'operating system' in label:
                    specs['operating_system'] = value

        return specs

    def _extract_brand(self, model_name):
        """Extract brand from model name"""
        if not model_name:
            return None

        brands = [
            'Samsung', 'Apple', 'iPhone', 'Xiaomi', 'Redmi', 'POCO',
            'Oppo', 'Vivo', 'Realme', 'Honor', 'Huawei', 'OnePlus',
            'Nokia', 'Motorola', 'Sony', 'Asus', 'Google', 'Pixel',
            'Nothing', 'Infinix', 'Tecno', 'Lenovo'
        ]

        model_upper = model_name.upper()

        for brand in brands:
            if brand.upper() in model_upper:
                if brand == 'iPhone':
                    return 'Apple'
                elif brand in ['Redmi', 'POCO']:
                    return 'Xiaomi'
                return brand

        # Try to get first word
        first_word = model_name.split()[0] if model_name.split() else None
        return first_word

    def _clean_text(self, text):
        """Clean and normalize text"""
        if not text:
            return ""
        return ' '.join(text.split()).strip()

    def save_to_database(self, phone_data):
        """Save scraped phone data to database"""
        with self.app.app_context():
            try:
                # Get or create brand
                brand_name = phone_data.get('brand')
                if not brand_name:
                    print(f"  [✗] No brand found for {phone_data.get('model_name')}")
                    return False

                brand = Brand.query.filter_by(name=brand_name).first()
                if not brand:
                    brand = Brand(
                        name=brand_name,
                        description=f"{brand_name} smartphones",
                        is_featured=brand_name in ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo']
                    )
                    db.session.add(brand)
                    db.session.flush()
                    print(f"  [+] Created brand: {brand_name}")

                # Check if phone exists
                model_name = phone_data.get('model_name')
                existing_phone = Phone.query.filter_by(model_name=model_name).first()

                if existing_phone:
                    print(f"  [•] Phone already exists: {model_name}")
                    return False

                # Create phone
                phone = Phone(
                    brand_id=brand.id,
                    model_name=model_name,
                    price=phone_data.get('price', 0),
                    availability_status='Available',
                    release_date=date.today()
                )
                db.session.add(phone)
                db.session.flush()

                # Create specifications
                specs_data = phone_data.get('specs', {})

                specs = PhoneSpecification(
                    phone_id=phone.id,
                    screen_size=specs_data.get('screen_size'),
                    screen_resolution=specs_data.get('screen_resolution'),
                    screen_type=specs_data.get('screen_type'),
                    processor=specs_data.get('processor'),
                    ram_options=specs_data.get('ram_options'),
                    storage_options=specs_data.get('storage_options'),
                    rear_camera=specs_data.get('rear_camera'),
                    rear_camera_main=specs_data.get('rear_camera_main'),
                    front_camera=specs_data.get('front_camera'),
                    front_camera_mp=specs_data.get('front_camera_mp'),
                    battery_capacity=specs_data.get('battery_capacity'),
                    has_5g=specs_data.get('has_5g', False),
                    operating_system=specs_data.get('operating_system')
                )
                db.session.add(specs)

                db.session.commit()
                print(f"  [✓] Added: {model_name} - RM {phone_data.get('price', 0):,.0f}")
                return True

            except Exception as e:
                db.session.rollback()
                print(f"  [✗] Error saving to database: {str(e)}")
                return False

    def scrape_all_phones(self, limit=30):
        """
        Main function to scrape phones from TechNave

        Args:
            limit: Maximum number of phones to scrape
        """
        print("=" * 60)
        print("TechNave Phone Scraper for DialSmart")
        print("=" * 60)

        # Get phone URLs
        phone_urls = self.scrape_phone_list()

        if not phone_urls:
            print("[ERROR] No phone URLs found. Check TechNave website structure.")
            return

        # Limit to specified number
        phone_urls = phone_urls[:limit]

        print(f"\n[INFO] Scraping {len(phone_urls)} phones...")

        success_count = 0
        failed_count = 0

        for i, url in enumerate(phone_urls, 1):
            print(f"\n[{i}/{len(phone_urls)}] Processing...")

            phone_data = self.scrape_phone_details(url)

            if phone_data and phone_data.get('model_name'):
                if self.save_to_database(phone_data):
                    success_count += 1
                else:
                    failed_count += 1
            else:
                failed_count += 1
                print(f"  [✗] Failed to extract data from {url}")

        print("\n" + "=" * 60)
        print(f"SCRAPING COMPLETE")
        print("=" * 60)
        print(f"  ✓ Successfully added: {success_count} phones")
        print(f"  ✗ Failed/Skipped: {failed_count} phones")
        print("=" * 60)


def main():
    """Main scraper execution"""
    import sys

    scraper = TechNaveScraper()

    if len(sys.argv) > 1:
        limit = int(sys.argv[1])
    else:
        limit = 30  # Default limit

    print(f"\nStarting TechNave scraper (limit: {limit} phones)...")
    print("This may take several minutes...\n")

    scraper.scrape_all_phones(limit=limit)


if __name__ == '__main__':
    main()
