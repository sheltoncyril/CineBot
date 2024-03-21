from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class Role(str, Enum):
    user = "user"
    assistant = "assistant"
    system = "system"


class Chat(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    creation_time: datetime = datetime.now()
    updated_time: datetime = datetime.now()

    messages: List["Message"] = Relationship(back_populates="chat")


class ChatResponse(SQLModel):
    id: str
    creation_time: datetime
    updated_time: datetime
    messages: List["MessageResponse"]


class MessageRequest(SQLModel):
    message: str
    role: Role = "user"


class MessageResponse(SQLModel):
    id: int
    seq_no: int
    message: str
    role: Role
    creation_time: datetime


class Message(MessageRequest, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    seq_no: int | None = None
    role: Role
    creation_time: datetime = datetime.now()
    chat_id: Optional[str] = Field(default=None, foreign_key="chat.id")
    chat: Optional[Chat] = Relationship(back_populates="messages")
