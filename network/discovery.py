"""
Servicio de Descubrimiento de Red Colmena
Utiliza mDNS para descubrir automáticamente otros nodos JARVIS en la red local
"""

import socket
import json
import threading
from typing import Dict, List, Optional, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class PeerInfo:
    """Información de un nodo par descubierto"""
    peer_id: str
    hostname: str
    port: int
    service_name: str
    last_seen: str
    capabilities: List[str]
    version: str

class DiscoveryService:
    """
    Servicio de descubrimiento para la Red Colmena
    Implementa mDNS/Bonjour para anunciar y descubrir nodos
    """
    
    SERVICE_TYPE = "_jarvis-hive._tcp.local."
    
    def __init__(self, node_id: str, hostname: str, port: int, capabilities: List[str]):
        self.node_id = node_id
        self.hostname = hostname
        self.port = port
        self.capabilities = capabilities
        self.discovered_peers: Dict[str, PeerInfo] = {}
        self.is_running = False
        self.discovery_callbacks: List[Callable] = []
        
        logger.info(f"[DISCOVERY] Servicio inicializado para {node_id}")
    
    def register_callback(self, callback: Callable):
        """
        Registra callback para cuando se descubre un nuevo nodo
        Callback recibe (peer_info: PeerInfo)
        """
        self.discovery_callbacks.append(callback)
    
    def start_discovery(self) -> bool:
        """
        Inicia el servicio de descubrimiento
        En una implementación real, usaría zeroconf (python-zeroconf)
        """
        self.is_running = True
        logger.info(f"[DISCOVERY] Iniciando descubrimiento mDNS en puerto {self.port}")
        
        # Simula descubrimiento inicial
        # En producción, usar zeroconf library
        discovery_thread = threading.Thread(target=self._discovery_loop, daemon=True)
        discovery_thread.start()
        
        return True
    
    def _discovery_loop(self):
        """
        Loop de descubrimiento que busca nodos cada cierto tiempo
        """
        while self.is_running:
            try:
                # Aquí iría la lógica de descubrimiento mDNS real
                # Por ahora, solo limpia peers expirados
                self._cleanup_stale_peers()
                threading.Event().wait(5)  # Espera 5 segundos
            except Exception as e:
                logger.error(f"[DISCOVERY] Error en loop: {e}")
    
    def announce_self(self):
        """
        Anuncia este nodo en la red
        En producción, usa zeroconf.ServiceInfo
        """
        logger.info(f"[DISCOVERY] Anunciando servicio: {self.hostname}:{self.port}")
    
    def discover_peers(self) -> Dict[str, PeerInfo]:
        """
        Descubre nodos pares en la red
        Retorna diccionario de pares descubiertos
        """
        return self.discovered_peers.copy()
    
    def add_discovered_peer(self, peer_info: PeerInfo):
        """
        Agrega un nodo descubierto
        """
        if peer_info.peer_id != self.node_id:  # No a uno mismo
            self.discovered_peers[peer_info.peer_id] = peer_info
            logger.info(f"[DISCOVERY] Nodo descubierto: {peer_info.peer_id}")
            
            # Ejecuta callbacks
            for callback in self.discovery_callbacks:
                try:
                    callback(peer_info)
                except Exception as e:
                    logger.error(f"[DISCOVERY] Error en callback: {e}")
    
    def _cleanup_stale_peers(self):
        """
        Elimina nodos que no han enviado heartbeat recientemente
        """
        cutoff_time = datetime.now() - timedelta(seconds=30)
        stale_peers = []
        
        for peer_id, peer_info in self.discovered_peers.items():
            try:
                last_seen = datetime.fromisoformat(peer_info.last_seen)
                if last_seen < cutoff_time:
                    stale_peers.append(peer_id)
            except:
                stale_peers.append(peer_id)
        
        for peer_id in stale_peers:
            del self.discovered_peers[peer_id]
            logger.warning(f"[DISCOVERY] Nodo expirado: {peer_id}")
    
    def stop_discovery(self):
        """
        Detiene el servicio de descubrimiento
        """
        self.is_running = False
        logger.info("[DISCOVERY] Descubrimiento detenido")
