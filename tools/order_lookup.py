from database.order_repository import get_order


def lookup_order(order_id: str) -> dict | None:
    """Tool wrapper: fetch order details by order ID."""
    return get_order(order_id)
