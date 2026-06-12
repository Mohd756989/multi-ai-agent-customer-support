"""
GET /api/v1/conversations/{thread_id}  — fetch conversation history
DELETE /api/v1/conversations/{thread_id}  — clear a conversation thread
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException
import sqlite3
import os

from api.schemas import ConversationHistoryResponse, ConversationTurn
from database.conversation_repository import get_conversation_history
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "database", "orders.db")


@router.get(
    "/conversations/{thread_id}",
    response_model=ConversationHistoryResponse,
    summary="Retrieve full conversation history for a thread",
)
async def get_history(thread_id: str) -> ConversationHistoryResponse:
    turns = get_conversation_history(thread_id)
    if not turns:
        raise HTTPException(
            status_code=404,
            detail=f"No conversation found for thread_id '{thread_id}'",
        )
    return ConversationHistoryResponse(
        thread_id=thread_id,
        turns=[ConversationTurn(**t) for t in turns],
        total=len(turns),
    )


@router.delete(
    "/conversations/{thread_id}",
    summary="Delete all messages in a conversation thread",
    responses={
        200: {"description": "Thread deleted successfully"},
        404: {"description": "Thread not found"},
    },
)
async def delete_thread(thread_id: str) -> dict:
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "DELETE FROM conversations WHERE thread_id = ?", (thread_id,)
        )
        deleted = cursor.rowcount
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        logger.error(f"Failed to delete thread {thread_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    if deleted == 0:
        raise HTTPException(
            status_code=404,
            detail=f"Thread '{thread_id}' not found or already empty",
        )

    logger.info(f"Deleted {deleted} messages from thread {thread_id}")
    return {"thread_id": thread_id, "deleted_messages": deleted}
