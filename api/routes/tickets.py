"""
POST /api/v1/tickets  — manually raise a support ticket (escalation)
"""

from __future__ import annotations
from fastapi import APIRouter

from api.schemas import TicketRequest, TicketResponse
from tools.ticket_generator import generate_ticket
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.post(
    "/tickets",
    response_model=TicketResponse,
    summary="Manually raise a support escalation ticket",
    description=(
        "Creates a new support ticket and returns the generated ticket ID. "
        "Used when the agent cannot resolve the issue automatically."
    ),
)
async def create_ticket(request: TicketRequest) -> TicketResponse:
    ticket_id = generate_ticket(
        query=request.query,
        customer_id=request.customer_id or "",
    )
    logger.info(f"Manual ticket raised via API: {ticket_id}")
    return TicketResponse(
        ticket_id=ticket_id,
        message=(
            f"Support ticket {ticket_id} has been raised. "
            "A team member will reach out within 24 hours."
        ),
    )
