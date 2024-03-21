from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Sender(str, Enum):
    user = "user"
    chatbot = "chatbot"
    server = "server"


class Chat(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    creation_time: datetime = datetime.now()
    updated_time: datetime = datetime.now()

    messages: List["Message"] = Relationship(back_populates="chat")


class ChatResponse(SQLModel):
    id: str
    creation_time: datetime
    updated_time: datetime
    messages: List["Message"]


class MessageRequest(SQLModel):
    message: str
    sender: Sender = "user"


class Message(MessageRequest, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender: Sender
    creation_time: datetime = datetime.now()

    chat_id: Optional[str] = Field(default=None, foreign_key="chat.id")
    chat: Optional[Chat] = Relationship(back_populates="messages")
