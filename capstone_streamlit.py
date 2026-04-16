
"""
capstone_streamlit.py — Document Intelligence Assistant Agent
Run: streamlit run capstone_streamlit.py
"""
import streamlit as st
import uuid
import os
import chromadb
from dotenv import load_dotenv
from typing import TypedDict, List
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

st.set_page_config(page_title="Document Intelligence Assistant", page_icon="book", layout="centered")
st.title("Legal Document Intelligence Assistant")
st.caption("Ask questions about legal contracts, clauses, and documents — powered by AI")

# ── Load models and KB (cached) ───────────────────────────
@st.cache_resource
def load_agent():
    llm      = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.Client()
    try: client.delete_collection("capstone_kb")
    except: pass
    collection = client.create_collection("capstone_kb")

    # TODO: Copy your DOCUMENTS list here
    DOCUMENTS = [
        {"id":"doc_001", "topic":"TODO", "text":"TODO — paste your documents here"},
    ]
    texts = [d["text"] for d in DOCUMENTS]
    collection.add(documents=texts, embeddings=embedder.encode(texts).tolist(),
                   ids=[d["id"] for d in DOCUMENTS],
                   metadatas=[{"topic":d["topic"]} for d in DOCUMENTS])

    # TODO: Copy your CapstoneState, node functions, and graph assembly here
    # ... (paste from notebook Parts 2-4)

    return agent_app, embedder, collection


try:
    agent_app, embedder, collection = load_agent()
    st.success(f"Knowledge base loaded — {collection.count()} documents")
except Exception as e:
    st.error(f"Failed to load agent: {e}")
    st.stop()

# ── Session state ─────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())[:8]

# ── Sidebar ───────────────────────────────────────────────
with st.sidebar:
    st.header("About")
    st.write("Ask questions about legal contracts, clauses, and documents — powered by AI")
    st.write(f"Session: {st.session_state.thread_id}")
    st.divider()
    st.write("**Topics covered:**")
    for t in ['Essential Elements of Legal Contracts', 'Types of Contracts and Their Enforceability', 'Contract Breach and Its Types', 'Remedies Available for Contract Breach', 'Non-Disclosure Agreements (NDAs) and Confidentiality', 'Intellectual Property Rights in Contracts', 'Termination Clauses and Contract Endings', 'Dispute Resolution: Arbitration and Litigation', 'Liability and Indemnity Clauses', 'Force Majeure and Unforeseeable Events']:
        st.write(f"* {t}")
    if st.button("New conversation"):
        st.session_state.messages = []
        st.session_state.thread_id = str(uuid.uuid4())[:8]
        st.rerun()

# ── Display history ───────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Chat input ────────────────────────────────────────────
if prompt := st.chat_input("Ask something..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            config = {"configurable": {"thread_id": st.session_state.thread_id}}
            result = agent_app.invoke({"question": prompt}, config=config)
            answer = result.get("answer", "Sorry, I could not generate an answer.")
        st.write(answer)
        faith = result.get("faithfulness", 0.0)
        if faith > 0:
            st.caption(f"Faithfulness: {faith:.2f} | Sources: {result.get(\'sources\', [])}")

    st.session_state.messages.append({"role":"assistant","content":answer})
