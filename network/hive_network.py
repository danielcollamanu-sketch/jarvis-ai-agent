"""
Red Colmena (Hive Network)
Protocolo P2P para múltiples instancias de JARVIS
Descubrimiento automático, compartir conocimiento y delegación de tareas
"""

import json
import socket
import threading
import uuid
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timedelta
from collections import deque
import logging

from .message_protocol import HiveMessage, MessageType
from .discovery import DiscoveryService, PeerInfo
from .sync_manager import SyncManager

logger = logging.getLogger(__name__)

class HiveNode:
    """
    Representa un nodo JARVIS en la red colmena
    """
    
    def __init__(self, node_id: str = None, hostname: str = "localhost", port: int = 9999):
        self.node_id = node_id or f"jarvis_{str(uuid.uuid4())[:8]}"
        self.hostname = hostname
        self.port = port
        self.version = "1.0.0"
        self.capabilities = ["learning", "research", "task_execution", "evolution"]
        self.started_at = datetime.now().isoformat()
        
        # Estado del nodo
        self.status = "initializing"
        self.cpu_load = 0.0
        self.memory_usage = 0.0
        self.active_tasks = []
        
        logger.info(f"[HIVE] Nodo creado: {self.node_id}")
    
    def get_info(self) -> Dict[str, Any]:
        """Obtiene información del nodo"""
        return {
            'node_id': self.node_id,
            'hostname': self.hostname,
            'port': self.port,
            'version': self.version,
            'status': self.status,
            'capabilities': self.capabilities,
            'started_at': self.started_at,
            'cpu_load': self.cpu_load,
            'memory_usage': self.memory_usage,
            'active_tasks': len(self.active_tasks),
        }

