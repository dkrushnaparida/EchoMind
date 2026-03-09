from fastapi import FastAPI
from pydantic import BaseModel

from backend.llm.ollama_client import OllamaClient


app = FastAPI()
llm = OllamaClient()


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"message": "EchoMind API running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = llm.chat(request.message)

    return ChatResponse(response=answer)
