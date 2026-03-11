from backend.memory.postgres_memory import get_recent_messages, search_memory
from backend.core.logger import get_logger

logger = get_logger(__name__)


def build_context(user_id, query, documents):
    recent_memory = get_recent_messages(user_id)
    recent_memory_text = (
        "\n".join([f"{m['role']}: {m['content']}" for m in recent_memory])
        if recent_memory
        else ""
    )

    semantic_memory = search_memory(user_id, query)
    semantic_memory_text = "\n".join(semantic_memory) if semantic_memory else ""

    memory_text = f"{recent_memory_text}\n{semantic_memory_text}"

    docs_text = "\n".join([doc.page_content for doc in documents]) if documents else ""

    logger.info("Context built successfully")

    return {"memory": memory_text, "documents": docs_text}
