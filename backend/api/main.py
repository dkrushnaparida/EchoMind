from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import StreamingResponse
from backend.agents.agent import handle_query_stream


app = FastAPI()


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.post("/chat")
def chat(req: ChatRequest):
    def generate():
        for token in handle_query_stream(req.user_id, req.message):
            yield token

    return StreamingResponse(generate(), media_type="text/plain")
