# Agent Message Queue

Message queue system for agent-to-agent communication.

## Features

- **Message Queuing** - Queue messages between agents
- **Pub/Sub** - Publish-subscribe messaging
- **Priority Queues** - Priority-based message handling
- **Message Persistence** - Store messages for reliability

## Quick Start

```python
from agent_message_queue import AgentMessageQueue

mq = AgentMessageQueue()
mq.enqueue("agent-1", {"msg": "hello"})
msg = mq.dequeue("agent-1")
```

## License

MIT
