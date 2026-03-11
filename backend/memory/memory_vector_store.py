from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from backend.core.config import settings


embeddings = OllamaEmbeddings(model="nomic-embed-text")

memory_vector_store = Chroma(
    collection_name="conversation_memory",
    embedding_function=embeddings,
    persist_directory=f"{settings.VECTOR_DB_DIR}/memory",
)
