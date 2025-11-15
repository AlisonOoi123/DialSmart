"""
Enhanced AI Recommendation Engine
Advanced recommendation system considering user demographics and preferences
"""
from app import db
from app.models import Phone, PhoneSpecification, UserPreference, Recommendation, User
from app.utils.helpers import calculate_match_score, generate_recommendation_reasoning, parse_memory_values
import json

class EnhancedAIRecommendationEngine:
    """
    Advanced AI-powered recommendation engine
    Considers: Age, Occupation, Budget, Usage Patterns, and Preferences
    """

    def __init__(self):
        self.min_match_threshold = 40  # Lowered threshold for more diverse recommendations

        # Demographic-based preference weights
        self.age_profiles = {
            '18-25': {
                'priorities': ['Performance', 'Gaming', 'Social Media', 'Camera'],
                'budget_preference': 'mid_range',
                'features': ['5G', 'High Refresh Rate', 'Fast Charging'],
                'max_price_comfort': 2500
            },
            '26-35': {
                'priorities': ['Camera', 'Performance', 'Battery', 'Design'],
                'budget_preference': 'upper_mid',
                'features': ['5G', 'Wireless Charging', 'Water Resistance'],
                'max_price_comfort': 4000
            },
            '36-45': {
                'priorities': ['Battery', 'Camera', 'Reliability', 'Business'],
                'budget_preference': 'premium',
                'features': ['Dual SIM', 'Expandable Storage', '5G'],
                'max_price_comfort': 5000
            },
            '46-55': {
                'priorities': ['Battery', 'Ease of Use', 'Camera', 'Display'],
                'budget_preference': 'mid_range',
                'features': ['Large Screen', 'Good Battery', 'Simple Interface'],
                'max_price_comfort': 3000
            },
            '56+': {
                'priorities': ['Battery', 'Ease of Use', 'Display', 'Camera'],
                'budget_preference': 'budget',
                'features': ['Large Display', 'Long Battery', 'Loud Speaker'],
                'max_price_comfort': 2000
            }
        }

        # Occupation-based profiles
        self.occupation_profiles = {
            'Student': {
                'priorities': ['Budget', 'Battery', 'Performance', 'Camera'],
                'max_budget': 2000,
                'recommended_features': ['Fast Charging', '5G', 'Good Camera'],
                'usage': ['Social Media', 'Gaming', 'Entertainment']
            },
            'Working Professional': {
                'priorities': ['Productivity', 'Battery', 'Camera', 'Build Quality'],
                'max_budget': 4500,
                'recommended_features': ['Dual SIM', '5G', 'Wireless Charging', 'Premium Build'],
                'usage': ['Business', 'Communication', 'Photography']
            },
            'Senior Citizen': {
                'priorities': ['Ease of Use', 'Battery', 'Display', 'Reliability'],
                'max_budget': 2500,
                'recommended_features': ['Large Display', 'Long Battery', 'Simple UI'],
                'usage': ['Communication', 'Entertainment']
            },
            'Freelancer': {
                'priorities': ['Camera', 'Performance', 'Battery', 'Portability'],
                'max_budget': 3500,
                'recommended_features': ['Excellent Camera', 'Fast Performance', '5G'],
                'usage': ['Photography', 'Work', 'Social Media']
            },
            'Gamer': {
                'priorities': ['Performance', 'Display', 'Battery', 'Cooling'],
                'max_budget': 3000,
                'recommended_features': ['High Refresh Rate', 'Gaming Processor', 'Fast Charging'],
                'usage': ['Gaming', 'Entertainment', 'Performance']
            }
        }

    def get_smart_recommendations(self, user_id, criteria=None, top_n=5):
        """
        Get intelligent recommendations based on user demographics

        Args:
            user_id: User ID
            criteria: Optional override criteria
            top_n: Number of recommendations

        Returns:
            List of recommended phones with enhanced scoring
        """
        user = User.query.get(user_id)
        if not user:
            return []

        # Get user profile
        user_profile = self._build_user_profile(user, criteria)

        # Get all active phones
        phones = Phone.query.filter_by(is_active=True).all()

        # Calculate enhanced match scores
        recommendations = []
        for phone in phones:
            phone_specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            # Enhanced scoring with demographics
            match_score = self._calculate_enhanced_score(
                user_profile, user, phone, phone_specs
            )

            if match_score >= self.min_match_threshold:
                reasoning = self._generate_smart_reasoning(
                    user_profile, user, phone, phone_specs, match_score
                )

                recommendations.append({
                    'phone': phone,
                    'specifications': phone_specs,
                    'match_score': match_score,
                    'reasoning': reasoning,
                    'demographic_fit': self._assess_demographic_fit(user, phone)
                })

        # Sort by match score
        recommendations.sort(key=lambda x: x['match_score'], reverse=True)

        # Save recommendations
        if user_id:
            self._save_recommendations(user_id, recommendations[:top_n])

        return recommendations[:top_n]

    def _build_user_profile(self, user, criteria=None):
        """Build comprehensive user profile"""
        profile = {
            'age_range': user.age_range or '26-35',
            'occupation': user.user_category or 'Working Professional',
            'preferences': UserPreference.query.filter_by(user_id=user.id).first()
        }

        # Get age-based preferences
        age_prefs = self.age_profiles.get(profile['age_range'], self.age_profiles['26-35'])
        profile['age_preferences'] = age_prefs

        # Get occupation-based preferences
        occupation_prefs = self.occupation_profiles.get(
            profile['occupation'],
            self.occupation_profiles['Working Professional']
        )
        profile['occupation_preferences'] = occupation_prefs

        # Override with criteria if provided
        if criteria:
            profile['criteria_override'] = criteria

        return profile

    def _calculate_enhanced_score(self, user_profile, user, phone, phone_specs):
        """
        Calculate enhanced match score considering demographics

        Scoring components:
        - Budget fit: 25%
        - Demographic fit: 20%
        - Specs match: 30%
        - Usage alignment: 15%
        - Feature match: 10%
        """
        score = 0

        # Get preferences
        user_prefs = user_profile.get('preferences')
        age_prefs = user_profile.get('age_preferences', {})
        occ_prefs = user_profile.get('occupation_preferences', {})

        # 1. Budget fit (25 points)
        budget_score = self._score_budget_fit(user_profile, phone)
        score += budget_score * 0.25

        # 2. Demographic fit (20 points)
        demographic_score = self._score_demographic_fit(user, phone, age_prefs, occ_prefs)
        score += demographic_score * 0.20

        # 3. Specs match (30 points)
        if user_prefs and phone_specs:
            specs_score = self._score_specs_match(user_prefs, phone_specs)
            score += specs_score * 0.30

        # 4. Usage alignment (15 points)
        usage_score = self._score_usage_alignment(user_profile, phone_specs)
        score += usage_score * 0.15

        # 5. Feature match (10 points)
        feature_score = self._score_feature_match(age_prefs, occ_prefs, phone_specs)
        score += feature_score * 0.10

        return round(score, 2)

    def _score_budget_fit(self, user_profile, phone):
        """Score based on budget fit"""
        user_prefs = user_profile.get('preferences')
        age_prefs = user_profile.get('age_preferences', {})
        occ_prefs = user_profile.get('occupation_preferences', {})

        # Get budget range
        if user_prefs:
            min_budget = user_prefs.min_budget
            max_budget = user_prefs.max_budget
        else:
            # Use demographic defaults
            max_comfort = age_prefs.get('max_price_comfort', 3000)
            occ_max = occ_prefs.get('max_budget', 3000)
            max_budget = min(max_comfort, occ_max)
            min_budget = 500

        # Perfect fit within budget
        if min_budget <= phone.price <= max_budget:
            return 100

        # Slightly under budget (good value)
        if phone.price < min_budget:
            return 85

        # Over budget - penalize based on how much
        if phone.price > max_budget:
            overage = (phone.price - max_budget) / max_budget
            if overage < 0.2:  # Within 20% over
                return 70
            elif overage < 0.5:  # Within 50% over
                return 40
            else:
                return 20  # Way over budget

        return 50

    def _score_demographic_fit(self, user, phone, age_prefs, occ_prefs):
        """Score based on demographic appropriateness"""
        score = 100

        # Price appropriateness for age group
        max_price_comfort = age_prefs.get('max_price_comfort', 3000)

        if phone.price > max_price_comfort * 1.5:
            score -= 30  # Too expensive for age group
        elif phone.price > max_price_comfort:
            score -= 15  # Slightly expensive

        # Occupation appropriateness
        if user.user_category == 'Student' and phone.price > 2500:
            score -= 20  # Too expensive for students

        if user.user_category == 'Senior Citizen':
            # Prefer phones with better battery and simpler features
            score += 10  # Will be adjusted in feature scoring

        return max(score, 0)

    def _score_specs_match(self, user_prefs, phone_specs):
        """Score based on specification match"""
        score = 0
        max_score = 0

        # RAM match
        max_score += 15
        if phone_specs.ram_options:
            ram_values = parse_memory_values(phone_specs.ram_options)
            if ram_values and max(ram_values) >= user_prefs.min_ram:
                score += 15

        # Storage match
        max_score += 15
        if phone_specs.storage_options:
            storage_values = parse_memory_values(phone_specs.storage_options)
            if storage_values and max(storage_values) >= user_prefs.min_storage:
                score += 15

        # Camera match
        max_score += 20
        if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= user_prefs.min_camera:
            score += 20

        # Battery match
        max_score += 20
        if phone_specs.battery_capacity and phone_specs.battery_capacity >= user_prefs.min_battery:
            score += 20

        # 5G match
        max_score += 15
        if user_prefs.requires_5g:
            if phone_specs.has_5g:
                score += 15
        else:
            score += 15  # No requirement

        # Screen size match
        max_score += 15
        if phone_specs.screen_size:
            if user_prefs.min_screen_size <= phone_specs.screen_size <= user_prefs.max_screen_size:
                score += 15

        return (score / max_score * 100) if max_score > 0 else 0

    def _score_usage_alignment(self, user_profile, phone_specs):
        """Score based on usage pattern alignment"""
        if not phone_specs:
            return 50

        score = 100

        age_prefs = user_profile.get('age_preferences', {})
        priorities = age_prefs.get('priorities', [])

        # Gaming priority
        if 'Gaming' in priorities:
            if phone_specs.refresh_rate and phone_specs.refresh_rate >= 90:
                score += 10
            if phone_specs.ram_options and '12GB' in phone_specs.ram_options:
                score += 10

        # Photography priority
        if 'Camera' in priorities or 'Photography' in priorities:
            if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= 48:
                score += 10

        # Battery priority
        if 'Battery' in priorities:
            if phone_specs.battery_capacity and phone_specs.battery_capacity >= 4500:
                score += 10

        return min(score, 100)

    def _score_feature_match(self, age_prefs, occ_prefs, phone_specs):
        """Score based on recommended features"""
        if not phone_specs:
            return 50

        score = 0
        total_features = 0

        # Combine recommended features
        recommended = age_prefs.get('features', []) + occ_prefs.get('recommended_features', [])

        for feature in recommended:
            total_features += 1

            if '5G' in feature and phone_specs.has_5g:
                score += 1
            elif 'Wireless Charging' in feature and phone_specs.wireless_charging:
                score += 1
            elif 'Fast Charging' in feature and phone_specs.charging_speed:
                if 'fast' in phone_specs.charging_speed.lower() or any(char.isdigit() and int(char) >= 3 for char in phone_specs.charging_speed):
                    score += 1
            elif 'Large Display' in feature or 'Large Screen' in feature:
                if phone_specs.screen_size and phone_specs.screen_size >= 6.5:
                    score += 1
            elif 'Water Resistance' in feature and phone_specs.water_resistance:
                score += 1

        return (score / total_features * 100) if total_features > 0 else 50

    def _generate_smart_reasoning(self, user_profile, user, phone, phone_specs, match_score):
        """Generate intelligent reasoning for recommendation"""
        reasons = []

        age_range = user_profile.get('age_range', '26-35')
        occupation = user_profile.get('occupation', 'Working Professional')

        # Demographic fit reason
        reasons.append(f"Perfect for {occupation}s in the {age_range} age group")

        # Budget reason
        user_prefs = user_profile.get('preferences')
        if user_prefs:
            if user_prefs.min_budget <= phone.price <= user_prefs.max_budget:
                reasons.append(f"Fits your budget of RM {user_prefs.min_budget:,.0f} - RM {user_prefs.max_budget:,.0f}")

        if phone_specs:
            # Key feature highlights
            if phone_specs.rear_camera_main and phone_specs.rear_camera_main >= 48:
                reasons.append(f"Excellent {phone_specs.rear_camera_main}MP camera for photography")

            if phone_specs.battery_capacity and phone_specs.battery_capacity >= 4500:
                reasons.append(f"Long-lasting {phone_specs.battery_capacity}mAh battery")

            if phone_specs.has_5g:
                reasons.append("Future-ready with 5G connectivity")

            if phone_specs.refresh_rate and phone_specs.refresh_rate >= 90:
                reasons.append(f"Smooth {phone_specs.refresh_rate}Hz display")

        return " • ".join(reasons[:4])  # Limit to top 4 reasons

    def _assess_demographic_fit(self, user, phone):
        """Assess how well phone fits user demographics"""
        fit_level = 'Good'

        if user.user_category == 'Student' and phone.price < 2000:
            fit_level = 'Excellent'
        elif user.user_category == 'Working Professional' and 2000 <= phone.price <= 5000:
            fit_level = 'Excellent'
        elif user.user_category == 'Senior Citizen' and phone.price < 2500:
            fit_level = 'Excellent'

        return fit_level

    def _save_recommendations(self, user_id, recommendations):
        """Save recommendations to database"""
        try:
            for rec in recommendations:
                recommendation = Recommendation(
                    user_id=user_id,
                    phone_id=rec['phone'].id,
                    match_percentage=rec['match_score'],
                    reasoning=rec['reasoning']
                )
                db.session.add(recommendation)

            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving recommendations: {e}")


# Integration function for existing code
def get_ai_recommendations(user_id, criteria=None, top_n=5):
    """
    Wrapper function to get AI recommendations

    Usage:
        from app.modules.enhanced_ai_engine import get_ai_recommendations
        recommendations = get_ai_recommendations(user_id, top_n=5)
    """
    engine = EnhancedAIRecommendationEngine()
    return engine.get_smart_recommendations(user_id, criteria, top_n)
