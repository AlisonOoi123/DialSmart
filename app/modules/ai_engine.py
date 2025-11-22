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
        self.min_match_threshold = 30  # Minimum match percentage to recommend (lowered for better results)

    def _extract_ram_values(self, ram_string):
        """
        Safely extract RAM values from string, handling various formats
        Examples: "8GB", "8 / 16 GB", "8GB, 16GB", "12 / 16 / 24TB" (typo)
        Returns list of integers
        """
        if not ram_string:
            return []

        import re
        # Find all numbers that appear before GB (ignore TB typos)
        matches = re.findall(r'(\d+)\s*(?:GB|gb)', str(ram_string))

        try:
            return [int(m) for m in matches]
        except (ValueError, AttributeError):
            return []

    def _extract_storage_values(self, storage_string):
        """
        Safely extract storage values from string, handling various formats
        Examples: "128GB", "128 / 256 GB", "256GB, 512GB", "1TB"
        Returns list of integers (in GB)
        """
        if not storage_string:
            return []

        import re
        # Find all numbers that appear before GB
        gb_matches = re.findall(r'(\d+)\s*(?:GB|gb)', str(storage_string))
        # Find all numbers that appear before TB and convert to GB
        tb_matches = re.findall(r'(\d+)\s*(?:TB|tb)', str(storage_string))

        try:
            values = [int(m) for m in gb_matches]
            values.extend([int(m) * 1024 for m in tb_matches])  # Convert TB to GB
            return values
        except (ValueError, AttributeError):
            return []

    def get_recommendations(self, user_id, criteria=None, top_n=3):
        """
        Get top N phone recommendations for a user

        Args:
            user_id: User ID to get recommendations for (can be None for anonymous users)
            criteria: Optional dictionary of criteria to override user preferences
            top_n: Number of recommendations to return

        Returns:
            List of recommended phones with match scores
        """
        # If criteria provided, use temporary preference object (for anonymous users or wizard)
        if criteria:
            user_prefs = self._create_temp_preferences(criteria)
        elif user_id:
            # Get or create user preferences for authenticated users
            from app.models import User
            user = User.query.get(user_id)
            if not user:
                return []

            user_prefs = UserPreference.query.filter_by(user_id=user_id).first()
            if not user_prefs:
                # Create default preferences if none exist
                user_prefs = self._create_default_preferences(user_id)
        else:
            # Anonymous user without criteria - use defaults
            user_prefs = self._create_temp_preferences({})

        # Get all active phones with their specifications
        phones = Phone.query.filter_by(is_active=True).all()

        # Calculate match scores for each phone
        all_scored_phones = []
        for phone in phones:
            phone_specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            # Calculate match score
            match_score = calculate_match_score(user_prefs, phone, phone_specs)

            reasoning = generate_recommendation_reasoning(
                match_score, user_prefs, phone, phone_specs
            )

            all_scored_phones.append({
                'phone': phone,
                'specifications': phone_specs,
                'match_score': match_score,
                'reasoning': reasoning
            })

        # Sort by match score (descending)
        all_scored_phones.sort(key=lambda x: x['match_score'], reverse=True)

        # Check if user has selected specific brands for balanced distribution
        preferred_brands = []
        if hasattr(user_prefs, 'preferred_brands'):
            if isinstance(user_prefs.preferred_brands, list):
                preferred_brands = user_prefs.preferred_brands
            elif isinstance(user_prefs.preferred_brands, str) and user_prefs.preferred_brands:
                try:
                    preferred_brands = json.loads(user_prefs.preferred_brands)
                except (json.JSONDecodeError, ValueError):
                    preferred_brands = []

        # Convert to integers
        try:
            preferred_brands = [int(b) for b in preferred_brands if b]
        except (ValueError, TypeError):
            preferred_brands = []

        # If user selected multiple brands, distribute recommendations evenly across brands
        if len(preferred_brands) > 1:
            recommendations = self._get_balanced_brand_recommendations(
                all_scored_phones, preferred_brands, top_n, self.min_match_threshold
            )
        else:
            # Original logic: Filter by threshold, but if no matches, return top N anyway
            recommendations = [p for p in all_scored_phones if p['match_score'] >= self.min_match_threshold]

            if not recommendations and all_scored_phones:
                # No phones meet threshold, return top N best matches anyway
                recommendations = all_scored_phones[:top_n]
            else:
                recommendations = recommendations[:top_n]

        # Save recommendations to database if using actual user preferences
        if not criteria and user_prefs and hasattr(user_prefs, 'user_id') and user_id:
            self._save_recommendations(user_id, recommendations[:top_n], user_prefs)

        return recommendations[:top_n]

    def _get_balanced_brand_recommendations(self, all_scored_phones, preferred_brands, top_n, threshold):
        """
        Get balanced recommendations across multiple selected brands.
        Distributes recommendations evenly across brands (e.g., if 3 brands selected and 5 recommendations needed,
        return 2 from brand A, 2 from brand B, 1 from brand C)

        Args:
            all_scored_phones: List of all phones with scores
            preferred_brands: List of preferred brand IDs
            top_n: Number of recommendations to return
            threshold: Minimum match threshold

        Returns:
            Balanced list of recommendations
        """
        # Group phones by brand (only from preferred brands)
        phones_by_brand = {brand_id: [] for brand_id in preferred_brands}

        for phone_data in all_scored_phones:
            brand_id = phone_data['phone'].brand_id
            if brand_id in preferred_brands:
                phones_by_brand[brand_id].append(phone_data)

        # Remove empty brands
        phones_by_brand = {k: v for k, v in phones_by_brand.items() if v}

        if not phones_by_brand:
            # No phones from preferred brands, return top N overall
            return all_scored_phones[:top_n]

        # Distribute recommendations using round-robin approach
        balanced_recommendations = []
        brand_ids = list(phones_by_brand.keys())
        brand_index = 0

        # Keep track of which index we're at for each brand
        brand_pointers = {brand_id: 0 for brand_id in brand_ids}

        # Round-robin distribution
        while len(balanced_recommendations) < top_n:
            current_brand = brand_ids[brand_index % len(brand_ids)]
            brand_phones = phones_by_brand[current_brand]
            pointer = brand_pointers[current_brand]

            # If this brand still has phones to recommend
            if pointer < len(brand_phones):
                phone_data = brand_phones[pointer]
                # Only add if meets threshold OR we don't have enough recommendations yet
                if phone_data['match_score'] >= threshold or len(balanced_recommendations) < len(brand_ids):
                    balanced_recommendations.append(phone_data)
                    brand_pointers[current_brand] += 1

            brand_index += 1

            # Safety check: if all brands exhausted, break
            if all(brand_pointers[b] >= len(phones_by_brand[b]) for b in brand_ids):
                break

        return balanced_recommendations[:top_n]

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

    def get_phones_by_usage(self, usage_type, budget_range=None, brand_names=None, top_n=5):
        """
        Get phones optimized for specific usage types

        Args:
            usage_type: Type of usage (Gaming, Photography, etc.)
            budget_range: Optional (min, max) price range
            brand_names: Optional list of brand names to filter by
            top_n: Number of results to return
        """
        from app.models import Brand
        query = Phone.query.filter_by(is_active=True)

        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Filter by brands if specified
        if brand_names:
            from app.models import Brand
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

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
                ram_values = self._extract_ram_values(specs.ram_options)
                if ram_values:
                    score += max(ram_values) * 10
                score += (specs.refresh_rate or 60) / 10
                score += specs.battery_capacity / 100 if specs.battery_capacity else 0

            elif usage_type == 'Photography':
                # High camera MP, good front camera
                score += (specs.rear_camera_main or 0) * 2
                score += (specs.front_camera_mp or 0)

                storage_values = []
                if specs.storage_options:
                    storage_str = specs.storage_options.replace('GB', '').replace('TB', '000')
                    for s in storage_str.split(','):
                        try:
                            storage_values.append(int(s.strip()))
                        except:
                            pass
                if storage_values:
                    score += max(storage_values) / 10

            elif usage_type == 'Business' or usage_type == 'Work':
                # Good battery, decent specs
                score += specs.battery_capacity / 100 if specs.battery_capacity else 0
                ram_values = self._extract_ram_values(specs.ram_options)
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

        # If multiple brands requested, distribute results evenly across brands
        if brand_names and len(brand_names) > 1:
            from app.models import Brand
            # Get brand IDs for requested brands
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)

            if len(brand_ids) > 1:
                # Group results by brand
                results_by_brand = {brand_id: [] for brand_id in brand_ids}
                for result in results:
                    brand_id = result['phone'].brand_id
                    if brand_id in results_by_brand:
                        results_by_brand[brand_id].append(result)

                # Remove empty brands
                results_by_brand = {k: v for k, v in results_by_brand.items() if v}

                if results_by_brand:
                    # Distribute evenly using round-robin
                    balanced_results = []
                    brand_ids_list = list(results_by_brand.keys())
                    brand_pointers = {brand_id: 0 for brand_id in brand_ids_list}

                    while len(balanced_results) < top_n:
                        added_this_round = False
                        for brand_id in brand_ids_list:
                            if brand_pointers[brand_id] < len(results_by_brand[brand_id]):
                                balanced_results.append(results_by_brand[brand_id][brand_pointers[brand_id]])
                                brand_pointers[brand_id] += 1
                                added_this_round = True
                                if len(balanced_results) >= top_n:
                                    break

                        # If no phones added this round, all brands exhausted
                        if not added_this_round:
                            break

                    return balanced_results[:top_n]

        return results[:top_n]

    def get_phones_by_features(self, features, budget_range=None, usage_type=None, brand_names=None, user_category=None, top_n=5):
        """
        Get phones based on specific feature priorities

        Args:
            features: List of prioritized features ['battery', 'camera', 'display', etc.]
            budget_range: Optional (min, max) price range
            usage_type: Optional usage type
            brand_names: Optional list of brand names
            user_category: Optional user category (senior, student, etc.)
            top_n: Number of results to return
        """
        from app.models import Brand
        query = Phone.query.filter_by(is_active=True)

        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Filter by brands if specified
        if brand_names:
            from app.models import Brand
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.all()
        results = []

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if not specs:
                continue

            score = 0

            # Score based on prioritized features
            for feature in features:
                if feature == 'battery':
                    # Long lasting battery
                    score += (specs.battery_capacity or 0) / 10
                elif feature == 'camera':
                    # Best camera
                    score += (specs.rear_camera_main or 0) * 3
                    score += (specs.front_camera_mp or 0)
                elif feature == 'display':
                    # AMOLED display
                    if specs.screen_type and 'amoled' in specs.screen_type.lower():
                        score += 100
                    elif specs.screen_type and 'oled' in specs.screen_type.lower():
                        score += 80
                    score += (specs.screen_size or 0) * 10
                    score += (specs.refresh_rate or 60) / 2
                elif feature == 'performance':
                    # Fast processor
                    ram_values = self._extract_ram_values(specs.ram_options)
                    if ram_values:
                        score += max(ram_values) * 15
                    if specs.processor and any(chip in specs.processor.lower() for chip in ['snapdragon 8', 'a17', 'a16', 'dimensity 9']):
                        score += 150
                    elif specs.processor:
                        score += 50
                elif feature == '5g':
                    # 5G support
                    if specs.has_5g:
                        score += 200

            # Additional scoring based on usage type
            if usage_type == 'Photography':
                # Photography users: prioritize camera MP first
                if specs.rear_camera_main:
                    score += specs.rear_camera_main * 5  # Heavily prioritize main camera
                if specs.front_camera_mp:
                    score += specs.front_camera_mp * 2  # Also consider selfie camera
                # Good display for reviewing photos
                if specs.screen_type and ('amoled' in specs.screen_type.lower() or 'oled' in specs.screen_type.lower()):
                    score += 80
            elif usage_type == 'Gaming':
                ram_values = self._extract_ram_values(specs.ram_options)
                if ram_values:
                    score += max(ram_values) * 10
                score += (specs.refresh_rate or 60) / 10

            # Adjustments for user category
            if user_category == 'senior':
                # Prefer budget phones with entertainment capabilities
                # Good battery for all-day use
                score += (specs.battery_capacity or 0) / 5
                # Larger screens for better visibility
                if specs.screen_size and specs.screen_size >= 6.5:
                    score += 50
                # Prefer budget-friendly options (lower price = higher score)
                if phone.price <= 1500:
                    score += 100
                elif phone.price <= 2500:
                    score += 50
                # Good display for entertainment
                if specs.screen_type and ('amoled' in specs.screen_type.lower() or 'oled' in specs.screen_type.lower()):
                    score += 60
            elif user_category == 'student':
                # Value phones with good performance (processor priority)
                # Prefer mid-range pricing (best value)
                if 1000 <= phone.price <= 2500:
                    score += 80
                # Prioritize good processor for multitasking
                if specs.processor:
                    if any(chip in specs.processor.lower() for chip in ['snapdragon 7', 'snapdragon 8', 'dimensity 8', 'dimensity 9', 'helio g9']):
                        score += 120
                    elif any(chip in specs.processor.lower() for chip in ['snapdragon', 'dimensity', 'helio']):
                        score += 60
                # Good RAM for performance
                ram_values = self._extract_ram_values(specs.ram_options)
                if ram_values:
                    max_ram = max(ram_values)
                    if max_ram >= 8:
                        score += 80
                    elif max_ram >= 6:
                        score += 50
                # Decent battery
                score += (specs.battery_capacity or 0) / 8
            elif user_category == 'professional':
                # Workers need: long battery, big storage, good performance
                # Long-lasting battery is critical
                if specs.battery_capacity:
                    if specs.battery_capacity >= 5000:
                        score += 150
                    elif specs.battery_capacity >= 4500:
                        score += 100
                    else:
                        score += specs.battery_capacity / 30
                # Big storage for work files
                storage_values = self._extract_storage_values(specs.storage_options)
                if storage_values:
                    max_storage = max(storage_values)
                    if max_storage >= 256:
                        score += 120
                    elif max_storage >= 128:
                        score += 80
                # Good performance/processor for productivity
                if specs.processor and any(chip in specs.processor.lower() for chip in ['snapdragon 8', 'snapdragon 7', 'dimensity 8', 'dimensity 9']):
                    score += 100
                # Decent RAM
                ram_values = self._extract_ram_values(specs.ram_options)
                if ram_values and max(ram_values) >= 8:
                    score += 60

            results.append({
                'phone': phone,
                'specifications': specs,
                'feature_score': score
            })

        # Sort by feature score
        results.sort(key=lambda x: x['feature_score'], reverse=True)

        # If multiple brands requested, distribute results evenly across brands
        if brand_names and len(brand_names) > 1:
            from app.models import Brand
            # Get brand IDs for requested brands
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)

            if len(brand_ids) > 1:
                # Group results by brand
                results_by_brand = {brand_id: [] for brand_id in brand_ids}
                for result in results:
                    brand_id = result['phone'].brand_id
                    if brand_id in results_by_brand:
                        results_by_brand[brand_id].append(result)

                # Remove empty brands
                results_by_brand = {k: v for k, v in results_by_brand.items() if v}

                if results_by_brand:
                    # Distribute evenly using round-robin
                    balanced_results = []
                    brand_ids_list = list(results_by_brand.keys())
                    brand_pointers = {brand_id: 0 for brand_id in brand_ids_list}

                    while len(balanced_results) < top_n:
                        added_this_round = False
                        for brand_id in brand_ids_list:
                            if brand_pointers[brand_id] < len(results_by_brand[brand_id]):
                                balanced_results.append(results_by_brand[brand_id][brand_pointers[brand_id]])
                                brand_pointers[brand_id] += 1
                                added_this_round = True
                                if len(balanced_results) >= top_n:
                                    break

                        # If no phones added this round, all brands exhausted
                        if not added_this_round:
                            break

                    return balanced_results[:top_n]

        return results[:top_n]
    
    def get_phones_by_battery(self, min_battery_mah, budget_range=None, brand_names=None, top_n=5):
        """
        Get phones with battery capacity above a certain threshold

        Args:
            min_battery_mah: Minimum battery capacity in mAh
            budget_range: Optional (min_price, max_price) tuple
            brand_names: Optional list of brand names to filter
            top_n: Number of results to return
        """
        from app.models import Brand
        query = Phone.query.join(PhoneSpecification).filter(
            Phone.is_active == True,
            PhoneSpecification.battery_capacity >= min_battery_mah
        )

        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Filter by brands if specified
        if brand_names:
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.order_by(PhoneSpecification.battery_capacity.desc()).limit(top_n).all()

        results = []
        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            results.append({
                'phone': phone,
                'specifications': specs
            })

        return results
    
    def get_phones_by_camera(self, min_camera_mp, budget_range=None, brand_names=None, top_n=5):
        """
        Get phones with camera MP above a certain threshold

        Args:
            min_camera_mp: Minimum rear camera megapixels
            budget_range: Optional (min_price, max_price) tuple
            brand_names: Optional list of brand names to filter
            top_n: Number of results to return
        """
        query = Phone.query.filter_by(is_active=True)

        from app.models import Brand
        query = Phone.query.join(PhoneSpecification).filter(
            Phone.is_active == True,
            PhoneSpecification.rear_camera_main >= min_camera_mp
        )

        if budget_range:
            min_price, max_price = budget_range
            query = query.filter(Phone.price >= min_price, Phone.price <= max_price)

        # Filter by brands if specified
        if brand_names:
            from app.models import Brand
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                query = query.filter(Phone.brand_id.in_(brand_ids))

        phones = query.order_by(PhoneSpecification.rear_camera_main.desc()).limit(top_n).all()

        results = []
        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs and specs.rear_camera_main:
                # Robust camera value handling with type conversion
                try:
                    # Handle different formats (e.g., "48", "48MP", "48.0")
                    camera_value = str(specs.rear_camera_main).replace('MP', '').strip()
                    camera_mp = float(camera_value)
                    
                    if camera_mp >= min_camera_mp:
                        results.append({
                            'phone': phone,
                            'specifications': specs,
                            'camera_score': camera_mp  
                        })
                except (ValueError, TypeError) as e:
                    # Log the issue but continue processing
                    print(f"Warning: Could not parse camera value for {phone.name}: {specs.rear_camera_main}")
                    continue
        
        # Sort by camera MP descending for best cameras first
        results.sort(key=lambda x: x['camera_score'], reverse=True)
        
        # Return top N results
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
