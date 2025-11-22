"""
AI Recommendation Engine
Machine learning-based phone recommendation system
"""
from app import db
from app.models import Phone, PhoneSpecification, UserPreference, Recommendation
from app.utils.helpers import calculate_match_score, generate_recommendation_reasoning
import json

class AIRecommendationEngine:
    """AI-powered recommendation engine for smartphones"""

    def __init__(self):
        self.min_match_threshold = 50  # Minimum match percentage to recommend

    def get_recommendations(self, user_id, criteria=None, top_n=3):
        """
        Get top N phone recommendations for a user

        Args:
            user_id: User ID to get recommendations for
            criteria: Optional dictionary of criteria to override user preferences
            top_n: Number of recommendations to return

        Returns:
            List of recommended phones with match scores
        """
        from app.models import User

        user = User.query.get(user_id)
        if not user:
            return []

        # Get or create user preferences
        user_prefs = UserPreference.query.filter_by(user_id=user_id).first()

        # If criteria provided, create temporary preference object
        if criteria:
            user_prefs = self._create_temp_preferences(criteria)
        elif not user_prefs:
            # Create default preferences if none exist
            user_prefs = self._create_default_preferences(user_id)

        # Get all active phones with their specifications
        # CRITICAL FIX: Filter by budget FIRST before scoring
        query = Phone.query.filter_by(is_active=True)

        # Apply budget filter if preferences exist
        if user_prefs and hasattr(user_prefs, 'min_budget') and hasattr(user_prefs, 'max_budget'):
            query = query.filter(
                Phone.price >= user_prefs.min_budget,
                Phone.price <= user_prefs.max_budget
            )

        phones = query.all()

        # Calculate match scores for each phone
        recommendations = []
        for phone in phones:
            phone_specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            # Calculate match score
            match_score = calculate_match_score(user_prefs, phone, phone_specs)

            # Only include if above threshold
            if match_score >= self.min_match_threshold:
                reasoning = generate_recommendation_reasoning(
                    match_score, user_prefs, phone, phone_specs
                )

                recommendations.append({
                    'phone': phone,
                    'specifications': phone_specs,
                    'match_score': match_score,
                    'reasoning': reasoning
                })

        # Sort by match score (descending)
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Save recommendations to database if using actual user preferences
        if not criteria and user_prefs and hasattr(user_prefs, 'user_id'):
            self._save_recommendations(user_id, recommendations[:top_n], user_prefs)

        return recommendations[:top_n]

    def _create_temp_preferences(self, criteria):
        """Create temporary preference object from criteria dictionary"""
        class TempPreference:
            pass

        prefs = TempPreference()
        prefs.min_budget = criteria.get('min_budget', 500)
        prefs.max_budget = criteria.get('max_budget', 5000)
        prefs.min_ram = criteria.get('min_ram', 4)
        prefs.min_storage = criteria.get('min_storage', 64)
        prefs.min_camera = criteria.get('min_camera', 12)
        prefs.min_battery = criteria.get('min_battery', 3000)
        prefs.requires_5g = criteria.get('requires_5g', False)
        prefs.min_screen_size = criteria.get('min_screen_size', 5.5)
        prefs.max_screen_size = criteria.get('max_screen_size', 7.0)
        prefs.primary_usage = criteria.get('primary_usage', '[]')
        prefs.important_features = criteria.get('important_features', '[]')
        prefs.preferred_brands = criteria.get('preferred_brands', '[]')

        return prefs

    def _create_default_preferences(self, user_id):
        """Create default preferences for a user"""
        prefs = UserPreference(
            user_id=user_id,
            min_budget=500,
            max_budget=5000,
            min_ram=4,
            min_storage=64,
            min_camera=12,
            min_battery=3000,
            requires_5g=False,
            min_screen_size=5.5,
            max_screen_size=7.0,
            primary_usage='[]',
            important_features='[]',
            preferred_brands='[]'
        )
        db.session.add(prefs)
        db.session.commit()
        return prefs

    def _save_recommendations(self, user_id, recommendations, user_prefs):
        """Save recommendations to database"""
        criteria_dict = {
            'min_budget': user_prefs.min_budget,
            'max_budget': user_prefs.max_budget,
            'min_ram': user_prefs.min_ram,
            'min_storage': user_prefs.min_storage,
            'min_camera': user_prefs.min_camera,
            'min_battery': user_prefs.min_battery,
            'requires_5g': user_prefs.requires_5g
        }

        for rec in recommendations:
            recommendation = Recommendation(
                user_id=user_id,
                phone_id=rec['phone'].id,
                match_percentage=rec['match_score'],
                reasoning=rec['reasoning'],
                user_criteria=json.dumps(criteria_dict)
            )
            db.session.add(recommendation)

        db.session.commit()

    def get_budget_recommendations(self, budget_range, top_n=5):
        """Get top phones within a specific budget range"""
        min_price, max_price = budget_range

        phones = Phone.query.filter(
            Phone.is_active == True,
            Phone.price >= min_price,
            Phone.price <= max_price
        ).order_by(Phone.price.desc()).limit(top_n).all()

        results = []
        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            results.append({
                'phone': phone,
                'specifications': specs
            })

        return results

    def get_phones_by_usage(self, usage_type, budget_range=None, top_n=5):
        """Get phones optimized for specific usage types"""
        query = Phone.query.filter_by(is_active=True)

        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        phones = query.all()
        results = []

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if not specs:
                continue

            score = 0

            # Score based on usage type
            if usage_type == 'Gaming':
                # High RAM, good processor, high refresh rate
                ram_values = [int(r.replace('GB', '')) for r in (specs.ram_options or '').split(',') if 'GB' in r]
                if ram_values:
                    score += max(ram_values) * 10
                score += (specs.refresh_rate or 60) / 10
                score += specs.battery_capacity / 100 if specs.battery_capacity else 0

            elif usage_type == 'Photography':
                # High camera MP, good front camera
                score += (specs.rear_camera_main or 0) * 2
                score += (specs.front_camera_mp or 0)

            elif usage_type == 'Business' or usage_type == 'Work':
                # Good battery, decent specs
                score += specs.battery_capacity / 100 if specs.battery_capacity else 0
                ram_values = [int(r.replace('GB', '')) for r in (specs.ram_options or '').split(',') if 'GB' in r]
                if ram_values:
                    score += max(ram_values) * 5

            elif usage_type == 'Entertainment':
                # Large screen, good battery
                score += (specs.screen_size or 0) * 20
                score += specs.battery_capacity / 100 if specs.battery_capacity else 0

            else:  # Social Media and general use
                # Balanced specs, good camera
                score += (specs.rear_camera_main or 0)
                score += specs.battery_capacity / 200 if specs.battery_capacity else 0

            results.append({
                'phone': phone,
                'specifications': specs,
                'usage_score': score
            })

        # Sort by usage score
        results.sort(key=lambda x: x['usage_score'], reverse=True)

        return results[:top_n]

    def get_similar_phones(self, phone_id, top_n=3):
        """Get phones similar to a given phone"""
        reference_phone = Phone.query.get(phone_id)
        if not reference_phone:
            return []

        reference_specs = PhoneSpecification.query.filter_by(phone_id=phone_id).first()

        # Find phones in similar price range (±30%)
        price_min = reference_phone.price * 0.7
        price_max = reference_phone.price * 1.3

        similar_phones = Phone.query.filter(
            Phone.is_active == True,
            Phone.id != phone_id,
            Phone.price >= price_min,
            Phone.price <= price_max
        ).all()

        results = []
        for phone in similar_phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            results.append({
                'phone': phone,
                'specifications': specs
            })

        return results[:top_n]

    def get_phones_by_battery(self, min_battery_mah, budget_range=None, brand_names=None, top_n=5):
        """Get phones with battery above threshold"""
        query = Phone.query.filter_by(is_active=True)

        # Apply budget filter
        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Apply brand filter
        if brand_names:
            from app.models import Brand
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brand_names)).all()]
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.all()
        results = []

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs and specs.battery_capacity and specs.battery_capacity >= min_battery_mah:
                results.append({
                    'phone': phone,
                    'specifications': specs,
                    'battery_score': specs.battery_capacity
                })

        # Sort by battery capacity descending
        results.sort(key=lambda x: x['battery_score'], reverse=True)
        return results[:top_n]

    def get_phones_by_camera(self, min_camera_mp, budget_range=None, brand_names=None, top_n=5):
        """Get phones with camera above threshold"""
        query = Phone.query.filter_by(is_active=True)

        # Apply budget filter
        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Apply brand filter
        if brand_names:
            from app.models import Brand
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brand_names)).all()]
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.all()
        results = []

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs and specs.rear_camera_main and specs.rear_camera_main >= min_camera_mp:
                results.append({
                    'phone': phone,
                    'specifications': specs,
                    'camera_score': specs.rear_camera_main
                })

        # Sort by camera MP descending
        results.sort(key=lambda x: x['camera_score'], reverse=True)
        return results[:top_n]

    def get_phones_by_features(self, features, budget_range=None, usage_type=None, brand_names=None, user_category=None, top_n=5):
        """Get phones by specific features"""
        query = Phone.query.filter_by(is_active=True)

        # Apply budget filter
        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Apply brand filter
        if brand_names:
            from app.models import Brand
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brand_names)).all()]
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.all()
        results = []

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if not specs:
                continue

            score = 0

            # Score based on features
            for feature in features:
                if feature == 'battery':
                    score += (specs.battery_capacity or 0) / 100
                elif feature == 'camera':
                    score += (specs.rear_camera_main or 0) * 2
                elif feature == 'performance':
                    ram_values = [int(r.replace('GB', '')) for r in (specs.ram_options or '').split(',') if 'GB' in r]
                    if ram_values:
                        score += max(ram_values) * 10
                elif feature == 'display':
                    score += (specs.screen_size or 0) * 20
                elif feature == '5g' and specs.has_5g:
                    score += 50

            # Add usage type scoring
            if usage_type:
                if usage_type == 'Gaming':
                    ram_values = [int(r.replace('GB', '')) for r in (specs.ram_options or '').split(',') if 'GB' in r]
                    if ram_values:
                        score += max(ram_values) * 10
                elif usage_type == 'Photography':
                    score += (specs.rear_camera_main or 0) * 2
                elif usage_type in ['Business', 'Work']:
                    score += (specs.battery_capacity or 0) / 100

            # Add user category scoring
            if user_category == 'senior':
                score += (specs.battery_capacity or 0) / 50  # Prioritize battery for seniors
            elif user_category == 'student':
                score += phone.price / -100  # Prefer cheaper phones for students

            results.append({
                'phone': phone,
                'specifications': specs,
                'feature_score': score
            })

        # Sort by feature score descending
        results.sort(key=lambda x: x['feature_score'], reverse=True)
        return results[:top_n]
