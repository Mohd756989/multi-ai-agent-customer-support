import os
from langchain_groq import ChatGroq

_llm = None  # module-level singleton


def get_llm(model: str = "llama-3.3-70b-versatile", temperature: float = 0) -> ChatOpenAI:
    """Return a shared ChatOpenAI instance (lazy singleton)."""
    global _llm
    if _llm is None:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise EnvironmentError("GROQ_API_KEY is not set.")
        _llm = ChatGroq(model=model, temperature=temperature, api_key=api_key)
    return _llm
