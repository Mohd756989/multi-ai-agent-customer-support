import uuid
from utils.logger import get_logger

logger = get_logger(__name__)


def generate_ticket(query: str, customer_id: str = "") -> str:
    """
    Generate a unique support ticket ID and log the escalation.
    Returns the ticket ID string.
    """
    ticket_id = f"TKT-{uuid.uuid4().hex[:8].upper()}"
    logger.info(f"Support ticket created: {ticket_id} | customer: {customer_id} | query: {query[:80]}")
    return ticket_id
