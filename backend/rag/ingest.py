import os
from pathlib import Path
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from backend.core.logger import get_logger

logger = get_logger(__name__)

DATA_PATH = "data/uploads"
VECTOR_DB_PATH = "data/vectordb"


def load_documents():
    documents = []

    for file in Path(DATA_PATH).glob("*"):
        logger.info(f"Loading file: {file}")
        if file.suffix == ".pdf":
            loader = PyPDFLoader(str(file))
        elif file.suffix == ".txt":
            loader = TextLoader(str(file))
        elif file.suffix == ".docx":
            loader = Docx2txtLoader(str(file))
        else:
            logger.warning(f"Unsupported file type: {file}")
            continue

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


def create_vector_store(chunks, collection_name="default"):
    os.makedirs(VECTOR_DB_PATH, exist_ok=True)
    embeddings = create_embeddings()
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTOR_DB_PATH,
        collection_name=collection_name,
    )
    # vectordb.persist()
    logger.info(f"DB created | collection={collection_name}")
    return vectordb


def run_ingestion(collection_name="default"):
    docs = load_documents()
    if not docs:
        logger.warning("No documents found")
        return None
    chunks = split_documents(docs)
    vectordb = create_vector_store(chunks, collection_name=collection_name)
    return vectordb


if __name__ == "__main__":
    run_ingestion()
