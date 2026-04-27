"""Design system: dark premium. Inspiré TradingView / fintech moderne."""

CSS = """
<style>
/* ========= GLOBAL ========= */
:root {
    --bg-0: #0a0e17;
    --bg-1: #0f1420;
    --bg-2: #151b2b;
    --bg-3: #1c2337;
    --bg-hover: #1f2740;
    --border: #232b42;
    --border-soft: #1a2135;
    --text-0: #ffffff;
    --text-1: #ffffff;
    --text-2: #d8dde8;
    --text-3: #b8c0d0;
    --accent: #7c5cff;
    --accent-2: #9b7bff;
    --green: #22c55e;
    --green-soft: #16a34a;
    --red: #ef4444;
    --red-soft: #dc2626;
    --yellow: #eab308;
    --orange: #f59e0b;
    --blue: #3b82f6;
    --cyan: #06b6d4;
}

html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif !important;
    -webkit-font-smoothing: antialiased;
}

.stApp {
    background: var(--bg-0) !important;
    color: var(--text-1);
}

.main .block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 100% !important;
}

/* Hide Streamlit chrome */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ========= SIDEBAR ========= */
[data-testid="stSidebar"] {
    background: var(--bg-1) !important;
    border-right: 1px solid var(--border-soft);
}
[data-testid="stSidebar"] > div {
    padding-top: 0.5rem;
}

/* ========= HEADER ========= */
.fv-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 1.25rem;
}
.fv-title {
    font-size: 2rem;
    font-weight: 700;
    color: var(--text-0);
    letter-spacing: -0.02em;
    margin: 0;
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.fv-title .spark { color: var(--accent); }
.fv-subtitle {
    color: var(--text-2);
    font-size: 0.95rem;
    margin-top: 0.35rem;
}
.fv-last-update {
    color: var(--text-2);
    font-size: 0.85rem;
    text-align: right;
}
.fv-last-update .value {
    color: var(--text-1);
    font-weight: 500;
    font-size: 0.92rem;
    display: flex;
    align-items: center;
    gap: 0.4rem;
    justify-content: flex-end;
}
.fv-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 10px rgba(34,197,94,.6);
    display: inline-block;
}

/* ========= LOGO ========= */
.fv-logo {
    padding: 1rem 1.25rem 1.25rem 1.25rem;
    border-bottom: 1px solid var(--border-soft);
    margin-bottom: 0.75rem;
}
.fv-logo-row {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-weight: 700;
    font-size: 1.15rem;
    color: var(--text-0);
}
.fv-logo-icon {
    width: 26px; height: 26px;
    border-radius: 6px;
    background: linear-gradient(135deg, var(--accent) 0%, var(--cyan) 100%);
    display: inline-flex; align-items: center; justify-content: center;
    color: white; font-size: 0.85rem; font-weight: 800;
}
.fv-logo-tagline {
    color: var(--text-2);
    font-size: 0.78rem;
    margin-top: 0.35rem;
    line-height: 1.35;
}

/* ========= INDEX CARDS ========= */
.fv-index-card {
    background: var(--bg-2);
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    min-height: 98px;
}
.fv-index-name {
    color: var(--text-2);
    font-size: 0.8rem;
    font-weight: 500;
    margin-bottom: 0.2rem;
}
.fv-index-price {
    color: var(--text-0);
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: -0.01em;
}
.fv-index-change { font-size: 0.82rem; font-weight: 600; margin-top: 0.15rem; }
.fv-up { color: var(--green); }
.fv-down { color: var(--red); }

.fv-market-open {
    background: linear-gradient(135deg, #3b2b75 0%, #4f2d8a 100%);
    border: 1px solid rgba(156,122,255,.3);
    color: white;
}
.fv-market-open .label { font-size: 0.85rem; color: #e4deff; font-weight: 600; }
.fv-market-open .zones {
    font-size: 0.85rem;
    color: white;
    margin-top: 0.55rem;
    display: flex; gap: 0.8rem; align-items: center;
}

/* ========= KPI CARDS ========= */
.fv-kpi {
    background: var(--bg-2);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 1rem 1.15rem;
    position: relative;
    min-height: 118px;
    display: flex; flex-direction: column; justify-content: center;
}
.fv-kpi-head {
    display: flex; align-items: center; gap: 0.55rem;
    color: var(--text-2); font-size: 0.82rem; font-weight: 500;
    margin-bottom: 0.35rem;
}
.fv-kpi-icon {
    width: 26px; height: 26px; border-radius: 7px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 0.85rem;
}
.fv-kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.1;
    color: var(--text-0);
}
.fv-kpi-sub {
    color: var(--text-2);
    font-size: 0.78rem;
    margin-top: 0.25rem;
}

.kpi-blue { background: linear-gradient(135deg, rgba(59,130,246,.08), var(--bg-2)); border-color: rgba(59,130,246,.2); }
.kpi-blue .fv-kpi-icon { background: rgba(59,130,246,.15); color: var(--blue); }
.kpi-green { background: linear-gradient(135deg, rgba(34,197,94,.08), var(--bg-2)); border-color: rgba(34,197,94,.2); }
.kpi-green .fv-kpi-icon { background: rgba(34,197,94,.15); color: var(--green); }
.kpi-green .fv-kpi-value { color: var(--green); }
.kpi-red { background: linear-gradient(135deg, rgba(239,68,68,.08), var(--bg-2)); border-color: rgba(239,68,68,.2); }
.kpi-red .fv-kpi-icon { background: rgba(239,68,68,.15); color: var(--red); }
.kpi-red .fv-kpi-value { color: var(--red); }
.kpi-orange { background: linear-gradient(135deg, rgba(245,158,11,.08), var(--bg-2)); border-color: rgba(245,158,11,.2); }
.kpi-orange .fv-kpi-icon { background: rgba(245,158,11,.15); color: var(--orange); }
.kpi-orange .fv-kpi-value { color: var(--orange); }
.kpi-violet { background: linear-gradient(135deg, rgba(124,92,255,.08), var(--bg-2)); border-color: rgba(124,92,255,.2); }
.kpi-violet .fv-kpi-icon { background: rgba(124,92,255,.15); color: var(--accent); }
.kpi-cyan { background: linear-gradient(135deg, rgba(6,182,212,.08), var(--bg-2)); border-color: rgba(6,182,212,.2); }
.kpi-cyan .fv-kpi-icon { background: rgba(6,182,212,.15); color: var(--cyan); }
.kpi-cyan .fv-kpi-value { color: var(--cyan); }

/* ========= SECTION / PANELS ========= */
.fv-panel {
    background: var(--bg-2);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 1.15rem 1.25rem;
}
.fv-panel-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-0);
    margin: 0 0 0.9rem 0;
    display: flex; align-items: center; justify-content: space-between;
    gap: 0.5rem;
}
.fv-panel-sub { color: var(--text-2); font-size: 0.85rem; }

/* ========= TABLE ========= */
.fv-table-wrap {
    background: var(--bg-2);
    border: 1px solid var(--border-soft);
    border-radius: 14px;
    padding: 1rem 1.15rem 0.5rem 1.15rem;
}
.fv-table-head {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-0);
    margin: 0 0 0.8rem 0;
}
.fv-count { color: var(--text-2); font-size: 0.85rem; font-weight: 400; margin-left: 0.5rem; }

[data-testid="stDataFrame"] {
    background: transparent;
}
[data-testid="stDataFrame"] div[role="grid"] {
    background: transparent !important;
    border: none !important;
}

/* ========= BADGES ========= */
.fv-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 0.22rem 0.75rem;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.01em;
}
.badge-achat { background: rgba(34,197,94,.16); color: #4ade80; border: 1px solid rgba(34,197,94,.3); }
.badge-surv { background: rgba(234,179,8,.14); color: #fbbf24; border: 1px solid rgba(234,179,8,.3); }
.badge-eviter { background: rgba(239,68,68,.14); color: #f87171; border: 1px solid rgba(239,68,68,.3); }
.badge-neutral { background: var(--bg-3); color: var(--text-1); border: 1px solid var(--border); }

/* ========= INPUTS ========= */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: var(--bg-2) !important;
    border: 1px solid var(--border) !important;
    color: var(--text-1) !important;
    border-radius: 10px !important;
}
.stTextInput input::placeholder { color: var(--text-3) !important; }

.stButton > button {
    background: var(--bg-2);
    border: 1px solid var(--border);
    color: var(--text-1);
    border-radius: 10px;
    padding: 0.5rem 1rem;
    font-weight: 500;
    transition: all .15s ease;
}
.stButton > button:hover {
    border-color: var(--accent);
    color: white;
    background: var(--bg-3);
}

/* Primary button */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent-2) 100%);
    border: none;
    color: white;
}

/* ========= TABS ========= */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.25rem;
    background: var(--bg-1);
    padding: 0.3rem;
    border-radius: 12px;
    border: 1px solid var(--border-soft);
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: var(--text-2) !important;
    font-weight: 500 !important;
    padding: 0.5rem 1rem !important;
    border: none !important;
}
.stTabs [aria-selected="true"] {
    background: var(--bg-3) !important;
    color: var(--text-0) !important;
}

/* ========= RADIO (sidebar nav) ========= */
[data-testid="stSidebar"] .stRadio > div {
    gap: 0.15rem;
}
[data-testid="stSidebar"] .stRadio label {
    background: transparent;
    border-radius: 10px;
    padding: 0.55rem 0.8rem;
    color: var(--text-1);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.15s ease;
    width: 100%;
    display: flex; align-items: center;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: var(--bg-2);
}

/* ========= SCROLLBARS ========= */
::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: var(--bg-0); }
::-webkit-scrollbar-thumb { background: var(--bg-3); border-radius: 10px; border: 2px solid var(--bg-0); }
::-webkit-scrollbar-thumb:hover { background: #2a3350; }

/* ========= MISC ========= */
h1, h2, h3, h4 { color: var(--text-0) !important; letter-spacing: -0.01em; }
p, li, span { color: var(--text-1) !important; }
hr { border-color: var(--border-soft); }

/* Force readable defaults for Streamlit widgets */
label, .stMarkdown p, .stMarkdown li, .stCaption, [data-testid="stMarkdownContainer"] p,
[data-testid="stWidgetLabel"] p, [data-testid="stWidgetLabel"] label {
    color: var(--text-1) !important;
}

/* Slider, select labels, multiselect tags */
[data-baseweb="tag"] { background: var(--bg-3) !important; color: var(--text-0) !important; }
[data-baseweb="select"] div { color: var(--text-1) !important; }
[data-baseweb="popover"] { background: var(--bg-2) !important; }
[data-baseweb="menu"] li { color: var(--text-1) !important; }
[data-baseweb="menu"] li:hover { background: var(--bg-3) !important; }

/* Checkbox */
[data-testid="stCheckbox"] label { color: var(--text-1) !important; }

/* Streamlit dataframe text */
[data-testid="stDataFrame"] * { color: var(--text-1) !important; }
[data-testid="stDataFrame"] [role="columnheader"] {
    color: var(--text-0) !important; font-weight: 600 !important;
}

/* Alerts */
[data-testid="stAlert"] { background: var(--bg-2) !important; border: 1px solid var(--border) !important; color: var(--text-1) !important; }
[data-testid="stAlert"] * { color: var(--text-1) !important; }

.fv-news-item {
    display: flex;
    gap: 0.85rem;
    padding: 0.8rem 0;
    border-bottom: 1px solid var(--border-soft);
}
.fv-news-item:last-child { border-bottom: none; }
.fv-news-icon {
    width: 34px; height: 34px;
    border-radius: 8px;
    background: var(--bg-3);
    flex-shrink: 0;
    display: inline-flex; align-items: center; justify-content: center;
}
.fv-news-title { color: var(--text-0); font-weight: 500; font-size: 0.92rem; }
.fv-news-meta { color: var(--text-2); font-size: 0.78rem; margin-top: 0.15rem; }
.fv-news-body { color: var(--text-2); font-size: 0.82rem; margin-top: 0.25rem; line-height: 1.4; }

/* Metric card for detail */
.fv-metric {
    background: var(--bg-2);
    border: 1px solid var(--border-soft);
    border-radius: 10px;
    padding: 0.85rem 1rem;
}
.fv-metric-label { color: var(--text-2); font-size: 0.78rem; }
.fv-metric-value { color: var(--text-0); font-size: 1.15rem; font-weight: 600; margin-top: 0.2rem; }

/* Score pill */
.fv-score-pill {
    display: inline-flex; align-items: center; justify-content: center;
    min-width: 38px;
    height: 26px;
    padding: 0 0.55rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 700;
}
.score-high { background: rgba(34,197,94,.18); color: #4ade80; }
.score-mid { background: rgba(234,179,8,.15); color: #fbbf24; }
.score-low { background: rgba(239,68,68,.15); color: #f87171; }

/* User card bottom sidebar */
.fv-pro-card {
    background: linear-gradient(135deg, rgba(124,92,255,.15), rgba(6,182,212,.08));
    border: 1px solid rgba(124,92,255,.3);
    border-radius: 14px;
    padding: 1rem;
    margin: 1rem 0.5rem 0.5rem 0.5rem;
}
.fv-pro-title { color: var(--text-0); font-weight: 700; margin-bottom: 0.3rem; }
.fv-pro-body { color: var(--text-2); font-size: 0.82rem; margin-bottom: 0.7rem; }

/* Empty / loading */
.fv-empty {
    text-align: center;
    color: var(--text-2);
    padding: 3rem 1rem;
    background: var(--bg-2);
    border: 1px dashed var(--border);
    border-radius: 14px;
}
</style>
"""


def inject_css(st_module):
    st_module.markdown(CSS, unsafe_allow_html=True)
