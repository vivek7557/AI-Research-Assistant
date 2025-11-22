
"""Simple in-memory Agent-to-Agent (A2A) messaging bus.
Agents can publish messages to topics and subscribe handlers.
This is suitable for local dev; production would use Redis/RabbitMQ/Kafka.
"""
import threading
from typing import Callable, Dict, List, Any

class AgentBus:
    def __init__(self):
        self._subs: Dict[str, List[Callable[[Dict[str,Any]], None]]] = {}
        self._lock = threading.Lock()

    def subscribe(self, topic: str, handler: Callable[[Dict[str,Any]], None]):
        with self._lock:
            self._subs.setdefault(topic, []).append(handler)

    def publish(self, topic: str, msg: Dict[str, Any]):
        handlers = []
        with self._lock:
            handlers = list(self._subs.get(topic, []))
        for h in handlers:
            try:
                h(msg)
            except Exception as e:
                print(f'AgentBus handler error: {e}')

# Simple example usage:
bus = AgentBus()
