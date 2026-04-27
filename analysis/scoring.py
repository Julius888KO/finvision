"""Scoring /100, profil, risque, conviction, recommandation."""

from __future__ import annotations


def _clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))


def _num(v):
    """Coerce une valeur en float, retourne None si impossible."""
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    if f != f:  # NaN
        return None
    return f


def compute_score(tech: dict, fund: dict, ytd: float | None, dist_52w_high: float | None) -> float:
    """
    Score composite normalisé /100.
    Chaque catégorie contribue selon la disponibilité de ses données.
    On normalise ensuite sur la somme des poids disponibles.
    """
    # Préparation
    trend = tech.get("trend") if tech else None
    rsi = _num(tech.get("rsi")) if tech else None
    ytd = _num(ytd)
    dist_52w_high = _num(dist_52w_high)

    pe = _num(fund.get("trailing_pe")) if fund else None
    peg = _num(fund.get("peg")) if fund else None
    pb = _num(fund.get("price_to_book")) if fund else None
    pm = _num(fund.get("profit_margin")) if fund else None
    om = _num(fund.get("operating_margin")) if fund else None
    roe = _num(fund.get("roe")) if fund else None
    de = _num(fund.get("debt_to_equity")) if fund else None
    cr = _num(fund.get("current_ratio")) if fund else None
    fcf = _num(fund.get("fcf")) if fund else None

    earned = 0.0  # points gagnés
    available = 0.0  # points disponibles (poids des catégories avec données)

    # ========== 1. TENDANCE / MOMENTUM (25 pts) ==========
    tech_max = 0.0
    tech_pts = 0.0
    if trend is not None:
        tech_max += 15
        if trend == "Haussière":
            tech_pts += 15
        elif trend == "Haussière faible":
            tech_pts += 10
        elif trend == "Baissière faible":
            tech_pts += 5
        # baissière = 0
    if rsi is not None:
        tech_max += 10
        if 45 <= rsi <= 65:
            tech_pts += 10
        elif 30 <= rsi < 45:
            tech_pts += 7
        elif rsi < 30:
            tech_pts += 6  # survendu = opportunité
        elif 65 < rsi <= 75:
            tech_pts += 4
        else:  # >75 surachat
            tech_pts += 1
    earned += tech_pts
    available += tech_max

    # ========== 2. PERFORMANCE YTD + 52W (20 pts) ==========
    perf_max = 0.0
    perf_pts = 0.0
    if ytd is not None:
        perf_max += 12
        if ytd > 20: perf_pts += 12
        elif ytd > 10: perf_pts += 10
        elif ytd > 5: perf_pts += 8
        elif ytd > 0: perf_pts += 6
        elif ytd > -10: perf_pts += 4
        elif ytd > -20: perf_pts += 2
        # <-20% = 0
    if dist_52w_high is not None:
        perf_max += 8
        if dist_52w_high > -5: perf_pts += 8
        elif dist_52w_high > -15: perf_pts += 6
        elif dist_52w_high > -30: perf_pts += 3
    earned += perf_pts
    available += perf_max

    # ========== 3. VALORISATION (20 pts) ==========
    val_max = 0.0
    val_pts = 0.0
    if pe is not None:
        val_max += 8
        if 0 < pe < 15: val_pts += 8
        elif 0 < pe < 25: val_pts += 6
        elif 0 < pe < 40: val_pts += 3
    if peg is not None:
        val_max += 7
        if 0 < peg < 1: val_pts += 7
        elif 0 < peg < 2: val_pts += 4
    if pb is not None:
        val_max += 5
        if 0 < pb < 3: val_pts += 5
        elif 0 < pb < 6: val_pts += 3
    earned += val_pts
    available += val_max

    # ========== 4. QUALITÉ (20 pts) ==========
    q_max = 0.0
    q_pts = 0.0
    if pm is not None:
        q_max += 7
        if pm > 0.20: q_pts += 7
        elif pm > 0.10: q_pts += 5
        elif pm > 0: q_pts += 2
    if om is not None:
        q_max += 6
        if om > 0.25: q_pts += 6
        elif om > 0.15: q_pts += 4
        elif om > 0: q_pts += 2
    if roe is not None:
        q_max += 7
        if roe > 0.20: q_pts += 7
        elif roe > 0.10: q_pts += 5
        elif roe > 0: q_pts += 2
    earned += q_pts
    available += q_max

    # ========== 5. SANTÉ FINANCIÈRE (15 pts) ==========
    h_max = 0.0
    h_pts = 0.0
    if de is not None:
        h_max += 6
        if de < 50: h_pts += 6
        elif de < 100: h_pts += 4
        elif de < 200: h_pts += 2
    if cr is not None:
        h_max += 4
        if cr > 1.5: h_pts += 4
        elif cr > 1: h_pts += 2
    if fcf is not None:
        h_max += 5
        if fcf > 0: h_pts += 5
    earned += h_pts
    available += h_max

    # Normalisation : ramène sur 100 selon ce qui était disponible
    if available <= 0:
        return 50.0
    normalized = (earned / available) * 100
    return round(_clamp(normalized), 1)


