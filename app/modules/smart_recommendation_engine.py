"""
Smart Phone Recommendation Engine
Intelligent phone filtering and recommendation based on specifications
"""
from app.models import Phone, PhoneSpecification, Brand
from sqlalchemy import and_, or_
import re


class SmartRecommendationEngine:
    """
    Advanced recommendation engine that filters phones based on detailed specifications
    """

    def __init__(self):
        pass

    def get_phones_by_budget(self, min_budget=None, max_budget=None, limit=10):
        """
        Get phones within budget range

        Args:
            min_budget: Minimum price
            max_budget: Maximum price
            limit: Maximum number of results

        Returns:
            List of phones with scores
        """
        query = Phone.query.filter(Phone.is_active == True)

        if min_budget is not None:
            query = query.filter(Phone.price >= min_budget)
        if max_budget is not None:
            query = query.filter(Phone.price <= max_budget)

        phones = query.order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_value_score(phone),
                'reason': self._get_budget_reason(phone, min_budget, max_budget)
            })

        # Sort by score
        results.sort(key=lambda x: x['score'], reverse=True)

        return results

    def get_phones_by_brand(self, brand_name, limit=10):
        """
        Get phones by brand

        Args:
            brand_name: Brand name
            limit: Maximum results

        Returns:
            List of phones
        """
        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()

        if not brand:
            return []

        phones = Phone.query.filter(
            Phone.brand_id == brand.id,
            Phone.is_active == True
        ).order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_value_score(phone),
                'reason': f"Popular {brand.name} model with great features"
            })

        return results

    def get_phones_by_usage(self, usage_type, budget=None, limit=10):
        """
        Get phones optimized for specific usage

        Args:
            usage_type: Usage type (Gaming, Photography, Business, etc.)
            budget: Optional budget tuple (min, max)
            limit: Maximum results

        Returns:
            List of phones optimized for the usage
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter if provided
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        usage_lower = usage_type.lower()

        if usage_lower == 'gaming':
            # Gaming: High refresh rate, powerful processor, good RAM
            query = query.filter(
                or_(
                    PhoneSpecification.refresh_rate >= 90,
                    PhoneSpecification.ram_options.like('%8GB%'),
                    PhoneSpecification.ram_options.like('%12GB%'),
                    PhoneSpecification.processor_brand.in_(['Qualcomm', 'Apple'])
                )
            )
        elif usage_lower == 'photography':
            # Photography: High MP camera, multiple lenses
            query = query.filter(
                or_(
                    PhoneSpecification.rear_camera_main >= 48,
                    PhoneSpecification.rear_camera.like('%MP%+%MP%')  # Multiple cameras
                )
            )
        elif usage_lower == 'business':
            # Business: Good battery, 5G, decent performance
            query = query.filter(
                or_(
                    PhoneSpecification.battery_capacity >= 4500,
                    PhoneSpecification.has_5g == True
                )
            )
        elif usage_lower == 'entertainment':
            # Entertainment: Large screen, good battery, AMOLED
            query = query.filter(
                or_(
                    PhoneSpecification.screen_size >= 6.5,
                    PhoneSpecification.screen_type.like('%AMOLED%'),
                    PhoneSpecification.battery_capacity >= 4500
                )
            )
        elif usage_lower == 'social media':
            # Social Media: Good front camera, decent performance
            query = query.filter(
                or_(
                    PhoneSpecification.front_camera_mp >= 16,
                    PhoneSpecification.rear_camera_main >= 48
                )
            )

        phones = query.order_by(Phone.price.desc()).limit(limit * 2).all()

        # Score and filter results
        results = []
        for phone in phones:
            score = self._calculate_usage_score(phone, usage_type)
            if score > 0:
                results.append({
                    'phone': phone,
                    'score': score,
                    'reason': self._get_usage_reason(phone, usage_type)
                })

        # Sort by score and limit
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:limit]

    def get_phones_by_feature(self, feature, budget=None, limit=10):
        """
        Get phones by specific feature

        Args:
            feature: Feature to filter by
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of phones with the feature
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        feature_lower = feature.lower()

        if '5g' in feature_lower:
            query = query.filter(PhoneSpecification.has_5g == True)
        elif 'wireless charging' in feature_lower or 'wireless_charging' in feature_lower:
            query = query.filter(PhoneSpecification.wireless_charging == True)
        elif 'water' in feature_lower or 'ip68' in feature_lower:
            query = query.filter(PhoneSpecification.water_resistance.isnot(None))
        elif 'expandable storage' in feature_lower or 'sd card' in feature_lower:
            query = query.filter(PhoneSpecification.expandable_storage == True)
        elif 'dual sim' in feature_lower:
            query = query.filter(PhoneSpecification.dual_sim == True)
        elif 'fast charging' in feature_lower:
            query = query.filter(PhoneSpecification.charging_speed.isnot(None))
        elif 'amoled' in feature_lower or 'oled' in feature_lower:
            query = query.filter(PhoneSpecification.screen_type.like('%AMOLED%'))
        elif 'nfc' in feature_lower:
            query = query.filter(PhoneSpecification.nfc == True)
        elif 'fingerprint' in feature_lower:
            query = query.filter(PhoneSpecification.fingerprint_sensor == True)
        elif 'face unlock' in feature_lower:
            query = query.filter(PhoneSpecification.face_unlock == True)

        phones = query.order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_value_score(phone),
                'reason': f"Includes {feature} feature"
            })

        return results

    def get_phones_by_camera(self, camera_spec, budget=None, limit=10):
        """
        Get phones by camera specifications

        Args:
            camera_spec: Camera specification to filter by
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of phones with good cameras
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        # Extract MP if mentioned
        mp_match = re.search(r'(\d+)\s*mp', camera_spec.lower())
        if mp_match:
            mp_value = int(mp_match.group(1))
            query = query.filter(PhoneSpecification.rear_camera_main >= mp_value)
        else:
            # Default to good cameras (48MP+)
            query = query.filter(PhoneSpecification.rear_camera_main >= 48)

        phones = query.order_by(PhoneSpecification.rear_camera_main.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_camera_score(phone),
                'reason': self._get_camera_reason(phone)
            })

        # Sort by camera score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def get_phones_by_performance(self, budget=None, limit=10):
        """
        Get high-performance phones

        Args:
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of high-performance phones
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        # Filter for flagship specs
        query = query.filter(
            or_(
                PhoneSpecification.processor_brand.in_(['Qualcomm', 'Apple']),
                PhoneSpecification.ram_options.like('%8GB%'),
                PhoneSpecification.ram_options.like('%12GB%'),
                PhoneSpecification.refresh_rate >= 90
            )
        )

        phones = query.order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_performance_score(phone),
                'reason': self._get_performance_reason(phone)
            })

        # Sort by performance score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def get_phones_by_battery(self, budget=None, limit=10):
        """
        Get phones with good battery life

        Args:
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of phones with good battery
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        # Filter for good battery (4500mAh+)
        query = query.filter(PhoneSpecification.battery_capacity >= 4500)

        phones = query.order_by(PhoneSpecification.battery_capacity.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_battery_score(phone),
                'reason': f"{phone.specifications.battery_capacity}mAh battery for all-day use"
            })

        return results

    def get_phones_by_display(self, display_spec, budget=None, limit=10):
        """
        Get phones by display specifications

        Args:
            display_spec: Display specification to filter by
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of phones with good displays
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        display_lower = display_spec.lower()

        if 'amoled' in display_lower or 'oled' in display_lower:
            query = query.filter(PhoneSpecification.screen_type.like('%AMOLED%'))
        elif '120hz' in display_lower:
            query = query.filter(PhoneSpecification.refresh_rate >= 120)
        elif '90hz' in display_lower:
            query = query.filter(PhoneSpecification.refresh_rate >= 90)
        elif 'large' in display_lower or 'big' in display_lower:
            query = query.filter(PhoneSpecification.screen_size >= 6.5)

        phones = query.order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_display_score(phone),
                'reason': self._get_display_reason(phone)
            })

        # Sort by display score
        results.sort(key=lambda x: x['score'], reverse=True)
        return results

    def get_phones_by_storage(self, storage_spec, budget=None, limit=10):
        """
        Get phones by storage requirements

        Args:
            storage_spec: Storage specification
            budget: Optional budget tuple
            limit: Maximum results

        Returns:
            List of phones with adequate storage
        """
        query = Phone.query.join(PhoneSpecification).filter(Phone.is_active == True)

        # Apply budget filter
        if budget:
            min_budget, max_budget = budget
            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

        storage_lower = storage_spec.lower()

        # Extract storage size if mentioned
        storage_match = re.search(r'(\d+)\s*gb', storage_lower)
        if storage_match:
            storage_size = storage_match.group(1)
            query = query.filter(PhoneSpecification.storage_options.like(f'%{storage_size}GB%'))
        elif 'expandable' in storage_lower or 'sd card' in storage_lower:
            query = query.filter(PhoneSpecification.expandable_storage == True)

        phones = query.order_by(Phone.price.desc()).limit(limit).all()

        results = []
        for phone in phones:
            results.append({
                'phone': phone,
                'score': self._calculate_value_score(phone),
                'reason': f"Offers {phone.specifications.storage_options} storage"
            })

        return results

    # Scoring functions

    def _calculate_value_score(self, phone):
        """Calculate overall value score"""
        score = 50  # Base score

        if phone.specifications:
            specs = phone.specifications

            # Camera score
            if specs.rear_camera_main:
                score += min(specs.rear_camera_main / 10, 15)

            # Battery score
            if specs.battery_capacity:
                score += min(specs.battery_capacity / 500, 10)

            # Display score
            if specs.refresh_rate is not None and specs.refresh_rate >= 90:
                score += 10

            # 5G bonus
            if specs.has_5g:
                score += 5

            # Price adjustment (better value for lower prices)
            if phone.price < 1500:
                score += 10

        return score

    def _calculate_usage_score(self, phone, usage_type):
        """Calculate usage-specific score"""
        if not phone.specifications:
            return 0

        specs = phone.specifications
        score = 0
        usage_lower = usage_type.lower()

        if usage_lower == 'gaming':
            if specs.refresh_rate is not None and specs.refresh_rate >= 120:
                score += 30
            elif specs.refresh_rate is not None and specs.refresh_rate >= 90:
                score += 20
            if specs.ram_options and ('8GB' in specs.ram_options or '12GB' in specs.ram_options):
                score += 25
            if specs.processor_brand and specs.processor_brand in ['Qualcomm', 'Apple']:
                score += 25
            if specs.battery_capacity is not None and specs.battery_capacity >= 4500:
                score += 20

        elif usage_lower == 'photography':
            if specs.rear_camera_main is not None and specs.rear_camera_main >= 108:
                score += 40
            elif specs.rear_camera_main is not None and specs.rear_camera_main >= 64:
                score += 30
            elif specs.rear_camera_main is not None and specs.rear_camera_main >= 48:
                score += 20
            if specs.rear_camera and '+' in specs.rear_camera:  # Multiple cameras
                score += 15
            if specs.screen_type and 'AMOLED' in specs.screen_type:
                score += 15
            if specs.front_camera_mp is not None and specs.front_camera_mp >= 32:
                score += 15

        elif usage_lower == 'business':
            if specs.has_5g:
                score += 25
            if specs.battery_capacity is not None and specs.battery_capacity >= 5000:
                score += 30
            elif specs.battery_capacity is not None and specs.battery_capacity >= 4500:
                score += 20
            if specs.processor_brand and specs.processor_brand in ['Qualcomm', 'Apple']:
                score += 15
            if specs.fast_charging:
                score += 10

        elif usage_lower == 'entertainment':
            if specs.screen_size is not None and specs.screen_size >= 6.7:
                score += 25
            elif specs.screen_size is not None and specs.screen_size >= 6.5:
                score += 15
            if specs.screen_type and 'AMOLED' in specs.screen_type:
                score += 25
            if specs.battery_capacity is not None and specs.battery_capacity >= 5000:
                score += 25
            if specs.refresh_rate is not None and specs.refresh_rate >= 90:
                score += 15

        elif usage_lower == 'social media':
            if specs.front_camera_mp is not None and specs.front_camera_mp >= 32:
                score += 30
            elif specs.front_camera_mp is not None and specs.front_camera_mp >= 16:
                score += 20
            if specs.rear_camera_main is not None and specs.rear_camera_main >= 48:
                score += 20
            if specs.screen_type and 'AMOLED' in specs.screen_type:
                score += 15
            if specs.battery_capacity is not None and specs.battery_capacity >= 4500:
                score += 15

        elif usage_lower == 'basic':
            # For senior citizens and basic users - prioritize ease of use, battery, durability
            if specs.battery_capacity is not None and specs.battery_capacity >= 5000:
                score += 40  # Long battery life is critical
            elif specs.battery_capacity is not None and specs.battery_capacity >= 4000:
                score += 25
            if specs.screen_size is not None and specs.screen_size >= 6.0:  # Bigger screen for readability
                score += 20
            if phone.price <= 1500:  # Budget-friendly
                score += 30
            # Simpler is better - avoid overly complex features
            if specs.ram_options and '4GB' in specs.ram_options:
                score += 15  # Sufficient RAM for basic tasks

        return score

    def _calculate_camera_score(self, phone):
        """Calculate camera score"""
        if not phone.specifications:
            return 0

        specs = phone.specifications
        score = 0

        if specs.rear_camera_main is not None:
            score += min(specs.rear_camera_main, 50)

        if specs.front_camera_mp is not None:
            score += min(specs.front_camera_mp, 20)

        if '+' in specs.rear_camera:  # Multiple cameras
            score += 15

        return score

    def _calculate_performance_score(self, phone):
        """Calculate performance score"""
        if not phone.specifications:
            return 0

        specs = phone.specifications
        score = 0

        if specs.processor_brand == 'Apple':
            score += 40
        elif specs.processor_brand == 'Qualcomm':
            score += 35

        if '12GB' in specs.ram_options:
            score += 30
        elif '8GB' in specs.ram_options:
            score += 20

        if specs.refresh_rate is not None and specs.refresh_rate >= 120:
            score += 20
        elif specs.refresh_rate is not None and specs.refresh_rate >= 90:
            score += 10

        return score

    def _calculate_battery_score(self, phone):
        """Calculate battery score"""
        if not phone.specifications or not phone.specifications.battery_capacity:
            return 0

        return phone.specifications.battery_capacity / 100

    def _calculate_display_score(self, phone):
        """Calculate display score"""
        if not phone.specifications:
            return 0

        specs = phone.specifications
        score = 0

        if 'AMOLED' in specs.screen_type:
            score += 30

        if specs.refresh_rate is not None and specs.refresh_rate >= 120:
            score += 30
        elif specs.refresh_rate is not None and specs.refresh_rate >= 90:
            score += 20

        if specs.screen_size is not None and specs.screen_size >= 6.7:
            score += 20
        elif specs.screen_size is not None and specs.screen_size >= 6.5:
            score += 10

        return score

    # Reason functions

    def _get_budget_reason(self, phone, min_budget, max_budget):
        """Get reason for budget recommendation"""
        return f"Great value at RM{phone.price:,.2f}"

    def _get_usage_reason(self, phone, usage_type):
        """Get reason for usage recommendation"""
        if not phone.specifications:
            return f"Good for {usage_type}"

        specs = phone.specifications
        usage_lower = usage_type.lower()

        if usage_lower == 'gaming':
            return f"{specs.refresh_rate}Hz display, {specs.ram_options} RAM - Perfect for gaming"
        elif usage_lower == 'photography':
            return f"{specs.rear_camera_main}MP main camera - Excellent for photography"
        elif usage_lower == 'business':
            return f"{'5G, ' if specs.has_5g else ''}{specs.battery_capacity}mAh battery - Ideal for business"
        elif usage_lower == 'entertainment':
            return f"{specs.screen_size}\" {specs.screen_type} display - Great for entertainment"
        else:
            return f"Optimized for {usage_type}"

    def _get_camera_reason(self, phone):
        """Get reason for camera recommendation"""
        if not phone.specifications:
            return "Good camera quality"

        specs = phone.specifications
        return f"{specs.rear_camera_main}MP main camera with {specs.rear_camera}"

    def _get_performance_reason(self, phone):
        """Get reason for performance recommendation"""
        if not phone.specifications:
            return "High performance"

        specs = phone.specifications
        return f"{specs.processor_brand} processor, {specs.ram_options} RAM"

    def _get_display_reason(self, phone):
        """Get reason for display recommendation"""
        if not phone.specifications:
            return "Great display"

        specs = phone.specifications
        return f"{specs.screen_size}\" {specs.screen_type}, {specs.refresh_rate}Hz"
