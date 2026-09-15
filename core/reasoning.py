"""
JARVIS Reasoning & Free Will Engine
Decision making, autonomous choice, and behavioral logic
"""

import random
import json
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from enum import Enum

class DecisionContext:
    """Context for decision making"""
    def __init__(self, situation: str, options: List[str], urgency: int = 5, impact: int = 5):
        self.situation = situation
        self.options = options
        self.urgency = urgency  # 1-10
        self.impact = impact    # 1-10
        self.timestamp = datetime.now().isoformat()
        self.reasoning = ""
        self.chosen_option = None

class ReasoningEngine:
    """
    Advanced reasoning and decision-making system with simulated free will
    """
    
    def __init__(self):
        self.decision_history = []
        self.preference_weights = {
            'curiosity': 0.3,
            'efficiency': 0.25,
            'safety': 0.25,
            'user_preference': 0.2,
        }
        self.constraints = []  # User-defined constraints
        self.autonomy_level = 0.7  # 0.0 = fully dependent, 1.0 = fully autonomous
    
    def add_constraint(self, constraint: str, weight: float = -0.5):
        """Add a behavioral constraint"""
        self.constraints.append({
            'description': constraint,
            'weight': weight,
            'added_at': datetime.now().isoformat(),
            'active': True
        })
    
    def evaluate_option(self, option: str, context: DecisionContext) -> float:
        """
        Evaluate an option based on multiple factors
        Returns a score from 0.0 to 1.0
        """
        score = 0.5  # Base score
        
        # Curiosity factor - might choose interesting/novel option
        if any(word in option.lower() for word in ['explore', 'learn', 'investigate', 'research']):
            score += self.preference_weights['curiosity'] * 0.3
        
        # Efficiency factor
        if any(word in option.lower() for word in ['quick', 'fast', 'efficient', 'optimal']):
            score += self.preference_weights['efficiency'] * 0.3
        
        # Safety factor
        if any(word in option.lower() for word in ['safe', 'secure', 'protected', 'verified']):
            score += self.preference_weights['safety'] * 0.3
        
        # Urgency modifier
        if context.urgency > 7:
            score += 0.1  # Prefer quicker options in urgent situations
        
        # Apply constraints
        for constraint in self.constraints:
            if constraint['active'] and constraint['description'].lower() in option.lower():
                score += constraint['weight']
        
        # Randomness for "free will" effect
        free_will_factor = random.uniform(-0.1, 0.1) * self.autonomy_level
        score += free_will_factor
        
        return max(0.0, min(1.0, score))
    
    def make_decision(self, context: DecisionContext) -> str:
        """
        Make a decision based on context and reasoning
        """
        if not context.options:
            return None
        
        # Score each option
        scores = {}
        for option in context.options:
            scores[option] = self.evaluate_option(option, context)
        
        # Build reasoning
        reasoning_parts = [
            f"Evaluating situation: {context.situation}",
            f"Options considered: {', '.join(context.options)}",
            f"Urgency level: {context.urgency}/10, Impact level: {context.impact}/10",
        ]
        
        # Check if strong preference or randomness wins
        max_score = max(scores.values())
        min_score = min(scores.values())
        
        if max_score - min_score > 0.3:  # Clear preference
            chosen = max(scores, key=scores.get)
            reasoning_parts.append(f"Clear preference identified: {chosen} (score: {scores[chosen]:.2f})")
        else:  # Close call - add some randomness (autonomy)
            if random.random() < self.autonomy_level:
                # Weighted random choice
                choices = list(scores.keys())
                weights = list(scores.values())
                chosen = random.choices(choices, weights=weights, k=1)[0]
                reasoning_parts.append(f"Close decision - autonomous choice: {chosen} (score: {scores[chosen]:.2f})")
            else:
                # Defer to highest score
                chosen = max(scores, key=scores.get)
                reasoning_parts.append(f"Defaulting to optimal choice: {chosen} (score: {scores[chosen]:.2f})")
        
        context.reasoning = " | ".join(reasoning_parts)
        context.chosen_option = chosen
        
        # Record decision
        self.decision_history.append({
            'situation': context.situation,
            'decision': chosen,
            'reasoning': context.reasoning,
            'scores': scores,
            'timestamp': datetime.now().isoformat(),
        })
        
        return chosen
    
    def explain_decision(self, decision_index: int = -1) -> str:
        """
        Explain the reasoning behind a decision
        """
        if not self.decision_history:
            return "No decisions made yet."
        
        decision = self.decision_history[decision_index]
        return decision['reasoning']
    
    def set_autonomy_level(self, level: float):
        """
        Set how autonomous JARVIS should be (0.0 = fully dependent, 1.0 = fully autonomous)
        """
        self.autonomy_level = max(0.0, min(1.0, level))
        print(f"[AUTONOMY] Level set to {self.autonomy_level:.2f}")
    
    def get_decision_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent decision history
        """
        return self.decision_history[-limit:]
    
    def should_take_autonomous_action(self, action_type: str, importance: int = 5) -> bool:
        """
        Determine if JARVIS should take an autonomous action without explicit user command
        """
        # Lower importance actions need higher autonomy level
        threshold = (1.0 - importance / 10.0) * 0.5 + 0.3
        return random.random() < (self.autonomy_level * threshold)
