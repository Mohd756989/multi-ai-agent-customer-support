import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage
from agents.technical_agent import technical_agent


@patch("agents.technical_agent.get_vector_store")
def test_technical_agent_returns_docs(mock_vs):
    mock_doc = MagicMock()
    mock_doc.page_content = "Try restarting the device and checking the power cable."
    mock_vs.return_value.similarity_search.return_value = [mock_doc]

    state = {
        "query": "My device won't turn on",
        "messages": [HumanMessage(content="My device won't turn on")],
        "docs": [],
    }

    result = technical_agent(state)
    assert "docs" in result
    assert len(result["docs"]) > 0