def risk_level(fund: dict, tech: dict, ytd: float | None) -> str:
    beta = _num(fund.get("beta")) if fund else None
    de = _num(fund.get("debt_to_equity")) if fund else None
    rsi = _num(tech.get("rsi")) if tech else None
    ytd = _num(ytd)

    risk_points = 0
    if beta is not None:
        if beta > 1.5: risk_points += 2
        elif beta > 1.2: risk_points += 1
    if de is not None and de > 150: risk_points += 2
    if rsi is not None and (rsi > 75 or rsi < 25): risk_points += 1
    if ytd is not None and ytd < -25: risk_points += 2

    if risk_points >= 4: return "Élevé"
    if risk_points >= 2: return "Moyen"
    return "Faible"


def conviction_level(score: float) -> str:
    if score >= 75: return "Élevée"
    if score >= 55: return "Moyenne"
    return "Faible"


def profile(fund: dict, tech: dict, ytd: float | None, dist_52w: float | None) -> str:
    pe = _num(fund.get("trailing_pe")) if fund else None
    pm = _num(fund.get("profit_margin")) if fund else None
    rev_g = _num(fund.get("revenue_growth")) if fund else None
    roe = _num(fund.get("roe")) if fund else None
    trend = tech.get("trend") if tech else None
    rsi = _num(tech.get("rsi")) if tech else None
    ytd = _num(ytd)
    dist_52w = _num(dist_52w)

    # Qualité: fondamentaux excellents
    if pm is not None and pm > 0.15 and roe is not None and roe > 0.18:
        return "Qualité"

    # Valeur: PE bas, rentable
    if pe is not None and 0 < pe < 15 and pm is not None and pm > 0.05:
        if ytd is not None and ytd < 0:
            return "Qualité décotée"
        return "Valeur"

    # Croissance: tendance haussière forte
    if trend == "Haussière" and ytd is not None and ytd > 15:
        return "Croissance"
    if rev_g is not None and rev_g > 0.15 and trend in ("Haussière", "Haussière faible"):
        return "Croissance"

    # Retournement: gros drawdown + rebond
    if dist_52w is not None and dist_52w < -25 and trend in ("Haussière faible", "Haussière"):
        return "Retournement"

    # Survendue : RSI bas + pas de chute excessive
    if rsi is not None and rsi < 35 and ytd is not None and ytd > -25:
        return "Survendue"

    # Piège de valeur: PE bas + tendance baissière + marges faibles ou inexistantes
    if pe is not None and 0 < pe < 12 and trend == "Baissière" and (pm is None or pm < 0.03):
        return "Piège de valeur"

    # Rebond cyclique
    if ytd is not None and ytd < -15 and trend == "Haussière faible":
        return "Rebond cyclique"

    # Défensive : tendance neutre/positive + dividende implicite
    if trend in ("Haussière", "Haussière faible") and ytd is not None and 0 < ytd < 15:
        return "Défensive"

    # Momentum sans fondamentaux → croissance présumée
    if trend == "Haussière" and ytd is not None and ytd > 5:
        return "Momentum"

    if trend == "Baissière":
        return "Sous pression"

    return "Mixte"


def recommendation(score: float, profile_: str, risk: str) -> str:
    if profile_ == "Piège de valeur":
        return "ÉVITER"
    if profile_ == "Sous pression" and score < 55:
        return "ÉVITER"
    # ACHAT: score solide + risque pas extrême, ou profils de qualité avec score correct
    if score >= 65 and risk != "Élevé":
        return "ACHAT"
    if score >= 70:
        return "ACHAT"
    if profile_ in ("Qualité", "Qualité décotée", "Croissance", "Retournement") and score >= 55:
        return "ACHAT"
    if score >= 50:
        return "SURVEILLANCE"
    if score < 35:
        return "ÉVITER"
    return "SURVEILLANCE"


def outlook(trend: str | None, score: float, profile_: str) -> dict:
    """Perspectives court / moyen / long terme."""
    short = "Neutre"
    mid = "Neutre"
    long = "Neutre"

    if trend == "Haussière":
        short = "Positive"
    elif trend == "Baissière":
        short = "Négative"
    elif trend and "faible" in trend:
        short = "Mitigée"

    if score >= 70:
        mid = "Positive"
    elif score < 50:
        mid = "Négative"

    if profile_ in ("Qualité", "Qualité décotée", "Croissance"):
        long = "Positive"
    elif profile_ in ("Piège de valeur", "Spéculatif"):
        long = "Négative"

    return {"court": short, "moyen": mid, "long": long}
