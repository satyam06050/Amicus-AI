import logging
from typing import List
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from documents import DOCUMENTS

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────────────────
# TYPE DEFINITIONS
# ─────────────────────────────────────────────────────────
from typing import TypedDict

class CapstoneState(TypedDict):
    question:      str
    messages:      List[dict]
    route:         str
    retrieved:     str
    sources:       List[str]
    tool_result:   str
    answer:        str
    faithfulness:  float
    eval_retries:  int
    document_name: str

# ─────────────────────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────────────────────
FAITHFULNESS_THRESHOLD = 0.7
MAX_EVAL_RETRIES       = 2

# ─────────────────────────────────────────────────────────
# NODE FUNCTIONS (extracted from monolithic load_agent)
# ─────────────────────────────────────────────────────────

def create_memory_node(llm, embedder, collection):
    """Create and return the memory node function."""
    def memory_node(state: CapstoneState) -> dict:
        msgs     = state.get("messages", [])
        question = state["question"]
        msgs     = msgs + [{"role": "user", "content": question}]
        if len(msgs) > 6:
            msgs = msgs[-6:]
        # Extract and persist user name if introduced
        updates: dict = {"messages": msgs}
        lower = question.lower()
        if "my name is" in lower:
            import re
            match = re.search(r"my name is ([\w]+)", lower)
            if match:
                updates["document_name"] = match.group(1).capitalize()
        return updates
    return memory_node

def create_router_node(llm):
    """Create and return the router node function."""
    def router_node(state: CapstoneState) -> dict:
        question = state["question"]
        messages = state.get("messages", [])
        recent   = "; ".join(
            f"{m['role']}: {m['content'][:60]}" for m in messages[-3:-1]
        ) or "none"

        prompt = f"""You are a router for a Legal Document Intelligence Assistant.

Available options:
- retrieve: search the knowledge base for contract and legal document information
- memory_only: answer from conversation history (e.g. 'what did you just say?' or 'can you clarify that?')
- tool: use the web_search tool for recent case law, current legal news, or information not in the knowledge base

Recent conversation: {recent}
Current question: {question}

Reply with ONLY one word: retrieve / memory_only / tool"""

        response = llm.invoke(prompt)
        decision = response.content.strip().lower()

        if "memory"  in decision: decision = "memory_only"
        elif "tool"  in decision: decision = "tool"
        else:                     decision = "retrieve"

        return {"route": decision}
    return router_node

def create_retrieval_node(embedder, collection):
    """Create and return the retrieval node function."""
    def retrieval_node(state: CapstoneState) -> dict:
        q_emb   = embedder.encode([state["question"]]).tolist()
        results = collection.query(query_embeddings=q_emb, n_results=3)
        chunks  = results["documents"][0]
        topics  = [m["topic"] for m in results["metadatas"][0]]
        context = "\n\n---\n\n".join(
            f"[{topics[i]}]\n{chunks[i]}" for i in range(len(chunks))
        )
        return {"retrieved": context, "sources": topics}
    return retrieval_node

def create_skip_retrieval_node():
    """Create and return the skip retrieval node function."""
    def skip_retrieval_node(state: CapstoneState) -> dict:
        return {"retrieved": "", "sources": []}
    return skip_retrieval_node

def create_tool_node(llm):
    """Create and return the web search tool node function."""
    def tool_node(state: CapstoneState) -> dict:
        question = state["question"]
        try:
            from duckduckgo_search import DDGS
            with DDGS() as ddgs:
                results = list(ddgs.text(question, max_results=3))
            if results:
                tool_result = "\n".join(
                    f"{r['title']}: {r['body'][:200]}" for r in results
                )
            else:
                tool_result = "No web search results found for that query."
        except ImportError:
            tool_result = "Web search tool not available. Please install duckduckgo-search."
        except Exception as e:
            logger.error(f"Web search error: {str(e)}")
            tool_result = f"Web search encountered an error: {str(e)[:100]}"
        return {"tool_result": tool_result}
    return tool_node

def create_answer_node(llm):
    """Create and return the answer generation node function."""
    def answer_node(state: CapstoneState) -> dict:
        question     = state["question"]
        retrieved    = state.get("retrieved", "")
        tool_result  = state.get("tool_result", "")
        messages     = state.get("messages", [])
        eval_retries = state.get("eval_retries", 0)

        context_parts = []
        if retrieved:
            context_parts.append(f"KNOWLEDGE BASE:\n{retrieved}")
        if tool_result:
            context_parts.append(f"WEB SEARCH RESULT:\n{tool_result}")
        context = "\n\n".join(context_parts)

        if context:
            system_content = f"""You are a Document Intelligence Assistant specialising in legal contracts and documents.
Answer using ONLY the information provided in the context below.
If the answer is not in the context, say clearly: "I don't have that information in my knowledge base."
Do NOT add information from your training data. Be precise, professional, and cite the topic area when relevant.

{context}"""
        else:
            system_content = "You are a helpful legal document assistant. Answer based on the conversation history only."

        if eval_retries > 0:
            system_content += "\n\nIMPORTANT: Your previous answer did not meet quality standards. Answer using ONLY information explicitly stated in the context above."

        lc_msgs = [SystemMessage(content=system_content)]
        for msg in messages[:-1]:
            if msg["role"] == "user":
                lc_msgs.append(HumanMessage(content=msg["content"]))
            else:
                lc_msgs.append(AIMessage(content=msg["content"]))
        lc_msgs.append(HumanMessage(content=question))

        response = llm.invoke(lc_msgs)
        return {"answer": response.content}
    return answer_node

