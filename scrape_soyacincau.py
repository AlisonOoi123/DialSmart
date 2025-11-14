"""
SoyaCincau Web Scraper for Malaysian Phone Database
Scrapes phone data with MYR pricing from SoyaCincau
"""
import requests
from bs4 import BeautifulSoup
import time
import re
import json
from datetime import datetime
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

class SoyaCincauScraper:
    """
    Scraper for SoyaCincau Malaysia
    Website: https://www.soyacincau.com/
    """

    def __init__(self):
        self.base_url = "https://www.soyacincau.com"
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

    def scrape_phone_articles(self, max_phones=50):
        """
        Scrape phone information from SoyaCincau articles

        Args:
            max_phones: Maximum number of phones to scrape

        Returns:
            List of phone data dictionaries
        """
        print(f"\n[INFO] Scraping phone articles from SoyaCincau...")

        phones_data = []

        # SoyaCincau categories and search patterns
        search_terms = ['smartphones', 'phones', 'flagship', 'budget-phone',
                        'samsung', 'xiaomi', 'oppo', 'vivo', 'realme']

        for search_term in search_terms:
            if len(phones_data) >= max_phones:
                break

            try:
                print(f"\n[INFO] Searching for: {search_term}")

                # Try search or category pages
                url = f"{self.base_url}/?s={search_term}"

                response = self.session.get(url, timeout=15)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Find article links
                    articles = soup.find_all('article')
                    if not articles:
                        articles = soup.find_all(['div', 'section'], class_=re.compile(r'post|article|entry'))

                    print(f"[INFO] Found {len(articles)} articles for '{search_term}'")

                    for article in articles[:10]:  # Process up to 10 articles per search term
                        try:
                            # Find article link
                            link = article.find('a', href=re.compile(r'/\d{4}/\d{2}/'))
                            if link:
                                article_url = link.get('href')
                                if not article_url.startswith('http'):
                                    article_url = self.base_url + article_url

                                # Scrape individual article
                                phone_data = self._scrape_article(article_url)
                                if phone_data:
                                    phones_data.append(phone_data)
                                    print(f"  [+] Extracted: {phone_data.get('model_name', 'Unknown')}")

                                    if len(phones_data) >= max_phones:
                                        break

                                time.sleep(2)  # Rate limiting between articles

                        except Exception as e:
                            continue

                    time.sleep(3)  # Rate limiting between search terms

                else:
                    print(f"[WARN] Could not access search results (status {response.status_code})")

            except Exception as e:
                print(f"[ERROR] Failed to search '{search_term}': {str(e)}")
                continue

        print(f"\n[INFO] Total phones scraped: {len(phones_data)}")
        return phones_data

    def _scrape_article(self, url):
        """Scrape individual article for phone details"""
        try:
            response = self.session.get(url, timeout=15)
            if response.status_code != 200:
                return None

            soup = BeautifulSoup(response.content, 'html.parser')

            phone_data = {
                'url': url,
                'scraped_at': datetime.utcnow()
            }

            # Extract title (usually contains phone model)
            title = soup.find(['h1', 'h2'], class_=re.compile(r'title|entry'))
            if not title:
                title = soup.find('h1')

            if title:
                title_text = title.get_text(strip=True)
                phone_data['model_name'] = self._extract_model_name(title_text)
                phone_data['brand'] = self._extract_brand(title_text)
            else:
                return None

            # Extract article content
            content = soup.find(['div', 'article'], class_=re.compile(r'content|entry|article-body'))
            if not content:
                content = soup.find('article')

            if content:
                content_text = content.get_text()

                # Extract price (MYR patterns)
                price_patterns = [
                    r'RM\s*(\d+[,\d]*)',
                    r'priced?\s+at\s+RM\s*(\d+[,\d]*)',
                    r'costs?\s+RM\s*(\d+[,\d]*)',
                    r'retails?\s+at\s+RM\s*(\d+[,\d]*)'
                ]
                for pattern in price_patterns:
                    price_match = re.search(pattern, content_text, re.IGNORECASE)
                    if price_match:
                        price_str = price_match.group(1).replace(',', '')
                        phone_data['price'] = float(price_str)
                        break

                # Extract specs
                # Screen size
                screen_match = re.search(r'(\d+\.?\d*)["\s-]*inch', content_text, re.IGNORECASE)
                if screen_match:
                    phone_data['screen_size'] = float(screen_match.group(1))

                # RAM
                ram_match = re.search(r'(\d+)\s*GB\s+(?:of\s+)?RAM', content_text, re.IGNORECASE)
                if ram_match:
                    phone_data['ram'] = f"{ram_match.group(1)}GB"

                # Storage
                storage_match = re.search(r'(\d+)\s*GB\s+(?:of\s+)?(?:storage|internal)', content_text, re.IGNORECASE)
                if storage_match:
                    phone_data['storage'] = f"{storage_match.group(1)}GB"

                # Camera (main sensor)
                camera_patterns = [
                    r'(\d+)\s*MP\s+(?:main|primary|rear)',
                    r'(?:main|primary)\s+(\d+)\s*MP',
                ]
                for pattern in camera_patterns:
                    camera_match = re.search(pattern, content_text, re.IGNORECASE)
                    if camera_match:
                        phone_data['camera'] = int(camera_match.group(1))
                        break

                # Battery
                battery_match = re.search(r'(\d+)\s*mAh', content_text, re.IGNORECASE)
                if battery_match:
                    phone_data['battery'] = int(battery_match.group(1))

                # Processor
                processor_patterns = [
                    r'(Snapdragon\s+\d+[^\s,\.]*)',
                    r'(MediaTek\s+\w+\s+\d+[^\s,\.]*)',
                    r'(Exynos\s+\d+[^\s,\.]*)',
                    r'(Apple\s+A\d+[^\s,\.]*)',
                ]
                for pattern in processor_patterns:
                    proc_match = re.search(pattern, content_text, re.IGNORECASE)
                    if proc_match:
                        phone_data['processor'] = proc_match.group(1)
                        break

                # 5G
                phone_data['has_5g'] = bool(re.search(r'\b5G\b', content_text))

            return phone_data if phone_data.get('model_name') else None

        except Exception as e:
            return None

    def _extract_model_name(self, text):
        """Extract phone model name from title"""
        # Remove common prefixes
        text = re.sub(r'(?:now|official|announced|launched|available|review|hands-on|first look)[:|-]?\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s+in\s+Malaysia.*', '', text, flags=re.IGNORECASE)

        # Keep only the phone model part
        model = text.strip()
        if len(model) > 80:
            model = model[:80]

        return model

    def _extract_brand(self, text):
        """Extract brand from title"""
        brands = ['Samsung', 'Apple', 'Xiaomi', 'Oppo', 'Vivo', 'Realme',
                  'Honor', 'OnePlus', 'Huawei', 'Nokia', 'Motorola', 'ASUS',
                  'Sony', 'Google', 'Nothing', 'Infinix', 'Tecno']

        for brand in brands:
            if brand.lower() in text.lower():
                return brand

        return 'Unknown'

    def save_to_database(self, phones_data):
        """Save scraped phone data to database"""
        with self.app.app_context():
            saved_count = 0
            skipped_count = 0

            for phone_data in phones_data:
                try:
                    # Get or create brand
                    brand_name = phone_data.get('brand', 'Unknown')
                    if brand_name == 'Unknown':
                        continue

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
                        storage_options=phone_data.get('storage', '128GB'),
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
    limit = 30
    if len(sys.argv) > 1:
        try:
            limit = int(sys.argv[1])
        except ValueError:
            print("Invalid limit. Using default: 30")

    print(f"\nStarting SoyaCincau scraper (limit: {limit} phones)...")
    print("This may take several minutes...\n")

    print("="*60)
    print("SoyaCincau Phone Scraper for DialSmart")
    print("="*60)

    scraper = SoyaCincauScraper()

    # Scrape phones
    phones_data = scraper.scrape_phone_articles(max_phones=limit)

    if phones_data:
        print(f"\n[INFO] Scraped {len(phones_data)} phones successfully")
        print("[INFO] Saving to database...")
        scraper.save_to_database(phones_data)
    else:
        print("\n[ERROR] No phone data collected. Check website structure or network connection.")


if __name__ == "__main__":
    main()
