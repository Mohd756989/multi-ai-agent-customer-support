import sqlite3
import os
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")


def _get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            thread_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def save_conversation(thread_id: str, role: str, content: str) -> None:
    """Persist a single conversation turn."""
    try:
        conn = _get_connection()
        conn.execute(
            "INSERT INTO conversations (thread_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (thread_id, role, content, datetime.utcnow().isoformat()),
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to save conversation turn: {e}")


def get_conversation_history(thread_id: str) -> list[dict]:
    """Retrieve all turns for a given thread_id, ordered by time."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM conversations WHERE thread_id = ? ORDER BY id ASC",
            (thread_id,),
        )
        rows = cursor.fetchall()
        conn.close()
        return [{"role": r[0], "content": r[1], "timestamp": r[2]} for r in rows]
    except sqlite3.Error as e:
        logger.error(f"Failed to fetch conversation history: {e}")
        return []
