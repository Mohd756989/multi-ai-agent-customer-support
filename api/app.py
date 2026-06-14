"""
FastAPI application factory.
Creates the app, registers routers, middleware, and exception handlers.
"""

from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from api.middleware import RequestLoggingMiddleware, RateLimitMiddleware
from api.routes import chat, conversations, orders, tickets, health
from utils.config import load_env
from utils.logger import get_logger

logger = get_logger(__name__)

API_PREFIX = "/api/v1"


def create_app() -> FastAPI:
    load_env(override=False)  # Load environment variables from .env file

    app = FastAPI(
        title="NovaTech Support API",
        description=(
            "REST API for the NovaTech multi-agent AI customer support system. "
            "Routes customer queries through a LangGraph pipeline of specialist agents "
            "(FAQ, Order Tracking, Refund, Technical) backed by a FAISS RAG knowledge base."
        ),
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # ── Middleware (order matters — outermost first) ──────────────────────
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # tighten in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(RateLimitMiddleware, max_requests=60, window_seconds=60)
    app.add_middleware(RequestLoggingMiddleware)

    # ── Routers ──────────────────────────────────────────────────────────
    app.include_router(health.router,        prefix=API_PREFIX, tags=["Health"])
    app.include_router(chat.router,          prefix=API_PREFIX, tags=["Chat"])
    app.include_router(conversations.router, prefix=API_PREFIX, tags=["Conversations"])
    app.include_router(orders.router,        prefix=API_PREFIX, tags=["Orders"])
    app.include_router(tickets.router,       prefix=API_PREFIX, tags=["Tickets"])

    # ── Global exception handlers ─────────────────────────────────────────
    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled exception on {request.url.path}: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "An unexpected error occurred. Check the server logs."},
        )

    @app.on_event("startup")
    async def startup():
        logger.info("NovaTech Support API starting up…")

    @app.on_event("shutdown")
    async def shutdown():
        logger.info("NovaTech Support API shutting down.")

    return app
