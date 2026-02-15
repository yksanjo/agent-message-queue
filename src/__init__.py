"""Agent Message Queue - Message queue system for agent-to-agent communication."""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import uuid
import heapq
from collections import defaultdict


class AgentType(Enum):
    NVIDIA_GPU = "nvidia"
    AWS_TRAINIUM = "trainium"
    GOOGLE_TPU = "tpu"
    CPU = "cpu"


class Protocol(Enum):
    MCP = "mcp"
    A2A = "a2a"
    CUSTOM = "custom"
    HTTP = "http"


@dataclass
class QueuedMessage:
    message_id: str
    sender: str
    receiver: str
    content: Any
    priority: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __lt__(self, other):
        return self.priority > other.priority


class AgentMessageQueue:
    """Message queue system for agent-to-agent communication."""
    
    def __init__(self):
        self.queues: Dict[str, List[QueuedMessage]] = defaultdict(list)
        self.pubsub: Dict[str, List[str]] = defaultdict(list)
        self.persistent: Dict[str, List[QueuedMessage]] = {}
    
    def enqueue(self, receiver: str, content: Any, sender: str = "system", priority: int = 0) -> str:
        message_id = str(uuid.uuid4())
        msg = QueuedMessage(message_id=message_id, sender=sender, receiver=receiver, content=content, priority=priority)
        
        if self.persistent.get(receiver):
            self.persistent[receiver].append(msg)
        else:
            heapq.heappush(self.queues[receiver], msg)
        
        return message_id
    
    def dequeue(self, receiver: str) -> Optional[QueuedMessage]:
        if receiver in self.queues and self.queues[receiver]:
            return heapq.heappop(self.queues[receiver])
        return None
    
    def peek(self, receiver: str) -> Optional[QueuedMessage]:
        if receiver in self.queues and self.queues[receiver]:
            return self.queues[receiver][0]
        return None
    
    def subscribe(self, topic: str, agent_id: str) -> None:
        if agent_id not in self.pubsub[topic]:
            self.pubsub[topic].append(agent_id)
    
    def unsubscribe(self, topic: str, agent_id: str) -> None:
        if topic in self.pubsub and agent_id in self.pubsub[topic]:
            self.pubsub[topic].remove(agent_id)
    
    def publish(self, topic: str, content: Any) -> int:
        subscribers = self.pubsub.get(topic, [])
        count = 0
        
        for agent_id in subscribers:
            self.enqueue(agent_id, content, sender=f"topic:{topic}")
            count += 1
        
        return count
    
    def get_queue_size(self, receiver: str) -> int:
        return len(self.queues.get(receiver, []))
    
    def clear_queue(self, receiver: str) -> int:
        size = self.get_queue_size(receiver)
        self.queues[receiver] = []
        return size


__all__ = ["AgentMessageQueue", "QueuedMessage", "AgentType", "Protocol"]
