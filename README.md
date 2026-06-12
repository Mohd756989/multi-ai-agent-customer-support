# NovaTech Support — Multi-Agent Customer Support AI

A production-ready, multi-agent AI customer support system built with **LangGraph**, **LangChain**, **FAISS**, and **GPT-4o-mini**. The system classifies incoming queries and routes them through specialist agents (FAQ, Order Tracking, Refund, Technical) before synthesising a final response via a generator agent.

---

## Architecture

```
User Query
    │
    ▼
Intent Classifier
    │
    ├──► FAQ Agent        ──┐
    ├──► Order Agent      ──┤
    ├──► Refund Agent     ──┼──► Generator Agent ──► Response
    └──► Technical Agent  ──┘
```

### Agents

| Agent | Responsibility |
|---|---|
| `intent_classifier` | Classifies query into `faq`, `order`, `refund`, `technical` |
| `faq_agent` | Retrieves FAQ docs via FAISS similarity search |
| `order_agent` | Looks up order status from SQLite database by order ID |
| `refund_agent` | Retrieves refund policy docs via FAISS similarity search |
| `technical_agent` | Retrieves troubleshooting docs via FAISS similarity search |
| `generator_agent` | Synthesises final response from retrieved context + history |
| `escalation_agent` | Generates a support ticket and hands off to human agents |

---

## Project Structure

```
multi-ai-customer-support/
├── app.py                      # CLI entry point
├── requirements.txt
├── .env                        # OPENAI_API_KEY goes here
│
├── agents/                     # Individual agent functions
│   ├── intent_classifier.py
│   ├── faq_agent.py
│   ├── order_agent.py
│   ├── refund_agent.py
│   ├── technical_agent.py
│   ├── generator_agent.py
│   └── escalation_agent.py
│
├── graph/                      # LangGraph workflow
│   ├── state.py                # SupportState TypedDict
│   ├── router.py               # Conditional routing logic
│   └── workflow.py             # StateGraph assembly
│
├── database/                   # SQLite order & conversation persistence
│   ├── order_repository.py
│   └── conversation_repository.py
│
├── rag/                        # RAG pipeline
│   ├── loader.py               # PDF loading
│   ├── splitter.py             # Chunking
│   ├── embeddings.py           # OpenAI embeddings
│   ├── vector_store.py         # FAISS store (create + load)
│   ├── retriever.py            # Retriever wrapper
│   └── ingest.py               # One-time ingestion script
│
├── data/                       # PDF knowledge base + FAISS index
│   ├── company_faq.pdf
│   ├── refund_policy.pdf
│   ├── troubleshooting.pdf
│   └── faiss_index/
│
├── llm/
│   └── model.py                # GPT-4o-mini singleton
│
├── prompts/                    # Prompt builders per agent
│   ├── intent_prompt.py
│   ├── faq_prompt.py
│   ├── refund_prompt.py
│   ├── technical_prompt.py
│   └── generator_prompt.py
│
├── memory/
│   ├── chat_memory.py          # LangGraph MemorySaver
│   └── sqlite_memory.py        # SQLite conversation persistence
│
├── tools/
│   ├── order_lookup.py
│   ├── ticket_generator.py
│   └── customer_lookup.py
│
├── utils/
│   ├── config.py               # .env loader
│   ├── logger.py               # Rotating file + console logger
│   └── helpers.py              # Utility functions
│
└── tests/                      # Pytest unit + integration tests
    ├── test_faq_agent.py
    ├── test_order_agent.py
    ├── test_refund_agent.py
    ├── test_technical_agent.py
    └── test_graph.py
```

---

## Setup

### 1. Clone & install dependencies

```bash
git clone https://github.com/your-username/multi-ai-customer-support.git
cd multi-ai-customer-support
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
OPENAI_API_KEY=sk-...
```

### 3. Add your PDFs

Place the following PDFs in the `data/` folder:
- `company_faq.pdf`
- `refund_policy.pdf`
- `troubleshooting.pdf`

### 4. Build the FAISS vector index

```bash
python -m rag.ingest
```

This reads all PDFs, chunks them, embeds with OpenAI, and saves the FAISS index to `data/faiss_index/`.

### 5. Run the CLI

```bash
python app.py
```

---

## Running Tests

```bash
pytest tests/ -v
```

All tests mock external dependencies (LLM, vector store, database) so no API key is needed for the test suite.

---

## Tech Stack

| Component | Technology |
|---|---|
| Agent Orchestration | LangGraph `StateGraph` |
| LLM | GPT-4o-mini (OpenAI) |
| Embeddings | OpenAI `text-embedding-ada-002` |
| Vector Store | FAISS (local) |
| Document Loading | LangChain `PyPDFLoader` |
| Conversation Memory | LangGraph `MemorySaver` + SQLite |
| Order Database | SQLite |
| Logging | Python `logging` (file + console) |

---

## Key Design Decisions

- **Modular agents**: Each agent is a pure function `(state) -> dict`, making them independently testable and swappable.
- **Singleton LLM & vector store**: Both are lazily initialised once per process to avoid redundant API calls and FAISS disk reads.
- **Pre-set response passthrough**: If a specialist agent (e.g. `order_agent`) resolves the query directly, `generator_agent` passes it through unchanged — no unnecessary LLM call.
- **Router as pure function**: Routing logic lives in `graph/router.py`, completely decoupled from LangGraph wiring in `workflow.py`.
