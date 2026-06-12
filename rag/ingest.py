"""
Run this script once to ingest the PDF knowledge base and build the FAISS index.

    python -m rag.ingest

PDFs expected in data/:
    - company_faq.pdf
    - refund_policy.pdf
    - troubleshooting.pdf
"""

import os
from rag.loader import load_pdf
from rag.splitter import create_chunks
from rag.vector_store import create_vector_store
from utils.config import load_env
from utils.logger import get_logger

logger = get_logger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

PDF_FILES = [
    "company_faq.pdf",
    "refund_policy (1).pdf",
    "troubleshooting.pdf",
    "user_manual.pdf",
    "account_faq.pdf"
]


def ingest():
    load_env()

    all_docs = []
    for filename in PDF_FILES:
        path = os.path.join(DATA_DIR, filename)
        if not os.path.exists(path):
            logger.warning(f"PDF not found, skipping: {path}")
            continue
        docs = load_pdf(path)
        all_docs.extend(docs)
        logger.info(f"Loaded {len(docs)} pages from {filename}")

    if not all_docs:
        logger.error("No documents loaded. Aborting ingestion.")
        return

    chunks = create_chunks(all_docs)
    logger.info(f"Total chunks: {len(chunks)}")

    create_vector_store(chunks)
    logger.info("✅ FAISS index built and saved successfully.")


if __name__ == "__main__":
    ingest()
