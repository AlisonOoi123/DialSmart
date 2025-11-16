"""
Chatbot Engine
NLP-powered conversational assistant for phone recommendations with ML-based intent classification
"""
from app import db
from app.models import ChatHistory, Phone, Brand
from app.modules.ai_engine import AIRecommendationEngine
from app.modules.smart_recommendation_engine import SmartRecommendationEngine
from app.modules.chatbot_responses import ResponseTemplates
import re
import json
import os
import pickle
from datetime import datetime

class ChatbotEngine:
    """Conversational AI chatbot for DialSmart with ML intent classification"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.smart_engine = SmartRecommendationEngine()
        self.response_templates = ResponseTemplates()
        self.ml_model = None
        self._load_ml_model()

        # Fallback keyword-based intents (if ML model not available)
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

    def _load_ml_model(self):
        """Load the trained ML intent classification model"""
        model_path = os.path.join(os.path.dirname(__file__), '../../models/chatbot_intent_classifier.pkl')
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.ml_model = pickle.load(f)
                print(f"ML intent classifier loaded successfully from {model_path}")
            except Exception as e:
                print(f"Error loading ML model: {e}")
                self.ml_model = None
        else:
            print(f"ML model not found at {model_path}. Using keyword-based intent detection.")

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
        """
        Detect user intent from message using ML model or keyword matching

        Args:
            message: User's message text

        Returns:
            Detected intent label
        """
        message_lower = message.lower()

        # Try ML-based intent classification first
        if self.ml_model is not None:
            try:
                predicted_intent = self.ml_model.predict([message_lower])[0]

                # Get confidence scores - LinearSVC uses decision_function instead of predict_proba
                try:
                    # Try predict_proba first (for calibrated classifiers)
                    proba = self.ml_model.predict_proba([message_lower])[0]
                    max_confidence = max(proba)
                except AttributeError:
                    # Fallback to decision_function (for LinearSVC)
                    decision = self.ml_model.decision_function([message_lower])[0]
                    # Normalize decision scores
                    max_confidence = max(decision) / (sum(abs(decision)) + 1e-10)

                # Only use ML prediction if confidence is reasonable (lower threshold for decision_function)
                if max_confidence > 0.05:  # Lowered from 0.3 for decision_function compatibility
                    return predicted_intent
            except Exception as e:
                print(f"Error in ML intent detection: {e}")

        # Fallback to keyword-based intent detection
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent

        return 'general'

    def _generate_response(self, user_id, message, intent):
        """Generate appropriate response based on intent using smart templates"""

        if intent == 'greeting':
            return {
                'response': self.response_templates.get_greeting(),
                'type': 'text',
                'quick_replies': ['Find a phone', 'Compare phones', 'Show me budget options']
            }

        elif intent == 'budget_query':
            # Extract budget from message
            budget = self._extract_budget(message)
            if budget:
                min_budget, max_budget = budget
                phones = self.smart_engine.get_phones_by_budget(min_budget, max_budget, limit=5)

                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'score': item['score']
                        })

                    response = self.response_templates.get_budget_response(
                        found=True,
                        min_budget=min_budget,
                        max_budget=max_budget,
                        phone_list=phone_list_text
                    )

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                else:
                    return {
                        'response': self.response_templates.get_budget_response(
                            found=False,
                            min_budget=min_budget,
                            max_budget=max_budget
                        ),
                        'type': 'text'
                    }
            else:
                return {
                    'response': self.response_templates.get_budget_response(),
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
                        'image': phone.main_image,
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
            # Detect usage type and persona
            persona = self._detect_persona(message)
            usage = self._detect_usage_type(message)
            if usage:
                # Check for explicit budget first, then persona budget, then None
                budget = self._extract_budget(message)
                if not budget and persona:
                    budget = persona['budget']  # Use persona-inferred budget
                phones = self.smart_engine.get_phones_by_usage(usage, budget, limit=5)

                if phones:
                    phone_list_text = ""
                    phone_list = []

                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image,
                            'score': item['score']
                        })

                    response = self.response_templates.get_usage_response(usage, phone_list_text)

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'usage': usage}
                    }

            return {
                'response': self.response_templates.get_usage_response(),
                'type': 'text'
            }

        elif intent == 'brand_query':
            # Extract brand name
            brand_name = self._extract_brand(message)
            if brand_name:
                phones = self.smart_engine.get_phones_by_brand(brand_name, limit=5)

                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })

                    response = self.response_templates.get_brand_response(brand_name, phone_list_text)

                    return {
                        'response': response,
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'brand': brand_name}
                    }

            return {
                'response': self.response_templates.get_brand_response(),
                'type': 'text'
            }

        elif intent == 'comparison':
            return {
                'response': self.response_templates.get_comparison_response(),
                'type': 'text',
                'action': 'redirect_compare'
            }

        elif intent == 'specification':
            # Handle merged specification intent (battery, camera, display, storage, performance, features)
            budget = self._extract_budget(message)
            message_lower = message.lower()

            # Detect which type of specification the user is asking about
            if any(word in message_lower for word in ['battery', 'mah', 'long lasting', 'battery life', 'charge', 'power']):
                # Battery query
                phones = self.smart_engine.get_phones_by_battery(budget, limit=5)
                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })
                    return {
                        'response': self.response_templates.get_battery_response(phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                return {
                    'response': self.response_templates.get_battery_response(),
                    'type': 'text'
                }

            elif any(word in message_lower for word in ['camera', 'photo', 'picture', 'mp', 'megapixel', 'selfie', 'front camera', 'rear camera']):
                # Camera query
                camera_spec = message_lower
                phones = self.smart_engine.get_phones_by_camera(camera_spec, budget, limit=5)
                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })
                    return {
                        'response': self.response_templates.get_camera_response(phone_list=phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                return {
                    'response': self.response_templates.get_camera_response(),
                    'type': 'text'
                }

            elif any(word in message_lower for word in ['display', 'screen', 'amoled', 'oled', 'lcd', 'refresh rate', 'hz', 'inch']):
                # Display query
                display_spec = message_lower
                phones = self.smart_engine.get_phones_by_display(display_spec, budget, limit=5)
                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })
                    return {
                        'response': self.response_templates.get_display_response(phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                return {
                    'response': self.response_templates.get_display_response(),
                    'type': 'text'
                }

            elif any(word in message_lower for word in ['storage', 'gb', 'rom', 'memory', 'space']):
                # Storage query
                storage_spec = message_lower
                phones = self.smart_engine.get_phones_by_storage(storage_spec, budget, limit=5)
                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })
                    return {
                        'response': self.response_templates.get_storage_response(phone_list=phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                return {
                    'response': self.response_templates.get_storage_response(),
                    'type': 'text'
                }

            elif any(word in message_lower for word in ['performance', 'processor', 'cpu', 'chipset', 'snapdragon', 'ram', 'speed', 'fast']):
                # Performance query
                phones = self.smart_engine.get_phones_by_performance(budget, limit=5)
                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })
                    return {
                        'response': self.response_templates.get_performance_response(phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list}
                    }
                return {
                    'response': self.response_templates.get_performance_response(),
                    'type': 'text'
                }

            else:
                # Feature query (5G, waterproof, NFC, etc.) or general specs
                feature = self._extract_feature(message)
                if feature:
                    phones = self.smart_engine.get_phones_by_feature(feature, budget, limit=5)
                    if phones:
                        phone_list_text = ""
                        phone_list = []
                        for item in phones:
                            phone = item['phone']
                            phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                            phone_list_text += f"   {item['reason']}\n\n"
                            phone_list.append({
                                'id': phone.id,
                                'name': phone.model_name,
                                'price': phone.price,
                                'image': phone.main_image
                            })
                        return {
                            'response': self.response_templates.get_feature_response(feature, phone_list_text),
                            'type': 'recommendation',
                            'metadata': {'phones': phone_list, 'feature': feature}
                        }

                # Fallback for general specification queries
                return {
                    'response': "I'd be happy to help you find phones with specific features! Could you tell me more about what you're looking for? For example:\n• Battery life\n• Camera quality\n• Display type\n• Storage capacity\n• Performance/processor\n• Features like 5G, waterproofing, etc.",
                    'type': 'text'
                }

        elif intent == 'camera_query':
            # Handle camera-specific queries
            budget = self._extract_budget(message)
            camera_spec = message.lower()
            phones = self.smart_engine.get_phones_by_camera(camera_spec, budget, limit=5)

            if phones:
                phone_list_text = ""
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list_text += f"   {item['reason']}\n\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'image': phone.main_image
                    })

                return {
                    'response': self.response_templates.get_camera_response(phone_list=phone_list_text),
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }

            return {
                'response': self.response_templates.get_camera_response(),
                'type': 'text'
            }

        elif intent == 'performance_query':
            # Handle performance queries
            budget = self._extract_budget(message)
            phones = self.smart_engine.get_phones_by_performance(budget, limit=5)

            if phones:
                phone_list_text = ""
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list_text += f"   {item['reason']}\n\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'image': phone.main_image
                    })

                return {
                    'response': self.response_templates.get_performance_response(phone_list_text),
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }

            return {
                'response': self.response_templates.get_performance_response(),
                'type': 'text'
            }

        elif intent == 'battery_query':
            # Handle battery queries
            budget = self._extract_budget(message)
            phones = self.smart_engine.get_phones_by_battery(budget, limit=5)

            if phones:
                phone_list_text = ""
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list_text += f"   {item['reason']}\n\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'image': phone.main_image
                    })

                return {
                    'response': self.response_templates.get_battery_response(phone_list_text),
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }

            return {
                'response': self.response_templates.get_battery_response(),
                'type': 'text'
            }

        elif intent == 'display_query':
            # Handle display queries
            budget = self._extract_budget(message)
            display_spec = message.lower()
            phones = self.smart_engine.get_phones_by_display(display_spec, budget, limit=5)

            if phones:
                phone_list_text = ""
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list_text += f"   {item['reason']}\n\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'image': phone.main_image
                    })

                return {
                    'response': self.response_templates.get_display_response(phone_list_text),
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }

            return {
                'response': self.response_templates.get_display_response(),
                'type': 'text'
            }

        elif intent == 'storage_query':
            # Handle storage queries
            budget = self._extract_budget(message)
            storage_spec = message.lower()
            phones = self.smart_engine.get_phones_by_storage(storage_spec, budget, limit=5)

            if phones:
                phone_list_text = ""
                phone_list = []
                for item in phones:
                    phone = item['phone']
                    phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                    phone_list_text += f"   {item['reason']}\n\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': phone.model_name,
                        'price': phone.price,
                        'image': phone.main_image
                    })

                return {
                    'response': self.response_templates.get_storage_response(phone_list=phone_list_text),
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }

            return {
                'response': self.response_templates.get_storage_response(),
                'type': 'text'
            }

        elif intent == 'feature_query':
            # Handle feature queries
            budget = self._extract_budget(message)
            feature = self._extract_feature(message)
            if feature:
                phones = self.smart_engine.get_phones_by_feature(feature, budget, limit=5)

                if phones:
                    phone_list_text = ""
                    phone_list = []
                    for item in phones:
                        phone = item['phone']
                        phone_list_text += f"📱 {phone.model_name} - RM{phone.price:,.2f}\n"
                        phone_list_text += f"   {item['reason']}\n\n"
                        phone_list.append({
                            'id': phone.id,
                            'name': phone.model_name,
                            'price': phone.price,
                            'image': phone.main_image
                        })

                    return {
                        'response': self.response_templates.get_feature_response(feature, phone_list_text),
                        'type': 'recommendation',
                        'metadata': {'phones': phone_list, 'feature': feature}
                    }

            return {
                'response': self.response_templates.get_feature_response(),
                'type': 'text'
            }

        elif intent == 'help':
            return {
                'response': self.response_templates.get_help_response(),
                'type': 'text'
            }

        else:  # general or fallback
            return {
                'response': self.response_templates.get_fallback_response(),
                'type': 'text',
                'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
            }

    def _extract_budget(self, message):
        """Extract budget range from message - Enhanced to handle 'within', ranges, and standalone numbers"""
        # Look for patterns like "RM1000", "1000", "under 2000", "between 1000 and 2000", "within 3000", "2000-3000"
        patterns = [
            r'between\s*rm?\s*(\d+)\s*(?:to|-|and)\s*rm?\s*(\d+)',  # between RM1000 and RM2000
            r'rm\s*(\d+)\s*(?:to|-|and)\s*rm\s*(\d+)',  # RM1000 to RM2000
            r'(\d+)\s*(?:to|-|and)\s*(\d+)',  # 1000 to 2000 or 2000-3000
            r'(?:under|below|within)\s*rm?\s*(\d+)',  # under/below/within RM2000 or within 3000
            r'rm\s*(\d+)',  # RM2000
            r'(?:^|\s)(\d{3,5})(?:\s|$)',  # standalone number like "3000" (3-5 digits)
        ]

        for pattern in patterns:
            match = re.search(pattern, message.lower())
            if match:
                if 'under' in message.lower() or 'below' in message.lower() or 'within' in message.lower():
                    max_budget = int(match.group(1))
                    return (500, max_budget)
                elif len(match.groups()) >= 2 and match.group(2):
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

    def _detect_persona(self, message):
        """Detect user persona from message to infer usage and budget needs"""
        message_lower = message.lower()

        # Persona patterns: (persona_name, usage_type, budget_range)
        personas = {
            'senior': (['senior', 'elderly', 'old age', 'retired'], 'Basic', (500, 1500)),
            'student': (['student', 'university', 'college'], 'Gaming', (1000, 3000)),
            'professional': (['professional', 'businessman', 'working', 'executive'], 'Business', (2500, 5000)),
            'photographer': (['photographer', 'content creator', 'vlogger'], 'Photography', (2000, 6000)),
            'gamer': (['gamer', 'gaming enthusiast'], 'Gaming', (2000, 5000)),
        }

        for persona_key, (keywords, usage, budget) in personas.items():
            if any(keyword in message_lower for keyword in keywords):
                return {'persona': persona_key, 'usage': usage, 'budget': budget}

        return None

    def _detect_usage_type(self, message):
        """Detect usage type from message - Enhanced with persona detection"""
        message_lower = message.lower()

        # First check for persona
        persona = self._detect_persona(message)
        if persona:
            return persona['usage']  # Return usage from persona mapping

        # Fallback to keyword-based detection
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
        elif 'basic' in message_lower or 'simple' in message_lower or 'call' in message_lower:
            return 'Basic'  # For senior citizens and basic users

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

    def _extract_feature(self, message):
        """Extract feature from message"""
        message_lower = message.lower()

        # Map common feature keywords to feature names
        feature_map = {
            '5g': '5G',
            'wireless charging': 'wireless charging',
            'waterproof': 'water resistance',
            'water resistant': 'water resistance',
            'ip68': 'water resistance',
            'expandable storage': 'expandable storage',
            'sd card': 'expandable storage',
            'dual sim': 'dual SIM',
            'fast charging': 'fast charging',
            'amoled': 'AMOLED display',
            'oled': 'AMOLED display',
            'nfc': 'NFC',
            'fingerprint': 'fingerprint sensor',
            'face unlock': 'face unlock',
            '120hz': '120Hz refresh rate',
            '90hz': '90Hz refresh rate'
        }

        for keyword, feature in feature_map.items():
            if keyword in message_lower:
                return feature

        return None

    def _save_chat_history(self, user_id, message, response, intent, session_id, metadata):
        """Save conversation to database - only for authenticated users"""
        # Only save if user_id is an integer (authenticated user)
        # Guest users (session_id strings) won't have history saved
        if not isinstance(user_id, int):
            return  # Skip saving for guest users

        try:
            # Convert numpy string to regular string if needed
            if hasattr(intent, 'item'):
                intent = intent.item()

            # Convert metadata to JSON string for Oracle compatibility
            metadata_json = json.dumps(metadata) if metadata else None

            chat = ChatHistory(
                user_id=user_id,
                message=message,
                response=response,
                intent=str(intent),
                session_id=session_id or datetime.utcnow().strftime('%Y%m%d%H%M%S'),
                chat_metadata=metadata_json  # Store as JSON string for Oracle
            )
            db.session.add(chat)
            db.session.commit()
        except Exception as e:
            # If saving fails, just log and continue (don't break the chat)
            print(f"Warning: Could not save chat history: {e}")
            db.session.rollback()

    def get_chat_history(self, user_id, session_id=None, limit=50):
        """Retrieve chat history for a user"""
        query = ChatHistory.query.filter_by(user_id=user_id)

        if session_id:
            query = query.filter_by(session_id=session_id)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
