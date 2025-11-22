"""
Enhanced NLU Engine with Machine Learning - FIXED VERSION
Natural Language Understanding for DialSmart chatbot
"""
import re
from typing import Dict, List, Tuple, Optional, Any
from rapidfuzz import fuzz, process
import numpy as np
from datetime import datetime

class NLUEngine:
    """ML-powered Natural Language Understanding Engine"""

    def __init__(self):
        # Brand sentiment mapping
        self.positive_sentiments = [
            'love', 'like', 'prefer', 'want', 'need', 'adore',
            'favorite', 'favourite', 'best', 'good', 'great',
            'excellent', 'amazing', 'fantastic', 'perfect', 'interested in'
        ]

        self.negative_sentiments = [
            'hate', 'dislike', 'don\'t like', 'dont like', 'don\'t love',
            'dont love', 'not like', 'not love', 'avoid', 'exclude',
            'no', 'never', 'reject', 'refuse', 'against', 'opposed to',
            'not interested', 'not want', 'don\'t want', 'dont want'
        ]

        # Brand name mappings (handle variations and keywords)
        self.brand_keywords = {
            'Apple': ['apple', 'iphone', 'ios'],
            'Samsung': ['samsung', 'galaxy'],
            'Xiaomi': ['xiaomi', 'redmi', 'poco', 'mi'],
            'Huawei': ['huawei', 'honor'],
            'Oppo': ['oppo'],
            'Vivo': ['vivo', 'iqoo'],
            'Realme': ['realme'],
            'Google': ['google', 'pixel'],
            'OnePlus': ['oneplus', 'one plus'],
            'Nokia': ['nokia'],
            'Sony': ['sony', 'xperia'],
            'Motorola': ['motorola', 'moto'],
            'Asus': ['asus', 'rog'],
            'Nothing': ['nothing'],
            'Infinix': ['infinix'],
            'Tecno': ['tecno'],
            'Honor': ['honor']
        }

        # Battery-related keywords
        self.battery_keywords = [
            'long lasting', 'long-lasting', 'battery life', 'battery',
            'long battery', 'best battery', 'good battery', 'durable',
            'all day', 'all-day', 'endurance', 'power', 'mah',
            'battery capacity', 'charge', 'charging'
        ]

        # Photography keywords
        self.photography_keywords = [
            'photographer', 'photography', 'camera', 'photo', 'picture',
            'selfie', 'video', 'recording', 'megapixel', 'mp',
            'lens', 'zoom', 'night mode', 'portrait', 'wide angle'
        ]

        # Storage keywords
        self.storage_keywords = [
            'storage', 'gb storage', 'internal storage', 'memory',
            'space', 'large storage', 'big storage'
        ]

        # Intent patterns
        self.intent_patterns = {
            'model_search': [
                r'\b(iphone|galaxy|redmi|poco|pixel|xperia|honor|oppo|vivo|realme|oneplus|nothing|moto)\s+\d+',
                r'\b([a-z]+)\s+\d+\s*(pro|max|ultra|plus|lite|se)?',
            ],
            'multi_model_search': [
                r'and', r'&', r'with', r','
            ],
            'spec_filter': [
                r'above\s+(\d+)\s*(mah|mp|gb)',
                r'over\s+(\d+)\s*(mah|mp|gb)',
                r'more than\s+(\d+)\s*(mah|mp|gb)',
                r'(\d+)\s*(mah|mp|gb)\s+or\s+(more|above|higher)',
                r'at least\s+(\d+)\s*(mah|mp|gb)',
            ]
        }

    def analyze_message(self, message: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Comprehensive message analysis

        Args:
            message: User's message
            context: Conversation context

        Returns:
            Dictionary with extracted entities, intent, and sentiment
        """
        message_lower = message.lower().strip()

        analysis = {
            'original_message': message,
            'brands': {
                'preferred': [],
                'excluded': []
            },
            'models': [],
            'specs': {
                'battery_min': None,
                'camera_min': None,
                'ram_min': None,
                'storage_min': None,
                'other': []
            },
            'budget': None,
            'usage_type': None,
            'intent': 'general',
            'is_multi_brand_query': False,
            'is_multi_model_query': False,
            'requires_battery_focus': False,
            'requires_camera_focus': False,
            'fuzzy_model_matches': [],
            'context_continuation': False,
            'is_simple_brand_query': False,
            'has_explicit_sentiment': False
        }

        # Check for context continuation
        if context and context.get('last_intent'):
            analysis['context_continuation'] = self._detect_context_continuation(
                message_lower, context
            )

        # Extract brand preferences with sentiment
        brand_analysis = self._extract_brand_preferences(message_lower)
        analysis['brands'] = brand_analysis
        analysis['is_multi_brand_query'] = len(brand_analysis['preferred']) > 1

        # Check if this is a simple brand-only query (no specs, just brand name)
        analysis['is_simple_brand_query'] = self._is_simple_brand_query(message_lower, brand_analysis)

        # Check if message has explicit sentiment (love/hate)
        analysis['has_explicit_sentiment'] = self._has_explicit_sentiment(message_lower)

        # Extract model names (exact and fuzzy)
        models = self._extract_model_names(message_lower)
        analysis['models'] = models
        analysis['is_multi_model_query'] = len(models) > 1 or ' and ' in message_lower or ' & ' in message_lower

        # Extract specifications
        specs = self._extract_specifications(message_lower)
        analysis['specs'] = specs

        # Extract budget
        budget = self._extract_budget(message_lower)
        analysis['budget'] = budget

        # Detect usage type
        usage_type = self._detect_usage_type(message_lower)
        analysis['usage_type'] = usage_type

        # Detect special focus
        analysis['requires_battery_focus'] = self._detect_battery_focus(message_lower)
        analysis['requires_camera_focus'] = self._detect_camera_focus(message_lower)

        # Determine intent
        intent = self._determine_intent(message_lower, analysis)
        analysis['intent'] = intent

        return analysis

    def _is_simple_brand_query(self, message: str, brand_analysis: Dict) -> bool:
        """Check if message is just a brand name without other criteria"""
        # Check if message is just a brand keyword
        for brand_keywords in self.brand_keywords.values():
            for keyword in brand_keywords:
                # Message is just the keyword or keyword + s
                if message.strip() in [keyword, keyword + 's', keyword + ' phone', keyword + ' phones']:
                    return True

        # Check if message is only brand names without specs
        if brand_analysis['preferred']:
            # Remove brand keywords from message
            clean_msg = message
            for brand, keywords in self.brand_keywords.items():
                for keyword in keywords:
                    clean_msg = clean_msg.replace(keyword, '')

            # If what's left is just whitespace or common words
            remaining = clean_msg.strip()
            common_words = ['phone', 'phones', 'and', 'the', 'a', 'an']
            remaining_words = [w for w in remaining.split() if w not in common_words]

            if not remaining_words:
                return True

        return False

    def _has_explicit_sentiment(self, message: str) -> bool:
        """Check if message contains explicit sentiment words"""
        for sentiment in self.positive_sentiments + self.negative_sentiments:
            if sentiment in message:
                return True
        return False

    def _extract_brand_preferences(self, message: str) -> Dict[str, List[str]]:
        """Extract brand preferences with sentiment analysis"""
        preferences = {
            'preferred': [],
            'excluded': []
        }

        # Analyze each brand
        for brand, keywords in self.brand_keywords.items():
            for keyword in keywords:
                if keyword in message:
                    # Check sentiment around the brand mention
                    sentiment = self._analyze_brand_sentiment(message, keyword)

                    if sentiment == 'positive':
                        if brand not in preferences['preferred']:
                            preferences['preferred'].append(brand)
                    elif sentiment == 'negative':
                        if brand not in preferences['excluded']:
                            preferences['excluded'].append(brand)
                    else:  # neutral - treat as preferred if mentioned
                        if brand not in preferences['preferred'] and brand not in preferences['excluded']:
                            preferences['preferred'].append(brand)

        return preferences

    def _analyze_brand_sentiment(self, message: str, brand_keyword: str) -> str:
        """Analyze sentiment around a brand mention"""
        # Find the position of the brand keyword
        pattern = r'\b' + re.escape(brand_keyword) + r'\b'
        match = re.search(pattern, message)

        if not match:
            return 'neutral'

        pos = match.start()

        # Get context window (words before and after)
        before = message[:pos].split()[-5:] if pos > 0 else []
        after = message[pos:].split()[:5]

        context = ' '.join(before + after).lower()

        # Check for negative sentiment
        for neg_word in self.negative_sentiments:
            if neg_word in context:
                return 'negative'

        # Check for positive sentiment
        for pos_word in self.positive_sentiments:
            if pos_word in context:
                return 'positive'

        # Check for negation patterns
        negation_patterns = [
            r'(don\'t|dont|do not|never|not)\s+\w+\s+' + re.escape(brand_keyword),
            r'(hate|dislike)\s+' + re.escape(brand_keyword),
            r'no\s+' + re.escape(brand_keyword)
        ]

        for pattern in negation_patterns:
            if re.search(pattern, message):
                return 'negative'

        # Check for positive patterns
        positive_patterns = [
            r'(love|like|prefer|want)\s+' + re.escape(brand_keyword),
            r'(love|like|prefer|want)\s+\w+\s+' + re.escape(brand_keyword),
            re.escape(brand_keyword) + r'\s+(is|are)?\s*(good|great|best|amazing)'
        ]

        for pattern in positive_patterns:
            if re.search(pattern, message):
                return 'positive'

        return 'neutral'

    def _extract_model_names(self, message: str) -> List[Dict[str, Any]]:
        """Extract phone model names from message - FIXED VERSION"""
        models = []

        # FIXED: Better patterns that don't split digits
        patterns = [
            # Pattern 1: brand + number + optional suffix (e.g., "iphone 17 pro", "redmi 14 pro")
            r'\b(iphone|galaxy|redmi|poco|pixel|xperia|honor|oppo|vivo|iqoo|realme|oneplus|nothing|moto|mi)\s+(\d+[a-z]?)\s*(pro\s*max|pro\s*plus|pro|max|ultra|plus|lite|se|c|x|t|s|note|mix|fold|flip|air)?\b',

            # Pattern 2: brand + word + number + suffix (e.g., "samsung galaxy s23", "xiaomi mix 4")
            # FIXED: Use [a-zA-Z]+ instead of \w+ to not match digits
            r'\b(xiaomi|samsung|apple|huawei|google|sony|nokia|motorola|asus)\s+([a-zA-Z]+)\s+(\d+[a-z]?)\s*(pro\s*max|pro\s*plus|pro|max|ultra|plus|lite|se|air)?\b',

            # Pattern 3: Just brand + number for Xiaomi (e.g., "xiaomi 17")
            r'\b(xiaomi)\s+(\d+)\s*(pro\s*max|pro\s*plus|pro|max|ultra|plus|lite|se|air)?\b',
        ]

        seen_models = set()

        for pattern in patterns:
            matches = re.finditer(pattern, message, re.IGNORECASE)
            for match in matches:
                groups = match.groups()
                # Join all captured groups
                model_text = ' '.join([g for g in groups if g]).strip()

                # Avoid duplicates
                model_key = model_text.lower()
                if model_key not in seen_models:
                    seen_models.add(model_key)
                    models.append({
                        'text': model_text,
                        'match_type': 'exact'
                    })

        return models

    def _extract_specifications(self, message: str) -> Dict[str, Any]:
        """Extract technical specifications from message"""
        specs = {
            'battery_min': None,
            'camera_min': None,
            'ram_min': None,
            'storage_min': None,
            'other': []
        }

        # Battery (mAh)
        battery_patterns = [
            r'above\s+(\d+)\s*mah',
            r'over\s+(\d+)\s*mah',
            r'(\d+)\s*mah\s+or\s+(more|above|higher)',
            r'at least\s+(\d+)\s*mah',
            r'more than\s+(\d+)\s*mah',
            r'(\d+)\+\s*mah',
        ]

        for pattern in battery_patterns:
            match = re.search(pattern, message)
            if match:
                specs['battery_min'] = int(match.group(1))
                break

        # Camera (MP)
        camera_patterns = [
            r'above\s+(\d+)\s*mp',
            r'over\s+(\d+)\s*mp',
            r'(\d+)\s*mp\s+or\s+(more|above|higher)',
            r'at least\s+(\d+)\s*mp',
            r'more than\s+(\d+)\s*mp',
            r'(\d+)\+\s*mp',
            r'camera.*?(\d+)\s*mp',
        ]

        for pattern in camera_patterns:
            match = re.search(pattern, message)
            if match:
                specs['camera_min'] = int(match.group(1))
                break

        # RAM
        ram_patterns = [
            r'(\d+)\s*gb\s+ram',
            r'ram\s+(\d+)\s*gb',
            r'at least\s+(\d+)\s*gb\s+ram',
        ]

        for pattern in ram_patterns:
            match = re.search(pattern, message)
            if match:
                specs['ram_min'] = int(match.group(1))
                break

        # Storage
        storage_patterns = [
            r'(\d+)\s*gb\s+storage',
            r'storage\s+(\d+)\s*gb',
            r'at least\s+(\d+)\s*gb\s+storage',
        ]

        for pattern in storage_patterns:
            match = re.search(pattern, message)
            if match:
                specs['storage_min'] = int(match.group(1))
                break

        # 5G
        if '5g' in message:
            specs['other'].append('5g')

        return specs

    def _extract_budget(self, message: str) -> Optional[Tuple[float, float]]:
        """Extract budget range from message"""
        # Look for patterns like "RM1000", "1000", "under 2000", "within 5000"
        patterns = [
            r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
            r'rm\s*(\d+)\s*-\s*rm\s*(\d+)',  # RM1000-RM2000
            r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000
            r'between\s+rm?\s*(\d+)\s+and\s+rm?\s*(\d+)',  # between 1000 and 2000
            r'under\s+rm?\s*(\d+)',  # under RM2000
            r'below\s+rm?\s*(\d+)',  # below 2000
            r'within\s+rm?\s*(\d+)',  # within 5000
            r'rm\s*(\d+)',  # RM2000
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                if 'under' in message.lower() or 'below' in message.lower():
                    max_budget = int(match.group(1))
                    return (100, max_budget)
                elif 'within' in message.lower():
                    # "within 5000" typically means up to that amount
                    max_budget = int(match.group(1))
                    return (100, max_budget)
                elif len(match.groups()) == 2:
                    return (int(match.group(1)), int(match.group(2)))
                else:
                    # Single value mentioned
                    value = int(match.group(1))
                    # If value is small (< 100), might be in hundreds
                    if value < 100:
                        return (100, value * 1000)
                    return (100, value)

        return None

    def _detect_usage_type(self, message: str) -> Optional[str]:
        """Detect intended usage type"""
        usage_mapping = {
            'Gaming': ['gam', 'game', 'gaming', 'play', 'player'],
            'Photography': ['photo', 'camera', 'picture', 'selfie', 'photographer', 'photography'],
            'Business': ['business', 'work', 'office', 'professional', 'productivity'],
            'Entertainment': ['entertainment', 'video', 'movie', 'media', 'streaming', 'youtube', 'netflix'],
            'Social Media': ['social', 'facebook', 'instagram', 'tiktok', 'whatsapp']
        }

        for usage, keywords in usage_mapping.items():
            for keyword in keywords:
                if keyword in message:
                    return usage

        return None

    def _detect_battery_focus(self, message: str) -> bool:
        """Detect if battery/longevity is a priority"""
        for keyword in self.battery_keywords:
            if keyword in message:
                return True
        return False

    def _detect_camera_focus(self, message: str) -> bool:
        """Detect if camera/photography is a priority"""
        for keyword in self.photography_keywords:
            if keyword in message:
                return True
        return False

    def _detect_context_continuation(self, message: str, context: Dict) -> bool:
        """Detect if this message continues from previous context"""
        # Simple brand-only queries that should use context
        simple_brand_only = False

        # Check if message is just a brand name or simple request
        for brand_keywords in self.brand_keywords.values():
            for keyword in brand_keywords:
                if message.strip() == keyword or message.strip() == keyword + 's':
                    simple_brand_only = True
                    break

        # If previous context had specific filters and current message is simple
        if simple_brand_only and context.get('last_specs'):
            return True

        # If previous context had battery focus and current is brand-only
        if simple_brand_only and context.get('battery_focus'):
            return True

        # If previous context had camera focus and current is brand-only
        if simple_brand_only and context.get('camera_focus'):
            return True

        return False

    def _determine_intent(self, message: str, analysis: Dict) -> str:
        """Determine the primary intent"""
        # Model search
        if analysis['models']:
            if analysis['is_multi_model_query']:
                return 'multi_model_search'
            return 'model_search'

        # Spec-based filtering
        if any([
            analysis['specs']['battery_min'],
            analysis['specs']['camera_min'],
            analysis['specs']['ram_min'],
            analysis['specs']['storage_min']
        ]):
            return 'spec_filter'

        # Usage-based
        if analysis['usage_type']:
            return 'usage_recommendation'

        # Battery focus
        if analysis['requires_battery_focus']:
            return 'battery_focused'

        # Camera focus
        if analysis['requires_camera_focus']:
            return 'camera_focused'

        # Brand query
        if analysis['brands']['preferred'] or analysis['brands']['excluded']:
            return 'brand_query'

        # Budget query
        if analysis['budget']:
            return 'budget_query'

        # Greeting
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'greetings']
        if any(kw in message for kw in greeting_keywords):
            return 'greeting'

        # Help
        help_keywords = ['help', 'how', 'what can you do']
        if any(kw in message for kw in help_keywords):
            return 'help'

        # Comparison
        if ' vs ' in message or ' versus ' in message or 'compare' in message:
            return 'comparison'

        return 'general'

    def fuzzy_match_model(self, query: str, available_models: List[str], threshold: int = 70) -> List[Dict[str, Any]]:
        """
        Fuzzy match a model query against available models

        Args:
            query: User's model query
            available_models: List of available model names
            threshold: Minimum match score (0-100)

        Returns:
            List of matches with scores
        """
        matches = process.extract(query, available_models, scorer=fuzz.token_sort_ratio, limit=10)

        results = []
        for match_text, score in matches:
            if score >= threshold:
                results.append({
                    'model': match_text,
                    'score': score,
                    'match_type': 'fuzzy'
                })

        return results
