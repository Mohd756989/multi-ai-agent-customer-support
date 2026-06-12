import re
from graph.state import SupportState
from database.order_repository import get_order
from utils.logger import get_logger

logger = get_logger(__name__)


def order_agent(state: SupportState) -> dict:
    """Look up order status from the database using an order ID found in the query."""
    query = state["query"]
    match = re.search(r"\d+", query)

    if not match:
        logger.info("No order ID found in query")
        return {"response": "Please provide your order ID so I can look it up for you."}

    order_id = match.group()
    order = get_order(order_id)

    if not order:
        logger.info(f"Order not found: {order_id}")
        return {"response": f"I couldn't find any order with ID {order_id}. Please double-check the number."}

    response = (
        f"Order {order['order_id']} for {order['customer_name']} "
        f"is currently **{order['status']}**. "
        f"Expected delivery: {order['expected_delivery']}."
    )
    logger.info(f"Order {order_id} found, status: {order['status']}")
    return {"response": response}
