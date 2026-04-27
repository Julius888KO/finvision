"""Analyse fondamentale: croissance revenus, EPS, marges, dette, FCF, valorisation."""

from __future__ import annotations

import pandas as pd


def safe(info: dict, key: str, default=None):
    v = info.get(key, default) if info else default
    if v is None:
        return default
    try:
        if pd.isna(v):
            return default
    except (TypeError, ValueError):
        pass
    # Coerce string numbers to float when possible
    if isinstance(v, str):
        try:
            return float(v.replace(",", "").strip())
        except (ValueError, AttributeError):
            return default
    return v


def extract_fundamentals(info: dict, financials: pd.DataFrame | None) -> dict:
    """Construit le dict fondamentaux à partir de yfinance.info + financials."""
    if info is None:
        info = {}

    market_cap = safe(info, "marketCap")
    trailing_pe = safe(info, "trailingPE")
    forward_pe = safe(info, "forwardPE")
    peg = safe(info, "pegRatio")
    price_to_book = safe(info, "priceToBook")
    ev_ebitda = safe(info, "enterpriseToEbitda")
    profit_margin = safe(info, "profitMargins")
    operating_margin = safe(info, "operatingMargins")
    gross_margin = safe(info, "grossMargins")
    debt_to_equity = safe(info, "debtToEquity")
    current_ratio = safe(info, "currentRatio")
    revenue_growth = safe(info, "revenueGrowth")
    earnings_growth = safe(info, "earningsGrowth")
    fcf = safe(info, "freeCashflow")
    roe = safe(info, "returnOnEquity")
    roa = safe(info, "returnOnAssets")
    beta = safe(info, "beta")

    # Croissance revenus sur 3 ans si financials disponibles
    rev_3y = None
    eps_trend = None
    if financials is not None and not financials.empty:
        try:
            if "Total Revenue" in financials.index:
                revs = financials.loc["Total Revenue"].dropna()
                if len(revs) >= 2:
                    oldest = revs.iloc[-1]
                    newest = revs.iloc[0]
                    if oldest and oldest > 0:
                        # CAGR approximatif
                        years = len(revs) - 1
                        rev_3y = ((newest / oldest) ** (1 / years) - 1) if years else None
        except Exception:
            pass

    return {
        "market_cap": market_cap,
        "trailing_pe": trailing_pe,
        "forward_pe": forward_pe,
        "peg": peg,
        "price_to_book": price_to_book,
        "ev_ebitda": ev_ebitda,
        "profit_margin": profit_margin,
        "operating_margin": operating_margin,
        "gross_margin": gross_margin,
        "debt_to_equity": debt_to_equity,
        "current_ratio": current_ratio,
        "revenue_growth": revenue_growth,
        "revenue_growth_3y": rev_3y,
        "earnings_growth": earnings_growth,
        "eps_trend": eps_trend,
        "fcf": fcf,
        "roe": roe,
        "roa": roa,
        "beta": beta,
    }
