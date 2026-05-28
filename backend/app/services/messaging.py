from typing import List, Dict, Any, Optional

from .persistence import SQLitePersistence


class InMemoryMessenger:
    """Simple message delivery abstraction used for tests.

    Implementations for real channels (Slack, email) should implement the
    same interface and be wired behind this abstraction.
    """

    def __init__(self, persistence: Optional[SQLitePersistence] = None):
        self.messages: List[Dict[str, Any]] = []
        self.persistence = persistence

    def send_message(
        self,
        channel: str,
        text: str,
        sender: str = "system",
        role: str = "assistant",
        agent_id: str | None = None,
    ) -> None:
        message = {
            "agent_id": agent_id,
            "sender": sender,
            "role": role,
            "channel": channel,
            "text": text,
        }
        self.messages.append(message)
        if self.persistence:
            self.persistence.save_message(channel, text, sender, role, agent_id)

    def get_messages(
        self, agent_id: str | None = None, channel: str | None = None
    ) -> List[Dict[str, Any]]:
        if self.persistence:
            return self.persistence.list_messages(agent_id=agent_id, channel=channel)
        results = [m for m in self.messages if (agent_id is None or m.get("agent_id") == agent_id) and (channel is None or m.get("channel") == channel)]
        return list(results)
