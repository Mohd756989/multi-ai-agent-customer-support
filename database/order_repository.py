import sqlite3
import os
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "orders.db")


def _get_connection():
    return sqlite3.connect(DB_PATH)


def get_order(order_id: str) -> dict | None:
    """Fetch a single order by order_id. Returns a dict or None if not found."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        result = cursor.fetchone()
        conn.close()

        if result is None:
            return None

        return {
            "order_id": result[0],
            "customer_name": result[1],
            "status": result[5],
            "expected_delivery": result[7],
        }
    except sqlite3.Error as e:
        logger.error(f"Database error fetching order {order_id}: {e}")
        return None


def list_orders(limit: int = 50) -> list[dict]:
    """Return up to `limit` orders as a list of dicts."""
    try:
        conn = _get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM orders LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "order_id": r[0],
                "customer_name": r[1],
                "status": r[5],
                "expected_delivery": r[7],
            }
            for r in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"Database error listing orders: {e}")
        return []
