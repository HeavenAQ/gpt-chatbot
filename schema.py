from dataclasses import asdict, dataclass
from enum import Enum
from typing import Literal


class SenderType(Enum):
    USER = "user"
    BOT = "bot"


@dataclass(frozen=True, kw_only=True, init=True)
class UserMessage:
    sender: Literal["user"]
    text: str

    def to_dict(self):
        return asdict(self)


@dataclass(frozen=True, kw_only=True, init=True)
class BotMessage:
    sender: Literal["bot"]
    question: str
    text: str

    def to_dict(self):
        return asdict(self)
