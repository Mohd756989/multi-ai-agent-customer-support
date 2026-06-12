from langchain_openai import OpenAIEmbeddings


def get_embeddings() -> OpenAIEmbeddings:
    """Return an OpenAI embeddings instance."""
    return OpenAIEmbeddings()
