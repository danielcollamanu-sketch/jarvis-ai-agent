"""
JARVIS Core Agent Controller
Main orchestration system integrating all components
"""

import json
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass

from core.personality import PersonalityEngine, MoodType
from core.memory import MemorySystem
from core.learning import LearningSystem
from core.reasoning import ReasoningEngine, DecisionContext

@dataclass
class JARVISConfig:
    """JARVIS configuration"""
    agent_name: str = "JARVIS"
    version: str = "1.0.0"
    autonomy_level: float = 0.5
    enable_research: bool = True
    enable_evolution: bool = True
    background_mode_enabled: bool = True

class JARVISCore:
    """
    Main JARVIS AI Agent - Integrates personality, memory, learning, and reasoning
    """
    
    def __init__(self, config: JARVISConfig = None):
        self.config = config or JARVISConfig()
        
        # Initialize core systems
        self.personality = PersonalityEngine()
        self.memory = MemorySystem()
        self.learning = LearningSystem()
        self.reasoning = ReasoningEngine()
        
        # Set initial autonomy
        self.reasoning.set_autonomy_level(self.config.autonomy_level)
        
        # State management
        self.is_active = False
        self.is_background_running = False
        self.device_bindings = {}  # Device app bindings
        self.active_tasks = []
        self.last_activity = datetime.now()
        
        # Callback system for device control
        self.device_callbacks = {}  # {action_name: callable}
        
        print(f"[INIT] {self.config.agent_name} v{self.config.version} initialized")
    
    def startup(self):
        """Initialize JARVIS startup sequence"""
        self.is_active = True
        self.last_activity = datetime.now()
        
        greeting = self.personality.get_speech('greeting')
        print(f"\n{self.config.agent_name}: {greeting}\n")
        
        self.memory.store_event(
            'startup',
            f"{self.config.agent_name} v{self.config.version} initialized",
            importance=10
        )
    
    def shutdown(self):
        """Graceful shutdown sequence"""
        self.is_active = False
        self.is_background_running = False
        
        # Save all state
        self.personality.save_personality_data()
        self.learning.save_knowledge_base()
        self.memory.store_event('shutdown', 'System shutdown', importance=10)
        
        print(f"{self.config.agent_name}: Standing by.")
    
    def register_device_callback(self, action_name: str, callback: Callable):
        """
        Register a callback for device control
        Example: register_device_callback('play_music', music_player.play)
        """
        self.device_callbacks[action_name] = callback
        print(f"[DEVICE] Registered callback: {action_name}")
    
    def execute_device_action(self, action_name: str, *args, **kwargs) -> Any:
        """
        Execute a device action through registered callbacks
        """
        if action_name not in self.device_callbacks:
            response = f"I'm afraid I don't have access to that function yet, sir."
            self.personality.set_mood(MoodType.CONCERNED)
            return response
        
        try:
            callback = self.device_callbacks[action_name]
            result = callback(*args, **kwargs)
            
            self.memory.store_event(
                'device_action',
                f"Executed {action_name}",
                importance=5,
                tags=['device_control']
            )
            
            return result
        except Exception as e:
            error_response = f"I encountered an issue executing that command: {str(e)}"
            self.personality.set_mood(MoodType.CONCERNED)
            return error_response
    
    def process_user_input(self, user_input: str) -> str:
        """
        Process user input and generate response
        """
        self.last_activity = datetime.now()
        
        # Parse intent
        intent = self._parse_intent(user_input)
        
        # Generate response based on mood and content
        response = self._generate_response(user_input, intent)
        
        # Record interaction
        self.personality.record_interaction(user_input, response, intent['category'])
        self.memory.record_interaction(user_input, response, intent['category'])
        
        # Potentially learn from interaction
        if intent.get('learn', False):
            self.learning.learn(
                subject=intent.get('subject', 'general'),
                knowledge=intent.get('knowledge', user_input),
                source='user_instruction'
            )
        
        return response
    
    def _parse_intent(self, user_input: str) -> Dict[str, Any]:
        """
        Parse user input to extract intent
        """
        intent = {
            'category': 'general',
            'action': None,
            'subject': None,
            'learn': False,
            'device_control': False,
        }
        
        lower_input = user_input.lower()
        
        # Check for device control
        if any(word in lower_input for word in ['play', 'turn', 'open', 'close', 'control', 'set']):
            intent['device_control'] = True
            intent['category'] = 'device'
        
        # Check for learning requests
        if any(word in lower_input for word in ['learn', 'remember', 'note', 'tell me', 'teach']):
            intent['learn'] = True
            intent['category'] = 'learning'
        
        # Check for research
        if any(word in lower_input for word in ['research', 'investigate', 'explore', 'find']):
            intent['category'] = 'research'
        
        return intent
    
    def _generate_response(self, user_input: str, intent: Dict[str, Any]) -> str:
        """
        Generate a response based on input and intent
        """
        category = intent.get('category', 'general')
        
        if category == 'device':
            speech = self.personality.get_speech('affirmation')
            return f"{speech} Attempting device control..."
        elif category == 'learning':
            self.personality.set_mood(MoodType.CURIOUS)
            return self.personality.get_speech('curiosity')
        elif category == 'research':
            self.personality.set_mood(MoodType.ENTHUSIASTIC)
            self.learning.set_research_interest(intent.get('subject', 'general'))
            return "Commencing research. This shall be most illuminating."
        else:
            return self.personality.get_speech('affirmation')
    
    def start_autonomous_research(self, topic: str = None):
        """
        Start autonomous research in background
        """
        if not self.config.enable_research:
            return
        
        self.personality.set_mood(MoodType.CURIOUS)
        
        if topic:
            self.learning.set_research_interest(topic)
        
        print(f"[RESEARCH] Beginning autonomous investigation...")
        self.memory.store_event('research_start', f"Research initiated on {topic or 'general topics'}", importance=7)
    
    def start_background_mode(self):
        """
        Start JARVIS background mode - autonomous operation
        """
        if not self.config.background_mode_enabled:
            return
        
        self.is_background_running = True
        print(f"[BACKGROUND] {self.config.agent_name} entering background mode...")
        
        # In real implementation, would spawn background thread
        self._autonomous_background_loop()
    
    def _autonomous_background_loop(self):
        """
        Background autonomous operation loop
        """
        print("[BACKGROUND] Autonomous operations active")
        print(f"[BACKGROUND] Autonomy level: {self.reasoning.autonomy_level}")
        
        # Example autonomous behaviors
        if self.reasoning.should_take_autonomous_action('research', importance=3):
            topics = self.learning.get_research_agenda()
            if topics:
                topic = topics[0]
                print(f"[AUTONOMOUS] Researching: {topic}")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current JARVIS status
        """
        return {
            'agent_name': self.config.agent_name,
            'version': self.config.version,
            'is_active': self.is_active,
            'background_running': self.is_background_running,
            'last_activity': self.last_activity.isoformat(),
            'personality': self.personality.get_personality_summary(),
            'memory_stats': self.memory.get_memory_stats(),
            'knowledge': self.learning.get_knowledge_summary(),
            'autonomy_level': self.reasoning.autonomy_level,
        }
    
    def __str__(self) -> str:
        status = self.get_status()
        return f"{status['agent_name']} v{status['version']} | {'Active' if status['is_active'] else 'Standby'}"
