"""
Chargement de données via yfinance, mutualisé avec le cache Streamlit.
Téléchargement en batch, enrichissement info/dividends par ticker à la demande.
"""

from __future__ import annotations

from datetime import datetime
import concurrent.futures as cf
import math

import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

from data.universe import (
    get_universe,
    country_from_ticker,
    INDICES,
)
from data.metadata import get_static_meta
from analysis.technical import compute_technical, week_52
from analysis.fundamental import extract_fundamentals
from analysis.scoring import (
    compute_score,
    risk_level,
    conviction_level,
    profile,
    recommendation,
    outlook,
)

# Début d'année pour YTD
YTD_START = "2026-01-01"
HISTORY_START = "2024-06-01"  # ~22 mois d'historique pour MM200


def _chunks(lst: list, size: int):
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


@st.cache_data(ttl=3600, show_spinner=False)
def load_prices(tickers: tuple[str, ...], start: str = HISTORY_START) -> pd.DataFrame:
    """Télécharge les historiques de prix en batch. Retourne un DF à colonnes MultiIndex."""
    dfs = []
    for chunk in _chunks(list(tickers), 80):
        try:
            data = yf.download(
                tickers=chunk,
                start=start,
                interval="1d",
                group_by="ticker",
                auto_adjust=True,
                progress=False,
                threads=True,
            )
            if data is not None and not data.empty:
                dfs.append(data)
        except Exception:
            continue
    if not dfs:
        return pd.DataFrame()
    return pd.concat(dfs, axis=1)


def _closes_for(data: pd.DataFrame, ticker: str) -> pd.Series | None:
    try:
        if isinstance(data.columns, pd.MultiIndex):
            if ticker in data.columns.get_level_values(0):
                sub = data[ticker]
                if "Close" in sub.columns:
                    return sub["Close"].dropna()
        else:
            if "Close" in data.columns:
                return data["Close"].dropna()
    except Exception:
        return None
    return None


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_ticker_info(ticker: str, full: bool = False) -> dict:
    """Récupère fast_info (rapide) et optionnellement info (lent, fragile)."""
    info = {}
    try:
        t = yf.Ticker(ticker)
        try:
            fi = t.fast_info
            if fi:
                for k_src, k_dst in [
                    ("market_cap", "marketCap"),
                    ("currency", "currency"),
                    ("last_price", "currentPrice"),
                    ("year_high", "fiftyTwoWeekHigh"),
                    ("year_low", "fiftyTwoWeekLow"),
                ]:
                    try:
                        info[k_dst] = getattr(fi, k_src, None)
                    except Exception:
                        pass
        except Exception:
            pass
        if full:
            try:
                i = t.info or {}
                info.update(i)
            except Exception:
                pass
    except Exception:
        pass
    return info


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_dividends(ticker: str) -> pd.Series:
    """Historique complet des dividendes."""
    try:
        t = yf.Ticker(ticker)
        div = t.dividends
        if div is None or len(div) == 0:
            return pd.Series(dtype=float)
        return div
    except Exception:
        return pd.Series(dtype=float)


def _dividend_summary(ticker: str, current_price: float | None) -> dict:
    div = fetch_dividends(ticker)
    if div is None or len(div) == 0:
        return {
            "dividend_yield": None,
            "dividend_frequency": None,
            "last_3y": pd.Series(dtype=float),
            "has_dividend": False,
        }
    now = pd.Timestamp.now(tz=div.index.tz) if div.index.tz is not None else pd.Timestamp.now()
    three_y_ago = now - pd.DateOffset(years=3)
    try:
        recent = div[div.index >= three_y_ago]
    except Exception:
        recent = div.tail(36)

    one_y_ago = now - pd.DateOffset(years=1)
    try:
        last_12 = div[div.index >= one_y_ago]
    except Exception:
        last_12 = div.tail(12)

    # Fréquence
    freq = None
    n = len(last_12)
    if n >= 10:
        freq = "Mensuelle"
    elif n >= 3:
        freq = "Trimestrielle"
    elif n == 2:
        freq = "Semestrielle"
    elif n == 1:
        freq = "Annuelle"

    annual = float(last_12.sum()) if n > 0 else 0.0
    yld = None
    if current_price and current_price > 0 and annual > 0:
        yld = annual / current_price

    return {
        "dividend_yield": yld,
        "dividend_frequency": freq,
        "last_3y": recent,
        "has_dividend": n > 0,
    }


