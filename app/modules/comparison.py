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
        comparison = {
            'price': {
                'label': 'Price',
                'phone1': f"RM {phone1.price:,.2f}",
                'phone2': f"RM {phone2.price:,.2f}",
                'winner': 1 if phone1.price < phone2.price else 2,
                'difference': abs(phone1.price - phone2.price)
            },
            'brand': {
                'label': 'Brand',
                'phone1': phone1.brand.name if phone1.brand else 'N/A',
                'phone2': phone2.brand.name if phone2.brand else 'N/A',
                'winner': None
            }
        }

        # Display comparisons
        if specs1 and specs2:
            comparison['screen_size'] = {
                'label': 'Screen Size',
                'phone1': f"{specs1.screen_size}\"" if specs1.screen_size else 'N/A',
                'phone2': f"{specs2.screen_size}\"" if specs2.screen_size else 'N/A',
                'winner': 1 if (specs1.screen_size or 0) > (specs2.screen_size or 0) else 2
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
                'winner': 1 if (specs1.refresh_rate or 0) > (specs2.refresh_rate or 0) else 2
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
                'winner': None
            }

            comparison['storage'] = {
                'label': 'Storage',
                'phone1': specs1.storage_options or 'N/A',
                'phone2': specs2.storage_options or 'N/A',
                'winner': None
            }

            # Camera comparisons
            comparison['rear_camera'] = {
                'label': 'Rear Camera',
                'phone1': specs1.rear_camera or 'N/A',
                'phone2': specs2.rear_camera or 'N/A',
                'winner': 1 if (specs1.rear_camera_main or 0) > (specs2.rear_camera_main or 0) else 2
            }

            comparison['front_camera'] = {
                'label': 'Front Camera',
                'phone1': specs1.front_camera or 'N/A',
                'phone2': specs2.front_camera or 'N/A',
                'winner': 1 if (specs1.front_camera_mp or 0) > (specs2.front_camera_mp or 0) else 2
            }

            # Battery comparisons
            comparison['battery'] = {
                'label': 'Battery Capacity',
                'phone1': f"{specs1.battery_capacity}mAh" if specs1.battery_capacity else 'N/A',
                'phone2': f"{specs2.battery_capacity}mAh" if specs2.battery_capacity else 'N/A',
                'winner': 1 if (specs1.battery_capacity or 0) > (specs2.battery_capacity or 0) else 2
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
                'winner': 1 if specs1.wireless_charging else 2 if specs2.wireless_charging else None
            }

            # Connectivity comparisons
            comparison['5g'] = {
                'label': '5G Support',
                'phone1': '✓ Yes' if specs1.has_5g else '✗ No',
                'phone2': '✓ Yes' if specs2.has_5g else '✗ No',
                'winner': 1 if specs1.has_5g else 2 if specs2.has_5g else None
            }

            comparison['nfc'] = {
                'label': 'NFC',
                'phone1': '✓ Yes' if specs1.nfc else '✗ No',
                'phone2': '✓ Yes' if specs2.nfc else '✗ No',
                'winner': 1 if specs1.nfc else 2 if specs2.nfc else None
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
                'winner': None
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
                'winner': 1 if (specs1.weight or 999) < (specs2.weight or 999) else 2
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
