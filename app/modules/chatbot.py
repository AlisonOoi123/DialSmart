"""
Chatbot Engine
NLP-powered conversational assistant for phone recommendations
"""
from app import db
from app.models import ChatHistory, Phone, Brand
from app.modules.ai_engine import AIRecommendationEngine
import re
import json
from datetime import datetime

class ChatbotEngine:
    """Conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.session_context = {}  # Track session context for brand preferences
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm', 'within', 'under', 'below'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better'],
            'specification': ['specs', 'specification', 'camera', 'battery', 'ram', 'storage', 'screen'],
            'brand_query': ['brand', 'samsung', 'apple', 'iphone', 'xiaomi', 'huawei', 'oppo', 'vivo', 'realme', 'honor', 'nokia'],
            'help': ['help', 'how', 'what can you do'],
            'usage_type': ['gaming', 'photography', 'camera', 'business', 'work', 'social media', 'entertainment']
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
        # Use session_id or user_id as context key
        context_key = session_id or f"user_{user_id}"

        # Initialize session context if not exists
        if context_key not in self.session_context:
            self.session_context[context_key] = {
                'wanted_brands': [],
                'unwanted_brands': [],
                'last_budget': None,
                'last_features': [],     # Track features like 'battery', 'camera'
                'last_usage': None       # Track usage like 'Gaming', 'Photography'
            }

        # Check if this is a fresh query (should clear old context)
        is_fresh = self._is_fresh_query(message)

        # Extract brand preferences from current message
        wanted, unwanted = self._extract_brand_preferences(message)

        # Detect if message is ONLY a brand name (e.g., just "oppo" or "samsung xiaomi")
        # If so, REPLACE previous brands instead of adding to them
        message_words = message.lower().strip().split()
        all_brand_keywords = ['apple', 'iphone', 'samsung', 'galaxy', 'xiaomi', 'vivo', 'oppo',
                               'huawei', 'honor', 'realme', 'redmi', 'poco', 'google', 'pixel',
                               'nokia', 'lenovo', 'asus']
        is_brand_only = len(message_words) <= 3 and all(word in all_brand_keywords for word in message_words)

        # Clear old context if this is a fresh query with strong preferences
        if is_fresh and (wanted or unwanted):
            self.session_context[context_key]['wanted_brands'] = []
            self.session_context[context_key]['unwanted_brands'] = []

        # Update session context with brand preferences
        if wanted:
            if is_brand_only:
                # REPLACE: Clear previous brands and set new ones
                self.session_context[context_key]['wanted_brands'] = wanted.copy()
                # NEW FIX: Also clear features and usage when brand-only (indicates new search context)
                # Example: After "long lasting phone", user says just "oppo" - this is a new brand search
                self.session_context[context_key]['last_features'] = []
                self.session_context[context_key]['last_usage'] = None
            else:
                # ADD: Merge with previous brands (for queries like "i love samsung")
                for brand in wanted:
                    if brand not in self.session_context[context_key]['wanted_brands']:
                        self.session_context[context_key]['wanted_brands'].append(brand)

            # Remove from unwanted if it was there
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

        # Extract and store features from current message
        features = self._detect_feature_priority(message)
        if features:
            # Merge with existing features (don't replace, accumulate)
            for feature in features:
                if feature not in self.session_context[context_key]['last_features']:
                    self.session_context[context_key]['last_features'].append(feature)

        # Extract and store usage from current message
        usage = self._detect_usage_type(message)
        if usage:
            self.session_context[context_key]['last_usage'] = usage

        # Detect intent
        intent = self._detect_intent(message.lower())

        # Generate response based on intent
        response_data = self._generate_response(user_id, message, intent, context_key)

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

        # Check each intent
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent

        return 'general'

    def _generate_response(self, user_id, message, intent, context_key):
        """Generate appropriate response based on intent"""

        # Get session context
        context = self.session_context.get(context_key, {})

        # FIX Issue 6: Better handling for specific model queries vs brand queries
        # Check if multiple brands AND model numbers are mentioned
        message_lower = message.lower()
        brands_mentioned = self._extract_multiple_brands(message)
        has_model_numbers = bool(re.search(r'\d+\s*(?:pro|max|ultra|plus|lite|mini|se)', message_lower))

        skip_phone_model = False
        if brands_mentioned and len(brands_mentioned) >= 1 and has_model_numbers:
            # This is likely a specific model query like "iphone 17 pro and xiaomi 17"
            # Don't skip phone model extraction
            skip_phone_model = False
        elif brands_mentioned and len(brands_mentioned) > 1 and ' and ' in message_lower and 'phone' in message_lower:
            # This is a brand comparison like "apple and samsung phone"
            skip_phone_model = True

        # Note: skip_phone_model flag can be used in future phone model extraction logic
        # Currently serves as documentation for handling different query types

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
                # Store budget in context
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
                    # Limit to top 5 after filtering
                    filtered_phones = filtered_phones[:5]

                    # Build response based on brand preferences
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
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
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
                    'response': "What's your budget range? For example, 'I'm looking for phones under RM2000'",
                    'type': 'text'
                }

        elif intent == 'recommendation' or intent == 'specification':
            # Extract brands and usage from CURRENT message
            current_wanted, current_unwanted = self._extract_brand_preferences(message)
            usage = self._detect_usage_type(message)
            budget = self._extract_budget(message)

            # Get session context
            session_brands = context.get('wanted_brands', [])
            session_unwanted = context.get('unwanted_brands', [])
            if not budget:
                budget = context.get('last_budget')

            # PRIORITY 2: Brands mentioned - always prioritize brand filtering
            if current_wanted or session_brands:
                phones = []

                # Brands + Usage (e.g., "apple and samsung gaming phone")
                if usage:
                    # IMPORTANT: Use ONLY the brands from current message + session wanted brands
                    # But if current message has explicit brands, prioritize those

                    # If current message explicitly mentions brands, use ONLY those
                    if current_wanted:
                        brands_to_use = current_wanted
                    else:
                        # Otherwise use session brands
                        brands_to_use = session_brands

                    phones = self.ai_engine.get_phones_by_usage(usage, budget, brands_to_use, top_n=5)

                    if phones:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                        brands_list = ", ".join(brands_to_use[:-1]) + f" and {brands_to_use[-1]}" if len(brands_to_use) > 1 else brands_to_use[0]
                        response = f"Great choice! Here are the best phones for {usage} from {brands_list}{budget_text}:\n\n"

                        phone_list = []
                        for item in phones:
                            phone = item['phone']
                            specs = item.get('specifications')

                            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                            # Add RAM and storage info if available
                            if specs and hasattr(specs, 'ram_options') and specs.ram_options:
                                response += f"   {specs.ram_options} RAM"
                                if hasattr(specs, 'storage_options') and specs.storage_options:
                                    response += f" - {specs.storage_options} Storage"
                                response += f" - Great for {usage.lower()}\n"

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
                                'usage': usage,
                                'budget': budget,
                                'brands': brands_to_use
                            }
                        }
                    else:
                        brands_list = ", ".join(brands_to_use[:-1]) + f" and {brands_to_use[-1]}" if len(brands_to_use) > 1 else brands_to_use[0]
                        return {
                            'response': f"I couldn't find {brands_list} phones for {usage} in that range. Would you like to see other brands?",
                            'type': 'text'
                        }

            # Fallback to original criteria-based recommendation
            criteria = self._extract_criteria(message)
            recommendations = self.ai_engine.get_recommendations(user_id, criteria=criteria, top_n=3)

            if recommendations:
                response = "Based on your needs, I recommend:\n\n"
                phone_list = []

                for rec in recommendations:
                    phone = rec['phone']
                    response += f"📱 {phone.model_name}\n"
                    response += f"   💰 RM{phone.price:,.2f}\n"
                    response += f"   ✨ {rec['match_score']}% match\n"
                    response += f"   {rec['reasoning'][:100]}...\n\n"

                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'match_score': rec['match_score']
                    })

                return {
                    'response': response,
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }
            else:
                return {
                    'response': "Let me help you find the perfect phone. What's your budget and what will you primarily use it for?",
                    'type': 'text'
                }

        elif intent == 'usage_type':
            # Detect usage type (already stored in session context)
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

                    # Build detailed response with budget and brand context
                    budget_text = ""
                    if budget:
                        min_b, max_b = budget
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}"

                    brand_text = ""
                    if wanted_brands:
                        if len(wanted_brands) == 1:
                            brand_text = f" from {wanted_brands[0]}"
                        else:
                            brands_list = ", ".join(wanted_brands[:-1]) + f" and {wanted_brands[-1]}"
                            brand_text = f" from {brands_list}"

                    response = f"Great choice! Here are the best phones for {usage}{brand_text}{budget_text}: 📱\n\n"
                    phone_list = []

                    for item in filtered_phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Add RAM and storage info if available
                        if specs and hasattr(specs, 'ram_options') and specs.ram_options:
                            response += f"   {specs.ram_options} RAM"
                            if hasattr(specs, 'storage_options') and specs.storage_options:
                                response += f" - {specs.storage_options} Storage"
                            response += f" - Great for {usage.lower()}\n"

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
                            'usage': usage,
                            'budget': budget,
                            'brands': wanted_brands
                        }
                    }

            return {
                'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Get session context
            session_features = context.get('last_features', [])
            session_usage = context.get('last_usage')
            wanted_brands = context.get('wanted_brands', [])
            unwanted_brands = context.get('unwanted_brands', [])

            # If we have session usage, use usage-based filtering with brands
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

                    response = f"Great! Here are the best {brand_text} phones for {session_usage}:\n\n"

                    phone_list = []
                    for item in filtered_phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

                        # Add specs if available
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
                            'usage': session_usage,
                            'brands': wanted_brands
                        }
                    }

            # NEW FIX: If we have session features (but no usage), use feature-based filtering
            # Example: "recommend a long lasting phone" then "vivo" → Show Vivo with good battery
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

                        # Show relevant specs based on features
                        if specs:
                            if 'battery' in session_features and specs.battery_capacity:
                                response += f"   🔋 {specs.battery_capacity}mAh battery\n"
                            if 'camera' in session_features and specs.rear_camera_main:
                                response += f"   📷 {specs.rear_camera_main}MP camera\n"
                            if 'display' in session_features and specs.screen_type:
                                response += f"   📺 {specs.screen_size}\" {specs.screen_type}\n"
                            if 'performance' in session_features and specs.processor:
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

            # Use wanted brands from session context for multi-brand queries
            if wanted_brands:
                budget = self._extract_budget(message)
                if not budget:
                    budget = context.get('last_budget')

                all_phones = []
                found_brands = []

                for brand_name in wanted_brands:
                    brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                    if brand:
                        query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                        # Apply budget filter if specified
                        if budget:
                            min_b, max_b = budget
                            query = query.filter(Phone.price >= min_b, Phone.price <= max_b)

                        phones = query.order_by(Phone.price.asc()).limit(5).all()

                        if phones:
                            found_brands.append(brand.name)
                            all_phones.extend([(phone, brand.name) for phone in phones])

                if all_phones:
                    # Build response
                    if len(found_brands) == 1:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        feature_text = f" with focus on {', '.join(session_features)}" if session_features else ""
                        response = f"Here are {found_brands[0]} phones{budget_text}{feature_text}:\n\n"
                    else:
                        budget_text = f" within RM{min_b:,.0f} - RM{max_b:,.0f}" if budget else ""
                        feature_text = f" with focus on {', '.join(session_features)}" if session_features else ""
                        brands_text = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}"
                        response = f"Here are phones from {brands_text}{budget_text}{feature_text}:\n\n"

                    phone_list = []
                    for phone, brand_name in all_phones[:5]:  # Limit to 5 total
                        response += f"📱 {brand_name} {phone.model_name} - RM{phone.price:,.2f}\n"
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
                            'features': session_features
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
            # SMART FALLBACK: Check if budget is extractable even for general queries
            budget = self._extract_budget(message)
            if budget:
                min_budget, max_budget = budget
                # Store budget in context
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
                    # Limit to top 5 after filtering
                    filtered_phones = filtered_phones[:5]

                    # Build response based on brand preferences
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
                        response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
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
                        'metadata': {'phones': phone_list, 'budget': budget}
                    }
                else:
                    if wanted_brands:
                        if len(wanted_brands) == 1:
                            brand_text = wanted_brands[0]
                        else:
                            brand_text = ", ".join(wanted_brands[:-1]) + f" and {wanted_brands[-1]}"
                        return {
                            'response': f"I couldn't find {brand_text} phones in that exact range. Would you like to adjust your budget or see other brands?",
                            'type': 'text'
                        }
                    else:
                        return {
                            'response': f"I couldn't find phones in that exact range. Would you like to adjust your budget?",
                            'type': 'text'
                        }

            # No budget found, give general help
            return {
                'response': "I'm here to help you find the perfect smartphone! You can ask me about phone recommendations, budget options, brands, or specifications. What would you like to know?",
                'type': 'text',
                'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
            }

    def _extract_budget(self, message):
        """Extract budget range from message"""
        # Look for patterns like "RM1000", "1000", "under 2000", "between 1000 and 2000"
        patterns = [
            r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
            r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000
            r'under\s*rm?\s*(\d+)',  # under RM2000
            r'below\s*rm?\s*(\d+)',  # below 2000
            r'rm\s*(\d+)',  # RM2000
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                if 'under' in message.lower() or 'below' in message.lower():
                    max_budget = int(match.group(1))
                    return (500, max_budget)
                elif len(match.groups()) == 2:
                    return (int(match.group(1)), int(match.group(2)))
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

        return criteria if criteria else None

    def _detect_usage_type(self, message):
        """Detect usage type from message"""
        message_lower = message.lower()

        if 'gam' in message_lower:
            return 'Gaming'
        elif 'photo' in message_lower or 'camera' in message_lower:
            return 'Photography'
        elif 'business' in message_lower or 'work' in message_lower:
            return 'Business'
        elif 'social' in message_lower:
            return 'Social Media'
        elif 'entertainment' in message_lower or 'video' in message_lower or 'movie' in message_lower:
            return 'Entertainment'

        return None

    def _extract_brand(self, message):
        """Extract brand name from message"""
        brands = ['Samsung', 'Apple', 'iPhone', 'Xiaomi', 'Huawei', 'Nokia', 'Lenovo', 'Honor', 'Oppo', 'Realme', 'Vivo']

        message_lower = message.lower()
        for brand in brands:
            if brand.lower() in message_lower:
                if brand.lower() == 'iphone':
                    return 'Apple'
                return brand

        return None

    def _is_fresh_query(self, message):
        """
        Detect if message represents a fresh query (should clear context)
        vs a refinement query (should preserve context)

        Fresh query indicators:
        - Contains strong negative brand preferences: "i not love X, i love Y"
        - Contains budget with brand preferences: "vivo within 2000"
        - Contains "recommend" with minimal context: "recommend a phone for me"

        Returns: True if fresh query, False if refinement
        """
        message_lower = message.lower()

        # Reset patterns - phrases that indicate starting fresh
        reset_patterns = [
            r'recommend.*phone for me',
            r'recommend.*a phone',
            r'find.*phone for me',
            r'show.*phone for me',
            r'suggest.*phone',
        ]

        for pattern in reset_patterns:
            if re.search(pattern, message_lower):
                return True

        # Check for negative + positive brand combo (strong indicator of fresh query)
        if re.search(r'(not|don\'t|dont)\s+(love|like|want|prefer)', message_lower):
            # Has negative preference, check if also has positive
            if re.search(r'(i love|i want|i like|i prefer)', message_lower):
                return True

        # NEW FIX: Check for budget with brand preferences
        # If message has BOTH budget AND brand, it's likely a fresh search
        # Examples: "vivo within 2000", "samsung under 3000", "i love vivo within 2000"
        has_budget = self._extract_budget(message) is not None
        wanted, unwanted = self._extract_brand_preferences(message)
        has_brand_pref = len(wanted) > 0 or len(unwanted) > 0

        if has_budget and has_brand_pref:
            # This is a fresh query like "vivo within 2000" or "i love samsung under 3000"
            return True

        return False

    def _detect_feature_priority(self, message):
        """
        Detect feature priorities from message

        Returns: List of feature keywords like ['battery', 'camera', 'performance']
        """
        message_lower = message.lower()
        features = []

        # Battery-related keywords
        if any(word in message_lower for word in ['long lasting', 'battery life', 'battery', 'long battery', 'last long']):
            features.append('battery')

        # Camera-related keywords
        if any(word in message_lower for word in ['camera', 'photo', 'photography', 'picture', 'selfie']):
            features.append('camera')

        # Performance-related keywords
        if any(word in message_lower for word in ['gaming', 'performance', 'fast', 'processor', 'speed']):
            features.append('performance')

        # Display-related keywords
        if any(word in message_lower for word in ['screen', 'display', 'amoled', 'oled']):
            features.append('display')

        # Storage-related keywords
        if any(word in message_lower for word in ['storage', 'memory', 'gb storage']):
            features.append('storage')

        return features

    def _extract_brand_preferences(self, message):
        """
        Extract brand preferences from message
        Returns: (wanted_brands, unwanted_brands)

        Examples:
        - "i want samsung" → (['Samsung'], [])
        - "i don't like oppo i want samsung" → (['Samsung'], ['Oppo'])
        - "i love samsung" → (['Samsung'], [])
        - "i love samsung and xiaomi" → (['Samsung', 'Xiaomi'], [])
        - "oppo and xiaomi" → (['Oppo', 'Xiaomi'], [])
        """
        message_lower = message.lower()

        # Brand keywords mapping
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
            'nokia': 'Nokia',
            'lenovo': 'Lenovo',
            'asus': 'Asus'
        }

        wanted_brands = []
        unwanted_brands = []

        # Negative patterns - brands user doesn't like
        negative_patterns = [
            (r"don't like\s+(\w+)", 1),
            (r"dont like\s+(\w+)", 1),
            (r"don't love\s+(\w+)", 1),
            (r"dont love\s+(\w+)", 1),
            (r"not love\s+(\w+)", 1),
            (r"not like\s+(\w+)", 1),
            (r"not prefer\s+(\w+)", 1),
            (r"don't prefer\s+(\w+)", 1),
            (r"dont prefer\s+(\w+)", 1),
            (r"don't want\s+(\w+)", 1),
            (r"dont want\s+(\w+)", 1),
            (r"not want\s+(\w+)", 1),
            (r"no\s+(\w+)", 1),
            (r"hate\s+(\w+)", 1),
            (r"dislike\s+(\w+)", 1),
            (r"avoid\s+(\w+)", 1),
            (r"except\s+(\w+)", 1),
            (r"anything but\s+(\w+)", 1),
        ]

        # Positive patterns - brands user wants/likes
        # Note: Must be specific to avoid matching negative contexts like "don't like"
        positive_patterns = [
            (r"i want\s+(\w+(?:\s+and\s+\w+)*)", 1),  # Handles "i want samsung and xiaomi"
            (r"i love\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"i like\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"i prefer\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"show me\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"give me\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"find me\s+(\w+(?:\s+and\s+\w+)*)", 1),
            (r"looking for\s+(\w+(?:\s+and\s+\w+)*)", 1),
        ]

        # Extract unwanted brands
        for pattern, group in negative_patterns:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                brand_keyword = match.group(group).lower()
                if brand_keyword in brand_keywords_map:
                    brand_name = brand_keywords_map[brand_keyword]
                    if brand_name not in unwanted_brands:
                        unwanted_brands.append(brand_name)

        # Extract wanted brands
        for pattern, group in positive_patterns:
            matches = re.finditer(pattern, message_lower)
            for match in matches:
                # Extract brand keywords, handle "and" separator
                brand_text = match.group(group).lower()
                # Split by "and" to get multiple brands
                brand_parts = re.split(r'\s+and\s+', brand_text)

                for brand_keyword in brand_parts:
                    brand_keyword = brand_keyword.strip()
                    if brand_keyword in brand_keywords_map:
                        brand_name = brand_keywords_map[brand_keyword]
                        if brand_name not in wanted_brands and brand_name not in unwanted_brands:
                            wanted_brands.append(brand_name)

        # Also check for standalone brand mentions (for queries like just "oppo and xiaomi")
        # Only if no wanted brands found from patterns above
        if not wanted_brands and not unwanted_brands:
            words = message_lower.split()
            for i, word in enumerate(words):
                if word in brand_keywords_map:
                    brand_name = brand_keywords_map[word]
                    if brand_name not in wanted_brands:
                        wanted_brands.append(brand_name)

        return (wanted_brands, unwanted_brands)

    def _extract_multiple_brands(self, message):
        """
        Extract all brand mentions from message (both wanted and unwanted)

        Returns:
            List of all brand names mentioned in message
        """
        wanted, unwanted = self._extract_brand_preferences(message)
        return wanted + unwanted

    def _filter_phones_by_brand(self, phones, wanted_brands, unwanted_brands):
        """
        Filter phone list by brand preferences

        Args:
            phones: List of phone items (dicts with 'phone' key)
            wanted_brands: List of brand names to include
            unwanted_brands: List of brand names to exclude

        Returns:
            Filtered list of phone items
        """
        if not wanted_brands and not unwanted_brands:
            return phones

        filtered = []

        for item in phones:
            phone = item['phone']
            phone_brand = phone.brand.name if phone.brand else None

            # Skip if brand is unwanted
            if unwanted_brands and phone_brand in unwanted_brands:
                continue

            # If wanted brands specified, only include those
            if wanted_brands:
                if phone_brand in wanted_brands:
                    filtered.append(item)
            else:
                # No wanted brands, just exclude unwanted
                filtered.append(item)

        return filtered

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