def _compute_ytd(close: pd.Series) -> float | None:
    if close is None or len(close) == 0:
        return None
    ytd_start = pd.Timestamp(YTD_START)
    try:
        idx = close.index
        if getattr(idx, "tz", None) is not None:
            ytd_start = ytd_start.tz_localize(idx.tz)
        past = close[close.index >= ytd_start]
        if len(past) < 2:
            return None
        start_price = float(past.iloc[0])
        last_price = float(past.iloc[-1])
        if start_price <= 0:
            return None
        return ((last_price - start_price) / start_price) * 100
    except Exception:
        return None


def _market_cap_label(mc: float | None) -> str:
    if mc is None:
        return "—"
    try:
        mc = float(mc)
    except Exception:
        return "—"
    if mc >= 1e12:
        return f"${mc/1e12:.2f}T"
    if mc >= 1e9:
        return f"${mc/1e9:.2f}B"
    if mc >= 1e6:
        return f"${mc/1e6:.2f}M"
    return f"${mc:.0f}"


def _mc_category(mc: float | None) -> str:
    if mc is None: return "Autre"
    if mc >= 200e9: return "Mega Cap"
    if mc >= 10e9: return "Large Cap"
    if mc >= 2e9: return "Mid Cap"
    if mc >= 300e6: return "Small Cap"
    return "Micro Cap"


@st.cache_data(ttl=1800, show_spinner="Chargement de l'univers boursier...")
def load_universe_data(max_tickers: int | None = None) -> pd.DataFrame:
    """Charge et enrichit l'univers complet. Retourne un DataFrame prêt pour l'UI."""
    universe = get_universe()
    if max_tickers:
        universe = universe[:max_tickers]

    # 1. Prix en batch
    prices = load_prices(tuple(universe))

    # 2. Enrichissement par ticker (parallélisé)
    rows = []

    def build_row(ticker: str) -> dict | None:
        try:
            close = _closes_for(prices, ticker)
            if close is None or len(close) < 20:
                return None
            ytd = _compute_ytd(close)
            tech = compute_technical(close)
            w52 = week_52(close)

            try:
                info = fetch_ticker_info(ticker, full=False)
            except Exception:
                info = {}
            # Merge static metadata (name/sector/country) — plus fiable et rapide
            meta = get_static_meta(ticker)
            if meta:
                info.setdefault("shortName", meta.get("name"))
                info.setdefault("sector", meta.get("sector"))
                info.setdefault("industry", meta.get("industry"))
                info.setdefault("country", meta.get("country"))
            fund = extract_fundamentals(info, None)

            price = tech.get("price")
            try:
                div = _dividend_summary(ticker, price)
            except Exception:
                div = {"dividend_yield": None, "dividend_frequency": None, "last_3y": pd.Series(dtype=float), "has_dividend": False}
        except Exception:
            return None

        try:
            score = compute_score(tech, fund, ytd, w52.get("dist_from_high"))
            risk = risk_level(fund, tech, ytd)
            conv = conviction_level(score)
            prof = profile(fund, tech, ytd, w52.get("dist_from_high"))
            reco = recommendation(score, prof, risk)
            out = outlook(tech.get("trend"), score, prof)
        except Exception:
            score, risk, conv, prof, reco = 50.0, "Moyen", "Faible", "Mixte", "SURVEILLANCE"
            out = {"court": "Neutre", "moyen": "Neutre", "long": "Neutre"}

        name = info.get("shortName") or info.get("longName") or ticker
        sector = info.get("sector") or "—"
        industry = info.get("industry") or "—"
        country = info.get("country") or country_from_ticker(ticker)

        return {
            "Ticker": ticker,
            "Entreprise": name,
            "Secteur": sector,
            "Industrie": industry,
            "Pays": country,
            "Devise": info.get("currency") or "USD",
            "Capitalisation": fund.get("market_cap"),
            "Cap_Label": _market_cap_label(fund.get("market_cap")),
            "Cap_Catégorie": _mc_category(fund.get("market_cap")),
            "Prix": price,
            "YTD %": ytd,
            "52W_High": w52.get("high_52w"),
            "52W_Low": w52.get("low_52w"),
            "Dist_52W_High": w52.get("dist_from_high"),
            "MA50": tech.get("ma50"),
            "MA200": tech.get("ma200"),
            "RSI": tech.get("rsi"),
            "Support": tech.get("support"),
            "Résistance": tech.get("resistance"),
            "Tendance": tech.get("trend"),
            "Buy_Zone": tech.get("buy_zone"),
            "Stop_Loss": tech.get("stop_loss"),
            "Entry_Trigger": tech.get("entry_trigger"),
            "Dividende_Yield": div.get("dividend_yield"),
            "Dividende_Fréquence": div.get("dividend_frequency"),
            "Dividende_A": div.get("has_dividend"),
            "PE": fund.get("trailing_pe"),
            "Forward_PE": fund.get("forward_pe"),
            "PEG": fund.get("peg"),
            "P/B": fund.get("price_to_book"),
            "EV/EBITDA": fund.get("ev_ebitda"),
            "Marge_Profit": fund.get("profit_margin"),
            "Marge_Op": fund.get("operating_margin"),
            "Marge_Brute": fund.get("gross_margin"),
            "Debt_Equity": fund.get("debt_to_equity"),
            "Current_Ratio": fund.get("current_ratio"),
            "Revenue_Growth": fund.get("revenue_growth"),
            "Earnings_Growth": fund.get("earnings_growth"),
            "ROE": fund.get("roe"),
            "ROA": fund.get("roa"),
            "Beta": fund.get("beta"),
            "FCF": fund.get("fcf"),
            "Score": score,
            "Risque": risk,
            "Conviction": conv,
            "Profil": prof,
            "Recommandation": reco,
            "Outlook_Court": out["court"],
            "Outlook_Moyen": out["moyen"],
            "Outlook_Long": out["long"],
        }

    # Parallélisation des enrichissements (info = calls réseaux)
    with cf.ThreadPoolExecutor(max_workers=16) as ex:
        results = list(ex.map(build_row, universe))

    rows = [r for r in results if r is not None]
    df = pd.DataFrame(rows)
    return df


