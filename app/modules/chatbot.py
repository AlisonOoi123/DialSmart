"""
Chatbot Engine
NLP-powered conversational assistant for phone recommendations
"""
from app import db
from app.models import ChatHistory, Phone, Brand, PhoneSpecification
from app.modules.ai_engine import AIRecommendationEngine
import re
import json
from datetime import datetime

class ChatbotEngine:
    """Conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want', 'i want', 'show me', 'best'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better'],
            'specification': ['specs', 'specification', 'camera', 'battery', 'ram', 'storage', 'screen', 'display', 'processor', 'cpu'],
            'brand_query': ['brand', 'samsung', 'galaxy', 'apple', 'iphone', 'xiaomi', 'huawei', 'honor', 'oppo', 'vivo', 'realme', 'google', 'pixel', 'asus', 'rog', 'infinix', 'poco', 'redmi'],
            'help': ['help', 'how', 'what can you do'],
            'usage_type': ['gaming', 'photography', 'camera', 'business', 'work', 'social media', 'entertainment', 'photographer', 'gamer']
        }

        # Feature keywords for enhanced understanding
        self.feature_keywords = {
            'battery': ['battery', 'long lasting', 'battery life', 'long battery', 'all day battery'],
            'camera': ['camera', 'photo', 'photography', 'photographer', 'selfie', 'picture'],
            'display': ['display', 'screen', 'amoled', 'oled', 'lcd', 'retina'],
            'performance': ['fast', 'processor', 'cpu', 'performance', 'speed', 'powerful', 'snapdragon', 'flagship'],
            '5g': ['5g', '5g support', '5g network'],
            'storage': ['storage', 'memory', 'gb storage', 'space'],
            'ram': ['ram', 'memory'],
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
        # Detect intent
        intent = self._detect_intent(message.lower())

        # Generate response based on intent
        response_data = self._generate_response(user_id, message, intent)

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

    def _generate_response(self, user_id, message, intent):
        """Generate appropriate response based on intent"""

        # NEW: Check for specific phone model query
        # Skip phone model extraction ONLY if asking for recommendations with specific requirements
        message_lower = message.lower()

        # Skip phone model extraction if message contains recommendation keywords with requirements
        skip_phone_model = any(keyword in message_lower for keyword in [
            'recommend', 'suggest', 'find me', 'looking for', 'need a phone', 'want a phone', 'best phone',
            'photographer', 'photography phone', 'gaming phone', 'gamer phone', 'business phone',
            'social media', 'entertainment', 'long lasting', 'amoled',
            'i want a phone', 'show me phones', 'within', 'under rm'
        ])

        # Also skip if multiple brands are mentioned (e.g., "apple and samsung phone")
        if not skip_phone_model:
            brands_mentioned = self._extract_multiple_brands(message)
            if len(brands_mentioned) > 1 or (brands_mentioned and ' and ' in message_lower and 'phone' in message_lower):
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

        elif intent == 'budget_query':
            # Extract budget from message
            budget = self._extract_budget(message)
            if budget:
                min_budget, max_budget = budget
                phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=3)

                if phones:
                    response = f"Here are the top phones within RM{min_budget} - RM{max_budget}:\n\n"
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
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
                        'metadata': {'phones': phone_list}
                    }
                else:
                    return {
                        'response': f"I couldn't find phones in that exact range. Would you like to adjust your budget?",
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
            budget = self._extract_budget(message)
            usage = self._detect_usage_type(message)
            brands = self._extract_multiple_brands(message)
            criteria = self._extract_criteria(message)

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
                brand_names = self._extract_multiple_brands(message)
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
            brand_names = self._extract_multiple_brands(message)

            if brand_names:
                # Check if budget is mentioned
                budget = self._extract_budget(message)
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
            'xiaomi': ['xiaomi']  # Removed 'mi ' to avoid conflicts
        }

        for brand_name, keywords in brand_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_brand = brand_name
                break

        # Step 2: Remove common query words to extract model name
        query_words = ['price', 'cost', 'how much', 'specs', 'specification', 'details', 'info', 'information',
                      'about', 'tell me', 'show me', 'what is', 'whats', 'the', 'of', 'spec', 'battery']

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
            r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
            r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000, within 2000-3000
            r'near\s*rm?\s*(\d+)\s*(?:to|-)\s*rm?\s*(\d+)',  # near 2000-3000 or near 2000 to 3000
            r'(?:under|below|within|max|maximum|near|around)\s*rm?\s*(\d+)',  # under/below/within/near RM2000
            r'rm\s*(\d+)',  # RM2000
            r'(?:^|\s)(\d{3,5})(?:\s|$)',  # standalone number 1000-99999
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                # First check if we have a range (2 groups)
                if len(match.groups()) == 2 and match.group(2):
                    # Handle "near X-Y" or "near X to Y" pattern (range)
                    if 'near' in message.lower():
                        return (int(match.group(1)), int(match.group(2)))
                    # Regular range pattern (including "within 2000-3000")
                    else:
                        return (int(match.group(1)), int(match.group(2)))
                # Handle "near X" pattern (±500 range)
                elif 'near' in message.lower() or 'around' in message.lower():
                    center = int(match.group(1))
                    return (max(500, center - 500), center + 500)
                # Handle single max budget keywords
                elif any(word in message.lower() for word in ['under', 'below', 'within', 'max', 'maximum']):
                    max_budget = int(match.group(1))
                    return (500, max_budget)
                else:
                    # Single value mentioned
                    value = int(match.group(1))
                    # Assume it's max budget
                    return (500, value)

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

    def _save_chat_history(self, user_id, message, response, intent, session_id, metadata):
        """Save conversation to database"""
        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=response,
            intent=intent,
            session_id=session_id or datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(chat)
        db.session.commit()

    def get_chat_history(self, user_id, session_id=None, limit=50):
        """Retrieve chat history for a user"""
        query = ChatHistory.query.filter_by(user_id=user_id)

        if session_id:
            query = query.filter_by(session_id=session_id)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
