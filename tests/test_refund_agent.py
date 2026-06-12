import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage
from agents.refund_agent import refund_agent


@patch("agents.refund_agent.get_vector_store")
def test_refund_agent_returns_docs(mock_vs):
    mock_doc = MagicMock()
    mock_doc.page_content = "Refunds are processed within 5-7 business days."
    mock_vs.return_value.similarity_search.return_value = [mock_doc]

    state = {
        "query": "How do I get a refund?",
        "messages": [HumanMessage(content="How do I get a refund?")],
        "docs": [],
    }

    result = refund_agent(state)
    assert "docs" in result
    assert len(result["docs"]) > 0