@st.cache_data(ttl=900, show_spinner=False)
def load_indices() -> dict:
    """Données d'indices pour l'en-tête."""
    out = {}
    tickers = list(INDICES.values())
    try:
        data = yf.download(
            tickers=tickers,
            period="5d",
            interval="1h",
            group_by="ticker",
            auto_adjust=True,
            progress=False,
            threads=True,
        )
    except Exception:
        data = None

    for name, sym in INDICES.items():
        try:
            if data is None or data.empty:
                raise ValueError("no data")
            if isinstance(data.columns, pd.MultiIndex):
                sub = data[sym]
                close = sub["Close"].dropna()
            else:
                close = data["Close"].dropna()
            if len(close) < 2:
                continue
            last = float(close.iloc[-1])
            prev = float(close.iloc[0])
            change = ((last - prev) / prev) * 100 if prev else 0
            out[name] = {
                "symbol": sym,
                "price": last,
                "change_pct": change,
                "history": close.tolist(),
            }
        except Exception:
            out[name] = {
                "symbol": sym,
                "price": None,
                "change_pct": None,
                "history": [],
            }
    return out


@st.cache_data(ttl=3600, show_spinner=False)
def load_stock_history(ticker: str, period: str = "2y") -> pd.DataFrame:
    """Historique complet pour un ticker (vue détail)."""
    try:
        t = yf.Ticker(ticker)
        hist = t.history(period=period, auto_adjust=True)
        return hist
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def load_full_info(ticker: str) -> dict:
    """Charge info + fast_info complet pour un ticker (vue détail uniquement)."""
    out = {}
    try:
        t = yf.Ticker(ticker)
        try:
            fi = t.fast_info
            if fi:
                for k_src, k_dst in [
                    ("market_cap", "marketCap"),
                    ("currency", "currency"),
                    ("last_price", "currentPrice"),
                    ("year_high", "fiftyTwoWeekHigh"),
                    ("year_low", "fiftyTwoWeekLow"),
                ]:
                    try:
                        out[k_dst] = getattr(fi, k_src, None)
                    except Exception:
                        pass
        except Exception:
            pass
        try:
            i = t.info or {}
            out.update(i)
        except Exception:
            pass
    except Exception:
        pass
    return out


def last_update_label() -> str:
    return datetime.now().strftime("%d %b. %Y %H:%M")
