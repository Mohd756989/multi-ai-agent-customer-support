"""
GET /api/v1/orders/{order_id}   — fetch a single order
GET /api/v1/orders              — list orders (with limit)
"""

from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query

from api.schemas import OrderResponse, OrderListResponse
from database.order_repository import get_order, list_orders
from utils.logger import get_logger

router = APIRouter()
logger = get_logger(__name__)


@router.get(
    "/orders/{order_id}",
    response_model=OrderResponse,
    summary="Look up a single order by order ID",
)
async def fetch_order(order_id: str) -> OrderResponse:
    order = get_order(order_id)
    if not order:
        raise HTTPException(
            status_code=404,
            detail=f"Order '{order_id}' not found",
        )
    logger.info(f"Order fetched via API: {order_id}")
    return OrderResponse(**order)


@router.get(
    "/orders",
    response_model=OrderListResponse,
    summary="List recent orders",
)
async def fetch_orders(
    limit: int = Query(default=20, ge=1, le=100, description="Max number of orders to return"),
) -> OrderListResponse:
    orders = list_orders(limit=limit)
    return OrderListResponse(
        orders=[OrderResponse(**o) for o in orders],
        total=len(orders),
    )
