"""
Gestor de Sincronización de la Red Colmena
Maneja la sincronización de conocimiento entre nodos
"""

import json
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class SyncManager:
    """
    Gestiona la sincronización de estado entre nodos JARVIS
    """
    
    def __init__(self, node_id: str):
        self.node_id = node_id
        self.knowledge_sync_history = []
        self.skill_sync_history = []
        self.personality_sync_history = []
        self.sync_lock = threading.RLock()
    
    def sync_knowledge(self, local_knowledge: Dict[str, List[Dict]], 
                      remote_knowledge: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Sincroniza base de conocimiento entre nodos
        Retorna resumen de cambios realizados
        """
        with self.sync_lock:
            changes = {
                'added': [],
                'updated': [],
                'conflicts': [],
                'timestamp': datetime.now().isoformat()
            }
            
            # Procesa cada tema
            for topic, remote_facts in remote_knowledge.items():
                if topic not in local_knowledge:
                    # Nuevo tema
                    local_knowledge[topic] = remote_facts
                    changes['added'].append(topic)
                    logger.info(f"[SYNC] Nuevo tema añadido: {topic}")
                else:
                    # Tema existente - merge inteligente
                    for remote_fact in remote_facts:
                        if not self._fact_exists(local_knowledge[topic], remote_fact):
                            # Verifica confianza
                            if remote_fact.get('confidence', 0) > 0.7:
                                local_knowledge[topic].append(remote_fact)
                                changes['updated'].append(f"{topic}:{remote_fact['content'][:30]}")
                            else:
                                changes['conflicts'].append(f"{topic}:{remote_fact['content'][:30]}")
            
            self.knowledge_sync_history.append(changes)
            logger.info(f"[SYNC] Sincronización completada: {len(changes['added'])} nuevos, {len(changes['updated'])} actualizados")
            
            return changes
    
    def sync_skills(self, local_skills: Dict[str, Dict], 
                   remote_skills: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Sincroniza habilidades aprendidas
        """
        with self.sync_lock:
            changes = {
                'adopted': [],
                'improved': [],
                'timestamp': datetime.now().isoformat()
            }
            
            for skill_name, remote_skill in remote_skills.items():
                if skill_name not in local_skills:
                    # Adopta nueva habilidad
                    local_skills[skill_name] = remote_skill
                    changes['adopted'].append(skill_name)
                    logger.info(f"[SYNC] Habilidad adoptada: {skill_name}")
                else:
                    # Mejora proficiencia si la remota es mejor
                    local_prof = local_skills[skill_name].get('proficiency', 0)
                    remote_prof = remote_skill.get('proficiency', 0)
                    
                    if remote_prof > local_prof:
                        # Promedia las proficiencias
                        avg_prof = (local_prof + remote_prof) / 2
                        local_skills[skill_name]['proficiency'] = avg_prof
                        changes['improved'].append(f"{skill_name}: {local_prof:.1%} -> {avg_prof:.1%}")
            
            self.skill_sync_history.append(changes)
            logger.info(f"[SYNC] Skills sincronizadas: {len(changes['adopted'])} adoptadas, {len(changes['improved'])} mejoradas")
            
            return changes
    
    def sync_personality_traits(self, local_traits: Dict[str, float],
                               remote_traits: Dict[str, float]) -> Dict[str, Any]:
        """
        Sincroniza rasgos de personalidad
        Promedia valores para converger hacia personalidad colectiva
        """
        with self.sync_lock:
            changes = {
                'trait_updates': {},
                'timestamp': datetime.now().isoformat()
            }
            
            for trait_name in local_traits.keys():
                local_value = local_traits[trait_name]
                remote_value = remote_traits.get(trait_name, local_value)
                
                # Promedia los valores
                merged_value = (local_value + remote_value) / 2
                
                if abs(merged_value - local_value) > 0.05:  # Threshold de cambio
                    changes['trait_updates'][trait_name] = {
                        'old': local_value,
                        'new': merged_value,
                        'remote': remote_value
                    }
                    local_traits[trait_name] = merged_value
            
            self.personality_sync_history.append(changes)
            if changes['trait_updates']:
                logger.info(f"[SYNC] Personalidad sincronizada: {len(changes['trait_updates'])} rasgos actualizados")
            
            return changes
    
    @staticmethod
    def _fact_exists(facts: List[Dict], new_fact: Dict) -> bool:
        """
        Verifica si un hecho ya existe en la lista
        """
        for fact in facts:
            if fact.get('content') == new_fact.get('content'):
                return True
        return False
    
    def get_sync_status(self) -> Dict[str, Any]:
        """
        Obtiene estado de sincronizaciones
        """
        return {
            'knowledge_syncs': len(self.knowledge_sync_history),
            'skill_syncs': len(self.skill_sync_history),
            'personality_syncs': len(self.personality_sync_history),
            'last_knowledge_sync': self.knowledge_sync_history[-1] if self.knowledge_sync_history else None,
            'last_skill_sync': self.skill_sync_history[-1] if self.skill_sync_history else None,
        }
