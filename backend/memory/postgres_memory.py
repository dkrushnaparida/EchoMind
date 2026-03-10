import psycopg
from backend.core.config import config
from backend.core.logger import get_logger

logger = get_logger(__name__)


class PostgresMemory:

    def __init__(self):
        self.conn = psycopg.connect(config.postgres_url)

    def save_message(self, session_id: str, role: str, message: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO chat_history (session_id, role, message)
                    VALUES (%s, %s, %s)
                    """,
                    (session_id, role, message),
                )
                self.conn.commit()
        except Exception as e:
            logger.error(f"Memory save failed: {e}")

    def load_history(self, session_id: str):
        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT role, message
                    FROM chat_history
                    WHERE session_id = %s
                    ORDER BY created_at ASC
                    """,
                    (session_id,),
                )

                rows = cur.fetchall()
                history = [{"role": role, "content": message} for role, message in rows]

                return history

        except Exception as e:
            logger.error(f"Memory load failed: {e}")
            return []
