"""
Simple implementations of various skills JARVIS can learn and practice
"""

import random
import time
from typing import Dict, Any, List

class SimpleGameSkill:
    """
    JARVIS learning game strategies
    """
    
    @staticmethod
    def play_number_guessing(target: int, attempts: int = 0, max_attempts: int = 10) -> Dict[str, Any]:
        """
        Practice number guessing with learning
        """
        if attempts == 0:
            # Random guess first time
            guess = random.randint(1, 100)
        else:
            # Improve based on feedback
            guess = random.randint(1, 100)
        
        attempts += 1
        
        if guess == target:
            return {
                'success': True,
                'guess': guess,
                'attempts': attempts,
                'message': f'Correct! Found it in {attempts} attempts'
            }
        elif attempts >= max_attempts:
            return {
                'success': False,
                'guess': guess,
                'attempts': attempts,
                'message': f'Max attempts reached. Target was {target}'
            }
        else:
            feedback = 'higher' if guess < target else 'lower'
            return {
                'success': False,
                'guess': guess,
                'attempts': attempts,
                'feedback': feedback,
                'message': f'Guess {guess} is too {feedback}'
            }

class SimpleProgrammingSkill:
    """
    JARVIS practicing programming concepts
    """
    
    @staticmethod
    def practice_fibonacci(n: int, memo: Dict = None) -> Dict[str, Any]:
        """
        Practice recursive and optimized algorithms
        """
        if memo is None:
            memo = {}
        
        if n in memo:
            return memo[n]
        
        if n <= 1:
            return n
        
        result = SimpleProgrammingSkill.practice_fibonacci(n-1, memo) + SimpleProgrammingSkill.practice_fibonacci(n-2, memo)
        memo[n] = result
        
        return result
    
    @staticmethod
    def practice_sorting(array: List[int], method: str = 'bubble') -> Dict[str, Any]:
        """
        Practice different sorting algorithms
        """
        start_time = time.time()
        
        if method == 'bubble':
            arr = array.copy()
            n = len(arr)
            for i in range(n):
                for j in range(0, n-i-1):
                    if arr[j] > arr[j+1]:
                        arr[j], arr[j+1] = arr[j+1], arr[j]
            sorted_arr = arr
        
        elif method == 'quick':
            def quick_sort(arr):
                if len(arr) <= 1:
                    return arr
                pivot = arr[0]
                less = [x for x in arr[1:] if x <= pivot]
                greater = [x for x in arr[1:] if x > pivot]
                return quick_sort(less) + [pivot] + quick_sort(greater)
            
            sorted_arr = quick_sort(array.copy())
        
        else:
            sorted_arr = sorted(array)
        
        elapsed = time.time() - start_time
        
        return {
            'success': True,
            'sorted_array': sorted_arr,
            'method': method,
            'time_taken': elapsed,
            'efficiency': 'good' if elapsed < 0.01 else 'moderate' if elapsed < 0.1 else 'poor'
        }

class SimpleStrategySkill:
    """
    JARVIS learning strategic decision making
    """
    
    @staticmethod
    def play_rock_paper_scissors(opponent_move: str, jarvis_strategy: str = 'random') -> Dict[str, Any]:
        """
        Practice strategy game with learning
        """
        moves = ['rock', 'paper', 'scissors']
        
        if jarvis_strategy == 'random':
            jarvis_move = random.choice(moves)
        elif jarvis_strategy == 'counter':
            # Learn to counter opponent's last move
            counters = {'rock': 'paper', 'paper': 'scissors', 'scissors': 'rock'}
            jarvis_move = counters.get(opponent_move, random.choice(moves))
        else:
            jarvis_move = random.choice(moves)
        
        # Determine winner
        if jarvis_move == opponent_move:
            result = 'tie'
        elif (jarvis_move == 'rock' and opponent_move == 'scissors') or \
             (jarvis_move == 'paper' and opponent_move == 'rock') or \
             (jarvis_move == 'scissors' and opponent_move == 'paper'):
            result = 'win'
        else:
            result = 'loss'
        
        return {
            'jarvis_move': jarvis_move,
            'opponent_move': opponent_move,
            'result': result,
            'strategy_used': jarvis_strategy,
        }
