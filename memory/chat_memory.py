from langgraph.checkpoint.memory import MemorySaver

_memory = None


def get_chat_memory() -> MemorySaver:
    """Return a shared in-memory MemorySaver (LangGraph checkpointer)."""
    global _memory
    if _memory is None:
        _memory = MemorySaver()
    return _memory
