from fastapi import FastAPI
from pydantic import BaseModel

from backend.llm.ollama_client import OllamaClient
from backend.memory.postgres_memory import PostgresMemory


app = FastAPI()

llm = OllamaClient()
memory = PostgresMemory()


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"status": "EchoMind running"}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    session_id = req.session_id
    user_message = req.message

    # Save user message
    memory.save_message(session_id, "user", user_message)

    # Load conversation history
    history = memory.load_history(session_id)

    # Generate response
    response = llm.chat(user_message, history)

    # Save assistant response
    memory.save_message(session_id, "assistant", response)

    return ChatResponse(response=response)
