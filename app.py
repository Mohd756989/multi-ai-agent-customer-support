import uuid
from langchain_core.messages import HumanMessage
from graph.workflow import build_graph
from utils.config import load_env
from utils.logger import get_logger

logger = get_logger(__name__)


def main():
    load_env(override=False)
    graph = build_graph()

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("\n🤖 NovaTech Support Agent is ready! (type 'exit' to quit)\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        state = {
            "query": query,
            "intent": "",
            "docs": [],
            "retrieved_docs": [],
            "customer_data": {},
            "response": "",
            "escalation": False,
            "messages": [HumanMessage(content=query)],
        }

        try:
            result = graph.invoke(state, config=config)
            print(f"\nAgent: {result['response']}\n")
            logger.info(f"Query: {query} | Intent: {result.get('intent')} | Response: {result['response'][:80]}...")
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print(f"\nAgent: Sorry, I encountered an error. Please try again.\n")


if __name__ == "__main__":
    main()
