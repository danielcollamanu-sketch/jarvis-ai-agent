"""
JARVIS Memory System
Persistent long-term and short-term memory management
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import os
from pathlib import Path

class MemorySystem:
    """
    Dual-layer memory system: Short-term (RAM) and Long-term (Persistent Storage)
    """
    
    def __init__(self, memory_db: str = "config/jarvis_memory.db"):
        self.memory_db = memory_db
        self.short_term_memory = []  # In-RAM cache
        self.short_term_capacity = 100
        self.context_window = 20  # Last N interactions
        
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize SQLite database for long-term memory"""
        os.makedirs(os.path.dirname(self.memory_db), exist_ok=True)
        
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        # Memory events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memory_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_type TEXT,
                content TEXT,
                timestamp DATETIME,
                importance INTEGER,
                tags TEXT,
                context TEXT
            )
        ''')
        
        # Learned facts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                topic TEXT,
                fact TEXT,
                confidence REAL,
                source TEXT,
                learned_at DATETIME,
                last_accessed DATETIME
            )
        ''')
        
        # Interaction history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_input TEXT,
                jarvis_response TEXT,
                category TEXT,
                timestamp DATETIME,
                outcome TEXT
            )
        ''')
        
        # Device state snapshots
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS device_states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state_data TEXT,
                timestamp DATETIME,
                device_id TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_event(self, event_type: str, content: str, importance: int = 5, tags: List[str] = None, context: str = None):
        """Store an event in long-term memory"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        tags_str = json.dumps(tags or [])
        
        cursor.execute('''
            INSERT INTO memory_events (event_type, content, timestamp, importance, tags, context)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (event_type, content, datetime.now().isoformat(), importance, tags_str, context))
        
        conn.commit()
        conn.close()
        
        # Also add to short-term
        self.short_term_memory.append({
            'type': event_type,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'importance': importance,
            'tags': tags or []
        })
        
        # Maintain capacity
        if len(self.short_term_memory) > self.short_term_capacity:
            self.short_term_memory.pop(0)
    
    def store_fact(self, topic: str, fact: str, confidence: float = 0.8, source: str = None):
        """Store a learned fact"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO learned_facts (topic, fact, confidence, source, learned_at, last_accessed)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (topic, fact, confidence, source, datetime.now().isoformat(), datetime.now().isoformat()))
        
        conn.commit()
        conn.close()
    
    def recall_facts(self, topic: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Recall facts about a topic"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT topic, fact, confidence, source, learned_at
            FROM learned_facts
            WHERE topic = ?
            ORDER BY confidence DESC
            LIMIT ?
        ''', (topic, limit))
        
        facts = []
        for row in cursor.fetchall():
            facts.append({
                'topic': row[0],
                'fact': row[1],
                'confidence': row[2],
                'source': row[3],
                'learned_at': row[4]
            })
        
        conn.close()
        return facts
    
    def record_interaction(self, user_input: str, response: str, category: str = "general", outcome: str = "success"):
        """Record an interaction in memory"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO interactions (user_input, jarvis_response, category, timestamp, outcome)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_input, response, category, datetime.now().isoformat(), outcome))
        
        conn.commit()
        conn.close()
        
        # Also store as event
        self.store_event(
            event_type='interaction',
            content=f"User: {user_input[:100]}",
            importance=3,
            tags=[category, outcome],
            context=response[:200]
        )
    
    def get_context_window(self, size: int = None) -> List[Dict[str, Any]]:
        """Get recent interactions for context"""
        size = size or self.context_window
        return self.short_term_memory[-size:]
    
    def store_device_state(self, state_data: Dict[str, Any], device_id: str = "primary"):
        """Snapshot current device state"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        state_json = json.dumps(state_data)
        cursor.execute('''
            INSERT INTO device_states (state_data, timestamp, device_id)
            VALUES (?, ?, ?)
        ''', (state_json, datetime.now().isoformat(), device_id))
        
        conn.commit()
        conn.close()
    
    def get_recent_events(self, hours: int = 24, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent memory events"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cutoff = datetime.now() - timedelta(hours=hours)
        
        cursor.execute('''
            SELECT event_type, content, timestamp, importance, tags
            FROM memory_events
            WHERE timestamp > ?
            ORDER BY importance DESC, timestamp DESC
            LIMIT ?
        ''', (cutoff.isoformat(), limit))
        
        events = []
        for row in cursor.fetchall():
            events.append({
                'type': row[0],
                'content': row[1],
                'timestamp': row[2],
                'importance': row[3],
                'tags': json.loads(row[4])
            })
        
        conn.close()
        return events
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory system statistics"""
        conn = sqlite3.connect(self.memory_db)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM memory_events')
        event_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM learned_facts')
        fact_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM interactions')
        interaction_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'short_term_size': len(self.short_term_memory),
            'events_stored': event_count,
            'facts_learned': fact_count,
            'interactions_recorded': interaction_count,
        }
