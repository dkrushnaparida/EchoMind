from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from backend.core.logger import get_logger

logger = get_logger(__name__)

VECTOR_DB_PATH = "data/vectordb"


def create_embeddings():
    return OllamaEmbeddings(model="nomic-embed-text:latest")


def get_retriever(collection_name: str = "default"):
    logger.info(f"Loading retriever | collection={collection_name}")
    embeddings = create_embeddings()
    vectordb = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embeddings,
        collection_name=collection_name,
    )

    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"k": 6, "score_threshold": 0.65},
    )

    return retriever


def retrieve_documents(question: str, collection_name: str = "default"):
    logger.info(f"User question: {question}")
    retriever = get_retriever(collection_name)
    docs = retriever.invoke(question)
    logger.info(f"Retrieved {len(docs)} documents")

    return docs


def build_context(docs):
    context = "\n\n".join(doc.page_content for doc in docs)

    return context