class HiveNetwork:
    """
    Red Colmena - Protocolo P2P para colaboración entre nodos JARVIS
    """
    
    def __init__(self, local_jarvis_core):
        self.local_jarvis = local_jarvis_core
        self.node = HiveNode(
            hostname=socket.gethostname(),
            port=9999
        )
        
        # Servicios de red
        self.discovery_service = DiscoveryService(
            node_id=self.node.node_id,
            hostname=self.node.hostname,
            port=self.node.port,
            capabilities=self.node.capabilities
        )
        
        self.sync_manager = SyncManager(self.node.node_id)
        
        # Estado de la red
        self.peers: Dict[str, PeerInfo] = {}
        self.message_queue: deque = deque(maxlen=1000)
        self.message_handlers: Dict[MessageType, Callable] = {}
        self.is_running = False
        
        # Estadísticas
        self.stats = {
            'messages_sent': 0,
            'messages_received': 0,
            'knowledge_syncs': 0,
            'task_delegations': 0,
        }
        
        self._register_message_handlers()
        logger.info(f"[HIVE] Red Colmena inicializada para {self.node.node_id}")
    
    def _register_message_handlers(self):
        """
        Registra handlers para diferentes tipos de mensajes
        """
        self.message_handlers = {
            MessageType.HEARTBEAT: self._handle_heartbeat,
            MessageType.ANNOUNCE: self._handle_announce,
            MessageType.KNOWLEDGE_SHARE: self._handle_knowledge_share,
            MessageType.SKILL_SHARE: self._handle_skill_share,
            MessageType.TASK_REQUEST: self._handle_task_request,
            MessageType.TASK_RESULT: self._handle_task_result,
            MessageType.STATUS_QUERY: self._handle_status_query,
        }
    
    def start(self):
        """
        Inicia la red colmena
        """
        self.is_running = True
        self.node.status = "online"
        
        # Inicia descubrimiento
        self.discovery_service.register_callback(self._on_peer_discovered)
        self.discovery_service.start_discovery()
        self.discovery_service.announce_self()
        
        # Inicia threads de procesamiento
        message_thread = threading.Thread(target=self._message_processing_loop, daemon=True)
        heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        sync_thread = threading.Thread(target=self._sync_loop, daemon=True)
        
        message_thread.start()
        heartbeat_thread.start()
        sync_thread.start()
        
        logger.info(f"[HIVE] Red Colmena iniciada para {self.node.node_id}")
    
    def stop(self):
        """
        Detiene la red colmena
        """
        self.is_running = False
        self.node.status = "offline"
        self.discovery_service.stop_discovery()
        logger.info(f"[HIVE] Red Colmena detenida para {self.node.node_id}")
    
    def broadcast_message(self, msg_type: MessageType, payload: Dict[str, Any]):
        """
        Envía un mensaje a todos los nodos en la red (broadcast)
        """
        message = HiveMessage(
            msg_type=msg_type,
            sender_id=self.node.node_id,
            payload=payload,
            target_id=None  # None = broadcast
        )
        
        self.message_queue.append(message)
        self.stats['messages_sent'] += 1
        logger.debug(f"[HIVE] Mensaje broadcast: {msg_type.value}")
    
    def send_message(self, target_id: str, msg_type: MessageType, payload: Dict[str, Any]):
        """
        Envía un mensaje a un nodo específico
        """
        message = HiveMessage(
            msg_type=msg_type,
            sender_id=self.node.node_id,
            payload=payload,
            target_id=target_id
        )
        
        self.message_queue.append(message)
        self.stats['messages_sent'] += 1
        logger.debug(f"[HIVE] Mensaje enviado a {target_id}: {msg_type.value}")
    
    def _on_peer_discovered(self, peer_info: PeerInfo):
        """
        Callback cuando se descubre un nuevo nodo
        """
        self.peers[peer_info.peer_id] = peer_info
        logger.info(f"[HIVE] Nodo descubierto en la red: {peer_info.peer_id}")
        
        # Envía saludo
        self.send_message(peer_info.peer_id, MessageType.ANNOUNCE, {
            'node_info': self.node.get_info()
        })
    
    def _message_processing_loop(self):
        """
        Loop principal de procesamiento de mensajes
        """
        while self.is_running:
            try:
                if self.message_queue:
                    message = self.message_queue.popleft()
                    
                    # Verifica si el mensaje es para este nodo
                    if message.target_id is None or message.target_id == self.node.node_id:
                        self._process_message(message)
                    else:
                        # Reenvía el mensaje si TTL > 0
                        if message.ttl > 0:
                            message.ttl -= 1
                            self.message_queue.append(message)
                
                threading.Event().wait(0.1)
            except Exception as e:
                logger.error(f"[HIVE] Error en loop de mensajes: {e}")
    
    def _process_message(self, message: HiveMessage):
        """
        Procesa un mensaje recibido
        """
        self.stats['messages_received'] += 1
        
        handler = self.message_handlers.get(message.type)
        if handler:
            try:
                handler(message)
            except Exception as e:
                logger.error(f"[HIVE] Error procesando {message.type.value}: {e}")
        else:
            logger.warning(f"[HIVE] No hay handler para {message.type.value}")
    
    def _heartbeat_loop(self):
        """
        Envía heartbeat periódicamente para mantener la red activa
        """
        while self.is_running:
            try:
                self.broadcast_message(MessageType.HEARTBEAT, {
                    'node_id': self.node.node_id,
                    'status': self.node.status,
                    'timestamp': datetime.now().isoformat(),
                })
                threading.Event().wait(5)  # Heartbeat cada 5 segundos
            except Exception as e:
                logger.error(f"[HIVE] Error en heartbeat: {e}")
    
    def _sync_loop(self):
        """
        Sincroniza conocimiento y habilidades periódicamente
        """
        while self.is_running:
            try:
                if self.peers:
                    # Selecciona un nodo aleatorio para sincronizar
                    import random
                    peer_id = random.choice(list(self.peers.keys()))
                    
                    self.send_message(peer_id, MessageType.KNOWLEDGE_SHARE, {
                        'knowledge': dict(self.local_jarvis.learning.knowledge_base),
                        'priority': 5,
                    })
                    
                    self.stats['knowledge_syncs'] += 1
                
                threading.Event().wait(30)  # Sincroniza cada 30 segundos
            except Exception as e:
                logger.error(f"[HIVE] Error en sync loop: {e}")
    
    # Message Handlers
    
    def _handle_heartbeat(self, message: HiveMessage):
        """Maneja heartbeat de otros nodos"""
        peer_id = message.payload.get('node_id')
        logger.debug(f"[HIVE] Heartbeat recibido de {peer_id}")
    
    def _handle_announce(self, message: HiveMessage):
        """Maneja anuncio de otro nodo"""
        node_info = message.payload.get('node_info')
        logger.info(f"[HIVE] Anuncio recibido: {node_info.get('node_id')}")
    
    def _handle_knowledge_share(self, message: HiveMessage):
        """Maneja compartir conocimiento"""
        remote_knowledge = message.payload.get('knowledge', {})
        
        # Sincroniza conocimiento
        sync_result = self.sync_manager.sync_knowledge(
            dict(self.local_jarvis.learning.knowledge_base),
            remote_knowledge
        )
        
        logger.info(f"[HIVE] Conocimiento sincronizado: {len(sync_result['added'])} nuevos temas")
    
    def _handle_skill_share(self, message: HiveMessage):
        """Maneja compartir habilidades"""
        remote_skills = message.payload.get('skills', {})
        
        sync_result = self.sync_manager.sync_skills(
            self.local_jarvis.skill_system.skills,
            remote_skills
        )
        
        logger.info(f"[HIVE] Habilidades sincronizadas: {len(sync_result['adopted'])} adoptadas")
    
    def _handle_task_request(self, message: HiveMessage):
        """Maneja solicitud de tarea delegada"""
        task_id = message.payload.get('task_id')
        task_type = message.payload.get('task_type')
        task_data = message.payload.get('data')
        
        logger.info(f"[HIVE] Tarea solicitada: {task_type} ({task_id})")
        
        # Simula ejecución de tarea
        result = {'success': True, 'result': 'Task completed'}
        
        self.send_message(message.sender_id, MessageType.TASK_RESULT, {
            'task_id': task_id,
            'result': result,
        })
    
    def _handle_task_result(self, message: HiveMessage):
        """Maneja resultado de tarea delegada"""
        task_id = message.payload.get('task_id')
        result = message.payload.get('result')
        
        logger.info(f"[HIVE] Resultado de tarea recibido: {task_id}")
    
    def _handle_status_query(self, message: HiveMessage):
        """Maneja consulta de estado"""
        status = self.node.get_info()
        
        self.send_message(message.sender_id, MessageType.STATUS_RESPONSE, {
            'status': status
        })
    
    def delegate_task(self, task_type: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Delega una tarea a otro nodo en la red
        Retorna task_id si es exitoso
        """
        if not self.peers:
            logger.warning("[HIVE] No hay nodos disponibles para delegación")
            return None
        
        import random
        target_peer = random.choice(list(self.peers.values()))
        task_id = str(uuid.uuid4())
        
        self.send_message(target_peer.peer_id, MessageType.TASK_REQUEST, {
            'task_id': task_id,
            'task_type': task_type,
            'data': data,
            'priority': 5,
        })
        
        self.stats['task_delegations'] += 1
        logger.info(f"[HIVE] Tarea delegada: {task_type} a {target_peer.peer_id}")
        
        return task_id
    
    def get_network_status(self) -> Dict[str, Any]:
        """
        Obtiene estado general de la red
        """
        return {
            'node': self.node.get_info(),
            'peers_connected': len(self.peers),
            'peers': {pid: p.peer_id for pid, p in self.peers.items()},
            'message_queue_size': len(self.message_queue),
            'stats': self.stats,
            'sync_status': self.sync_manager.get_sync_status(),
        }
