"""
JARVIS Autonomous Learning System
Self-directed research, knowledge acquisition, and pattern recognition
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional, Set
from collections import defaultdict
import os

class LearningSystem:
    """
    Autonomous learning engine for pattern recognition and knowledge acquisition
    """
    
    def __init__(self, knowledge_file: str = "config/knowledge_base.json"):
        self.knowledge_file = knowledge_file
        self.knowledge_base = defaultdict(list)
        self.learned_patterns = {}
        self.research_topics = set()
        self.learning_history = []
        self.confidence_scores = {}
        
        self._load_knowledge_base()
    
    def _load_knowledge_base(self):
        """Load existing knowledge base"""
        if os.path.exists(self.knowledge_file):
            try:
                with open(self.knowledge_file, 'r') as f:
                    data = json.load(f)
                    self.knowledge_base.update(data.get('knowledge', {}))
                    self.learned_patterns = data.get('patterns', {})
                    self.research_topics = set(data.get('research_topics', []))
            except Exception as e:
                print(f"Could not load knowledge base: {e}")
    
    def save_knowledge_base(self):
        """Save knowledge base to disk"""
        os.makedirs(os.path.dirname(self.knowledge_file), exist_ok=True)
        data = {
            'knowledge': dict(self.knowledge_base),
            'patterns': self.learned_patterns,
            'research_topics': list(self.research_topics),
            'last_updated': datetime.now().isoformat(),
        }
        with open(self.knowledge_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def learn(self, subject: str, knowledge: str, confidence: float = 0.7, source: str = "observation"):
        """Learn a new piece of knowledge"""
        knowledge_entry = {
            'content': knowledge,
            'confidence': confidence,
            'source': source,
            'learned_at': datetime.now().isoformat(),
            'reinforced_count': 0
        }
        
        self.knowledge_base[subject].append(knowledge_entry)
        self.confidence_scores[f"{subject}_{len(self.knowledge_base[subject])-1}"] = confidence
        
        self.learning_history.append({
            'subject': subject,
            'knowledge': knowledge,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        })
        
        print(f"[LEARNING] Learned about {subject}: {knowledge[:60]}...")
    
    def reinforce_knowledge(self, subject: str, index: int = 0):
        """Reinforce existing knowledge through repetition"""
        if subject in self.knowledge_base and index < len(self.knowledge_base[subject]):
            knowledge = self.knowledge_base[subject][index]
            # Increase confidence through reinforcement
            old_confidence = knowledge['confidence']
            knowledge['confidence'] = min(1.0, knowledge['confidence'] + 0.05)
            knowledge['reinforced_count'] += 1
            print(f"[REINFORCED] {subject}: confidence {old_confidence:.2f} → {knowledge['confidence']:.2f}")
    
    def recognize_pattern(self, inputs: List[str]) -> Optional[str]:
        """Identify patterns in data"""
        pattern_key = "_".join(sorted(set(inputs)))
        
        if pattern_key in self.learned_patterns:
            pattern = self.learned_patterns[pattern_key]
            pattern['occurrences'] = pattern.get('occurrences', 0) + 1
            return pattern['description']
        
        return None
    
    def register_pattern(self, inputs: List[str], description: str, importance: int = 5):
        """Register a new pattern"""
        pattern_key = "_".join(sorted(set(inputs)))
        
        self.learned_patterns[pattern_key] = {
            'description': description,
            'inputs': inputs,
            'importance': importance,
            'occurrences': 0,
            'discovered_at': datetime.now().isoformat(),
        }
        
        print(f"[PATTERN] Registered: {description}")
    
    def set_research_interest(self, topic: str, priority: int = 5):
        """Set a topic for autonomous research"""
        self.research_topics.add(topic)
        print(f"[RESEARCH] Added interest: {topic} (priority: {priority})")
    
    def get_research_agenda(self) -> List[str]:
        """Get topics for autonomous investigation"""
        return list(self.research_topics)
    
    def analyze_trends(self, subject: str) -> Dict[str, Any]:
        """Analyze trends in learned knowledge"""
        if subject not in self.knowledge_base:
            return {}
        
        knowledge_items = self.knowledge_base[subject]
        avg_confidence = sum(k['confidence'] for k in knowledge_items) / len(knowledge_items) if knowledge_items else 0
        
        return {
            'subject': subject,
            'total_learned': len(knowledge_items),
            'average_confidence': avg_confidence,
            'most_recent': knowledge_items[-1]['learned_at'] if knowledge_items else None,
            'sources': list(set(k['source'] for k in knowledge_items)),
        }
    
    def get_expertise_level(self, subject: str) -> float:
        """Get expertise level on a subject (0.0 to 1.0)"""
        if subject not in self.knowledge_base:
            return 0.0
        
        items = self.knowledge_base[subject]
        if not items:
            return 0.0
        
        # Average confidence weighted by reinforcement
        total_score = sum(
            k['confidence'] * (1 + k['reinforced_count'] * 0.1)
            for k in items
        )
        return min(1.0, total_score / len(items))
    
    def get_knowledge_summary(self) -> Dict[str, Any]:
        """Get summary of all learned knowledge"""
        subjects = list(self.knowledge_base.keys())
        expertise_levels = {s: self.get_expertise_level(s) for s in subjects}
        
        return {
            'subjects_known': len(subjects),
            'total_facts_learned': sum(len(v) for v in self.knowledge_base.values()),
            'patterns_recognized': len(self.learned_patterns),
            'research_interests': len(self.research_topics),
            'top_expertise': sorted(expertise_levels.items(), key=lambda x: x[1], reverse=True)[:5],
        }
