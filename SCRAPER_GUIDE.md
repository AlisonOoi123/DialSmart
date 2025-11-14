# Malaysian Phone Data Scrapers Guide

This guide explains how to use the web scrapers to collect phone data from Malaysian tech websites.

## Available Scrapers

DialSmart includes scrapers for three major Malaysian tech websites:

1. **Lowyat.NET** (`scrape_lowyat.py`)
   - Malaysia's largest tech community
   - Comprehensive phone database
   - MYR pricing
   - Best for: Large volume of phones across all brands

2. **SoyaCincau** (`scrape_soyacincau.py`)
   - Popular Malaysian tech news site
   - Phone reviews with detailed specs
   - MYR pricing
   - Best for: Latest phone launches and reviews

3. **Amanz** (`scrape_amanz.py`)
   - Malaysian tech news portal (Malay + English)
   - Phone news and reviews
   - MYR pricing
   - Best for: Local market coverage

## Quick Start

### Option 1: Run All Scrapers at Once (Recommended)

Collect data from all three sources automatically:

```bash
# Collect 100 total phones (distributed across all scrapers)
python scrape_all.py 100

# Collect 200 phones
python scrape_all.py 200

# Use default limits (110 phones: 50 from Lowyat, 30 from SoyaCincau, 30 from Amanz)
python scrape_all.py
```

### Option 2: Run Individual Scrapers

Run each scraper separately for more control:

#### Lowyat Scraper
```bash
# Scrape 50 phones from Lowyat
python scrape_lowyat.py 50

# Scrape 100 phones
python scrape_lowyat.py 100
```

#### SoyaCincau Scraper
```bash
# Scrape 30 phones from SoyaCincau
python scrape_soyacincau.py 30

# Scrape 50 phones
python scrape_soyacincau.py 50
```

#### Amanz Scraper
```bash
# Scrape 30 phones from Amanz
python scrape_amanz.py 30

# Scrape 50 phones
python scrape_amanz.py 50
```

## How the Scrapers Work

### Data Extraction

Each scraper extracts the following information:

- **Model Name**: Phone model (e.g., "Samsung Galaxy S24 Ultra")
- **Brand**: Manufacturer (Samsung, Apple, Xiaomi, etc.)
- **Price**: In Malaysian Ringgit (RM)
- **Screen Size**: Display size in inches
- **Processor**: CPU/Chipset (Snapdragon, MediaTek, etc.)
- **RAM**: Memory options (e.g., "8GB", "12GB")
- **Storage**: Internal storage (e.g., "128GB", "256GB")
- **Camera**: Main rear camera megapixels
- **Battery**: Battery capacity in mAh
- **5G Support**: Whether the phone supports 5G networks

### Duplicate Prevention

- Scrapers automatically check for existing phones in the database
- Duplicate phones (same brand + model name) are skipped
- Only new phones are added to the database

### Rate Limiting

Scrapers are designed to be respectful:

- 2-3 second delays between requests
- Session warmup before scraping
- Proper browser headers to avoid blocking

## Expected Output

When running a scraper, you'll see:

```
============================================================
Lowyat.NET Phone Scraper for DialSmart
============================================================

[INFO] Scraping SAMSUNG phones...
[INFO] Found 25 Samsung phone entries
  [+] Created brand: Samsung
  [✓] Added: Samsung Galaxy S24 Ultra - RM 5,999.00
  [✓] Added: Samsung Galaxy S24+ - RM 4,699.00
  ...

[INFO] Scraping XIAOMI phones...
  [✓] Added: Xiaomi 14 Pro - RM 3,299.00
  ...

============================================================
Scraping Summary:
  • Total scraped: 50
  • Successfully saved: 45
  • Skipped (duplicates): 5
============================================================
```

## Troubleshooting

### No phones collected

**Problem**: Scraper runs but finds 0 phones

**Solutions**:
1. Check your internet connection
2. Website may be blocking scrapers (403 Forbidden)
3. Website structure may have changed
4. Try a different scraper
5. Fallback: Use `python init_database.py` for built-in dataset

### 403 Forbidden errors

**Problem**: Website blocks the scraper

**Solutions**:
1. Wait a few minutes and try again (you may have been rate-limited)
2. Try a different scraper
3. Use the built-in dataset instead

### Incomplete data

**Problem**: Phones saved but missing some specs

**Explanation**: This is normal! Not all articles contain complete specifications. The scrapers extract whatever information is available.

**Solution**: You can manually complete the data via the Admin Panel after scraping.

## Best Practices

### For Maximum Data Collection

1. **Start with `scrape_all.py`** - Collects from all sources at once
   ```bash
   python scrape_all.py 150
   ```

2. **Run scrapers at different times** - If one source is blocking, try others
   ```bash
   python scrape_lowyat.py 50
   # Wait 30 minutes
   python scrape_soyacincau.py 30
   ```

3. **Don't scrape too aggressively** - Use reasonable limits (50-100 phones per run)

4. **Check what you have first**
   ```bash
   # Login as admin and check Admin Dashboard > Phones
   # This shows how many phones are already in the database
   ```

### For Regular Updates

Run scrapers periodically to get new phones:

```bash
# Weekly update - collect latest 20 phones from each source
python scrape_lowyat.py 20
python scrape_soyacincau.py 20
python scrape_amanz.py 20
```

## Alternative: Use Built-in Dataset

If web scraping doesn't work, use the comprehensive built-in dataset:

```bash
python init_database.py
```

This provides:
- 30+ phones covering all major brands
- Complete specifications
- MYR pricing (RM 799 - RM 6,299)
- Ready-to-use test data

## Verifying Your Data

After scraping, verify your database:

1. **Run the application**:
   ```bash
   python run.py
   ```

2. **Login as admin**:
   - Email: admin@dialsmart.my
   - Password: admin123

3. **Check the database**:
   - Go to Admin Dashboard
   - Click "Phones" to see all phones
   - Verify brands, models, and prices

4. **Test recommendations**:
   - Logout and login as user (user@dialsmart.my / user123)
   - Try the recommendation wizard
   - Test the chatbot

## Support

If you encounter issues:

1. Check this guide first
2. Verify your internet connection
3. Try the built-in dataset (`python init_database.py`)
4. Check if websites are accessible in your browser
5. Look at the error messages for clues

## Technical Details

### Dependencies

All scrapers use:
- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `html.parser` - Built-in Python parser (no C++ compiler needed)

### Scraper Architecture

Each scraper:
1. Creates a session with browser headers
2. Fetches phone listings or articles
3. Extracts phone data using regex and CSS selectors
4. Parses Malaysian pricing (RM format)
5. Creates brands automatically
6. Saves phones and specifications to database
7. Prevents duplicates

### Rate Limiting

- Lowyat: 2 seconds between requests
- SoyaCincau: 2 seconds between articles, 3 seconds between searches
- Amanz: 2 seconds between articles, 3 seconds between categories
- Master script: 5 seconds between different scrapers

## Summary

**Quick commands**:

```bash
# Best option - run all scrapers
python scrape_all.py 100

# Individual scrapers
python scrape_lowyat.py 50
python scrape_soyacincau.py 30
python scrape_amanz.py 30

# Fallback - built-in dataset
python init_database.py

# Run your app
python run.py
```

Good luck with your data collection! 🚀
