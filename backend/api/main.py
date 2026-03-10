from fastapi import FastAPI
from pydantic import BaseModel

from backend.agents.agent import handle_query
from backend.memory.postgres_memory import save_message


app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


class ChatResponse(BaseModel):
    response: str


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):

    response = handle_query(user_id=req.user_id, query=req.message)

    save_message(req.user_id, "user", req.message)
    save_message(req.user_id, "assistant", response)

    return ChatResponse(response=response)
