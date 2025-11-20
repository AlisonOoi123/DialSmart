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
                'last_budget': None
            }
            
        # Extract brand preferences from current message
        wanted, unwanted = self._extract_brands_with_preferences(message)

        message_words = message.lower().strip().split()
        all_brand_keywords = ['apple', 'iphone', 'samsung', 'galaxy', 'xiaomi', 'vivo', 'oppo',
                            'huawei', 'honor', 'realme', 'redmi', 'poco', 'google', 'pixel']
        is_brand_only = len(message_words) <= 3 and all(word in all_brand_keywords for word in message_words)

        # Update session context with brand preferences
        if wanted:
            if is_brand_only:
                # REPLACE: Clear previous brands
                self.session_context[context_key]['wanted_brands'] = wanted.copy()
            else:
                # ADD: Merge with previous brands
                for brand in wanted:
                    if brand not in self.session_context[context_key]['wanted_brands']:
                        self.session_context[context_key]['wanted_brands'].append(brand)

            # Remove from unwanted
            for brand in wanted:
                if brand in self.session_context[context_key]['unwanted_brands']:
                    self.session_context[context_key]['unwanted_brands'].remove(brand)

        if unwanted:
            # Add to unwanted brands if not already there
            for brand in unwanted:
                if brand not in self.session_context[context_key]['unwanted_brands']:
                    self.session_context[context_key]['unwanted_brands'].append(brand)
                # Remove from wanted if it was there
                if brand in self.session_context[context_key]['wanted_brands']:
                    self.session_context[context_key]['wanted_brands'].remove(brand)

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
            'without', 'avoid', 'not', 'except', 'excluding',
            'dont want', "don't want", 'no need for',
            
            # Open comparison
            'difference between brands', 'brand comparison',
            'which brand better', 'brand suggestions'
        ])

        # Initialize brands_mentioned to avoid UnboundLocalError
        brands_mentioned = None

        # Also skip if multiple brands are mentioned (e.g., "apple and samsung phone")
        if not skip_phone_model:
            brands_mentioned = self._extract_multiple_brands(message)
            if len(brands_mentioned) > 1 or (brands_mentioned and ' and ' in message_lower and 'phone' in message_lower):
                skip_phone_model = True

        if brands_mentioned and len(brands_mentioned) == 1:
                # Remove brand name and common words to see what's left
                test_message = message_lower
                for brand in brands_mentioned:
                    test_message = test_message.replace(brand.lower(), '')
                # Remove common words
                test_message = test_message.replace('phone', '').replace('phones', '').replace('smartphone', '').replace('smartphones', '').strip()
                # If nothing meaningful left (or just articles/prepositions), it's a generic brand query
                if len(test_message) < 3 or test_message in ['a', 'an', 'the', 'any', 'all', 'some']:
                    skip_phone_model = True

        # Try to extract phone model if NOT asking for recommendations
        if not skip_phone_model:
            phone_model = self._extract_phone_model(message)
            if phone_model:
                return self._handle_specific_phone_query(message, phone_model)
        # END NEW CODE

        if intent == 'greeting':
            return {
                'response': "Hello! I'm DialSmart AI Assistant. I'm here to help you find the perfect smartphone. How can I assist you today?",
                'type': 'text',
                'quick_replies': ['Find a phone', 'Compare phones', 'Show me budget options']
            }

        # Check if the query is phone-related (skip for greetings and help)
        if intent not in ['greeting', 'help'] and not self._is_phone_related(message):
            return {
                'response': "I'm DialSmart AI Assistant, and I specialize in helping you find the perfect smartphone! 📱\n\nI can assist you with:\n• Phone recommendations based on your needs\n• Budget-friendly options\n• Brand comparisons\n• Phone specifications\n• Phones for gaming, photography, business, etc.\n\nWhat kind of phone are you looking for today?",
                'type': 'text',
                'quick_replies': ['Find a phone under RM2000', 'Gaming phones', 'Best camera phones', 'Show popular brands']
            }


        elif intent == 'budget_query' or intent == 'timeline':
            # Extract budget from message
            budget = self._extract_budget(message)
            wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
            context = self.session_context.get(context_key, {})
            session_wanted = context.get('wanted_brands', [])
            session_unwanted = context.get('unwanted_brands', [])

            # Combine current message brands with session brands
            all_wanted_brands = list(set(wanted_brands + session_wanted))
            all_unwanted_brands = list(set(unwanted_brands + session_unwanted))

            brand_names = all_wanted_brands
            
            release_date_criteria = self._extract_release_date_criteria(message)
            if budget:
                min_budget, max_budget = budget
                 # If brands mentioned, filter by brand
                if brand_names:
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
                            'metadata': {'phones': phone_list, 'brands': found_brands, 'budget': budget, 'release_date': release_date_criteria}
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
            # Detect all parameters from message
            features = self._detect_feature_priority(message)
            user_category = self._detect_user_category(message)
            
            # Check current message first, then context
            budget = self._extract_budget(message)
            if not budget and 'last_budget' in context:
                budget = context['last_budget']  # ← Use previous budget!
            
            usage = self._detect_usage_type(message)
            
            # FIX 6: Merge current brands with session context brands
            wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
            
            # Get session context brands
            session_wanted = context.get('wanted_brands', [])
            session_unwanted = context.get('unwanted_brands', [])
            
            # Merge: Combine current message brands with session brands
            all_wanted_brands = list(set(wanted_brands + session_wanted))
            all_unwanted_brands = list(set(unwanted_brands + session_unwanted))
            
            # Use merged brands
            brands = all_wanted_brands if all_wanted_brands else None

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
                            if specs and specs.ram_options:
                                response += f"   {specs.ram_options} RAM"
                                if specs.storage_options:
                                    response += f" - {specs.storage_options} Storage"
                                response += f"\n"
                            response += "\n"

                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': phone.brand.name,
                                'price': phone.price,
                                'image': phone.main_image,
                                'ram': specs.ram_options if specs else None,
                                'storage': specs.storage_options if specs else None
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
                                if 'performance' in features and specs.processor:
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
                    all_phones = []
                    found_brands = []

                    for brand_name in brands:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                            if budget:
                                min_b, max_b = budget
                                query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                            phones_found = query.limit(3).all()  # Limit per brand
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
                        if specs and specs.ram_options:
                            response += f"   {specs.ram_options} RAM"
                            if specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += f"\n"
                        response += "\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'ram': specs.ram_options if specs else None,
                            'storage': specs.storage_options if specs else None
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
                    feature_desc = " and ".join([f.replace('_', ' ') for f in features])
                    budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
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
            if usage:
                budget = self._extract_budget(message)
                wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
                brand_names = wanted_brands
                phones = self.ai_engine.get_phones_by_usage(usage, budget, brand_names, top_n=5)

                if phones:
                    budget_text = ""
                    if budget:
                        min_b, max_b = budget
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}"

                    brand_text = ""
                    if brand_names:
                        if len(brand_names) == 1:
                            brand_text = f" from {brand_names[0]}"
                        else:
                            brands_list = ", ".join(brand_names[:-1]) + f" and {brand_names[-1]}"
                            brand_text = f" from {brands_list}"

                    response = f"Great choice! Here are the best phones for {usage}{brand_text}{budget_text}: 📱\n\n"
                    phone_list = []

                    for item in phones:
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
                            'brands': brand_names
                        }
                    }

            return {
                'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Extract all mentioned brands
            wanted_brands, unwanted_brands = self._extract_brands_with_preferences(message)
            brand_names = wanted_brands  # Use wanted brands

            if brand_names:
                # Check if budget is mentioned
                budget = self._extract_budget(message)
                if not budget and 'last_budget' in context:
                    budget = context['last_budget']
                usage = self._detect_usage_type(message)

                all_phones = []
                found_brands = []

                for brand_name in brand_names:
                    brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                    if brand:
                        query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                        # Apply budget filter if specified
                        if budget:
                            min_b, max_b = budget
                            query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                        phones = query.limit(5).all()

                        if phones:
                            found_brands.append(brand.name)
                            all_phones.extend([(phone, brand.name) for phone in phones])

                if all_phones:
                    # Build response
                    if len(found_brands) == 1:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        usage_text = f" for {usage}" if usage else ""
                        response = f"Here are {found_brands[0]} phones{budget_text}{usage_text}:\n\n"
                    else:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        usage_text = f" for {usage}" if usage else ""
                        brands_text = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}"
                        response = f"Here are phones from {brands_text}{budget_text}{usage_text}:\n\n"

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
                        'metadata': {
                            'phones': phone_list,
                            'brands': found_brands,
                            'budget': budget,
                            'usage': usage
                        }
                    }

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
• "Find me a phone under RM2000"
• "Best phones for gaming"
• "Show me Samsung phones"
• "I need a phone with good camera"
""",
                'type': 'text'
            }

        else:  # general

            # SMART FALLBACK: Check if budget is extractable even for general queries (e.g., "phone 1000-3000")
            budget = self._extract_budget(message)
            if budget:
                min_budget, max_budget = budget
                # Store budget in context
                context['last_budget'] = budget

                phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=10)

                # Filter by brand preferences
                wanted_brands = context.get('wanted_brands', [])
                unwanted_brands = context.get('unwanted_brands', [])

                filtered_phones = self._filter_phones_by_brand(phones, wanted_brands, unwanted_brands)

                if filtered_phones:
                    # Limit to top 5 after filtering
                    filtered_phones = filtered_phones[:5]

                    # Build response based on brand preferences
                    if wanted_brands:
                        brand_names = ', '.join(wanted_brands)
                        response = f"Here are the best {brand_names} phones within RM{min_budget} - RM{max_budget}:\n\n"
                    else:
                        response = f"Here are the top phones within RM{min_budget} - RM{max_budget}:\n\n"
                                        
                    phone_list = []
                    for item in filtered_phones:
                        phone = item['phone']
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'brand': phone.brand.name,
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'budget': budget}
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
                    'response': "I'm here to help you find the perfect smartphone! You can ask me about phone recommendations, budget options, brands, or specifications. What would you like to know?",
                    'type': 'text',
                    'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
            }

    # NEW METHODS for specific phone queries
    def _extract_phone_model(self, message):
        """Extract specific phone model name from message with brand awareness"""
        message_lower = message.lower()
        from sqlalchemy import or_, func

        # Step 1: Detect if a specific brand is mentioned
        # All 13 known brands (matches database brands exactly)
        detected_brand = None
        brand_keywords = {
            'apple': ['apple', 'iphone'],
            'asus': ['asus', 'rog'],
            'google': ['google', 'pixel'],
            'honor': ['honor'],
            'huawei': ['huawei'],
            'infinix': ['infinix'],
            'oppo': ['oppo'],
            'poco': ['poco'],
            'realme': ['realme'],
            'redmi': ['redmi'],
            'samsung': ['samsung', 'galaxy'],
            'vivo': ['vivo'],
            'xiaomi': ['xiaomi']  
        }

        for brand_name, keywords in brand_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_brand = brand_name
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
        if detected_brand and detected_brand in brand_keywords:
            for keyword in brand_keywords[detected_brand]:
                cleaned_message = cleaned_message.replace(keyword, ' ')

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

        return None

    def _handle_specific_phone_query(self, message, phones):
        """Handle query about specific phone model"""
        message_lower = message.lower()

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
        patterns = [
           # Range patterns with RM on both sides
            (r'(?:rm|RM)\s*(\d+)\s*(?:to|-|and)\s*(?:rm|RM)\s*(\d+)', 'range'),  # RM1000 to RM2000 or rm 1000 to rm 2000
            # Near with range pattern (e.g., "near 2000-3000" or "near 2000 to 3000")
            (r'near\s*(?:rm\s*)?(\d+)\s*(?:to|-)\s*(?:rm\s*)?(\d+)', 'range'),  # near 2000-3000 or near rm2000 to rm3000
            # Range patterns without RM
            (r'(\d+)\s*(?:to|-|and)\s*(\d+)', 'range'),  # 1000 to 2000

            # Above patterns WITH RM (with or without space)
            (r'(?:above|over|more than)\s+(?:rm|RM)\s*(\d+)', 'min'),  # above RM3000 or above rm 3000
            # Above patterns WITHOUT RM
            (r'(?:above|over|more than)\s+(\d+)', 'min'),  # above 3000

            # Within/under/below/max/maximum patterns WITH RM (with or without space)
            (r'(?:within|under|below|max|maximum)\s+(?:rm|RM)\s*(\d+)', 'max'),  # within RM2000 or within rm 2000
            # Within/under/below/max/maximum patterns WITHOUT RM
            (r'(?:within|under|below|max|maximum)\s+(\d+)', 'max'),  # within 2000

            # Near/around single value pattern (±500 range)
            (r'(?:near|around)\s+(?:rm\s*)?(\d+)', 'near'),  # near 2000 or near rm2000

            # Single RM value (with or without space)
            (r'(?:rm|RM)\s*(\d+)', 'single'),  # RM2000 or rm 2000

            # Standalone number (3-5 digits)
            (r'(?:^|\s)(\d{3,5})(?:\s|$)', 'single'),  # 1000, 2000, etc.
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

        # Check if any phone keyword is in the message
        for keyword in phone_keywords:
            if keyword in message_lower:
                return True

        # Check if any brand is mentioned (brands are phone-related)
        if self._extract_multiple_brands(message):
            return True

        # Check if budget is mentioned (likely phone shopping)
        if self._extract_budget(message):
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
        elif 'camera' in message_lower and not any(word in message_lower for word in ['gaming', 'game']):
            return 'Photography'
        elif 'business' in message_lower or 'work' in message_lower or 'office' in message_lower:
            return 'Business'
        elif 'social' in message_lower:
            return 'Social Media'
        elif 'entertainment' in message_lower or 'video' in message_lower or 'movie' in message_lower:
            return 'Entertainment'

        return None

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
        brands = self._extract_multiple_brands(message)
        return brands[0] if brands else None

    def _extract_multiple_brands(self, message):
        """Extract all brand names mentioned in message"""
        # All 13 known brands (matches database brands exactly)
        brand_keywords = {
            'Apple': ['apple', 'iphone'],
            'Asus': ['asus', 'rog'],
            'Google': ['google', 'pixel'],
            'Honor': ['honor'],
            'Huawei': ['huawei'],
            'Infinix': ['infinix'],
            'Oppo': ['oppo'],
            'Poco': ['poco'],
            'Realme': ['realme'],
            'Redmi': ['redmi'],
            'Samsung': ['samsung', 'galaxy'],
            'Vivo': ['vivo'],
            'Xiaomi': ['xiaomi']  # Removed 'mi', 'redmi', 'poco' to avoid conflicts
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

        # Negative indicators
        negative_patterns = [
            r"don't like\s+(\w+)",
            r"dont like\s+(\w+)",
            r"don't like\s+(\w+)",
            r"dont want\s+(\w+)",
            r"don't want\s+(\w+)",
            r"don't love\s+(\w+)",
            r"dont\s+(\w+)",
            r"don't\s+(\w+)",
            r"not\s+(\w+)",
            r"no\s+(\w+)",
            r"not prefer\s+(\w+)",
            r"not love\s+(\w+)",
            r"hate\s+(\w+)",
            r"dislike\s+(\w+)",
            r"avoid\s+(\w+)",
            r"except\s+(\w+)",
            r"but\s+(\w+)",
            r"anything but\s+(\w+)",
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

        # Extract brands from negative context
        for pattern in negative_patterns:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                brand_keyword = match.group(1).lower()
                if brand_keyword in brand_keywords_map:
                    brand_name = brand_keywords_map[brand_keyword]
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
