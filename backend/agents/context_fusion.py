from backend.memory.postgres_memory import get_recent_messages
from backend.core.logger import get_logger

logger = get_logger(__name__)


def build_context(query, user_id, documents):

    memory = get_recent_messages(user_id)

    memory_text = (
        "\n".join([f"{m['role']}: {m['content']}" for m in memory]) if memory else ""
    )

    docs_text = "\n".join([doc.page_content for doc in documents]) if documents else ""

    logger.info("Context built successfully")

    return {"memory": memory_text, "documents": docs_text}
