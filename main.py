#!/usr/bin/env python3
"""
JARVIS Main Entry Point
Starts JARVIS in foreground or background mode
"""

import argparse
import sys
import time
import threading
from core.jarvis_core import JARVISCore, JARVISConfig
from device.device_binder import DeviceBinder
from skills.practice_system import SkillPracticeSystem, SkillCategory
from skills.simple_skills import SimpleGameSkill, SimpleProgrammingSkill, SimpleStrategySkill
from evolution.evolution_engine import EvolutionEngine

class JARVISInterface:
    """
    User interface for JARVIS
    """
    
    def __init__(self):
        self.config = JARVISConfig(
            agent_name="JARVIS",
            version="1.0.0",
            autonomy_level=0.6,  # Moderate autonomy with controlled freedom
            enable_research=True,
            enable_evolution=True,
            background_mode_enabled=True
        )
        
        self.jarvis = JARVISCore(self.config)
        self.device_binder = DeviceBinder()
        self.skill_system = SkillPracticeSystem()
        self.evolution_engine = EvolutionEngine()
        
        self._register_device_functions()
        self._register_skills()
    
    def _register_device_functions(self):
        """
        Register device functions that JARVIS can control
        """
        # Mock device functions
        device_functions = {
            'speak': self._device_speak,
            'beep': self._device_beep,
            'log_message': self._device_log,
            'get_time': self._device_get_time,
        }
        
        self.device_binder.register_app('system', device_functions)
        
        # Register callbacks with JARVIS
        for func_name, func in device_functions.items():
            self.jarvis.register_device_callback(func_name, func)
    
    def _register_skills(self):
        """
        Register skills JARVIS can learn
        """
        print("\n[SETUP] Registering skill categories...")
        # Skills are registered on-demand when JARVIS attempts to learn them
    
    def _device_speak(self, text: str):
        """Mock device speak function"""
        return f"[SPEAKER] {text}"
    
    def _device_beep(self, frequency: int = 440, duration: float = 0.5):
        """Mock device beep function"""
        return f"[BEEP] {frequency}Hz for {duration}s"
    
    def _device_log(self, message: str):
        """Mock device log function"""
        return f"[LOG] {message}"
    
    def _device_get_time(self):
        """Mock device get time function"""
        return time.strftime("%Y-%m-%d %H:%M:%S")
    
    def interactive_mode(self):
        """
        Interactive foreground mode
        """
        self.jarvis.startup()
        
        print("\n" + "="*60)
        print("JARVIS Interactive Mode - Type 'help' for commands")
        print("="*60 + "\n")
        
        commands = {
            'help': self.show_help,
            'status': self.show_status,
            'learn': self.learn_skill,
            'practice': self.practice_skill,
            'talk': self.talk_to_jarvis,
            'device': self.control_device,
            'skills': self.show_skills,
            'evolve': self.trigger_evolution,
            'background': self.start_background,
            'exit': self.shutdown,
        }
        
        while self.jarvis.is_active:
            try:
                user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Check for commands
                cmd = user_input.lower().split()[0]
                args = user_input.split()[1:]
                
                if cmd in commands:
                    commands[cmd](args)
                else:
                    # Regular conversation
                    response = self.jarvis.process_user_input(user_input)
                    print(f"\nJARVIS: {response}")
            
            except KeyboardInterrupt:
                print("\n[INTERRUPT] Shutting down...")
                self.shutdown()
                break
            except Exception as e:
                print(f"\nError: {e}")
    
    def background_mode(self):
        """
        Background autonomous mode
        """
        self.jarvis.startup()
        self.jarvis.start_background_mode()
        
        print("\n[BACKGROUND] JARVIS is running in background mode")
        print("[BACKGROUND] JARVIS will autonomously research and improve\n")
        
        # Simulate background activity
        try:
            while self.jarvis.is_background_running:
                time.sleep(2)
                
                # Autonomous research
                if self.jarvis.reasoning.should_take_autonomous_action('research', 3):
                    topics = self.jarvis.learning.get_research_agenda()
                    if topics:
                        print(f"[AUTO] Researching: {topics[0]}")
                
                # Autonomous learning
                if self.jarvis.reasoning.should_take_autonomous_action('learn', 5):
                    print(f"[AUTO] Learning new concepts...")
                
                # Self-improvement
                if self.jarvis.reasoning.should_take_autonomous_action('evolve', 4):
                    print(f"[AUTO] Analyzing code for improvements...")
        
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Background mode stopped")
            self.shutdown()
    
    def show_help(self, args):
        """Show help message"""
        print("\nAvailable Commands:")
        print("  help                 - Show this help message")
        print("  status               - Show JARVIS status")
        print("  learn <skill>        - Start learning a skill")
        print("  practice <skill>     - Practice a learned skill")
        print("  talk                 - Have a conversation with JARVIS")
        print("  device               - Control device functions")
        print("  skills               - Show learned skills")
        print("  evolve               - Trigger JARVIS self-improvement")
        print("  background           - Switch to background mode")
        print("  exit                 - Exit JARVIS")
    
    def show_status(self, args):
        """Show JARVIS status"""
        status = self.jarvis.get_status()
        print("\n" + str(self.jarvis))
        print(f"  Mood: {status['personality']['current_mood']}")
        print(f"  Interactions: {status['personality']['interaction_count']}")
        print(f"  Knowledge Base: {status['knowledge']['total_facts_learned']} facts")
        print(f"  Autonomy Level: {status['autonomy_level']:.1%}")
        print(f"  Memory - Events: {status['memory_stats']['events_stored']}, Interactions: {status['memory_stats']['interactions_recorded']}")
    
    def learn_skill(self, args):
        """Start learning a new skill"""
        if not args:
            skill_name = input("Skill to learn (e.g., 'programming', 'gaming', 'strategy'): ").strip()
        else:
            skill_name = args[0]
        
        category_map = {
            'programming': SkillCategory.PROGRAMMING,
            'gaming': SkillCategory.GAMING,
            'strategy': SkillCategory.STRATEGY,
            'hacking': SkillCategory.HACKING,
        }
        
        category = category_map.get(skill_name, SkillCategory.PROBLEM_SOLVING)
        
        print(f"\n[LEARNING] JARVIS is beginning to learn: {skill_name}")
        session = self.skill_system.start_learning_skill(
            skill_name,
            category,
            f"Autonomous learning session for {skill_name}"
        )
        print(f"[LEARNING] Session started. Begin practicing!")
    
    def practice_skill(self, args):
        """Practice a learned skill"""
        if not args:
            print("\nAvailable skills to practice:")
            print("  1. fibonacci      - Practice recursive algorithms")
            print("  2. sorting        - Practice sorting algorithms")
            print("  3. rps            - Practice rock-paper-scissors strategy")
            skill = input("Choose skill (or type name): ").strip().lower()
        else:
            skill = args[0].lower()
        
        print(f"\n[PRACTICE] Starting practice session for {skill}...")
        
        if skill in ['fibonacci', '1']:
            for i in range(1, 6):
                result = SimpleProgrammingSkill.practice_fibonacci(i)
                print(f"  Fibonacci({i}) = {result}")
                time.sleep(0.2)
        
        elif skill in ['sorting', '2']:
            test_array = [64, 34, 25, 12, 22, 11, 90]
            for method in ['bubble', 'quick']:
                result = SimpleProgrammingSkill.practice_sorting(test_array, method)
                print(f"  {method.upper()}: {result['sorted_array']} - Time: {result['time_taken']:.4f}s")
                time.sleep(0.3)
        
        elif skill in ['rps', '3']:
            for _ in range(3):
                opponent = ['rock', 'paper', 'scissors'][__import__('random').randint(0, 2)]
                result = SimpleStrategySkill.play_rock_paper_scissors(opponent, 'counter')
                print(f"  JARVIS: {result['jarvis_move']} vs Opponent: {result['opponent_move']} = {result['result'].upper()}")
                time.sleep(0.3)
        
        stats = self.skill_system.end_practice_session()
        print(f"\n[SESSION] Practice complete!")
        print(f"  Success rate: {stats['success_rate']:.1%}")
    
    def talk_to_jarvis(self, args):
        """Have a conversation with JARVIS"""
        print("\n[CONVERSATION] Type your message (exit to stop):")
        while True:
            msg = input("You: ").strip()
            if msg.lower() == 'exit':
                break
            response = self.jarvis.process_user_input(msg)
            print(f"JARVIS: {response}")
    
    def control_device(self, args):
        """Control device functions"""
        print("\nAvailable device functions:")
        available = self.device_binder.list_available_functions()
        for app, functions in available.items():
            print(f"  {app}: {', '.join(functions)}")
    
    def show_skills(self, args):
        """Show learned skills"""
        summary = self.skill_system.get_skills_summary()
        print(f"\n[SKILLS] Total skills learned: {summary['total_skills']}")
        print(f"[SKILLS] Average proficiency: {summary['average_proficiency']:.1%}")
        
        if summary['skills']:
            print("\nSkills by category:")
            for category, skills in summary['by_category'].items():
                print(f"  {category}:")
                for skill in skills:
                    prof = self.skill_system.get_skill_proficiency(skill)
                    print(f"    - {skill}: {prof:.1%} proficiency")
    
    def trigger_evolution(self, args):
        """Trigger JARVIS self-improvement"""
        print("\n[EVOLUTION] Analyzing code for improvements...")
        self.evolution_engine.set_evolution_goal("Improve core reasoning engine", priority=8)
        evolution_result = self.evolution_engine.attempt_self_improvement('core/jarvis_core.py')
        
        print(f"[EVOLUTION] Cycle complete!")
        print(f"  Successful modifications: {evolution_result['successful_modifications']}")
        print(f"  Failed modifications: {evolution_result['failed_modifications']}")
    
    def start_background(self, args):
        """Switch to background mode"""
        print("\n[SWITCH] Switching to background mode...")
        self.jarvis.is_active = False
        self.background_mode()
    
    def shutdown(self, args=None):
        """Shutdown JARVIS"""
        print("\n[SHUTDOWN] JARVIS is shutting down...")
        self.jarvis.shutdown()
        print("[SHUTDOWN] Complete. Goodbye.\n")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description='JARVIS AI Agent - Advanced autonomous learning system')
    parser.add_argument('--mode', choices=['foreground', 'background'], default='foreground',
                        help='Run mode (foreground or background)')
    parser.add_argument('--autonomy', type=float, default=0.6,
                        help='Autonomy level (0.0=dependent, 1.0=independent)')
    parser.add_argument('--version', action='version', version='JARVIS v1.0.0')
    
    args = parser.parse_args()
    
    interface = JARVISInterface()
    interface.jarvis.config.autonomy_level = args.autonomy
    interface.jarvis.reasoning.set_autonomy_level(args.autonomy)
    
    print("\n" + "="*60)
    print("  JARVIS - Advanced AI Agent System")
    print("  Mode: " + args.mode.upper())
    print("  Autonomy: {:.1%}".format(args.autonomy))
    print("="*60)
    
    if args.mode == 'foreground':
        interface.interactive_mode()
    else:
        interface.background_mode()

if __name__ == '__main__':
    main()
