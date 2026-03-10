from backend.rag.retriever import RAGRetriever
from backend.memory.postgres_memory import PostgresMemory


class ContextFusion:

    def __init__(self):
        self.retriever = RAGRetriever()
        self.memory = PostgresMemory()

    def build_context(self, user_id: str, query: str):
        memory_context = self.memory.get_recent_conversation(user_id)
        rag_docs = self.retriever.retrieve(query)
        rag_context = "\n\n".join([doc.page_content for doc in rag_docs])

        final_context = f"""
        Conversation Memory:
        {memory_context}

        Knowledge Base:
        {rag_context}
        """

        return final_context
