"""
Custom FastAPI middleware:
  - RequestLoggingMiddleware  — logs method, path, status, and latency
  - RateLimitMiddleware       — simple in-memory rate limiter (60 req/min per IP)
"""

from __future__ import annotations
import time
import collections
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from utils.logger import get_logger

logger = get_logger(__name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log every request with method, path, status code, and elapsed time."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000

        logger.info(
            f"{request.method} {request.url.path} "
            f"→ {response.status_code} ({elapsed_ms:.1f}ms)"
        )
        response.headers["X-Response-Time"] = f"{elapsed_ms:.1f}ms"
        return response


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Allow up to `max_requests` requests per `window_seconds` per client IP.
    Returns HTTP 429 when exceeded.
    Health-check endpoint is exempt.
    """

    def __init__(self, app, max_requests: int = 60, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests   = max_requests
        self.window_seconds = window_seconds
        # {ip: deque of timestamps}
        self._store: dict[str, collections.deque] = {}

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Skip rate-limiting for health checks
        if request.url.path.endswith("/health"):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - self.window_seconds

        if client_ip not in self._store:
            self._store[client_ip] = collections.deque()

        timestamps = self._store[client_ip]

        # Drop timestamps outside the window
        while timestamps and timestamps[0] < window_start:
            timestamps.popleft()

        if len(timestamps) >= self.max_requests:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return Response(
                content='{"detail":"Rate limit exceeded. Try again in a minute."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": str(self.window_seconds),
                    "X-RateLimit-Limit": str(self.max_requests),
                    "X-RateLimit-Remaining": "0",
                },
            )

        timestamps.append(now)
        response = await call_next(request)
        response.headers["X-RateLimit-Limit"]     = str(self.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(self.max_requests - len(timestamps))
        return response
