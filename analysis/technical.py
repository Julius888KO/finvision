"""Indicateurs techniques: MM50, MM200, RSI, supports/résistances, tendance."""

from __future__ import annotations

import numpy as np
import pandas as pd


def sma(series: pd.Series, window: int) -> float | None:
    if series is None or len(series) < window:
        return None
    return float(series.tail(window).mean())


def rsi(series: pd.Series, period: int = 14) -> float | None:
    if series is None or len(series) < period + 1:
        return None
    delta = series.diff().dropna()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi_val = 100 - (100 / (1 + rs))
    last = rsi_val.iloc[-1]
    if pd.isna(last):
        return None
    return float(last)


def support_resistance(series: pd.Series, window: int = 60) -> tuple[float | None, float | None]:
    """Support = plus bas récent, résistance = plus haut récent."""
    if series is None or len(series) < 10:
        return None, None
    tail = series.tail(window)
    return float(tail.min()), float(tail.max())


def trend(price: float | None, ma50: float | None, ma200: float | None) -> str:
    if price is None or ma50 is None or ma200 is None:
        return "Indéterminée"
    if price > ma50 > ma200:
        return "Haussière"
    if price < ma50 < ma200:
        return "Baissière"
    if ma50 > ma200:
        return "Haussière faible"
    return "Baissière faible"


def compute_technical(close: pd.Series) -> dict:
    """Calcule tous les indicateurs techniques pour une série de clôtures."""
    price = float(close.iloc[-1]) if close is not None and len(close) else None
    ma50 = sma(close, 50)
    ma200 = sma(close, 200)
    rsi_val = rsi(close, 14)
    support, resistance = support_resistance(close, 60)
    trend_val = trend(price, ma50, ma200)

    # Buy zone = entre support et support + 3% de la fourchette
    buy_zone = None
    if support is not None and resistance is not None:
        rng = resistance - support
        buy_zone = (support, support + 0.15 * rng)

    # Stop-loss = support - 5%
    stop_loss = support * 0.95 if support else None

    # Entry trigger: croisement MM50 > MM200 ou RSI sort de zone survendue
    entry = None
    if ma50 and ma200 and price:
        if price > ma50 and ma50 > ma200 and rsi_val and 40 < rsi_val < 65:
            entry = "Momentum haussier confirmé"
        elif rsi_val and rsi_val < 35:
            entry = "Zone de survente — rebond possible"
        elif price < ma200:
            entry = "Attendre retour au-dessus MM200"

    return {
        "price": price,
        "ma50": ma50,
        "ma200": ma200,
        "rsi": rsi_val,
        "support": support,
        "resistance": resistance,
        "trend": trend_val,
        "buy_zone": buy_zone,
        "stop_loss": stop_loss,
        "entry_trigger": entry,
    }


def week_52(close: pd.Series) -> dict:
    if close is None or len(close) == 0:
        return {"high_52w": None, "low_52w": None, "dist_from_high": None}
    tail = close.tail(252)  # ~1 an de trading
    high = float(tail.max())
    low = float(tail.min())
    price = float(tail.iloc[-1])
    dist = ((price - high) / high) * 100 if high else None
    return {"high_52w": high, "low_52w": low, "dist_from_high": dist}
