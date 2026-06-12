import pytest
from unittest.mock import patch
from langchain_core.messages import HumanMessage
from agents.order_agent import order_agent


@patch("agents.order_agent.get_order")
def test_order_agent_found(mock_get_order):
    mock_get_order.return_value = {
        "order_id": "12345",
        "customer_name": "Alice",
        "status": "shipped",
        "expected_delivery": "2025-07-01",
    }

    state = {"query": "Where is my order 12345?", "messages": [HumanMessage(content="Where is my order 12345?")]}
    result = order_agent(state)
    assert "shipped" in result["response"]
    assert "12345" in result["response"]


@patch("agents.order_agent.get_order")
def test_order_agent_not_found(mock_get_order):
    mock_get_order.return_value = None
    state = {"query": "Track order 99999", "messages": []}
    result = order_agent(state)
    assert "99999" in result["response"] or "not find" in result["response"].lower()


def test_order_agent_no_id():
    state = {"query": "Where is my package?", "messages": []}
    result = order_agent(state)
    assert "order ID" in result["response"] or "provide" in result["response"].lower()
