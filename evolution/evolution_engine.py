"""
JARVIS Code Evolution System
Allows JARVIS to analyze, modify, and improve its own code
"""

import os
import json
import shutil
import hashlib
from datetime import datetime
from typing import Dict, List, Any, Optional
import ast
import inspect

class CodeAnalyzer:
    """
    Analyzes JARVIS code for optimization opportunities
    """
    
    def __init__(self):
        self.analysis_history = []
    
    def analyze_code(self, code: str) -> Dict[str, Any]:
        """
        Analyze code for issues and improvement opportunities
        """
        analysis = {
            'timestamp': datetime.now().isoformat(),
            'code_hash': hashlib.md5(code.encode()).hexdigest(),
            'issues': [],
            'suggestions': [],
            'complexity': 'unknown',
        }
        
        # Check for common issues
        lines = code.split('\n')
        
        # Check for unused variables
        if 'unused' in code.lower():
            analysis['issues'].append('Potentially unused variables detected')
            analysis['suggestions'].append('Review variable assignments')
        
        # Check for performance issues
        if 'for ' in code and ' for ' in code:  # Nested loops
            analysis['issues'].append('Possible nested loops detected')
            analysis['suggestions'].append('Consider using list comprehensions or vectorization')
        
        # Check for error handling
        if 'try:' not in code:
            analysis['suggestions'].append('Consider adding error handling')
        
        # Basic complexity estimate
        complexity_score = len(lines) + code.count('def ') * 2 + code.count('class ') * 5
        if complexity_score < 50:
            analysis['complexity'] = 'low'
        elif complexity_score < 200:
            analysis['complexity'] = 'medium'
        else:
            analysis['complexity'] = 'high'
        
        self.analysis_history.append(analysis)
        return analysis

class CodeModifier:
    """
    Safely modifies JARVIS code with version control
    """
    
    def __init__(self, backup_dir: str = "evolution/backups"):
        self.backup_dir = backup_dir
        self.modification_history = []
        os.makedirs(backup_dir, exist_ok=True)
    
    def backup_code(self, file_path: str, code_content: str) -> str:
        """
        Create a backup of code before modification
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.basename(file_path)
        backup_path = os.path.join(self.backup_dir, f"{timestamp}_{filename}")
        
        with open(backup_path, 'w') as f:
            f.write(code_content)
        
        print(f"[BACKUP] Code backed up to {backup_path}")
        return backup_path
    
    def suggest_modification(self, code: str, improvement_type: str) -> Dict[str, Any]:
        """
        Suggest a code modification
        """
        suggestion = {
            'timestamp': datetime.now().isoformat(),
            'improvement_type': improvement_type,
            'original_code': code[:500],
            'suggested_modification': None,
            'reason': None,
            'safety_score': 0.5,
        }
        
        if improvement_type == 'performance':
            suggestion['reason'] = 'Code can be optimized for better performance'
            suggestion['suggested_modification'] = 'Use list comprehensions instead of loops'
            suggestion['safety_score'] = 0.8
        
        elif improvement_type == 'reliability':
            suggestion['reason'] = 'Add error handling for robustness'
            suggestion['suggested_modification'] = 'Wrap critical sections in try-except'
            suggestion['safety_score'] = 0.9
        
        elif improvement_type == 'readability':
            suggestion['reason'] = 'Improve code clarity and documentation'
            suggestion['suggested_modification'] = 'Add more descriptive variable names'
            suggestion['safety_score'] = 0.95
        
        return suggestion
    
    def apply_modification(self, file_path: str, modification: Dict[str, Any], safety_threshold: float = 0.7) -> bool:
        """
        Apply a code modification if it passes safety checks
        """
        if modification['safety_score'] < safety_threshold:
            print(f"[EVOLUTION] Modification rejected - safety score {modification['safety_score']:.2f} below threshold")
            return False
        
        try:
            with open(file_path, 'r') as f:
                original_content = f.read()
            
            # Backup before modification
            self.backup_code(file_path, original_content)
            
            # Apply modification (simplified - in reality would be more sophisticated)
            modified_content = original_content
            # Actual modification logic would go here
            
            with open(file_path, 'w') as f:
                f.write(modified_content)
            
            self.modification_history.append({
                'file': file_path,
                'timestamp': datetime.now().isoformat(),
                'modification_type': modification['improvement_type'],
                'success': True,
            })
            
            print(f"[EVOLUTION] Successfully applied {modification['improvement_type']} modification")
            return True
        
        except Exception as e:
            print(f"[EVOLUTION] Modification failed: {e}")
            return False

class EvolutionEngine:
    """
    Main system for JARVIS self-improvement and code evolution
    """
    
    def __init__(self):
        self.analyzer = CodeAnalyzer()
        self.modifier = CodeModifier()
        self.evolution_log = []
        self.evolution_goals = []
    
    def set_evolution_goal(self, goal: str, priority: int = 5):
        """
        Set a goal for self-improvement
        """
        self.evolution_goals.append({
            'goal': goal,
            'priority': priority,
            'set_at': datetime.now().isoformat(),
            'completed': False,
        })
        print(f"[EVOLUTION] Goal set: {goal} (priority: {priority})")
    
    def analyze_and_suggest_improvements(self, code_file: str) -> List[Dict[str, Any]]:
        """
        Analyze code and suggest improvements
        """
        try:
            with open(code_file, 'r') as f:
                code_content = f.read()
            
            # Analyze
            analysis = self.analyzer.analyze_code(code_content)
            
            # Generate suggestions
            suggestions = []
            for issue in analysis['issues']:
                suggestion = self.modifier.suggest_modification(
                    code_content,
                    'performance' if 'performance' in issue.lower() else 'reliability'
                )
                suggestions.append(suggestion)
            
            return suggestions
        
        except Exception as e:
            print(f"[EVOLUTION] Error analyzing code: {e}")
            return []
    
    def attempt_self_improvement(self, code_file: str, max_attempts: int = 3) -> Dict[str, Any]:
        """
        Attempt to improve code through iteration
        """
        print(f"[EVOLUTION] Beginning self-improvement cycle for {code_file}")
        
        improvements = {
            'file': code_file,
            'timestamp': datetime.now().isoformat(),
            'attempts': 0,
            'successful_modifications': 0,
            'failed_modifications': 0,
            'details': []
        }
        
        suggestions = self.analyze_and_suggest_improvements(code_file)
        
        for i, suggestion in enumerate(suggestions[:max_attempts]):
            improvements['attempts'] += 1
            success = self.modifier.apply_modification(code_file, suggestion)
            
            if success:
                improvements['successful_modifications'] += 1
                improvements['details'].append({
                    'attempt': i + 1,
                    'type': suggestion['improvement_type'],
                    'result': 'success'
                })
            else:
                improvements['failed_modifications'] += 1
                improvements['details'].append({
                    'attempt': i + 1,
                    'type': suggestion['improvement_type'],
                    'result': 'failed'
                })
        
        self.evolution_log.append(improvements)
        print(f"[EVOLUTION] Self-improvement cycle complete: {improvements['successful_modifications']}/{improvements['attempts']} modifications successful")
        
        return improvements
    
    def get_evolution_status(self) -> Dict[str, Any]:
        """
        Get current evolution status
        """
        return {
            'evolution_goals': len(self.evolution_goals),
            'completed_goals': sum(1 for g in self.evolution_goals if g['completed']),
            'total_evolutions': len(self.evolution_log),
            'successful_modifications': sum(
                e['successful_modifications'] for e in self.evolution_log
            ),
            'evolution_log': self.evolution_log[-5:],  # Last 5 evolutions
        }
