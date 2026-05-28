import os
import httpx

class SlackClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv('SLACK_BOT_TOKEN')
        self.api_url = 'https://slack.com/api/chat.postMessage'

    def send_message(self, channel: str, text: str):
        if not self.token:
            raise ValueError('Slack bot token is required to send a Slack message.')

        if channel.startswith('slack:'):
            channel = channel.split(':', 1)[1]

        with httpx.Client(timeout=15.0) as client:
            response = client.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.token}',
                    'Content-Type': 'application/json',
                },
                json={
                    'channel': channel,
                    'text': text,
                },
            )
            response.raise_for_status()
            payload = response.json()
            if not payload.get('ok'):
                raise ValueError(f"Slack API error: {payload.get('error')}")
            return payload
