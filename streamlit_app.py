import uuid
import streamlit as st

from langchain_core.messages import HumanMessage

from graph.workflow import build_graph
from utils.config import load_env

# Load environment variables
load_env()

# Build graph only once
@st.cache_resource
def get_graph():
    return build_graph()

graph = get_graph()

# Page Config
st.set_page_config(
    page_title="NovaTech Support Agent",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 NovaTech Support Agent")

# Create session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

config = {
    "configurable": {
        "thread_id": st.session_state.thread_id
    }
}

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
prompt = st.chat_input("Ask me anything...")

if prompt:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            state = {
                "query": prompt,
                "intent": "",
                "docs": [],
                "retrieved_docs": [],
                "customer_data": {},
                "response": "",
                "escalation": False,
                "messages": [
                    HumanMessage(content=prompt)
                ],
            }

            try:

                result = graph.invoke(
                    state,
                    config=config
                )

                response = result["response"]

                st.markdown(response)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response
                    }
                )

            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.error(error_msg)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": error_msg
                    }
                )
with st.sidebar:

    st.header("⚙️ Settings")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.write("Thread ID")
    st.code(st.session_state.thread_id)

    st.divider()

    st.write("NovaTech AI Support")