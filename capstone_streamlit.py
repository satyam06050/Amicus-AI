def get_custom_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Bebas+Neue&family=IBM+Plex+Mono:wght@400;600&display=swap');

/* ── RESET & BASE ─────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #F2EFE6 !important;
    font-family: 'Space Mono', monospace !important;
}

[data-testid="stApp"] {
    background-color: #F2EFE6 !important;
}

/* Kill all Streamlit default polish */
[data-testid="stHeader"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
section[data-testid="stSidebar"] > div { padding-top: 1.5rem !important; }

/* ── SIDEBAR ──────────────────────────────────────── */
[data-testid="stSidebar"] {
    background-color: #1A1A1A !important;
    border-right: 4px solid #000 !important;
}

[data-testid="stSidebar"] * {
    color: #F2EFE6 !important;
    font-family: 'Space Mono', monospace !important;
}

[data-testid="stSidebar"] .stMarkdown h3 {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.8rem !important;
    letter-spacing: 0.12em;
    color: #F2EFE6 !important;
    margin-bottom: 0.2rem !important;
    border-bottom: 3px solid #F2EFE6;
    padding-bottom: 0.4rem;
}

[data-testid="stSidebar"] hr {
    border: none !important;
    border-top: 2px solid #333 !important;
    margin: 1rem 0 !important;
}

/* ── METRIC CARDS ─────────────────────────────────── */
.metric-card {
    background: #000;
    border: 3px solid #F2EFE6;
    padding: 0.75rem 1rem;
    margin-bottom: 0.25rem;
}

.metric-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #888 !important;
    margin-bottom: 0.2rem;
}

.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    color: #F2EFE6 !important;
    line-height: 1;
}

/* ── SIDEBAR BUTTONS ──────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 2px solid #444 !important;
    color: #F2EFE6 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    text-align: left !important;
    border-radius: 0 !important;
    padding: 0.5rem 0.75rem !important;
    transition: all 0.08s ease !important;
    letter-spacing: 0.02em;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: #F2EFE6 !important;
    color: #000 !important;
    border-color: #F2EFE6 !important;
    transform: translate(-2px, -2px) !important;
    box-shadow: 3px 3px 0 #888 !important;
}

/* New Conversation button — accent */
[data-testid="stSidebar"] .stButton:last-of-type > button {
    border-color: #E8C547 !important;
    color: #E8C547 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] .stButton:last-of-type > button:hover {
    background: #E8C547 !important;
    color: #000 !important;
}

/* ── PILLS / BADGES ───────────────────────────────── */
.topic-pill {
    display: inline-block;
    background: transparent;
    border: 2px solid #555;
    color: #AAA !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    margin: 2px 2px;
    border-radius: 0;
}

.route-badge {
    display: inline-block;
    background: #E8C547;
    color: #000 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.6rem;
    font-weight: 700;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding: 1px 6px;
    border-radius: 0;
}

.source-tag {
    display: inline-block;
    background: #1A1A1A;
    color: #999 !important;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.05em;
    padding: 1px 8px;
    margin: 2px 2px;
    border: 1px solid #333;
    border-radius: 0;
}

/* ── FAITHFULNESS BAR ─────────────────────────────── */
.faith-bar-bg {
    height: 6px;
    background: #333;
    border-radius: 0;
    display: inline-block;
    vertical-align: middle;
}

.faith-bar-fill {
    height: 6px;
    border-radius: 0;
    transition: width 0.3s ease;
}

/* ── MAIN AREA ────────────────────────────────────── */
.main-title {
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: clamp(2.8rem, 6vw, 5rem);
    letter-spacing: 0.08em;
    color: #000;
    line-height: 0.95;
    margin-bottom: 0.1rem;
    border-left: 10px solid #000;
    padding-left: 1rem;
    text-transform: uppercase;
}

.sub-caption {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    color: #555;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    margin-left: calc(1rem + 10px);
    border-bottom: 2px solid #000;
    padding-bottom: 0.75rem;
}

/* ── CHAT MESSAGES ────────────────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.75rem 0 !important;
    border-bottom: 1px solid #CCC !important;
    border-radius: 0 !important;
}

/* User message bubble */
[data-testid="stChatMessage"][data-testid*="user"],
[aria-label*="user"] [data-testid="stMarkdownContainer"] {
    font-family: 'Space Mono', monospace !important;
}

