"""
Conversation Context Manager
Maintains conversation state and context across multiple turns
"""
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from collections import defaultdict

class ConversationContext:
    """Manages conversation context for individual sessions"""

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.created_at = datetime.utcnow()
        self.last_updated = datetime.utcnow()

        # Conversation history
        self.messages = []

        # Persistent context
        self.brand_preferences = {
            'preferred': set(),
            'excluded': set()
        }

        self.current_filters = {
            'budget': None,
            'battery_min': None,
            'camera_min': None,
            'ram_min': None,
            'storage_min': None,
            'usage_type': None,
            'has_5g': None
        }

        # Last intent and entities
        self.last_intent = None
        self.last_entities = {}

        # Focus tracking
        self.battery_focus = False
        self.camera_focus = False
        self.photography_focus = False

        # Query history
        self.previous_recommendations = []

    def update(self, analysis: Dict[str, Any]):
        """Update context with new analysis"""
        self.last_updated = datetime.utcnow()

        # Add to message history
        self.messages.append({
            'timestamp': self.last_updated,
            'analysis': analysis
        })

        # Update brand preferences
        # FIXED: Only accumulate if explicit sentiment, otherwise it's a context switch
        if analysis.get('has_explicit_sentiment'):
            # Explicit hate/love - accumulate preferences
            if analysis['brands']['preferred']:
                for brand in analysis['brands']['preferred']:
                    self.brand_preferences['preferred'].add(brand)
                    # Remove from excluded if previously excluded
                    self.brand_preferences['excluded'].discard(brand)

            if analysis['brands']['excluded']:
                for brand in analysis['brands']['excluded']:
                    self.brand_preferences['excluded'].add(brand)
                    # Remove from preferred if previously preferred
                    self.brand_preferences['preferred'].discard(brand)
        elif analysis.get('is_simple_brand_query') and not analysis.get('context_continuation'):
            # Simple brand query without sentiment - this is a new search, don't accumulate
            # Keep excluded brands, but preferred brands are for this query only
            pass
        else:
            # Other cases - accumulate as before
            if analysis['brands']['preferred']:
                for brand in analysis['brands']['preferred']:
                    self.brand_preferences['preferred'].add(brand)
                    self.brand_preferences['excluded'].discard(brand)

            if analysis['brands']['excluded']:
                for brand in analysis['brands']['excluded']:
                    self.brand_preferences['excluded'].add(brand)
                    self.brand_preferences['preferred'].discard(brand)

        # Update filters (new values override old)
        if analysis.get('budget'):
            self.current_filters['budget'] = analysis['budget']

        if analysis['specs'].get('battery_min'):
            self.current_filters['battery_min'] = analysis['specs']['battery_min']

        if analysis['specs'].get('camera_min'):
            self.current_filters['camera_min'] = analysis['specs']['camera_min']

        if analysis['specs'].get('ram_min'):
            self.current_filters['ram_min'] = analysis['specs']['ram_min']

        if analysis['specs'].get('storage_min'):
            self.current_filters['storage_min'] = analysis['specs']['storage_min']

        if analysis.get('usage_type'):
            self.current_filters['usage_type'] = analysis['usage_type']

        # Update focus flags
        if analysis.get('requires_battery_focus'):
            self.battery_focus = True

        if analysis.get('requires_camera_focus'):
            self.camera_focus = True
            self.photography_focus = True

        # Update last intent and entities
        self.last_intent = analysis.get('intent')
        self.last_entities = analysis

    def get_active_filters(self) -> Dict[str, Any]:
        """Get currently active filters"""
        active = {}

        for key, value in self.current_filters.items():
            if value is not None:
                active[key] = value

        return active

    def get_brand_preferences(self) -> Dict[str, List[str]]:
        """Get brand preferences as lists"""
        return {
            'preferred': list(self.brand_preferences['preferred']),
            'excluded': list(self.brand_preferences['excluded'])
        }

    def should_maintain_focus(self) -> Dict[str, bool]:
        """Check if should maintain specific focus"""
        return {
            'battery': self.battery_focus,
            'camera': self.camera_focus,
            'photography': self.photography_focus
        }

    def clear_filters(self):
        """Clear all filters (for new search)"""
        self.current_filters = {
            'budget': None,
            'battery_min': None,
            'camera_min': None,
            'ram_min': None,
            'storage_min': None,
            'usage_type': None,
            'has_5g': None
        }
        self.battery_focus = False
        self.camera_focus = False
        self.photography_focus = False

    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """Check if context has expired"""
        return (datetime.utcnow() - self.last_updated) > timedelta(minutes=timeout_minutes)


class ContextManager:
    """Global context manager for all conversations"""

    def __init__(self):
        self.contexts: Dict[str, ConversationContext] = {}
        self.cleanup_interval = 3600  # Clean up every hour

    def get_context(self, session_id: str) -> ConversationContext:
        """Get or create context for a session"""
        # Clean up expired contexts
        self._cleanup_expired()

        if session_id not in self.contexts:
            self.contexts[session_id] = ConversationContext(session_id)

        return self.contexts[session_id]

    def update_context(self, session_id: str, analysis: Dict[str, Any]):
        """Update context with new analysis"""
        context = self.get_context(session_id)
        context.update(analysis)

    def clear_context(self, session_id: str):
        """Clear context for a session"""
        if session_id in self.contexts:
            del self.contexts[session_id]

    def _cleanup_expired(self, timeout_minutes: int = 30):
        """Remove expired contexts"""
        expired = [
            session_id for session_id, ctx in self.contexts.items()
            if ctx.is_expired(timeout_minutes)
        ]

        for session_id in expired:
            del self.contexts[session_id]

    def get_all_contexts(self) -> Dict[str, ConversationContext]:
        """Get all active contexts (for debugging)"""
        return self.contexts
