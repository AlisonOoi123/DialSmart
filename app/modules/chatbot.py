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
                'last_budget': None
            }

        # Extract brand preferences from current message
        wanted, unwanted = self._extract_brand_preferences(message)

        # Update session context with brand preferences
        if wanted:
            # Add to wanted brands if not already there
            for brand in wanted:
                if brand not in self.session_context[context_key]['wanted_brands']:
                    self.session_context[context_key]['wanted_brands'].append(brand)
                # Remove from unwanted if it was there
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
                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
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

        elif intent == 'recommendation':
            # Check for specific criteria in message
            criteria = self._extract_criteria(message)

            # Get recommendations
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
            # Detect usage type
            usage = self._detect_usage_type(message)
            if usage:
                budget = self._extract_budget(message)
                phones = self.ai_engine.get_phones_by_usage(usage, budget, top_n=3)

                if phones:
                    response = f"Great choice! Here are the best phones for {usage}:\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'usage': usage}
                    }

            return {
                'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Extract brand name
            brand_name = self._extract_brand(message)
            if brand_name:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    # Apply budget filter if available from context
                    query = Phone.query.filter_by(brand_id=brand.id, is_active=True)

                    last_budget = context.get('last_budget')
                    if last_budget:
                        min_budget, max_budget = last_budget
                        query = query.filter(Phone.price >= min_budget, Phone.price <= max_budget)
                        response = f"Here are {brand.name} phones within RM{min_budget} - RM{max_budget}:\n\n"
                    else:
                        response = f"Here are some popular {brand.name} phones:\n\n"

                    phones = query.order_by(Phone.price.asc()).limit(5).all()

                    phone_list = []
                    for phone in phones:
                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'brand': brand.name}
                    }

            return {
                'response': "Which brand are you interested in? We have Samsung, Apple, Xiaomi, Huawei, and more!",
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

    def _extract_brand_preferences(self, message):
        """
        Extract brand preferences from message
        Returns: (wanted_brands, unwanted_brands)

        Examples:
        - "i want samsung" → (['Samsung'], [])
        - "i don't like oppo i want samsung" → (['Samsung'], ['Oppo'])
        - "i love samsung" → (['Samsung'], [])
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
            'lenovo': 'Lenovo'
        }

        wanted_brands = []
        unwanted_brands = []

        # Negative patterns - brands user doesn't like
        negative_patterns = [
            (r"don't like\s+(\w+)", 1),
            (r"dont like\s+(\w+)", 1),
            (r"not\s+(\w+)", 1),
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
            (r"i want\s+(\w+)", 1),
            (r"i love\s+(\w+)", 1),
            (r"i like\s+(\w+)", 1),
            (r"i prefer\s+(\w+)", 1),
            (r"show me\s+(\w+)", 1),
            (r"give me\s+(\w+)", 1),
            (r"find me\s+(\w+)", 1),
            (r"looking for\s+(\w+)", 1),
            # Removed standalone "want", "like", "love", "prefer" to prevent false matches
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
                brand_keyword = match.group(group).lower()
                if brand_keyword in brand_keywords_map:
                    brand_name = brand_keywords_map[brand_keyword]
                    if brand_name not in wanted_brands and brand_name not in unwanted_brands:
                        wanted_brands.append(brand_name)

        return (wanted_brands, unwanted_brands)

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
