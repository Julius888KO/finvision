"""Composants UI réutilisables (header, KPI, table, détail)."""

from __future__ import annotations

import html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components


# ---------- Formatters ----------

def fmt_pct(v, decimals: int = 2) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"{v:+.{decimals}f}%"


def fmt_price(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"${v:,.2f}"


def fmt_number(v, decimals: int = 2) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"{v:,.{decimals}f}"


def fmt_ratio_pct(v, decimals: int = 2) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"{v*100:+.{decimals}f}%"


def fmt_cap(mc) -> str:
    if mc is None or (isinstance(mc, float) and np.isnan(mc)):
        return "—"
    try:
        mc = float(mc)
    except Exception:
        return "—"
    if mc >= 1e12: return f"${mc/1e12:.2f}T"
    if mc >= 1e9: return f"${mc/1e9:.2f}B"
    if mc >= 1e6: return f"${mc/1e6:.2f}M"
    return f"${mc:,.0f}"


# ---------- Header ----------

def render_header(last_update: str):
    st.markdown(
        f"""
        <div class="fv-header">
          <div>
            <h1 class="fv-title">Dashboard Boursier <span class="spark">✦</span></h1>
            <div class="fv-subtitle">Analyse complète du marché pour des décisions d'investissement éclairées</div>
          </div>
          <div class="fv-last-update">
            Dernière mise à jour
            <div class="value">{last_update} <span class="fv-dot"></span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_logo_sidebar():
    st.markdown(
        """
        <div class="fv-logo">
          <div class="fv-logo-row">
            <span class="fv-logo-icon">▲</span> FinVision
          </div>
          <div class="fv-logo-tagline">Prenez de meilleures<br/>décisions en Bourse</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ---------- Indices strip ----------

def _sparkline(values: list[float], color: str, height: int = 40) -> go.Figure:
    if not values:
        values = [0, 0]
    fig = go.Figure(
        go.Scatter(
            y=values,
            mode="lines",
            line=dict(color=color, width=2, shape="spline"),
            fill="tozeroy",
            fillcolor=f"rgba({_hex_to_rgb(color)},.12)",
            hoverinfo="skip",
        )
    )
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False,
    )
    return fig


def _hex_to_rgb(h: str) -> str:
    h = h.lstrip("#")
    return f"{int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)}"


def render_indices(indices: dict):
    cols = st.columns([1, 1, 1, 1, 1, 1])
    items = list(indices.items())
    for i in range(5):
        if i >= len(items):
            continue
        name, d = items[i]
        with cols[i]:
            price = d.get("price")
            chg = d.get("change_pct")
            color = "#22c55e" if (chg or 0) >= 0 else "#ef4444"
            cls = "fv-up" if (chg or 0) >= 0 else "fv-down"
            price_txt = f"{price:,.2f}" if price is not None else "—"
            chg_txt = f"{chg:+.2f}%" if chg is not None else "—"
            st.markdown(
                f"""
                <div class="fv-index-card">
                  <div class="fv-index-name">{name}</div>
                  <div class="fv-index-price">{price_txt}</div>
                """,
                unsafe_allow_html=True,
            )
            st.plotly_chart(
                _sparkline(d.get("history", []), color, height=38),
                use_container_width=True,
                config={"displayModeBar": False},
            )
            st.markdown(
                f'<div class="fv-index-change {cls}">{chg_txt}</div></div>',
                unsafe_allow_html=True,
            )
    # Market open card
    with cols[5]:
        st.markdown(
            """
            <div class="fv-index-card fv-market-open">
              <div class="label">Marchés Ouverts</div>
              <div class="zones">US &nbsp; • &nbsp; EU &nbsp; • &nbsp; ASIE</div>
              <div style="text-align:right; margin-top:.35rem; font-size:1.4rem;">🌐</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------- KPI cards ----------

def render_kpis(df: pd.DataFrame):
    total = len(df)
    avg_ytd = df["YTD %"].mean() if total else None
    below10 = int((df["YTD %"] <= -10).sum())
    below20 = int((df["YTD %"] <= -20).sum())
    div_count = int(df["Dividende_A"].sum()) if "Dividende_A" in df.columns else 0
    avg_score = df["Score"].mean() if total else 0
    achat = int((df["Recommandation"] == "ACHAT").sum())
    surv = int((df["Recommandation"] == "SURVEILLANCE").sum())
    evt = int((df["Recommandation"] == "ÉVITER").sum())

    cards = [
        ("kpi-blue", "👥", "Total actions", f"{total:,}", "Univers couvert"),
        ("kpi-green", "📈", "YTD moyen", f"{avg_ytd:+.2f}%" if avg_ytd is not None else "—", "Performance moyenne"),
        ("kpi-red", "⏱", "Sous -10%", f"{below10:,}", f"{_safe_pct(below10, total)} du total"),
        ("kpi-red", "⚠", "Sous -20%", f"{below20:,}", f"{_safe_pct(below20, total)} du total"),
        ("kpi-cyan", "💎", "Actions à dividende", f"{div_count:,}", f"{_safe_pct(div_count, total)} du total"),
        ("kpi-violet", "⚙", "Score moyen", f"{avg_score:.1f}/100" if avg_score else "—", "Score global"),
        ("kpi-green", "✔", "ACHAT", f"{achat:,}", f"{_safe_pct(achat, total)} du total"),
        ("kpi-orange", "◐", "SURVEILLANCE", f"{surv:,}", f"{_safe_pct(surv, total)} du total"),
        ("kpi-red", "✕", "ÉVITER", f"{evt:,}", f"{_safe_pct(evt, total)} du total"),
    ]

    # Rendu en 2 lignes pour éviter la surcharge : 5 + 4
    row = st.columns(9)
    for i, (cls, icon, title, value, sub) in enumerate(cards):
        with row[i]:
            st.markdown(
                f"""
                <div class="fv-kpi {cls}">
                  <div class="fv-kpi-head"><span class="fv-kpi-icon">{icon}</span> {title}</div>
                  <div class="fv-kpi-value">{value}</div>
                  <div class="fv-kpi-sub">{sub}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def _safe_pct(n, total):
    if not total:
        return "0.0%"
    return f"{n/total*100:.1f}%"


# ---------- Main table ----------

def _ytd_html(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    color = "#22c55e" if v >= 0 else "#ef4444"
    return f'<span style="color:{color};font-weight:600">{v:+.2f}%</span>'


def _score_html(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    cls = "score-high" if v >= 70 else ("score-mid" if v >= 50 else "score-low")
    return f'<span class="fv-score-pill {cls}">{int(round(v))}</span>'


def _reco_html(r):
    if r == "ACHAT":
        return '<span class="fv-badge badge-achat">ACHAT</span>'
    if r == "SURVEILLANCE":
        return '<span class="fv-badge badge-surv">SURVEILLANCE</span>'
    if r == "ÉVITER":
        return '<span class="fv-badge badge-eviter">ÉVITER</span>'
    return f'<span class="fv-badge badge-neutral">{r or "—"}</span>'


def _risk_html(r):
    colors = {"Faible": "#4ade80", "Moyen": "#fbbf24", "Élevé": "#f87171"}
    c = colors.get(r, "#d8dde8")
    return f'<span style="color:{c};font-weight:500">{r or "—"}</span>'


def _conv_html(c):
    colors = {"Élevée": "#4ade80", "Moyenne": "#fbbf24", "Faible": "#d8dde8"}
    return f'<span style="color:{colors.get(c,"#d8dde8")};font-weight:500">{c or "—"}</span>'


def _div_html(v):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "—"
    return f"{v*100:.2f}%"


def render_main_table(df: pd.DataFrame, page_size: int = 12, key: str = "main_table"):
    """Rendu HTML de la table — premium, rapide, sans surcharge."""
    if df is None or df.empty:
        st.markdown('<div class="fv-empty">Aucun résultat avec les filtres actuels.</div>', unsafe_allow_html=True)
        return

    total = len(df)
    # Pagination state
    page_key = f"{key}_page"
    size_key = f"{key}_size"
    if page_key not in st.session_state:
        st.session_state[page_key] = 1
    if size_key not in st.session_state:
        st.session_state[size_key] = page_size

    size = st.session_state[size_key]
    pages = max(1, (total + size - 1) // size)
    page = min(st.session_state[page_key], pages)

    start = (page - 1) * size
    end = start + size
    sub = df.iloc[start:end]

    # Build rows
    rows_html = []
    for _, r in sub.iterrows():
        rows_html.append(
            f"""
            <tr>
              <td class="col-ticker">{html.escape(str(r['Ticker']))}</td>
              <td class="col-name">{html.escape(str(r['Entreprise'])[:32])}</td>
              <td class="col-dim">{html.escape(str(r['Secteur'])[:18])}</td>
              <td class="col-dim">{html.escape(str(r['Pays'])[:12])}</td>
              <td class="col-right col-light">{r.get('Cap_Label','—')}</td>
              <td class="col-right">{_ytd_html(r.get('YTD %'))}</td>
              <td class="col-right col-light">{fmt_price(r.get('Prix'))}</td>
              <td class="col-right col-dim">{_div_html(r.get('Dividende_Yield'))}</td>
              <td class="col-center">{_score_html(r.get('Score'))}</td>
              <td>{_risk_html(r.get('Risque'))}</td>
              <td>{_conv_html(r.get('Conviction'))}</td>
              <td class="col-light">{html.escape(str(r.get('Profil','—')))}</td>
              <td class="col-center">{_reco_html(r.get('Recommandation'))}</td>
            </tr>
            """
        )

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8" />
    <style>
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        padding: 0;
        background: #0a0e17;
        color: #ffffff;
        font-family: -apple-system, BlinkMacSystemFont, "Inter", "Segoe UI", Roboto, sans-serif;
        -webkit-font-smoothing: antialiased;
      }}
      .wrap {{
        background: #151b2b;
        border: 1px solid #1a2135;
        border-radius: 14px;
        padding: 1rem 1.15rem;
      }}
      .title {{
        font-size: 1rem;
        font-weight: 600;
        color: #ffffff;
        margin-bottom: 0.8rem;
      }}
      .count {{
        color: #d8dde8;
        font-size: .85rem;
        font-weight: 400;
        margin-left: 0.5rem;
      }}
      table {{ width: 100%; border-collapse: collapse; font-size: 0.9rem; }}
      thead tr {{
        color: #d8dde8;
        font-size: .72rem;
        text-transform: uppercase;
        letter-spacing: .06em;
        border-bottom: 1px solid #1a2135;
      }}
      th {{ padding: .7rem .4rem; text-align: left; font-weight: 600; }}
      th.col-right {{ text-align: right; }}
      th.col-center {{ text-align: center; }}
      tbody tr {{ border-bottom: 1px solid #1c2337; }}
      tbody tr:hover {{ background: #1a2135; }}
      td {{ padding: .75rem .4rem; color: #ffffff; }}
      .col-ticker {{ font-weight: 700; color: #ffffff; }}
      .col-name {{ color: #ffffff; }}
      .col-dim {{ color: #d8dde8; }}
      .col-light {{ color: #ffffff; }}
      .col-right {{ text-align: right; }}
      .col-center {{ text-align: center; }}

      .fv-badge {{
        display: inline-block;
        padding: .24rem .75rem;
        border-radius: 999px;
        font-size: .78rem;
        font-weight: 700;
      }}
      .badge-achat {{ background: rgba(34,197,94,.18); color: #4ade80; border: 1px solid rgba(34,197,94,.35); }}
      .badge-surv {{ background: rgba(234,179,8,.16); color: #fbbf24; border: 1px solid rgba(234,179,8,.35); }}
      .badge-eviter {{ background: rgba(239,68,68,.16); color: #f87171; border: 1px solid rgba(239,68,68,.35); }}
      .badge-neutral {{ background: #1c2337; color: #ffffff; border: 1px solid #232b42; }}

      .fv-score-pill {{
        display: inline-block;
        min-width: 40px;
        padding: .22rem .6rem;
        border-radius: 999px;
        font-size: .82rem;
        font-weight: 700;
        text-align: center;
      }}
      .score-high {{ background: rgba(34,197,94,.2); color: #4ade80; }}
      .score-mid {{ background: rgba(234,179,8,.18); color: #fbbf24; }}
      .score-low {{ background: rgba(239,68,68,.18); color: #f87171; }}

      ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
      ::-webkit-scrollbar-thumb {{ background: #2a3350; border-radius: 10px; }}
      ::-webkit-scrollbar-track {{ background: #0a0e17; }}
    </style>
    </head>
    <body>
      <div class="wrap">
        <div class="title">Toutes les actions <span class="count">{total:,} résultats</span></div>
        <table>
          <thead>
            <tr>
              <th>Ticker</th>
              <th>Entreprise</th>
              <th>Secteur</th>
              <th>Pays</th>
              <th class="col-right">Cap. boursière</th>
              <th class="col-right">YTD %</th>
              <th class="col-right">Prix</th>
              <th class="col-right">Dividende</th>
              <th class="col-center">Score</th>
              <th>Risque</th>
              <th>Conviction</th>
              <th>Profil</th>
              <th class="col-center">Recommandation</th>
            </tr>
          </thead>
          <tbody>
            {''.join(rows_html)}
          </tbody>
        </table>
      </div>
    </body>
    </html>
    """

    # Height: ~48px per row + header/padding
    iframe_height = min(900, 120 + len(sub) * 48)
    components.html(full_html, height=iframe_height, scrolling=True)

    # Pagination controls
    cols = st.columns([1, 6, 1])
    with cols[1]:
        pag_cols = st.columns([1, 1, 6, 1, 1])
        with pag_cols[0]:
            if st.button("‹", key=f"{key}_prev", use_container_width=True, disabled=page <= 1):
                st.session_state[page_key] = max(1, page - 1)
                st.rerun()
        with pag_cols[2]:
            st.markdown(
                f"<div style='text-align:center; color:#d8dde8; padding-top:.45rem;'>Page <b style='color:#fff'>{page}</b> sur {pages}</div>",
                unsafe_allow_html=True,
            )
        with pag_cols[4]:
            if st.button("›", key=f"{key}_next", use_container_width=True, disabled=page >= pages):
                st.session_state[page_key] = min(pages, page + 1)
                st.rerun()

        size_options = [12, 25, 50, 100]
        new_size = st.selectbox(
            "Taille de page",
            size_options,
            index=size_options.index(size) if size in size_options else 0,
            key=f"{key}_size_select",
            label_visibility="collapsed",
        )
        if new_size != size:
            st.session_state[size_key] = new_size
            st.session_state[page_key] = 1
            st.rerun()


# ---------- Charts ----------

def sector_ytd_chart(df: pd.DataFrame) -> go.Figure:
    if df is None or df.empty:
        return go.Figure()
    g = df.groupby("Secteur")["YTD %"].mean().dropna().sort_values(ascending=False).head(12)
    colors = ["#22c55e" if v >= 0 else "#ef4444" for v in g.values]
    fig = go.Figure(
        go.Bar(
            x=g.index, y=g.values,
            marker_color=colors,
            text=[f"{v:+.2f}%" for v in g.values],
            textposition="outside",
            hovertemplate="<b>%{x}</b><br>YTD: %{y:.2f}%<extra></extra>",
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=60),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=11),
        xaxis=dict(tickangle=-20, gridcolor="#1a2135"),
        yaxis=dict(gridcolor="#1a2135", ticksuffix="%", zerolinecolor="#2a3350"),
    )
    return fig


def score_distribution_chart(df: pd.DataFrame) -> go.Figure:
    if df is None or df.empty:
        return go.Figure()
    bins = [0, 20, 40, 60, 80, 100]
    labels = ["0-20", "20-40", "40-60", "60-80", "80-100"]
    cats = pd.cut(df["Score"].dropna(), bins=bins, labels=labels, include_lowest=True)
    counts = cats.value_counts().reindex(labels).fillna(0)
    colors = ["#ef4444", "#f59e0b", "#eab308", "#84cc16", "#22c55e"]
    fig = go.Figure(
        go.Bar(
            x=counts.index, y=counts.values,
            marker_color=colors,
            text=[f"{int(v):,}" for v in counts.values],
            textposition="outside",
            hovertemplate="Score %{x}<br>%{y} actions<extra></extra>",
        )
    )
    fig.update_layout(
        height=320,
        margin=dict(l=10, r=10, t=10, b=40),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=11),
        xaxis=dict(title="Score", gridcolor="#1a2135"),
        yaxis=dict(gridcolor="#1a2135"),
    )
    return fig


def reco_donut_chart(df: pd.DataFrame) -> go.Figure:
    achat = int((df["Recommandation"] == "ACHAT").sum())
    surv = int((df["Recommandation"] == "SURVEILLANCE").sum())
    evt = int((df["Recommandation"] == "ÉVITER").sum())
    fig = go.Figure(
        go.Pie(
            labels=["ACHAT", "SURVEILLANCE", "ÉVITER"],
            values=[achat, surv, evt],
            hole=0.65,
            marker=dict(colors=["#22c55e", "#eab308", "#ef4444"], line=dict(color="#0f1420", width=3)),
            textinfo="none",
            hovertemplate="<b>%{label}</b><br>%{value} (%{percent})<extra></extra>",
        )
    )
    fig.update_layout(
        height=240,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
    )
    return fig


def stock_price_chart(hist: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    if hist is None or hist.empty:
        return fig
    close = hist["Close"].dropna()
    # MM50, MM200
    ma50 = close.rolling(50).mean()
    ma200 = close.rolling(200).mean()
    fig.add_trace(go.Scatter(
        x=close.index, y=close.values, mode="lines", name="Prix",
        line=dict(color="#7c5cff", width=2),
        fill="tozeroy", fillcolor="rgba(124,92,255,0.08)",
    ))
    fig.add_trace(go.Scatter(x=ma50.index, y=ma50.values, mode="lines", name="MM50",
                             line=dict(color="#22c55e", width=1.5, dash="dot")))
    fig.add_trace(go.Scatter(x=ma200.index, y=ma200.values, mode="lines", name="MM200",
                             line=dict(color="#f59e0b", width=1.5, dash="dot")))
    fig.update_layout(
        height=380,
        margin=dict(l=10, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=11),
        xaxis=dict(gridcolor="#1a2135"),
        yaxis=dict(gridcolor="#1a2135"),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#d8dde8")),
        hovermode="x unified",
    )
    return fig


def dividends_chart(dividends: pd.Series) -> go.Figure:
    fig = go.Figure()
    if dividends is None or len(dividends) == 0:
        return fig
    fig.add_trace(go.Bar(
        x=dividends.index, y=dividends.values,
        marker_color="#06b6d4",
        hovertemplate="%{x|%d %b %Y}<br>%{y:.3f}<extra></extra>",
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=10, r=10, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff", size=11),
        xaxis=dict(gridcolor="#1a2135"),
        yaxis=dict(gridcolor="#1a2135"),
    )
    return fig


# ---------- Detail view ----------

def render_stock_detail(row: pd.Series, history: pd.DataFrame, dividends: pd.Series, info: dict | None = None):
    from data.loader import fetch_dividends
    from analysis.narrative import analyse_court_terme, analyse_moyen_terme, analyse_long_terme

    info = info or {}

    def pick(key_row, *info_keys):
        """Prend la valeur du row, sinon tente info."""
        v = row.get(key_row)
        try:
            import numpy as _np
            if v is None or (isinstance(v, float) and _np.isnan(v)):
                v = None
        except Exception:
            pass
        if v in (None, "", "—"):
            for k in info_keys:
                iv = info.get(k)
                if iv not in (None, "", "—"):
                    return iv
        return v

    st.markdown(
        f"""
        <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:0.75rem;">
          <div>
            <div style="color:#d8dde8; font-size:.85rem;">{html.escape(str(row.get('Secteur','')))} • {html.escape(str(row.get('Pays','')))}</div>
            <div style="font-size:1.6rem; font-weight:700; color:#fff; margin-top:.15rem;">
              {html.escape(str(row['Ticker']))} <span style="color:#d8dde8; font-weight:500; font-size:1.1rem; margin-left:.5rem;">{html.escape(str(row['Entreprise']))}</span>
            </div>
          </div>
          <div>{_reco_html(row.get('Recommandation'))}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Price + YTD + score headline
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(_metric_card("Prix actuel", fmt_price(row.get("Prix"))), unsafe_allow_html=True)
    with c2:
        ytd = row.get("YTD %")
        color = "#22c55e" if (ytd or 0) >= 0 else "#ef4444"
        val = f'<span style="color:{color}">{fmt_pct(ytd)}</span>'
        st.markdown(_metric_card("YTD (depuis 01/01/2026)", val), unsafe_allow_html=True)
    with c3:
        st.markdown(_metric_card("Score global", f"{row.get('Score','—')}/100"), unsafe_allow_html=True)
    with c4:
        st.markdown(_metric_card("Capitalisation", row.get("Cap_Label", "—")), unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Chart + key data
    c_chart, c_side = st.columns([2, 1])
    with c_chart:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Historique de cours</div>', unsafe_allow_html=True)
        st.plotly_chart(stock_price_chart(history), use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    with c_side:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Technique</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:.6rem;">
              <div class="fv-metric"><div class="fv-metric-label">MM 50</div><div class="fv-metric-value">{fmt_price(row.get('MA50'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">MM 200</div><div class="fv-metric-value">{fmt_price(row.get('MA200'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">RSI (14)</div><div class="fv-metric-value">{fmt_number(row.get('RSI'), 1)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Tendance</div><div class="fv-metric-value" style="font-size:.95rem;">{row.get('Tendance','—')}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Support</div><div class="fv-metric-value">{fmt_price(row.get('Support'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Résistance</div><div class="fv-metric-value">{fmt_price(row.get('Résistance'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Stop-Loss</div><div class="fv-metric-value" style="color:#f87171">{fmt_price(row.get('Stop_Loss'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">52W High</div><div class="fv-metric-value">{fmt_price(row.get('52W_High'))}</div></div>
            </div>
            <div style="margin-top:.8rem; padding:.7rem; background:#1c2337; border-radius:8px; color:#ffffff; font-size:.85rem;">
              <b style="color:#9b7bff;">Signal d'entrée:</b> {row.get('Entry_Trigger') or 'Aucun signal actionnable'}
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Description de l'entreprise — privilégier le français
    try:
        from data.descriptions_fr import get_description_fr
        description_fr = get_description_fr(row.get("Ticker", ""))
    except Exception:
        description_fr = None
    description = description_fr or (info or {}).get("longBusinessSummary") or (info or {}).get("description")
    if description:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">À propos de l\'entreprise</div>', unsafe_allow_html=True)
        website = (info or {}).get("website") or ""
        employees = (info or {}).get("fullTimeEmployees")
        hq = ", ".join(filter(None, [(info or {}).get("city"), (info or {}).get("country")]))
        meta_bits = []
        if hq:
            meta_bits.append(f"📍 {html.escape(str(hq))}")
        if employees:
            try:
                meta_bits.append(f"👥 {int(employees):,} employés")
            except Exception:
                pass
        if website:
            meta_bits.append(f'🔗 <a href="{html.escape(website)}" target="_blank" style="color:#9b7bff;text-decoration:none;">Site web</a>')
        if (info or {}).get("industry"):
            meta_bits.append(f"🏭 {html.escape(str((info or {}).get('industry')))}")

        st.markdown(
            f"""
            <div style="color:#d8dde8; font-size:.85rem; margin-bottom:.7rem;">{' &nbsp;•&nbsp; '.join(meta_bits)}</div>
            <div style="color:#ffffff; line-height:1.65; font-size:.92rem;">{html.escape(description)}</div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("<br/>", unsafe_allow_html=True)

    # Fundamental + Dividends
    # Helper pour fusionner row + info
    def _val(key_row, *info_keys):
        v = row.get(key_row)
        try:
            import numpy as _np
            if v is None or (isinstance(v, float) and _np.isnan(v)):
                v = None
        except Exception:
            pass
        if v in (None, "", "—"):
            for k in info_keys:
                iv = (info or {}).get(k)
                if iv not in (None, "", "—"):
                    return iv
        return v

    cf1, cf2 = st.columns(2)
    with cf1:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Fondamentaux</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:grid; grid-template-columns:1fr 1fr; gap:.5rem;">
              <div class="fv-metric"><div class="fv-metric-label">PER (TTM)</div><div class="fv-metric-value">{fmt_number(_val('PE','trailingPE'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">PER (Forward)</div><div class="fv-metric-value">{fmt_number(_val('Forward_PE','forwardPE'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">PEG</div><div class="fv-metric-value">{fmt_number(_val('PEG','pegRatio'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">P/B</div><div class="fv-metric-value">{fmt_number(_val('P/B','priceToBook'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">EV / EBITDA</div><div class="fv-metric-value">{fmt_number(_val('EV/EBITDA','enterpriseToEbitda'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">P/S</div><div class="fv-metric-value">{fmt_number(_val('priceToSales','priceToSalesTrailing12Months'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Marge nette</div><div class="fv-metric-value">{fmt_ratio_pct(_val('Marge_Profit','profitMargins'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Marge opé.</div><div class="fv-metric-value">{fmt_ratio_pct(_val('Marge_Op','operatingMargins'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Marge brute</div><div class="fv-metric-value">{fmt_ratio_pct(_val('Marge_Brute','grossMargins'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">ROE</div><div class="fv-metric-value">{fmt_ratio_pct(_val('ROE','returnOnEquity'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">ROA</div><div class="fv-metric-value">{fmt_ratio_pct(_val('ROA','returnOnAssets'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Debt / Equity</div><div class="fv-metric-value">{fmt_number(_val('Debt_Equity','debtToEquity'), 1)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Current Ratio</div><div class="fv-metric-value">{fmt_number(_val('Current_Ratio','currentRatio'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Beta</div><div class="fv-metric-value">{fmt_number(_val('Beta','beta'), 2)}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Croissance revenus</div><div class="fv-metric-value">{fmt_ratio_pct(_val('Revenue_Growth','revenueGrowth'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Croissance EPS</div><div class="fv-metric-value">{fmt_ratio_pct(_val('Earnings_Growth','earningsGrowth'))}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with cf2:
        has_div = row.get("Dividende_A") and dividends is not None and len(dividends) > 0
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Dividendes (3 ans)</div>', unsafe_allow_html=True)
        if has_div:
            yld = row.get("Dividende_Yield")
            freq = row.get("Dividende_Fréquence") or "—"
            st.markdown(
                f"""
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:.5rem; margin-bottom:.5rem;">
                  <div class="fv-metric"><div class="fv-metric-label">Rendement</div><div class="fv-metric-value" style="color:#06b6d4">{_div_html(yld) if yld else 'Donnée non disponible'}</div></div>
                  <div class="fv-metric"><div class="fv-metric-label">Fréquence</div><div class="fv-metric-value">{freq}</div></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            three_y_ago = pd.Timestamp.now(tz=dividends.index.tz) - pd.DateOffset(years=3) if dividends.index.tz is not None else pd.Timestamp.now() - pd.DateOffset(years=3)
            try:
                recent = dividends[dividends.index >= three_y_ago]
            except Exception:
                recent = dividends.tail(12)
            st.plotly_chart(dividends_chart(recent), use_container_width=True, config={"displayModeBar": False})
        else:
            st.markdown(
                '<div style="color:#d8dde8; padding:1rem 0;">Donnée non disponible — cette action ne verse pas de dividende ou l\'historique n\'est pas accessible.</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br/>", unsafe_allow_html=True)

    # Outlook + Risk
    co1, co2, co3 = st.columns(3)
    with co1:
        oc = row.get("Outlook_Court", "—")
        om = row.get("Outlook_Moyen", "—")
        ol = row.get("Outlook_Long", "—")
        badge_colors = {"Positive": "#4ade80", "Négative": "#f87171", "Mitigée": "#fbbf24", "Neutre": "#d8dde8"}
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Perspectives — synthèse</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:flex; flex-direction:column; gap:.5rem;">
              <div class="fv-metric"><div class="fv-metric-label">Court terme (1-3 mois)</div>
                <div class="fv-metric-value" style="color:{badge_colors.get(oc,'#fff')}">{oc}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Moyen terme (6-18 mois)</div>
                <div class="fv-metric-value" style="color:{badge_colors.get(om,'#fff')}">{om}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Long terme (3-10 ans)</div>
                <div class="fv-metric-value" style="color:{badge_colors.get(ol,'#fff')}">{ol}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with co2:
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Profil & Risque</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:flex; flex-direction:column; gap:.5rem;">
              <div class="fv-metric"><div class="fv-metric-label">Profil</div><div class="fv-metric-value">{row.get('Profil','—')}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Niveau de risque</div><div class="fv-metric-value">{row.get('Risque','—')}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Conviction</div><div class="fv-metric-value">{row.get('Conviction','—')}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with co3:
        buy_zone = row.get("Buy_Zone")
        bz_txt = "—"
        if buy_zone and isinstance(buy_zone, (tuple, list)) and len(buy_zone) == 2:
            bz_txt = f"${buy_zone[0]:,.2f} – ${buy_zone[1]:,.2f}"
        st.markdown('<div class="fv-panel"><div class="fv-panel-title">Plan de trade</div>', unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="display:flex; flex-direction:column; gap:.5rem;">
              <div class="fv-metric"><div class="fv-metric-label">Zone d'achat</div><div class="fv-metric-value" style="color:#4ade80">{bz_txt}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Stop-loss</div><div class="fv-metric-value" style="color:#f87171">{fmt_price(row.get('Stop_Loss'))}</div></div>
              <div class="fv-metric"><div class="fv-metric-label">Objectif (résistance)</div><div class="fv-metric-value">{fmt_price(row.get('Résistance'))}</div></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ---- Analyses narratives détaillées ----
    st.markdown("<br/>", unsafe_allow_html=True)
    st.markdown('<div class="fv-panel"><div class="fv-panel-title">Analyse détaillée</div>', unsafe_allow_html=True)

    tabs = st.tabs(["📊 Court terme (1-3 mois)", "🏢 Moyen terme (6-18 mois)", "🌐 Long terme (3-10 ans)"])

    with tabs[0]:
        txt = analyse_court_terme(row)
        st.markdown(
            f'<div style="color:#ffffff; line-height:1.75; font-size:.95rem; padding:.3rem 0;">{txt}</div>',
            unsafe_allow_html=True,
        )
    with tabs[1]:
        txt = analyse_moyen_terme(row, info)
        st.markdown(
            f'<div style="color:#ffffff; line-height:1.75; font-size:.95rem; padding:.3rem 0;">{txt}</div>',
            unsafe_allow_html=True,
        )
    with tabs[2]:
        txt = analyse_long_terme(row, info)
        st.markdown(
            f'<div style="color:#ffffff; line-height:1.75; font-size:.95rem; padding:.3rem 0;">{txt}</div>',
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def _metric_card(label: str, value: str) -> str:
    return f"""
    <div class="fv-metric">
      <div class="fv-metric-label">{label}</div>
      <div class="fv-metric-value">{value}</div>
    </div>
    """


# ---------- Rankings ----------

def render_ranking_list(df: pd.DataFrame, title: str, limit: int = 10):
    if df is None or df.empty:
        st.markdown(f'<div class="fv-empty">Pas de données pour "{title}"</div>', unsafe_allow_html=True)
        return
    st.markdown(f'<div class="fv-panel"><div class="fv-panel-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    sub = df.head(limit)
    rows = []
    for _, r in sub.iterrows():
        ytd = r.get("YTD %")
        col = "#22c55e" if (ytd or 0) >= 0 else "#ef4444"
        rows.append(
            f"""
            <div style="display:flex; justify-content:space-between; align-items:center; padding:.55rem 0; border-bottom:1px solid #1a2135;">
              <div>
                <div style="color:#fff; font-weight:600; font-size:.9rem;">{html.escape(str(r['Ticker']))}</div>
                <div style="color:#d8dde8; font-size:.78rem;">{html.escape(str(r['Entreprise'])[:28])}</div>
              </div>
              <div style="display:flex; gap:1rem; align-items:center;">
                <span style="color:#ffffff; font-size:.82rem;">{int(round(r.get('Score',0)))}/100</span>
                <span style="color:{col}; font-weight:600; font-size:.85rem;">{fmt_pct(ytd)}</span>
              </div>
            </div>
            """
        )
    st.markdown("".join(rows), unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ---------- News placeholder ----------

def render_news_panel(df: pd.DataFrame):
    """Panneau actualités — génère des catalyseurs synthétiques depuis la data."""
    st.markdown('<div class="fv-panel"><div class="fv-panel-title">Actualités & Catalyseurs</div>', unsafe_allow_html=True)
    if df is None or df.empty:
        st.markdown('<div class="fv-empty">Aucune actualité disponible.</div></div>', unsafe_allow_html=True)
        return
    top = df.nlargest(3, "YTD %") if "YTD %" in df.columns else df.head(3)
    items = []
    for _, r in top.iterrows():
        items.append(
            f"""
            <div class="fv-news-item">
              <div class="fv-news-icon">📈</div>
              <div style="flex:1;">
                <div class="fv-news-title">{html.escape(str(r['Entreprise']))} affiche {fmt_pct(r.get('YTD %'))} YTD</div>
                <div class="fv-news-meta">{html.escape(str(r['Ticker']))} • {html.escape(str(r.get('Secteur','')))}</div>
                <div class="fv-news-body">Score global: {int(round(r.get('Score',0)))}/100 — Recommandation: {r.get('Recommandation','—')}</div>
              </div>
            </div>
            """
        )
    st.markdown("".join(items) + "</div>", unsafe_allow_html=True)
