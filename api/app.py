# from services.Recomender import recomend_me
import re
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.api_models import Chat, ChatResponse, Message, MessageRequest
from services import service_registry
from services.db_service import DB
from sqlmodel import Session
from utils.id_generators import generate_id_with_prefix

expr = re.compile(r"(\([0-9]{4}\))$")


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
db = DB()
db.init()


@app.post("/chat", response_model=Chat)
def create_chat(session: Session = Depends(db.get_session)):
    chat = Chat(id=generate_id_with_prefix("chat"))
    session.add(chat)
    session.commit()
    session.refresh(chat)
    return chat


@app.get("/chat/{chat_id}", response_model=ChatResponse)
def get_chat(chat_id: str, session: Session = Depends(db.get_session)):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    return chat


@app.post("/chat/{chat_id}/message", response_model=Message)
def send_query(chat_id: str, prompt: MessageRequest, session: Session = Depends(db.get_session)):
    chat = session.get(Chat, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if chat.messages:
        msg_seq_no = chat.messages[-1].seq_no + 1
    else:
        msg_seq_no = 1
    suggestions = list()
    movie1, _ = service_registry.get_service("tfidf_recommender_service").recommend(prompt.message)
    suggestions.extend(movie1)
    movie2, _ = service_registry.get_service("similarity_recommender_service").recommend(prompt.message)
    for movie in movie2:
        suggestions.append(expr.sub("", movie).strip())
    prompt = Message.model_validate(prompt)
    prompt.seq_no = msg_seq_no
    msg_seq_no += 1
    response = Message(message="We suggest that you watch " + " ".join(suggestions), role="system", chat_id=chat.id, seq_no=msg_seq_no)
    chat.updated_time = response.creation_time
    chat.messages.append(prompt)
    chat.messages.append(response)
    session.add(chat)
    session.commit()
    session.refresh(response)
    return response