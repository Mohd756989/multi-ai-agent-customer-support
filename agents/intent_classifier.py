from graph.state import SupportState
from llm.model import get_llm
from prompts.intent_prompt import build_intent_prompt
from utils.logger import get_logger

logger = get_logger(__name__)



def classify_intent(state: SupportState) -> dict:
    """Classify the user query into one of: faq, refund, order, technical."""
    llm = get_llm()
    query = state["messages"][-1].content
    prompt = build_intent_prompt(query)

    result = llm.invoke(prompt)
    intent = result.content.strip().lower()

    logger.info(f"Classified intent: '{intent}' for query: '{query[:60]}'")
    return {"intent": intent}
