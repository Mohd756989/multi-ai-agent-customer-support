"""
NovaTech Support — Streamlit UI (API-backed)
Calls the FastAPI backend at API_BASE_URL for all agent interactions.

Run backend first:   python api_server.py
Run UI:              streamlit run streamlit_app.py
"""

import uuid
import os
import httpx
import streamlit as st
from datetime import datetime

# ── Config ───────────────────────────────────────────────────────────────────
API_BASE_URL = "https://multi-ai-agent.up.railway.app/api/v1" # <-- UPDATE if your API is hosted elsewhere
REQUEST_TIMEOUT = 60  # seconds — agent pipeline can take a moment

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NovaTech Support",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-base:       #0D0F14;
    --bg-surface:    #13161E;
    --bg-card:       #1A1D27;
    --bg-input:      #1E2130;
    --border:        #2A2E3E;
    --border-soft:   #222536;
    --accent:        #6C63FF;
    --accent-glow:   rgba(108,99,255,0.18);
    --accent-muted:  rgba(108,99,255,0.12);
    --text-primary:  #E8EAF0;
    --text-secondary:#8B90A7;
    --text-muted:    #52566A;
    --user-bubble:   #1E2347;
    --agent-bubble:  #161921;
    --radius:        12px;
    --radius-sm:     8px;
}
html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg-base) !important;
    font-family: 'Inter', sans-serif;
    color: var(--text-primary);
}
[data-testid="stSidebar"] {
    background-color: var(--bg-surface) !important;
    border-right: 1px solid var(--border);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 1.5rem; }
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.main .block-container { padding: 0 !important; max-width: 100% !important; }

.nt-header {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 32px;
    border-bottom: 1px solid var(--border);
    background: var(--bg-surface);
    position: sticky; top: 0; z-index: 100;
}
.nt-logo {
    width: 36px; height: 36px; background: var(--accent);
    border-radius: 10px; display: flex; align-items: center;
    justify-content: center; font-size: 18px; font-weight: 700;
    color: #fff; box-shadow: 0 0 16px var(--accent-glow);
}
.nt-header-title { font-size: 16px; font-weight: 600; color: var(--text-primary); }
.nt-header-sub   { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
.nt-status-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: #10B981; box-shadow: 0 0 6px rgba(16,185,129,0.6);
    margin-left: auto; animation: pulse-dot 2s infinite;
}
.nt-status-dot.offline { background: #EF4444; box-shadow: 0 0 6px rgba(239,68,68,0.6); animation: none; }
@keyframes pulse-dot { 0%,100%{opacity:1}50%{opacity:.4} }

.nt-chat-window { padding: 24px 32px; display: flex; flex-direction: column; gap: 20px; min-height: calc(100vh - 200px); }

.nt-msg { display: flex; gap: 12px; align-items: flex-start; animation: msg-in 0.25s ease-out; }
@keyframes msg-in { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:translateY(0)} }
.nt-msg.user  { flex-direction: row-reverse; }
.nt-msg.agent { flex-direction: row; }

.nt-avatar {
    width: 34px; height: 34px; border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 15px; flex-shrink: 0;
}
.nt-avatar.user  { background: var(--user-bubble); border: 1px solid var(--border); }
.nt-avatar.agent { background: var(--accent-muted); border: 1px solid var(--accent); box-shadow: 0 0 10px var(--accent-glow); }

