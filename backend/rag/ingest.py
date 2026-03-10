import os
from pathlib import Path

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.core.logger import get_logger

logger = get_logger(__name__)

DATA_PATH = "data/uploads"
VECTOR_DB_PATH = "data/vectordb"


def load_documents():
    documents = []

    for file in Path(DATA_PATH).glob("*.pdf"):
        logger.info(f"Loading file: {file}")
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        documents.extend(docs)

    return documents


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = text_splitter.split_documents(documents)

    logger.info(f"Created {len(chunks)} chunks")

    return chunks


def create_embeddings():
    embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

    return embeddings


def create_vector_store(chunks):

    embeddings = create_embeddings()
    vectordb = Chroma.from_documents(
        documents=chunks, embedding=embeddings, persist_directory=VECTOR_DB_PATH
    )

    logger.info("database created successfully")

    return vectordb


def run_ingestion():
    docs = load_documents()

    if not docs:
        logger.warning("No documents found")
        return

    chunks = split_documents(docs)

    vectordb = create_vector_store(chunks)

    return vectordb


if __name__ == "__main__":
    run_ingestion()
