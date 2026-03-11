import psycopg2
from datetime import datetime


DB_CONFIG = {
    "dbname": "echomind",
    "user": "postgres",
    "password": "Dwiti@1995",
    "host": "localhost",
    "port": "5432",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def save_message(user_id: str, role: str, content: str):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO conversation_memory (user_id, role, content, created_at)
    VALUES (%s, %s, %s, %s)
    """

    cursor.execute(query, (user_id, role, content, datetime.utcnow()))

    conn.commit()
    cursor.close()
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
