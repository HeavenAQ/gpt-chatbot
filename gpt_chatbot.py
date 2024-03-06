from typing import Any

from flask import Flask

from chatbot import Linebot
from config import GPTChatBotConfig
from db import FireStore
from llm import GPT


class GPTChatbot:
    def __init__(self, config: GPTChatBotConfig):
        self.config = config
        self.server = Flask(__name__)
        self.gpt = GPT(config.openai)
        self.chatbot = Linebot(config.line)
        self.db = FireStore(config.firestore)
        self.server.logger.info("GPTChatbot initialized")

    def send_gpt_query(self, event: Any) -> str:
        question = event.message.text
        context_id = event.message.quoted_message_id
        user = self.db.get_user(event.source.user_id)
        if not user:
            self.db.create_user(event.source.user_id, {})
            return self.gpt.send_query(question)

        if context_id:
            question = user[context_id] + question

        return self.gpt.send_query(question)
