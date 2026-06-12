import pytest
from unittest.mock import MagicMock, patch
from langchain_core.messages import HumanMessage
from agents.faq_agent import faq_agent


@patch("agents.faq_agent.get_vector_store")
def test_faq_agent_returns_docs(mock_vs):
    mock_doc = MagicMock()
    mock_doc.page_content = "NovaTech return window is 30 days."
    mock_vs.return_value.similarity_search.return_value = [mock_doc]

    state = {
        "query": "What is the return policy?",
        "messages": [HumanMessage(content="What is the return policy?")],
        "docs": [],
    }

    result = faq_agent(state)
    assert "docs" in result
    assert len(result["docs"]) == 1
    assert "30 days" in result["docs"][0].page_content