/* Message content */
[data-testid="stChatMessage"] p,
[data-testid="stChatMessage"] li,
[data-testid="stChatMessage"] span {
    font-family: 'Space Mono', monospace !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
    color: #111 !important;
}

/* ── CHAT INPUT ───────────────────────────────────── */
[data-testid="stChatInputContainer"] {
    border-top: 4px solid #000 !important;
    background: #F2EFE6 !important;
    padding: 1rem 0 !important;
}

[data-testid="stChatInputContainer"] textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.9rem !important;
    background: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    color: #000 !important;
    padding: 0.75rem !important;
    box-shadow: 4px 4px 0 #000 !important;
}

[data-testid="stChatInputContainer"] textarea:focus {
    box-shadow: 6px 6px 0 #E8C547 !important;
    outline: none !important;
}

[data-testid="stChatInputContainer"] button {
    background: #000 !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    color: #E8C547 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.1em;
}

/* ── EXPANDERS ────────────────────────────────────── */
[data-testid="stExpander"] {
    border: 2px solid #000 !important;
    border-radius: 0 !important;
    background: #fff !important;
    margin-top: 0.5rem !important;
}

[data-testid="stExpander"] summary {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
    color: #000 !important;
    background: #F2EFE6 !important;
    padding: 0.5rem 1rem !important;
    border-bottom: 2px solid #000 !important;
}

[data-testid="stExpander"] > div > div {
    padding: 0.75rem 1rem !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
}

/* ── SPINNER / STATUS ─────────────────────────────── */
[data-testid="stSpinner"] {
    border: 3px solid #000 !important;
    padding: 1rem !important;
    background: #E8C547 !important;
    border-radius: 0 !important;
}

[data-testid="stSpinner"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    color: #000 !important;
}

/* ── ALERTS ───────────────────────────────────────── */
[data-testid="stInfo"] {
    background: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    border-left: 8px solid #000 !important;
}

[data-testid="stSuccess"] {
    background: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    border-left: 8px solid #4CAF50 !important;
}

[data-testid="stError"] {
    background: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    border-left: 8px solid #E53935 !important;
}

[data-testid="stWarning"] {
    background: #fff !important;
    border: 3px solid #000 !important;
    border-radius: 0 !important;
    border-left: 8px solid #E8C547 !important;
}

[data-testid="stInfo"] p,
[data-testid="stSuccess"] p,
[data-testid="stError"] p,
[data-testid="stWarning"] p {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    color: #000 !important;
}

/* ── FILE UPLOADER ────────────────────────────────── */
[data-testid="stFileUploader"] {
    border: 3px dashed #555 !important;
    border-radius: 0 !important;
    background: #111 !important;
    padding: 0.5rem !important;
}

[data-testid="stFileUploader"] label,
[data-testid="stFileUploader"] p,
[data-testid="stFileUploader"] span {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.72rem !important;
    color: #999 !important;
}

[data-testid="stFileUploader"] button {
    background: #E8C547 !important;
    color: #000 !important;
    border: 2px solid #E8C547 !important;
    border-radius: 0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-weight: 700 !important;
    font-size: 0.72rem !important;
}

/* ── DIVIDER ──────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 2px solid #000 !important;
    margin: 1rem 0 !important;
}

/* ── SCROLLBAR ────────────────────────────────────── */
::-webkit-scrollbar { width: 8px; background: #F2EFE6; }
::-webkit-scrollbar-thumb { background: #000; border: 2px solid #F2EFE6; }

/* ── EMPTY STATE ──────────────────────────────────── */
.empty-state-box {
    border: 4px solid #000;
    padding: 3rem 2rem;
    text-align: center;
    background: #fff;
    box-shadow: 8px 8px 0 #000;
    margin: 2rem 0;
}

.empty-state-icon {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    color: #000;
    line-height: 1;
    display: block;
    margin-bottom: 0.5rem;
}

.empty-state-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2rem;
    letter-spacing: 0.1em;
    color: #000;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}

.empty-state-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    color: #555;
    letter-spacing: 0.05em;
}

/* ── CODE BLOCKS ──────────────────────────────────── */
code, pre {
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.8rem !important;
    background: #1A1A1A !important;
    color: #E8C547 !important;
    border-radius: 0 !important;
    border: 2px solid #000 !important;
}
</style>
"""