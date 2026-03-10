from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from backend.core.config import settings


embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

vectordb = Chroma(
    persist_directory=settings.VECTOR_DB_DIR, embedding_function=embeddings
)


def get_relevant_documents(query: str, k: int = 4):
    retriever = vectordb.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(query)

    return docs
