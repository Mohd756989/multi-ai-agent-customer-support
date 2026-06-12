import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage


@patch("agents.intent_classifier.get_llm")
@patch("agents.faq_agent.get_vector_store")
@patch("agents.generator_agent.get_llm")
def test_graph_faq_flow(mock_gen_llm, mock_vs, mock_intent_llm):
    """FAQ intent should route through faq_agent -> generator_agent."""
    from graph.workflow import build_graph

    # Mock intent classification → "faq"
    mock_intent_llm.return_value.invoke.return_value = MagicMock(content="faq")

    # Mock vector store docs
    mock_doc = MagicMock()
    mock_doc.page_content = "NovaTech ships within 3-5 business days."
    mock_vs.return_value.similarity_search.return_value = [mock_doc]

    # Mock generator response
    mock_gen_llm.return_value.invoke.return_value = MagicMock(
        content="We ship within 3-5 business days."
    )

    graph = build_graph()
    config = {"configurable": {"thread_id": "test-faq-001"}}

    result = graph.invoke(
        {
            "query": "How long does shipping take?",
            "messages": [HumanMessage(content="How long does shipping take?")],
            "docs": [],
            "response": "",
        },
        config=config,
    )

    assert result["intent"] == "faq"
    assert result["response"] != ""


@patch("agents.intent_classifier.get_llm")
@patch("agents.order_agent.get_order")
@patch("agents.generator_agent.get_llm")
def test_graph_order_flow(mock_gen_llm, mock_get_order, mock_intent_llm):
    """Order intent should route through order_agent -> generator_agent."""
    from graph.workflow import build_graph

    mock_intent_llm.return_value.invoke.return_value = MagicMock(content="order")
    mock_get_order.return_value = {
        "order_id": "7890",
        "customer_name": "Bob",
        "status": "delivered",
        "expected_delivery": "2025-06-01",
    }
    mock_gen_llm.return_value.invoke.return_value = MagicMock(content="Your order was delivered.")

    graph = build_graph()
    config = {"configurable": {"thread_id": "test-order-001"}}

    result = graph.invoke(
        {
            "query": "What is the status of order 7890?",
            "messages": [HumanMessage(content="What is the status of order 7890?")],
            "docs": [],
            "response": "",
        },
        config=config,
    )

    assert result["intent"] == "order"
    assert "delivered" in result["response"].lower() or result["response"] != ""


@patch("agents.intent_classifier.get_llm")
@patch("agents.refund_agent.get_vector_store")
@patch("agents.generator_agent.get_llm")
def test_graph_refund_flow(mock_gen_llm, mock_vs, mock_intent_llm):
    """Refund intent should route through refund_agent -> generator_agent."""
    from graph.workflow import build_graph

    mock_intent_llm.return_value.invoke.return_value = MagicMock(content="refund")
    mock_doc = MagicMock()
    mock_doc.page_content = "Refunds processed in 5-7 business days."
    mock_vs.return_value.similarity_search.return_value = [mock_doc]
    mock_gen_llm.return_value.invoke.return_value = MagicMock(
        content="Refunds take 5-7 business days."
    )

    graph = build_graph()
    config = {"configurable": {"thread_id": "test-refund-001"}}

    result = graph.invoke(
        {
            "query": "How do I request a refund?",
            "messages": [HumanMessage(content="How do I request a refund?")],
            "docs": [],
            "response": "",
        },
        config=config,
    )

    assert result["intent"] == "refund"
    assert result["response"] != ""
