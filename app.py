import streamlit as st
import diabetes_ui
import insurance_ui

st.set_page_config(
    page_title="MediAI Suite",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #020817;
    --bg-secondary: #0a1628;
    --bg-card: rgba(10, 25, 50, 0.8);
    --bg-glass: rgba(255, 255, 255, 0.03);
    --border: rgba(56, 189, 248, 0.12);
    --border-hover: rgba(56, 189, 248, 0.35);
    --accent-cyan: #38bdf8;
    --accent-blue: #3b82f6;
    --accent-emerald: #10b981;
    --accent-rose: #f43f5e;
    --accent-amber: #f59e0b;
    --text-primary: #f0f9ff;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --glow-cyan: 0 0 30px rgba(56, 189, 248, 0.15);
    --glow-blue: 0 0 30px rgba(59, 130, 246, 0.15);
}

*, *::before, *::after {
    box-sizing: border-box;
}

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif !important;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ─── ANIMATED BACKGROUND ─── */
.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.06) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(59,130,246,0.05) 0%, transparent 60%) !important;
}

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c1b 0%, #030f20 100%) !important;
    border-right: 1px solid var(--border) !important;
    width: 280px !important;
}

[data-testid="stSidebar"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
}

[data-testid="stSidebarContent"] {
    padding: 2rem 1.5rem !important;
}

/* ─── LOGO AREA ─── */
.sidebar-logo {
    text-align: center;
    margin-bottom: 2.5rem;
    padding-bottom: 2rem;
    border-bottom: 1px solid var(--border);
    position: relative;
}

.sidebar-logo::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 20%; right: 20%;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), transparent);
    opacity: 0.6;
}

.logo-icon {
    font-size: 2.8rem;
    display: block;
    margin-bottom: 0.6rem;
    filter: drop-shadow(0 0 12px rgba(56,189,248,0.6));
    animation: pulse-glow 3s ease-in-out infinite;
}

@keyframes pulse-glow {
    0%, 100% { filter: drop-shadow(0 0 12px rgba(56,189,248,0.6)); }
    50% { filter: drop-shadow(0 0 20px rgba(56,189,248,0.9)); }
}

.logo-title {
    font-size: 1.4rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.logo-tagline {
    font-size: 0.72rem;
    color: var(--text-muted);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
}

/* ─── NAV LABEL ─── */
.nav-label {
    font-size: 0.65rem;
    font-weight: 600;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.8rem;
    margin-top: 0.5rem;
    padding-left: 0.2rem;
}

/* ─── RADIO BUTTONS → NAV ITEMS ─── */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.5rem !important;
}

[data-testid="stSidebar"] .stRadio label {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 0.85rem 1.1rem !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    display: flex !important;
    align-items: center !important;
    gap: 0.5rem !important;
    width: 100% !important;
}

[data-testid="stSidebar"] .stRadio label:hover {
    border-color: var(--border-hover) !important;
    background: rgba(56, 189, 248, 0.06) !important;
    color: var(--text-primary) !important;
    transform: translateX(3px) !important;
    box-shadow: var(--glow-cyan) !important;
}

[data-testid="stSidebar"] .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.88rem !important;
}

/* ─── SIDEBAR STATUS ─── */
.status-badge {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.7rem 1rem;
    background: rgba(16, 185, 129, 0.08);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 8px;
    margin-top: auto;
    font-size: 0.78rem;
    color: var(--accent-emerald);
}

.status-dot {
    width: 7px;
    height: 7px;
    background: var(--accent-emerald);
    border-radius: 50%;
    animation: blink 2s ease-in-out infinite;
}

@keyframes blink {
    0%, 100% { opacity: 1; box-shadow: 0 0 6px var(--accent-emerald); }
    50% { opacity: 0.4; box-shadow: none; }
}

/* ─── MAIN CONTENT ─── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ─── PAGE HEADER ─── */
.page-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 2.5rem;
    padding-bottom: 1.8rem;
    border-bottom: 1px solid var(--border);
    position: relative;
}

.page-header::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0; width: 120px;
    height: 1px;
    background: linear-gradient(90deg, var(--accent-cyan), transparent);
}

.page-title {
    font-size: 1.9rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-primary);
    line-height: 1.2;
}

