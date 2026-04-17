import streamlit as st
import uuid
import logging
from dotenv import load_dotenv
from documents import DOCUMENTS
from agent import load_agent
from utils import sanitize_input

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document Intelligence Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Source+Sans+3:wght@300;400;500&display=swap');

/* ── Root ── */
html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0f1117;
    color: #e8e2d5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #161a22 !important;
    border-right: 1px solid #2a2f3d;
}

[data-testid="stSidebar"] * {
    color: #c5bfb0 !important;
}

/* ── Title ── */
.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #e8d5a3;
    letter-spacing: -0.5px;
    margin-bottom: 0.1rem;
}

.sub-caption {
    font-size: 0.92rem;
    color: #7a7565;
    font-weight: 300;
    letter-spacing: 0.5px;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid #2a2f3d;
    padding-bottom: 1rem;
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: #161a22 !important;
    border: 1px solid #2a2f3d !important;
    border-radius: 10px !important;
    margin-bottom: 0.6rem;
    padding: 0.8rem 1rem !important;
}

[data-testid="stChatMessage"][data-testid*="user"] {
    background: #1a1f2e !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: #161a22 !important;
    border: 1px solid #3a3f50 !important;
    border-radius: 10px !important;
    color: #e8e2d5 !important;
}

[data-testid="stChatInput"]:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 2px rgba(201,168,76,0.15) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid #3a3f50 !important;
    color: #c5bfb0 !important;
    border-radius: 6px !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-size: 0.85rem !important;
    padding: 0.4rem 1rem !important;
    transition: all 0.2s ease !important;
}

.stButton > button:hover {
    border-color: #c9a84c !important;
    color: #e8d5a3 !important;
    background: rgba(201,168,76,0.08) !important;
}

/* ── Metric cards ── */
.metric-card {
    background: #161a22;
    border: 1px solid #2a2f3d;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    color: #7a7565;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: #e8d5a3;
}

/* ── Topic pill ── */
.topic-pill {
    display: inline-block;
    background: #1f2535;
    border: 1px solid #2a2f3d;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.75rem;
    color: #9a9080;
    margin: 2px;
}

/* ── Source tag ── */
.source-tag {
    display: inline-block;
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 4px;
    padding: 1px 8px;
    font-size: 0.72rem;
    color: #c9a84c;
    margin: 2px;
}

/* ── Route badge ── */
.route-badge {
    display: inline-block;
    background: rgba(100, 180, 220, 0.2);
    border: 1px solid rgba(100, 180, 220, 0.4);
    border-radius: 12px;
    padding: 2px 8px;
    font-size: 0.7rem;
    color: #64b4dc;
    margin: 2px;
    font-weight: 500;
}

/* ── Faithfulness bar ── */
.faith-bar-bg {
    background: #2a2f3d;
    border-radius: 4px;
    height: 4px;
    margin-top: 4px;
}
.faith-bar-fill {
    height: 4px;
    border-radius: 4px;
    transition: width 0.5s ease;
}

/* ── Divider ── */
hr {
    border-color: #2a2f3d !important;
    margin: 1rem 0 !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: #c9a84c !important;
}

/* ── Status / success ── */
.stSuccess {
    background: rgba(40, 80, 50, 0.3) !important;
    border-color: #2a5235 !important;
    color: #7ec89a !important;
}

