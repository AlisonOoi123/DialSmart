"""
Phone Comparison Module
Handles side-by-side phone comparisons
"""
from app import db
from app.models import Phone, PhoneSpecification, Comparison

class PhoneComparison:
    """Phone comparison functionality"""

    def __init__(self):
        self.comparison_categories = [
            'price',
            'display',
            'performance',
            'camera',
            'battery',
            'connectivity',
            'features'
        ]

    def compare_phones(self, phone1_id, phone2_id, user_id=None):
        """
        Compare two phones side-by-side

        Args:
            phone1_id: ID of first phone
            phone2_id: ID of second phone
            user_id: Optional user ID to save comparison

        Returns:
            Dictionary with comparison data
        """
        phone1 = Phone.query.get(phone1_id)
        phone2 = Phone.query.get(phone2_id)

        if not phone1 or not phone2:
            return None

        specs1 = PhoneSpecification.query.filter_by(phone_id=phone1_id).first()
        specs2 = PhoneSpecification.query.filter_by(phone_id=phone2_id).first()

        # Build comparison data
        comparison_data = {
            'phone1': {
                'info': phone1,
                'specs': specs1
            },
            'phone2': {
                'info': phone2,
                'specs': specs2
            },
            'comparison': self._build_comparison_table(phone1, specs1, phone2, specs2),
            'winner': self._determine_winner(phone1, specs1, phone2, specs2)
        }

        # Save comparison if user_id provided
        if user_id:
            self._save_comparison(user_id, phone1_id, phone2_id)

        return comparison_data

    def _build_comparison_table(self, phone1, specs1, phone2, specs2):
        """Build detailed comparison table"""
        # Helper function to determine winner for numeric comparisons
        def get_numeric_winner(val1, val2, higher_is_better=True):
            """Return winner only if values are different"""
            v1 = val1 or 0
            v2 = val2 or 0
            if v1 == v2:
                return None
            if higher_is_better:
                return 1 if v1 > v2 else 2
            else:
                return 1 if v1 < v2 else 2

        # Helper function to extract maximum value from RAM/Storage strings
        def extract_max_value(text):
            """
            Extract maximum numeric value from strings like '8GB', '12GB / 16GB', '128GB / 256GB'
            Returns the maximum value as integer (in GB)
            """
            if not text:
                return 0
            import re
            # Find all numbers followed by GB or TB
            matches = re.findall(r'(\d+)\s*([GT])B', text.upper())
            if not matches:
                return 0
            # Convert to GB and get maximum
            values = []
            for num, unit in matches:
                if unit == 'T':  # Convert TB to GB
                    values.append(int(num) * 1024)
                else:  # GB
                    values.append(int(num))
            return max(values) if values else 0

        comparison = {
            'price': {
                'label': 'Price',
                'phone1': f"RM {phone1.price:,.2f}",
                'phone2': f"RM {phone2.price:,.2f}",
                'winner': get_numeric_winner(phone1.price, phone2.price, higher_is_better=False),
                'difference': abs(phone1.price - phone2.price)
            },
            'brand': {
                'label': 'Brand',
                'phone1': phone1.brand.name if phone1.brand else 'N/A',
                'phone2': phone2.brand.name if phone2.brand else 'N/A',
                'winner': None
            },
            'release_date': {
                'label': 'Release Date',
                'phone1': phone1.release_date.strftime('%b %Y') if phone1.release_date else 'N/A',
                'phone2': phone2.release_date.strftime('%b %Y') if phone2.release_date else 'N/A',
                'winner': None
            },
            'availability': {
                'label': 'Availability',
                'phone1': phone1.availability_status or 'N/A',
                'phone2': phone2.availability_status or 'N/A',
                'winner': None
            }
        }

        # Display comparisons
        if specs1 and specs2:
            comparison['screen_size'] = {
                'label': 'Screen Size',
                'phone1': f"{specs1.screen_size}\"" if specs1.screen_size else 'N/A',
                'phone2': f"{specs2.screen_size}\"" if specs2.screen_size else 'N/A',
                'winner': get_numeric_winner(specs1.screen_size, specs2.screen_size)
            }

            comparison['resolution'] = {
                'label': 'Resolution',
                'phone1': specs1.screen_resolution or 'N/A',
                'phone2': specs2.screen_resolution or 'N/A',
                'winner': None
            }

            comparison['screen_type'] = {
                'label': 'Display Type',
                'phone1': specs1.screen_type or 'N/A',
                'phone2': specs2.screen_type or 'N/A',
                'winner': None
            }

            comparison['refresh_rate'] = {
                'label': 'Refresh Rate',
                'phone1': f"{specs1.refresh_rate}Hz" if specs1.refresh_rate else 'N/A',
                'phone2': f"{specs2.refresh_rate}Hz" if specs2.refresh_rate else 'N/A',
                'winner': get_numeric_winner(specs1.refresh_rate, specs2.refresh_rate)
            }

            # Performance comparisons
            comparison['processor'] = {
                'label': 'Processor',
                'phone1': specs1.processor or 'N/A',
                'phone2': specs2.processor or 'N/A',
                'winner': None
            }

            comparison['ram'] = {
                'label': 'RAM',
                'phone1': specs1.ram_options or 'N/A',
                'phone2': specs2.ram_options or 'N/A',
                'winner': get_numeric_winner(
                    extract_max_value(specs1.ram_options),
                    extract_max_value(specs2.ram_options)
                )
            }

            comparison['storage'] = {
                'label': 'Storage',
                'phone1': specs1.storage_options or 'N/A',
                'phone2': specs2.storage_options or 'N/A',
                'winner': get_numeric_winner(
                    extract_max_value(specs1.storage_options),
                    extract_max_value(specs2.storage_options)
                )
            }

            # Helper function for boolean comparisons (defined here for expandable_storage)
            def get_boolean_winner(val1, val2):
                """Return winner only if boolean values are different"""
                if val1 == val2:
                    return None
                return 1 if val1 else 2

            comparison['expandable_storage'] = {
                'label': 'Expandable Storage',
                'phone1': '✓ Yes' if specs1.expandable_storage else '✗ No',
                'phone2': '✓ Yes' if specs2.expandable_storage else '✗ No',
                'winner': get_boolean_winner(specs1.expandable_storage, specs2.expandable_storage)
            }

            # Camera comparisons
            comparison['rear_camera'] = {
                'label': 'Rear Camera',
                'phone1': specs1.rear_camera or 'N/A',
                'phone2': specs2.rear_camera or 'N/A',
                'winner': get_numeric_winner(specs1.rear_camera_main, specs2.rear_camera_main)
            }

            comparison['front_camera'] = {
                'label': 'Front Camera',
                'phone1': specs1.front_camera or 'N/A',
                'phone2': specs2.front_camera or 'N/A',
                'winner': get_numeric_winner(specs1.front_camera_mp, specs2.front_camera_mp)
            }

            # Battery comparisons
            comparison['battery'] = {
                'label': 'Battery Capacity',
                'phone1': f"{specs1.battery_capacity}mAh" if specs1.battery_capacity else 'N/A',
                'phone2': f"{specs2.battery_capacity}mAh" if specs2.battery_capacity else 'N/A',
                'winner': get_numeric_winner(specs1.battery_capacity, specs2.battery_capacity)
            }

            comparison['charging'] = {
                'label': 'Charging',
                'phone1': specs1.charging_speed or 'N/A',
                'phone2': specs2.charging_speed or 'N/A',
                'winner': None
            }

            comparison['wireless_charging'] = {
                'label': 'Wireless Charging',
                'phone1': '✓ Yes' if specs1.wireless_charging else '✗ No',
                'phone2': '✓ Yes' if specs2.wireless_charging else '✗ No',
                'winner': get_boolean_winner(specs1.wireless_charging, specs2.wireless_charging)
            }

            # Connectivity comparisons
            comparison['5g'] = {
                'label': '5G Support',
                'phone1': '✓ Yes' if specs1.has_5g else '✗ No',
                'phone2': '✓ Yes' if specs2.has_5g else '✗ No',
                'winner': get_boolean_winner(specs1.has_5g, specs2.has_5g)
            }

            comparison['nfc'] = {
                'label': 'NFC',
                'phone1': '✓ Yes' if specs1.nfc else '✗ No',
                'phone2': '✓ Yes' if specs2.nfc else '✗ No',
                'winner': get_boolean_winner(specs1.nfc, specs2.nfc)
            }

            comparison['wifi'] = {
                'label': 'WiFi',
                'phone1': specs1.wifi_standard or 'N/A',
                'phone2': specs2.wifi_standard or 'N/A',
                'winner': None
            }

            comparison['bluetooth'] = {
                'label': 'Bluetooth',
                'phone1': specs1.bluetooth_version or 'N/A',
                'phone2': specs2.bluetooth_version or 'N/A',
                'winner': None
            }

            comparison['dual_sim'] = {
                'label': 'Dual SIM',
                'phone1': '✓ Yes' if specs1.dual_sim else '✗ No',
                'phone2': '✓ Yes' if specs2.dual_sim else '✗ No',
                'winner': get_boolean_winner(specs1.dual_sim, specs2.dual_sim)
            }

            # Additional features
            comparison['os'] = {
                'label': 'Operating System',
                'phone1': specs1.operating_system or 'N/A',
                'phone2': specs2.operating_system or 'N/A',
                'winner': None
            }

            comparison['fingerprint'] = {
                'label': 'Fingerprint Sensor',
                'phone1': '✓ Yes' if specs1.fingerprint_sensor else '✗ No',
                'phone2': '✓ Yes' if specs2.fingerprint_sensor else '✗ No',
                'winner': get_boolean_winner(specs1.fingerprint_sensor, specs2.fingerprint_sensor)
            }

            comparison['face_unlock'] = {
                'label': 'Face Unlock',
                'phone1': '✓ Yes' if specs1.face_unlock else '✗ No',
                'phone2': '✓ Yes' if specs2.face_unlock else '✗ No',
                'winner': get_boolean_winner(specs1.face_unlock, specs2.face_unlock)
            }

            comparison['water_resistance'] = {
                'label': 'Water Resistance',
                'phone1': specs1.water_resistance or 'N/A',
                'phone2': specs2.water_resistance or 'N/A',
                'winner': None
            }

            comparison['weight'] = {
                'label': 'Weight',
                'phone1': f"{specs1.weight}g" if specs1.weight else 'N/A',
                'phone2': f"{specs2.weight}g" if specs2.weight else 'N/A',
                'winner': get_numeric_winner(specs1.weight, specs2.weight, higher_is_better=False)
            }

            comparison['dimensions'] = {
                'label': 'Dimensions',
                'phone1': specs1.dimensions or 'N/A',
                'phone2': specs2.dimensions or 'N/A',
                'winner': None
            }

            comparison['colors'] = {
                'label': 'Available Colors',
                'phone1': specs1.colors_available or 'N/A',
                'phone2': specs2.colors_available or 'N/A',
                'winner': None
            }

        return comparison

    def _determine_winner(self, phone1, specs1, phone2, specs2):
        """Determine overall winner based on multiple factors"""
        phone1_score = 0
        phone2_score = 0

        # Price (lower is better)
        if phone1.price < phone2.price:
            phone1_score += 1
        else:
            phone2_score += 1

        if specs1 and specs2:
            # Screen size
            if (specs1.screen_size or 0) > (specs2.screen_size or 0):
                phone1_score += 1
            elif (specs2.screen_size or 0) > (specs1.screen_size or 0):
                phone2_score += 1

            # Camera
            if (specs1.rear_camera_main or 0) > (specs2.rear_camera_main or 0):
                phone1_score += 1
            elif (specs2.rear_camera_main or 0) > (specs1.rear_camera_main or 0):
                phone2_score += 1

            # Battery
            if (specs1.battery_capacity or 0) > (specs2.battery_capacity or 0):
                phone1_score += 1
            elif (specs2.battery_capacity or 0) > (specs1.battery_capacity or 0):
                phone2_score += 1

            # 5G
            if specs1.has_5g and not specs2.has_5g:
                phone1_score += 1
            elif specs2.has_5g and not specs1.has_5g:
                phone2_score += 1

            # Refresh rate
            if (specs1.refresh_rate or 0) > (specs2.refresh_rate or 0):
                phone1_score += 1
            elif (specs2.refresh_rate or 0) > (specs1.refresh_rate or 0):
                phone2_score += 1

        if phone1_score > phone2_score:
            return {'phone': 1, 'name': phone1.model_name, 'score': phone1_score}
        elif phone2_score > phone1_score:
            return {'phone': 2, 'name': phone2.model_name, 'score': phone2_score}
        else:
            return {'phone': None, 'name': 'Tie', 'score': phone1_score}

    def _save_comparison(self, user_id, phone1_id, phone2_id):
        """Save comparison to database"""
        comparison = Comparison(
            user_id=user_id,
            phone1_id=phone1_id,
            phone2_id=phone2_id
        )
        db.session.add(comparison)
        db.session.commit()

    def get_user_comparisons(self, user_id, limit=10):
        """Get user's comparison history"""
        comparisons = Comparison.query.filter_by(user_id=user_id)\
            .order_by(Comparison.created_at.desc())\
            .limit(limit)\
            .all()

        results = []
        for comp in comparisons:
            results.append({
                'id': comp.id,
                'phone1': comp.phone1,
                'phone2': comp.phone2,
                'created_at': comp.created_at,
                'is_saved': comp.is_saved
            })

        return results

    def save_comparison(self, comparison_id):
        """Mark a comparison as saved"""
        comparison = Comparison.query.get(comparison_id)
        if comparison:
            comparison.is_saved = True
            db.session.commit()
            return True
        return False

    def delete_comparison(self, comparison_id, user_id):
        """Delete a comparison"""
        comparison = Comparison.query.filter_by(id=comparison_id, user_id=user_id).first()
        if comparison:
            db.session.delete(comparison)
            db.session.commit()
            return True
        return False
