from langchain_core.messages import AIMessage
from graph.state import SupportState
from llm.model import get_llm
from prompts.generator_prompt import build_generator_prompt
from utils.logger import get_logger

logger = get_logger(__name__)
llm = get_llm()


def generator_agent(state: SupportState) -> dict:
    """
    Generate the final response.
    If a specialist agent (e.g. order_agent) already set state['response'],
    use it directly. Otherwise synthesize from retrieved docs and history.
    """
    if state.get("response"):
        content = state["response"]
        logger.info("Generator using pre-set response from specialist agent")
    else:
        history = "\n".join([msg.content for msg in state["messages"]])
        context = "\n".join([doc.page_content for doc in state.get("docs", [])])
        prompt = build_generator_prompt(history, context)
        response_obj = llm.invoke(prompt)
        content = response_obj.content
        logger.info("Generator synthesised response from docs")

    return {
        "response": content,
        "messages": [AIMessage(content=content)],
    }
