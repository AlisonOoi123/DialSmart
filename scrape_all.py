"""
Master Scraper - Run all Malaysian phone scrapers
Collects data from Lowyat, SoyaCincau, and Amanz
"""
import sys
import time
from datetime import datetime

def run_scraper(scraper_name, limit):
    """Run a specific scraper"""
    print(f"\n{'='*70}")
    print(f"Running {scraper_name} Scraper")
    print(f"{'='*70}\n")

    try:
        if scraper_name == "Lowyat":
            from scrape_lowyat import LowyatScraper
            scraper = LowyatScraper()
            phones_data = scraper.scrape_phone_specs(max_phones=limit)
            if phones_data:
                scraper.save_to_database(phones_data)
            return len(phones_data)

        elif scraper_name == "SoyaCincau":
            from scrape_soyacincau import SoyaCincauScraper
            scraper = SoyaCincauScraper()
            phones_data = scraper.scrape_phone_articles(max_phones=limit)
            if phones_data:
                scraper.save_to_database(phones_data)
            return len(phones_data)

        elif scraper_name == "Amanz":
            from scrape_amanz import AmanzScraper
            scraper = AmanzScraper()
            phones_data = scraper.scrape_phone_articles(max_phones=limit)
            if phones_data:
                scraper.save_to_database(phones_data)
            return len(phones_data)

    except Exception as e:
        print(f"\n[ERROR] {scraper_name} scraper failed: {str(e)}")
        return 0


def main():
    """Run all scrapers in sequence"""

    # Default limits for each scraper
    lowyat_limit = 50
    soyacincau_limit = 30
    amanz_limit = 30

    # Parse command line arguments
    if len(sys.argv) > 1:
        try:
            total_limit = int(sys.argv[1])
            # Distribute limit across scrapers
            lowyat_limit = int(total_limit * 0.5)  # 50% from Lowyat
            soyacincau_limit = int(total_limit * 0.25)  # 25% from SoyaCincau
            amanz_limit = int(total_limit * 0.25)  # 25% from Amanz
        except ValueError:
            print("Invalid limit. Using defaults.")

    print("\n" + "="*70)
    print("DialSmart - Master Phone Scraper")
    print("Collecting data from multiple Malaysian tech websites")
    print("="*70)
    print(f"\nTarget collection:")
    print(f"  • Lowyat.NET: {lowyat_limit} phones")
    print(f"  • SoyaCincau: {soyacincau_limit} phones")
    print(f"  • Amanz: {amanz_limit} phones")
    print(f"  • Total target: {lowyat_limit + soyacincau_limit + amanz_limit} phones")
    print("\nThis will take several minutes. Please be patient...")

    start_time = datetime.now()
    results = {}

    # Run each scraper
    scrapers = [
        ("Lowyat", lowyat_limit),
        ("SoyaCincau", soyacincau_limit),
        ("Amanz", amanz_limit)
    ]

    for scraper_name, limit in scrapers:
        try:
            count = run_scraper(scraper_name, limit)
            results[scraper_name] = count

            # Wait between scrapers to be polite
            if scraper_name != scrapers[-1][0]:  # Don't wait after last scraper
                print(f"\n[INFO] Waiting 5 seconds before next scraper...")
                time.sleep(5)

        except KeyboardInterrupt:
            print(f"\n\n[WARN] Scraping interrupted by user")
            break
        except Exception as e:
            print(f"\n[ERROR] Failed to run {scraper_name}: {str(e)}")
            results[scraper_name] = 0
            continue

    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"\nScraping completed in {duration:.1f} seconds ({duration/60:.1f} minutes)")
    print("\nResults by source:")

    total_collected = 0
    for scraper_name, count in results.items():
        total_collected += count
        print(f"  • {scraper_name}: {count} phones")

    print(f"\n{'='*70}")
    print(f"TOTAL PHONES COLLECTED: {total_collected}")
    print(f"{'='*70}\n")

    if total_collected > 0:
        print("✓ Success! Your database has been populated with Malaysian phone data.")
        print("\nNext steps:")
        print("  1. Run your application: python run.py")
        print("  2. Login and test recommendations")
        print("  3. Try the AI chatbot with different queries")
    else:
        print("⚠ No phones were collected. Possible issues:")
        print("  • Network connection problems")
        print("  • Websites blocking scrapers")
        print("  • Website structure has changed")
        print("\nFallback option: Run 'python init_database.py' to use the built-in dataset")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Scraping stopped by user")
        sys.exit(0)
