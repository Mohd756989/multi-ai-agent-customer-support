from graph.state import SupportState
from rag.vector_store import get_vector_store
from utils.logger import get_logger

logger = get_logger(__name__)


def technical_agent(state: SupportState) -> dict:
    """Retrieve troubleshooting documents from the vector store."""
    logger.info("Technical agent running")
    vector_store = get_vector_store()
    docs = vector_store.similarity_search(state["query"], k=5)
    return {"docs": docs}
