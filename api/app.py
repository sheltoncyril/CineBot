# from services.Recomender import recomend_me
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.models import Chat, ChatResponse, Message, MessageRequest
from services import service_registry
from services.db_service import DBService
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    service_registry.init()
    yield
    service_registry.cleanup()


app = FastAPI(lifespan=lifespan)
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
db_service = DBService()
db_service.init()


@app.post("/chat", response_model=Chat)
def create_chat(session: Session = Depends(db_service.get_session)):
    return service_registry.get_service("chat_application_service").create_chat(session)


@app.get("/chat/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: str, session: Session = Depends(db_service.get_session)):
    return service_registry.get_service("chat_application_service").get_chat(session, chat_id)


@app.post("/chat/{chat_id}/message", response_model=Message)
def process_message(chat_id: str, message_request: MessageRequest, session: Session = Depends(db_service.get_session)):
    return service_registry.get_service("chat_application_service").process_message(session, chat_id, message_request)
