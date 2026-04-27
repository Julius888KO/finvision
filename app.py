"""
FinVision — Dashboard Boursier.
Application Streamlit: vue d'ensemble, filtres, analyse stock, rankings.
"""

from __future__ import annotations

import pandas as pd
import streamlit as st

from data.loader import (
    load_universe_data,
    load_indices,
    load_stock_history,
    fetch_dividends,
    load_full_info,
    last_update_label,
)
from ui.styles import inject_css
from ui.components import (
    render_header,
    render_logo_sidebar,
    render_indices,
    render_kpis,
    render_main_table,
    render_stock_detail,
    render_ranking_list,
    render_news_panel,
    sector_ytd_chart,
    score_distribution_chart,
    reco_donut_chart,
)

# ---------- Config ----------

st.set_page_config(
    page_title="FinVision — Dashboard Boursier",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css(st)


# ---------- State ----------

if "selected_ticker" not in st.session_state:
    st.session_state.selected_ticker = None
if "nav" not in st.session_state:
    st.session_state.nav = "Vue d'ensemble"


# ---------- Data ----------

# Taille de l'univers chargé (modifiable via sidebar → Paramètres)
if "universe_size" not in st.session_state:
    st.session_state.universe_size = 300  # chargement confortable


@st.cache_data(ttl=1800, show_spinner=False)
def _get_data(size: int) -> pd.DataFrame:
    return load_universe_data(max_tickers=size)


with st.spinner(f"Chargement des données de marché ({st.session_state.universe_size} actions)..."):
    df = _get_data(st.session_state.universe_size)
    indices = load_indices()

if df is None or df.empty:
    st.error(
        "Aucune donnée récupérée. Causes possibles:\n"
        "- Connexion Internet indisponible\n"
        "- yfinance temporairement bloqué par Yahoo\n"
        "- Python 3.14 incompatible avec certaines dépendances (essayez Python 3.11/3.12)\n\n"
        "Relancez l'app après avoir vidé le cache : `python -m streamlit cache clear`"
    )
    st.stop()


# ---------- Sidebar ----------

with st.sidebar:
    render_logo_sidebar()

    nav_options = [
        "Vue d'ensemble",
        "Toutes les actions",
        "Meilleures performances",
        "Pires performances",
        "Sous -10%",
        "Sous -20%",
        "Entre -10% et -20%",
        "Actions à dividende",
        "Opportunités",
        "Pièges potentiels",
        "Portefeuille",
        "Paramètres",
    ]
    sel = st.radio(
        "Navigation",
        nav_options,
        label_visibility="collapsed",
        index=nav_options.index(st.session_state.nav) if st.session_state.nav in nav_options else 0,
        key="nav_radio",
    )
    st.session_state.nav = sel

    # Pro card
    st.markdown(
        """
        <div class="fv-pro-card">
          <div class="fv-pro-title">✦ Passez Pro</div>
          <div class="fv-pro-body">Accédez à des analyses avancées, des alertes et plus encore.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:.6rem; padding:.6rem .8rem; background:#151b2b; border-radius:12px; margin:0 .3rem;">
          <div style="width:34px; height:34px; border-radius:50%; background:linear-gradient(135deg,#7c5cff,#06b6d4); display:flex; align-items:center; justify-content:center; color:white; font-weight:700;">P</div>
          <div>
            <div style="color:#fff; font-weight:600; font-size:.88rem;">Paul Bonjour</div>
            <div style="color:#d8dde8; font-size:.75rem;">Premium</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Header ----------

render_header(last_update_label())


# ---------- Detail view (priority) ----------

if st.session_state.selected_ticker:
    ticker = st.session_state.selected_ticker
    row_df = df[df["Ticker"] == ticker]
    if row_df.empty:
        st.session_state.selected_ticker = None
        st.rerun()
    row = row_df.iloc[0]

    c_back, _ = st.columns([1, 8])
    with c_back:
        if st.button("← Retour", key="back_btn"):
            st.session_state.selected_ticker = None
            st.rerun()

    with st.spinner("Chargement des données du titre..."):
        history = load_stock_history(ticker, period="2y")
        divs = fetch_dividends(ticker)
        info = load_full_info(ticker)

    render_stock_detail(row, history, divs, info)
    st.stop()


# ---------- Filtering helpers ----------

def _apply_filters(
    df_in: pd.DataFrame,
    search: str,
    sectors: list,
    countries: list,
    cap_cats: list,
    perf_band: str,
    recos: list,
    score_min: int,
    dividend_only: bool,
) -> pd.DataFrame:
    out = df_in.copy()
    if search:
        s = search.lower().strip()
        mask = out["Ticker"].str.lower().str.contains(s, na=False) | out["Entreprise"].str.lower().str.contains(s, na=False)
        out = out[mask]
    if sectors:
        out = out[out["Secteur"].isin(sectors)]
    if countries:
        out = out[out["Pays"].isin(countries)]
    if cap_cats:
        out = out[out["Cap_Catégorie"].isin(cap_cats)]
    if perf_band and perf_band != "Toutes":
        if perf_band == "> +20%":
            out = out[out["YTD %"] > 20]
        elif perf_band == "0% à +20%":
            out = out[(out["YTD %"] >= 0) & (out["YTD %"] <= 20)]
        elif perf_band == "0% à -10%":
            out = out[(out["YTD %"] < 0) & (out["YTD %"] >= -10)]
        elif perf_band == "-10% à -20%":
            out = out[(out["YTD %"] < -10) & (out["YTD %"] >= -20)]
        elif perf_band == "< -20%":
            out = out[out["YTD %"] < -20]
    if recos:
        out = out[out["Recommandation"].isin(recos)]
    if score_min > 0:
        out = out[out["Score"] >= score_min]
    if dividend_only:
        out = out[out["Dividende_A"] == True]
    return out


def _filter_bar(df_in: pd.DataFrame, key: str = "filters"):
    """Barre de filtres complète. Retourne le DF filtré + option de tri."""
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(
            '<div style="display:flex; align-items:center; gap:.5rem; padding:.55rem .85rem; background:#151b2b; border:1px solid #232b42; border-radius:10px; color:#ffffff; font-weight:500;">⚙ Filtres avancés</div>',
            unsafe_allow_html=True,
        )
    with c2:
        search = st.text_input(
            "Rechercher",
            placeholder="Rechercher un ticker ou une entreprise...",
            key=f"{key}_search",
            label_visibility="collapsed",
        )

    f1, f2, f3, f4, f5, f6, f7 = st.columns(7)
    with f1:
        sectors = st.multiselect("Secteur", sorted(df_in["Secteur"].dropna().unique()), key=f"{key}_sec")
    with f2:
        countries = st.multiselect("Pays", sorted(df_in["Pays"].dropna().unique()), key=f"{key}_cnt")
    with f3:
        caps = st.multiselect(
            "Capitalisation",
            ["Mega Cap", "Large Cap", "Mid Cap", "Small Cap", "Micro Cap"],
            key=f"{key}_cap",
        )
    with f4:
        perf = st.selectbox(
            "Performance",
            ["Toutes", "> +20%", "0% à +20%", "0% à -10%", "-10% à -20%", "< -20%"],
            key=f"{key}_perf",
        )
    with f5:
        recos = st.multiselect("Recommandation", ["ACHAT", "SURVEILLANCE", "ÉVITER"], key=f"{key}_reco")
    with f6:
        score_min = st.slider("Score min.", 0, 100, 0, 5, key=f"{key}_score")
    with f7:
        dividend_only = st.checkbox("Dividende", key=f"{key}_div")

    sort_col, reset_col = st.columns([3, 1])
    with sort_col:
        sort_by = st.selectbox(
            "Trier par",
            ["Score (↓)", "YTD % (↓)", "YTD % (↑)", "Capitalisation (↓)", "Dividende (↓)"],
            key=f"{key}_sort",
        )
    with reset_col:
        st.markdown("<div style='height: 1.75rem;'></div>", unsafe_allow_html=True)
        if st.button("Réinitialiser", key=f"{key}_reset", use_container_width=True):
            for k in [f"{key}_search", f"{key}_sec", f"{key}_cnt", f"{key}_cap", f"{key}_perf", f"{key}_reco", f"{key}_score", f"{key}_div"]:
                if k in st.session_state:
                    del st.session_state[k]
            st.rerun()

    filtered = _apply_filters(df_in, search, sectors, countries, caps, perf, recos, score_min, dividend_only)

    # Tri
    sort_map = {
        "Score (↓)": ("Score", False),
        "YTD % (↓)": ("YTD %", False),
        "YTD % (↑)": ("YTD %", True),
        "Capitalisation (↓)": ("Capitalisation", False),
        "Dividende (↓)": ("Dividende_Yield", False),
    }
    col, asc = sort_map[sort_by]
    filtered = filtered.sort_values(col, ascending=asc, na_position="last")
    return filtered


def _stock_selector(filtered: pd.DataFrame, key: str = "sel"):
    """Sélecteur pour ouvrir le détail d'un titre."""
    if filtered.empty:
        return
    opts = ["— Ouvrir un titre —"] + [f"{r['Ticker']}  |  {r['Entreprise']}" for _, r in filtered.head(500).iterrows()]
    choice = st.selectbox("Ouvrir la fiche détaillée", opts, key=key, label_visibility="collapsed")
    if choice and choice != opts[0]:
        ticker = choice.split("|")[0].strip()
        st.session_state.selected_ticker = ticker
        st.rerun()


# ---------- Views ----------

def view_overview():
    render_indices(indices)
    st.markdown("<br/>", unsafe_allow_html=True)
    render_kpis(df)
    st.markdown("<br/>", unsafe_allow_html=True)

    # Filters
    filtered = _filter_bar(df, key="ov")

    # Main layout: table on left, side panels on right
    left, right = st.columns([2.3, 1])

    with left:
        render_main_table(filtered, page_size=12, key="ov_tbl")
        st.markdown("<br/>", unsafe_allow_html=True)
        _stock_selector(filtered, key="ov_open")

    with right:
        # Reco donut
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Répartition des recommandations</div>', unsafe_allow_html=True)
        total = len(filtered)
        if total > 0:
            c_chart, c_legend = st.columns([1, 1])
            with c_chart:
                st.plotly_chart(reco_donut_chart(filtered), use_container_width=True, config={"displayModeBar": False})
            with c_legend:
                achat = int((filtered["Recommandation"] == "ACHAT").sum())
                surv = int((filtered["Recommandation"] == "SURVEILLANCE").sum())
                evt = int((filtered["Recommandation"] == "ÉVITER").sum())
                st.markdown(
                    f"""
                    <div style="padding-top:.5rem;">
                      <div style="display:flex; align-items:center; gap:.5rem; margin-bottom:.6rem;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#22c55e;"></span>
                        <div><div style="color:#4ade80; font-weight:600;">ACHAT</div><div style="color:#d8dde8; font-size:.78rem;">{achat} ({achat/total*100:.1f}%)</div></div>
                      </div>
                      <div style="display:flex; align-items:center; gap:.5rem; margin-bottom:.6rem;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#eab308;"></span>
                        <div><div style="color:#fbbf24; font-weight:600;">SURVEILLANCE</div><div style="color:#d8dde8; font-size:.78rem;">{surv} ({surv/total*100:.1f}%)</div></div>
                      </div>
                      <div style="display:flex; align-items:center; gap:.5rem;">
                        <span style="width:10px; height:10px; border-radius:50%; background:#ef4444;"></span>
                        <div><div style="color:#f87171; font-weight:600;">ÉVITER</div><div style="color:#d8dde8; font-size:.78rem;">{evt} ({evt/total*100:.1f}%)</div></div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<br/>", unsafe_allow_html=True)

        # Top 5 opportunités
        top5 = filtered[filtered["Recommandation"] == "ACHAT"].nlargest(5, "Score")
        render_ranking_list(top5, "Top 5 Opportunités", 5)

        st.markdown("<br/>", unsafe_allow_html=True)

        # News
        render_news_panel(filtered)

    st.markdown("<br/><br/>", unsafe_allow_html=True)

    # Bottom charts: sector YTD, score distribution
    cb1, cb2 = st.columns([1.5, 1])
    with cb1:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Performance YTD par secteur</div>', unsafe_allow_html=True)
        st.plotly_chart(sector_ytd_chart(filtered), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
    with cb2:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Distribution des scores</div>', unsafe_allow_html=True)
        st.plotly_chart(score_distribution_chart(filtered), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


def view_all_stocks():
    filtered = _filter_bar(df, key="all")
    render_main_table(filtered, page_size=25, key="all_tbl")
    st.markdown("<br/>", unsafe_allow_html=True)
    _stock_selector(filtered, key="all_open")


def view_sub(title: str, sub: pd.DataFrame, key: str):
    st.markdown(f"### {title}")
    st.markdown(f'<div style="color:#d8dde8; margin-bottom:1rem;">{len(sub):,} actions</div>', unsafe_allow_html=True)
    filtered = _filter_bar(sub, key=key)
    render_main_table(filtered, page_size=25, key=f"{key}_tbl")
    st.markdown("<br/>", unsafe_allow_html=True)
    _stock_selector(filtered, key=f"{key}_open")


def view_rankings():
    c1, c2, c3 = st.columns(3)
    with c1:
        render_ranking_list(
            df[df["Recommandation"] == "ACHAT"].nlargest(10, "Score"),
            "Top 10 Opportunités",
            10,
        )
    with c2:
        render_ranking_list(df.nlargest(10, "YTD %"), "Top 10 Meilleures performances", 10)
    with c3:
        render_ranking_list(df.nsmallest(10, "YTD %"), "Top 10 Pires performances", 10)

    st.markdown("<br/>", unsafe_allow_html=True)

    c4, c5 = st.columns(2)
    with c4:
        render_ranking_list(df[df["Profil"] == "Piège de valeur"].head(5), "Top 5 Pièges de valeur", 5)
    with c5:
        oversold = df[(df["RSI"] < 35) & (df["Score"] >= 60)].nlargest(5, "Score")
        render_ranking_list(oversold, "Top 5 Survendues de qualité", 5)


def view_portfolio():
    st.markdown("### Portefeuille")
    st.markdown(
        '<div style="color:#d8dde8;">Simulateur de portefeuille basé sur les recommandations ACHAT.</div>',
        unsafe_allow_html=True,
    )
    buys = df[df["Recommandation"] == "ACHAT"].nlargest(10, "Score").copy()
    if buys.empty:
        st.info("Aucune action ACHAT dans les filtres actuels.")
        return

    # Pondération par score
    buys["Poids %"] = (buys["Score"] / buys["Score"].sum() * 100).round(2)

    st.markdown("<br/>", unsafe_allow_html=True)
    cols = st.columns([2, 1])
    with cols[0]:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Allocation suggérée (Top 10 ACHAT)</div>', unsafe_allow_html=True)
        disp = buys[["Ticker", "Entreprise", "Secteur", "Score", "Poids %", "YTD %", "Recommandation"]].reset_index(drop=True)
        st.dataframe(disp, use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)
    with cols[1]:
        import plotly.graph_objects as go

        fig = go.Figure(
            go.Pie(
                labels=buys["Ticker"],
                values=buys["Poids %"],
                hole=0.55,
                marker=dict(line=dict(color="#0f1420", width=2)),
                textinfo="label+percent",
                textfont=dict(color="white", size=11),
            )
        )
        fig.update_layout(
            height=340, margin=dict(l=0, r=0, t=0, b=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
        )
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Répartition</div>', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)


def view_settings():
    st.markdown("### Paramètres")
    st.markdown(
        """
        <div class="fv-panel">
          <div class="fv-panel-title">Cache</div>
          <div style="color:#d8dde8; margin-bottom:1rem;">Videz le cache pour rafraîchir les données de marché.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("🔄 Rafraîchir toutes les données", type="primary"):
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="fv-panel">
          <div class="fv-panel-title">Taille de l'univers</div>
          <div style="color:#d8dde8; margin-bottom:.6rem;">
            Nombre d'actions à charger. Plus d'actions = chargement plus long.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    size = st.select_slider(
        "Actions chargées",
        options=[100, 200, 300, 500, 700, 900],
        value=st.session_state.universe_size,
        key="universe_size_slider",
    )
    if size != st.session_state.universe_size:
        st.session_state.universe_size = size
        st.cache_data.clear()
        st.rerun()

    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="fv-panel">
          <div class="fv-panel-title">À propos</div>
          <div style="color:#ffffff; line-height:1.7;">
            <b>FinVision</b> — Dashboard boursier pour investisseurs et traders.<br/>
            <span style="color:#d8dde8;">Source de données: Yahoo Finance (yfinance). YTD calculé depuis le 1er janvier 2026.</span><br/>
            <span style="color:#d8dde8;">Univers couvert: {len(df):,} actions US + Europe.</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Routing ----------

nav = st.session_state.nav

if nav == "Vue d'ensemble":
    view_overview()
elif nav == "Toutes les actions":
    view_all_stocks()
elif nav == "Meilleures performances":
    view_sub("Meilleures performances", df.nlargest(min(200, len(df)), "YTD %"), "best")
elif nav == "Pires performances":
    view_sub("Pires performances", df.nsmallest(min(200, len(df)), "YTD %"), "worst")
elif nav == "Sous -10%":
    view_sub("Actions sous -10% YTD", df[df["YTD %"] <= -10], "sub10")
elif nav == "Sous -20%":
    view_sub("Actions sous -20% YTD", df[df["YTD %"] <= -20], "sub20")
elif nav == "Entre -10% et -20%":
    view_sub("Entre -10% et -20% YTD", df[(df["YTD %"] <= -10) & (df["YTD %"] > -20)], "between")
elif nav == "Actions à dividende":
    view_sub("Actions à dividende", df[df["Dividende_A"] == True], "div")
elif nav == "Opportunités":
    view_sub("Opportunités (ACHAT)", df[df["Recommandation"] == "ACHAT"].sort_values("Score", ascending=False), "opp")
elif nav == "Pièges potentiels":
    view_sub("Pièges potentiels", df[(df["Recommandation"] == "ÉVITER") | (df["Profil"] == "Piège de valeur")], "trap")
elif nav == "Portefeuille":
    view_portfolio()
elif nav == "Paramètres":
    view_settings()
else:
    view_overview()
