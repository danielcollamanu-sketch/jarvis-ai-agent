# JARVIS AI Agent - Red Colmena (Hive Network)

## Descripción General

La **Red Colmena** es un protocolo P2P descentralizado que permite que múltiples instancias de JARVIS:

- 🔍 **Se descubran automáticamente** en la red local vía mDNS
- 📚 **Compartan conocimiento** sincronizando sus bases de datos
- 🎓 **Compartan habilidades** mejorando el aprendizaje colectivo
- 💼 **Deleguen tareas** según capacidad disponible
- 🧠 **Sincronicen personalidad** para convergencia colectiva
- ⚙️ **Tomen decisiones distribuidas** mediante consenso

## Arquitectura

```
        ┌─────────────────────┐
        │  Discovery Service  │ (mDNS)
        │  Descubrimiento     │
        └──────────┬──────────┘
                   │
      ┌────────────┼────────────┐
      │            │            │
  ┌───▼──────┐ ┌──▼────────┐ ┌─▼──────────┐
  │  JARVIS  │ │  JARVIS   │ │   JARVIS   │
  │ Nodo 1   │ │  Nodo 2   │ │   Nodo 3   │
  └───┬──────┘ └──┬────────┘ └─┬──────────┘
      │           │            │
      └───────────┼────────────┘
                  │
        ┌─────────▼──────────┐
        │   Hive Network     │
        │   P2P Mesh         │
        └────────────────────┘
             │      │      │
        ┌────▼──┬───▼──┬───▼────┐
        │Message│Sync  │Task    │
        │Queue  │Mgr   │Deleg   │
        └───────┴──────┴────────┘
```

## Tipos de Mensajes

### Discovery (Descubrimiento)
- `HEARTBEAT`: Señal de vida periódica
- `ANNOUNCE`: Anuncio de disponibilidad de nodo

### Knowledge Sharing (Compartir Conocimiento)
- `KNOWLEDGE_SHARE`: Sincronizar base de conocimiento
- `SKILL_SHARE`: Compartir habilidades aprendidas
- `PERSONALITY_SYNC`: Sincronizar rasgos de personalidad

### Task Delegation (Delegación de Tareas)
- `TASK_REQUEST`: Solicitud de tarea a otro nodo
- `TASK_RESPONSE`: Respuesta a solicitud
- `TASK_RESULT`: Resultado de tarea completada

### Consensus (Consenso)
- `VOTE_REQUEST`: Solicitar voto para decisión colectiva
- `VOTE_RESPONSE`: Respuesta de voto

### Health (Salud)
- `STATUS_QUERY`: Consultar estado de nodo
- `STATUS_RESPONSE`: Respuesta de estado

## Protocolo de Sincronización

### 1. Conocimiento
```python
# Compara hechos locales vs remotos
# Merge inteligente basado en confianza
# Resuelve conflictos mediante consensus
```

### 2. Habilidades
```python
# Adopta nuevas habilidades de pares
# Promedia proficiencia entre nodos
# Acelera aprendizaje colectivo
```

### 3. Personalidad
```python
# Promedia rasgos de personalidad
# Converge hacia personalidad emergente colectiva
# Mantiene individualidad con threshold de cambio
```

## Delegación de Tareas

```python
hive = HiveNetwork(jarvis_instance)
hive.start()

# Delega investigación a nodo disponible
task_id = hive.delegate_task(
    task_type='research',
    data={'topic': 'quantum_computing', 'depth': 'deep'}
)

# Espera resultado
result = hive.wait_for_result(task_id, timeout=30)
```

## Estadísticas

```python
status = hive.get_network_status()
# {
#   'node': {...},
#   'peers_connected': 3,
#   'message_queue_size': 42,
#   'stats': {
#       'messages_sent': 156,
#       'messages_received': 189,
#       'knowledge_syncs': 12,
#       'task_delegations': 5
#   }
# }
```

## Seguridad

- TTL (Time To Live) para prevenir loops infinitos
- Validación de nodos descubiertos
- Versionado de conocimiento para auditoría
- Encriptación opcional para mensajes sensibles

## Instalación

```bash
pip install zeroconf  # Para mDNS
```

## Uso

```python
from core.jarvis_core import JARVISCore, JARVISConfig
from network.hive_network import HiveNetwork

# Crea instancia JARVIS
jarvis = JARVISCore()
jarvis.startup()

# Inicia Red Colmena
hive = HiveNetwork(jarvis)
hive.start()

# Monitorea red
print(hive.get_network_status())
```
