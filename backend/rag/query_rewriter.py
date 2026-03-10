from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

from backend.core.logger import get_logger

logger = get_logger(__name__)


class QueryRewriter:
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0)

        self.prompt = ChatPromptTemplate.from_template(
            """
        You are a search query optimizer for a RAG system.

        Rewrite the user question into a concise semantic search query.

        Rules:
        - keep meaning same
        - remove conversational words
        - expand keywords if useful
        - output ONLY the rewritten query

        User Question:
        {query}
        """
        )

        self.chain = self.prompt | self.llm

    def rewrite(self, query: str) -> str:
        try:
            result = self.chain.invoke({"query": query})
            rewritten = result.content.strip()

            logger.info(f"Query rewritten: {rewritten}")

            return rewritten

        except Exception as e:
            logger.error(f"Query rewrite failed: {e}")
            return query
