from langchain_openai import ChatOpenAI
import os

_llm = None  # module-level singleton


def get_llm(model: str = "gpt-4o-mini", temperature: float = 0) -> ChatOpenAI:
    """Return a shared ChatOpenAI instance (lazy singleton)."""
    global _llm
    if _llm is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise EnvironmentError("OPENAI_API_KEY is not set.")
        _llm = ChatOpenAI(model=model, temperature=temperature, api_key=api_key)
    return _llm