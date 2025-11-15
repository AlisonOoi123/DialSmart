"""
Chatbot Engine
NLP-powered conversational assistant for phone recommendations
"""
from app import db
from app.models import ChatHistory, Phone, Brand, Recommendation
from app.modules.ai_engine import AIRecommendationEngine
import re
import json
from datetime import datetime

class ChatbotEngine:
    """Conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        # Enhanced keyword lists for better matching
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'greetings', 'howdy', 'hiya'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm', 'ringgit', 'myr', 'how much', 'under', 'below', 'within', 'range'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want', 'show', 'get', 'search', 'phone', '5g', 'smartphone', 'which phone', 'best phone', 'top phone'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better', 'which is better', 'or', 'between'],
            'specification': ['specs', 'specification', 'camera', 'battery', 'ram', 'storage', 'screen', 'display', 'processor', 'features', 'megapixel', 'mp', 'mah', 'gb', 'inch'],
            'brand_query': ['brand', 'samsung', 'apple', 'iphone', 'xiaomi', 'huawei', 'oppo', 'vivo', 'realme', 'infinix', 'poco', 'oneplus', 'google', 'pixel', 'asus', 'honor'],
            'help': ['help', 'how', 'what can you do', 'what can i ask', 'guide', 'assist', 'support'],
            'usage_type': ['gaming', 'photography', 'camera', 'business', 'work', 'social media', 'entertainment', 'video', 'games', 'photos', 'selfie', 'streaming']
        }
        # Conversation context storage (session_id -> context dict)
        self.conversation_context = {}

    def process_message(self, user_id, message, session_id=None):
        """
        Process user message and generate response with context awareness

        Args:
            user_id: User ID
            message: User's message text
            session_id: Optional session ID for conversation grouping and context

        Returns:
            Dictionary with response and metadata
        """
        # Detect intent with context awareness
        intent = self._detect_intent(message.lower(), session_id)

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

        # Save recommendations to Recommendation table if phones were recommended
        metadata = response_data.get('metadata', {})
        if metadata.get('phones'):
            # Extract criteria from message for tracking
            criteria = self._extract_criteria(message)
            if not criteria:
                criteria = {}
            criteria['source'] = 'chatbot'
            criteria['intent'] = intent

            # Save recommendations
            self._save_recommendations(user_id, metadata['phones'], criteria)

        return response_data

    def _detect_intent(self, message, session_id=None):
        """
        Detect user intent from message with enhanced multi-keyword matching
        Returns primary intent and detected keywords
        """
        message_lower = message.lower()
        intent_scores = {}
        detected_keywords = []

        # Score each intent based on keyword matches
        for intent, keywords in self.intents.items():
            score = 0
            for keyword in keywords:
                if keyword in message_lower:
                    score += 1
                    detected_keywords.append((intent, keyword))

            if score > 0:
                intent_scores[intent] = score

        # Check conversation context for follow-up questions
        if session_id and session_id in self.conversation_context:
            context = self.conversation_context[session_id]
            last_intent = context.get('last_intent')

            # Boost scoring for related intents in follow-up
            if last_intent == 'recommendation' and 'specification' in intent_scores:
                intent_scores['specification'] += 1

        # Return intent with highest score
        if intent_scores:
            primary_intent = max(intent_scores, key=intent_scores.get)

            # Store context
            if session_id:
                self.conversation_context[session_id] = {
                    'last_intent': primary_intent,
                    'keywords': detected_keywords,
                    'message': message
                }

            return primary_intent

        return 'general'

    def _generate_response(self, user_id, message, intent):
        """Generate appropriate response based on intent"""

        if intent == 'greeting':
            import random
            greetings = [
                "Hello! I'm DialSmart AI Assistant. I'm here to help you find the perfect smartphone. How can I assist you today?",
                "Hi there! Looking for a new phone? I can help you find the perfect match based on your needs and budget!",
                "Hey! Welcome to DialSmart. Tell me what you're looking for in a phone, and I'll recommend the best options for you!",
                "Greetings! I specialize in helping people find their ideal smartphone. What features are most important to you?"
            ]
            return {
                'response': random.choice(greetings),
                'type': 'text',
                'quick_replies': ['Find a phone', 'Show budget options', 'Best for gaming', 'Best camera phones']
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
                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
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
                        'match_score': rec['match_score'],
                        'image': phone.main_image
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
            # Detect usage type and use intelligent recommendation system
            usage = self._detect_usage_type(message)
            if usage:
                # Build criteria with usage type
                criteria = self._extract_criteria(message) or {}
                criteria['primary_usage'] = usage

                # Use the intelligent recommendation system
                recommendations = self.ai_engine.get_recommendations(user_id, criteria=criteria, top_n=3)

                if recommendations:
                    response = f"Great choice! Here are the best phones for {usage}:\n\n"
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
                            'match_score': rec['match_score'],
                            'image': phone.main_image
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
                    phones = Phone.query.filter_by(brand_id=brand.id, is_active=True).limit(5).all()
                    response = f"Here are some popular {brand.name} phones:\n\n"

                    phone_list = []
                    for phone in phones:
                        response += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
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

        else:  # general - try to be helpful even without clear intent
            import random

            # Try to extract any useful information from the message
            criteria_found = self._extract_criteria(message)
            budget_found = self._extract_budget(message)
            brand_found = self._extract_brand(message)
            usage_found = self._detect_usage_type(message)

            # If we found any criteria, try to help
            if criteria_found or budget_found or brand_found or usage_found:
                responses = [
                    f"I understand you're interested in a phone{' for ' + usage_found if usage_found else ''}. Let me find some options for you!",
                    "Great! I can help you with that. Let me search for phones matching your requirements.",
                    "I'm on it! Searching for the best phones based on what you told me..."
                ]

                # Try to recommend based on what we found
                recommendations = self.ai_engine.get_recommendations(user_id, criteria=criteria_found if criteria_found else {}, top_n=3)

                if recommendations:
                    response = random.choice(responses) + "\n\n"
                    phone_list = []

                    for rec in recommendations[:3]:
                        phone = rec['phone']
                        response += f"📱 {phone.model_name}\n"
                        response += f"   💰 RM{phone.price:,.2f}\n"
                        response += f"   ✨ {rec['match_score']}% match\n\n"

                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'match_score': rec['match_score'],
                            'image': phone.main_image
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }

            # Fallback to conversational response
            fallback_responses = [
                "I'm here to help you find the perfect smartphone! You can ask me about phone recommendations, budget options, brands, or specifications. What would you like to know?",
                "I'd love to help you find a great phone! Tell me - what's most important to you? Budget, camera quality, gaming performance, or something else?",
                "Looking for a new phone? I can help! Just tell me your budget or what you'll mainly use it for, and I'll suggest the best options.",
                "I specialize in finding the perfect phone for your needs. What are you looking for - a budget phone, gaming phone, camera phone, or something else?"
            ]

            return {
                'response': random.choice(fallback_responses),
                'type': 'text',
                'quick_replies': ['Under RM1500', 'Best for gaming', 'Best camera', 'Show all brands']
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
        message_lower = message.lower()

        # Extract budget
        budget = self._extract_budget(message)
        if budget:
            criteria['min_budget'], criteria['max_budget'] = budget

        # Check for 5G mention
        if '5g' in message_lower:
            criteria['requires_5g'] = True

        # Extract brand preference
        brand_name = self._extract_brand(message)
        if brand_name:
            criteria['preferred_brands'] = [brand_name]

        # Check for RAM mention
        ram_match = re.search(r'(\d+)\s*gb\s*ram', message_lower)
        if ram_match:
            criteria['min_ram'] = int(ram_match.group(1))

        # Check for storage mention
        storage_match = re.search(r'(\d+)\s*gb\s*storage', message_lower)
        if storage_match:
            criteria['min_storage'] = int(storage_match.group(1))

        # Check for camera mention
        camera_match = re.search(r'(\d+)\s*mp', message_lower)
        if camera_match:
            criteria['min_camera'] = int(camera_match.group(1))

        # Extract primary usage keywords
        usage = self._detect_usage_type(message)
        if usage:
            criteria['primary_usage'] = usage

        # Extract important features from keywords
        important_features = []

        # Battery keywords
        if any(word in message_lower for word in ['battery', 'long battery', 'battery life', 'mah']):
            important_features.append('Battery')

        # Camera keywords
        if any(word in message_lower for word in ['camera', 'photo', 'photography', 'picture', 'selfie', 'mp']):
            important_features.append('Camera')

        # Performance keywords
        if any(word in message_lower for word in ['fast', 'performance', 'speed', 'processor', 'gaming', 'game', 'ram']):
            important_features.append('Performance')

        # Storage keywords
        if any(word in message_lower for word in ['storage', 'memory', 'gb storage', 'large storage']):
            important_features.append('Storage')

        # 5G keywords
        if '5g' in message_lower:
            important_features.append('5G')

        # Design keywords
        if any(word in message_lower for word in ['design', 'premium', 'look', 'beautiful', 'stylish']):
            important_features.append('Design')

        if important_features:
            criteria['important_features'] = important_features

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
        brands = ['Samsung', 'Apple', 'iPhone', 'Xiaomi', 'Huawei', 'Nokia', 'Lenovo',
                  'Honor', 'Oppo', 'Realme', 'Vivo', 'Infinix', 'Poco', 'Redmi', 'Google', 'Asus']

        message_lower = message.lower()
        for brand in brands:
            if brand.lower() in message_lower:
                if brand.lower() == 'iphone':
                    return 'Apple'
                return brand

        return None

    def _save_chat_history(self, user_id, message, response, intent, session_id, metadata):
        """Save conversation to database"""
        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=response,
            intent=intent,
            session_id=session_id or datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            chat_metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(chat)
        db.session.commit()

    def _save_recommendations(self, user_id, phones, criteria=None):
        """Save chatbot recommendations to Recommendation table"""
        for phone_data in phones:
            # Extract phone_id and match_score from phone_data
            phone_id = phone_data.get('id')
            match_score = phone_data.get('match_score', 0)

            if not phone_id:
                continue

            # Build reasoning based on available data
            phone = Phone.query.get(phone_id)
            if not phone:
                continue

            reasoning = f"Recommended via chatbot based on your query."
            if match_score > 0:
                reasoning = f"{match_score}% match - {phone.model_name} meets your requirements."

            # Save to database
            recommendation = Recommendation(
                user_id=user_id,
                phone_id=phone_id,
                match_percentage=match_score,
                reasoning=reasoning,
                user_criteria=json.dumps(criteria) if criteria else None
            )
            db.session.add(recommendation)

        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error saving chatbot recommendations: {str(e)}")

    def get_chat_history(self, user_id, session_id=None, limit=50):
        """Retrieve chat history for a user"""
        query = ChatHistory.query.filter_by(user_id=user_id)

        if session_id:
            query = query.filter_by(session_id=session_id)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
