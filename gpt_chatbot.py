from typing import Any

from firebase_admin import json
from flask import Flask

from chatbot import Linebot
from config import GPTChatBotConfig
from db import FireStore
from llm import GPT
from schema import BotMessage, SenderType, UserMessage


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
        context_id = event.message.quoted_message_id or ""
        user = self.db.get_user(event.source.user_id)
        if not user:
            self.db.create_user(event.source.user_id, {})
            return self.gpt.send_query(question)

        context = ""
        if context_msg := user.get(context_id):
            prev_question = context_msg.get("question", "")
            text = context_msg.get("text", "")
            context = f"{text}\n{prev_question}"

        return self.gpt.send_query(f"{context}\n{question}")

    def store_gpt_response(self, event: Any, line_res: str, gpt_res: str):
        data = json.loads(line_res)
        res_msg_id = data["sentMessages"][0]["id"]
        user_msg = {
            event.message.id: UserMessage(
                sender=SenderType.USER.value,
                text=event.message.text,
            ).to_dict()
        }

        bot_msg = {
            res_msg_id: BotMessage(
                sender=SenderType.BOT.value,
                question=event.message.text,
                text=gpt_res,
            ).to_dict()
        }

        self.db.update_user(event.source.user_id, user_msg | bot_msg)
