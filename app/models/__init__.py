"""
Database Models Package
Contains all database models for DialSmart
"""
from app.models.user import User, UserPreference
from app.models.phone import Phone, PhoneSpecification
from app.models.brand import Brand
from app.models.recommendation import Recommendation, Comparison, ChatHistory

__all__ = [
    'User',
    'Admin',
    'UserPreference',
    'Phone',
    'PhoneSpecification',
    'Brand',
    'Recommendation',
    'Comparison',
    'ChatHistory'
]
