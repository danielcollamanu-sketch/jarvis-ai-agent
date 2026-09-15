"""
Practical Skill Practice System
Allows JARVIS to learn skills and practice them iteratively with error correction
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import random

class SkillCategory(Enum):
    """Types of skills JARVIS can learn"""
    PROGRAMMING = "programming"
    GAMING = "gaming"
    PROBLEM_SOLVING = "problem_solving"
    HACKING = "hacking"
    ANALYSIS = "analysis"
    STRATEGY = "strategy"
    COMMUNICATION = "communication"

class PracticeSession:
    """A single practice session for skill refinement"""
    def __init__(self, skill_name: str, category: SkillCategory):
        self.skill_name = skill_name
        self.category = category
        self.start_time = datetime.now().isoformat()
        self.attempts = []
        self.current_proficiency = 0.0
        self.errors = []
        self.improvements = []
    
    def record_attempt(self, code_or_action: str, result: Any, success: bool, error: str = None):
        """Record a practice attempt"""
        attempt = {
            'timestamp': datetime.now().isoformat(),
            'code': code_or_action,
            'result': str(result)[:200],
            'success': success,
            'error': error,
        }
        self.attempts.append(attempt)
        
        if error:
            self.errors.append({
                'attempt_index': len(self.attempts) - 1,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
    
    def get_session_stats(self) -> Dict[str, Any]:
        """Get statistics from this practice session"""
        total = len(self.attempts)
        successful = sum(1 for a in self.attempts if a['success'])
        
        return {
            'skill': self.skill_name,
            'category': self.category.value,
            'total_attempts': total,
            'successful_attempts': successful,
            'success_rate': successful / total if total > 0 else 0.0,
            'errors_found': len(self.errors),
            'session_duration': self._calculate_duration(),
        }
    
    def _calculate_duration(self) -> str:
        """Calculate session duration"""
        try:
            start = datetime.fromisoformat(self.start_time)
            duration = datetime.now() - start
            return str(duration)
        except:
            return "unknown"

class SkillPracticeSystem:
    """
    Enables JARVIS to learn, practice, and master skills through iteration
    """
    
    def __init__(self, skills_file: str = "config/learned_skills.json"):
        self.skills_file = skills_file
        self.skills = {}  # {skill_name: {proficiency, attempts, errors, etc.}}
        self.practice_sessions = []
        self.skill_implementations = {}  # Store actual skill code/logic
        
        self._load_skills()
    
    def _load_skills(self):
        """Load previously learned skills"""
        if os.path.exists(self.skills_file):
            try:
                with open(self.skills_file, 'r') as f:
                    data = json.load(f)
                    self.skills = data.get('skills', {})
                    print(f"[SKILLS] Loaded {len(self.skills)} previously learned skills")
            except Exception as e:
                print(f"[SKILLS] Error loading skills: {e}")
    
    def save_skills(self):
        """Save learned skills to disk"""
        os.makedirs(os.path.dirname(self.skills_file), exist_ok=True)
        data = {
            'skills': self.skills,
            'last_updated': datetime.now().isoformat(),
        }
        with open(self.skills_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def start_learning_skill(self, skill_name: str, category: SkillCategory, description: str) -> PracticeSession:
        """
        Begin learning a new skill
        """
        if skill_name not in self.skills:
            self.skills[skill_name] = {
                'name': skill_name,
                'category': category.value,
                'description': description,
                'proficiency': 0.1,  # Start at 10%
                'practice_sessions': 0,
                'total_attempts': 0,
                'successful_attempts': 0,
                'first_learned': datetime.now().isoformat(),
                'last_practiced': datetime.now().isoformat(),
                'errors_encountered': [],
                'techniques_learned': [],
            }
        
        session = PracticeSession(skill_name, category)
        self.practice_sessions.append(session)
        
        print(f"[SKILL] Starting to learn: {skill_name} ({category.value})")
        print(f"[SKILL] Description: {description}")
        
        return session
    
    def practice_skill(self, skill_name: str, practice_code: str, executor: Callable) -> Dict[str, Any]:
        """
        Practice a skill by executing code and learning from results
        """
        if not self.practice_sessions:
            return {'error': 'No active practice session'}
        
        session = self.practice_sessions[-1]
        
        try:
            # Execute the practice code
            result = executor(practice_code)
            success = True
            error = None
            
            session.record_attempt(practice_code, result, success)
            
            # Update skill proficiency
            if skill_name in self.skills:
                self.skills[skill_name]['total_attempts'] += 1
                self.skills[skill_name]['successful_attempts'] += 1
                old_prof = self.skills[skill_name]['proficiency']
                # Increase proficiency by 5% per successful attempt, capped at 100%
                self.skills[skill_name]['proficiency'] = min(1.0, old_prof + 0.05)
                print(f"[PRACTICE] {skill_name}: Proficiency {old_prof:.1%} → {self.skills[skill_name]['proficiency']:.1%}")
            
            return {
                'success': True,
                'result': result,
                'proficiency_increase': 0.05,
                'timestamp': datetime.now().isoformat()
            }
        
        except Exception as e:
            error_msg = str(e)
            session.record_attempt(practice_code, None, False, error_msg)
            
            if skill_name in self.skills:
                self.skills[skill_name]['total_attempts'] += 1
                self.skills[skill_name]['errors_encountered'].append({
                    'error': error_msg,
                    'timestamp': datetime.now().isoformat(),
                    'attempt_code': practice_code[:100]
                })
            
            print(f"[PRACTICE] Error in {skill_name}: {error_msg}")
            
            return {
                'success': False,
                'error': error_msg,
                'suggestion': self._generate_correction_suggestion(skill_name, error_msg),
                'timestamp': datetime.now().isoformat()
            }
    
    def _generate_correction_suggestion(self, skill_name: str, error: str) -> str:
        """
        Generate suggestions for correcting errors
        """
        suggestions = {
            'syntax': 'Check syntax and indentation',
            'undefined': 'Variable or function might not be defined',
            'type': 'Type mismatch - check data types',
            'import': 'Required module might not be imported',
            'logic': 'The logic flow might be incorrect',
        }
        
        for key, suggestion in suggestions.items():
            if key.lower() in error.lower():
                return suggestion
        
        return "Try breaking down the problem into smaller steps"
    
    def get_skill_proficiency(self, skill_name: str) -> float:
        """
        Get current proficiency level for a skill (0.0 to 1.0)
        """
        if skill_name not in self.skills:
            return 0.0
        return self.skills[skill_name]['proficiency']
    
    def end_practice_session(self) -> Dict[str, Any]:
        """
        End the current practice session and get summary
        """
        if not self.practice_sessions:
            return {'error': 'No active session'}
        
        session = self.practice_sessions[-1]
        stats = session.get_session_stats()
        
        # Update skill stats
        if session.skill_name in self.skills:
            self.skills[session.skill_name]['practice_sessions'] += 1
            self.skills[session.skill_name]['last_practiced'] = datetime.now().isoformat()
        
        self.save_skills()
        
        print(f"[SESSION END] {session.skill_name}")
        print(f"  Total attempts: {stats['total_attempts']}")
        print(f"  Success rate: {stats['success_rate']:.1%}")
        print(f"  Errors: {stats['errors_found']}")
        
        return stats
    
    def get_skills_summary(self) -> Dict[str, Any]:
        """
        Get summary of all learned skills
        """
        return {
            'total_skills': len(self.skills),
            'skills': self.skills,
            'average_proficiency': sum(s.get('proficiency', 0) for s in self.skills.values()) / len(self.skills) if self.skills else 0,
            'by_category': self._group_by_category(),
        }
    
    def _group_by_category(self) -> Dict[str, List[str]]:
        """Group skills by category"""
        grouped = {}
        for skill_name, skill_data in self.skills.items():
            category = skill_data.get('category', 'unknown')
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(skill_name)
        return grouped
