"""
CSV Dataset Importer for DialSmart
Imports phone data from fyp_phoneDataset.csv
"""
import csv
import re
from datetime import datetime
from app import create_app, db
from app.models import Brand, Phone, PhoneSpecification

class CSVDatasetImporter:
    """Import phone data from CSV file"""

    def __init__(self, csv_file_path='fyp_phoneDataset.csv'):
        self.csv_file_path = csv_file_path
        self.app = create_app()

    def parse_price(self, price_str):
        """Extract numeric price from string like 'MYR 741'"""
        if not price_str or price_str.strip() == '':
            return 0.0

        # Remove currency symbols and extract number
        price_match = re.search(r'(\d+[,\d]*\.?\d*)', str(price_str).replace(',', ''))
        if price_match:
            return float(price_match.group(1))
        return 0.0

    def parse_screen_size(self, screen_str):
        """Extract screen size in inches"""
        if not screen_str:
            return None

        # Look for patterns like "6.78 inches"
        match = re.search(r'(\d+\.?\d*)\s*inch', str(screen_str), re.IGNORECASE)
        if match:
            return float(match.group(1))
        return None

    def parse_battery_capacity(self, battery_str):
        """Extract battery capacity in mAh"""
        if not battery_str:
            return None

        # Look for patterns like "5500 mAh"
        match = re.search(r'(\d+)\s*mAh', str(battery_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def parse_camera_mp(self, camera_str):
        """Extract main camera megapixels"""
        if not camera_str:
            return None

        # Look for first MP value (usually the main camera)
        match = re.search(r'(\d+)\s*MP', str(camera_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def parse_ppi(self, ppi_str):
        """Extract PPI value"""
        if not ppi_str:
            return None

        match = re.search(r'(\d+)\s*ppi', str(ppi_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None

    def parse_refresh_rate(self, display_str):
        """Extract refresh rate from display string"""
        if not display_str:
            return 60  # Default

        match = re.search(r'(\d+)\s*Hz', str(display_str), re.IGNORECASE)
        if match:
            return int(match.group(1))
        return 60

    def check_5g(self, technology_str, network_5g_str):
        """Check if phone supports 5G"""
        if technology_str and '5g' in str(technology_str).lower():
            return True
        if network_5g_str and str(network_5g_str).strip() and str(network_5g_str).strip() != '':
            return True
        return False

    def check_nfc(self, nfc_str):
        """Check if phone has NFC"""
        if not nfc_str:
            return False
        nfc_lower = str(nfc_str).lower().strip()
        return nfc_lower == 'yes' or nfc_lower == 'true'

    def parse_release_date(self, date_str):
        """Parse release date"""
        if not date_str or str(date_str).strip() == '':
            return None

        try:
            # Try to parse "Released 2025, April" format
            match = re.search(r'(\d{4})', str(date_str))
            if match:
                year = int(match.group(1))
                # Use January 1st as default if only year is provided
                return datetime(year, 1, 1).date()
        except:
            pass

        return None

    def import_csv(self):
        """Import all phones from CSV file"""
        with self.app.app_context():
            try:
                print("\n" + "="*70)
                print("DialSmart CSV Dataset Importer")
                print("="*70)
                print(f"\nReading CSV file: {self.csv_file_path}")

                # Read CSV file with UTF-8-sig encoding to handle BOM
                with open(self.csv_file_path, 'r', encoding='utf-8-sig') as csvfile:
                    reader = csv.DictReader(csvfile)

                    # Clean up fieldnames (remove BOM and whitespace)
                    if reader.fieldnames:
                        reader.fieldnames = [name.strip() for name in reader.fieldnames if name and name.strip()]

                    phones_data = list(reader)
                    total_phones = len(phones_data)

                    print(f"Found {total_phones} phones in CSV file\n")
                    print("Starting import...\n")

                    imported_count = 0
                    skipped_count = 0
                    error_count = 0

                    for idx, row in enumerate(phones_data, 1):
                        try:
                            # Get or create brand
                            brand_name = row.get('Brand', '').strip()
                            if not brand_name:
                                print(f"  [{idx}/{total_phones}] ✗ Skipped: No brand name")
                                skipped_count += 1
                                continue

                            brand = Brand.query.filter_by(name=brand_name).first()
                            if not brand:
                                brand = Brand(
                                    name=brand_name,
                                    description=f"{brand_name} smartphones",
                                    is_active=True,
                                    is_featured=brand_name.lower() in ['samsung', 'apple', 'xiaomi']
                                )
                                db.session.add(brand)
                                db.session.flush()
                                print(f"  [+] Created brand: {brand_name}")

                            # Get model name
                            model_name = row.get('Model', '').strip()
                            if not model_name:
                                print(f"  [{idx}/{total_phones}] ✗ Skipped: No model name")
                                skipped_count += 1
                                continue

                            # Check if phone already exists
                            existing_phone = Phone.query.filter_by(
                                brand_id=brand.id,
                                model_name=model_name
                            ).first()

                            if existing_phone:
                                print(f"  [{idx}/{total_phones}] ⊘ Skipped (duplicate): {model_name}")
                                skipped_count += 1
                                continue

                            # Parse price
                            price = self.parse_price(row.get('Price', '0'))

                            # Create phone
                            phone = Phone(
                                brand_id=brand.id,
                                model_name=model_name,
                                price=price,
                                main_image=row.get('Image URL', '').strip(),
                                availability_status=row.get('Status', 'Available').strip(),
                                release_date=self.parse_release_date(row.get('Release Date', '')),
                                is_active=True
                            )
                            db.session.add(phone)
                            db.session.flush()

                            # Create specifications
                            specs = PhoneSpecification(
                                phone_id=phone.id,

                                # Display
                                screen_size=self.parse_screen_size(row.get('Screen Size', '')),
                                screen_type=row.get('Type', '').strip(),
                                display_type=row.get('Display Type', '').strip(),
                                screen_resolution=row.get('Resolution', '').strip(),
                                refresh_rate=self.parse_refresh_rate(row.get('Display Type', '')),
                                ppi=self.parse_ppi(row.get('PPI', '')),
                                multitouch=row.get('Multi-touch', '').strip(),
                                protection=row.get('Protection', '').strip(),

                                # Performance
                                chipset=row.get('Chipset', '').strip(),
                                processor=row.get('Chipset', '').strip(),  # Use chipset as processor
                                cpu=row.get('CPU', '').strip(),
                                gpu=row.get('GPU', '').strip(),
                                ram_options=row.get('RAM', '').strip(),
                                storage_options=row.get('Storage', '').strip(),
                                card_slot=row.get('Card Slot', '').strip(),
                                expandable_storage='microSD' in str(row.get('Card Slot', '')),

                                # Camera
                                rear_camera=row.get('Rear Camera', '').strip(),
                                rear_camera_main=self.parse_camera_mp(row.get('Rear Camera', '')),
                                front_camera=row.get('Front Camera', '').strip(),
                                front_camera_mp=self.parse_camera_mp(row.get('Front Camera', '')),
                                flash=row.get('Flash', '').strip(),
                                camera_features=row.get('Camera Features', '').strip(),
                                video_recording=row.get('Video Recording', '').strip(),

                                # Battery
                                battery=row.get('Battery', '').strip(),
                                battery_capacity=self.parse_battery_capacity(row.get('Battery Capacity', '')),
                                fast_charging=row.get('Fast Charging', '').strip(),
                                charging_speed=row.get('Fast Charging', '').strip(),
                                wireless_charging=row.get('Wireless Charging', '').strip(),
                                removable_battery=row.get('Removable Battery', '').strip(),

                                # Network
                                sim=row.get('SIM', '').strip(),
                                technology=row.get('Technology', '').strip(),
                                network_5g=row.get('5G Networks', '').strip(),
                                network_4g=row.get('4G Networks', '').strip(),
                                network_3g=row.get('3G Networks', '').strip(),
                                network_2g=row.get('2G Networks', '').strip(),
                                network_speed=row.get('Network Speed', '').strip(),
                                has_5g=self.check_5g(row.get('Technology', ''), row.get('5G Networks', '')),

                                # Connectivity
                                wifi_standard=row.get('Wi-Fi', '').strip(),
                                bluetooth_version=row.get('Bluetooth', '').strip(),
                                gps=row.get('GPS', '').strip(),
                                nfc=row.get('NFC', '').strip(),
                                usb=row.get('USB', '').strip(),
                                audio_jack=row.get('Audio Jack', '').strip(),
                                radio=row.get('Radio', '').strip(),

                                # OS
                                operating_system=row.get('OS', '').strip(),

                                # Physical
                                dimensions=row.get('Dimensions', '').strip(),
                                weight=row.get('Weight', '').strip(),
                                colors_available=row.get('Color', '').strip(),
                                body_material=row.get('Body Material', '').strip(),

                                # Features
                                sensors=row.get('Sensors', '').strip(),
                                dual_sim='Dual' in str(row.get('SIM', '')),

                                # Reference
                                product_url=row.get('URL', '').strip()
                            )
                            db.session.add(specs)
                            db.session.commit()

                            imported_count += 1
                            price_display = f"RM {phone.price:,.2f}" if phone.price > 0 else "Price N/A"
                            print(f"  [{idx}/{total_phones}] ✓ Imported: {brand_name} {model_name} - {price_display}")

                        except Exception as e:
                            db.session.rollback()
                            error_count += 1
                            print(f"  [{idx}/{total_phones}] ✗ Error: {row.get('Model', 'Unknown')} - {str(e)}")
                            continue

                # Final summary
                print("\n" + "="*70)
                print("Import Summary")
                print("="*70)
                print(f"Total phones in CSV: {total_phones}")
                print(f"Successfully imported: {imported_count}")
                print(f"Skipped (duplicates): {skipped_count}")
                print(f"Errors: {error_count}")
                print("="*70 + "\n")

                if imported_count > 0:
                    print("✓ Success! Your database has been populated with the CSV dataset.")
                    print("\nNext steps:")
                    print("  1. Run your application: python run.py")
                    print("  2. Login as admin to verify phones: admin@dialsmart.my / admin123")
                    print("  3. Test AI recommendations with the new data")
                else:
                    print("⚠ No phones were imported. Check the CSV file path and format.")

            except FileNotFoundError:
                print(f"\n✗ Error: CSV file not found at '{self.csv_file_path}'")
                print("\nPlease ensure:")
                print("  1. The CSV file 'fyp_phoneDataset.csv' is in the project root directory")
                print("  2. The file path is correct")
            except Exception as e:
                print(f"\n✗ Error during import: {str(e)}")
                import traceback
                traceback.print_exc()


def main():
    import sys

    # Get CSV file path from command line or use default
    csv_file = 'fyp_phoneDataset.csv'
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]

    print(f"\nStarting CSV import from: {csv_file}\n")

    importer = CSVDatasetImporter(csv_file)
    importer.import_csv()


if __name__ == "__main__":
    main()
