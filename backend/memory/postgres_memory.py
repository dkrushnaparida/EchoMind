import psycopg2
from datetime import datetime
from backend.core.config import settings
from backend.memory.memory_vector_store import memory_vector_store

DB_CONFIG = {
    "dbname": "echomind",
    "user": "postgres",
    "password": "Dwiti@1995",
    "host": "localhost",
    "port": "5432",
}


def get_connection():
    print("Connecting to DB:", settings.DB_NAME)
    return psycopg2.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )


def save_message(user_id: str, role: str, content: str):

    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO conversations (user_id, role, content)
    VALUES (%s, %s, %s)
    """
    cur.execute(query, (user_id, role, content))
    conn.commit()
    # print("Saved message:", role)
    memory_vector_store.add_texts(
        texts=[content], metadatas=[{"user_id": user_id, "role": role}]
    )

    cur.close()
    conn.close()


def get_recent_messages(user_id: str, limit: int = 5):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    SELECT role, content
    FROM conversation_memory
    WHERE user_id = %s
    ORDER BY created_at DESC
    LIMIT %s
    """

    cursor.execute(query, (user_id, limit))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    messages = []

    for role, content in rows:
        messages.append({"role": role, "content": content})

    return messages[::-1]


def search_memory(user_id: str, query: str, k: int = 3):
    results = memory_vector_store.similarity_search(query, k=k)
    memories = []

    for r in results:
        if r.metadata.get("user_id") == user_id:
            memories.append(r.page_content)

    return memories
