from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from backend.core.config import settings
from backend.core.logger import get_logger
from backend.rag.query_rewriter import QueryRewriter

logger = get_logger(__name__)


class RAGRetriever:
    def __init__(self):

        self.embeddings = OllamaEmbeddings(model="nomic-embed-text:latest")

        self.vectorstore = Chroma(
            persist_directory="data/vectordb", embedding_function=self.embeddings
        )

        self.rewriter = QueryRewriter()

        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})

    def retrieve(self, query: str):
        rewritten_query = self.rewriter.rewrite(query)
        logger.info(f"Original Query: {query}")
        logger.info(f"Rewritten Query: {rewritten_query}")

        docs = self.retriever.invoke(rewritten_query)

        return docs
