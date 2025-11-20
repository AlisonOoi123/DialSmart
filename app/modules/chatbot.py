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
        # Session context for conversation memory
        self.session_context = {}
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon'],
            'budget_query': ['budget', 'price', 'cost', 'cheap', 'affordable', 'expensive', 'rm', 'within', 'under', 'below', 'above', 'over', 'near', 'around', 'max', 'maximum'],
            'recommendation': ['recommend', 'suggest', 'find', 'looking for', 'need', 'want', 'show me', 'best'],
            'comparison': ['compare', 'difference', 'vs', 'versus', 'better'],
            'specification': ['specs', 'specification'],
            'brand_query': ['brand', 'samsung', 'apple', 'iphone', 'xiaomi', 'huawei', 'oppo', 'vivo', 'realme', 'redmi', 'poco'],
            'help': ['help', 'how', 'what can you do'],
            'usage_type': ['gaming', 'photography', 'camera', 'business', 'work', 'social media', 'entertainment', 'gamer', 'photographer', 'student']
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
            self.session_context[context_key] = {}

        # Detect intent
        intent = self._detect_intent(message.lower())

        # Generate response based on intent, passing session context
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

        # Check if the query is phone-related (skip for greetings and help)
        if intent not in ['greeting', 'help'] and not self._is_phone_related(message):
            return {
                'response': "I'm DialSmart AI Assistant, and I specialize in helping you find the perfect smartphone! 📱\n\nI can assist you with:\n• Phone recommendations based on your needs\n• Budget-friendly options\n• Brand comparisons\n• Phone specifications\n• Phones for gaming, photography, business, etc.\n\nWhat kind of phone are you looking for today?",
                'type': 'text',
                'quick_replies': ['Find a phone under RM2000', 'Gaming phones', 'Best camera phones', 'Show popular brands']
            }

        elif intent == 'budget_query':
            # Extract budget from message
            budget = self._extract_budget(message)

            # CRITICAL FIX: Check for brands in budget query (e.g., "vivo under rm 2000")
            brand_names = self._extract_multiple_brands(message)

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
                            phones = query.limit(5).all()

                            if phones:
                                found_brands.append(brand.name)
                                all_phones.extend([(phone, brand.name) for phone in phones])

                    if all_phones:
                        brands_text = ", ".join(found_brands[:-1]) + f" and {found_brands[-1]}" if len(found_brands) > 1 else found_brands[0]
                        response = f"Here are {brands_text} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"

                        phone_list = []
                        for phone, brand_name in all_phones:
                            response += f"📱 {brand_name} {phone.model_name} - RM{phone.price:,.2f}\n"
                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'brand': brand_name,
                                'price': phone.price
                            })

                        return {
                            'response': response,
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'brands': found_brands, 'budget': budget}
                        }
                    else:
                        brands_text = ", ".join(brand_names[:-1]) + f" and {brand_names[-1]}" if len(brand_names) > 1 else brand_names[0]
                        return {
                            'response': f"I couldn't find {brands_text} phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}. Would you like to see phones from other brands?",
                            'type': 'text'
                        }

                # No brand mentioned, show general budget recommendations
                phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=3)

                if phones:
                    response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
                    phone_list = []
                    for item in phones:
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
                # Try to get budget from current message first
                budget = self._extract_budget(message)

                # If no budget in current message, check context from previous message
                if not budget and 'last_budget' in context:
                    budget = context['last_budget']

                # Try to get brands from current message first
                brand_names = self._extract_multiple_brands(message)

                # If no brand in current message, check context from previous message
                if not brand_names and 'last_brands' in context:
                    brand_names = context['last_brands']

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

                    response = f"Great choice! Here are the best phones for {usage}{brand_text}{budget_text}:\n\n"
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
                        'metadata': {'phones': phone_list, 'usage': usage, 'brands': brand_names}
                    }

            return {
                'response': "What will you primarily use your phone for? Gaming, photography, business, or entertainment?",
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Extract all mentioned brands
            brand_names = self._extract_multiple_brands(message)

            if brand_names:
                # CONTEXT-AWARE: Check current message first, then session context
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
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
                        usage_text = f" for {usage}" if usage else ""
                        response = f"Here are {found_brands[0]} phones{budget_text}{usage_text}:\n\n"
                    else:
                        budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}" if budget else ""
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
                            'price': phone.price
                        })

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'brands': found_brands, 'budget': budget, 'usage': usage}
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
                phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=3)

                if phones:
                    response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
                    phone_list = []
                    for item in phones:
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

            # No budget extractable, return generic greeting
            return {
                'response': "I'm here to help you find the perfect smartphone! You can ask me about phone recommendations, budget options, brands, or specifications. What would you like to know?",
                'type': 'text',
                'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
            }

    def _extract_budget(self, message):
        """
        Extract budget range from message
        Handles: RM2000, rm2000, RM 2000, rm 2000, 2000
        Keywords: under/within/below/above/over/near/around/max/maximum with all combinations
        """
        message_lower = message.lower()

        # Look for patterns like "RM1000", "1000", "under 2000", "within 3000", "near 3000", "between 1000 and 2000", "above 3000"
        patterns = [
            r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
            r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000, within 2000-3000
            r'near\s*rm?\s*(\d+)\s*(?:to|-)\s*rm?\s*(\d+)',  # near 2000-3000 or near 2000 to 3000
            r'(?:under|below|within|max|maximum|near|around)\s+(?:rm\s+)?(\d+)',
            r'(?:above|over|more than)\s+(?:rm\s+)?(\d+)',  # above 3000, over rm5000, more than 4000
            r'rm\s*(\d+)',  # RM2000
            r'(?:^|\s)(\d{3,5})(?:\s|$)',  # standalone number 1000-99999
        ]

        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                # First check if we have a range (2 groups)
                if len(match.groups()) == 2 and match.group(2):
                    # Handle "near X-Y" or "near X to Y" pattern (range)
                    if 'near' in message_lower:
                        return (int(match.group(1)), int(match.group(2)))
                    # Regular range pattern (including "within 2000-3000")
                    else:
                        return (int(match.group(1)), int(match.group(2)))
                # Handle "above/over/more than" keywords - minimum budget
                elif any(word in message_lower for word in ['above', 'over', 'more than']):
                    min_budget = int(match.group(1))
                    return (min_budget, 15000)  # Set reasonable upper limit
                # Handle "near X" pattern (±500 range)
                elif 'near' in message_lower or 'around' in message_lower:
                    center = int(match.group(1))
                    return (max(500, center - 500), center + 500)
                # Handle single max budget keywords
                elif any(word in message_lower for word in ['under', 'below', 'within', 'max', 'maximum']):
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

        # Extract brands - HIGHEST PRIORITY
        brands = self._extract_multiple_brands(message)
        if brands:
            # Get brand IDs from database
            brand_ids = []
            for brand_name in brands:
                brand = Brand.query.filter(Brand.name.ilike(f"%{brand_name}%")).first()
                if brand:
                    brand_ids.append(brand.id)
            if brand_ids:
                criteria['preferred_brands'] = json.dumps(brand_ids)

        # Check for usage type
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

    def _is_phone_related(self, message):
        """Check if the message is related to phones/smartphones"""
        message_lower = message.lower()

        # Phone-related keywords
        phone_keywords = [
            'phone', 'smartphone', 'mobile', 'device', 'handset',
            'android', 'ios', 'cell', 'cellular', 'telephone', 'iphone',
            'galaxy', 'xiaomi', 'huawei', 'oppo', 'vivo', 'samsung',
            'screen', 'display', 'camera', 'battery', 'processor',
            'ram', 'storage', '5g', 'spec', 'specification'
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

    def _extract_brand(self, message):
        """Extract single brand name from message (for backward compatibility)"""
        brands = self._extract_multiple_brands(message)
        return brands[0] if brands else None

    def _extract_multiple_brands(self, message):
        """Extract all brand names mentioned in message"""
        # All known brands with aliases
        brand_keywords = {
            'Samsung': ['samsung', 'galaxy'],
            'Apple': ['apple', 'iphone'],
            'Xiaomi': ['xiaomi', 'mi'],
            'Huawei': ['huawei'],
            'Oppo': ['oppo'],
            'Vivo': ['vivo'],
            'Realme': ['realme'],
            'Honor': ['honor'],
            'Google': ['google', 'pixel'],
            'Asus': ['asus', 'rog'],
            'Infinix': ['infinix'],
            'Redmi': ['redmi'],
            'Poco': ['poco'],
            'Nokia': ['nokia'],
            'Lenovo': ['lenovo']
        }

        message_lower = message.lower()
        found_brands = []

        for brand_name, keywords in brand_keywords.items():
            for keyword in keywords:
                # Use word boundary to avoid false matches
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, message_lower):
                    if brand_name not in found_brands:
                        found_brands.append(brand_name)
                    break

        return found_brands

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