.nt-bubble { max-width: 68%; padding: 14px 18px; border-radius: var(--radius); line-height: 1.65; font-size: 14px; }
.nt-bubble.user  { background: var(--user-bubble); border: 1px solid var(--border); color: var(--text-primary); border-top-right-radius: 4px; }
.nt-bubble.agent { background: var(--agent-bubble); border: 1px solid var(--border-soft); color: var(--text-primary); border-top-left-radius: 4px; }
.nt-bubble.agent strong { color: #C4B5FD; }
.nt-bubble.agent code   { background: rgba(108,99,255,0.12); padding: 2px 6px; border-radius: 4px; font-family:'JetBrains Mono',monospace; font-size:12px; color:#A78BFA; }

.nt-meta { font-size: 11px; color: var(--text-muted); margin-top: 6px; display:flex; gap:8px; align-items:center; }

.nt-intent { display:inline-flex; align-items:center; gap:5px; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:.5px; }
.intent-faq       { background:rgba(59,130,246,.15);  color:#93C5FD; border:1px solid rgba(59,130,246,.3); }
.intent-order     { background:rgba(16,185,129,.15);  color:#6EE7B7; border:1px solid rgba(16,185,129,.3); }
.intent-refund    { background:rgba(245,158,11,.15);  color:#FCD34D; border:1px solid rgba(245,158,11,.3); }
.intent-technical { background:rgba(239,68,68,.15);   color:#FCA5A5; border:1px solid rgba(239,68,68,.3);  }

.nt-api-badge { display:inline-flex; align-items:center; gap:4px; padding:2px 8px; border-radius:20px; font-size:10px; font-family:'JetBrains Mono',monospace; background:rgba(16,185,129,.1); color:#6EE7B7; border:1px solid rgba(16,185,129,.25); }

.nt-input-row { position:sticky; bottom:0; background:var(--bg-base); border-top:1px solid var(--border); padding:16px 32px 20px; display:flex; gap:10px; align-items:flex-end; }

[data-testid="stTextArea"] textarea {
    background: var(--bg-input) !important; border:1px solid var(--border) !important;
    border-radius: var(--radius) !important; color: var(--text-primary) !important;
    font-family:'Inter',sans-serif !important; font-size:14px !important; resize:none !important;
    padding:14px 16px !important; transition:border-color .2s;
}
[data-testid="stTextArea"] textarea:focus { border-color:var(--accent) !important; box-shadow:0 0 0 3px var(--accent-glow) !important; }
[data-testid="stTextArea"] label { display:none !important; }

.stButton > button {
    background: var(--accent) !important; color:#fff !important; border:none !important;
    border-radius:var(--radius) !important; padding:14px 28px !important; font-size:14px !important;
    font-weight:600 !important; font-family:'Inter',sans-serif !important;
    box-shadow:0 0 16px var(--accent-glow) !important; transition:all .2s !important;
}
.stButton > button:hover { filter:brightness(1.12) !important; transform:translateY(-1px) !important; }
.stButton > button:active { transform:translateY(0) !important; }

.nt-sidebar-label { font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:1px; color:var(--text-muted); margin-bottom:10px; }
.nt-stat-card { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); padding:12px 14px; margin-bottom:8px; }
.nt-stat-label { font-size:11px; color:var(--text-secondary); }
.nt-stat-value { font-size:20px; font-weight:700; color:var(--text-primary); margin-top:2px; }
.nt-stat-value.accent { color:var(--accent); }

.nt-doc-card { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px 12px; margin-bottom:6px; font-size:12px; color:var(--text-secondary); line-height:1.5; }
.nt-doc-card:hover { border-color:var(--accent); color:var(--text-primary); }
.nt-doc-source { font-size:10px; color:var(--text-muted); font-family:'JetBrains Mono',monospace; margin-top:4px; }

.nt-new-btn > button { background:transparent !important; border:1px solid var(--border) !important; color:var(--text-secondary) !important; box-shadow:none !important; width:100%; font-size:13px !important; padding:10px 16px !important; }
.nt-new-btn > button:hover { border-color:var(--accent) !important; color:var(--text-primary) !important; transform:none !important; box-shadow:none !important; filter:none !important; }

.nt-empty { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:55vh; gap:16px; color:var(--text-muted); text-align:center; }
.nt-empty-icon  { font-size:48px; opacity:.4; }
.nt-empty-title { font-size:18px; font-weight:600; color:var(--text-secondary); }
.nt-empty-sub   { font-size:13px; max-width:360px; line-height:1.6; }
.nt-suggestion-grid { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px; max-width:480px; }
.nt-suggestion { background:var(--bg-card); border:1px solid var(--border); border-radius:var(--radius-sm); padding:10px 14px; font-size:12px; color:var(--text-secondary); }

.nt-error-banner { margin:16px 32px; padding:14px 18px; background:rgba(239,68,68,.1); border:1px solid rgba(239,68,68,.3); border-radius:10px; color:#FCA5A5; font-size:13px; line-height:1.6; }

::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:var(--bg-base); }
::-webkit-scrollbar-thumb { background:var(--border); border-radius:3px; }
::-webkit-scrollbar-thumb:hover { background:var(--accent); }
</style>
""", unsafe_allow_html=True)


# ── Session state ─────────────────────────────────────────────────────────────
def _init():
    defaults = {
        "thread_id":     str(uuid.uuid4()),
        "messages":      [],
        "intent_counts": {"faq": 0, "order": 0, "refund": 0, "technical": 0},
        "total_queries": 0,
        "last_docs":     [],
        "last_intent":   "",
        "input_key":     0,
        "api_status":    "unknown",   # "ok" | "error" | "unknown"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init()


# ── API helpers ───────────────────────────────────────────────────────────────
def api_chat(query: str, thread_id: str) -> dict:
    """POST /api/v1/chat and return the JSON response dict."""
    with httpx.Client(timeout=REQUEST_TIMEOUT) as client:
        resp = client.post(
            f"{API_BASE_URL}/chat",
            json={"query": query, "thread_id": thread_id},
        )
        resp.raise_for_status()
        return resp.json()


def api_health() -> dict | None:
    """GET /api/v1/health — returns dict or None on failure."""
    try:
        with httpx.Client(timeout=4) as client:
            resp = client.get(f"{API_BASE_URL}/health")
            resp.raise_for_status()
            return resp.json()
    except Exception:
        return None


def check_api_status():
    """Probe the API and update session state."""
    result = api_health()
    st.session_state.api_status = "ok" if result else "error"
    return result


# ── Helpers ───────────────────────────────────────────────────────────────────
INTENT_ICONS  = {"faq": "💬", "order": "📦", "refund": "💳", "technical": "🔧"}
INTENT_LABELS = {"faq": "FAQ", "order": "Order", "refund": "Refund", "technical": "Technical"}

def intent_badge(intent: str) -> str:
    cls   = f"intent-{intent}" if intent in INTENT_ICONS else "intent-faq"
    icon  = INTENT_ICONS.get(intent, "💬")
    label = INTENT_LABELS.get(intent, intent.upper())
    return f'<span class="nt-intent {cls}">{icon} {label}</span>'

def ts_now() -> str:
    return datetime.now().strftime("%H:%M")

def new_conversation():
    st.session_state.thread_id   = str(uuid.uuid4())
    st.session_state.messages    = []
    st.session_state.last_docs   = []
    st.session_state.last_intent = ""
    st.session_state.input_key  += 1


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:0 8px 20px;">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="width:30px;height:30px;background:#6C63FF;border-radius:8px;
                        display:flex;align-items:center;justify-content:center;
                        font-weight:700;font-size:14px;color:#fff;
                        box-shadow:0 0 12px rgba(108,99,255,0.4);">N</div>
            <div>
                <div style="font-weight:700;font-size:14px;color:#E8EAF0;">NovaTech Support</div>
                <div style="font-size:11px;color:#52566A;">Multi-Agent AI · FastAPI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # New conversation
    st.markdown('<div class="nt-new-btn">', unsafe_allow_html=True)
    if st.button("＋  New Conversation", key="new_conv"):
        new_conversation()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Stats
    st.markdown('<div class="nt-sidebar-label">Session Stats</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f'<div class="nt-stat-card"><div class="nt-stat-label">Queries</div><div class="nt-stat-value accent">{st.session_state.total_queries}</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="nt-stat-card"><div class="nt-stat-label">Messages</div><div class="nt-stat-value">{len(st.session_state.messages)}</div></div>', unsafe_allow_html=True)

    # Intent breakdown
    st.markdown('<br><div class="nt-sidebar-label">Intent Breakdown</div>', unsafe_allow_html=True)
    color_map = {"faq": "#3B82F6", "order": "#10B981", "refund": "#F59E0B", "technical": "#EF4444"}
    for intent, count in st.session_state.intent_counts.items():
        bar_w = int((count / max(st.session_state.total_queries, 1)) * 100)
        col   = color_map[intent]
        st.markdown(f"""
        <div style="margin-bottom:10px;">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
                <span style="font-size:12px;color:#8B90A7;">{INTENT_ICONS[intent]} {INTENT_LABELS[intent]}</span>
                <span style="font-size:12px;font-weight:600;color:#E8EAF0;">{count}</span>
            </div>
            <div style="height:4px;background:#1A1D27;border-radius:2px;">
                <div style="height:4px;width:{bar_w}%;background:{col};border-radius:2px;
                            box-shadow:0 0 6px {col}55;transition:width .4s ease;"></div>
            </div>
        </div>""", unsafe_allow_html=True)

    # Retrieved context
    if st.session_state.last_docs:
        st.markdown('<br><div class="nt-sidebar-label">Retrieved Context</div>', unsafe_allow_html=True)
        for doc in st.session_state.last_docs[:3]:
            snippet  = doc["content"][:120].replace("<","&lt;").replace(">","&gt;")
            source   = os.path.basename(doc.get("source","knowledge base"))
            page     = doc.get("page")
            page_str = f" · p.{page}" if page else ""
            st.markdown(f'<div class="nt-doc-card"><div>{snippet}…</div><div class="nt-doc-source">📄 {source}{page_str}</div></div>', unsafe_allow_html=True)

    # Thread ID
    st.markdown(f"""<br>
    <div style="font-size:10px;color:#52566A;font-family:'JetBrains Mono',monospace;
                padding:8px 10px;background:#13161E;border-radius:6px;border:1px solid #2A2E3E;word-break:break-all;">
        thread: {st.session_state.thread_id[:24]}…
    </div>""", unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:8px;font-size:10px;color:#52566A;font-family:'JetBrains Mono',monospace;
                padding:8px 10px;background:#13161E;border-radius:6px;border:1px solid #2A2E3E;">
        📖 <a href="{API_BASE_URL.replace('/api/v1','')}/docs" target="_blank"
              style="color:#6C63FF;text-decoration:none;">Swagger UI</a>
        &nbsp;·&nbsp;
        <a href="{API_BASE_URL.replace('/api/v1','')}/redoc" target="_blank"
           style="color:#6C63FF;text-decoration:none;">ReDoc</a>
    </div>""", unsafe_allow_html=True)


# ── Main panel ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="nt-header">
    <div class="nt-logo">N</div>
    <div>
        <div class="nt-header-title">NovaTech Customer Support</div>
        <div class="nt-header-sub">LangGraph · GPT-4o-mini · FAISS RAG · FastAPI</div>
    </div>
    <div class="nt-status-dot" title="Agent online"></div>
</div>
""", unsafe_allow_html=True)

# Chat window
st.markdown('<div class="nt-chat-window">', unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown("""
    <div class="nt-empty">
        <div class="nt-empty-icon">⚡</div>
        <div class="nt-empty-title">How can we help you today?</div>
        <div class="nt-empty-sub">
            Ask about orders, refunds, product troubleshooting, or general questions —
            our AI agents route your query automatically.
        </div>
        <div class="nt-suggestion-grid">
            <div class="nt-suggestion">📦 Where is my order #4521?</div>
            <div class="nt-suggestion">💳 How do I request a refund?</div>
            <div class="nt-suggestion">🔧 My device won't turn on</div>
            <div class="nt-suggestion">💬 What's your return window?</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    for msg in st.session_state.messages:
        role    = msg["role"]
        content = msg["content"].replace("<","&lt;").replace(">","&gt;")
        ts      = msg.get("ts", "")

        if role == "user":
            st.markdown(f"""
            <div class="nt-msg user">
                <div class="nt-avatar user">👤</div>
                <div>
                    <div class="nt-bubble user">{content}</div>
                    <div class="nt-meta" style="justify-content:flex-end;">{ts}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        else:
            intent     = msg.get("intent", "")
            badge      = intent_badge(intent) if intent else ""
            api_badge  = '<span class="nt-api-badge">⚡ via API</span>'
            st.markdown(f"""
            <div class="nt-msg agent">
                <div class="nt-avatar agent">⚡</div>
                <div>
                    <div class="nt-bubble agent">{content}</div>
                    <div class="nt-meta">{ts} {badge} {api_badge}</div>
                </div>
            </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Input area ────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([9, 1])
with col_input:
    user_input = st.text_area(
        label="Message",
        placeholder="Type your message…",
        height=56,
        key=f"chat_input_{st.session_state.input_key}",
        label_visibility="collapsed",
    )
with col_btn:
    send = st.button("Send ↑", key="send_btn", use_container_width=True)

# ── Send handler ──────────────────────────────────────────────────────────────
if send and user_input and user_input.strip():
    query = user_input.strip()

    st.session_state.messages.append({"role": "user", "content": query, "ts": ts_now()})
    st.session_state.total_queries += 1

    with st.spinner("Routing to agents…"):
        try:
            data = api_chat(query, st.session_state.thread_id)
            st.session_state.api_status = "ok"

            response = data.get("response", "")
            intent   = data.get("intent", "faq")
            docs     = data.get("retrieved_docs", [])
            ticket   = data.get("ticket_id")

            # Append ticket notice if escalated
            if ticket:
                response += f"\n\n🎫 **Ticket raised:** `{ticket}`"

            if intent in st.session_state.intent_counts:
                st.session_state.intent_counts[intent] += 1
            st.session_state.last_docs   = docs
            st.session_state.last_intent = intent

            st.session_state.messages.append({
                "role": "agent", "content": response,
                "intent": intent, "ts": ts_now(),
            })

        except httpx.ConnectError:
            st.session_state.api_status = "error"
            st.session_state.messages.append({
                "role": "agent",
                "content": (
                    "⚠ **Cannot reach the API server.**\n\n"
                    f"Make sure the backend is running:\n\n"
                    "`python api_server.py`\n\n"
                    f"Expected at: `{API_BASE_URL}`"
                ),
                "intent": "", "ts": ts_now(),
            })
        except httpx.HTTPStatusError as e:
            st.session_state.messages.append({
                "role": "agent",
                "content": f"⚠ API error {e.response.status_code}: {e.response.text[:200]}",
                "intent": "", "ts": ts_now(),
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "agent",
                "content": f"⚠ Unexpected error: {str(e)[:200]}",
                "intent": "", "ts": ts_now(),
            })

    st.session_state.input_key += 1
    st.rerun()
