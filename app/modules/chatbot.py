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
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better'],
            'specification': ['specs', 'specification', 'camera', 'battery', 'ram', 'storage', 'screen'],
            'brand_query': ['brand', 'samsung', 'apple', 'iphone', 'xiaomi', 'huawei'],
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

        # Check each intent
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent

        return 'general'

    def _generate_response(self, user_id, message, intent):
        """Generate appropriate response based on intent"""

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

                # Check if brands are mentioned
                brand_names = self._extract_brand(message)
                brand_ids = None
                brand_display_names = []

                if brand_names:
                    brand_ids = []
                    for brand_name in brand_names:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                            brand_display_names.append(brand.name)

                # Get more phones if multiple brands requested
                top_n = 5 if not brand_ids else max(5, 3 * len(brand_ids))
                phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), brand_ids=brand_ids, top_n=top_n)

                if phones:
                    if brand_display_names:
                        brands_str = " and ".join(brand_display_names)
                        response = f"Check out these {brands_str} models"
                    else:
                        response = f"Here are the top phones"

                    response += f" within RM{min_budget} - RM{max_budget}:\n\n"
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
                        'metadata': {'phones': phone_list, 'brands': brand_display_names}
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

                # Check if brands are mentioned
                brand_names = self._extract_brand(message)
                brand_ids = None
                brand_display_names = []

                if brand_names:
                    brand_ids = []
                    for brand_name in brand_names:
                        brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                        if brand:
                            brand_ids.append(brand.id)
                            brand_display_names.append(brand.name)

                # Get more phones if multiple brands requested
                top_n = 5 if not brand_ids else max(5, 3 * len(brand_ids))
                phones = self.ai_engine.get_phones_by_usage(usage, budget, brand_ids=brand_ids, top_n=top_n)

                if phones:
                    if brand_display_names:
                        brands_str = " and ".join(brand_display_names)
                        response = f"Great choice! Here are our {brands_str} smartphones"
                    else:
                        response = f"Great choice! Here are the best phones"

                    response += f" for {usage}:\n\n"
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        specs = item.get('specifications')

                        # Add relevant feature info based on usage
                        feature_info = ""
                        if usage == 'Photography' and specs and specs.rear_camera_main:
                            feature_info = f"{specs.rear_camera_main}MP main camera - Excellent for photography"
                        elif usage == 'Gaming' and specs and specs.ram_options:
                            feature_info = f"{specs.ram_options} RAM - Great for gaming"
                        elif usage == 'Business' and specs and specs.battery_capacity:
                            feature_info = f"{specs.battery_capacity}mAh battery - Long-lasting for work"

                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        if feature_info:
                            response += f"   {feature_info}\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'usage': usage, 'brands': brand_display_names}
                    }

            return {
                'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Extract brand names (can be multiple)
            brand_names = self._extract_brand(message)
            if brand_names:
                # Get Brand IDs for all mentioned brands
                brand_ids = []
                brand_display_names = []
                for brand_name in brand_names:
                    brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                    if brand:
                        brand_ids.append(brand.id)
                        brand_display_names.append(brand.name)

                if brand_ids:
                    # Query phones from each brand to ensure balanced results
                    phones = []
                    phones_per_brand = max(3, 10 // len(brand_ids))  # At least 3 phones per brand

                    for brand_id in brand_ids:
                        brand_phones = Phone.query.filter(
                            Phone.brand_id == brand_id,
                            Phone.is_active == True
                        ).order_by(Phone.price.desc()).limit(phones_per_brand).all()
                        phones.extend(brand_phones)

                    if phones:
                        brands_str = " and ".join(brand_display_names)
                        response = f"Here are our {brands_str} smartphones:\n\n"

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
                            'metadata': {'phones': phone_list, 'brands': brand_display_names}
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

        # Extract brands
        brand_names = self._extract_brand(message)
        if brand_names:
            brand_ids = []
            for brand_name in brand_names:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                criteria['brand_ids'] = brand_ids

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
        """Extract brand names from message (can return multiple brands)"""
        brands = ['Samsung', 'Apple', 'iPhone', 'Xiaomi', 'Huawei', 'Nokia', 'Lenovo',
                  'Honor', 'Oppo', 'Realme', 'Vivo', 'Poco', 'Redmi', 'Google', 'Asus', 'Infinix']

        message_lower = message.lower()
        found_brands = []

        for brand in brands:
            if brand.lower() in message_lower:
                # Map iPhone to Apple
                if brand.lower() == 'iphone':
                    if 'Apple' not in found_brands:
                        found_brands.append('Apple')
                else:
                    if brand not in found_brands:
                        found_brands.append(brand)

        return found_brands if found_brands else None

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
