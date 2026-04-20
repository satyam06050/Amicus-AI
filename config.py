# ─────────────────────────────────────────────────────────
# CONFIGURATION FILE
# ─────────────────────────────────────────────────────────

import os
from pathlib import Path

# ─────────────────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────────────────
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"
UPLOADS_DIR = DATA_DIR / "uploads"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DB_PATH.mkdir(exist_ok=True)
UPLOADS_DIR.mkdir(exist_ok=True)

# ─────────────────────────────────────────────────────────
# KNOWLEDGE BASE
# ─────────────────────────────────────────────────────────
from documents import DOCUMENTS
KB_TOPICS = [d["topic"] for d in DOCUMENTS]

# ─────────────────────────────────────────────────────────
# LLM CONFIGURATION
# ─────────────────────────────────────────────────────────
LLM_MODEL = "llama-3.3-70b-versatile"
LLM_TEMPERATURE = 0
LLM_TIMEOUT = 30

# ─────────────────────────────────────────────────────────
# EMBEDDING CONFIGURATION
# ─────────────────────────────────────────────────────────
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# ─────────────────────────────────────────────────────────
# CHROMADB CONFIGURATION
# ─────────────────────────────────────────────────────────
CHROMA_COLLECTION_NAME = "capstone_kb"
CHROMA_PERSISTENCE = True  # Use persistent storage instead of in-memory

# ─────────────────────────────────────────────────────────
# RETRIEVAL CONFIGURATION
# ─────────────────────────────────────────────────────────
RETRIEVAL_TOP_K = 3  # Number of documents to retrieve
MAX_CONTEXT_LENGTH = 5000  # For eval node

# ─────────────────────────────────────────────────────────
# EVALUATION CONFIGURATION
# ─────────────────────────────────────────────────────────
FAITHFULNESS_THRESHOLD = 0.7
MAX_EVAL_RETRIES = 2

# ─────────────────────────────────────────────────────────
# CONVERSATION CONFIGURATION
# ─────────────────────────────────────────────────────────
MAX_MESSAGES_WINDOW = 6  # Sliding window for message history
MAX_INPUT_LENGTH = 500

# ─────────────────────────────────────────────────────────
# DOCUMENT UPLOAD CONFIGURATION
# ─────────────────────────────────────────────────────────
ALLOWED_UPLOAD_TYPES = {".pdf", ".txt", ".docx"}
MAX_UPLOAD_SIZE_MB = 10
CHUNK_SIZE = 500  # Characters per chunk
CHUNK_OVERLAP = 100  # Overlap between chunks

# ─────────────────────────────────────────────────────────
# WEB SEARCH CONFIGURATION
# ─────────────────────────────────────────────────────────
WEB_SEARCH_TOP_K = 3
WEB_SEARCH_TIMEOUT = 5

# ─────────────────────────────────────────────────────────
# STREAMLIT CONFIGURATION
# ─────────────────────────────────────────────────────────
DOMAIN_NAME = "Document Intelligence Assistant"
DOMAIN_DESCRIPTION = "Ask questions about legal contracts, clauses, and documents — answers grounded in the knowledge base."
PAGE_ICON = "⚖️"
PAGE_TITLE = "Document Intelligence Assistant"
LAYOUT = "wide"

# ─────────────────────────────────────────────────────────
# APP CONFIGURATION
# ─────────────────────────────────────────────────────────
DEBUG_MODE = os.getenv("DEBUG_MODE", "false").lower() == "true"
LOG_LEVEL = "DEBUG" if DEBUG_MODE else "INFO"
