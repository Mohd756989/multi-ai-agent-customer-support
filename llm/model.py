from langchain_openai import ChatOpenAI
import os
_llm = None  # module-level singleton

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
def get_llm(model: str = "gpt-4o-mini", temperature: float = 0) -> ChatOpenAI:
    """Return a shared ChatOpenAI instance (lazy singleton)."""
    global _llm
    if _llm is None:
        _llm = ChatOpenAI(model=model, temperature=temperature,api_key=os.getenv("OPENAI_API_KEY"))
    return _llm
