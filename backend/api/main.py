from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

import shutil
from pathlib import Path

from backend.core.logger import get_logger
from backend.llm.ollama_client import OllamaClient
from backend.rag.retriever import retrieve_documents, build_context
from backend.rag.ingest import run_ingestion

logger = get_logger(__name__)

app = FastAPI()

llm_client = OllamaClient()
UPLOAD_DIR = "data/uploads"
CURRENT_COLLECTION = "default"


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.2:3b"


class ChatResponse(BaseModel):
    response: str


@app.get("/")
def root():
    return {"status": "EchoMind API running"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global CURRENT_COLLECTION
    Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
    file_path = Path(UPLOAD_DIR) / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    collection_name = Path(file.filename).stem
    logger.info(f"Uploaded file: {file.filename}")
    run_ingestion(collection_name=collection_name)
    CURRENT_COLLECTION = collection_name
    logger.info(f"Active collection set to: {CURRENT_COLLECTION}")

    return {
        "status": "success",
        "file": file.filename,
        "collection": collection_name,
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    user_message = request.message
    logger.info(f"User message: {user_message}")
    docs = retrieve_documents(user_message, collection_name=CURRENT_COLLECTION)
    context = build_context(docs)

    prompt = f"""
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {user_message}
    """

    llm = llm_client.get_llm()
    response = llm.invoke(prompt)
    answer = response.content
    logger.info("Answer generated")
    return ChatResponse(response=answer)
