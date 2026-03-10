from fastapi import FastAPI
from pydantic import BaseModel
from backend.rag.retriever import ask_question
from backend.core.logger import get_logger

logger = get_logger(__name__)
app = FastAPI()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"message": "EchoMind API running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    logger.info(f"User message: {request.message}")
    answer = ask_question(request.message)
    return ChatResponse(response=answer)
