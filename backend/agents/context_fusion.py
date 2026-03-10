from backend.rag.retriever import get_relevant_documents
from backend.memory.postgres_memory import get_recent_messages


def build_context(user_query: str, user_id: str) -> dict:
    memory_messages = get_recent_messages(user_id=user_id, limit=5)

    memory_context = "\n".join(
        [f"{m['role']}: {m['content']}" for m in memory_messages]
    )

    docs = get_relevant_documents(user_query)
    doc_context = "\n".join([doc.page_content for doc in docs])

    return {
        "memory": memory_context,
        "documents": doc_context,
    }
