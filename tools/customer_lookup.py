import sqlite3
import os
from utils.logger import get_logger

logger = get_logger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "orders.db")


def lookup_customer(customer_id: str) -> dict | None:
    """
    Look up basic customer info by customer_id.
    Returns a dict or None if not found.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT customer_id, customer_name, email FROM customers WHERE customer_id = ?",
            (customer_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return None
        return {"customer_id": row[0], "customer_name": row[1], "email": row[2]}
    except sqlite3.Error as e:
        logger.error(f"Customer lookup error for {customer_id}: {e}")
        return None
