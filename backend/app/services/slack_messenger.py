from .messaging import InMemoryMessenger
from connectors.slack.slack_client import SlackClient
from .persistence import SQLitePersistence

class SlackMessenger(InMemoryMessenger):
    def __init__(self, persistence: SQLitePersistence | None = None, slack_client: SlackClient | None = None):
        super().__init__(persistence)
        self.slack_client = slack_client or SlackClient()

    def send_message(
        self,
        channel: str,
        text: str,
        sender: str = "system",
        role: str = "assistant",
        agent_id: str | None = None,
    ) -> None:
        if channel.startswith("slack:"):
            try:
                self.slack_client.send_message(channel, text)
            except Exception:
                pass
        super().send_message(channel, text, sender=sender, role=role, agent_id=agent_id)