/* ── Warning ── */
.stWarning {
    background: rgba(80, 60, 20, 0.3) !important;
    border-color: #5a4010 !important;
    color: #c9a84c !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a2f3d; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a3f50; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────
DOMAIN_NAME        = "Document Intelligence Assistant"
DOMAIN_DESCRIPTION = "Ask questions about legal contracts, clauses, and documents — answers grounded in the knowledge base."
KB_TOPICS          = [d["topic"] for d in DOCUMENTS]

# ─────────────────────────────────────────────────────────
# LOAD AGENT (cached)
# ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_agent_cached():
    return load_agent()

# ─────────────────────────────────────────────────────────
# SESSION STATE INIT
# ─────────────────────────────────────────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "thread_id"     not in st.session_state: st.session_state.thread_id     = str(uuid.uuid4())[:8]
if "total_queries" not in st.session_state: st.session_state.total_queries = 0
if "faith_scores"  not in st.session_state: st.session_state.faith_scores  = []  # FIX: was "avg_faithfulness"

# ─────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚖️ Document Intelligence")
    st.markdown(
        f"<div style='font-size:0.82rem; color:#7a7565; margin-bottom:1rem;'>{DOMAIN_DESCRIPTION}</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # Session metrics
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Queries</div>
            <div class='metric-value'>{st.session_state.total_queries}</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        avg_f = (sum(st.session_state.faith_scores) / len(st.session_state.faith_scores)
                 if st.session_state.faith_scores else 0.0)
        st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-label'>Avg Faith</div>
            <div class='metric-value'>{avg_f:.2f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown(
        f"<div style='font-size:0.72rem; color:#4a4535; margin-top:0.5rem;'>Session: {st.session_state.thread_id}</div>",
        unsafe_allow_html=True
    )

    st.divider()

    # Topics
    st.markdown("<div style='font-size:0.75rem; color:#7a7565; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;'>Topics Covered</div>", unsafe_allow_html=True)
    for topic in KB_TOPICS:
        st.markdown(f"<span class='topic-pill'>{topic}</span>", unsafe_allow_html=True)

    st.divider()

    # Sample questions
    st.markdown("<div style='font-size:0.75rem; color:#7a7565; letter-spacing:1px; text-transform:uppercase; margin-bottom:0.5rem;'>Try Asking</div>", unsafe_allow_html=True)
    sample_questions = [
        "What are the elements of a valid contract?",
        "What is anticipatory breach?",
        "When does force majeure apply?",
        "What is an NDA and how long does it last?",
        "What remedies exist for contract breach?",
    ]
    for sq in sample_questions:
        if st.button(sq, key=f"sample_{sq[:20]}", use_container_width=True):
            st.session_state.pending_question = sq

    st.divider()

    # New conversation
    if st.button("🗑️ New Conversation", use_container_width=True):
        st.session_state.messages      = []
        st.session_state.thread_id     = str(uuid.uuid4())[:8]
        st.session_state.total_queries = 0
        st.session_state.faith_scores  = []
        st.session_state.pop("pending_question", None)
        st.rerun()

# ─────────────────────────────────────────────────────────
# MAIN AREA
# ─────────────────────────────────────────────────────────
st.markdown("<div class='main-title'>⚖️ Document Intelligence Assistant</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='sub-caption'>Legal contract analysis · Clause explanation · Document Q&A · Powered by LangGraph + ChromaDB</div>",
    unsafe_allow_html=True
)

# Agent load
with st.spinner("Loading knowledge base and agent…"):
    try:
        agent_app, embedder, collection = load_agent_cached()
        agent_loaded = True
        load_error   = None
    except Exception as e:
        agent_loaded = False
        load_error   = str(e)
        logger.error(f"Agent load failed: {load_error}")

if not agent_loaded:
    st.error(f"⚠️ Failed to load agent: {load_error}")
    st.info("Make sure your GROQ_API_KEY is set in your .env file and all packages are installed.")
    st.stop()

# ── Display chat history ───────────────────────────────
for msg in st.session_state.messages:
    role = msg["role"]
    with st.chat_message(role, avatar="👤" if role == "user" else "⚖️"):
        st.markdown(msg["content"])
        if role == "assistant" and "meta" in msg:
            meta      = msg["meta"]
            faith     = meta.get("faithfulness", 0.0)
            sources   = meta.get("sources", [])
            route     = meta.get("route", "")
            bar_color = "#4caf84" if faith >= 0.7 else "#c9a84c" if faith >= 0.4 else "#c95050"
            st.markdown(f"""
            <div style='margin-top:0.6rem;'>
                <div style='display:flex; align-items:center; gap:8px; flex-wrap:wrap;'>
                    <span style='font-size:0.72rem; color:#7a7565;'>Faithfulness</span>
                    <div class='faith-bar-bg' style='width:80px; display:inline-block;'>
                        <div class='faith-bar-fill' style='width:{int(faith*80)}px; background:{bar_color};'></div>
                    </div>
                    <span style='font-size:0.72rem; color:{bar_color};'>{faith:.2f}</span>
                    <span class='route-badge'>{route.upper()}</span>
                </div>
                <div style='margin-top:4px;'>
                    {''.join(f"<span class='source-tag'>{s}</span>" for s in sources)}
                </div>
            </div>
            """, unsafe_allow_html=True)

# ── Pending question from sidebar ──────────────────────
pending = st.session_state.pop("pending_question", None)

# ── Chat input ─────────────────────────────────────────
prompt = st.chat_input("Ask about contracts, clauses, legal documents…") or pending

if prompt:
    prompt = sanitize_input(prompt)

    if not prompt:
        st.warning("Input was empty or too short after sanitization.")
    else:
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant", avatar="⚖️"):
            status_placeholder = st.empty()
            try:
                status_placeholder.info("🔄 Analyzing question...")
                config = {"configurable": {"thread_id": st.session_state.thread_id}}
                result = agent_app.invoke({"question": prompt}, config=config)

                answer  = result.get("answer", "Sorry, I could not generate an answer.")
                faith   = result.get("faithfulness", 0.0)
                sources = result.get("sources", [])
                route   = result.get("route", "retrieve")

                status_placeholder.empty()
                st.markdown(answer)

                bar_color = "#4caf84" if faith >= 0.7 else "#c9a84c" if faith >= 0.4 else "#c95050"
                st.markdown(f"""
                <div style='margin-top:0.6rem;'>
                    <div style='display:flex; align-items:center; gap:8px; flex-wrap:wrap;'>
                        <span style='font-size:0.72rem; color:#7a7565;'>Faithfulness</span>
                        <div class='faith-bar-bg' style='width:80px; display:inline-block;'>
                            <div class='faith-bar-fill' style='width:{int(faith*80)}px; background:{bar_color};'></div>
                        </div>
                        <span style='font-size:0.72rem; color:{bar_color};'>{faith:.2f}</span>
                        <span class='route-badge'>{route.upper()}</span>
                    </div>
                    <div style='margin-top:4px;'>
                        {''.join(f"<span class='source-tag'>{s}</span>" for s in sources)}
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "meta": {"faithfulness": faith, "sources": sources, "route": route}
                })
                st.session_state.total_queries += 1
                st.session_state.faith_scores.append(faith)

            except Exception as e:
                status_placeholder.empty()
                err_msg = f"An error occurred: {str(e)}"
                logger.error(err_msg)
                st.error(err_msg)
                st.session_state.messages.append({"role": "assistant", "content": err_msg})

        st.rerun()

# ── Empty state ────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center; padding: 3rem 1rem; color:#4a4535;'>
        <div style='font-size:3rem; margin-bottom:1rem;'>⚖️</div>
        <div style='font-family: Playfair Display, serif; font-size:1.2rem; color:#7a7565; margin-bottom:0.5rem;'>
            Ask anything about legal contracts and documents
        </div>
        <div style='font-size:0.85rem; color:#3a3530;'>
            Try a sample question from the sidebar, or type your own below.
        </div>
    </div>
    """, unsafe_allow_html=True)