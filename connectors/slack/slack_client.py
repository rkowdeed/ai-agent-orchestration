import os

class SlackClient:
    def __init__(self, token: str | None = None):
        self.token = token or os.getenv('SLACK_BOT_TOKEN')

    def send_message(self, channel: str, text: str):
        # placeholder: implement with slack_sdk.WebClient
        raise NotImplementedError()
