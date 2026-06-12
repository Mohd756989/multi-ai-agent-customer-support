from langchain_community.document_loaders import PyPDFLoader
from utils.logger import get_logger

logger = get_logger(__name__)


def load_pdf(pdf_path: str) -> list:
    """Load a PDF file and return a list of LangChain Document objects."""
    logger.info(f"Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    logger.info(f"Loaded {len(docs)} pages from {pdf_path}")
    return docs
