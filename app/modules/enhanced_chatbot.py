"""
Enhanced ML-Powered Chatbot Engine
Intelligent conversational assistant with context awareness and advanced NLU
"""
from app import db
from app.models import ChatHistory, Phone, Brand, PhoneSpecification
from app.modules.ai_engine import AIRecommendationEngine
from app.modules.nlu_engine import NLUEngine
from app.modules.context_manager import ContextManager
from fuzzywuzzy import fuzz, process
from sqlalchemy import and_, or_
import re
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class EnhancedChatbotEngine:
    """ML-powered conversational AI chatbot for DialSmart"""

    def __init__(self):
        self.ai_engine = AIRecommendationEngine()
        self.nlu_engine = NLUEngine()
        self.context_manager = ContextManager()

    def process_message(self, user_id, message, session_id=None):
        """
        Process user message with ML-powered NLU and context awareness

        Args:
            user_id: User ID (can be None for guests)
            message: User's message text
            session_id: Session ID for conversation grouping

        Returns:
            Dictionary with response and metadata
        """
        if not session_id:
            session_id = f"session_{user_id or 'guest'}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"

        # Get conversation context
        context = self.context_manager.get_context(session_id)
        context_dict = {
            'last_intent': context.last_intent,
            'last_specs': context.get_active_filters(),
            'battery_focus': context.battery_focus,
            'camera_focus': context.camera_focus,
            'brand_preferences': context.get_brand_preferences()
        }

        # Analyze message with NLU
        analysis = self.nlu_engine.analyze_message(message, context_dict)

        # Update context
        self.context_manager.update_context(session_id, analysis)
        context = self.context_manager.get_context(session_id)

        # Generate response based on analysis
        response_data = self._generate_intelligent_response(
            user_id, message, analysis, context
        )

        # Save to chat history
        if user_id:
            self._save_chat_history(
                user_id=user_id,
                message=message,
                response=response_data['response'],
                intent=analysis['intent'],
                session_id=session_id,
                metadata=response_data.get('metadata', {})
            )

        return response_data

    def _generate_intelligent_response(self, user_id, message, analysis: Dict, context) -> Dict:
        """Generate intelligent response based on NLU analysis and context"""

        intent = analysis['intent']

        # Greeting
        if intent == 'greeting':
            return self._handle_greeting()

        # Help
        elif intent == 'help':
            return self._handle_help()

        # Model search (single or multiple)
        elif intent in ['model_search', 'multi_model_search']:
            return self._handle_model_search(analysis, context)

        # Spec filter (battery, camera, etc.)
        elif intent == 'spec_filter':
            return self._handle_spec_filter(analysis, context)

        # Battery focused recommendation
        elif intent == 'battery_focused':
            return self._handle_battery_recommendation(analysis, context)

        # Camera/Photography focused
        elif intent == 'camera_focused':
            return self._handle_photography_recommendation(analysis, context)

        # Usage type recommendation
        elif intent == 'usage_recommendation':
            return self._handle_usage_recommendation(analysis, context)

        # Brand query
        elif intent == 'brand_query':
            return self._handle_brand_query(analysis, context)

        # Budget query
        elif intent == 'budget_query':
            return self._handle_budget_query(analysis, context)

        # Comparison
        elif intent == 'comparison':
            return self._handle_comparison()

        # General/fallback
        else:
            return self._handle_general(analysis, context)

    def _handle_greeting(self) -> Dict:
        """Handle greeting messages"""
        return {
            'response': "Hello! I'm DialSmart AI Assistant. I'm here to help you find the perfect smartphone. How can I assist you today?",
            'type': 'text',
            'quick_replies': ['Find a phone', 'Compare phones', 'Show me budget options']
        }

    def _handle_help(self) -> Dict:
        """Handle help requests"""
        return {
            'response': """I can help you with:

📱 Find phone recommendations based on your needs
💰 Search phones within your budget
🔍 Compare different phone models
📊 Get detailed specifications
🏷️ Browse phones by brand
🔋 Find long-lasting phones with great battery
📸 Recommend phones for photography

Just ask me anything like:
• "Find me a phone under RM2000"
• "Best phones for gaming"
• "Show me Samsung phones"
• "I need a phone with good camera"
• "Long lasting phone"
• "iPhone 15 pro and Xiaomi 14 pro"
""",
            'type': 'text'
        }

    def _handle_model_search(self, analysis: Dict, context) -> Dict:
        """Handle model-specific search (including multi-model queries)"""
        models = analysis['models']

        if analysis['is_multi_model_query'] or len(models) > 1:
            # Handle multiple models (e.g., "iphone 17 pro and xiaomi 17 pro")
            return self._search_multiple_models(analysis)
        else:
            # Handle single model search
            return self._search_single_model(models[0] if models else analysis['original_message'], analysis, context)

    def _search_single_model(self, model_query: Any, analysis: Dict, context) -> Dict:
        """Search for a single phone model with fuzzy matching"""
        # Extract model text
        if isinstance(model_query, dict):
            model_text = model_query['text']
        else:
            model_text = str(model_query)

        # Get all phone models from database
        all_phones = Phone.query.filter_by(is_active=True).all()
        model_names = [f"{p.brand.name} {p.model_name}" for p in all_phones if p.brand]

        # Try fuzzy matching
        matches = process.extract(model_text, model_names, scorer=fuzz.token_sort_ratio, limit=10)

        # Filter matches with score >= 60 (more lenient for partial names)
        good_matches = [(name, score) for name, score in matches if score >= 60]

        if good_matches:
            # Get the actual phone objects
            matched_phones = []
            for matched_name, score in good_matches:
                for phone in all_phones:
                    full_name = f"{phone.brand.name} {phone.model_name}"
                    if full_name == matched_name:
                        matched_phones.append(phone)
                        break

            # Limit to top 5
            matched_phones = matched_phones[:5]

            if len(matched_phones) == 1:
                phone = matched_phones[0]
                specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()

                response = f"I found {phone.brand.name} {phone.model_name}:\n\n"
                response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                if specs:
                    if specs.battery_capacity:
                        response += f"🔋 {specs.battery_capacity}mAh battery\n"
                    if specs.rear_camera_main:
                        response += f"📸 {specs.rear_camera_main}MP camera\n"
                    if specs.ram_options:
                        response += f"💾 {specs.ram_options} RAM\n"
                    if specs.storage_options:
                        response += f"💿 {specs.storage_options} Storage\n"

                response += f"\n👉 View Details"

                return {
                    'response': response,
                    'type': 'recommendation',
                    'metadata': {
                        'phones': [{
                            'id': phone.id,
                            'name': f"{phone.brand.name} {phone.model_name}",
                            'price': phone.price
                        }]
                    }
                }
            else:
                # Multiple matches found
                response = f"I found {len(matched_phones)} phone(s) matching your query:\n\n"
                phone_list = []

                for phone in matched_phones:
                    response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                    response += f"👉 View Details\n"
                    phone_list.append({
                        'id': phone.id,
                        'name': f"{phone.brand.name} {phone.model_name}",
                        'price': phone.price
                    })

                response += "\nClick any link above to see full details!"

                return {
                    'response': response,
                    'type': 'recommendation',
                    'metadata': {'phones': phone_list}
                }
        else:
            return {
                'response': f"I couldn't find a specific model matching '{model_text}'. Would you like to:\n• See all phones from a specific brand\n• Get recommendations based on your budget\n• Browse by category",
                'type': 'text'
            }

    def _search_multiple_models(self, analysis: Dict) -> Dict:
        """Search for multiple phone models"""
        # Extract all model names from the message
        message = analysis['original_message']

        # Split by common separators
        model_queries = re.split(r'\s+and\s+|\s*&\s*|\s*,\s*', message, flags=re.IGNORECASE)

        # Get all phones
        all_phones = Phone.query.filter_by(is_active=True).all()
        model_names_map = {f"{p.brand.name} {p.model_name}": p for p in all_phones if p.brand}

        found_phones = []

        for query in model_queries:
            query = query.strip()
            if not query:
                continue

            # Fuzzy match each query
            matches = process.extract(query, list(model_names_map.keys()), scorer=fuzz.token_sort_ratio, limit=1)

            if matches and matches[0][1] >= 60:
                matched_name = matches[0][0]
                phone = model_names_map[matched_name]
                if phone not in found_phones:
                    found_phones.append(phone)

        if found_phones:
            response = f"I found {len(found_phones)} phone(s) matching your query:\n\n"
            phone_list = []

            for phone in found_phones:
                response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
                response += f"👉 View Details\n"
                phone_list.append({
                    'id': phone.id,
                    'name': f"{phone.brand.name} {phone.model_name}",
                    'price': phone.price
                })

            response += "\nClick any link above to see full details!"

            # Add side-by-side display data
            for phone in found_phones:
                brand_name = phone.brand.name if phone.brand else 'Unknown'
                response += f"\n{brand_name} {phone.model_name}\n"
                response += f"{brand_name} {phone.model_name}\n"
                response += f"RM {phone.price:.2f}\n"

            return {
                'response': response,
                'type': 'recommendation',
                'metadata': {'phones': phone_list}
            }
        else:
            return {
                'response': "Sorry, I could not find the phone models you specified. Please check the model names and try again.",
                'type': 'text'
            }

    def _handle_spec_filter(self, analysis: Dict, context) -> Dict:
        """Handle specification-based filtering"""
        specs = analysis['specs']
        brands = context.get_brand_preferences()

        # Build query
        query = Phone.query.filter_by(is_active=True)

        filters = []
        response_filters = []

        # Brand filter (apply context preferences)
        if brands['preferred']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['preferred'])).all()]
            if brand_ids:
                filters.append(Phone.brand_id.in_(brand_ids))
                response_filters.append(f"Brands: {', '.join(brands['preferred'])}")

        # Exclude hated brands
        if brands['excluded']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['excluded'])).all()]
            if brand_ids:
                filters.append(~Phone.brand_id.in_(brand_ids))

        # Budget filter
        budget = context.current_filters.get('budget') or analysis.get('budget')
        if budget:
            min_price, max_price = budget
            filters.append(Phone.price >= min_price)
            filters.append(Phone.price <= max_price)
            response_filters.append(f"Budget: RM{min_price} - RM{max_price}")

        if filters:
            query = query.filter(and_(*filters))

        phones = query.all()

        # Further filter by specs (using PhoneSpecification)
        filtered_phones = []
        for phone in phones:
            phone_specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if not phone_specs:
                continue

            include = True

            # Battery filter
            if specs.get('battery_min'):
                if not phone_specs.battery_capacity or phone_specs.battery_capacity < specs['battery_min']:
                    include = False

            # Camera filter
            if specs.get('camera_min'):
                if not phone_specs.rear_camera_main or phone_specs.rear_camera_main < specs['camera_min']:
                    include = False

            # RAM filter
            if specs.get('ram_min'):
                # Parse RAM options
                ram_values = self._extract_numeric_values(phone_specs.ram_options or '')
                if not ram_values or max(ram_values) < specs['ram_min']:
                    include = False

            # Storage filter
            if specs.get('storage_min'):
                storage_values = self._extract_numeric_values(phone_specs.storage_options or '')
                if not storage_values or max(storage_values) < specs['storage_min']:
                    include = False

            if include:
                filtered_phones.append((phone, phone_specs))

        if not filtered_phones:
            filter_desc = ' and '.join(response_filters) if response_filters else 'your requirements'
            return {
                'response': f"I couldn't find phones matching {filter_desc}. Would you like to:\n• Adjust your budget\n• See similar phones\n• Browse by brand",
                'type': 'text'
            }

        # Sort by relevance (battery for battery queries, camera for camera queries)
        if specs.get('battery_min'):
            filtered_phones.sort(key=lambda x: x[1].battery_capacity or 0, reverse=True)
        elif specs.get('camera_min'):
            filtered_phones.sort(key=lambda x: x[1].rear_camera_main or 0, reverse=True)

        # Limit to top 5
        filtered_phones = filtered_phones[:5]

        # Build response
        filter_desc = ', '.join(response_filters) if response_filters else 'your filters'
        if specs.get('battery_min'):
            response = f"Here are phones with battery above {specs['battery_min']}mAh"
            if brands['preferred']:
                response += f" from {', '.join(brands['preferred'])}"
            response += ":\n\n"
        elif specs.get('camera_min'):
            response = f"Here are phones with camera above {specs['camera_min']}MP"
            if brands['preferred']:
                response += f" from {', '.join(brands['preferred'])}"
            response += ":\n\n"
        else:
            response = f"Here are the best phones for {filter_desc}:\n\n"

        phone_list = []
        for phone, phone_specs in filtered_phones:
            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

            if specs.get('battery_min') and phone_specs.battery_capacity:
                response += f"🔋 {phone_specs.battery_capacity}mAh battery\n"
            if specs.get('camera_min') and phone_specs.rear_camera_main:
                response += f"📸 {phone_specs.rear_camera_main}MP camera\n"

            response += "\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        # Add visual list at end
        for phone, phone_specs in filtered_phones:
            brand_name = phone.brand.name if phone.brand else 'Unknown'
            response += f"{brand_name} {phone.model_name}\n"
            response += f"{brand_name} {phone.model_name}\n"
            response += f"RM {phone.price:.2f}\n\n"

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list}
        }

    def _handle_battery_recommendation(self, analysis: Dict, context) -> Dict:
        """Handle requests for long-lasting phones / good battery"""
        brands = context.get_brand_preferences()

        # Build query
        query = Phone.query.filter_by(is_active=True)

        filters = []

        # Brand preference from context
        if brands['preferred']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['preferred'])).all()]
            if brand_ids:
                filters.append(Phone.brand_id.in_(brand_ids))

        # Exclude hated brands
        if brands['excluded']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['excluded'])).all()]
            if brand_ids:
                filters.append(~Phone.brand_id.in_(brand_ids))

        # Budget filter from context
        budget = context.current_filters.get('budget') or analysis.get('budget')
        if budget:
            min_price, max_price = budget
            filters.append(Phone.price >= min_price)
            filters.append(Phone.price <= max_price)

        if filters:
            query = query.filter(and_(*filters))

        phones = query.all()

        # Filter and sort by battery capacity
        phone_battery_pairs = []
        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs and specs.battery_capacity and specs.battery_capacity >= 4000:  # At least 4000mAh
                phone_battery_pairs.append((phone, specs))

        # Sort by battery capacity descending
        phone_battery_pairs.sort(key=lambda x: x[1].battery_capacity, reverse=True)

        # Limit to top 5
        phone_battery_pairs = phone_battery_pairs[:5]

        if not phone_battery_pairs:
            return {
                'response': "I couldn't find phones with good battery in your criteria. Would you like to adjust your filters?",
                'type': 'text'
            }

        # Build response
        brand_text = f" from {', '.join(brands['preferred'])}" if brands['preferred'] else ""
        budget_text = ""
        if budget:
            budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

        response = f"Here are the best{brand_text} phones with battery{budget_text}:\n\n"

        phone_list = []
        for phone, specs in phone_battery_pairs:
            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
            response += f"🔋 {specs.battery_capacity}mAh battery\n\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        # Add visual list
        for phone, specs in phone_battery_pairs:
            brand_name = phone.brand.name if phone.brand else 'Unknown'
            response += f"{brand_name} {phone.model_name}\n"
            response += f"{brand_name} {phone.model_name}\n"
            response += f"RM {phone.price:.2f}\n\n"

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list}
        }

    def _handle_photography_recommendation(self, analysis: Dict, context) -> Dict:
        """Handle photography/camera focused recommendations"""
        brands = context.get_brand_preferences()

        # Build query
        query = Phone.query.filter_by(is_active=True)

        filters = []

        # Brand preference
        if brands['preferred']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['preferred'])).all()]
            if brand_ids:
                filters.append(Phone.brand_id.in_(brand_ids))

        # Exclude hated brands
        if brands['excluded']:
            brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['excluded'])).all()]
            if brand_ids:
                filters.append(~Phone.brand_id.in_(brand_ids))

        # Budget filter
        budget = context.current_filters.get('budget') or analysis.get('budget')
        if budget:
            min_price, max_price = budget
            filters.append(Phone.price >= min_price)
            filters.append(Phone.price <= max_price)

        if filters:
            query = query.filter(and_(*filters))

        phones = query.all()

        # Filter by camera quality (consider both camera MP and storage)
        phone_camera_pairs = []
        min_camera_mp = analysis['specs'].get('camera_min', 48)  # Default to 48MP for photography

        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            if specs and specs.rear_camera_main and specs.rear_camera_main >= min_camera_mp:
                # Calculate camera score (camera MP + storage bonus)
                camera_score = specs.rear_camera_main

                # Add storage bonus
                storage_values = self._extract_numeric_values(specs.storage_options or '')
                if storage_values:
                    max_storage = max(storage_values)
                    camera_score += max_storage / 10  # Bonus for large storage

                phone_camera_pairs.append((phone, specs, camera_score))

        # Sort by camera score
        phone_camera_pairs.sort(key=lambda x: x[2], reverse=True)

        # Limit to top 5
        phone_camera_pairs = phone_camera_pairs[:5]

        if not phone_camera_pairs:
            return {
                'response': f"I couldn't find phones with camera above {min_camera_mp}MP matching your criteria. Would you like to see phones with lower camera specifications?",
                'type': 'text'
            }

        # Build response
        brand_text = f" from {', '.join(brands['preferred'])}" if brands['preferred'] else ""
        budget_text = ""
        if budget:
            budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

        response = f"Great choice! Here are the best phones for Photography{brand_text}{budget_text}:\n\n"

        phone_list = []
        for phone, specs, score in phone_camera_pairs:
            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"
            if specs.rear_camera_main:
                response += f"📸 {specs.rear_camera_main}MP camera\n"
            if specs.storage_options:
                response += f"💿 {specs.storage_options} Storage\n"
            response += "\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list}
        }

    def _handle_usage_recommendation(self, analysis: Dict, context) -> Dict:
        """Handle usage-type based recommendations"""
        usage_type = analysis['usage_type']
        budget = context.current_filters.get('budget') or analysis.get('budget')

        phones = self.ai_engine.get_phones_by_usage(usage_type, budget, top_n=5)

        if not phones:
            return {
                'response': f"I couldn't find phones optimized for {usage_type}. Would you like to see general recommendations?",
                'type': 'text'
            }

        response = f"Great choice! Here are the best phones for {usage_type}:\n\n"
        phone_list = []

        for item in phones:
            phone = item['phone']
            specs = item.get('specifications')

            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

            if specs:
                if usage_type == 'Photography' and specs.rear_camera_main:
                    response += f"📸 {specs.rear_camera_main}MP camera\n"
                elif specs.battery_capacity:
                    response += f"🔋 {specs.battery_capacity}mAh battery\n"

            response += "\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list, 'usage': usage_type}
        }

    def _handle_brand_query(self, analysis: Dict, context) -> Dict:
        """Handle brand-specific queries with context awareness"""
        brands = context.get_brand_preferences()

        # If context has battery/camera focus, maintain it
        focus = context.should_maintain_focus()

        if focus['battery'] and brands['preferred']:
            # Continue with battery recommendation but for new brand
            return self._handle_battery_recommendation(analysis, context)
        elif focus['camera'] and brands['preferred']:
            # Continue with camera recommendation but for new brand
            return self._handle_photography_recommendation(analysis, context)

        # Regular brand query
        if not brands['preferred']:
            return {
                'response': "Which brand are you interested in? We have Samsung, Apple, Xiaomi, Huawei, Vivo, Oppo, Realme, and more!",
                'type': 'text'
            }

        # Build query
        query = Phone.query.filter_by(is_active=True)

        # Filter by preferred brands
        brand_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['preferred'])).all()]
        if brand_ids:
            query = query.filter(Phone.brand_id.in_(brand_ids))

        # Exclude hated brands
        if brands['excluded']:
            excluded_ids = [b.id for b in Brand.query.filter(Brand.name.in_(brands['excluded'])).all()]
            if excluded_ids:
                query = query.filter(~Phone.brand_id.in_(excluded_ids))

        # Apply budget filter if exists in context
        budget = context.current_filters.get('budget') or analysis.get('budget')
        if budget:
            min_price, max_price = budget
            query = query.filter(and_(Phone.price >= min_price, Phone.price <= max_price))

        phones = query.limit(5).all()

        if not phones:
            brand_names = ', '.join(brands['preferred'])
            return {
                'response': f"I couldn't find {brand_names} phones matching your criteria. Would you like to adjust your filters?",
                'type': 'text'
            }

        # Build response
        brand_names = ', and '.join(brands['preferred']) if len(brands['preferred']) > 1 else brands['preferred'][0]
        budget_text = ""
        if budget:
            budget_text = f" within RM{budget[0]:,.0f} - RM{budget[1]:,.0f}"

        response = f"Here are {brand_names} phones{budget_text}:\n\n"

        phone_list = []
        for phone in phones:
            specs = PhoneSpecification.query.filter_by(phone_id=phone.id).first()
            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

            if specs:
                if specs.ram_options:
                    response += f"{specs.ram_options} RAM - "
                if specs.storage_options:
                    response += f"{specs.storage_options} Storage"
                response += "\n"

            response += "\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        # Add visual display
        for phone in phones:
            brand_name = phone.brand.name if phone.brand else 'Unknown'
            response += f"{brand_name} {phone.model_name}\n"
            response += f"{brand_name} {phone.model_name}\n"
            response += f"RM {phone.price:.2f}\n\n"

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list, 'brands': brands['preferred']}
        }

    def _handle_budget_query(self, analysis: Dict, context) -> Dict:
        """Handle budget-based queries"""
        budget = analysis.get('budget')
        if not budget:
            return {
                'response': "What's your budget range? For example, 'I'm looking for phones under RM2000' or 'phones between RM1000 and RM3000'",
                'type': 'text'
            }

        min_budget, max_budget = budget

        phones = self.ai_engine.get_budget_recommendations((min_budget, max_budget), top_n=5)

        if not phones:
            return {
                'response': f"I couldn't find phones in that exact range (RM{min_budget}-RM{max_budget}). Would you like to adjust your budget?",
                'type': 'text'
            }

        response = f"Here are the top phones within RM{min_budget:,.0f} - RM{max_budget:,.0f}:\n\n"
        phone_list = []

        for item in phones:
            phone = item['phone']
            specs = item.get('specifications')

            response += f"📱 {phone.brand.name} {phone.model_name} - RM{phone.price:,.2f}\n"

            if specs and specs.ram_options:
                response += f"{specs.ram_options} RAM - "
                if specs.storage_options:
                    response += f"{specs.storage_options} Storage"
                response += "\n"

            response += "\n"

            phone_list.append({
                'id': phone.id,
                'name': f"{phone.brand.name} {phone.model_name}",
                'price': phone.price
            })

        return {
            'response': response,
            'type': 'recommendation',
            'metadata': {'phones': phone_list}
        }

    def _handle_comparison(self) -> Dict:
        """Handle comparison requests"""
        return {
            'response': "I can help you compare phones! Please go to the Compare page and select two phones you'd like to compare side-by-side.",
            'type': 'text',
            'action': 'redirect_compare'
        }

    def _handle_general(self, analysis: Dict, context) -> Dict:
        """Handle general/unclear queries"""
        return {
            'response': "I'm here to help you find the perfect smartphone! You can ask me about:\n\n• Phone recommendations\n• Specific models (e.g., 'iPhone 15', 'Xiaomi 14 Pro')\n• Budget options\n• Brand preferences\n• Phones with specific features (battery, camera, etc.)\n\nWhat would you like to know?",
            'type': 'text',
            'quick_replies': ['Find a phone', 'Budget options', 'Popular brands']
        }

    def _extract_numeric_values(self, text: str) -> List[int]:
        """Extract numeric values from text like '4GB, 6GB, 8GB'"""
        if not text:
            return []

        numbers = re.findall(r'(\d+)\s*GB', text, re.IGNORECASE)
        return [int(n) for n in numbers]

    def _save_chat_history(self, user_id, message, response, intent, session_id, metadata):
        """Save conversation to database"""
        chat = ChatHistory(
            user_id=user_id,
            message=message,
            response=response,
            intent=intent,
            session_id=session_id or datetime.utcnow().strftime('%Y%m%d%H%M%S'),
            response_metadata=json.dumps(metadata) if metadata else None
        )
        db.session.add(chat)
        db.session.commit()

    def get_chat_history(self, user_id, session_id=None, limit=50):
        """Retrieve chat history for a user"""
        query = ChatHistory.query.filter_by(user_id=user_id)

        if session_id:
            query = query.filter_by(session_id=session_id)

        return query.order_by(ChatHistory.created_at.desc()).limit(limit).all()
