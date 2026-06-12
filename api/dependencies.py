"""
FastAPI dependency injection — graph singleton, DB checks.
"""

from __future__ import annotations
import os
from functools import lru_cache
from fastapi import HTTPException

from graph.workflow import build_graph
from utils.logger import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def get_graph():
    """
    Build and cache the LangGraph workflow once per process.
    Raises HTTP 503 if initialisation fails.
    """
    try:
        graph = build_graph()
        logger.info("LangGraph workflow initialised")
        return graph
    except Exception as e:
        logger.error(f"Failed to build graph: {e}")
        raise HTTPException(
            status_code=503,
            detail=f"Support agents unavailable: {str(e)}",
        )


def require_graph():
    """Dependency that yields the compiled graph or raises 503."""
    return get_graph()


def check_vector_store() -> str:
    """Return 'ok' or an error string describing the FAISS index state."""
    faiss_path = os.path.join("data", "faiss_index", "index.faiss")
    return "ok" if os.path.exists(faiss_path) else "index not found — run python -m rag.ingest"


def check_database() -> str:
    """Return 'ok' or an error string describing the SQLite DB state."""
    db_path = os.path.join("database", "orders.db")
    return "ok" if os.path.exists(db_path) else "orders.db not found"
