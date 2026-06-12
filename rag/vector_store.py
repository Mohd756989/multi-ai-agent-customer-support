import os
from langchain_community.vectorstores import FAISS
from rag.embeddings import get_embeddings
from utils.logger import get_logger

logger = get_logger(__name__)

FAISS_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "faiss_index")

_vector_store = None  # module-level singleton


def create_vector_store(chunks: list) -> FAISS:
    """
    Build a FAISS vector store from document chunks and persist it to disk.
    Call this once during initial ingestion.
    """
    global _vector_store
    embeddings = get_embeddings()
    _vector_store = FAISS.from_documents(chunks, embeddings)
    _vector_store.save_local(FAISS_INDEX_PATH)
    logger.info(f"Vector store created and saved to {FAISS_INDEX_PATH}")
    return _vector_store


def get_vector_store() -> FAISS:
    """
    Load the FAISS vector store from disk (lazy singleton).
    Raises FileNotFoundError if the index has not been built yet.
    """
    global _vector_store
    if _vector_store is not None:
        return _vector_store

    if not os.path.exists(FAISS_INDEX_PATH):
        raise FileNotFoundError(
            f"FAISS index not found at '{FAISS_INDEX_PATH}'. "
            "Run rag/ingest.py first to build the vector store."
        )

    embeddings = get_embeddings()
    _vector_store = FAISS.load_local(
        FAISS_INDEX_PATH,
        embeddings,
        allow_dangerous_deserialization=True,
    )
    logger.info(f"Vector store loaded from {FAISS_INDEX_PATH}")
    return _vector_store
