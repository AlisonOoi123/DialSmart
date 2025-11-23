"""
Chatbot Engine
NLP-powered conversational assistant for phone recommendations
"""
from app import db
from app.models import ChatHistory, Phone, Brand, PhoneSpecification
from app.modules.ai_engine import AIRecommendationEngine
import re
import json
from datetime import datetime, timedelta

class ChatbotEngine:
    """Conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.session_context = {}
        self.intents = {
            'greeting': [
                'hello', 'hi', 'hey', 'good morning', 'good afternoon', 
                'good evening', 'greetings', 'hola', 'yo', 'sup',
                'whats up', "what's up", 'howdy', 'hiya'
            ],
            
            'budget_query': [
                # Price terms
                'budget', 'price', 'cost', 'cheap', 'affordable', 'expensive',
                'pricing', 'rate', 'value', 'worth', 'spend',
                # Currency
                'rm', 'ringgit', 'dollar', 'usd', 'sgd', 'myr',
                # Range terms
                'within', 'under', 'below', 'above', 'over', 'near',
                'around', 'between', 'from', 'to',
                # Limits
                'max', 'maximum', 'min', 'minimum', 'limit', 'cap',
                # Value terms
                'value for money', 'vfm', 'bang for buck', 'best price',
                'good deal', 'bargain', 'discount', 'sale', 'offer',
                'promotion', 'promo', 'clearance'
            ],
            
            'recommendation': [
                'recommend', 'suggestion', 'suggest', 'advice', 'advise',
                'find', 'search', 'looking for', 'looking to buy',
                'need', 'want', 'i want', 'i need', 'help me find',
                'show me', 'can you show', 'which phone',
                'best', 'top', 'good', 'great', 'excellent',
                'should i buy', 'should i get', 'what to buy',
                'help me choose', 'help me pick', 'help me select'
            ],
            
            'comparison': [
                'compare', 'comparison', 'difference', 'different',
                'vs', 'versus', 'or', 'better', 'best',
                'which is better', 'which one', 'prefer', 'choose between',
                'decide between', 'pick between', 'a or b',
                'pros and cons', 'advantage', 'disadvantage'
            ],
            
            'specification': [
                # General
                'specs', 'specification', 'specifications', 'features',
                'details', 'tech specs', 'full specs',
                # Display
                'camera', 'battery', 'ram', 'storage', 'screen', 'display',
                'processor', 'cpu', 'gpu', 'chipset',
                # Camera specific
                'megapixel', 'mp', 'front camera', 'rear camera',
                'selfie', 'photo quality', 'video recording',
                'night mode', 'portrait', 'zoom', 'lens',
                # Battery specific
                'mah', 'battery life', 'charging', 'fast charging',
                'wireless charging', 'battery capacity',
                # Performance
                'performance', 'speed', 'benchmark', 'antutu',
                'gaming performance', 'multitasking',
                # Display specific
                'refresh rate', '90hz', '120hz', '144hz',
                'resolution', 'oled', 'amoled', 'lcd',
                # Connectivity
                '5g', '4g', 'wifi', 'bluetooth', 'nfc',
                # Build
                'build quality', 'design', 'weight', 'dimensions'
            ],
            
            'brand_query': [
                # General brand terms
                'brand', 'manufacturer', 'company', 'make',
                # All brands (from brand_keywords_map)
                'samsung', 'galaxy', 'apple', 'iphone', 'xiaomi',
                'huawei', 'honor', 'oppo', 'vivo', 'realme',
                'google', 'pixel', 'asus', 'rog', 'infinix',
                'poco', 'redmi', 'oneplus', 'motorola', 'moto',
                'nokia', 'sony', 'xperia', 'nothing', 'tecno'
            ],
            
            'help': [
                'help', 'how', 'what can you do', 'what do you do',
                'how to use', 'how does this work', 'guide',
                'assist', 'assistance', 'support', 'tutorial',
                'explain', 'tell me about', 'information'
            ],
            
            'usage_type': [
                # Gaming
                'gaming', 'game', 'gamer', 'mobile gaming',
                'pubg', 'cod', 'free fire', 'mobile legends',
                'esports', 'gaming phone',
                # Photography
                'photography', 'photographer', 'photo', 'picture',
                'camera phone', 'best camera', 'vlogging', 'content creation',
                'instagram', 'tiktok', 'youtube',
                # Business/Work
                'business', 'work', 'office', 'professional',
                'productivity', 'email', 'video call', 'zoom',
                'teams', 'conference',
                # Entertainment
                'social media', 'entertainment', 'streaming',
                'netflix', 'youtube', 'video', 'music',
                'multimedia', 'media consumption',
                # General usage
                'daily use', 'everyday use', 'casual use',
                'basic use', 'browsing', 'calling', 'messaging'
            ],
            
            'timeline': [
                # Latest
                'latest', 'newest', 'new', 'recent', 'recently released',
                'just launched', 'just released', 'brand new',
                # Specific years
                'released', 'from 2024', 'from 2023', 'from 2025',
                'year 2024', 'year 2023', 'year 2025',
                '2024 phone', '2023 phone', '2025 phone',
                # Relative time
                'last year', 'last month', 'this year', 'this month',
                'past year', 'past month', 'recent months',
                # Upcoming
                'upcoming', 'coming soon', 'future', 'next month',
                'next year', 'to be released', 'pre-order',
                # Combined
                'cheapest new', 'latest budget', 'newest flagship'
            ],
            
            # NEW INTENT CATEGORIES
            
            'purchase_intent': [
                'buy', 'purchase', 'get', 'order', 'shopping',
                'where to buy', 'how to buy', 'available',
                'in stock', 'out of stock', 'pre-order',
                'shop', 'store', 'retail', 'online'
            ],
            
            'color_preference': [
                'color', 'colour', 'black', 'white', 'blue',
                'red', 'green', 'purple', 'silver', 'gold',
                'pink', 'yellow', 'gray', 'grey', 'rose',
                'midnight', 'starlight', 'graphite', 'sierra blue'
            ],
            
            'condition': [
                'new', 'brand new', 'sealed', 'original',
                'used', 'second hand', 'refurbished', 'pre-owned',
                'like new', 'open box', 'reconditioned'
            ],
            
            'size_preference': [
                'small', 'compact', 'mini', 'pocket size',
                'large', 'big', 'big screen', 'large display',
                'medium', 'standard size', 'normal size',
                'lightweight', 'heavy', 'portable'
            ],
            
            'urgency': [
                'urgent', 'asap', 'immediately', 'right now',
                'today', 'this week', 'soon', 'quickly',
                'fast delivery', 'quick'
            ]
        }

        # EXPANDED FEATURE KEYWORDS
        self.feature_keywords = {
            'battery': [
                'battery', 'long lasting', 'battery life', 'long battery',
                'all day battery', 'mah', 'battery capacity',
                'power', 'endurance', 'standby time', 'screen on time',
                'battery drain', 'battery backup', 'battery performance',
                '5000mah', '6000mah', 'big battery', 'huge battery'
            ],
            
            'camera': [
                'camera', 'photo', 'photography', 'photographer',
                'selfie', 'picture', 'image quality', 'photo quality',
                'megapixel', 'mp', '50mp', '64mp', '108mp', '200mp',
                'front camera', 'rear camera', 'main camera',
                'ultra wide', 'telephoto', 'macro', 'depth',
                'night mode', 'portrait', 'zoom', 'optical zoom',
                'video recording', '4k video', '8k video',
                'slow motion', 'time lapse', 'pro mode',
                'ai camera', 'ois', 'image stabilization'
            ],
            
            'display': [
                'display', 'screen', 'amoled', 'oled', 'lcd',
                'super amoled', 'retina', 'ips',
                'screen size', 'big screen', 'large display',
                '6.5 inch', '6.7 inch', 'inch display',
                'resolution', 'full hd', 'quad hd', '4k display',
                'brightness', 'outdoor visibility', 'sunlight',
                'gorilla glass', 'screen protection',
                'curved display', 'flat screen', 'edge screen',
                'notch', 'punch hole', 'under display'
            ],
            
            'performance': [
                'fast', 'processor', 'cpu', 'performance', 'speed',
                'powerful', 'snapdragon', 'flagship', 'chipset',
                'dimensity', 'exynos', 'bionic', 'tensor',
                'benchmark', 'antutu', 'geekbench', 'smooth',
                'lag free', 'no lag', 'smooth performance',
                'multitasking', 'app switching', 'loading speed',
                'gaming performance', 'graphics', 'gpu',
                'heating', 'thermal', 'cooling', 'temperature'
            ],
            
            '5g': [
                '5g', '5g support', '5g network', '5g connectivity',
                '5g enabled', '5g phone', 'dual 5g', 'sa nsa',
                'network speed', 'fast internet'
            ],
            
            'storage': [
                'storage', 'memory', 'gb storage', 'space',
                'internal storage', 'rom', '64gb', '128gb',
                '256gb', '512gb', '1tb', 'expandable storage',
                'sd card', 'micro sd', 'storage expansion',
                'ufs', 'storage speed'
            ],
            
            'ram': [
                'ram', 'memory', 'gb ram', '4gb', '6gb', '8gb',
                '12gb', '16gb', 'lpddr', 'multitasking',
                'app memory', 'virtual ram', 'ram expansion'
            ],
            
            'charging': [
                'charging', 'fast charging', 'quick charge',
                'rapid charge', 'super vooc', 'warp charge',
                'turbo charge', 'hypercharge', 'flash charge',
                'wireless charging', 'reverse charging',
                '15w', '18w', '25w', '33w', '45w', '65w',
                '120w', '150w', 'charging speed',
                'charger', 'charging cable', 'usb-c'
            ],
            
            'design': [
                'design', 'build quality', 'premium', 'looks',
                'aesthetics', 'beautiful', 'stylish', 'elegant',
                'sleek', 'modern', 'minimalist', 'color',
                'finish', 'matte', 'glossy', 'glass back',
                'metal frame', 'plastic', 'weight', 'slim',
                'thin', 'compact', 'ergonomic', 'grip'
            ],
            
            'security': [
                'fingerprint', 'face unlock', 'face id',
                'biometric', 'security', 'in-display fingerprint',
                'side fingerprint', 'rear fingerprint',
                'unlock speed', 'secure', 'privacy'
            ],
            
            'audio': [
                'speaker', 'audio', 'sound', 'sound quality',
                'stereo speaker', 'dual speaker', 'loud',
                'dolby atmos', 'headphone jack', '3.5mm',
                'audio jack', 'call quality', 'microphone'
            ],
            
            'durability': [
                'durable', 'durability', 'water resistant',
                'waterproof', 'ip67', 'ip68', 'ip rating',
                'dust proof', 'splash proof', 'rugged',
                'drop test', 'gorilla glass', 'protection'
            ],

            'timeline': [
                # Latest/Newest keywords
                'latest', 'newest', 'new', 'recent', 'recently released',
                'just launched', 'just released', 'brand new',
                'most recent', 'recently launched', 'new release',
                'new model', 'latest model', 'newest model',
                # Specific years
                'released', 'from 2024', 'from 2023', 'from 2025',
                'year 2024', 'year 2023', 'year 2025',
                '2024 phone', '2023 phone', '2025 phone',
                # Relative time
                'last year', 'last month', 'this year', 'this month',
                'past year', 'past month', 'recent months',
                'last 6 months', 'last 12 months', 'past 6 months',
                # Upcoming
                'upcoming', 'coming soon', 'future', 'next month',
                'next year', 'to be released', 'pre-order',
                # Combined timeline + other features
                'cheapest new', 'latest budget', 'newest flagship',
                'latest phones', 'newest phones', 'recent phones'
            ]
        }

        # EXPANDED USER CATEGORIES
        self.user_categories = {
            'senior': [
                'senior', 'elderly', 'senior citizen', 'old age',
                'old people', 'retiree', 'retired', 'grandparent',
                'grandma', 'grandpa', 'older person', 'aged',
                'pension', 'senior friendly', 'easy to use',
                'simple phone', 'basic phone', 'large font',
                'loud speaker', 'hearing aid compatible'
            ],
            
            'student': [
                'student', 'college', 'university', 'school',
                'teen', 'teenager', 'young', 'youth',
                'studying', 'education', 'campus', 'dorm',
                'undergrad', 'graduate', 'high school',
                'budget student', 'affordable for student'
            ],
            
            'professional': [
                'professional', 'business', 'work', 'office',
                'worker', 'working', 'employee', 'businessman',
                'businesswoman', 'corporate', 'executive',
                'manager', 'entrepreneur', 'freelancer',
                'work from home', 'remote work', 'productivity'
            ],
            
            'gamer': [
                'gamer', 'gaming', 'mobile gamer', 'esports',
                'competitive gaming', 'pro gamer', 'streamer',
                'pubg player', 'cod player', 'mobile legends',
                'gaming enthusiast'
            ],
            
            'content_creator': [
                'content creator', 'vlogger', 'youtuber',
                'influencer', 'tiktoker', 'instagrammer',
                'blogger', 'videographer', 'photographer',
                'social media', 'streaming', 'live stream'
            ],
            
            'parent': [
                'parent', 'mom', 'dad', 'mother', 'father',
                'family', 'kids', 'children', 'for my child',
                'for my son', 'for my daughter', 'family phone'
            ]
        }

        # User category keywords
        self.user_categories = {
            'senior': ['senior', 'elderly', 'senior citizen', 'old age', 'old people', 'retiree'],
            'student': ['student', 'college', 'university', 'school', 'teen', 'teenager', 'young'],
            'professional': ['professional', 'business', 'work', 'office', 'worker', 'working', 'employee', 'businessman'],
        }

    def process_message(self, user_id, message, session_id=None):
        """
        Process user message and generate response

        Args:
            user_id: User ID
            message: User's message text
            session_id: Optional session ID for conversation grouping

        Returns:
            Dictionary with response and metadata
        """

         # Use user_id as session key if session_id not provided
        context_key = session_id or f"user_{user_id}"

        # Initialize context for this session if not exists
        if context_key not in self.session_context:
            self.session_context[context_key] = {
                'wanted_brands': [],
                'unwanted_brands': [],
                'last_budget': None,
                'last_features': [],     # Track features like 'battery', 'camera'
                'last_usage': None,      # Track usage like 'Gaming', 'Photography'
                'last_query_type': None  # Track query type like 'cheapest', 'gaming', etc.
            }

        # Check if this is a fresh query (should clear old context)
        is_fresh = self._is_fresh_query(message)

        # Extract brand preferences from current message
        wanted, unwanted = self._extract_brands_with_preferences(message)

        message_words = message.lower().strip().split()
        all_brand_keywords = ['apple', 'iphone', 'samsung', 'galaxy', 'xiaomi', 'vivo', 'oppo',
                            'huawei', 'honor', 'realme', 'redmi', 'poco', 'google', 'pixel']
        is_brand_only = len(message_words) <= 3 and all(word in all_brand_keywords for word in message_words)

        # Clear old context if this is a fresh query with strong preferences
        if is_fresh and (wanted or unwanted):
            self.session_context[context_key]['wanted_brands'] = []
            self.session_context[context_key]['unwanted_brands'] = []

        # Update session context with brand preferences
        if wanted:
            if is_fresh or is_brand_only:
                # REPLACE: Clear previous brands (for fresh queries or brand-only queries)
                self.session_context[context_key]['wanted_brands'] = wanted.copy()
                if is_brand_only:
                    self.session_context[context_key]['last_features'] = []
                    self.session_context[context_key]['last_usage'] = None
            else:
                # ADD: Merge with previous brands (only for refinement queries)
                for brand in wanted:
                    if brand not in self.session_context[context_key]['wanted_brands']:
                        self.session_context[context_key]['wanted_brands'].append(brand)

            # Remove from unwanted
            for brand in wanted:
                if brand in self.session_context[context_key]['unwanted_brands']:
                    self.session_context[context_key]['unwanted_brands'].remove(brand)

        if unwanted:
            if is_fresh:
                # REPLACE: For fresh queries, replace unwanted brands
                self.session_context[context_key]['unwanted_brands'] = unwanted.copy()
            else:
                # ADD: For refinement queries, add to existing unwanted brands
                for brand in unwanted:
                    if brand not in self.session_context[context_key]['unwanted_brands']:
                        self.session_context[context_key]['unwanted_brands'].append(brand)

            # Remove from wanted if it was there
            for brand in unwanted:
                if brand in self.session_context[context_key]['wanted_brands']:
                    self.session_context[context_key]['wanted_brands'].remove(brand)

        # CRITICAL FIX: Reject pure negative statements without actual phone request
        # Examples: "i hate samsung", "i don't like apple", "not xiaomi"
        # These should prompt user to specify what they DO want, not show random phones
        if unwanted and not wanted:
            # Check if this is ONLY a negative statement (no budget, no features, no usage)
            has_budget = self._extract_budget(message) is not None
            has_features = len(self._detect_feature_priority(message)) > 0
            has_usage = self._detect_usage_type(message) is not None

            # If it's a pure negative statement with NO other phone request
            if not has_budget and not has_features and not has_usage:
                # Check if message has any phone request keywords
                request_keywords = ['recommend', 'suggest', 'find', 'show', 'want', 'need',
                                   'looking for', 'phone', 'best', 'good', 'budget']
                has_request = any(keyword in message.lower() for keyword in request_keywords)

                # Pure negative statement without request - reject it
                if not has_request or message.lower().strip() in ['i hate ' + b.lower() for b in unwanted]:
                    return {
                        'response': "I'm DialSmart AI Assistant, and I specialize in helping you find the perfect smartphone! 📱\n\nI can assist you with:\n• Phone recommendations based on your needs\n• Budget-friendly options\n• Brand comparisons\n• Phone specifications\n• Phones for gaming, photography, business, etc.\n\nWhat kind of phone are you looking for today?",
                        'type': 'text',
                        'quick_replies': ['Find a phone under RM2000', 'Gaming phones', 'Best camera phones', 'Show popular brands']
                    }

        # Extract and store features from current message
        features = self._detect_feature_priority(message)

        # CRITICAL FIX: Check if this is a fresh recommendation query
        # Fresh queries like "recommend latest phone" should REPLACE old features/brands, not accumulate
        is_recommendation_query = any(word in message.lower() for word in ['recommend', 'suggest', 'find', 'show', 'latest', 'newest', 'best'])

        # Check if brands are explicitly mentioned in current message
        current_brands = self._extract_multiple_brands(message)

        if features:
            if is_recommendation_query:
                # REPLACE: For fresh recommendation queries, clear old features
                self.session_context[context_key]['last_features'] = features
                # ALSO clear brands if not explicitly mentioned (e.g., "recommend latest phone" shouldn't use old brands)
                if not current_brands:
                    self.session_context[context_key]['wanted_brands'] = []
                    self.session_context[context_key]['unwanted_brands'] = []
            else:
                # ACCUMULATE: For refinement queries, merge with existing features
                for feature in features:
                    if feature not in self.session_context[context_key]['last_features']:
                        self.session_context[context_key]['last_features'].append(feature)

        # Extract and store usage from current message
        usage = self._detect_usage_type(message)
        if usage:
            self.session_context[context_key]['last_usage'] = usage

        # Detect intent
        intent = self._detect_intent(message.lower())

        response_data = self._generate_response(user_id, message, intent, context_key)

        # Update session context with any extracted information
        budget = self._extract_budget(message)
        if budget:
            self.session_context[context_key]['last_budget'] = budget

        brands = self._extract_multiple_brands(message)
        if brands:
            self.session_context[context_key]['last_brands'] = brands

        # Save to chat history
        self._save_chat_history(
            user_id=user_id,
            message=message,
            response=response_data['response'],
            intent=intent,
            session_id=session_id,
            metadata=response_data.get('metadata', {})
        )

        return response_data

    def _detect_intent(self, message):
        """Detect user intent from message"""
        message_lower = message.lower()

        # Special check: If user category is mentioned, treat as recommendation
        user_category = self._detect_user_category(message_lower)
        if user_category:
            return 'recommendation'

        # Special check: If usage type (photography, gaming, etc.) is mentioned, prioritize it over budget
        usage_type = self._detect_usage_type(message_lower)
        if usage_type:
            return 'recommendation'

        # CRITICAL FIX: If brands are mentioned, treat as recommendation/brand query
        # This handles queries like "samsung", "i like samsung", "show me vivo phones"
        brands = self._extract_multiple_brands(message_lower)
        if brands:
            # Check if this is a brand preference statement
            # CRITICAL FIX: Use word boundaries to avoid false matches
            # Example: "note" shouldn't match preference keyword "not"
            import re
            brand_preference_keywords = ['like', 'love', 'prefer', 'want', 'hate', 'dislike', 'not', 'only']
            has_preference = any(
                re.search(r'\b' + re.escape(keyword) + r'\b', message_lower)
                for keyword in brand_preference_keywords
            )
            if has_preference:
                return 'recommendation'
            # Simple brand mention (e.g., "samsung", "show me samsung")
            elif len(message_lower.split()) <= 5:  # Short query, likely brand-only
                # CRITICAL FIX: Check for model indicators before classifying as generic brand query
                # Model indicators: numbers (e.g., "14", "12"), or model keywords (e.g., "note", "pro", "ultra")
                # Examples:
                #   - "redmi note 14" → HAS model indicators → NOT generic brand query
                #   - "samsung" → NO model indicators → generic brand query
                #   - "vivo phone" → NO model indicators → generic brand query
                import re
                has_number = bool(re.search(r'\d+', message_lower))
                model_keywords = ['note', 'pro', 'ultra', 'max', 'plus', 'lite', 'mini', 'air',
                                 'fold', 'flip', 'edge', 'play', 'magic', 'nova', 'enjoy',
                                 'reno', 'find', 'narzo', 'neo', 'hot', 'rog', 'zenfone',
                                 'galaxy', 'pixel', 'iphone', 'mate', 'pura', 'mix', 'civi']
                has_model_keyword = any(keyword in message_lower for keyword in model_keywords)

                # Only classify as generic recommendation if NO model indicators
                if not has_number and not has_model_keyword:
                    return 'recommendation'
                # Has model indicators → let it fall through to phone model extraction

        # Check each intent with word boundary matching to avoid false matches
        # (e.g., "hi" shouldn't match "within")
        # Priority order matters! More specific intents should be checked first
        priority_intents = ['greeting', 'recommendation', 'comparison', 'specification', 'usage_type', 'budget_query', 'brand_query', 'help']

        for intent_name in priority_intents:
            if intent_name not in self.intents:
                continue
            keywords = self.intents[intent_name]
            for keyword in keywords:
                # Use word boundaries for single words, direct match for phrases
                if ' ' in keyword:
                    # Multi-word phrase - direct substring match
                    if keyword in message_lower:
                        return intent_name
                else:
                    # Single word - use word boundary regex
                    import re
                    pattern = r'\b' + re.escape(keyword) + r'\b'
                    if re.search(pattern, message_lower):
                        return intent_name

        return 'general'

    def _generate_response(self, user_id, message, intent, context_key):
        """Generate appropriate response based on intent"""

        # CRITICAL FIX: Check for greeting FIRST before any phone model extraction
        if intent == 'greeting':
            return {
                'response': "Hello! I'm DialSmart AI Assistant. I'm here to help you find the perfect smartphone. How can I assist you today?",
                'type': 'text',
                'quick_replies': ['Find a phone', 'Compare phones', 'Show me budget options']
            }

        # CRITICAL FIX: Reject malicious/inappropriate queries immediately
        # This catches typos like "hake" (hack), "stel" (steal), etc.
        if self._contains_malicious_intent(message):
            return {
                'response': "I'm DialSmart AI Assistant, and I specialize in helping you find the perfect smartphone! 📱\n\nI can assist you with:\n• Phone recommendations based on your needs\n• Budget-friendly options\n• Brand comparisons\n• Phone specifications\n• Phones for gaming, photography, business, etc.\n\nWhat kind of phone are you looking for today?",
                'type': 'text',
                'quick_replies': ['Find a phone under RM2000', 'Gaming phones', 'Best camera phones', 'Show popular brands']
            }

        # Get session context
        context = self.session_context.get(context_key, {})

        # NEW: Check for specific phone model query
        # Skip phone model extraction ONLY if asking for recommendations with specific requirements
        message_lower = message.lower()

        # Skip phone model extraction if message contains recommendation keywords with requirements
        skip_phone_model = any(keyword in message_lower for keyword in [
            # Direct recommendation requests
            'recommend', 'recommendation', 'suggest', 'suggestion', 'advise', 'advice',
            'help me find', 'help me choose', 'help me pick', 'help me select',
            'find me', 'find a', 'show me', 'give me', 'suggest me',
            'can you recommend', 'can you suggest', 'what phone should',
            'which phone should', 'what do you recommend', 'any recommendation',
            
            # Looking/searching phrases
            'looking for', 'looking to buy', 'searching for', 'search for',
            'want to buy', 'planning to buy', 'thinking of buying',
            'in the market for', 'shopping for',
            
            # Need/want expressions
            'need a phone', 'need phone', 'want a phone', 'want phone',
            'i need', 'i want', 'i am looking', "i'm looking",
            'need recommendations', 'want suggestions',
            
            # Best/top queries
            'best phone', 'best smartphone', 'top phone', 'top smartphone',
            'best option', 'best choice', 'good phone', 'great phone',
            'excellent phone', 'perfect phone', 'ideal phone',
            'which is best', 'what is best', 'whats the best', "what's the best",
            'top rated', 'highest rated', 'most popular',
            
            # Budget-related searches
            'within', 'under rm', 'below rm', 'around rm', 'near rm',
            'budget of', 'price range', 'rm budget', 'under budget',
            'cheap phone', 'affordable phone', 'budget phone',
            'phone under', 'phone within', 'phone below', 'phone around',
            'best under', 'best within', 'best below',
            'cheapest', 'most affordable', 'value for money',
            
            # Usage-specific requests
            'photographer', 'photography phone', 'camera phone',
            'for photography', 'best camera', 'good camera',
            'gaming phone', 'gamer phone', 'for gaming', 'best for gaming',
            'good for gaming', 'gaming performance',
            'business phone', 'for business', 'work phone', 'for work',
            'office phone', 'professional phone', 'productivity phone',
            'social media', 'for social media', 'instagram phone',
            'content creation', 'for content creator', 'vlogging phone',
            'video recording', 'for vlogging',
            
            # Feature-specific searches
            'entertainment', 'streaming phone', 'media phone',
            'long lasting', 'long battery', 'big battery', 'best battery',
            'all day battery', 'battery life',
            'amoled', 'oled display', 'good display', 'best display',
            'large screen', 'big screen', '120hz', 'high refresh',
            '5g phone', 'with 5g', '5g support', 'best 5g',
            'fast charging', 'wireless charging', 'quick charge',
            'good performance', 'fast phone', 'powerful phone',
            
            # User category searches
            'student phone', 'for student', 'college phone',
            'senior phone', 'elderly phone', 'for senior citizen',
            'simple phone', 'easy to use', 'basic phone',
            'parent phone', 'for mom', 'for dad', 'family phone',
            
            # General shopping queries
            'i want a phone', 'show me phones', 'what phones',
            'which phones', 'any phones', 'phones with',
            'phones that have', 'phones under', 'phones within',
            'suitable phone', 'right phone', 'perfect match',
            
            # Comparison shopping (looking for options, not specific models)
            'compare phones', 'phone comparison', 'options under',
            'alternatives', 'similar phones', 'other phones',
            'what else', 'any other', 'more options',
            
            # New/latest searches
            'latest phone', 'newest phone', 'new release',
            'recently released', 'just launched', 'new phones',
            'latest models', 'newest models', '2024 phones',
            '2025 phones', 'this year', 'recent phones',
            
            # Open-ended requests
            'what should i buy', 'what should i get', 'what to buy',
            'help me buy', 'buying advice', 'purchase advice',
            'phone advice', 'phone suggestion',
            
            # Size preference searches
            'small phone', 'compact phone', 'mini phone',
            'large phone', 'big phone', 'phablet',
            'lightweight phone', 'pocket size',
            
            # Brand comparison (without specific model)
            'samsung or iphone', 'xiaomi or realme', 'oppo or vivo',
            'which brand', 'best brand', 'reliable brand',
            'good brand', 'trusted brand',
            
            # Specific needs without model
            'dual sim', 'expandable storage', 'sd card',
            'headphone jack', 'water resistant', 'ip68',
            'wireless charging', 'nfc support', 'ir blaster',
            
            # Quality indicators
            'quality phone', 'reliable phone', 'durable phone',
            'premium phone', 'flagship phone', 'mid range',
            'entry level', 'high end', 'top tier',
            
            # Usage duration
            'for daily use', 'everyday phone', 'all rounder',
            'versatile phone', 'multipurpose phone',
            
            # Upgrade/replacement scenarios
            'upgrade', 'replace', 'replacement', 'new phone',
            'switch from', 'move from', 'upgrade from',
            
            # Gift/purchase for others
            'gift', 'for my', 'buying for', 'present for',
            'gift for mom', 'gift for dad', 'for someone',
            
            # Feature priority
            'prioritize', 'focus on', 'mainly for', 'primarily for',
            'important features', 'must have', 'should have',
            
            # Condition specifications
            'brand new', 'new phone', 'fresh phone', 'unused',
            
            # Availability searches
            'available phones', 'in stock', 'can buy now',
            'currently available', 'on sale',
            
            # Review-based searches
            'highly rated', 'good reviews', 'positive reviews',
            'recommended by', 'popular choice',
            
            # Problem-solving searches
            'better than', 'improvement over', 'instead of',
            'to replace', 'as alternative',
            
            # Multiple options
            'few options', 'some options', 'several phones',
            'list of phones', 'top 5', 'top 10', 'best 5',
            
            # Specification ranges (without specific model)
            'with 8gb ram', 'with 128gb', 'with 5000mah',
            'has 108mp', 'has 120hz', 'with snapdragon',
            
            # Intent indicators
            'planning to', 'thinking about', 'considering',
            'interested in', 'curious about', 'exploring',
            
            # Requirement-based
            'that meets', 'matching my needs', 'fits my needs',
            'according to', 'based on my', 'suitable for',
            
            # Exploration phrases
            'what are', 'are there', 'do you have',
            'can you show', 'could you suggest', 'would you recommend',
            
            # Preference indicators
            'prefer', 'preference', 'like to have', 'would like',
            'hoping for', 'wish to have',
            
            # Budget consciousness
            'worth buying', 'value phone', 'bang for buck',
            'worth the price', 'good deal', 'best deal',
            
            # Urgency without specific model
            'need urgently', 'asap', 'right now', 'immediately',
            'quick recommendation', 'fast suggestion',
            
            # Lifestyle-based
            'minimalist phone', 'flashy phone', 'stylish phone',
            'professional looking', 'trendy phone', 'modern phone',
            
            # Multiple criteria
            'good camera and battery', 'gaming and camera',
            'performance and battery', 'display and camera',
            
            # Negative searches (what to avoid)
            # CRITICAL FIX: Removed 'not' - too generic, matches "note" in "redmi note 14"
            # Use specific phrases instead
            'without', 'avoid', 'hate', 'except', 'excluding',
            'dont want', "don't want", 'no need for', 'i do not want',
            
            # Open comparison
            'difference between brands', 'brand comparison',
            'which brand better', 'brand suggestions'
        ])

        # Initialize brands_mentioned to avoid UnboundLocalError
        brands_mentioned = None

        # CRITICAL FIX: Skip phone model extraction for camera/battery threshold queries
        # These should be handled by threshold filters, not model search
        import re
        if re.search(r'(?:camera|battery).*?(?:above|over|more than|at least)\s+\d+', message_lower):
            skip_phone_model = True
        elif re.search(r'(?:above|over|more than|at least)\s+\d+\s*(?:mp|mah)', message_lower):
            skip_phone_model = True

        # Also skip if multiple brands are mentioned (e.g., "apple and samsung phone")
        # BUT allow if it looks like specific model query (has numbers or model identifiers)
        if not skip_phone_model:
            # CRITICAL FIX: Import re module for regex operations
            import re

            brands_mentioned = self._extract_multiple_brands(message)
            if len(brands_mentioned) > 1 or (brands_mentioned and ' and ' in message_lower and 'phone' in message_lower):
                # Check if this looks like a specific model query
                # Model indicators: numbers, "pro", "ultra", "max", "plus", "lite", etc.
                # FIXED: Added 'play' keyword and improved number matching for cases like "10A", "14X"
                model_indicators = re.search(r'\d+[a-z]?|pro|ultra|max|plus|lite|mini|air|note|fold|flip|edge|play', message_lower)
                if not model_indicators:
                    # No model indicators, so it's a generic brand query
                    skip_phone_model = True

        if brands_mentioned and len(brands_mentioned) == 1:
                # Remove brand name and common words to see what's left
                test_message = message_lower
                for brand in brands_mentioned:
                    test_message = test_message.replace(brand.lower(), '')
                # Remove common words - CRITICAL FIX: Added 'model', 'models' and descriptive words to avoid false model detection
                common_words = ['phone', 'phones', 'smartphone', 'smartphones', 'model', 'models',
                               'with', 'good', 'great', 'best', 'nice', 'excellent', 'amazing',
                               'for', 'the', 'a', 'an', 'any', 'some', 'all',
                               'i like', 'i love', 'i prefer', 'i want', 'i need',
                               'like', 'love', 'prefer', 'want', 'need', 'hate', 'dislike']
                for word in common_words:
                    test_message = test_message.replace(word, ' ')
                test_message = ' '.join(test_message.split())  # Remove extra spaces

                # CRITICAL FIX: Import re module for regex operations
                import re

                # Check if remaining text is a model identifier
                # Model identifiers: numbers (e.g., "17", "15"), or model keywords (e.g., "pro", "ultra")
                has_number = re.search(r'\d+', test_message)
                has_model_keyword = any(keyword in test_message for keyword in ['pro', 'ultra', 'max', 'plus', 'lite', 'mini', 'note', 'fold', 'flip', 'edge', 'air'])

                # CRITICAL FIX: Check if remaining text is mostly feature/spec keywords
                # If it's a feature query (performance, battery, camera, etc.), skip model extraction
                is_feature_query = any(keyword in test_message for keyword in [
                    'performance', 'battery', 'camera', 'display', 'screen', 'storage',
                    'ram', 'memory', 'processor', 'fast', 'slow', 'cheap', 'expensive',
                    'gaming', 'photography', 'selfie', '5g', 'mah', 'gb'
                ])

                # CRITICAL FIX: If it's a feature query, skip phone model extraction even if numbers present
                # Numbers in feature queries are spec values (256GB, 12GB, 100MP), not model numbers (14 Pro, S23)
                if is_feature_query:
                    skip_phone_model = True
                # If nothing meaningful left AND no model indicators, it's a generic brand query
                elif (len(test_message) < 2) and not has_number and not has_model_keyword:
                    skip_phone_model = True

        # Try to extract phone model if NOT asking for recommendations
        if not skip_phone_model:
            try:
                # NEW: Check for multiple phone models (e.g., "iphone 17 pro and xiaomi 17 pro")
                if ' and ' in message_lower and not any(word in message_lower for word in ['recommend', 'suggest', 'find', 'show', 'best', 'which', 'what']):
                    # Split by 'and' and try to extract each model
                    parts = message_lower.split(' and ')
                    all_phones = []
                    for i, part in enumerate(parts):
                        phones = self._extract_phone_model(part)
                        if phones:
                            all_phones.extend(phones if isinstance(phones, list) else [phones])

                    if len(all_phones) >= 1:
                        # At least one specific model found - show it
                        # FIXED: Changed threshold from >= 2 to >= 1 to show partial results
                        # This handles cases where one model exists but the other doesn't
                        return self._handle_specific_phone_query(message, all_phones, is_multi_model=True)

                # Standard single model extraction
                phone_model = self._extract_phone_model(message)
                if phone_model:
                    return self._handle_specific_phone_query(message, phone_model)
                elif not skip_phone_model:
                    # Model query but no phones found - provide helpful message
                    # Extract brand and model name for better error message
                    brands_in_query = self._extract_multiple_brands(message)
                    if brands_in_query:
                        brand_text = brands_in_query[0]
                        # Remove brand name to get potential model
                        model_text = message_lower
                        for brand in brands_in_query:
                            model_text = model_text.replace(brand.lower(), '').strip()
                        model_text = model_text.replace('phone', '').replace('smartphone', '').strip()

                        if model_text:
                            return {
                                'response': f"I couldn't find a specific model matching '{brand_text} {model_text}'. Would you like to:\n• See all {brand_text} phones\n• Try a different model name\n• Get recommendations based on your budget",
                                'type': 'text',
                                'quick_replies': [f'Show {brand_text} phones', 'Find phones under RM2000', 'Latest phones']
                            }
            except Exception as e:
                # Error during model extraction - log and continue with general intent handling
                import traceback
                print(f"Error in phone model extraction: {e}")
                traceback.print_exc()
                # Don't return error - let it fall through to general intent handling
        # END NEW CODE

        # CRITICAL FIX: Handle yes/no responses to pending questions
        yes_responses = ['yes', 'yeah', 'yep', 'sure', 'ok', 'okay', 'show me', 'show them']
        if message_lower.strip() in yes_responses:
            pending = context.get('pending_question')
            if pending and pending.get('type') == 'camera_relaxed':
                # User said yes to seeing phones with lower camera MP
                # Show phones with camera >= 50MP (relaxed threshold)
                relaxed_camera = 50  # Lower threshold
                brands = pending.get('brands')
                budget = pending.get('budget')

                phones = self.ai_engine.get_phones_by_camera(
                    min_camera_mp=relaxed_camera,
                    budget_range=budget,
                    brand_names=brands,
                    top_n=5
                )

                # Clear pending question
                self.session_context[context_key]['pending_question'] = None

                if phones:
                    brand_text = f"{', '.join(brands)} " if brands else ""
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Here are {brand_text}phones with camera above {relaxed_camera}MP{budget_text}:\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        if specs and specs.rear_camera_main:
                            response += f"   📷 {specs.rear_camera_main}MP main camera\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'camera': specs.rear_camera_main if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'camera_threshold': relaxed_camera, 'brands': brands, 'budget': budget}
                    }
                else:
                    # FIXED: Handle case where even relaxed threshold finds no phones
                    brand_text = f"{', '.join(brands)} " if brands else ""
                    budget_text = f" within your budget" if budget else ""
                    return {
                        'response': f"I couldn't find {brand_text}phones with camera above {relaxed_camera}MP{budget_text}. Please try:\n• Different brand\n• Adjust your budget\n• Browse all phones",
                        'type': 'text',
                        'quick_replies': ['Show all brands', 'Phones under RM3000', 'Browse all phones']
                    }

        # Check if the query is phone-related (skip for greetings and help)
        if intent not in ['greeting', 'help'] and not self._is_phone_related(message):
            return {
                'response': "I'm DialSmart AI Assistant, and I specialize in helping you find the perfect smartphone! 📱\n\nI can assist you with:\n• Phone recommendations based on your needs\n• Budget-friendly options\n• Brand comparisons\n• Phone specifications\n• Phones for gaming, photography, business, etc.\n\nWhat kind of phone are you looking for today?",
                'type': 'text',
                'quick_replies': ['Find a phone under RM2000', 'Gaming phones', 'Best camera phones', 'Show popular brands']
            }

        if intent == 'budget_query' or intent == 'timeline':
            # Extract budget from message
            budget = self._extract_budget(message)
            wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
            context = self.session_context.get(context_key, {})
            session_wanted = context.get('wanted_brands', [])
            session_unwanted = context.get('unwanted_brands', [])
            session_usage = context.get('last_usage')

            # Combine current message brands with session brands
            all_wanted_brands = list(set(wanted_brands + session_wanted))
            all_unwanted_brands = list(set(unwanted_brands + session_unwanted))

            brand_names = all_wanted_brands
            
            release_date_criteria = self._extract_release_date_criteria(message)
            if budget:
                min_budget, max_budget = budget
                 # If brands mentioned, filter by brand
                if brand_names:
                    # CRITICAL FIX: Import Brand to avoid UnboundLocalError
                    from app.models import Brand

                    all_phones = []
                    found_brands = []

                    for brand_name in brand_names:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            query = Phone.query.filter_by(brand_id=brand.id, is_active=True)
                            query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)
                            if release_date_criteria:
                                start_date, end_date = release_date_criteria
                                query = query.filter(Phone.release_date >= start_date, Phone.release_date <= end_date)
                            phones = query.limit(5).all()

                            if phones:
                                found_brands.append(brand.name)
                                all_phones.extend([(phone, brand.name) for phone in phones])

                    # FILTER OUT UNWANTED BRANDS
                    if all_unwanted_brands:
                        filtered_phones = []
                        for phone, brand_name in all_phones:
                            if brand_name not in all_unwanted_brands:
                                filtered_phones.append((phone, brand_name))
                        all_phones = filtered_phones

                    if all_phones:
                        brands_text = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}" if len(found_brands) > 1 else found_brands[0]
                        # Build timeline text
                        timeline_text = ""
                        if release_date_criteria:
                            start_date, end_date = release_date_criteria
                            from datetime import datetime
                            if start_date.year == end_date.year:
                                timeline_text = f" from {start_date.year}"
                            else:
                                timeline_text = f" released between {start_date.strftime('%b %Y')} and {end_date.strftime('%b %Y')}"

                        response = f"Here are {brands_text} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}{timeline_text}:\n\n"

                        phone_list = []
                        for phone, brand_name in all_phones:
                            response += f"📱 {brand_name} {phone.model_name} - RM{phone.price:,.2f}\n"
                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': brand_name,
                                'price': phone.price,
                                'image': phone.main_image,
                                'url': f'/phone/{phone.id}'
                            })

                        return {
                            'response': response,
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'usage': session_usage,'brands': found_brands, 'budget': budget, 'release_date': release_date_criteria}
                        }
                    else:
                        brands_text = ", ".join(brand_names[:-1]) + f" and {brand_names[-1]}" if len(brand_names) > 1 else brand_names[0]
                        return {
                            'response': f"I couldn't find {brands_text} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}. Would you like to see phones from other brands?",
                            'type': 'text'
                        }

                # Build query with budget and optional timeline filter
                query = Phone.query.join(Brand).filter(
                    Phone.is_active == True,
                    Phone.price >= min_budget,
                    Phone.price <= max_budget
                )

                # Exclude unwanted brands
                if all_unwanted_brands:
                    unwanted_brand_ids = []
                    for brand_name in all_unwanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            unwanted_brand_ids.append(brand.id)
                    if unwanted_brand_ids:
                        query = query.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                # Apply release date filter if specified
                if release_date_criteria:
                    start_date, end_date = release_date_criteria
                    query = query.filter(Phone.release_date >= start_date, Phone.release_date <= end_date)

                # Order by price and limit results
                phones = query.order_by(Phone.price).limit(5).all()

                if phones:
                    # Build timeline text
                    timeline_text = ""
                    if release_date_criteria:
                        start_date, end_date = release_date_criteria
                        from datetime import datetime
                        if start_date.year == end_date.year:
                            timeline_text = f" from {start_date.year}"
                        else:
                            timeline_text = f" released between {start_date.strftime('%b %Y')} and {end_date.strftime('%b %Y')}"

                    response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}{timeline_text}:\n\n"
                    phone_list = []
                    for phone in phones:
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'url': f'/phone/{phone.id}'
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'budget': budget, 'release_date': release_date_criteria}
                    }
                else:
                    return {
                        'response': f"I couldn't find phones in that exact range. Would you like to adjust your budget?",
                        'type': 'text'
                    }
                # Handle timeline-only queries (no budget specified, but has timeline)
            elif release_date_criteria:
                start_date, end_date = release_date_criteria

                # Build query with timeline filter
                query = Phone.query.join(Brand).filter(
                    Phone.is_active == True,
                    Phone.release_date >= start_date,
                    Phone.release_date <= end_date
                )

                # If brand specified, filter by brand
                if brand_names:
                    brand_ids = []
                    for brand_name in brand_names:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                    if brand_ids:
                        query = query.filter(Phone.brand_id.in_(brand_ids))

                # Special handling for "cheapest new" queries
                if 'cheapest' in message.lower() or 'cheap' in message.lower():
                    phones = query.order_by(Phone.price).limit(5).all()
                    cheapest_text = "cheapest " if 'cheapest' in message.lower() else ""
                else:
                    # Order by release date (newest first)
                    phones = query.order_by(Phone.release_date.desc()).limit(5).all()
                    cheapest_text = ""

                if phones:
                    # Build timeline description
                    from datetime import datetime
                    if start_date.year == end_date.year:
                        timeline_desc = f"from {start_date.year}"
                    else:
                        timeline_desc = f"released between {start_date.strftime('%b %Y')} and {end_date.strftime('%b %Y')}"

                    brand_text = ""
                    if brand_names:
                        brand_text = f"{', '.join(brand_names)} "

                    response = f"Here are the {cheapest_text}{brand_text}phones {timeline_desc}:\n\n"
                    phone_list = []
                    for phone in phones:
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        if phone.release_date:
                            response += f"   📅 Released: {phone.release_date.strftime('%b %Y')}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'url': f'/phone/{phone.id}',
                            'release_date': phone.release_date.isoformat() if phone.release_date else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'release_date': release_date_criteria}
                    }
                else:
                    return {
                        'response': f"I couldn't find phones matching your criteria. Would you like to try a different time period?",
                        'type': 'text'
                    }
            else:
                return {
                    'response': "What's your budget range? For example, 'I'm looking for phones under RM2000'",
                    'type': 'text'
                }

        elif intent == 'recommendation' or intent == 'specification':
            # CRITICAL FIX: Detect all parameters from message, then fall back to session context
            features = self._detect_feature_priority(message)
            if not features and 'last_features' in context and context['last_features']:
                features = context['last_features']  # ← Use previous features!

            user_category = self._detect_user_category(message)

            # CRITICAL FIX: Detect if this is a spec/feature query
            # For spec queries, DON'T use session budget/usage to avoid incorrect filtering
            spec_keywords = ['5g', '5G', 'storage', 'ram', 'memory', 'camera', 'battery',
                            'processor', 'display', 'screen', 'mah', 'mp', 'gb', 'performance',
                            'long lasting', 'good battery']
            is_spec_query = any(keyword in message.lower() for keyword in spec_keywords)

            # Extract budget from current message
            budget = self._extract_budget(message)

            # CRITICAL FIX: Only use session budget for NON-SPEC queries
            # Examples:
            # - "5g phone" should NOT use session budget (spec query)
            # - "recommend phone" SHOULD use session budget (general query)
            # - "realme with good performance" should NOT use session budget (spec query)
            if not budget and not is_spec_query and 'last_budget' in context:
                budget = context['last_budget']  # ← Use previous budget for general queries only!

            # Detect usage type from current message
            usage = self._detect_usage_type(message)

            # CRITICAL FIX: Only use session usage for NON-SPEC queries
            # "long lasting phone" should NOT be detected as Photography from session
            if not usage and not is_spec_query and 'last_usage' in context:
                usage = context['last_usage']  # ← Use previous usage for general queries only!

            # FIX 6: Merge current brands with session context brands
            wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)

            # Get session context brands
            session_wanted = context.get('wanted_brands', [])
            session_unwanted = context.get('unwanted_brands', [])

            # CRITICAL FIX: For spec queries (storage, RAM, 5G, etc.) with explicit brand mentions,
            # use ONLY current message brands, not session brands to avoid wrong results
            # Example: "256GB storage vivo" should show ONLY Vivo, not previous session brands
            # Example: "5G phone recommend" should show ALL 5G phones, not just Samsung from session
            if wanted_brands:
                # User explicitly mentioned brands in current message - use ONLY those
                all_wanted_brands = wanted_brands
                all_unwanted_brands = unwanted_brands
            elif is_spec_query:
                # Spec query without brand mentions - don't use session brands
                all_wanted_brands = []
                all_unwanted_brands = unwanted_brands  # But keep unwanted brands
            else:
                # No brands in current message and not a spec query - merge with session brands
                all_wanted_brands = list(set(wanted_brands + session_wanted))
                all_unwanted_brands = list(set(unwanted_brands + session_unwanted))

            # Use merged brands
            brands = all_wanted_brands if all_wanted_brands else None

            # NEW: Check for battery or camera threshold queries
            battery_threshold = self._extract_battery_threshold(message)
            camera_threshold = self._extract_camera_threshold(message)

            # CRITICAL FIX: Extract RAM, storage, and 5G requirements
            ram_requirement = self._extract_ram_requirement(message)
            storage_requirement = self._extract_storage_requirement(message)
            requires_5g = self._extract_5g_requirement(message)

            # CRITICAL FIX: Check for "cheapest" queries
            # Handle queries like "recommend cheapest phones", "most affordable phones"
            cheapest_keywords = ['cheapest', 'most affordable', 'value for money', 'vfm', 'bang for buck',
                                'lowest price', 'budget friendly', 'most economical', 'least expensive']
            is_cheapest_query = any(keyword in message_lower for keyword in cheapest_keywords)

            # PRIORITY -1: Cheapest phones query (e.g., "recommend cheapest phones", "most affordable phones")
            if is_cheapest_query and not battery_threshold and not camera_threshold:
                from app.models import Brand
                from sqlalchemy import func

                # CRITICAL FIX: Get cheapest phone FROM EACH BRAND (not overall cheapest)
                # Step 1: Build base query
                query = Phone.query.filter_by(is_active=True)

                # Apply budget filter if specified (but for cheapest queries, use very low default)
                if budget:
                    min_budget, max_budget = budget
                    query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)
                else:
                    # CRITICAL FIX: For cheapest queries without budget, use low range (RM10-3000)
                    query = query.filter(Phone.price >= 10, Phone.price <= 3000)

                # Apply brand filters
                if brands:
                    brand_ids = []
                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                    if brand_ids:
                        query = query.filter(Phone.brand_id.in_(brand_ids))

                # Exclude unwanted brands
                if all_unwanted_brands:
                    unwanted_brand_ids = []
                    for brand_name in all_unwanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            unwanted_brand_ids.append(brand.id)
                    if unwanted_brand_ids:
                        query = query.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                # Step 2: Get cheapest phone from each brand using subquery
                # Get minimum price for each brand
                subquery = db.session.query(
                    Phone.brand_id,
                    func.min(Phone.price).label('min_price')
                ).filter_by(is_active=True)

                if budget:
                    subquery = subquery.filter(Phone.price >= min_budget, Phone.price <= max_budget)
                else:
                    subquery = subquery.filter(Phone.price >= 10, Phone.price <= 3000)

                if brands and brand_ids:
                    subquery = subquery.filter(Phone.brand_id.in_(brand_ids))
                if all_unwanted_brands and unwanted_brand_ids:
                    subquery = subquery.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                subquery = subquery.group_by(Phone.brand_id).subquery()

                # Join with subquery to get actual phones with minimum price per brand
                phones_query = db.session.query(Phone).join(
                    subquery,
                    (Phone.brand_id == subquery.c.brand_id) & (Phone.price == subquery.c.min_price)
                ).filter(Phone.is_active == True)

                # Order by price ascending and limit to 5 brands
                phones = phones_query.order_by(Phone.price.asc()).limit(5).all()

                if phones:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "

                    budget_text = ""
                    if budget:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

                    response = f"Here are the most affordable {brand_text}phones{budget_text}:\n\n"
                    phone_list = []

                    for phone in phones:
                        specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        if specs:
                            if specs.ram_options:
                                response += f"   💾 {specs.ram_options} RAM"
                                if specs.storage_options:
                                    response += f" - {specs.storage_options} Storage"
                                response += "\n"
                            if specs.battery_capacity:
                                response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'specs': {
                                'ram': specs.ram_options if specs else None,
                                'storage': specs.storage_options if specs else None,
                                'battery': specs.battery_capacity if specs else None
                            }
                        })

                    # CRITICAL FIX: Save query_type to context for sequential queries
                    self.session_context[context_key]['last_query_type'] = 'cheapest'

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'brands': brands,
                            'budget': budget,
                            'query_type': 'cheapest'
                        }
                    }
                else:
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    brand_text = f"{brands_list} " if brands else ""
                    return {
                        'response': f"I couldn't find {brand_text}phones{budget_text}. Would you like to adjust your budget or brand preferences?",
                        'type': 'text'
                    }

            # PRIORITY 0: Battery threshold query (e.g., "realme phone above 5000mah battery")
            if battery_threshold:
                phones = self.ai_engine.get_phones_by_battery(
                    min_battery_mah=battery_threshold,
                    budget_range=budget,
                    brand_names=brands,
                    top_n=5
                )

                if phones:
                    brand_text = ""
                    if brands:
                        brand_text = f"{', '.join(brands)} "
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Here are the best {brand_text}phones with battery above {battery_threshold}mAh{budget_text}:\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        if specs and specs.battery_capacity:
                            response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'battery': specs.battery_capacity if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'battery_threshold': battery_threshold, 'brands': brands, 'budget': budget}
                    }
                else:
                    brand_text = f"{', '.join(brands)} " if brands else ""
                    budget_text = f" within your budget" if budget else ""
                    return {
                        'response': f"I couldn't find {brand_text}phones with battery above {battery_threshold}mAh{budget_text}. Would you like to see phones with slightly lower battery capacity?",
                        'type': 'text'
                    }

            # PRIORITY 0.5: Camera threshold query (e.g., "phone camera above 100MP")
            if camera_threshold:
                phones = self.ai_engine.get_phones_by_camera(
                    min_camera_mp=camera_threshold,
                    budget_range=budget,
                    brand_names=brands,
                    top_n=5
                )

                if phones:
                    brand_text = ""
                    if brands:
                        brand_text = f"{', '.join(brands)} "
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Here are the best {brand_text}phones with camera above {camera_threshold}MP{budget_text}:\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        if specs and specs.rear_camera_main:
                            response += f"   📷 {specs.rear_camera_main}MP main camera\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'camera': specs.rear_camera_main if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'camera_threshold': camera_threshold, 'brands': brands, 'budget': budget}
                    }
                else:
                    brand_text = f"{', '.join(brands)} " if brands else ""
                    budget_text = f" within your budget" if budget else ""

                    # CRITICAL FIX: Save pending question to context for "yes" response handling
                    self.session_context[context_key]['pending_question'] = {
                        'type': 'camera_relaxed',
                        'brands': brands,
                        'camera_threshold': camera_threshold,
                        'budget': budget
                    }

                    return {
                        'response': f"I couldn't find {brand_text}phones with camera above {camera_threshold}MP{budget_text}. Would you like to see phones with slightly lower megapixel cameras?",
                        'type': 'text'
                    }

            # CRITICAL FIX: RAM requirement query (e.g., "12GB RAM phone", "phone with 16gb ram")
            if ram_requirement:
                from app.models import Brand
                query = Phone.query.filter_by(is_active=True)

                # Apply budget filter
                if budget:
                    min_budget, max_budget = budget
                    query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

                # Apply brand filters
                if brands:
                    brand_ids = []
                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                    if brand_ids:
                        query = query.filter(Phone.brand_id.in_(brand_ids))

                # Exclude unwanted brands
                if all_unwanted_brands:
                    unwanted_brand_ids = []
                    for brand_name in all_unwanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            unwanted_brand_ids.append(brand.id)
                    if unwanted_brand_ids:
                        query = query.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                phones = query.all()

                # Filter by RAM requirement
                matching_phones = []
                for phone in phones:
                    specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
                    if specs and specs.ram_options:
                        # CRITICAL FIX: Handle multiple RAM formats: "8GB, 12GB" or "8 / 12 / 16 GB" or "8 / 12 / 16"
                        import re
                        ram_text = specs.ram_options.upper().replace('GB', '').replace('RAM', '').strip()
                        # Extract all numbers from the RAM text
                        ram_values = [int(x.strip()) for x in re.findall(r'\d+', ram_text) if x.strip().isdigit()]
                        if ram_values and max(ram_values) >= ram_requirement:
                            matching_phones.append((phone, specs, max(ram_values)))

                # Sort by RAM (highest first)
                matching_phones.sort(key=lambda x: x[2], reverse=True)
                matching_phones = matching_phones[:5]

                if matching_phones:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "

                    budget_text = ""
                    if budget:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

                    response = f"Here are {brand_text}phones with {ram_requirement}GB or more RAM{budget_text}:\n\n"
                    phone_list = []

                    for phone, specs, _ in matching_phones:  # Unpack (phone, specs, max_ram)
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        response += f"   💾 {specs.ram_options} RAM"
                        if specs.storage_options:
                            response += f" - {specs.storage_options} Storage"
                        response += "\n"
                        if specs.processor:
                            response += f"   ⚡ {specs.processor}\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'ram': specs.ram_options,
                            'storage': specs.storage_options if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'ram_requirement': ram_requirement, 'brands': brands, 'budget': budget}
                    }
                else:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "
                    budget_text = f" within your budget" if budget else ""
                    return {
                        'response': f"I couldn't find {brand_text}phones with {ram_requirement}GB RAM{budget_text}. Would you like to see phones with slightly lower RAM?",
                        'type': 'text'
                    }

            # CRITICAL FIX: Storage requirement query (e.g., "256GB storage samsung", "512gb phone")
            if storage_requirement:
                from app.models import Brand
                query = Phone.query.filter_by(is_active=True)

                # Apply budget filter
                if budget:
                    min_budget, max_budget = budget
                    query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

                # Apply brand filters
                if brands:
                    brand_ids = []
                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                    if brand_ids:
                        query = query.filter(Phone.brand_id.in_(brand_ids))

                # Exclude unwanted brands
                if all_unwanted_brands:
                    unwanted_brand_ids = []
                    for brand_name in all_unwanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            unwanted_brand_ids.append(brand.id)
                    if unwanted_brand_ids:
                        query = query.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                phones = query.all()

                # Filter by storage requirement
                matching_phones = []
                for phone in phones:
                    specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
                    if specs and specs.storage_options:
                        # CRITICAL FIX: Handle multiple storage formats: "128GB, 256GB" or "128 / 256 / 512 GB" or "128 / 256"
                        import re
                        storage_text = specs.storage_options.upper().replace('GB', '').replace('TB', '000').replace('STORAGE', '').strip()
                        # Extract all numbers from the storage text
                        storage_values = [int(x.strip()) for x in re.findall(r'\d+', storage_text) if x.strip().isdigit()]
                        if storage_values and max(storage_values) >= storage_requirement:
                            matching_phones.append((phone, specs, max(storage_values)))

                # Sort by storage (highest first)
                matching_phones.sort(key=lambda x: x[2], reverse=True)
                matching_phones = matching_phones[:5]

                if matching_phones:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "

                    budget_text = ""
                    if budget:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

                    response = f"Here are {brand_text}phones with {storage_requirement}GB or more storage{budget_text}:\n\n"
                    phone_list = []

                    for phone, specs, _ in matching_phones:  # Unpack (phone, specs, max_storage)
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        response += f"   📦 {specs.storage_options} Storage"
                        if specs.ram_options:
                            response += f" - {specs.ram_options} RAM"
                        response += "\n"
                        if specs.processor:
                            response += f"   ⚡ {specs.processor}\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'storage': specs.storage_options,
                            'ram': specs.ram_options if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'storage_requirement': storage_requirement, 'brands': brands, 'budget': budget}
                    }
                else:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "
                    budget_text = f" within your budget" if budget else ""
                    return {
                        'response': f"I couldn't find {brand_text}phones with {storage_requirement}GB storage{budget_text}. Would you like to see phones with slightly lower storage?",
                        'type': 'text'
                    }

            # CRITICAL FIX: 5G requirement query (e.g., "5g phone recommend", "phone with 5g")
            if requires_5g and not battery_threshold and not camera_threshold:
                from app.models import Brand
                query = Phone.query.filter_by(is_active=True)

                # Apply budget filter
                if budget:
                    min_budget, max_budget = budget
                    query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)

                # Apply brand filters
                if brands:
                    brand_ids = []
                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                    if brand_ids:
                        query = query.filter(Phone.brand_id.in_(brand_ids))

                # Exclude unwanted brands
                if all_unwanted_brands:
                    unwanted_brand_ids = []
                    for brand_name in all_unwanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            unwanted_brand_ids.append(brand.id)
                    if unwanted_brand_ids:
                        query = query.filter(~Phone.brand_id.in_(unwanted_brand_ids))

                phones = query.all()

                # Filter by 5G support
                matching_phones = []
                for phone in phones:
                    specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
                    if specs and specs.has_5g:
                        matching_phones.append((phone, specs))

                # Sort by price descending (show premium 5G phones first)
                matching_phones.sort(key=lambda x: x[0].price, reverse=True)
                matching_phones = matching_phones[:5]

                if matching_phones:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "

                    budget_text = ""
                    if budget:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

                    response = f"Here are {brand_text}phones with 5G support{budget_text}:\n\n"
                    phone_list = []

                    for phone, specs in matching_phones:
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        response += f"   📶 5G Support\n"
                        if specs.ram_options:
                            response += f"   💾 {specs.ram_options} RAM"
                            if specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += "\n"
                        if specs.processor:
                            response += f"   ⚡ {specs.processor}\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'has_5g': True,
                            'ram': specs.ram_options if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'requires_5g': True, 'brands': brands, 'budget': budget}
                    }
                else:
                    brand_text = ""
                    if brands:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        brand_text = f"{brands_list} "
                    budget_text = f" within your budget" if budget else ""
                    return {
                        'response': f"I couldn't find {brand_text}5G phones{budget_text}. Most 5G phones are in the higher price range. Would you like to adjust your budget?",
                        'type': 'text'
                    }

            # PRIORITY 1: User category (student, senior, professional) - handle first
            if user_category:
                # Set default budget ranges for each category
                if user_category == 'student':
                    budget = budget or (1000, 2500)
                    category_name = "students"
                    intro = "Perfect! Here are the best value phones for students - great performance for studying and entertainment:"
                elif user_category == 'senior':
                    budget = budget or (800, 2000)  # Increased range to ensure phones are available
                    category_name = "seniors"
                    intro = "Great! Here are user-friendly phones for seniors - simple to use with excellent battery life:"
                elif user_category == 'professional':
                    budget = budget or (2000, 5000)
                    category_name = "professionals"
                    intro = "Excellent! Here are reliable phones for professionals - long battery, big storage, and great performance:"
                else:
                    budget = budget or (1000, 3000)
                    category_name = user_category + "s"
                    intro = f"Here are the best phones for {category_name}:"

                # Get recommendations based on user category
                try:
                    phones = self.ai_engine.get_phones_by_features(
                        features=[],  # No specific features, let category scoring decide
                        budget_range=budget,
                        usage_type=usage,
                        brand_names=brands,
                        user_category=user_category,
                        top_n=5
                    )
                except Exception as e:
                    # Log error and return fallback
                    import traceback
                    traceback.print_exc()
                    phones = []

                if phones:
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"
                    response = f"{intro}\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Show relevant specs based on user category
                        if specs:
                            if user_category == 'student':
                                # Students: processor, RAM, battery
                                if specs.processor:
                                    response += f"   ⚡ {specs.processor}\n"
                                if specs.ram_options:
                                    response += f"   🧠 {specs.ram_options} RAM\n"
                                if specs.battery_capacity:
                                    response += f"   🔋 {specs.battery_capacity}mAh\n"
                            elif user_category == 'senior':
                                # Seniors: screen size, battery, simple features
                                if specs.screen_size:
                                    response += f"   📺 {specs.screen_size}\" display (easy to read)\n"
                                if specs.battery_capacity:
                                    response += f"   🔋 {specs.battery_capacity}mAh (long lasting)\n"
                                if specs.ram_options:
                                    response += f"   🧠 {specs.ram_options} RAM\n"
                            elif user_category == 'professional':
                                # Professionals: battery, storage, RAM
                                if specs.battery_capacity:
                                    response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                                if specs.storage_options:
                                    response += f"   💾 {specs.storage_options} storage\n"
                                if specs.ram_options:
                                    response += f"   🧠 {specs.ram_options} RAM\n"

                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'specs': {
                                'battery': specs.battery_capacity if specs else None,
                                'camera': specs.rear_camera_main if specs else None,
                                'processor': specs.processor if specs else None,
                                'ram': specs.ram_options if specs else None,
                                'storage': specs.storage_options if specs else None
                            }
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'user_category': user_category,
                            'budget': budget
                        }
                    }
                else:
                    # No phones found for this category - provide helpful fallback
                    budget_text = f"RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"
                    return {
                        'response': f"I couldn't find phones specifically for {category_name} within {budget_text}. Let me show you our available phones. What's your preferred budget range?",
                        'type': 'text',
                        'quick_replies': ['Under RM1000', 'RM1000-RM2000', 'RM2000-RM3000', 'Above RM3000']
                    }

            # PRIORITY 2: Brands mentioned - always prioritize brand filtering
            if brands:
                phones = []

                # Brands + Usage (e.g., "apple and samsung gaming phone")
                if usage:
                    phones = self.ai_engine.get_phones_by_usage(usage, budget, brands, top_n=5)

                    if phones:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        response = f"Great choice! Here are the best phones for {usage} from {brands_list}{budget_text}:\n\n"

                        phone_list = []
                        for item in phones:
                            phone = item['phone']
                            specs = item.get('specifications')
                            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                            # CRITICAL FIX: Show usage-specific highlights
                            if specs:
                                if usage == 'Photography' and specs.rear_camera_main:
                                    response += f"   📷 {specs.rear_camera_main}MP camera\n"
                                if usage == 'Gaming' and specs.processor:
                                    response += f"   ⚡ {specs.processor}\n"
                                if usage in ['Business', 'Work'] and specs.battery_capacity:
                                    response += f"   🔋 {specs.battery_capacity}mAh battery\n"

                                # Always show RAM and storage
                                if specs.ram_options:
                                    response += f"   💾 {specs.ram_options} RAM"
                                    if specs.storage_options:
                                        response += f" - {specs.storage_options} Storage"
                                    response += "\n"
                            response += "\n"

                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': phone.brand.name,
                                'price': phone.price,
                                'image': phone.main_image,
                                'ram': specs.ram_options if specs else None,
                                'storage': specs.storage_options if specs else None,
                                'camera': specs.rear_camera_main if specs else None,
                                'battery': specs.battery_capacity if specs else None
                            })

                        return {
                            'response': response,
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'usage': usage, 'brands': brands, 'budget': budget}
                        }
                    else:
                        # No phones found with these brands for this usage
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        return {
                            'response': f"I couldn't find {brands_list} phones for {usage.lower()}. Would you like to see {usage.lower()} phones from other brands, or choose different brands?",
                            'type': 'text',
                            'quick_replies': [f'Show all {usage} phones', 'Try different brands']
                        }

                # Brands + Features (e.g., "apple and samsung with good camera")
                elif features:
                    phones = self.ai_engine.get_phones_by_features(features, budget, usage, brands, user_category, top_n=5)

                    if phones:
                        feature_desc = " and ".join([f.replace('_', ' ') for f in features])
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        response = f"Here are the best {brands_list} phones with {feature_desc}{budget_text}:\n\n"

                        phone_list = []
                        for item in phones:
                            phone = item['phone']
                            specs = item.get('specifications')
                            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                            if specs:
                                if 'battery' in features and specs.battery_capacity:
                                    response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                                if 'camera' in features and specs.rear_camera_main:
                                    response += f"   📷 {specs.rear_camera_main}MP camera\n"
                                if 'display' in features and specs.screen_type:
                                    response += f"   📺 {specs.screen_size}\" {specs.screen_type}\n"
                                if 'performance' in features:
                                    # CRITICAL FIX: Show RAM and processor for performance queries
                                    if specs.ram_options:
                                        response += f"   💾 {specs.ram_options} RAM\n"
                                    if specs.processor:
                                        response += f"   ⚡ {specs.processor}\n"
                            response += "\n"

                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': phone.brand.name,
                                'price': phone.price,
                                'image': phone.main_image,
                                'specs': {
                                    'battery': specs.battery_capacity if specs else None,
                                    'camera': specs.rear_camera_main if specs else None,
                                    'display': specs.screen_type if specs else None,
                                }
                            })

                        return {
                            'response': response,
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'features': features, 'brands': brands, 'budget': budget}
                        }
                    else:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        feature_desc = " and ".join([f.replace('_', ' ') for f in features])
                        return {
                            'response': f"I couldn't find {brands_list} phones with {feature_desc}. Would you like to see similar phones from other brands?",
                            'type': 'text',
                            'quick_replies': ['Show all brands', 'Try different features']
                        }

                # Brands only (e.g., "apple and samsung phone")
                else:
                    from app.models import Brand  # CRITICAL FIX: Import Brand to avoid UnboundLocalError

                    all_phones = []
                    found_brands = []

                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                            if budget:
                                min_b, max_b = budget
                                query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                            # CRITICAL FIX: Sort by RELEASE_DATE (newest first) to show latest phones
                            phones_found = query.order_by(Phone.release_date.desc()).limit(3).all()
                            if phones_found:
                                found_brands.append(brand.name)
                                all_phones.extend([(p, brand.name) for p in phones_found])

                    if all_phones:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                        brands_list = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}" if len(found_brands) > 1 else found_brands[0]
                        response = f"Here are phones from {brands_list}{budget_text}:\n\n"

                        phone_list = []
                        for phone, brand_name in all_phones:
                            response += f"📱 {brand_name} {phone.model_name} - RM{phone.price:,.2f}\n"
                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': brand_name,
                                'price': phone.price,
                                'image': phone.main_image
                            })

                        return {
                            'response': response,
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'brands': found_brands, 'budget': budget}
                        }
                    else:
                        brands_list = ", ".join(brands[:-1]) + f" and {brands[-1]}" if len(brands) > 1 else brands[0]
                        budget_text = f" within your budget" if budget else ""
                        return {
                            'response': f"I couldn't find {brands_list} phones{budget_text}. Would you like to see phones from other brands?",
                            'type': 'text',
                            'quick_replies': ['Show all brands', 'Adjust budget']
                        }

            # PRIORITY 3: Usage type without brands (e.g., "gaming phone")
            if usage:
                phones = self.ai_engine.get_phones_by_usage(usage, budget, None, top_n=5)

                if phones:
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Great choice! Here are the best phones for {usage}{budget_text}:\n\n"

                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # CRITICAL FIX: Show relevant specs based on usage type
                        if specs:
                            # Show usage-specific highlights
                            if usage == 'Photography' and specs.rear_camera_main:
                                response += f"   📷 {specs.rear_camera_main}MP camera\n"
                            if usage == 'Gaming' and specs.processor:
                                response += f"   ⚡ {specs.processor}\n"
                            if usage in ['Business', 'Work'] and specs.battery_capacity:
                                response += f"   🔋 {specs.battery_capacity}mAh battery\n"

                            # Always show RAM and storage
                            if specs.ram_options:
                                response += f"   💾 {specs.ram_options} RAM"
                                if specs.storage_options:
                                    response += f" - {specs.storage_options} Storage"
                                response += "\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'ram': specs.ram_options if specs else None,
                            'storage': specs.storage_options if specs else None,
                            'camera': specs.rear_camera_main if specs else None,
                            'battery': specs.battery_capacity if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'usage': usage, 'budget': budget}
                    }

            # PRIORITY 4: Features without brands (e.g., "phone with good camera")
            if features:
                phones = self.ai_engine.get_phones_by_features(features, budget, usage, None, user_category, top_n=5)

                if phones:
                    # FIXED: Special handling for timeline (latest/newest) queries
                    is_timeline_query = 'timeline' in features
                    display_features = [f for f in features if f != 'timeline']  # Remove timeline from display

                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""

                    if is_timeline_query and not display_features:
                        # Pure timeline query: "recommend latest phone"
                        response = f"Here are the latest phones{budget_text}:\n\n"
                    elif is_timeline_query and display_features:
                        # Timeline + other features: "latest phone with good camera"
                        feature_desc = " and ".join([f.replace('_', ' ') for f in display_features])
                        response = f"Here are the latest phones with {feature_desc}{budget_text}:\n\n"
                    else:
                        # Regular features: "phone with good camera"
                        feature_desc = " and ".join([f.replace('_', ' ') for f in features])
                        response = f"Here are the best phones with {feature_desc}{budget_text}:\n\n"

                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        if specs:
                            if 'battery' in features and specs.battery_capacity:
                                response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                            if 'camera' in features and specs.rear_camera_main:
                                response += f"   📷 {specs.rear_camera_main}MP camera\n"
                            if 'display' in features and specs.screen_type:
                                response += f"   📺 {specs.screen_size}\" {specs.screen_type}\n"
                            if 'performance' in features:
                                # CRITICAL FIX: Show RAM and processor for performance queries
                                if specs.ram_options:
                                    response += f"   💾 {specs.ram_options} RAM\n"
                                if specs.processor:
                                    response += f"   ⚡ {specs.processor}\n"
                            if 'ram' in features and specs.ram_options:
                                response += f"   💾 {specs.ram_options} RAM\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'specs': {
                                'battery': specs.battery_capacity if specs else None,
                                'camera': specs.rear_camera_main if specs else None,
                                'display': specs.screen_type if specs else None,
                            }
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'features': features, 'budget': budget}
                    }

            criteria = self._extract_criteria(message)
            # PRIORITY 5: Budget/criteria only (e.g., "phone under RM2000")
            if criteria or budget:
                recommendations = self.ai_engine.get_recommendations(user_id, criteria=criteria, top_n=5)

                if recommendations:
                    response = "Based on your needs, I recommend:\n\n"
                    phone_list = []

                    for rec in recommendations:
                        phone = rec['phone']
                        response += f"📱 {phone.brand.name} {phone.model_name}\n"
                        response += f"   💰 RM{phone.price:,.2f}\n"
                        response += f"   ✨ {rec['match_score']}% match\n"
                        response += f"   {rec['reasoning'][:100]}...\n\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'match_score': rec['match_score']
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }

            # PRIORITY 6: Fallback - ask for more info
            return {
                'response': "Let me help you find the perfect phone. What's your budget and what will you primarily use it for?",
                'type': 'text',
                'quick_replies': ['Under RM2000', 'Gaming', 'Photography', 'Show popular phones']
            }

        elif intent == 'usage_type':
            # Detect usage type
            usage = self._detect_usage_type(message)
            if not usage:
                usage = context.get('last_usage')
                
            if usage:
                # Get budget from message or session
                budget = self._extract_budget(message)
                if not budget:
                    budget = context.get('last_budget')

                phones = self.ai_engine.get_phones_by_usage(usage, budget, top_n=10)

                # Filter by brand preferences from session
                wanted_brands = context.get('wanted_brands', [])
                unwanted_brands = context.get('unwanted_brands', [])

                filtered_phones = self._filter_phones_by_brand(phones, wanted_brands, unwanted_brands)

                if filtered_phones:
                    # Limit to top 5 after filtering
                    filtered_phones = filtered_phones[:5]

                    budget_text = ""
                    if budget:
                        min_b, max_b = budget
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}"

                    brand_text = ""
                    if wanted_brands:
                        if len(wanted_brands) == 1:
                            brand_text = wanted_brands[0]
                        else:
                            brand_text = ", ".join(wanted_brands[:-1]) + f" and {wanted_brands[-1]}"
                        response = f"Here are the best {brand_text} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
                    else:
                        response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"

                    phone_list = []

                    for item in filtered_phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Add RAM and storage info if available
                        if specs and specs.ram_options:
                            response += f"   {specs.ram_options} RAM"
                            if specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += f" - Great for {usage.lower()}\n"

                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,  # Add image URL
                            'ram': specs.ram_options if specs else None,
                            'storage': specs.storage_options if specs else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'usage': usage,
                            'budget': budget,
                            'brands': wanted_brands,
                            'usage': session_usage
                        }
                    }
                else:
                    if wanted_brands:
                        brand_names = ', '.join(wanted_brands)
                        return {
                            'response': f"I couldn't find {brand_names} phones in that exact range. Would you like to adjust your budget or see other brands?",
                            'type': 'text'
                        }
                    else:
                        return {
                            'response': f"I couldn't find phones in that exact range. Would you like to adjust your budget?",
                            'type': 'text'
                        }
            else:
                return {
                    'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                    'type': 'text'
                }

        elif intent == 'brand_query':
            # Get session context from both versions
            session_features = context.get('last_features', [])
            session_usage = context.get('last_usage')
            wanted_brands = context.get('wanted_brands', [])
            unwanted_brands = context.get('unwanted_brands', [])

            # PRIORITY 1: If we have session usage AND wanted brands → Use usage-based filtering (Version 1)
            if session_usage and wanted_brands:
                budget = self._extract_budget(message)
                if not budget:
                    budget = context.get('last_budget')

                phones = self.ai_engine.get_phones_by_usage(session_usage, budget, top_n=10)
                filtered_phones = self._filter_phones_by_brand(phones, wanted_brands, unwanted_brands)

                if filtered_phones:
                    filtered_phones = filtered_phones[:5]

                    # Build response with brand context
                    if len(wanted_brands) == 1:
                        brand_text = wanted_brands[0]
                    else:
                        brand_text = ", ".join(wanted_brands[:-1]) + f" and {wanted_brands[-1]}"

                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Great! Here are the best {brand_text} phones for {session_usage}{budget_text}:\n\n"

                    phone_list = []
                    for item in filtered_phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Add specs if available (Version 1 feature)
                        if specs and hasattr(specs, 'ram_options') and specs.ram_options:
                            response += f"   {specs.ram_options} RAM"
                            if hasattr(specs, 'storage_options') and specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += "\n"

                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image if hasattr(phone, 'main_image') else None,
                            'ram': specs.ram_options if specs and hasattr(specs, 'ram_options') else None,
                            'storage': specs.storage_options if specs and hasattr(specs, 'storage_options') else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'usage': session_usage,
                            'brands': wanted_brands,
                            'budget': budget
                        }
                    }

            # PRIORITY 2: If we have session features (but no usage) AND wanted brands → Feature-based filtering (Version 1)
            if session_features and wanted_brands and not session_usage:
                budget = self._extract_budget(message)
                if not budget:
                    budget = context.get('last_budget')

                # Use AI engine's feature-based filtering
                phones_items = self.ai_engine.get_phones_by_features(
                    features=session_features,
                    budget_range=budget,
                    usage_type=None,
                    brand_names=wanted_brands,
                    user_category=None,
                    top_n=10
                )

                if phones_items:
                    phones_items = phones_items[:5]

                    # Build response with feature context
                    feature_names = {
                        'battery': 'long battery life',
                        'camera': 'excellent camera',
                        'display': 'great display',
                        'performance': 'powerful performance',
                        '5g': '5G support',
                        'charging': 'fast charging',
                        'design': 'premium design',
                        'storage': 'ample storage',
                        'ram': 'high RAM'
                    }
                    feature_desc = ', '.join([feature_names.get(f, f) for f in session_features])

                    if len(wanted_brands) == 1:
                        brand_text = wanted_brands[0]
                    else:
                        brand_text = ", ".join(wanted_brands[:-1]) + f" and {wanted_brands[-1]}"

                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                    response = f"Here are {brand_text} phones with {feature_desc}{budget_text}:\n\n"

                    phone_list = []
                    for item in phones_items:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Show relevant specs based on features (Version 1 feature)
                        if specs:
                            if 'battery' in session_features and hasattr(specs, 'battery_capacity') and specs.battery_capacity:
                                response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                            if 'camera' in session_features and hasattr(specs, 'rear_camera_main') and specs.rear_camera_main:
                                response += f"   📷 {specs.rear_camera_main}MP camera\n"
                            if 'display' in session_features and hasattr(specs, 'screen_type') and specs.screen_type:
                                response += f"   📺 {specs.screen_size}\" {specs.screen_type}\n"
                            if 'performance' in session_features and hasattr(specs, 'processor') and specs.processor:
                                response += f"   ⚡ {specs.processor}\n"

                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image if hasattr(phone, 'main_image') else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'features': session_features,
                            'brands': wanted_brands,
                            'budget': budget
                        }
                    }

            # PRIORITY 3: Standard brand query with session context (Merged from both versions)
            if wanted_brands:
                from app.models import Brand  # CRITICAL FIX: Import Brand to avoid UnboundLocalError

                budget = self._extract_budget(message)
                if not budget:
                    budget = context.get('last_budget')

                # CRITICAL FIX: Detect usage from message or use previous usage from context
                usage = self._detect_usage_type(message)
                if not usage:
                    usage = context.get('last_usage')

                # CRITICAL FIX: Check if previous query was "cheapest" and preserve that context
                last_query_type = context.get('last_query_type')

                all_phones = []
                found_brands = []

                # CRITICAL FIX: If usage is present (e.g., "gaming"), use AI engine to filter by usage
                if usage:
                    # Use AI engine to get phones by usage and brands
                    phones_data = self.ai_engine.get_phones_by_usage(usage, budget, wanted_brands, top_n=5)
                    if phones_data:
                        for item in phones_data:
                            phone = item['phone']
                            all_phones.append((phone, phone.brand.name))
                            if phone.brand.name not in found_brands:
                                found_brands.append(phone.brand.name)
                else:
                    # Standard brand query without usage
                    for brand_name in wanted_brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                            # Apply budget filter if specified
                            if budget:
                                min_b, max_b = budget
                                query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                            # CRITICAL FIX: Apply ordering based on previous query type
                            if last_query_type == 'cheapest':
                                # Previous query was "cheapest" - maintain price ascending order
                                phones = query.order_by(Phone.price.asc()).limit(5).all()
                            else:
                                # Default ordering - newest first
                                phones = query.order_by(Phone.release_date.desc()).limit(5).all()

                            if phones:
                                found_brands.append(brand.name)
                                all_phones.extend([(phone, brand.name) for phone in phones])

                if all_phones:
                    # Build response (Enhanced from both versions)
                    if len(found_brands) == 1:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        usage_text = f" for {usage}" if usage else ""
                        feature_text = f" with focus on {', '.join(session_features)}" if session_features else ""
                        response = f"Here are {found_brands[0]} phones{budget_text}{usage_text}{feature_text}:\n\n"
                    else:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        usage_text = f" for {usage}" if usage else ""
                        feature_text = f" with focus on {', '.join(session_features)}" if session_features else ""
                        brands_text = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}"
                        response = f"Here are phones from {brands_text}{budget_text}{usage_text}{feature_text}:\n\n"

                    phone_list = []
                    for phone, brand_name in all_phones[:5]:  # Limit to 5 total
                        response += f"📱 {brand_name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        
                        # Add specifications display (Version 1 enhancement)
                        try:
                            specs = phone.specifications
                            if specs and hasattr(specs, 'ram_options') and specs.ram_options:
                                response += f"   {specs.ram_options} RAM"
                                if hasattr(specs, 'storage_options') and specs.storage_options:
                                    response += f" - {specs.storage_options} Storage"
                                response += "\n"
                        except:
                            pass
                        
                        response += "\n"
                        
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': brand_name,
                            'price': phone.price,
                            'image': phone.main_image if hasattr(phone, 'main_image') else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list,
                            'brands': found_brands,
                            'budget': budget,
                            'usage': usage,
                            'features': session_features
                        }
                    }

            # Fallback message
            return {
                'response': "Which brand are you interested in? We have Samsung, Apple, Xiaomi, Huawei, Oppo, Vivo, Realme, and more!",
                'type': 'text'
            }

        elif intent == 'comparison':
            return {
                'response': "I can help you compare phones! Please go to the Compare page and select two phones you'd like to compare side-by-side.",
                'type': 'text',
                'action': 'redirect_compare'
            }

        elif intent == 'help':
            return {
                'response': """I can help you with:

        📱 Find phone recommendations based on your needs
        💰 Search phones within your budget
        🔍 Compare different phone models
        📊 Get detailed specifications
        🏷️ Browse phones by brand

        Just ask me anything like:
        - "Find me a phone under RM2000"
        - "Best phones for gaming"
        - "Show me Samsung phones"
        - "I need a phone with good camera"
        """,
                'type': 'text'
            }

        else:  # general intent
            # SMART FALLBACK: Check if budget is extractable (Version 2 feature)
            budget = self._extract_budget(message)
            if budget:
                min_budget, max_budget = budget
                context['last_budget'] = budget

                # Get session features and usage
                session_features = context.get('last_features', [])
                session_usage = context.get('last_usage')

                # If we have session usage, use usage-based query with budget
                if session_usage:
                    phones = self.ai_engine.get_phones_by_usage(session_usage, budget, top_n=10)
                else:
                    phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=10)

                # Filter by brand preferences
                wanted_brands = context.get('wanted_brands', [])
                unwanted_brands = context.get('unwanted_brands', [])

                filtered_phones = self._filter_phones_by_brand(phones, wanted_brands, unwanted_brands)

                if filtered_phones:
                    filtered_phones = filtered_phones[:5]

                    # Build response based on brand preferences
                    if wanted_brands:
                        brand_names = ', '.join(wanted_brands)
                        response = f"Here are the best {brand_names} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
                    else:
                        response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
                                    
                    phone_list = []
                    for item in filtered_phones:
                        phone = item['phone']
                        specs = item.get('specifications')
                        
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        
                        # Add specs (Version 1 enhancement)
                        if specs and hasattr(specs, 'ram_options') and specs.ram_options:
                            response += f"   {specs.ram_options} RAM"
                            if hasattr(specs, 'storage_options') and specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += "\n"
                        
                        response += "\n"
                        
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image if hasattr(phone, 'main_image') else None
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {
                            'phones': phone_list, 
                            'budget': budget,
                            'usage': session_usage,
                            'brands': wanted_brands
                        }
                    }
                else:
                    if wanted_brands:
                        brand_names = ', '.join(wanted_brands)
                        return {
                            'response': f"I couldn't find {brand_names} phones in that exact range. Would you like to adjust your budget or see other brands?",
                            'type': 'text'
                        }
                    else:
                        return {
                            'response': f"I couldn't find phones in that exact range. Would you like to adjust your budget?",
                            'type': 'text'
                        }
            
            # Default fallback
            return {
                'response': "I'm here to help you find the perfect smartphone! You can ask me about phone recommendations, budget options, brands, or specifications. What would you like to know?",
                'type': 'text',
                'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
            }

    # NEW METHODS for specific phone queries
    def _extract_phone_model(self, message):
        """Extract specific phone model name from message with brand awareness and fuzzy matching"""
        message_lower = message.lower()
        from sqlalchemy import or_, func
        from difflib import SequenceMatcher

        # Step 1: Detect if a specific brand is mentioned
        # All 13 known brands (matches database brands exactly)
        # Keywords extracted from actual fyp_phoneDataset.csv data
        detected_brand = None
        brand_keywords = {
            'apple': ['apple', 'iphone'],
            'asus': ['asus', 'rog', 'zenfone'],
            'google': ['google', 'pixel'],
            'honor': ['honor', 'magic', 'play'],  # Magic, Play series (removed 'gt' - conflicts)
            'huawei': ['huawei', 'mate', 'pura', 'nova', 'enjoy'],  # Mate, Pura, Nova, Enjoy series
            'infinix': ['infinix', 'hot'],  # Hot series (removed 'note' - conflicts with Redmi Note)
            'oppo': ['oppo', 'reno', 'find'],  # Reno, Find series (removed 'a', 'f' - too generic)
            'poco': ['poco'],
            'realme': ['realme', 'narzo', 'neo'],  # Narzo, Neo series (removed 'gt' - conflicts)
            'redmi': ['redmi', 'note'],  # Note series
            'samsung': ['samsung', 'galaxy', 'fold', 'flip'],  # Galaxy, Fold, Flip series
            'vivo': ['vivo', 'iqoo'],  # iQOO sub-brand (removed single letters - too generic)
            'xiaomi': ['xiaomi', 'mi', 'mix', 'civi']  # Mi, Mix, Civi (removed 'redmi', 'poco' - separate brands)
        }

        for brand_name, keywords in brand_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_brand = brand_name
                break

        # FIXED: If no exact brand keyword match, try fuzzy matching for typos (e.g., "opop" → "oppo")
        if not detected_brand:
            import difflib
            # Extract potential brand words (single words that might be brand names)
            words = message_lower.split()
            for word in words:
                # Check if word is similar to any brand name
                all_brand_names = list(brand_keywords.keys())
                matches = difflib.get_close_matches(word, all_brand_names, n=1, cutoff=0.75)
                if matches:
                    detected_brand = matches[0]
                    break

        # Step 2: Remove common query words to extract model name
        query_words = [
            # Question words
            'what', 'whats', "what's", 'which', 'how', 'when', 'where', 'why', 'who',
            'what is', 'what are', 'whats the', "what's the", 'which is', 'which are',
            'how much', 'how about', 'how good', 'how is', 'how does',
            
            # Articles and determiners
            'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your',
            'its', "it's", 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            
            # Prepositions
            'of', 'in', 'on', 'at', 'to', 'for', 'with', 'from', 'by', 'about',
            'as', 'into', 'like', 'through', 'after', 'over', 'between', 'out',
            'against', 'during', 'without', 'before', 'under', 'around', 'among',
            
            # Common verbs in queries
            'tell', 'tell me', 'show', 'show me', 'give', 'give me', 'provide',
            'get', 'find', 'search', 'look', 'looking', 'want', 'need', 'have',
            'has', 'do', 'does', 'did', 'can', 'could', 'would', 'should', 'will',
            'know', 'see', 'check', 'compare', 'review',
            
            # Price-related words
            'price', 'cost', 'costs', 'priced', 'pricing', 'how much', 'worth',
            'expensive', 'cheap', 'affordable', 'budget', 'rate', 'rates',
            'value', 'rm', 'ringgit', 'dollar', 'myr', 'usd', 'sgd',
            
            # Specification-related words
            'specs', 'spec', 'specification', 'specifications', 'details', 'detail',
            'info', 'information', 'feature', 'features', 'about', 'description',
            'review', 'reviews', 'overview', 'summary', 'complete', 'full',
            'technical', 'tech', 'detailed',
            
            # Individual spec terms
            'battery', 'camera', 'display', 'screen', 'processor', 'chipset',
            'ram', 'storage', 'memory', 'performance', 'cpu', 'gpu',
            '5g', '4g', 'connectivity', 'network', 'charging', 'fast charging',
            
            # Comparison words
            'vs', 'versus', 'or', 'compare', 'comparison', 'difference', 'different',
            'better', 'best', 'worse', 'worst', 'between', 'against',
            
            # Quality/opinion words
            'good', 'bad', 'great', 'excellent', 'poor', 'better', 'best',
            'worth', 'quality', 'recommend', 'recommended', 'opinion',
            'think', 'thoughts', 'review', 'rating', 'rated',
            
            # Possession and relationships
            'my', 'your', 'his', 'her', 'their', 'our', 'mine', 'yours',
            'owned', 'own', 'have', 'has', 'had', 'got', 'getting',
            
            # Action words
            'buy', 'buying', 'purchase', 'purchasing', 'get', 'getting',
            'looking', 'search', 'searching', 'find', 'finding',
            'choose', 'choosing', 'pick', 'picking', 'select', 'selecting',
            
            # Time-related
            'new', 'old', 'latest', 'newest', 'current', 'now', 'today',
            'recent', 'recently', 'just', 'year', 'month', 'time',
            '2024', '2023', '2025', 'this year', 'last year',
            
            # Condition/state
            'available', 'availability', 'stock', 'in stock', 'out of stock',
            'released', 'launched', 'launch', 'release', 'coming', 'upcoming',
            
            # Modifiers
            'very', 'really', 'quite', 'pretty', 'too', 'so', 'such',
            'much', 'many', 'more', 'most', 'less', 'least', 'enough',
            'just', 'only', 'even', 'also', 'still', 'already',
            
            # Connecting words
            'and', 'but', 'or', 'nor', 'yet', 'so', 'because', 'since',
            'if', 'then', 'than', 'though', 'although', 'while', 'whereas',
            
            # Polite phrases
            'please', 'kindly', 'thank', 'thanks', 'sorry', 'excuse',
            'hello', 'hi', 'hey', 'can you', 'could you', 'would you',
            'may i', 'can i', 'i want', 'i need', 'i would like',
            
            # Negation
            'not', 'no', 'never', 'nothing', 'none', 'neither', 'nobody',
            "don't", "doesn't", "didn't", "won't", "wouldn't", "can't", "couldn't",
            "isn't", "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't",
            
            # Pronouns
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her',
            'us', 'them', 'myself', 'yourself', 'himself', 'herself', 'itself',
            'ourselves', 'themselves', 'someone', 'anyone', 'everyone',
            
            # Size/quantity descriptors
            'big', 'small', 'large', 'huge', 'tiny', 'mini', 'compact',
            'full', 'half', 'whole', 'entire', 'complete',
            
            # Availability questions
            'where can', 'when can', 'how can', 'can i', 'is there',
            'are there', 'do they', 'does it', 'will it',
            
            # Phone-specific query terms
            'phone', 'smartphone', 'mobile', 'device', 'handset', 'model',
            'series', 'version', 'variant', 'edition', 'type', 'kind',
            
            # Brand mentions (will be handled separately but good to remove from model name)
            'brand', 'make', 'manufacturer', 'company', 'made by',
            
            # Recommendation context
            'recommend', 'suggest', 'advice', 'opinion', 'think about',
            'thoughts on', 'what about', 'how about',
            
            # Ownership/experience
            'using', 'used', 'use', 'user', 'owner', 'owned', 'experience',
            'tried', 'tested', 'test', 'hands on',
            
            # Availability/stock
            'available in', 'sold in', 'buy from', 'purchase from',
            'shop', 'store', 'retail', 'online', 'offline',
            
            # Comparison modifiers
            'more', 'less', 'better than', 'worse than', 'same as',
            'similar to', 'like', 'unlike', 'as good as',
            
            # Uncertainty phrases
            'maybe', 'perhaps', 'possibly', 'probably', 'might', 'may',
            'could be', 'would be', 'seems', 'looks', 'appears',
            
            # Question starters
            'is it', 'does it', 'can it', 'will it', 'should i',
            'would it', 'has it', 'do you', 'did you', 'have you',
            
            # Color/appearance (unless part of actual model name)
            'color', 'colour', 'black', 'white', 'blue', 'red', 'green',
            'silver', 'gold', 'gray', 'grey', 'pink', 'purple', 'yellow',
            
            # Condition descriptors
            'new', 'used', 'refurbished', 'second hand', 'original',
            'genuine', 'authentic', 'fake', 'real', 'official',
            
            # Size descriptors that aren't part of model names
            'inch', 'inches', 'cm', 'mm', 'gram', 'grams', 'kg',
            
            # Performance descriptors
            'fast', 'slow', 'smooth', 'laggy', 'powerful', 'weak',
            'strong', 'reliable', 'unreliable', 'stable', 'unstable',
            
            # Value judgments
            'worth buying', 'worth it', 'worthwhile', 'overpriced',
            'underpriced', 'fair price', 'reasonable', 'unreasonable',
            
            # Possession questions
            'have you', 'do you have', 'got any', 'any available',
            'in your', 'from your',
            
            # General descriptors
            'nice', 'beautiful', 'ugly', 'pretty', 'amazing', 'awesome',
            'terrible', 'horrible', 'fantastic', 'wonderful', 'perfect',
            
            # Technical jargon (common non-model terms)
            'flagship', 'mid range', 'entry level', 'budget', 'premium',
            'high end', 'low end', 'top tier', 'bottom tier',
            
            # Launch/release terms
            'when will', 'when did', 'release date', 'launch date',
            'coming out', 'come out', 'announced', 'announcement',
            
            # Update/version terms (unless part of model)
            'update', 'updated', 'version', 'upgraded', 'upgrade',
            'downgrade', 'downgraded', 'software', 'firmware',
            
            # Measurement units
            'mp', 'megapixel', 'mah', 'gb', 'tb', 'hz', 'ghz',
            'watt', 'w', 'v', 'volt', 'amp', 'ampere',
            
            # Punctuation words
            'yes', 'no', 'ok', 'okay', 'sure', 'fine', 'alright',
            'yeah', 'yep', 'nope', 'yup', 'uh', 'um', 'hmm',
            
            # Internet slang (common in queries)
            'lol', 'btw', 'omg', 'tbh', 'imo', 'imho', 'fyi',
            'asap', 'etc', 'aka', 'ps',
        ]

        cleaned_message = message_lower
        for word in query_words:
            cleaned_message = cleaned_message.replace(word, ' ')

        # Also remove brand keywords from cleaned message to get just the model
        # CRITICAL FIX: Only remove the primary brand name, not secondary keywords
        # Example: For "samsung galaxy f07", remove "samsung" but keep "galaxy" (part of model name)
        if detected_brand:
            # Only remove the detected brand name itself, not all keywords
            cleaned_message = cleaned_message.replace(detected_brand, ' ')

        # Clean up extra spaces
        cleaned_message = ' '.join(cleaned_message.split()).strip()

        if len(cleaned_message) < 2:  # Too short to be a phone model
            return None

        # Step 3: Search with brand filtering if brand was detected
        if detected_brand:
            # Search within the detected brand first
            brand_obj = Brand.query.filter(Brand.name.ilike(f'%{detected_brand}%')).first()

            if brand_obj:
                # Strategy 1: Exact model name match within brand
                phones = Phone.query.filter(
                    Phone.is_active == True,
                    Phone.brand_id == brand_obj.id,
                    Phone.model_name.ilike(f'%{cleaned_message}%')
                ).limit(5).all()

                if phones:
                    return phones

                # Strategy 2: Try with original message (brand + model)
                phones = Phone.query.join(Brand).filter(
                    Phone.is_active == True,
                    Phone.brand_id == brand_obj.id,
                    or_(
                        Phone.model_name.ilike(f'%{message_lower}%'),
                        func.concat(func.concat(Brand.name, ' '), Phone.model_name).ilike(f'%{message_lower}%')
                    )
                ).limit(5).all()

                if phones:
                    return phones

                # Strategy 3: For Samsung, also try without "Galaxy" keyword
                # Example: "galaxy f07" → also try "f07"
                if detected_brand == 'samsung' and 'galaxy' in cleaned_message:
                    cleaned_without_galaxy = cleaned_message.replace('galaxy', ' ').strip()
                    if len(cleaned_without_galaxy) >= 2:
                        phones = Phone.query.filter(
                            Phone.is_active == True,
                            Phone.brand_id == brand_obj.id,
                            Phone.model_name.ilike(f'%{cleaned_without_galaxy}%')
                        ).limit(5).all()

                        if phones:
                            return phones

        # Step 4: Fallback - search without brand filtering
        # Strategy 1: Search model_name directly (e.g., "galaxy s23 fe")
        phones = Phone.query.join(Brand).filter(
            Phone.is_active == True,
            Phone.model_name.ilike(f'%{cleaned_message}%')
        ).limit(5).all()

        if phones:
            return phones

        # Strategy 2: Search brand + model together (e.g., "samsung galaxy s23 fe")
        phones = Phone.query.join(Brand).filter(
            Phone.is_active == True,
            or_(
                func.concat(func.concat(Brand.name, ' '), Phone.model_name).ilike(f'%{cleaned_message}%'),
                func.concat(func.concat(Phone.model_name, ' '), Brand.name).ilike(f'%{cleaned_message}%')
            )
        ).limit(5).all()

        if phones:
            return phones

        # Strategy 3: Fuzzy matching (ML-enhanced) - find closest matches
        # This makes the chatbot more intelligent and flexible
        def similarity(a, b):
            """Calculate similarity ratio between two strings"""
            return SequenceMatcher(None, a.lower(), b.lower()).ratio()

        # CRITICAL FIX: Extract model numbers from query for exact matching
        import re
        query_numbers = re.findall(r'\d+', cleaned_message)

        # Get all phones from the detected brand (or all phones if no brand)
        if detected_brand:
            brand_obj = Brand.query.filter(Brand.name.ilike(f'%{detected_brand}%')).first()
            if brand_obj:
                candidate_phones = Phone.query.filter_by(brand_id=brand_obj.id, is_active=True).all()
            else:
                candidate_phones = Phone.query.filter_by(is_active=True).limit(100).all()
        else:
            # No specific brand - search all phones (limited to 200 for performance)
            candidate_phones = Phone.query.filter_by(is_active=True).limit(200).all()

        # Score each phone based on similarity to cleaned_message
        scored_phones = []
        for phone in candidate_phones:
            # Try multiple similarity scores
            model_score = similarity(cleaned_message, phone.model_name)
            brand_model_score = similarity(cleaned_message, f"{phone.brand.name} {phone.model_name}")

            # Use the best score
            best_score = max(model_score, brand_model_score)

            # CRITICAL FIX: Boost score if model numbers match exactly
            # This prevents "14 pro" from matching "15 pro", "11 pro", etc.
            if query_numbers:
                model_numbers = re.findall(r'\d+', phone.model_name)
                # If all query numbers are found in model name, boost score
                if all(num in model_numbers for num in query_numbers):
                    best_score += 0.3  # Significant boost for exact number match
                # If ANY query number matches, small boost (allows partial matches)
                elif any(num in model_numbers for num in query_numbers):
                    best_score += 0.1  # Small boost for partial number match
                # If query has number but NO numbers match at all, heavy penalty
                # FIXED: Increased penalty to prevent "A78" matching "A98", "A38"
                elif model_numbers:
                    best_score -= 0.5  # Heavy penalty when NO numbers match

            # Only include if similarity is above threshold
            # FIXED: Lowered from 0.6 to 0.5 for better fuzzy matching when exact models don't exist
            if best_score >= 0.5:
                scored_phones.append((phone, best_score))

        # CRITICAL FIX: Sort by RELEASE_DATE first (newest first), then by similarity score
        # This ensures "Zenfone 12 and Redmi Note 14" shows NEWEST models, not oldest
        from datetime import datetime
        scored_phones.sort(key=lambda x: (
            x[0].release_date if x[0].release_date else datetime(1900, 1, 1).date(),  # Newest first
            x[1]  # Then by similarity score
        ), reverse=True)

        # Return top 5 matches
        if scored_phones:
            return [phone for phone, score in scored_phones[:5]]

        return None

    def _handle_specific_phone_query(self, message, phones, is_multi_model=False):
        """Handle query about specific phone model

        Args:
            message: User's message
            phones: Phone object or list of Phone objects
            is_multi_model: True if phones come from multi-model extraction (e.g., "phone1 and phone2")
        """
        message_lower = message.lower()

        # CRITICAL FIX: Skip variant filtering for multi-model queries
        # When user explicitly asks for multiple different phones (e.g., "mate 70 air and galaxy f07"),
        # we should show ALL the phones they asked for, not filter based on keywords
        if len(phones) > 1 and not is_multi_model:
            # Variant keywords are modifiers that create variants of a base model (e.g., "Pro", "Max")
            variant_keywords = ['pro', 'max', 'plus', 'ultra', 'mini', 'lite', 'edge', 'fold', 'flip', 'air']
            # Model line keywords identify different product lines within a brand (e.g., "Note", "GT", "Hot")
            model_line_keywords = ['note', 'hot', 'smart', 'a', 'c', 'f', 'y', 'x', 'v', 'k', 'p', 'z', 'gt', 'magic', 'nova']

            # Check which variant keywords are in the user's message
            mentioned_variants = [kw for kw in variant_keywords if kw in message_lower]

            # CRITICAL FIX: Extract model line from query (e.g., "gt" from "gt 30")
            # This helps filter out different model lines like "Note 30" vs "GT 30"
            mentioned_model_lines = [kw for kw in model_line_keywords if kw in message_lower]

            if mentioned_variants:
                # User specified a variant - filter to show ONLY phones matching that variant
                # Example: "realme 14 pro" should show ONLY Pro variants (14 Pro, 14 Pro Plus, 14 Pro Lite)
                # but NOT base models (14, 14X)
                filtered_phones = []
                for phone in phones:
                    model_lower = phone.model_name.lower()
                    # Check if this phone matches ANY of the mentioned variants
                    if any(variant in model_lower for variant in mentioned_variants):
                        filtered_phones.append(phone)

                # Use filtered phones if we found any, otherwise use all
                if filtered_phones:
                    phones = filtered_phones
            elif mentioned_model_lines:
                # CRITICAL FIX: User specified a model line (e.g., "GT 30")
                # Filter to show ONLY phones from that model line
                # Example: "infinix gt 30" should show ONLY GT 30, NOT Note 30i or Hot 30
                filtered_phones = []
                for phone in phones:
                    model_lower = phone.model_name.lower()
                    # Check if phone matches ALL mentioned model lines
                    if all(line in model_lower for line in mentioned_model_lines):
                        # Also check that phone doesn't have UNMENTIONED variant keywords
                        has_unmentioned_variant = any(
                            variant in model_lower and variant not in mentioned_variants
                            for variant in variant_keywords
                        )
                        if not has_unmentioned_variant:
                            filtered_phones.append(phone)

                if filtered_phones:
                    phones = filtered_phones
            # If no variant or model line keyword mentioned, show ALL phones (base + all variants)
            # Example: "iphone 17" should show iPhone 17, 17 Air, 17 Pro, 17 Pro Max

        # Determine what information is being requested
        is_price_query = any(word in message_lower for word in ['price', 'cost', 'how much', 'rm'])
        is_spec_query = any(word in message_lower for word in ['specs', 'specification', 'spec'])
        is_battery_query = 'battery' in message_lower

        if len(phones) == 1:
            phone = phones[0]
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

            response = f"📱 **{phone.brand.name} {phone.model_name}**\n\n"

            # Always show price
            response += f"💰 **Price:** RM{phone.price:,.2f}\n\n"

            # Show specific information based on query
            if is_price_query and not is_spec_query and not is_battery_query:
                # Price only - already shown above
                pass
            elif is_battery_query and specs and specs.battery_capacity:
                # Battery specific query
                response += f"🔋 **Battery:** {specs.battery_capacity}mAh\n"
                if specs.fast_charging_wattage:
                    response += f"⚡ **Fast Charging:** {specs.fast_charging_wattage}W\n"
            elif is_spec_query or (not is_price_query and not is_battery_query):
                # Full specs
                if specs:
                    response += "📊 **Key Specifications:**\n"
                    if specs.processor:
                        response += f"   • Processor: {specs.processor}\n"
                    if specs.ram_options:
                        response += f"   • RAM: {specs.ram_options}\n"
                    if specs.storage_options:
                        response += f"   • Storage: {specs.storage_options}\n"
                    if specs.screen_size and specs.screen_type:
                        response += f"   • Display: {specs.screen_size}\" {specs.screen_type}\n"
                    if specs.rear_camera_main:
                        response += f"   • Main Camera: {specs.rear_camera_main}MP\n"
                    if specs.battery_capacity:
                        response += f"   • Battery: {specs.battery_capacity}mAh\n"
                    if specs.has_5g:
                        response += f"   • 5G: Yes ✅\n"

            # Add View Details button
            response += f"\n👉 [View Full Details](/phone/{phone.id})"

            return {
                'response': response,
                'type': 'phone_details',
                'metadata': {
                    'phones': [{
                        'id': phone.id,
                        'name': phone.model_name,
                        'brand': phone.brand.name,
                        'price': phone.price,
                        'image': phone.main_image,
                        'url': f'/phone/{phone.id}'
                    }]
                }
            }

        elif len(phones) > 1:
            # Multiple phones match - show all with prices and view details
            response = f"I found {len(phones)} phones matching your query:\n\n"
            phone_list = []

            for phone in phones:
                response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                response += f"   👉 [View Details](/phone/{phone.id})\n"
                phone_list.append({
                    'id': phone.id,
                    'name': phone.model_name,
                    'brand': phone.brand.name,
                    'price': phone.price,
                    'image': phone.main_image,
                    'url': f'/phone/{phone.id}'
                })

            response += "\nClick any link above to see full details!"

            return {
                'response': response,
                'type': 'recommendation',
                'metadata': {'phones': phone_list}
            }

        return None
    # END NEW METHODS

    def _extract_budget(self, message):
        """Extract budget range from message"""
        # Look for patterns like "RM1000", "1000", "under 2000", "within 3000", "near 3000", "between 1000 and 2000"
        # IMPORTANT: Avoid matching specification numbers like "5000mah" or "108mp"

        patterns = [
           # Range patterns with RM on both sides
            (r'(?:rm|RM)\s*(\d+)\s*(?:to|-|and)\s*(?:rm|RM)\s*(\d+)', 'range'),  # RM1000 to RM2000 or rm 1000 to rm 2000
            # Near with range pattern (e.g., "near 2000-3000" or "near 2000 to 3000")
            (r'near\s*(?:rm\s*)?(\d+)\s*(?:to|-)\s*(?:rm\s*)?(\d+)', 'range'),  # near 2000-3000 or near rm2000 to rm3000
            # Range patterns without RM (but not followed by spec keywords)
            (r'(\d+)\s*(?:to|-|and)\s*(\d+)(?!\s*(?:mah|mp|gb|hz|inch|mm))', 'range'),  # 1000 to 2000

            # Above patterns WITH RM (with or without space)
            (r'(?:above|over|more than)\s+(?:rm|RM)\s*(\d+)', 'min'),  # above RM3000 or above rm 3000
            # Above patterns WITHOUT RM (but not followed by spec keywords)
            (r'(?:above|over|more than)\s+(\d+)(?!\s*(?:mah|mp|gb|hz|inch|mm))', 'min'),  # above 3000

            # Within/under/below/max/maximum patterns WITH RM (with or without space)
            (r'(?:within|under|below|max|maximum)\s+(?:rm|RM)\s*(\d+)', 'max'),  # within RM2000 or within rm 2000
            # Within/under/below/max/maximum patterns WITHOUT RM (but not followed by spec keywords)
            (r'(?:within|under|below|max|maximum)\s+(\d+)(?!\s*(?:mah|mp|gb|hz|inch|mm))', 'max'),  # within 2000

            # Near/around single value pattern (±500 range) - but not spec numbers
            (r'(?:near|around)\s+(?:rm\s*)?(\d+)(?!\s*(?:mah|mp|gb|hz|inch|mm))', 'near'),  # near 2000 or near rm2000

            # Single RM value (with or without space)
            (r'(?:rm|RM)\s*(\d+)', 'single'),  # RM2000 or rm 2000

            # Standalone number (3-5 digits) - but not followed by spec keywords
            (r'(?:^|\s)(\d{3,5})(?!\s*(?:mah|mp|gb|hz|inch|mm))(?:\s|$)', 'single'),  # 1000, 2000, etc.
        ]

        for pattern, pattern_type in patterns:

            match = re.search(pattern, message.lower())

            if match:

                # Handle based on pattern type

                if pattern_type == 'range':

                    # Range pattern (e.g., "1000-2000", "near 1000-2000")

                    return (int(match.group(1)), int(match.group(2)))



                elif pattern_type == 'min':

                    # Minimum budget pattern (e.g., "above 3000", "over rm 5000")

                    min_budget = int(match.group(1))

                    return (min_budget, 15000)  # Set reasonable upper limit



                elif pattern_type == 'max':

                    # Maximum budget pattern (e.g., "under 2000", "within rm 3000")

                    max_budget = int(match.group(1))

                    return (500, max_budget)



                elif pattern_type == 'near':

                    # Near/around pattern (±500 range)

                    center = int(match.group(1))

                    return (max(500, center - 500), center + 500)



                elif pattern_type == 'single':

                    # Single value mentioned (assume max budget)

                    value = int(match.group(1))
                    return (500, value)

        return None

    def _extract_battery_threshold(self, message):
        """
        Extract battery capacity threshold from message (in mAh)
        Examples:
        - "phone above 5000mah" → 5000
        - "battery above 6000 mah" → 6000
        - "5000mah battery" → 5000
        Returns: int or None
        """
        message_lower = message.lower()

        # Patterns for battery threshold
        patterns = [
            r'(?:above|over|more than|at least)\s+(\d+)\s*mah',  # above 5000mah
            r'(?:above|over|more than|at least)\s+(\d+)\s+mah',  # above 5000 mah
            r'(\d+)\s*mah\s+(?:or|and)\s+(?:above|more|higher)',  # 5000mah or above
            r'battery\s+(?:above|over|at least)\s+(\d+)',  # battery above 5000
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))

        return None

    def _extract_camera_threshold(self, message):
        """
        Extract camera MP threshold from message
        Examples:
        - "camera above 100mp" → 100
        - "phone above 64 mp camera" → 64
        - "108mp camera" → 108
        Returns: int or None
        """
        message_lower = message.lower()

        # Patterns for camera threshold
        patterns = [
            r'camera\s+(?:above|over|more than|at least)\s+(\d+)\s*mp',  # camera above 100mp
            r'(?:above|over|more than|at least)\s+(\d+)\s*mp\s+camera',  # above 100mp camera
            r'(\d+)\s*mp\s+(?:or|and)\s+(?:above|more|higher)',  # 100mp or above
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))

        return None

    def _extract_ram_requirement(self, message):
        """
        Extract RAM requirement from message
        Examples:
        - "12GB RAM" → 12
        - "8gb ram phone" → 8
        - "phone with 16gb" → 16
        Returns: int (GB) or None
        """
        message_lower = message.lower()

        # Patterns for RAM requirement
        patterns = [
            r'(\d+)\s*gb\s+ram',  # 12gb ram, 8 gb ram
            r'ram\s+(\d+)\s*gb',  # ram 12gb, ram 8 gb
            r'(\d+)\s*gb(?:\s+of)?\s+(?:memory|ram)',  # 12gb of memory
            r'with\s+(\d+)\s*gb(?:\s+ram)?',  # with 12gb, with 12gb ram
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                return int(match.group(1))

        return None

    def _extract_storage_requirement(self, message):
        """
        Extract storage requirement from message
        Examples:
        - "256GB storage" → 256
        - "512gb" → 512
        - "phone with 128gb storage" → 128
        Returns: int (GB) or None
        """
        message_lower = message.lower()

        # Patterns for storage requirement
        patterns = [
            r'(\d+)\s*gb\s+storage',  # 256gb storage, 128 gb storage
            r'storage\s+(\d+)\s*gb',  # storage 256gb
            r'(\d+)\s*gb(?:\s+of)?\s+(?:internal\s+)?storage',  # 256gb of storage
            r'with\s+(\d+)\s*gb\s+storage',  # with 256gb storage
            # Match standalone storage values (but not RAM)
            r'(?<!ram\s)(?<!memory\s)(\d+)\s*gb(?:\s|$|,)(?!\s*ram)(?!\s*memory)',  # 256gb (but not "8gb ram")
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                storage_val = int(match.group(1))
                # Storage is usually 64GB or more, RAM is usually 16GB or less
                # This helps disambiguate "12gb" from "256gb"
                if storage_val >= 32:  # Likely storage, not RAM
                    return storage_val

        return None

    def _extract_5g_requirement(self, message):
        """
        Check if 5G is required from message
        Examples:
        - "5g phone" → True
        - "with 5g" → True
        - "5g support" → True
        Returns: bool
        """
        message_lower = message.lower()

        # Patterns for 5G requirement
        patterns = [
            r'\b5g\b',  # 5g (with word boundaries)
            r'5g\s+(?:phone|support|network|connectivity|enabled)',
            r'(?:with|has)\s+5g',
        ]

        for pattern in patterns:
            if re.search(pattern, message_lower):
                return True

        return False

    def _filter_phones_by_brand(self, phones_items, wanted_brands, unwanted_brands):
        """
        Filter phone results by wanted/unwanted brands

        Args:
            phones_items: List of phone items (dict with 'phone' key)
            wanted_brands: List of brand names to include
            unwanted_brands: List of brand names to exclude

        Returns:
            Filtered list of phone items
        """
        if not wanted_brands and not unwanted_brands:
            return phones_items

        filtered = []
        for item in phones_items:
            phone = item.get('phone')
            if not phone or not hasattr(phone, 'brand'):
                continue

            brand_name = phone.brand.name if hasattr(phone.brand, 'name') else str(phone.brand)

            # Check unwanted brands first
            if unwanted_brands and brand_name in unwanted_brands:
                continue

            # Check wanted brands
            if wanted_brands and brand_name not in wanted_brands:
                continue

            filtered.append(item)

        return filtered

    def _contains_malicious_intent(self, message):
        """
        Detect malicious, attack, or inappropriate queries
        Returns True if message contains negative/attack keywords

        Examples:
        - "i want to hack xiaomi" → True (contains "hack")
        - "steal phone" → True (contains "steal")
        - "crack samsung" → True (contains "crack")
        - "xiaomi phone" → False (legitimate query)
        """
        message_lower = message.lower()

        # Malicious/attack keywords that indicate inappropriate queries
        malicious_keywords = [
            # Hacking & Unauthorized Access
            'hack', 'hacking', 'hacker', 'hacked', 'hax', 'h4ck',
            'exploit', 'exploiting', 'exploited', 'vulnerability', 'vuln',
            'breach', 'breaching', 'breached', 'penetrate', 'penetration',
            'backdoor', 'rootkit', 'shell', 'remote access',
            'brute force', 'bruteforce', 'dictionary attack',
            'sql injection', 'xss', 'csrf', 'code injection',
            'zero day', 'zeroday', '0day',
            
            # Theft & Stealing
            'steal', 'stealing', 'theft', 'stolen', 'thief',
            'rob', 'robbing', 'robbery', 'robbed',
            'swipe', 'snatch', 'pilfer', 'loot',
            
            # Cracking & Breaking
            'crack', 'cracking', 'cracked', 'cracker',
            'break', 'breaking', 'broke', 'broken',
            'bypass', 'bypassing', 'bypassed',
            'circumvent', 'workaround', 'evade',
            
            # Malware & Viruses
            'malware', 'virus', 'trojan', 'worm',
            'ransomware', 'spyware', 'adware', 'keylogger',
            'botnet', 'rat', 'remote administration tool',
            'payload', 'dropper', 'backdoor',
            
            # Fraud & Scams
            'fraud', 'fraudulent', 'scam', 'scammer', 'scamming',
            'fake', 'counterfeit', 'forged', 'phishing',
            'spoof', 'spoofing', 'impersonate', 'impersonation',
            'ponzi', 'pyramid scheme',
            
            # Illegal Activities
            'illegal', 'unlawful', 'illicit', 'criminal',
            'pirate', 'piracy', 'pirated', 'warez',
            'torrent', 'crack download', 'keygen',
            'serial key', 'activation code', 'license crack',
            
            # Device Manipulation
            'jailbreak', 'jailbreaking', 'jailbroken',
            'root', 'rooting', 'rooted', 'superuser',
            'unlock bootloader', 'bootloader unlock',
            'custom rom', 'flash rom', 'mod',
            'remove lock', 'bypass lock', 'unlock stolen',
            'imei change', 'imei hack', 'network unlock',
            'carrier unlock', 'sim unlock',
            
            # Security Bypass
            'bypass security', 'disable security', 'remove security',
            'bypass password', 'password crack', 'password reset hack',
            'bypass frp', 'frp bypass', 'factory reset protection',
            'bypass mdm', 'remove mdm', 'mdm bypass',
            'bypass authentication', 'disable encryption',
            
            # Attack Methods
            'attack', 'attacking', 'attacked', 'attacker',
            'dos', 'ddos', 'denial of service',
            'man in the middle', 'mitm',
            'session hijack', 'packet sniff', 'intercept',
            'eavesdrop', 'wiretap', 'surveillance',
            
            # Data Theft
            'data breach', 'data leak', 'leak data',
            'extract data', 'dump database', 'database dump',
            'scrape data', 'harvest data',
            'steal credentials', 'steal password', 'phish',
            
            # Damage & Destruction
            'destroy', 'damage', 'sabotage', 'vandalize',
            'corrupt', 'corrupting', 'brick', 'bricking',
            'delete system', 'wipe data malicious',
            
            # Surveillance & Spying
            'spy', 'spying', 'spyware', 'monitor secretly',
            'track without permission', 'stalk', 'stalking',
            'hidden camera', 'secret recording',
            'keylogger', 'screen capture malicious',
            
            # Social Engineering
            'social engineering', 'manipulate', 'trick',
            'pretexting', 'baiting', 'tailgate',
            
            # Money-related Fraud
            'money laundering', 'embezzle', 'extort', 'blackmail',
            'credit card fraud', 'identity theft', 'wire fraud',
            
            # Network Attacks
            'port scan', 'network scan', 'vulnerability scan malicious',
            'packet injection', 'arp spoofing', 'dns poisoning',
            
            # Cryptocurrency Attacks
            'crypto mining malware', 'cryptojacking',
            'wallet hack', 'blockchain attack',
            
            # Mobile-specific Attacks
            'sms bombing', 'call flooding', 'sim swap',
            'baseband exploit', 'modem hack',
            
            # Evasion Techniques
            'hide malware', 'obfuscate code', 'anti-detection',
            'sandbox escape', 'vm detection bypass',
            
            # Harmful Intent Indicators
            'how to harm', 'destroy someone', 'revenge hack',
            'get back at', 'teach them lesson hack',
            
            # Brand-specific Attacks (add more as needed)
            'xiaomi exploit', 'samsung vulnerability hack',
            'iphone jailbreak stolen', 'huawei backdoor',
            
            # l33t speak variations (common obfuscations)
            'h4ck', 'cr4ck', 'expl0it', 'br3ach',
            'pwn', 'pwned', 'pwning', '0wn', 'owned',
            
            # Combination phrases (high confidence indicators)
            'steal phone', 'hack phone', 'crack phone',
            'bypass icloud', 'remove google account',
            'unlock without password', 'access without permission',
            
            # Tools commonly used for attacks
            'metasploit', 'burp suite malicious', 'kali linux hack',
            'nmap malicious', 'wireshark intercept', 'aircrack',
            
            # Additional suspicious intents
            'unauthorized access', 'without authorization',
            'without permission', 'illegally access',
            'black hat', 'grey hat', 'dark web'
        ]

        # Check if any malicious keyword is present
        for keyword in malicious_keywords:
            # Use word boundary to avoid false positives
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, message_lower):
                return True

        # CRITICAL FIX: Fuzzy matching for typos (e.g., "hake" → "hack", "h@ck" → "hack")
        # Common typos and obfuscations of dangerous keywords
        from difflib import SequenceMatcher

        # Common typo variants (manually added for high-confidence detection)
        typo_variants = ['hake', 'hak', 'hakc', 'hac', 'haack',  # hack typos
                        'stel', 'stea', 'steall',  # steal typos
                        'crk', 'crak', 'crakc',  # crack typos
                        'expl0it', 'exployt']  # exploit typos

        words = message_lower.split()
        for word in words:
            # Check typo variants first
            if word in typo_variants:
                return True

            # Then check similarity with critical keywords
            critical_keywords = ['hack', 'steal', 'crack', 'exploit', 'breach', 'jailbreak', 'root']
            for critical in critical_keywords:
                # Check similarity ratio (>= 0.75 catches more typos)
                similarity = SequenceMatcher(None, word, critical).ratio()
                if similarity >= 0.75 and len(word) >= 3:
                    return True  # Likely malicious intent with typo

        return False
    
    def _is_phone_related(self, message):
        """Check if the message is related to phones/smartphones"""
        message_lower = message.lower()

        # SAFETY CHECK: Reject malicious/attack queries first
        if self._contains_malicious_intent(message):
            return False

        # Phone-related keywords
        phone_keywords = [
            # General Device Terms
            'phone', 'smartphone', 'mobile', 'device', 'handset', 
            'cell', 'cellular', 'telephone', 'cellphone', 'mobile phone',
            'smart phone', 'feature phone', 'flip phone', 'slider phone',
            'phablet', 'mini phone', 'compact phone',
            
            # Operating Systems
            'android', 'ios', 'iphone os', 'one ui', 'miui', 'coloros',
            'funtouch', 'emui', 'harmonyos', 'oxygenos', 'realme ui',
            'flyme', 'magic ui', 'origin os', 'pixel experience',
            
            # Major Brands
            'iphone', 'samsung', 'galaxy', 'xiaomi', 'redmi', 'poco',
            'huawei', 'honor', 'oppo', 'vivo', 'realme', 'oneplus',
            'google pixel', 'pixel', 'motorola', 'moto', 'nokia',
            'sony xperia', 'xperia', 'lg', 'asus', 'rog phone',
            'zenfone', 'blackberry', 'htc', 'lenovo', 'zte',
            'meizu', 'infinix', 'tecno', 'itel', 'alcatel',
            'nothing phone', 'fairphone', 'cat phone', 'doogee',
            'ulefone', 'blackview', 'oukitel', 'umidigi',
            
            # Popular Model Series
            's series', 'note series', 'ultra', 'plus', 'pro', 'max',
            'lite', 'mini', 'fold', 'flip', 'edge', 'a series',
            'm series', 'f series', 'k series', 'mi series',
            'redmi note', 'galaxy s', 'galaxy a', 'galaxy z',
            'iphone pro', 'iphone plus', 'se', 'xr', 'xs',
            
            # Display/Screen Terms
            'screen', 'display', 'lcd', 'oled', 'amoled', 'super amoled',
            'retina', 'gorilla glass', 'screen size', 'inch display',
            'resolution', 'pixel density', 'ppi', 'refresh rate',
            '60hz', '90hz', '120hz', '144hz', 'adaptive sync',
            'hdr', 'hdr10', 'hdr10+', 'dolby vision',
            'notch', 'punch hole', 'bezel', 'screen protector',
            'tempered glass', 'curved screen', 'flat display',
            'foldable screen', 'flexible display',
            
            # Camera Terms
            'camera', 'megapixel', 'mp camera', 'front camera',
            'rear camera', 'selfie camera', 'main camera',
            'ultra wide', 'telephoto', 'macro', 'depth sensor',
            'periscope', 'optical zoom', 'digital zoom', 'hybrid zoom',
            'night mode', 'portrait mode', 'pro mode', 'ai camera',
            'image stabilization', 'ois', 'eis', 'gimbal',
            '4k video', '8k video', 'slow motion', 'time lapse',
            'dual camera', 'triple camera', 'quad camera', 'penta camera',
            'camera setup', 'lens', 'aperture', 'sensor size',
            
            # Battery & Charging
            'battery', 'mah', 'battery life', 'battery capacity',
            'charging', 'fast charging', 'quick charge', 'rapid charge',
            'super vooc', 'warp charge', 'dash charge', 'turbo charge',
            'wireless charging', 'reverse charging', 'power bank',
            'battery drain', 'screen on time', 'standby time',
            '15w', '18w', '25w', '33w', '45w', '65w', '120w', '150w',
            'charger', 'charging speed', 'charging cable', 'usb-c',
            
            # Processor/Performance
            'processor', 'chipset', 'cpu', 'gpu', 'soc',
            'snapdragon', 'dimensity', 'exynos', 'kirin', 'bionic',
            'helio', 'tensor', 'unisoc', 'mediatek',
            'performance', 'benchmark', 'antutu', 'geekbench',
            'gaming performance', 'multitasking', 'smooth',
            'lag', 'heating', 'thermal', 'throttling',
            
            # Memory & Storage
            'ram', 'rom', 'storage', 'internal storage', 'memory',
            'gb ram', 'gb storage', 'expandable storage', 'sd card',
            'micro sd', 'ufs', 'emmc', 'nvme',
            '64gb', '128gb', '256gb', '512gb', '1tb',
            '4gb ram', '6gb ram', '8gb ram', '12gb ram', '16gb ram',
            
            # Connectivity
            '5g', '4g', 'lte', '3g', 'network', 'connectivity',
            'wifi', 'wi-fi', 'bluetooth', 'nfc', 'infrared',
            'gps', 'dual sim', 'dual standby', 'esim',
            'wifi 6', 'wifi 6e', 'wifi 7', 'bluetooth 5.0',
            'usb-c', 'usb type-c', 'micro usb', 'headphone jack',
            '3.5mm jack', 'aux port',
            
            # Features & Sensors
            'fingerprint', 'face unlock', 'face id', 'in-display fingerprint',
            'side mounted', 'rear fingerprint', 'biometric',
            'sensor', 'proximity sensor', 'gyroscope', 'accelerometer',
            'compass', 'barometer', 'ambient light',
            'water resistant', 'ip67', 'ip68', 'ip rating',
            'dust proof', 'splash proof', 'waterproof',
            
            # Audio
            'speaker', 'stereo speaker', 'dual speaker', 'mono speaker',
            'dolby atmos', 'audio quality', 'microphone',
            'noise cancellation', 'call quality', 'earpiece',
            
            # Build & Design
            'design', 'build quality', 'premium', 'plastic', 'metal',
            'glass back', 'matte finish', 'glossy', 'color',
            'weight', 'dimensions', 'thickness', 'slim', 'compact',
            'ergonomic', 'grip', 'button placement',
            
            # Software & UI
            'software', 'firmware', 'update', 'android version',
            'android 14', 'android 13', 'ios 17', 'ios 16',
            'system update', 'security patch', 'bloatware',
            'custom rom', 'stock android', 'clean ui',
            'features', 'customization', 'themes', 'launcher',
            
            # Price & Value
            'price', 'cost', 'budget', 'affordable', 'cheap',
            'expensive', 'value for money', 'worth it', 'deal',
            'discount', 'offer', 'sale', 'promotion',
            'flagship', 'mid range', 'entry level', 'premium',
            'best phone', 'top phone', 'phone under',
            
            # Usage & Requirements
            'gaming phone', 'camera phone', 'photography',
            'video recording', 'content creation', 'vlogging',
            'business phone', 'work phone', 'daily driver',
            'backup phone', 'second phone', 'spare phone',
            
            # Accessories
            'case', 'cover', 'screen guard', 'protector',
            'charger', 'cable', 'earphone', 'earbuds',
            'power adapter', 'accessories',
            
            # Shopping/Purchase Terms
            'buy', 'purchase', 'recommend', 'recommendation',
            'suggest', 'suggestion', 'best', 'top', 'which phone',
            'what phone', 'should i buy', 'worth buying',
            'comparison', 'compare', 'vs', 'versus', 'or',
            'difference between', 'better', 'best option',
            
            # Technical Specs
            'specification', 'specs', 'spec sheet', 'features list',
            'full specs', 'technical details', 'review',
            'hands on', 'unboxing', 'first impression',
            
            # Issues/Problems
            'problem', 'issue', 'error', 'bug', 'glitch',
            'not working', 'broken', 'repair', 'fix',
            'troubleshoot', 'warranty', 'service center',
            
            # Carrier/Network
            'carrier', 'network provider', 'operator',
            'sim card', 'prepaid', 'postpaid', 'plan',
            'data plan', 'unlimited', 'coverage',
            
            # Second-hand/Used
            'used phone', 'second hand', 'refurbished',
            'pre owned', 'reconditioned', 'renewed',
            
            # Release/Launch
            'launch', 'release', 'launch date', 'coming soon',
            'upcoming', 'leaked', 'rumor', 'announcement',
            'pre order', 'available', 'in stock',
            
            # Ratings/Reviews
            'rating', 'review', 'user review', 'expert review',
            'pros and cons', 'advantage', 'disadvantage',
            'good', 'bad', 'excellent', 'poor',
            
            # Common Questions
            'how much', 'which is better', 'is it good',
            'should i get', 'worth it', 'recommend for',
            'suitable for', 'good for', 'best for',
            
            # Regional/Market Terms
            'global version', 'china version', 'international',
            'variant', 'model number', 'region lock',
            
            # Measurements
            'inch', 'mm', 'cm', 'gram', 'ounce', 'hz', 'ghz'
        ]

        # CRITICAL FIX: Check for strong phone keywords first
        # These are keywords that clearly indicate phone-related queries
        strong_keywords = [
            'phone', 'smartphone', 'mobile', 'device', 'handset', 'iphone',
            'android', 'samsung', 'galaxy', 'xiaomi', 'huawei', 'oppo', 'vivo',
            'realme', 'pixel', 'oneplus', 'honor', 'infinix', 'poco', 'redmi',
            'camera phone', 'gaming phone', 'budget phone', 'flagship'
        ]

        has_strong_keyword = any(keyword in message_lower for keyword in strong_keywords)

        # Check if any brand is mentioned (brands are phone-related)
        has_brand = bool(self._extract_multiple_brands(message))

        # Check if budget is mentioned (likely phone shopping)
        has_budget = bool(self._extract_budget(message))

        # CRITICAL FIX: Require strong evidence of phone-related intent
        # Don't treat generic words like "buy" alone as phone-related
        if has_strong_keyword or has_brand:
            return True

        # If has budget AND other phone keywords, likely phone-related
        if has_budget:
            weak_keywords = ['spec', 'display', 'battery', 'camera', 'ram', 'storage', '5g', '4g']
            if any(keyword in message_lower for keyword in weak_keywords):
                return True

        # Check for phone keyword combinations (need at least 2 phone-related terms)
        phone_keyword_count = sum(1 for keyword in phone_keywords if keyword in message_lower)
        if phone_keyword_count >= 2:
            return True

        return False
    
    def _extract_release_date_criteria(self, message):
        """
        Extract release date criteria from message
        Returns a tuple (start_date, end_date) or None

        Handles:
        - Specific years: "2024", "2023"
        - Relative periods: "last year", "last 5 months", "last 6 months", "this year"
        - Latest/newest: shows most recent phones (last 12 months)
        """
        from datetime import datetime, timedelta
        from dateutil.relativedelta import relativedelta

        message_lower = message.lower()
        today = datetime.now().date()

        # Check for "latest" or "newest" - show phones from last 12 months
        if any(word in message_lower for word in ['latest', 'newest', 'most recent']):
            start_date = today - timedelta(days=365)
            return (start_date, today)

        # Check for specific year mentions (e.g., "2024", "year 2024", "from 2024", "released in 2024")
        year_match = re.search(r'(?:year|from|in|released in)?\s*(\d{4})', message_lower)
        if year_match:
            year = int(year_match.group(1))
            # Validate year is reasonable (between 2020 and current year + 1)
            if 2020 <= year <= today.year + 1:
                start_date = datetime(year, 1, 1).date()
                end_date = datetime(year, 12, 31).date()
                return (start_date, end_date)

        # Check for "this year"
        if 'this year' in message_lower:
            start_date = datetime(today.year, 1, 1).date()
            return (start_date, today)

        # Check for "last year"
        if 'last year' in message_lower:
            last_year = today.year - 1
            start_date = datetime(last_year, 1, 1).date()
            end_date = datetime(last_year, 12, 31).date()
            return (start_date, end_date)

        # Check for "last X months" (e.g., "last 5 months", "last 6 months")
        months_match = re.search(r'last\s+(\d+)\s+months?', message_lower)
        if months_match:
            months = int(months_match.group(1))
            start_date = today - timedelta(days=months * 30)  # Approximate
            return (start_date, today)

        # Check for "recent" - show phones from last 6 months
        if 'recent' in message_lower:
            start_date = today - timedelta(days=180)
            return (start_date, today)

        return None

    def _extract_criteria(self, message):
        """Extract phone criteria from message"""
        criteria = {}

        # Extract budget
        budget = self._extract_budget(message)
        if budget:
            criteria['min_budget'], criteria['max_budget'] = budget

        # Check for usage type and add to criteria
        usage = self._detect_usage_type(message)
        if usage:
            criteria['primary_usage'] = json.dumps([usage])

        # Check for 5G mention
        if '5g' in message.lower():
            criteria['requires_5g'] = True

        # Check for RAM mention
        ram_match = re.search(r'(\d+)\s*gb\s*ram', message.lower())
        if ram_match:
            criteria['min_ram'] = int(ram_match.group(1))

        # Check for storage mention
        storage_match = re.search(r'(\d+)\s*gb\s*storage', message.lower())
        if storage_match:
            criteria['min_storage'] = int(storage_match.group(1))

        # Check for camera mention
        camera_match = re.search(r'(\d+)\s*mp', message.lower())
        if camera_match:
            criteria['min_camera'] = int(camera_match.group(1))

        # Check for battery mention
        battery_match = re.search(r'(\d+)\s*mah', message.lower())
        if battery_match:
            criteria['min_battery'] = int(battery_match.group(1))

        return criteria if criteria else None

    def _detect_usage_type(self, message):
        """Detect usage type from message"""
        message_lower = message.lower()

        if 'gam' in message_lower:
            return 'Gaming'
        elif 'photographer' in message_lower or 'photo' in message_lower or 'picture' in message_lower:
            return 'Photography'
        elif 'vlog' in message_lower or 'content creator' in message_lower or 'youtuber' in message_lower:
            return 'Photography'  # Vloggers need good cameras too
        elif 'camera' in message_lower and not any(word in message_lower for word in ['gaming', 'game']):
            return 'Photography'
        elif 'business' in message_lower or 'work' in message_lower or 'office' in message_lower:
            return 'Business'
        elif 'social' in message_lower:
            return 'Social Media'
        elif 'entertainment' in message_lower or 'video' in message_lower or 'movie' in message_lower:
            return 'Entertainment'

        return None
    
    def _is_fresh_query(self, message):
        """
        Detect if message represents a fresh query (should clear context)
        vs a refinement query (should preserve context)

        Fresh query indicators:
        - Contains strong negative brand preferences: "i not love X, i love Y"
        - Contains budget with brand preferences: "vivo within 2000"
        - Contains "recommend" with minimal context: "recommend a phone for me"
        - Contains explicit brand preferences with features/usage: "i love samsung, give me gaming phone"
        - Contains "give me" or "show me" with specific requirements
        - Contains "i want/prefer/love/like" with a brand: "i want xiaomi"

        Returns: True if fresh query, False if refinement
        """
        message_lower = message.lower()

        # Reset patterns - phrases that indicate starting fresh
        reset_patterns = [
            r'recommend.*phone',
            r'find.*phone for me',
            r'show.*phone for me',
            r'suggest.*phone',
            r'give me.*phone',
        ]

        for pattern in reset_patterns:
            if re.search(pattern, message_lower):
                return True

        # CRITICAL FIX: Check for explicit "i want/prefer/love/like X" statements
        # These should REPLACE previous preferences, not merge
        if re.search(r'\b(i want|i prefer|i love|i like)\b', message_lower):
            # Extract brands to see if user is specifying a new preference
            wanted, unwanted = self._extract_brands_with_preferences(message)
            if wanted:  # User explicitly wants specific brands
                return True

        # Check for negative + positive brand combo (strong indicator of fresh query)
        if re.search(r'(not|don\'t|dont)\s+(love|like|want|prefer)', message_lower):
            # Has negative preference, check if also has positive
            if re.search(r'(i love|i want|i like|i prefer)', message_lower):
                return True

        # Check for budget with brand preferences
        # If message has BOTH budget AND brand, it's likely a fresh search
        # Examples: "vivo within 2000", "samsung under 3000", "i love vivo within 2000"
        has_budget = self._extract_budget(message) is not None
        wanted, unwanted = self._extract_brands_with_preferences(message)
        has_brand_pref = len(wanted) > 0 or len(unwanted) > 0

        if has_budget and has_brand_pref:
            # This is a fresh query like "vivo within 2000" or "i love samsung under 3000"
            return True

        # Check for explicit brand preferences with usage/features
        # Examples: "i love samsung and xiaomi, give me gaming phone"
        has_usage = self._detect_usage_type(message) is not None
        has_features = len(self._detect_feature_priority(message)) > 0

        if has_brand_pref and (has_usage or has_features or has_budget):
            # Has explicit brand plus other requirements - likely a fresh query
            if re.search(r'(i love|i want|i like|i prefer|give me|show me)', message_lower):
                return True

        return False

    def _detect_feature_priority(self, message):
        """Detect which phone feature is being prioritized"""
        message_lower = message.lower()
        detected_features = []

        for feature, keywords in self.feature_keywords.items():
            for keyword in keywords:
                if keyword in message_lower:
                    if feature not in detected_features:
                        detected_features.append(feature)
                    break

        return detected_features

    def _detect_user_category(self, message):
        """Detect user category from message"""
        message_lower = message.lower()

        for category, keywords in self.user_categories.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return category

        return None

    def _extract_brand(self, message):
        """Extract single brand name from message (for backward compatibility)"""
        brands = ['Samsung', 'Apple', 'iPhone', 'Xiaomi', 'Huawei', 'Infinix', 'Google', 'Honor', 'Oppo', 'Realme', 'Vivo', 'Asus', 'Poco', 'Redmi']

        message_lower = message.lower()
        for brand in brands:
            if brand.lower() in message_lower:
                if brand.lower() == 'iphone':
                    return 'Apple'
                return brand

        return None

    def _extract_multiple_brands(self, message):
        """Extract all brand names mentioned in message"""
        # All 13 known brands (matches database brands exactly)
        # Keywords extracted from actual fyp_phoneDataset.csv data
        brand_keywords = {
            'Apple': ['apple', 'iphone'],
            'Asus': ['asus', 'rog', 'zenfone'],
            'Google': ['google', 'pixel'],
            'Honor': ['honor', 'magic', 'play'],  # Magic, Play series (removed 'gt' - conflicts)
            'Huawei': ['huawei', 'mate', 'pura', 'nova', 'enjoy'],  # Mate, Pura, Nova, Enjoy series
            'Infinix': ['infinix', 'hot'],  # Hot series (removed 'note' - conflicts with Redmi Note)
            'Oppo': ['oppo', 'reno', 'find'],  # Reno, Find series (removed 'a', 'f' - too generic)
            'Poco': ['poco'],
            'Realme': ['realme', 'narzo', 'neo'],  # Narzo, Neo series (removed 'gt' - conflicts)
            'Redmi': ['redmi', 'note'],  # Note series
            'Samsung': ['samsung', 'galaxy', 'fold', 'flip'],  # Galaxy, Fold, Flip series
            'Vivo': ['vivo', 'iqoo'],  # iQOO sub-brand (removed single letters - too generic)
            'Xiaomi': ['xiaomi', 'mi', 'mix', 'civi']  # Mi, Mix, Civi (removed 'redmi', 'poco' - separate brands)
        }

        message_lower = message.lower()
        found_brands = []

        for brand_name, keywords in brand_keywords.items():
            for keyword in keywords:
                # Use word boundary to avoid false matches
                import re
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, message_lower):
                    if brand_name not in found_brands:
                        found_brands.append(brand_name)
                    break

        return found_brands
    
    def _extract_brands_with_preferences(self, message):
        """
        Extract brand preferences from message, handling both positive and negative preferences
        Returns: (wanted_brands, unwanted_brands)

        Examples:
        - "i want samsung" → (['Samsung'], [])
        - "i don't like oppo i want samsung" → (['Samsung'], ['Oppo'])
        - "not oppo, show me xiaomi" → (['Xiaomi'], ['Oppo'])
        - "anything but apple" → ([], ['Apple'])
        """
        message_lower = message.lower()

        # Negative indicators (ordered from most specific to least specific)
        negative_patterns = [
            r"don't like\s+(\w+)",
            r"dont like\s+(\w+)",
            r"don't want\s+(\w+)",
            r"dont want\s+(\w+)",
            r"don't love\s+(\w+)",
            r"dont love\s+(\w+)",
            r"don't prefer\s+(\w+)",
            r"dont prefer\s+(\w+)",
            r"not love\s+(\w+)",
            r"not like\s+(\w+)",
            r"not want\s+(\w+)",
            r"not prefer\s+(\w+)",
            r"hate\s+(\w+)",
            r"dislike\s+(\w+)",
            r"avoid\s+(\w+)",
            r"except\s+(\w+)",
            r"anything but\s+(\w+)",
            r"no\s+(\w+)",  # "no apple", "no samsung"
            # CRITICAL FIX: Handle "not X" pattern but only for brand keywords
            # We'll validate against brand_keywords_map to avoid false matches
        ]

        # Positive indicators
        positive_patterns = [
            r"i want\s+(\w+)",
            r"i like\s+(\w+)",
            r"i love\s+(\w+)",
            r"i prefer\s+(\w+)",
            r"i looking for\s+(\w+)",
            r"i would like\s+(\w+)",
            r"show me\s+(\w+)",
            r"give me\s+(\w+)",
            r"find\s+(\w+)",
            r"find me\s+(\w+)",
            r"looking for\s+(\w+)",
            r"only\s+(\w+)",  # CRITICAL FIX: Handle "only vivo", "only samsung"
        ]

        brand_keywords_map = {
            'apple': 'Apple', 'iphone': 'Apple',
            'samsung': 'Samsung', 'galaxy': 'Samsung',
            'xiaomi': 'Xiaomi',
            'vivo': 'Vivo',
            'oppo': 'Oppo',
            'huawei': 'Huawei',
            'honor': 'Honor',
            'realme': 'Realme',
            'redmi': 'Redmi',
            'poco': 'Poco',
            'google': 'Google', 'pixel': 'Google',
            'asus': 'Asus', 'rog': 'Asus',
            'infinix': 'Infinix',
        }

        wanted_brands = []
        unwanted_brands = []

        # CRITICAL FIX: Extract brands from negative context
        for pattern in negative_patterns:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                brand_keyword = match.group(1).lower()
                if brand_keyword in brand_keywords_map:
                    brand_name = brand_keywords_map[brand_keyword]
                    if brand_name not in unwanted_brands:
                        unwanted_brands.append(brand_name)

        # CRITICAL FIX: Handle "not X" pattern specifically for brands
        # This handles cases like "not apple, not samsung"
        not_brand_pattern = r'\bnot\s+(\w+)'
        not_matches = re.finditer(not_brand_pattern, message_lower)
        for match in not_matches:
            potential_brand = match.group(1).lower()
            # Only add if it's actually a brand keyword
            if potential_brand in brand_keywords_map:
                brand_name = brand_keywords_map[potential_brand]
                if brand_name not in unwanted_brands:
                    unwanted_brands.append(brand_name)

        # Extract brands from positive context
        for pattern in positive_patterns:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                brand_keyword = match.group(1).lower()
                if brand_keyword in brand_keywords_map:
                    brand_name = brand_keywords_map[brand_keyword]
                    if brand_name not in wanted_brands and brand_name not in unwanted_brands:
                        wanted_brands.append(brand_name)

        # Handle "brand1 and brand2" patterns
        # Examples: "i love samsung and xiaomi", "i want vivo and oppo"
        and_pattern = r'(i\s+(?:love|like|want|prefer))\s+(\w+)\s+and\s+(\w+)'
        and_matches = re.finditer(and_pattern, message_lower)
        for match in and_matches:
            brand1_keyword = match.group(2).lower()
            brand2_keyword = match.group(3).lower()
            if brand1_keyword in brand_keywords_map:
                brand_name = brand_keywords_map[brand1_keyword]
                if brand_name not in wanted_brands and brand_name not in unwanted_brands:
                    wanted_brands.append(brand_name)
            if brand2_keyword in brand_keywords_map:
                brand_name = brand_keywords_map[brand2_keyword]
                if brand_name not in wanted_brands and brand_name not in unwanted_brands:
                    wanted_brands.append(brand_name)

        # If no explicit positive/negative context found, fall back to simple brand detection
        if not wanted_brands and not unwanted_brands:
            all_brands = self._extract_multiple_brands(message)
            wanted_brands = all_brands

        return (wanted_brands, unwanted_brands)

    def _save_chat_history(self, user_id, message, response, intent, session_id, metadata):
        """
        Save conversation to database

        Note: user_id can be None for guest (non-logged in) users.
        Guest conversations are saved with user_id=NULL for analytics purposes.
        """
        try:
            chat = ChatHistory(
                user_id=user_id,  # Can be None for guest users
                message=message,
                response=response,
                intent=intent,
                session_id=session_id or datetime.utcnow().strftime('%Y%m%d%H%M%S'),
                metadata=json.dumps(metadata) if metadata else None
            )
            db.session.add(chat)
            db.session.commit()
        except Exception as e:
            # Log error but don't fail the chatbot response
            print(f"Error saving chat history: {e}")
            db.session.rollback()

    def get_chat_history(self, user_id, session_id=None, limit=50):
        """Retrieve chat history for a user"""
        query = ChatHistory.query.filter_by(user_id=user_id)

        if session_id:
            query = query.filter_by(session_id=session_id)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
