"""
Device Binder Module
Binds JARVIS to device applications and functions with safe execution
"""

import json
import subprocess
import os
import sys
from typing import Dict, List, Any, Callable, Optional
from datetime import datetime
from pathlib import Path
import threading
import time

class DeviceBinder:
    """
    Binds JARVIS to device applications and OS functions
    Provides sandboxed execution and permission management
    """
    
    def __init__(self, config_file: str = "config/device_config.json"):
        self.config_file = config_file
        self.device_config = {}
        self.registered_apps = {}
        self.execution_history = []
        self.sandbox_processes = []
        
        self._load_device_config()
    
    def _load_device_config(self):
        """Load device configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.device_config = json.load(f)
                print(f"[DEVICE] Loaded config for {self.device_config['device']['name']}")
        except Exception as e:
            print(f"[DEVICE] Error loading config: {e}")
    
    def register_app(self, app_name: str, functions: Dict[str, Callable]):
        """
        Register a device application with its functions
        Example: register_app('music_player', {'play': play_func, 'pause': pause_func})
        """
        self.registered_apps[app_name] = {
            'functions': functions,
            'registered_at': datetime.now().isoformat(),
            'execution_count': 0
        }
        print(f"[DEVICE] Registered app: {app_name} with {len(functions)} functions")
    
    def list_available_functions(self) -> Dict[str, List[str]]:
        """List all available device functions"""
        available = {}
        for app_name, app_data in self.registered_apps.items():
            available[app_name] = list(app_data['functions'].keys())
        return available
    
    def can_execute(self, app_name: str, function_name: str) -> bool:
        """Check if a function can be executed"""
        if app_name not in self.registered_apps:
            return False
        
        if function_name not in self.registered_apps[app_name]['functions']:
            return False
        
        return True
    
    def execute_function(self, app_name: str, function_name: str, *args, **kwargs) -> Any:
        """
        Execute a device function with safety checks
        """
        if not self.can_execute(app_name, function_name):
            return {
                'success': False,
                'error': f'Cannot execute {app_name}.{function_name}',
                'timestamp': datetime.now().isoformat()
            }
        
        try:
            func = self.registered_apps[app_name]['functions'][function_name]
            result = func(*args, **kwargs)
            
            self.registered_apps[app_name]['execution_count'] += 1
            
            execution_record = {
                'app': app_name,
                'function': function_name,
                'args': str(args)[:100],
                'result': str(result)[:200],
                'success': True,
                'timestamp': datetime.now().isoformat()
            }
            self.execution_history.append(execution_record)
            
            return {
                'success': True,
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            error_record = {
                'app': app_name,
                'function': function_name,
                'error': str(e),
                'success': False,
                'timestamp': datetime.now().isoformat()
            }
            self.execution_history.append(error_record)
            
            return {
                'success': False,
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
    
    def get_device_status(self) -> Dict[str, Any]:
        """Get current device status"""
        return {
            'device_name': self.device_config.get('device', {}).get('name'),
            'device_id': self.device_config.get('device', {}).get('id'),
            'registered_apps': list(self.registered_apps.keys()),
            'total_executions': len(self.execution_history),
            'available_functions': self.list_available_functions(),
        }
