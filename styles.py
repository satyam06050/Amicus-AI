# ─────────────────────────────────────────────────────────
# STREAMLIT CUSTOM STYLES
# ─────────────────────────────────────────────────────────

def get_custom_css():
    """Return custom CSS for the Streamlit app."""
    return """
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

/* ── File uploader ── */
[data-testid="stFileUploadDropzone"] {
    background: #161a22 !important;
    border: 2px dashed #2a2f3d !important;
    border-radius: 8px !important;
}

</style>
"""
