from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from backend.core.config import settings
from backend.rag.query_rewriter import QueryRewriter
from backend.core.logger import get_logger

logger = get_logger(__name__)


class RAGRetriever:
    def __init__(self):
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vectorstore = Chroma(
            persist_directory=settings.VECTOR_DB_DIR,
            embedding_function=self.embeddings,
        )

        self.rewriter = QueryRewriter()

    def retrieve(self, query: str):
        rewritten_query = self.rewriter.rewrite(query)

        logger.info(f"Original Query: {query}")
        logger.info(f"Rewritten Query: {rewritten_query}")
        docs = self.vectorstore.similarity_search(rewritten_query, k=5)

        return docs
