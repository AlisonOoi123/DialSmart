"""
Business Logic Modules Package
Contains AI engine, chatbot, and comparison modules
"""
from app.modules.ai_engine import AIRecommendationEngine
from app.modules.chatbot import ChatbotEngine
from app.modules.comparison import PhoneComparison

__all__ = ['AIRecommendationEngine', 'ChatbotEngine', 'PhoneComparison']
