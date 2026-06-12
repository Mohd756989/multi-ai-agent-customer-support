from database.conversation_repository import save_conversation, get_conversation_history


class SQLiteMemory:
    """
    Thin wrapper around the conversation repository for persisting
    and replaying multi-turn conversation history per thread.
    """

    def __init__(self, thread_id: str):
        self.thread_id = thread_id

    def add(self, role: str, content: str) -> None:
        save_conversation(self.thread_id, role, content)

    def history(self) -> list[dict]:
        return get_conversation_history(self.thread_id)

    def formatted_history(self) -> str:
        turns = self.history()
        return "\n".join(f"{t['role'].capitalize()}: {t['content']}" for t in turns)
