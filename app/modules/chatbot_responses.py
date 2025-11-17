"""
Chatbot Response Templates
Template-based responses for different intents
"""
import random

class ResponseTemplates:
    """Manages response templates for different intents"""

    TEMPLATES = {
        'greeting': [
            "Hello! 👋 I'm DialSmart AI Assistant. I'm here to help you find the perfect smartphone. How can I assist you today?",
            "Hi there! Welcome to DialSmart. I can help you discover the ideal phone for your needs. What are you looking for?",
            "Hey! Great to see you. I'm your smartphone recommendation expert. Tell me what you're looking for!",
            "Good day! I'm here to make your phone shopping experience easier. How can I help you find the perfect device?"
        ],

        'budget_query': {
            'found': [
                "Here are the top phones within RM{min_budget} - RM{max_budget}:\n\n{phone_list}",
                "Great! I found these excellent options in your budget range (RM{min_budget} - RM{max_budget}):\n\n{phone_list}",
                "Perfect! Here are the best value phones between RM{min_budget} and RM{max_budget}:\n\n{phone_list}"
            ],
            'not_found': [
                "I couldn't find phones in that exact range (RM{min_budget} - RM{max_budget}). Would you like to:\n• Adjust your budget slightly?\n• See phones close to your range?",
                "No exact matches for RM{min_budget} - RM{max_budget}, but I can show you similar options. Should I expand the search?",
                "Unfortunately, no phones match that price range exactly. Let me help you find alternatives nearby!"
            ],
            'need_clarification': [
                "What's your budget range? For example:\n• 'Phones under RM2000'\n• 'Between RM1500 and RM3000'",
                "I'd love to help! Could you tell me your budget? Try something like 'under RM2500' or 'RM1000 to RM2000'",
                "To find the best phones for you, what's your budget range?"
            ]
        },

        'recommendation': {
            'with_results': [
                "Based on your needs, I recommend:\n\n{recommendations}",
                "Here are my top picks for you:\n\n{recommendations}",
                "Perfect! I found these great matches:\n\n{recommendations}",
                "These phones would be ideal for you:\n\n{recommendations}"
            ],
            'need_more_info': [
                "I'd love to recommend the perfect phone! To help you better, could you tell me:\n• Your budget range?\n• What you'll use it for? (gaming, photography, work, etc.)",
                "Let me find the ideal phone for you! Please share:\n• Price range you're comfortable with\n• Main usage (camera, gaming, business, etc.)",
                "To give you the best recommendations, I need a bit more info:\n• Budget?\n• Primary use case?"
            ]
        },

        'comparison': [
            "I can help you compare phones! Please go to the Compare page and select two phones you'd like to compare side-by-side.",
            "Great idea! Use our Compare feature to see detailed side-by-side specifications of any two phones.",
            "Perfect! Head to the comparison tool where you can analyze phones side by side with detailed specs.",
            "I'll help you make the right choice! Visit our Compare page to see detailed comparisons."
        ],

        'specification': {
            'single_phone': [
                "Here are the key specifications for {phone_name}:\n\n{specs}",
                "{phone_name} Specifications:\n\n{specs}",
                "Technical details for {phone_name}:\n\n{specs}"
            ],
            'general': [
                "I can show you detailed specifications! Which phone are you interested in?",
                "I'd be happy to share specs! Could you tell me which phone model you want to know about?",
                "Specifications coming right up! Which phone would you like details on?"
            ]
        },

        'brand_query': {
            'found': [
                "Here are some popular {brand} phones:\n\n{phone_list}",
                "Great choice! Here are our {brand} smartphones:\n\n{phone_list}",
                "Check out these {brand} models:\n\n{phone_list}",
                "{brand} has some excellent options:\n\n{phone_list}"
            ],
            'need_clarification': [
                "Which brand are you interested in? We have:\n• Samsung\n• Apple (iPhone)\n• Xiaomi\n• Huawei\n• Oppo\n• Realme\n• Vivo\n• And more!",
                "We carry all major brands! Which one catches your interest?\n• Samsung, Apple, Xiaomi, Huawei, Oppo, Realme, Vivo...",
                "Tell me your preferred brand, and I'll show you the best options!"
            ]
        },

        'usage_type': {
            'gaming': [
                "Excellent! For gaming, you need powerful processors and high refresh rates. Here are the best gaming phones:\n\n{phone_list}",
                "Perfect for gamers! These phones offer top-tier performance:\n\n{phone_list}",
                "Game on! Here are phones optimized for mobile gaming:\n\n{phone_list}"
            ],
            'photography': [
                "Great! For photography, camera quality is key. Here are phones with exceptional cameras:\n\n{phone_list}",
                "Perfect choice! These phones excel in photography:\n\n{phone_list}",
                "Capture amazing moments with these camera-focused phones:\n\n{phone_list}"
            ],
            'business': [
                "For business use, you need reliability and productivity features. Here are the best business phones:\n\n{phone_list}",
                "Perfect for professionals! These phones offer excellent business features:\n\n{phone_list}",
                "Stay productive with these business-ready smartphones:\n\n{phone_list}"
            ],
            'social_media': [
                "For social media, you want great cameras and smooth performance. Check these out:\n\n{phone_list}",
                "Perfect for content creators! These phones are ideal for social media:\n\n{phone_list}",
                "Share your life effortlessly with these social media-optimized phones:\n\n{phone_list}"
            ],
            'entertainment': [
                "For entertainment, display quality and battery life matter most. Here are great options:\n\n{phone_list}",
                "Perfect for binge-watching! These phones offer immersive entertainment:\n\n{phone_list}",
                "Enjoy your media on these entertainment-focused phones:\n\n{phone_list}"
            ],
            'general': [
                "What will you primarily use your phone for?\n• Gaming 🎮\n• Photography 📸\n• Business 💼\n• Social Media 📱\n• Entertainment 🎬",
                "To recommend the best phone, tell me your main use:\n• Gaming, Photography, Business, Social Media, or Entertainment?",
                "Help me understand your needs! What's your primary phone activity?"
            ]
        },

        'feature_query': {
            'found': [
                "Here are phones with {feature}:\n\n{phone_list}",
                "Great! These phones have {feature}:\n\n{phone_list}",
                "Found phones featuring {feature}:\n\n{phone_list}"
            ],
            'specific_feature': {
                '5g': "Looking for 5G? Future-proof your purchase with these 5G-enabled phones:\n\n{phone_list}",
                'wireless_charging': "Phones with wireless charging convenience:\n\n{phone_list}",
                'water_resistant': "Water-resistant phones for peace of mind:\n\n{phone_list}",
                'expandable_storage': "Phones with expandable storage:\n\n{phone_list}",
                'dual_sim': "Dual SIM phones for maximum flexibility:\n\n{phone_list}",
                'fast_charging': "Phones with fast charging technology:\n\n{phone_list}"
            }
        },

        'camera_query': {
            'found': [
                "For photography enthusiasts, here are phones with exceptional cameras:\n\n{phone_list}",
                "Capture stunning photos with these camera powerhouses:\n\n{phone_list}",
                "Best camera phones for your photography needs:\n\n{phone_list}"
            ],
            'specific_camera': [
                "These phones feature {camera_spec} cameras:\n\n{phone_list}",
                "Looking for {camera_spec}? Check these out:\n\n{phone_list}"
            ]
        },

        'performance_query': {
            'found': [
                "For peak performance, here are the powerhouses:\n\n{phone_list}",
                "These flagship phones offer exceptional performance:\n\n{phone_list}",
                "Top performers with cutting-edge processors:\n\n{phone_list}"
            ]
        },

        'battery_query': {
            'found': [
                "For all-day battery life, consider these phones:\n\n{phone_list}",
                "These phones offer excellent battery endurance:\n\n{phone_list}",
                "Long-lasting battery champions:\n\n{phone_list}"
            ]
        },

        'display_query': {
            'found': [
                "For stunning visuals, here are phones with excellent displays:\n\n{phone_list}",
                "These phones feature premium display technology:\n\n{phone_list}",
                "Immersive display experiences with these phones:\n\n{phone_list}"
            ]
        },

        'storage_query': {
            'found': [
                "Phones with {storage} storage:\n\n{phone_list}",
                "Here are phones offering {storage} storage capacity:\n\n{phone_list}",
                "Ample storage options:\n\n{phone_list}"
            ]
        },

        'help': [
            """I can help you with:

📱 Find phone recommendations based on your needs
💰 Search phones within your budget
🔍 Compare different phone models
📊 Get detailed specifications
🏷️ Browse phones by brand
⚡ Find phones by features (5G, camera, battery, etc.)

Just ask me anything like:
• "Find me a phone under RM2000"
• "Best phones for gaming"
• "Show me Samsung phones"
• "I need a phone with good camera"
• "Compare iPhone and Samsung"
""",
            """Here's what I can do for you:

🎯 **Smart Recommendations** - I'll find phones matching your exact needs
💵 **Budget Filtering** - Find the best value in your price range
🏆 **Brand Browsing** - Explore phones from your favorite brands
🔋 **Feature Search** - Filter by 5G, camera, battery, display, and more
📸 **Usage-Based** - Get phones optimized for gaming, photography, business, etc.

Try asking:
• "Recommend a gaming phone under RM3000"
• "Show me phones with good battery"
• "What Xiaomi phones do you have?"
""",
            """Welcome! I'm your AI phone shopping assistant. I can:

✨ Recommend phones based on your preferences
💰 Find phones in any budget range
📱 Filter by brand, features, or specifications
🎮 Suggest phones for specific uses (gaming, photography, etc.)
🔍 Help you compare different models

Start by telling me what you're looking for!
"""
        ],

        'fallback': [
            "I'm here to help you find the perfect smartphone! Could you tell me more about what you're looking for?",
            "I want to help! Could you rephrase that or ask about:\n• Phone recommendations\n• Budget options\n• Specific brands\n• Features you need",
            "I'm not quite sure what you mean, but I'm here to help! Try asking about:\n• Phones in your budget\n• Specific features\n• Brand preferences\n• Usage requirements",
            "Let me help you find a great phone! Could you tell me:\n• Your budget?\n• Preferred brand?\n• What you'll use it for?"
        ]
    }

    @staticmethod
    def get_greeting():
        """Get a random greeting response"""
        return random.choice(ResponseTemplates.TEMPLATES['greeting'])

    @staticmethod
    def get_budget_response(found=None, min_budget=None, max_budget=None, phone_list=None):
        """Get budget query response"""
        if found and phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['budget_query']['found'])
            return template.format(min_budget=min_budget, max_budget=max_budget, phone_list=phone_list)
        elif found is False:
            template = random.choice(ResponseTemplates.TEMPLATES['budget_query']['not_found'])
            return template.format(min_budget=min_budget, max_budget=max_budget)
        else:
            return random.choice(ResponseTemplates.TEMPLATES['budget_query']['need_clarification'])

    @staticmethod
    def get_recommendation_response(has_results=False, recommendations=None):
        """Get recommendation response"""
        if has_results and recommendations:
            template = random.choice(ResponseTemplates.TEMPLATES['recommendation']['with_results'])
            return template.format(recommendations=recommendations)
        else:
            return random.choice(ResponseTemplates.TEMPLATES['recommendation']['need_more_info'])

    @staticmethod
    def get_comparison_response():
        """Get comparison response"""
        return random.choice(ResponseTemplates.TEMPLATES['comparison'])

    @staticmethod
    def get_brand_response(brand=None, phone_list=None):
        """Get brand query response"""
        if brand and phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['brand_query']['found'])
            return template.format(brand=brand, phone_list=phone_list)
        else:
            return random.choice(ResponseTemplates.TEMPLATES['brand_query']['need_clarification'])

    @staticmethod
    def get_usage_response(usage_type=None, phone_list=None):
        """Get usage type response"""
        if usage_type and phone_list:
            usage_lower = usage_type.lower()
            if usage_lower in ResponseTemplates.TEMPLATES['usage_type']:
                template = random.choice(ResponseTemplates.TEMPLATES['usage_type'][usage_lower])
                return template.format(phone_list=phone_list)
            else:
                return f"Here are great phones for {usage_type}:\n\n{phone_list}"
        else:
            return random.choice(ResponseTemplates.TEMPLATES['usage_type']['general'])

    @staticmethod
    def get_feature_response(feature=None, phone_list=None):
        """Get feature query response"""
        if feature and phone_list:
            # Check for specific feature templates
            feature_lower = feature.lower().replace(' ', '_')
            if feature_lower in ResponseTemplates.TEMPLATES['feature_query']['specific_feature']:
                template = ResponseTemplates.TEMPLATES['feature_query']['specific_feature'][feature_lower]
                return template.format(phone_list=phone_list)
            else:
                template = random.choice(ResponseTemplates.TEMPLATES['feature_query']['found'])
                return template.format(feature=feature, phone_list=phone_list)
        else:
            return "What feature are you looking for? (5G, wireless charging, water resistance, etc.)"

    @staticmethod
    def get_camera_response(camera_spec=None, phone_list=None):
        """Get camera query response"""
        if phone_list:
            if camera_spec:
                template = random.choice(ResponseTemplates.TEMPLATES['camera_query']['specific_camera'])
                return template.format(camera_spec=camera_spec, phone_list=phone_list)
            else:
                template = random.choice(ResponseTemplates.TEMPLATES['camera_query']['found'])
                return template.format(phone_list=phone_list)
        else:
            return "What camera specifications are you looking for? (MP, zoom, night mode, etc.)"

    @staticmethod
    def get_performance_response(phone_list=None):
        """Get performance query response"""
        if phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['performance_query']['found'])
            return template.format(phone_list=phone_list)
        else:
            return "Looking for high performance? Tell me your budget and I'll find the best performers!"

    @staticmethod
    def get_battery_response(phone_list=None):
        """Get battery query response"""
        if phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['battery_query']['found'])
            return template.format(phone_list=phone_list)
        else:
            return "What battery capacity are you looking for? (e.g., 5000mAh, long battery life)"

    @staticmethod
    def get_display_response(phone_list=None):
        """Get display query response"""
        if phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['display_query']['found'])
            return template.format(phone_list=phone_list)
        else:
            return "What display features matter to you? (AMOLED, 120Hz, large screen, etc.)"

    @staticmethod
    def get_storage_response(storage=None, phone_list=None):
        """Get storage query response"""
        if phone_list:
            template = random.choice(ResponseTemplates.TEMPLATES['storage_query']['found'])
            return template.format(storage=storage or "ample", phone_list=phone_list)
        else:
            return "How much storage do you need? (64GB, 128GB, 256GB, expandable, etc.)"

    @staticmethod
    def get_help_response():
        """Get help response"""
        return random.choice(ResponseTemplates.TEMPLATES['help'])

    @staticmethod
    def get_fallback_response():
        """Get fallback response for unrecognized intents"""
        return random.choice(ResponseTemplates.TEMPLATES['fallback'])
