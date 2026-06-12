"""
GET /api/v1/health  — liveness + dependency health check
"""

from __future__ import annotations
from fastapi import APIRouter

from api.schemas import HealthResponse
from api.dependencies import check_vector_store, check_database

router = APIRouter()

API_VERSION = "1.0.0"


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="API health check",
    description="Returns the health status of the API and its key dependencies.",
)
async def health_check() -> HealthResponse:
    return HealthResponse(
        status="ok",
        version=API_VERSION,
        vector_store=check_vector_store(),
        database=check_database(),
    )
