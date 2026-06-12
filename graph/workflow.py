from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from graph.state import SupportState
from graph.router import router
from agents.intent_classifier import classify_intent
from agents.faq_agent import faq_agent
from agents.order_agent import order_agent
from agents.refund_agent import refund_agent
from agents.technical_agent import technical_agent
from agents.generator_agent import generator_agent


def build_graph():
    """Build and compile the LangGraph support workflow."""
    builder = StateGraph(SupportState)

    # Register nodes
    builder.add_node("intent_classifier", classify_intent)
    builder.add_node("faq_agent", faq_agent)
    builder.add_node("order_agent", order_agent)
    builder.add_node("refund_agent", refund_agent)
    builder.add_node("technical_agent", technical_agent)
    builder.add_node("generator_agent", generator_agent)

    # Entry point
    builder.set_entry_point("intent_classifier")

    # Conditional routing from intent classifier
    builder.add_conditional_edges(
        "intent_classifier",
        router,
        {
            "order_agent": "order_agent",
            "refund_agent": "refund_agent",
            "technical_agent": "technical_agent",
            "faq_agent": "faq_agent",
        },
    )

    # All specialist agents feed into generator
    for agent in ["order_agent", "refund_agent", "technical_agent", "faq_agent"]:
        builder.add_edge(agent, "generator_agent")

    builder.add_edge("generator_agent", END)

    memory = MemorySaver()
    return builder.compile(checkpointer=memory)
