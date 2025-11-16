"""
Automatic Price Update Scheduler
Runs periodic updates for phone prices and new launches
"""
import schedule
import time
from datetime import datetime
from phone_data_updater import PhoneDataUpdater
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def run_price_update():
    """Run price update task"""
    logger.info("Starting scheduled price update...")
    try:
        updater = PhoneDataUpdater()
        updater.update_all_prices()
        logger.info("Price update completed successfully")
    except Exception as e:
        logger.error(f"Price update failed: {str(e)}")


def check_new_phones():
    """Check for new phone launches"""
    logger.info("Checking for new phone launches...")
    try:
        updater = PhoneDataUpdater()
        updater.check_new_launches()
        logger.info("New phone check completed")
    except Exception as e:
        logger.error(f"New phone check failed: {str(e)}")


def generate_daily_report():
    """Generate daily price report"""
    logger.info("Generating daily price report...")
    try:
        updater = PhoneDataUpdater()
        updater.generate_price_report()
        logger.info("Daily report generated")
    except Exception as e:
        logger.error(f"Report generation failed: {str(e)}")


def main():
    """Main scheduler function"""
    logger.info("=" * 60)
    logger.info("DialSmart Automatic Update Scheduler Started")
    logger.info("=" * 60)

    # Schedule tasks

    # Update prices every 6 hours
    schedule.every(6).hours.do(run_price_update)

    # Check for new phones daily at 9 AM
    schedule.every().day.at("09:00").do(check_new_phones)

    # Generate report daily at 6 PM
    schedule.every().day.at("18:00").do(generate_daily_report)

    # Run initial updates
    logger.info("Running initial updates...")
    run_price_update()
    check_new_phones()

    logger.info("\nScheduled tasks:")
    logger.info("  • Price updates: Every 6 hours")
    logger.info("  • New phone check: Daily at 9:00 AM")
    logger.info("  • Price report: Daily at 6:00 PM")
    logger.info("\nPress Ctrl+C to stop the scheduler\n")

    # Keep the scheduler running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        logger.info("\nScheduler stopped by user")


if __name__ == '__main__':
    main()
