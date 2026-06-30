from typing import TypedDict, List, Annotated
from langchain_core.documents import Document
from langgraph.graph.message import add_messages


class SupportState(TypedDict):
    query: str
    chat_history: list
    intent: str
    sentiment: str
    messages: Annotated[list, add_messages]
    retrieved_docs: list
    customer_info: dict
    response: str
    memory:str
    confidence: float
    ticket_id: str
    customer_id: str
    docs: List[Document]
    conversation_history: List[str]
    escalation_required: bool
