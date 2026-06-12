from graph.state import SupportState
from utils.logger import get_logger

logger = get_logger(__name__)


def router(state: SupportState) -> str:
    """Route to the appropriate agent based on classified intent."""
    intent = state["intent"]
    logger.info(f"Routing intent: {intent}")

    if intent == "order":
        return "order_agent"

    if intent == "refund":
        return "refund_agent"

    if intent == "technical":
        return "technical_agent"

    return "faq_agent"
