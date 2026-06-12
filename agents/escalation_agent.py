from graph.state import SupportState
from tools.ticket_generator import generate_ticket
from utils.logger import get_logger

logger = get_logger(__name__)


def escalation_agent(state: SupportState) -> dict:
    """
    Escalate unresolved queries to a human agent.
    Generates a support ticket and returns an acknowledgement response.
    """
    logger.info("Escalation agent triggered")
    ticket_id = generate_ticket(state.get("query", ""), state.get("customer_id", ""))

    response = (
        f"I'm escalating your issue to our support team. "
        f"Your ticket ID is **{ticket_id}**. "
        f"A team member will reach out within 24 hours."
    )

    return {
        "response": response,
        "ticket_id": ticket_id,
        "escalation_required": True,
    }
