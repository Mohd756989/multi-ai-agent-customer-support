from langchain_huggingface import HuggingFaceEmbeddings


def get_embeddings():
    """Return a HuggingFace embeddings instance."""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode("Hello world")

print(len(embeddings))  # should print 384