def create_eval_node(llm):
    """Create and return the evaluation node function."""
    def eval_node(state: CapstoneState) -> dict:
        answer  = state.get("answer", "")
        context = state.get("retrieved", "")[:500]
        retries = state.get("eval_retries", 0)

        if not context:
            return {"faithfulness": 1.0, "eval_retries": retries + 1}

        prompt = f"""Rate faithfulness: does this answer use ONLY information from the context?
Reply with ONLY a number between 0.0 and 1.0.
1.0 = fully faithful. 0.5 = some hallucination. 0.0 = mostly hallucinated.

Context: {context}
Answer: {answer[:300]}"""

        result = llm.invoke(prompt).content.strip()
        try:
            score = float(result.split()[0].replace(",", "."))
            score = max(0.0, min(1.0, score))
        except Exception as e:
            logger.warning(f"Failed to parse faithfulness score: {str(e)}")
            score = 0.5

        return {"faithfulness": score, "eval_retries": retries + 1}
    return eval_node

def create_save_node():
    """Create and return the save node function."""
    def save_node(state: CapstoneState) -> dict:
        messages = state.get("messages", [])
        messages = messages + [{"role": "assistant", "content": state["answer"]}]
        return {"messages": messages}
    return save_node

# ─────────────────────────────────────────────────────────
# ROUTING FUNCTIONS
# ─────────────────────────────────────────────────────────

def route_decision(state: CapstoneState) -> str:
    """Decide whether to retrieve from KB, use memory only, or search web."""
    route = state.get("route", "retrieve")
    if route == "tool":         return "tool"
    if route == "memory_only":  return "skip"
    return "retrieve"

def eval_decision(state: CapstoneState) -> str:
    """Decide whether to save answer or retry evaluation."""
    score   = state.get("faithfulness", 1.0)
    retries = state.get("eval_retries", 0)
    if score >= FAITHFULNESS_THRESHOLD or retries >= MAX_EVAL_RETRIES:
        return "save"
    return "answer"

# ─────────────────────────────────────────────────────────
# AGENT LOADER
# ─────────────────────────────────────────────────────────

def load_agent():
    """
    Load and build the LangGraph agent.
    
    Returns:
        tuple: (agent_app, embedder, collection)
    """
    llm      = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    embedder = SentenceTransformer("all-MiniLM-L6-v2")

    # Build ChromaDB
    client = chromadb.Client()
    try:
        client.delete_collection("capstone_kb")
    except Exception as e:
        # Collection doesn't exist yet; safe to proceed
        logger.debug(f"Could not delete existing collection: {str(e)}")

    collection = client.create_collection("capstone_kb")

    texts      = [d["text"]  for d in DOCUMENTS]
    ids        = [d["id"]    for d in DOCUMENTS]
    embeddings = embedder.encode(texts).tolist()

    collection.add(
        documents  = texts,
        embeddings = embeddings,
        ids        = ids,
        metadatas  = [{"topic": d["topic"]} for d in DOCUMENTS]
    )

    # Instantiate all node functions
    memory_node    = create_memory_node(llm, embedder, collection)
    router_node    = create_router_node(llm)
    retrieval_node = create_retrieval_node(embedder, collection)
    skip_node      = create_skip_retrieval_node()
    tool_node      = create_tool_node(llm)
    answer_node    = create_answer_node(llm)
    eval_node      = create_eval_node(llm)
    save_node      = create_save_node()

    # Build graph
    graph = StateGraph(CapstoneState)

    graph.add_node("memory",   memory_node)
    graph.add_node("router",   router_node)
    graph.add_node("retrieve", retrieval_node)
    graph.add_node("skip",     skip_node)
    graph.add_node("tool",     tool_node)
    graph.add_node("answer",   answer_node)
    graph.add_node("eval",     eval_node)
    graph.add_node("save",     save_node)

    graph.set_entry_point("memory")
    graph.add_edge("memory", "router")

    graph.add_conditional_edges(
        "router", route_decision,
        {"retrieve": "retrieve", "skip": "skip", "tool": "tool"}
    )

    graph.add_edge("retrieve", "answer")
    graph.add_edge("skip",     "answer")
    graph.add_edge("tool",     "answer")
    graph.add_edge("answer",   "eval")

    graph.add_conditional_edges(
        "eval", eval_decision,
        {"answer": "answer", "save": "save"}
    )
    graph.add_edge("save", END)

    checkpointer = MemorySaver()
    agent_app    = graph.compile(checkpointer=checkpointer)

    return agent_app, embedder, collection
