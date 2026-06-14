"""
POST /api/v1/chat  — main multi-agent conversation endpoint
"""

from __future__ import annotations
import traceback
import uuid
from fastapi import APIRouter, Depends, HTTPException
from langchain_core.messages import HumanMessage

from api.schemas import ChatRequest, ChatResponse, RetrievedDoc
from api.dependencies import require_graph
from database.conversation_repository import save_conversation
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send a message to the support agent",
    description=(
        "Routes the customer query through the LangGraph multi-agent pipeline "
        "(intent classification → specialist agent → response generator) and "
        "returns a structured response with the detected intent and any retrieved documents."
    ),
)
async def chat(
    request: ChatRequest,
    graph=Depends(require_graph),
) -> ChatResponse:
    thread_id = request.thread_id or str(uuid.uuid4())
    config    = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "query":         request.query,
        "intent":        "",
        "docs":          [],
        "retrieved_docs": [],
        "customer_data": {},
        "response":      "",
        "escalation":    False,
        "customer_id":   request.customer_id or "",
        "messages":      [HumanMessage(content=request.query)],
    }

    try:
        result = graph.invoke(initial_state, config=config)
    except FileNotFoundError as e:
        if "faiss" in str(e).lower():
            raise HTTPException(
                status_code=503,
                detail="Knowledge base index not found. Run `python -m rag.ingest` first.",
            )
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Agent error for thread {thread_id}: {e}")
        logger.error(f"FULL TRACEBACK:\n{traceback.format_exc()}") 
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")

    # Persist both turns
    save_conversation(thread_id, "user",  request.query)
    save_conversation(thread_id, "agent", result.get("response", ""))

    # Serialise retrieved docs
    raw_docs = result.get("docs", [])
    retrieved_docs = [
        RetrievedDoc(
            content=doc.page_content[:300],
            source=str(doc.metadata.get("source", "knowledge base")),
            page=doc.metadata.get("page"),
        )
        for doc in raw_docs
    ]

    return ChatResponse(
        response=result.get("response", ""),
        intent=result.get("intent", "faq"),
        thread_id=thread_id,
        retrieved_docs=retrieved_docs,
        ticket_id=result.get("ticket_id"),
        escalated=bool(result.get("escalation_required", False)),
    )