.page-title span {
    background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.page-subtitle {
    font-size: 0.88rem;
    color: var(--text-muted);
    margin-top: 0.4rem;
    font-weight: 400;
    letter-spacing: 0.01em;
}

.page-badge {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.4rem 0.9rem;
    background: rgba(56, 189, 248, 0.1);
    border: 1px solid rgba(56, 189, 248, 0.25);
    border-radius: 20px;
    color: var(--accent-cyan);
}

/* ─── GLASS CARDS ─── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.8rem;
    backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(56,189,248,0.3), transparent);
}

.glass-card:hover {
    border-color: var(--border-hover);
    box-shadow: var(--glow-cyan);
}

/* ─── SECTION HEADERS ─── */
.section-header {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--accent-cyan);
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.section-header::before {
    content: '';
    display: inline-block;
    width: 4px;
    height: 16px;
    background: var(--accent-cyan);
    border-radius: 2px;
}

/* ─── SLIDERS ─── */
[data-testid="stSlider"] {
    padding: 0.2rem 0 !important;
}

[data-testid="stSlider"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.03em !important;
    margin-bottom: 0.2rem !important;
}

[data-testid="stSlider"] [data-testid="stTickBar"] {
    display: none !important;
}

[data-testid="stSlider"] .st-bx {
    background: rgba(56,189,248,0.15) !important;
}

/* ─── SELECTBOX ─── */
[data-testid="stSelectbox"] label {
    font-size: 0.8rem !important;
    font-weight: 500 !important;
    color: var(--text-secondary) !important;
    letter-spacing: 0.03em !important;
}

[data-testid="stSelectbox"] > div > div {
    background: rgba(10,25,50,0.9) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}

[data-testid="stSelectbox"] > div > div:hover {
    border-color: var(--border-hover) !important;
}

/* ─── BUTTON ─── */
.stButton > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0ea5e9, #3b82f6) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 1.5rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    cursor: pointer !important;
    transition: all 0.25s ease !important;
    margin-top: 1rem !important;
    box-shadow: 0 4px 20px rgba(56,189,248,0.25) !important;
    position: relative !important;
    overflow: hidden !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(56,189,248,0.4) !important;
    background: linear-gradient(135deg, #38bdf8, #60a5fa) !important;
}

.stButton > button:active {
    transform: translateY(0px) !important;
}

/* ─── METRIC CARDS ─── */
[data-testid="stMetric"] {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    padding: 1.1rem 1.3rem !important;
    transition: all 0.25s ease !important;
}

[data-testid="stMetric"]:hover {
    border-color: var(--border-hover) !important;
    box-shadow: var(--glow-cyan) !important;
}

[data-testid="stMetricLabel"] {
    font-size: 0.7rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}

[data-testid="stMetricValue"] {
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
}

/* ─── ALERTS ─── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    padding: 1rem 1.3rem !important;
}

.stSuccess {
    background: rgba(16,185,129,0.08) !important;
    border-color: rgba(16,185,129,0.3) !important;
    color: #6ee7b7 !important;
}

.stError {
    background: rgba(244,63,94,0.08) !important;
    border-color: rgba(244,63,94,0.3) !important;
    color: #fda4af !important;
}

.stWarning {
    background: rgba(245,158,11,0.08) !important;
    border-color: rgba(245,158,11,0.3) !important;
    color: #fcd34d !important;
}

.stInfo {
    background: rgba(56,189,248,0.06) !important;
    border-color: rgba(56,189,248,0.2) !important;
    color: #7dd3fc !important;
}

/* ─── PROGRESS BAR ─── */
[data-testid="stProgress"] > div {
    background: rgba(56,189,248,0.1) !important;
    border-radius: 999px !important;
    height: 6px !important;
}

[data-testid="stProgress"] > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue)) !important;
    border-radius: 999px !important;
    box-shadow: 0 0 10px rgba(56,189,248,0.5) !important;
}

/* ─── DIVIDER ─── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ─── SPINNER ─── */
[data-testid="stSpinner"] {
    color: var(--accent-cyan) !important;
}

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(56,189,248,0.25);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover { background: rgba(56,189,248,0.45); }

/* ─── COLUMN GAPS ─── */
[data-testid="stHorizontalBlock"] {
    gap: 1.5rem !important;
}

/* Hide radio button circles */
[data-testid="stSidebar"] .stRadio [data-testid="radio"] {
    display: none !important;
}

/* ─── CAPTION ─── */
.stCaption {
    color: var(--text-muted) !important;
    font-size: 0.82rem !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SIDEBAR ───
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <span class="logo-icon">⚕️</span>
        <div class="logo-title">MediAI Suite</div>
        <div class="logo-tagline">Clinical Intelligence Platform</div>
    </div>
    <div class="nav-label">Applications</div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Navigate",
        ["🩺  Diabetes Analyzer", "💰  Insurance Predictor"],
        label_visibility="collapsed"
    )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="status-badge">
        <div class="status-dot"></div>
        All ML models online
    </div>
    <br>
    <div style="font-size:0.68rem; color:#334155; text-align:center; letter-spacing:0.1em; text-transform:uppercase;">
        v2.0 · Built with Streamlit
    </div>
    """, unsafe_allow_html=True)

# ─── ROUTING ───
if page == "🩺  Diabetes Analyzer":
    diabetes_ui.run()
elif page == "💰  Insurance Predictor":
    insurance_ui.run()