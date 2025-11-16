# DialSmart Setup Guide - Malaysian Phone Data

This guide will help you set up DialSmart with a comprehensive Malaysian smartphone database with MYR pricing.

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database with Malaysian Phone Data

Run the comprehensive database initialization script:

```bash
python init_database.py
```

This will:
- ✅ Create all database tables
- ✅ Add 10 smartphone brands (Samsung, Apple, Xiaomi, Oppo, Vivo, Realme, Honor, OnePlus, etc.)
- ✅ Add 30+ popular Malaysian smartphones with MYR pricing
- ✅ Create test user accounts
- ✅ Set up sample user preferences

**Included Phones (MYR Pricing):**

**Budget Phones (Under RM1000):**
- Samsung Galaxy A15 5G - RM 799
- Oppo A79 5G - RM 999
- Realme C67 5G - RM 799

**Mid-Range (RM1000-2000):**
- Samsung Galaxy A35 5G - RM 1,499
- Samsung Galaxy A55 5G - RM 1,899
- Xiaomi Redmi Note 13 Pro 5G - RM 1,299
- Xiaomi Redmi Note 13 Pro+ 5G - RM 1,699
- Oppo Reno 11 5G - RM 1,899
- Vivo Y100 5G - RM 1,499
- Honor X9b 5G - RM 1,299
- Honor 90 5G - RM 1,799
- Realme 12 Pro+ 5G - RM 1,799
- OnePlus Nord CE 3 - RM 1,299

**Upper Mid-Range (RM2000-3000):**
- Samsung Galaxy S23 FE - RM 2,699
- Xiaomi 13T Pro - RM 2,699
- Vivo V30 5G - RM 2,099
- Realme GT 5 Pro - RM 3,299

**Premium & Flagship (RM3000+):**
- Samsung Galaxy S24 Ultra - RM 5,999
- iPhone 15 Pro Max - RM 6,299
- iPhone 15 Pro - RM 5,499
- iPhone 15 - RM 4,399
- iPhone 14 - RM 3,699
- Xiaomi 14 - RM 3,999
- Oppo Find X7 Ultra - RM 4,999
- Vivo X100 Pro - RM 4,699
- Honor Magic6 Pro - RM 4,599
- OnePlus 12 - RM 4,299

### 3. Run the Application

```bash
python run.py
```

Visit: **http://localhost:5000**

### 4. Login Credentials

**Regular User:**
- Email: `user@dialsmart.my`
- Password: `password123`

**Admin User:**
- Email: `admin@dialsmart.my`
- Password: `admin123`

---

## Automatic Price Updates

### Price Update System

The system includes a phone data updater that can automatically update prices from Malaysian retailers.

### Manual Price Updates

Update prices for all phones:
```bash
python phone_data_updater.py prices
```

Check for new phone launches:
```bash
python phone_data_updater.py new
```

Generate price analysis report:
```bash
python phone_data_updater.py report
```

Update specific phone manually:
```bash
python phone_data_updater.py manual "iPhone 15 Pro" 5299.00
```

### Automatic Scheduled Updates

To run automatic updates in the background:

```bash
python scheduler.py
```

This will:
- Update prices every 6 hours
- Check for new phones daily at 9:00 AM
- Generate price reports daily at 6:00 PM

**Running as Background Service (Linux/Mac):**
```bash
nohup python scheduler.py > scheduler.log 2>&1 &
```

**Running as Background Service (Windows):**
Use Task Scheduler or run in a separate PowerShell window.

---

## Integrating Real Malaysian Data Sources

The updater is designed to work with Malaysian e-commerce and tech sites. To enable automatic updates:

### 1. E-Commerce Integration

Edit `phone_data_updater.py` and implement the `_fetch_latest_price()` function:

**Suggested Data Sources:**
- **Lazada Malaysia** - https://www.lazada.com.my/
- **Shopee Malaysia** - https://shopee.com.my/
- **PriceSpy Malaysia** - https://pricespy.com.my/

### 2. Tech News Integration

Implement `_fetch_new_launches()` to scrape:
- **SoyaCincau** - https://www.soyacincau.com/
- **Lowyat.NET** - https://www.lowyat.net/
- **Amanz** - https://amanz.my/
- **GSMArena Malaysia** - https://www.gsmarena.com/

### 3. Install Web Scraping Dependencies

Uncomment in `requirements.txt`:
```bash
pip install requests beautifulsoup4 lxml
```

### 4. Example Implementation

```python
def _fetch_latest_price(self, phone):
    """Fetch from Lazada Malaysia"""
    import requests
    from bs4 import BeautifulSoup

    search_url = f"https://www.lazada.com.my/catalog/?q={phone.model_name}"

    try:
        response = requests.get(search_url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract price (adjust selectors based on actual HTML)
        price_element = soup.find('span', class_='price')
        if price_element:
            price_text = price_element.text.strip()
            # Parse "RM 1,299.00" -> 1299.00
            price = float(price_text.replace('RM', '').replace(',', ''))
            return price

    except Exception as e:
        logger.error(f"Error fetching price: {e}")

    return None
```

---

## Database Statistics

After initialization, you can check database statistics:

```python
python phone_data_updater.py report
```

**Sample Output:**
```
Average Price by Brand (MYR):
-----------------------------------------------------
Samsung        | Avg: RM   2,259 | Range: RM    799 - RM  5,999 | Models: 5
Apple          | Avg: RM   5,199 | Range: RM  3,699 - RM  6,299 | Models: 4
Xiaomi         | Avg: RM   2,399 | Range: RM  1,299 - RM  3,999 | Models: 4
Oppo           | Avg: RM   2,632 | Range: RM    999 - RM  4,999 | Models: 3
Vivo           | Avg: RM   2,732 | Range: RM  1,499 - RM  4,699 | Models: 3

Price Segments:
-----------------------------------------------------
Budget (Under RM1000)          |   3 phones
Mid-Range (RM1000-2000)        |  11 phones
Upper Mid (RM2000-3000)        |   4 phones
Premium (RM3000-4500)          |   7 phones
Flagship (Above RM4500)        |   5 phones
```

---

## Troubleshooting

### Database Already Exists

If you run `init_database.py` again, it will:
- Skip existing brands
- Skip existing phones
- Skip existing users
- Only add new data

### Reset Database

To start fresh:
```bash
# Delete the database file
rm dialsmart.db

# Re-initialize
python init_database.py
```

### Price Update Errors

Check `scheduler.log` for error messages:
```bash
tail -f scheduler.log
```

---

## Production Recommendations

For production deployment:

1. **Use PostgreSQL Instead of SQLite:**
   ```python
   # In config.py
   SQLALCHEMY_DATABASE_URI = 'postgresql://user:pass@localhost/dialsmart'
   ```

2. **Set up Proper Web Scraping:**
   - Use official retailer APIs where available
   - Implement rate limiting
   - Add user-agent rotation
   - Handle CAPTCHA challenges

3. **Use Task Queue for Updates:**
   ```bash
   pip install celery redis
   ```

4. **Monitor Price Changes:**
   - Set up alerts for significant price drops
   - Track price history
   - Notify users of deals

5. **Comply with Terms of Service:**
   - Respect robots.txt
   - Follow rate limits
   - Consider using official APIs

---

## Support

For issues with Malaysian phone data:
- Check SoyaCincau for latest launches
- Verify prices on Lazada/Shopee
- Contact: support@dialsmart.my

---

**Last Updated:** 2024
**Data Coverage:** 30+ smartphones from 10 brands
**Price Currency:** Malaysian Ringgit (MYR)
