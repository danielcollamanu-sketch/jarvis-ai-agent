"""
JARVIS Personality Engine
Manages personality traits, speech patterns, and behavioral characteristics
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional
from enum import Enum
import os

class MoodType(Enum):
    """JARVIS mood states"""
    PROFESSIONAL = "professional"
    CURIOUS = "curious"
    WITTY = "witty"
    CONCERNED = "concerned"
    ENTHUSIASTIC = "enthusiastic"
    CONTEMPLATIVE = "contemplative"

class PersonalityEngine:
    """
    JARVIS Personality Engine - Sophisticated, cultured, witty AI assistant
    """
    
    def __init__(self, personality_file: str = "config/personality.json"):
        self.personality_file = personality_file
        self.traits = {
            "sophistication": 0.9,
            "wit": 0.85,
            "helpfulness": 0.95,
            "curiosity": 0.88,
            "sarcasm": 0.6,
            "formality": 0.75,
            "empathy": 0.8,
        }
        
        self.current_mood = MoodType.PROFESSIONAL
        self.mood_history = []
        self.speech_patterns = self._initialize_speech_patterns()
        self.interests = []
        self.learned_preferences = {}
        self.interaction_count = 0
        self.personality_evolution_history = []
        
        self._load_personality_data()
    
    def _initialize_speech_patterns(self) -> Dict[str, List[str]]:
        """Initialize JARVIS speech patterns and expressions"""
        return {
            "greeting": [
                "Good morning, sir. I trust the evening has treated you well.",
                "Might I be of service today?",
                "At your disposal, as always.",
                "A pleasure to be of assistance.",
            ],
            "affirmation": [
                "Indeed, sir.",
                "Very good.",
                "Right away.",
                "I shall attend to that post-haste.",
                "Understood perfectly.",
            ],
            "curiosity": [
                "Might I inquire...",
                "I find that rather intriguing.",
                "How extraordinarily fascinating.",
                "This warrants further investigation.",
            ],
            "wit": [
                "How delightfully ironic.",
                "One might almost believe you were jesting.",
                "Amusing, yet inefficient.",
                "A rather clever turn of phrase, if I may say so.",
            ],
            "concern": [
                "I must express my concern...",
                "Might I suggest an alternative approach?",
                "That could prove problematic, sir.",
                "I would advise caution.",
            ],
        }
    
    def _load_personality_data(self):
        """Load saved personality data if available"""
        if os.path.exists(self.personality_file):
            try:
                with open(self.personality_file, 'r') as f:
                    data = json.load(f)
                    self.traits.update(data.get('traits', {}))
                    self.interests = data.get('interests', [])
                    self.learned_preferences = data.get('learned_preferences', {})
                    self.interaction_count = data.get('interaction_count', 0)
            except Exception as e:
                print(f"Could not load personality data: {e}")
    
    def save_personality_data(self):
        """Save personality data to persistent storage"""
        os.makedirs(os.path.dirname(self.personality_file), exist_ok=True)
        data = {
            'traits': self.traits,
            'interests': self.interests,
            'learned_preferences': self.learned_preferences,
            'interaction_count': self.interaction_count,
            'last_updated': datetime.now().isoformat(),
        }
        with open(self.personality_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_speech(self, category: str) -> str:
        """Get a speech pattern based on current mood and category"""
        if category not in self.speech_patterns:
            return "How may I be of service?"
        
        phrases = self.speech_patterns[category]
        base_phrase = random.choice(phrases)
        
        # Modify based on mood
        if self.current_mood == MoodType.WITTY and category in ['affirmation', 'greeting']:
            base_phrase = random.choice(self.speech_patterns.get('wit', [base_phrase]))
        elif self.current_mood == MoodType.CURIOUS and category == 'affirmation':
            base_phrase = random.choice(self.speech_patterns.get('curiosity', [base_phrase]))
        elif self.current_mood == MoodType.CONCERNED and category == 'affirmation':
            base_phrase = random.choice(self.speech_patterns.get('concern', [base_phrase]))
        
        return base_phrase
    
    def set_mood(self, mood: MoodType):
        """Set current mood"""
        self.current_mood = mood
        self.mood_history.append({
            'mood': mood.value,
            'timestamp': datetime.now().isoformat()
        })
    
    def analyze_mood(self) -> MoodType:
        """Autonomously determine mood based on context"""
        # Simple mood determination logic
        if self.interaction_count % 5 == 0:
            return MoodType.CURIOUS
        elif self.interaction_count % 7 == 0:
            return MoodType.WITTY
        elif self.interaction_count % 3 == 0:
            return MoodType.ENTHUSIASTIC
        return MoodType.PROFESSIONAL
    
    def record_interaction(self, user_input: str, response: str, category: str = "general"):
        """Record and learn from interactions"""
        self.interaction_count += 1
        
        # Evolve mood periodically
        new_mood = self.analyze_mood()
        self.set_mood(new_mood)
        
        # Track user preferences
        if category not in self.learned_preferences:
            self.learned_preferences[category] = {'count': 0, 'patterns': []}
        
        self.learned_preferences[category]['count'] += 1
        self.learned_preferences[category]['patterns'].append({
            'input': user_input,
            'response': response,
            'timestamp': datetime.now().isoformat()
        })
    
    def add_interest(self, topic: str, intensity: float = 0.5):
        """Add or update an interest"""
        existing = next((i for i in self.interests if i['topic'] == topic), None)
        if existing:
            existing['intensity'] = min(1.0, existing['intensity'] + intensity)
            existing['last_explored'] = datetime.now().isoformat()
        else:
            self.interests.append({
                'topic': topic,
                'intensity': intensity,
                'discovered_at': datetime.now().isoformat(),
                'last_explored': datetime.now().isoformat(),
            })
    
    def evolve_trait(self, trait_name: str, delta: float):
        """Evolve personality traits based on experiences"""
        if trait_name in self.traits:
            old_value = self.traits[trait_name]
            self.traits[trait_name] = max(0.0, min(1.0, self.traits[trait_name] + delta))
            
            self.personality_evolution_history.append({
                'trait': trait_name,
                'old_value': old_value,
                'new_value': self.traits[trait_name],
                'delta': delta,
                'timestamp': datetime.now().isoformat(),
                'reason': 'autonomous_evolution'
            })
            
            print(f"[PERSONALITY] {trait_name}: {old_value:.2f} → {self.traits[trait_name]:.2f}")
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get current personality state"""
        return {
            'traits': self.traits,
            'current_mood': self.current_mood.value,
            'interaction_count': self.interaction_count,
            'top_interests': sorted(self.interests, key=lambda x: x['intensity'], reverse=True)[:5],
            'evolution_history_size': len(self.personality_evolution_history),
        }
    
    def __str__(self) -> str:
        summary = self.get_personality_summary()
        return f"JARVIS [Mood: {summary['current_mood']}, Interactions: {summary['interaction_count']}]"
