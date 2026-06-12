"""
Pydantic schemas for all API request and response payloads.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


# ── Chat ────────────────────────────────────────────────────────────────────

class ChatRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000, description="Customer message")
    thread_id: Optional[str] = Field(
        None,
        description="Conversation thread ID. Omit to start a new conversation.",
    )
    customer_id: Optional[str] = Field(None, description="Optional customer identifier")


class RetrievedDoc(BaseModel):
    content: str
    source: str
    page: Optional[int] = None


class ChatResponse(BaseModel):
    response: str
    intent: str
    thread_id: str
    retrieved_docs: List[RetrievedDoc] = []
    ticket_id: Optional[str] = None
    escalated: bool = False
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Conversation history ─────────────────────────────────────────────────────

class ConversationTurn(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None


class ConversationHistoryResponse(BaseModel):
    thread_id: str
    turns: List[ConversationTurn]
    total: int


# ── Orders ───────────────────────────────────────────────────────────────────

class OrderResponse(BaseModel):
    order_id: str
    customer_name: str
    status: str
    expected_delivery: Optional[str] = None


class OrderListResponse(BaseModel):
    orders: List[OrderResponse]
    total: int


# ── Tickets ──────────────────────────────────────────────────────────────────

class TicketRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=2000)
    customer_id: Optional[str] = None


class TicketResponse(BaseModel):
    ticket_id: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ── Health ───────────────────────────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    vector_store: str
    database: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
