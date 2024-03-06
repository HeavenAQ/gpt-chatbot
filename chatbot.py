from linebot.v3 import WebhookHandler
from linebot.v3.messaging import Configuration

from config import LineConfig


class Linebot:
    def __init__(self, line_config: LineConfig):
        self.config = Configuration(access_token=line_config.access_token)
        self.handler = WebhookHandler(line_config.channel_secret)
