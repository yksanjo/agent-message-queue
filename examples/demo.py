#!/usr/bin/env python3
"""Demo for Agent Message Queue."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src import AgentMessageQueue

def main():
    print("Agent Message Queue Demo")
    mq = AgentMessageQueue()
    mq.enqueue("agent-1", "Hello")
    mq.enqueue("agent-1", "World")
    msg = mq.dequeue("agent-1")
    print(f"Got: {msg.content if msg else 'None'}")
    print("Done!")

if __name__ == "__main__": main()
