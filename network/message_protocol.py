"""
Protocolo de Mensajes de la Red Colmena
Define los tipos y estructura de mensajes entre nodos JARVIS
"""

import json
import uuid
from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

class MessageType(Enum):
    """Tipos de mensajes en la red colmena"""
    # Discovery
    HEARTBEAT = "heartbeat"              # Señal de vida periódica
    ANNOUNCE = "announce"                # Anuncio de disponibilidad
    
    # Knowledge Sharing
    KNOWLEDGE_SHARE = "knowledge_share"  # Compartir conocimiento
    SKILL_SHARE = "skill_share"          # Compartir habilidades aprendidas
    PERSONALITY_SYNC = "personality_sync" # Sincronizar personalidad
    
    # Task Delegation
    TASK_REQUEST = "task_request"        # Solicitud de tarea
    TASK_RESPONSE = "task_response"      # Respuesta de tarea
    TASK_RESULT = "task_result"          # Resultado de tarea
    
    # Consensus
    VOTE_REQUEST = "vote_request"        # Solicitar voto para decisión
    VOTE_RESPONSE = "vote_response"      # Respuesta de voto
    
    # Health
    STATUS_QUERY = "status_query"        # Consultar estado
    STATUS_RESPONSE = "status_response"  # Respuesta de estado

class HiveMessage:
    """
    Estructura de mensaje en la red colmena
    """
    
    def __init__(self, 
                 msg_type: MessageType,
                 sender_id: str,
                 payload: Dict[str, Any],
                 target_id: Optional[str] = None,
                 conversation_id: Optional[str] = None):
        
        self.id = str(uuid.uuid4())
        self.type = msg_type
        self.sender_id = sender_id
        self.target_id = target_id  # None = broadcast
        self.payload = payload
        self.conversation_id = conversation_id or str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        self.priority = payload.get('priority', 5)  # 1-10
        self.ttl = payload.get('ttl', 3)  # Time To Live (hops)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte mensaje a diccionario"""
        return {
            'id': self.id,
            'type': self.type.value,
            'sender_id': self.sender_id,
            'target_id': self.target_id,
            'payload': self.payload,
            'conversation_id': self.conversation_id,
            'timestamp': self.timestamp,
            'priority': self.priority,
            'ttl': self.ttl,
        }
    
    def to_json(self) -> str:
        """Convierte mensaje a JSON"""
        return json.dumps(self.to_dict())
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> 'HiveMessage':
        """Crea mensaje desde diccionario"""
        msg_type = MessageType(data['type'])
        msg = HiveMessage(
            msg_type=msg_type,
            sender_id=data['sender_id'],
            payload=data['payload'],
            target_id=data.get('target_id'),
            conversation_id=data.get('conversation_id')
        )
        msg.id = data['id']
        msg.timestamp = data['timestamp']
        msg.ttl = data.get('ttl', 3)
        return msg
    
    def __str__(self) -> str:
        return f"HiveMessage({self.type.value} from {self.sender_id[:8]}...)"
