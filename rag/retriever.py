from rag.vector_store import get_vector_store
from utils.logger import get_logger

logger = get_logger(__name__)


def get_retriever(k: int = 5):
    """Return a LangChain retriever backed by the FAISS vector store."""
    vector_store = get_vector_store()
    return vector_store.as_retriever(search_kwargs={"k": k})


def retrieve(query: str, k: int = 5) -> list:
    """Run a similarity search and return the top-k documents."""
    retriever = get_retriever(k=k)
    docs = retriever.invoke(query)
    logger.info(f"Retrieved {len(docs)} docs for query: '{query[:60]}'")
    return docs
