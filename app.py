import uuid
from langchain_core.messages import HumanMessage
from graph.workflow import build_graph
from utils.config import load_env
from utils.logger import get_logger
from memory.long_term_memory import LongTermMemory

logger = get_logger(__name__)


def main():
    load_env()
    graph = build_graph()

    # Persistent memory store
    memory = LongTermMemory()

    # Fixed user id (replace with actual login/customer id)
    user_id = "customer_123"

    print("\n🤖 NovaTech Support Agent is ready! (type 'exit' to quit)\n")

    while True:
        query = input("You: ").strip()

        if query.lower() == "exit":
            print("Goodbye!")
            break

        if not query:
            continue

        # Retrieve old memories
        past_memories = memory.retrieve_memory(query, user_id=user_id)

        state = {
            "query": query,
            "intent": "",
            "docs": [],
            "retrieved_docs": [],
            "customer_data": {},
            "memory": past_memories,   # Long-term memory injected here
            "response": "",
            "escalation": False,
            "messages": [HumanMessage(content=query)],
        }

        try:
            result = graph.invoke(state)

            print(f"\nAgent: {result['response']}\n")

            # Save important conversation to long-term memory
            memory.save_memory(
                user_id=user_id,
                text=f"User: {query} | Agent: {result['response']}"
            )

            logger.info(
                f"Query: {query} | Intent: {result.get('intent')} | Response: {result['response'][:80]}..."
            )

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            print("\nAgent: Sorry, I encountered an error. Please try again.\n")


if __name__ == "__main__":
    main()