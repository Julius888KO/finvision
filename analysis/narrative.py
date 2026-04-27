"""Génère des paragraphes d'analyse court/moyen/long terme en français.

Sans markdown ** — utilisation de balises HTML <strong> et <span> pour la mise en valeur.
"""

from __future__ import annotations


# ---------- Helpers ----------

def _num(v):
    if v is None:
        return None
    try:
        f = float(v)
        if f != f:
            return None
        return f
    except (TypeError, ValueError):
        return None


def _b(text: str) -> str:
    """Mise en gras sans markdown."""
    return f'<strong style="color:#ffffff;">{text}</strong>'


def _hi(text: str, color: str = "#a78bfa") -> str:
    """Surligne en couleur."""
    return f'<strong style="color:{color};">{text}</strong>'


def _p(text: str) -> str:
    """Paragraphe."""
    return f'<p style="margin:.4rem 0 .9rem 0;">{text}</p>'


def _h(text: str) -> str:
    """Sous-titre."""
    return f'<div style="color:#a78bfa; font-size:.82rem; font-weight:600; letter-spacing:.06em; text-transform:uppercase; margin:.9rem 0 .4rem 0;">{text}</div>'


# ---------- Court terme ----------

def analyse_court_terme(row) -> str:
    """Analyse détaillée sur 1 à 3 mois : technique, momentum, niveaux, risque tactique."""
    trend = row.get("Tendance")
    rsi = _num(row.get("RSI"))
    price = _num(row.get("Prix"))
    ma50 = _num(row.get("MA50"))
    ma200 = _num(row.get("MA200"))
    ytd = _num(row.get("YTD %"))
    dist_high = _num(row.get("Dist_52W_High"))
    dist_low = _num(row.get("Dist_52W_Low"))
    support = _num(row.get("Support"))
    resistance = _num(row.get("Résistance"))
    vol = _num(row.get("Volatilité")) or _num(row.get("Volatility"))
    beta = _num(row.get("Beta"))
    ticker = row.get("Ticker") or ""
    company = row.get("Entreprise") or ticker

    out = []

    # Intro
    intro_parts = []
    intro_parts.append(
        f"Sur l'horizon tactique des {_b('1 à 3 mois')}, l'analyse de {_b(str(company))} "
        f"s'appuie principalement sur les signaux techniques, le momentum récent et la position "
        f"relative du cours par rapport à ses moyennes mobiles et à ses niveaux clés."
    )
    out.append(_p(" ".join(intro_parts)))

    # --- Tendance ---
    out.append(_h("Structure de tendance"))
    tr = []
    if trend == "Haussière":
        tr.append(
            f"Le titre évolue dans une {_hi('tendance haussière structurée', '#4ade80')} : "
            f"le cours est au-dessus des moyennes mobiles 50 et 200 jours, et la MM50 se situe "
            f"au-dessus de la MM200 (configuration dite « golden cross »)."
        )
        tr.append(
            "Ce type de configuration technique historiquement favorable indique une dynamique acheteuse "
            "installée. Les retracements vers la MM50 constituent généralement des zones d'entrée à privilégier."
        )
    elif trend == "Haussière faible":
        tr.append(
            f"La tendance est {_hi('modérément haussière', '#facc15')} : la MM50 remonte au-dessus de la MM200 "
            f"mais l'écart reste étroit, ce qui traduit une phase de stabilisation après correction."
        )
        tr.append(
            "Tant que le cours respecte la MM50 en support glissant, la probabilité de continuation "
            "haussière reste favorable, sans euphorie."
        )
    elif trend == "Baissière":
        tr.append(
            f"Le titre est en {_hi('tendance baissière confirmée', '#f87171')} : cours sous les deux moyennes mobiles, "
            f"MM50 sous MM200 (« death cross »)."
        )
        tr.append(
            "Dans ce type de configuration, tenter d'attraper un couteau qui tombe est statistiquement "
            "perdant. Mieux vaut attendre une reprise de la MM50, une cassure de résistance ou une "
            "divergence haussière sur le RSI hebdomadaire avant toute initiation."
        )
    elif trend == "Baissière faible":
        tr.append(
            f"La tendance court terme est {_hi('fragile', '#facc15')}, sans excès baissier mais sans signal "
            f"de reprise confirmé. Le cours peut retester ses supports avant de choisir une direction."
        )
    else:
        tr.append("La tendance technique n'est pas nettement définie sur les derniers mois : phase de range ou consolidation horizontale.")

    if price and ma50 and ma200:
        if price > ma50 > ma200:
            tr.append(f"Prix ({price:.2f}) > MM50 ({ma50:.2f}) > MM200 ({ma200:.2f}) : empilement haussier classique.")
        elif price < ma50 < ma200:
            tr.append(f"Prix ({price:.2f}) < MM50 ({ma50:.2f}) < MM200 ({ma200:.2f}) : empilement baissier — attendre inversion.")
        elif price > ma200 and price < ma50:
            tr.append(f"Le cours ({price:.2f}) est sous la MM50 ({ma50:.2f}) mais tient la MM200 ({ma200:.2f}) — zone de test clé.")

    out.append(_p(" ".join(tr)))

    # --- Momentum / RSI ---
    out.append(_h("Momentum et force relative"))
    mom = []
    if rsi is not None:
        if rsi > 75:
            mom.append(
                f"Le {_b('RSI (14 jours)')} affiche {_hi(f'{rsi:.1f}', '#f87171')}, caractéristique d'un "
                f"{_b('surachat marqué')}. Statistiquement, au-delà de 75, la probabilité d'une respiration "
                f"ou d'un repli temporaire augmente significativement sur les 2-4 semaines qui suivent."
            )
            mom.append(
                "Cela ne signifie pas que la tendance va s'inverser : un titre en momentum puissant "
                "peut rester suracheté longtemps. Mais pour une nouvelle entrée, patienter un retour "
                "vers la zone 55-60 réduit le risque de timing."
            )
        elif rsi > 65:
            mom.append(
                f"Le RSI à {_hi(f'{rsi:.1f}', '#facc15')} traduit une {_b('zone de surchauffe modérée')} : "
                f"momentum fort, mais l'élasticité du cours commence à se tendre."
            )
        elif 45 <= rsi <= 65:
            mom.append(
                f"Le RSI à {_hi(f'{rsi:.1f}', '#4ade80')} se situe en {_b('zone neutre-constructive')}, "
                f"cohérent avec un comportement sain — ni euphorie ni panique."
            )
        elif 30 <= rsi < 45:
            mom.append(
                f"Le RSI à {_hi(f'{rsi:.1f}', '#facc15')} suggère un momentum faible. "
                f"Une consolidation est probablement en cours ; surveiller un retour au-dessus de 50 "
                f"comme signal de reprise."
            )
        else:
            mom.append(
                f"Le RSI à {_hi(f'{rsi:.1f}', '#4ade80')} place le titre en {_b('état de survente technique')}. "
                f"Historiquement, cette zone favorise un rebond mécanique, mais la qualité du rebond "
                f"dépend de la confirmation par d'autres signaux (cassure de MM20, divergence haussière, "
                f"volume d'accumulation)."
            )
    else:
        mom.append("Données de RSI indisponibles — lecture du momentum limitée à l'action des prix.")

    if ytd is not None:
        if ytd > 25:
            mom.append(f"La performance YTD de {_hi(f'+{ytd:.1f}%', '#4ade80')} confirme un momentum annuel très fort.")
        elif ytd > 0:
            mom.append(f"La performance YTD de {_hi(f'+{ytd:.1f}%', '#4ade80')} reste positive, en ligne avec les indices de référence.")
        elif ytd > -15:
            mom.append(f"La performance YTD de {_hi(f'{ytd:.1f}%', '#facc15')} témoigne d'une période difficile mais pas de capitulation.")
        else:
            mom.append(f"La performance YTD de {_hi(f'{ytd:.1f}%', '#f87171')} reflète un décrochage significatif, souvent lié à un catalyseur négatif spécifique ou à une rotation sectorielle défavorable.")
    out.append(_p(" ".join(mom)))

    # --- Niveaux ---
    out.append(_h("Niveaux techniques et gestion du risque"))
    lvl = []
    if support and resistance and price:
        mid = (support + resistance) / 2
        pos_pct = (price - support) / (resistance - support) * 100 if resistance != support else 50
        lvl.append(
            f"Les niveaux clés à surveiller : {_b('support')} à {_hi(f'${support:.2f}', '#4ade80')} "
            f"et {_b('résistance')} à {_hi(f'${resistance:.2f}', '#f87171')}. "
            f"Au cours actuel ({_b(f'${price:.2f}')}), le titre se situe à {_b(f'{pos_pct:.0f}%')} "
            f"de la fourchette entre ces deux bornes."
        )
        if pos_pct > 70:
            lvl.append("Position haute de range : risque asymétrique défavorable sur une nouvelle entrée — privilégier un pullback.")
        elif pos_pct < 30:
            lvl.append("Position basse de range : risk/reward plus intéressant, à condition que le support absorbe la pression vendeuse.")
        else:
            lvl.append(
                f"Position médiane de range. Un stop-loss technique se placerait sous ${support*0.97:.2f} "
                f"(environ 3% sous le support), pour un objectif initial de résistance à ${resistance:.2f}."
            )
    if dist_high is not None:
        if dist_high > -3:
            lvl.append(f"Le titre cote {_hi('à proximité du plus haut 52 semaines', '#4ade80')} — dynamique très favorable mais attention au pullback technique.")
        elif dist_high > -15:
            lvl.append(f"Le cours est à {_b(f'{dist_high:.1f}%')} du plus haut 52 semaines : marge de progression raisonnable sans être extrême.")
        elif dist_high > -30:
            lvl.append(f"Le titre a corrigé de {_hi(f'{dist_high:.1f}%', '#facc15')} depuis son plus haut — un rebond technique est envisageable si le support actuel tient.")
        else:
            lvl.append(f"{_hi(f'Drawdown sévère ({dist_high:.1f}%)', '#f87171')} depuis le plus haut — le retournement demande des catalyseurs solides, pas seulement un rebond technique.")
    out.append(_p(" ".join(lvl)))

    # --- Volatilité / beta ---
    if vol is not None or beta is not None:
        out.append(_h("Volatilité et comportement de marché"))
        vb = []
        if vol is not None:
            if vol > 0.5:
                vb.append(f"La volatilité annualisée est {_hi('élevée', '#f87171')} ({vol*100:.0f}%) — mouvements amples, position à dimensionner prudemment.")
            elif vol > 0.3:
                vb.append(f"La volatilité annualisée est {_b('modérée')} ({vol*100:.0f}%), typique d'une action de croissance.")
            else:
                vb.append(f"La volatilité annualisée est {_hi('faible', '#4ade80')} ({vol*100:.0f}%) — comportement de valeur défensive.")
        if beta is not None:
            if beta > 1.3:
                vb.append(f"Beta de {beta:.2f} : sensibilité amplifiée au marché global (+1% indice ≈ +{beta:.1f}% sur le titre).")
            elif beta < 0.8:
                vb.append(f"Beta de {beta:.2f} : réactions amorties, bon diversifiant défensif.")
            else:
                vb.append(f"Beta de {beta:.2f} : réaction alignée sur le marché.")
        out.append(_p(" ".join(vb)))

    # --- Synthèse tactique ---
    out.append(_h("Synthèse tactique"))
    synth = []
    bull = 0
    bear = 0
    if trend in ("Haussière", "Haussière faible"): bull += 1
    if trend in ("Baissière", "Baissière faible"): bear += 1
    if rsi is not None:
        if 30 <= rsi <= 65: bull += 1
        if rsi < 30: bull += 1  # survente = rebond possible
        if rsi > 75: bear += 1
    if ytd is not None:
        if ytd > 5: bull += 1
        if ytd < -15: bear += 1
    if dist_high is not None:
        if dist_high > -10: bull += 1
        if dist_high < -25: bear += 1

    if bull >= bear + 2:
        synth.append(f"La balance des signaux court terme est {_hi('favorable', '#4ade80')} : les voyants techniques, le momentum et la position dans la fourchette convergent vers un biais acheteur sur l'horizon 1 à 3 mois.")
        synth.append("Stratégie : privilégier les pullbacks techniques plutôt que le momentum pur, placer un stop sous le dernier support significatif et viser la résistance majeure.")
    elif bear >= bull + 2:
        synth.append(f"La balance des signaux court terme est {_hi('défavorable', '#f87171')} : multiples feux rouges techniques. La probabilité d'une poursuite du mouvement baissier domine.")
        synth.append("Stratégie : éviter les entrées en longue sans confirmation (cassure MM50 + croisement RSI, ou divergence haussière claire). Pour les porteurs, envisager un hedge ou un allègement.")
    else:
        synth.append(f"La balance des signaux est {_hi('mitigée', '#facc15')} — situation de marché indécise sans edge clair.")
        synth.append("Stratégie : patience. Attendre une confirmation technique (cassure de range, regain RSI au-dessus de 55, croisement MM50/MM200) avant d'engager du capital.")
    out.append(_p(" ".join(synth)))

    return "".join(out)


# ---------- Moyen terme ----------

def analyse_moyen_terme(row, info: dict | None = None) -> str:
    """Analyse détaillée sur 6 à 18 mois : valorisation, rentabilité, croissance, profil."""
    info = info or {}
    pe = _num(row.get("PE") or info.get("trailingPE"))
    forward_pe = _num(row.get("Forward_PE") or info.get("forwardPE"))
    peg = _num(row.get("PEG") or info.get("pegRatio"))
    pb = _num(row.get("P/B") or info.get("priceToBook"))
    ps = _num(info.get("priceToSalesTrailing12Months"))
    ev_ebitda = _num(info.get("enterpriseToEbitda"))
    pm = _num(row.get("Marge_Profit") or info.get("profitMargins"))
    om = _num(row.get("Marge_Op") or info.get("operatingMargins"))
    gm = _num(info.get("grossMargins"))
    roe = _num(row.get("ROE") or info.get("returnOnEquity"))
    roa = _num(info.get("returnOnAssets"))
    rev_g = _num(row.get("Revenue_Growth") or info.get("revenueGrowth"))
    eps_g = _num(row.get("Earnings_Growth") or info.get("earningsGrowth"))
    de = _num(row.get("Debt_Equity") or info.get("debtToEquity"))
    cr = _num(info.get("currentRatio"))
    fcf = _num(info.get("freeCashflow"))
    mc = _num(row.get("Capitalisation") or info.get("marketCap"))
    sector = row.get("Secteur") or "—"
    profile_ = row.get("Profil") or "—"
    company = row.get("Entreprise") or row.get("Ticker") or ""

    out = []

    # Intro
    out.append(_p(
        f"L'horizon {_b('6 à 18 mois')} pour {_b(str(company))} se joue sur la convergence entre valorisation, "
        f"dynamique bénéficiaire, qualité des marges et solidité du bilan. Cette échelle de temps permet aux "
        f"fondamentaux de s'imposer face au bruit de marché, à condition qu'aucun choc macro majeur ne vienne "
        f"rebattre les cartes entre-temps."
    ))

    # --- Valorisation ---
    out.append(_h("Valorisation"))
    val = []
    if pe and pe > 0:
        if pe < 12:
            val.append(f"PER TTM de {_hi(f'{pe:.1f}', '#4ade80')} : {_b('valorisation décotée')}, souvent signe d'un marché prudent (secteur cyclique, fin de cycle, révisions baissières intégrées) ou d'une opportunité si les fondamentaux sont intacts.")
        elif pe < 20:
            val.append(f"PER TTM de {_hi(f'{pe:.1f}', '#4ade80')} : valorisation {_b('dans la norme historique')} du marché (S&P 500 moyenne historique ~16-18x).")
        elif pe < 35:
            val.append(f"PER TTM de {_hi(f'{pe:.1f}', '#facc15')} : valorisation {_b('légèrement tendue')}, à justifier par une croissance supérieure à la moyenne.")
        else:
            val.append(f"PER TTM de {_hi(f'{pe:.1f}', '#f87171')} : valorisation {_b('élevée')} — le marché price une forte croissance future, toute déception peut être sévèrement sanctionnée.")

    if forward_pe and pe and forward_pe < pe * 0.85:
        val.append(f"Le PER forward ({forward_pe:.1f}) est nettement inférieur au TTM ({pe:.1f}) : le consensus anticipe une {_hi('hausse des bénéfices', '#4ade80')} dans les 12 prochains mois — signal positif.")
    elif forward_pe and pe and forward_pe > pe * 1.1:
        val.append(f"Le PER forward ({forward_pe:.1f}) est supérieur au TTM : attention, {_hi('révisions baissières', '#f87171')} potentielles des résultats à venir.")

    if peg and peg > 0:
        if peg < 1:
            val.append(f"PEG de {_hi(f'{peg:.2f}', '#4ade80')} (inférieur à 1) : la valorisation est {_b('attractive au regard du taux de croissance')} — configuration recherchée.")
        elif peg < 2:
            val.append(f"PEG de {_b(f'{peg:.2f}')} : ratio équilibré, la croissance justifie la prime de valorisation.")
        else:
            val.append(f"PEG de {_hi(f'{peg:.2f}', '#facc15')} : prime de valorisation élevée par rapport à la croissance.")

    if pb:
        if pb < 1:
            val.append(f"P/B de {_hi(f'{pb:.2f}', '#4ade80')} : cours sous la valeur comptable, souvent valeur profonde (ou piège de valeur selon la qualité du bilan).")
        elif pb > 5:
            val.append(f"P/B de {_b(f'{pb:.2f}')} : élevé, peu significatif pour une entreprise asset-light (tech, services) mais à surveiller pour une industrie capitalistique.")
    if ev_ebitda:
        if ev_ebitda < 10:
            val.append(f"EV/EBITDA de {_hi(f'{ev_ebitda:.1f}', '#4ade80')} : multiple modéré, cohérent avec une valorisation raisonnable.")
        elif ev_ebitda > 20:
            val.append(f"EV/EBITDA de {_hi(f'{ev_ebitda:.1f}', '#facc15')} : multiple élevé, qui suppose des perspectives de rentabilité soutenues.")
    if ps:
        val.append(f"Ratio cours/ventes de {_b(f'{ps:.2f}')}.")
    if not val:
        val.append("Données de valorisation partiellement indisponibles — lecture limitée.")
    out.append(_p(" ".join(val)))

    # --- Rentabilité ---
    out.append(_h("Rentabilité et qualité opérationnelle"))
    prof = []
    if pm is not None:
        if pm > 0.20:
            prof.append(f"Marge nette de {_hi(f'{pm*100:.1f}%', '#4ade80')} : {_b('excellente')}, caractéristique d'une entreprise disposant d'un avantage concurrentiel (pricing power, technologie, marque forte).")
        elif pm > 0.10:
            prof.append(f"Marge nette de {_hi(f'{pm*100:.1f}%', '#4ade80')} : {_b('solide')}, dans la partie haute du spectre industriel.")
        elif pm > 0.03:
            prof.append(f"Marge nette de {_b(f'{pm*100:.1f}%')} : correcte sans être remarquable — probablement un business à marges structurellement fines (distribution, commodity).")
        elif pm > 0:
            prof.append(f"Marge nette de {_hi(f'{pm*100:.1f}%', '#facc15')} : rentabilité fragile, peu de coussin en cas de dégradation du cycle.")
        else:
            prof.append(f"Marge nette de {_hi(f'{pm*100:.1f}%', '#f87171')} : {_b('perte nette')} — thèse de redressement à vérifier impérativement.")

    if om is not None:
        prof.append(f"Marge opérationnelle à {_b(f'{om*100:.1f}%')} : indicateur clé de l'efficacité hors effets financiers et fiscaux.")
    if gm is not None:
        prof.append(f"Marge brute à {_b(f'{gm*100:.1f}%')} — plancher de rentabilité structurelle.")

    if roe is not None and roe > 0:
        if roe > 0.20:
            prof.append(f"ROE de {_hi(f'{roe*100:.1f}%', '#4ade80')} : {_b('très bonne rentabilité des capitaux propres')}, au-dessus du coût du capital. Les entreprises qui soutiennent durablement un ROE > 15% sont souvent des compounders de long terme.")
        elif roe > 0.10:
            prof.append(f"ROE de {_b(f'{roe*100:.1f}%')} : rentabilité correcte, sans être exceptionnelle.")
        else:
            prof.append(f"ROE de {_hi(f'{roe*100:.1f}%', '#facc15')} : modeste, interroge sur l'efficacité de l'allocation du capital.")
    if roa is not None and roa > 0:
        prof.append(f"ROA de {_b(f'{roa*100:.1f}%')} — rentabilité rapportée à l'ensemble des actifs.")
    out.append(_p(" ".join(prof)))

    # --- Croissance ---
    out.append(_h("Dynamique de croissance"))
    gr = []
    if rev_g is not None:
        if rev_g > 0.20:
            gr.append(f"Chiffre d'affaires en {_hi(f'hyper-croissance (+{rev_g*100:.1f}%)', '#4ade80')} — profil de leader d'un marché en expansion.")
        elif rev_g > 0.10:
            gr.append(f"Revenus en {_hi(f'forte croissance (+{rev_g*100:.1f}%)', '#4ade80')} — dynamique commerciale solide.")
        elif rev_g > 0.03:
            gr.append(f"Revenus en progression modérée ({_b(f'+{rev_g*100:.1f}%')}).")
        elif rev_g > 0:
            gr.append(f"Revenus quasi stables ({_b(f'+{rev_g*100:.1f}%')}) — absence de dynamique top-line.")
        else:
            gr.append(f"Revenus en recul ({_hi(f'{rev_g*100:.1f}%', '#f87171')}) — signal de dégradation de la demande ou des parts de marché.")

    if eps_g is not None:
        if eps_g > 0.20:
            gr.append(f"Bénéfice par action en {_hi(f'forte hausse (+{eps_g*100:.1f}%)', '#4ade80')} — effet ciseau positif (croissance + marges) souvent favorable au cours.")
        elif eps_g > 0:
            gr.append(f"BPA en hausse ({_b(f'+{eps_g*100:.1f}%')}).")
        else:
            gr.append(f"BPA en baisse ({_hi(f'{eps_g*100:.1f}%', '#f87171')}) — vigilance particulière à l'exercice à venir.")

    if not gr:
        gr.append("Données de croissance indisponibles — zone d'ombre à combler via les publications de résultats.")
    out.append(_p(" ".join(gr)))

    # --- Santé financière ---
    out.append(_h("Solidité du bilan"))
    fin = []
    if de is not None:
        if de < 50:
            fin.append(f"Ratio Dette/Capitaux propres de {_hi(f'{de:.0f}', '#4ade80')} : {_b('bilan très sain')}, grande flexibilité stratégique et défensive.")
        elif de < 150:
            fin.append(f"Dette/Capitaux propres de {_b(f'{de:.0f}')} : endettement maîtrisé, dans la norme pour beaucoup de secteurs matures.")
        elif de < 300:
            fin.append(f"Dette/Capitaux propres de {_hi(f'{de:.0f}', '#facc15')} : endettement élevé — point de vigilance en environnement de taux élevés.")
        else:
            fin.append(f"Dette/Capitaux propres de {_hi(f'{de:.0f}', '#f87171')} : {_b('endettement très élevé')} — fragilité structurelle en cas de ralentissement économique.")
    if cr is not None:
        if cr >= 1.5:
            fin.append(f"Ratio de liquidité courante de {_hi(f'{cr:.2f}', '#4ade80')} : liquidité confortable.")
        elif cr >= 1:
            fin.append(f"Ratio de liquidité courante de {_b(f'{cr:.2f}')} : couverture des obligations court terme correcte.")
        else:
            fin.append(f"Ratio de liquidité courante de {_hi(f'{cr:.2f}', '#f87171')} : {_b('tension potentielle')} sur la trésorerie court terme.")
    if fcf is not None:
        if fcf > 0:
            fin.append(f"{_hi('Free cash-flow positif', '#4ade80')} — capacité à financer investissements, dividendes et rachats sans s'endetter davantage.")
        else:
            fin.append(f"{_hi('Free cash-flow négatif', '#f87171')} — dépendance au financement externe, contrainte en environnement de taux élevés.")
    if not fin:
        fin.append("Données de bilan indisponibles — vérifier via le rapport annuel.")
    out.append(_p(" ".join(fin)))

    # --- Profil ---
    profile_text = {
        "Qualité": f"Profil {_hi('Qualité', '#4ade80')} : marges élevées, rentabilité supérieure, franchise durable. Sur 6-18 mois, ce type de titre tend à résister mieux que la moyenne aux phases de stress de marché.",
        "Qualité décotée": f"Profil {_hi('Qualité décotée', '#4ade80')} : fondamentaux solides combinés à une valorisation attractive — configuration value-quality historiquement l'une des plus rentables à moyen terme.",
        "Valeur": f"Profil {_hi('Valeur', '#4ade80')} : le marché pourrait sous-estimer le potentiel de normalisation. Patience requise, la ré-évaluation peut prendre plusieurs trimestres.",
        "Croissance": f"Profil {_hi('Croissance', '#a78bfa')} : thèse adossée à la poursuite de l'expansion — surveiller de près les révisions d'estimations trimestre après trimestre.",
        "Retournement": f"Profil {_hi('Retournement', '#facc15')} : le titre sort d'une période difficile — à confirmer par au moins deux trimestres de surprise positive sur les résultats.",
        "Survendue": f"Statut {_hi('Survendu', '#4ade80')} : opportunité tactique intéressante si les fondamentaux restent intacts — fenêtre de ré-accumulation typiquement limitée à quelques semaines/mois.",
        "Rebond cyclique": f"Profil {_hi('Rebond cyclique', '#facc15')} : dépend directement du cycle économique ; surveiller les indicateurs avancés (PMI, confiance, commandes industrielles).",
        "Défensive": f"Profil {_hi('Défensif', '#4ade80')} : visibilité et régularité des flux — adapté à un cœur de portefeuille, moins exposé aux drawdowns majeurs.",
        "Momentum": f"Profil {_hi('Momentum', '#a78bfa')} : dynamique forte mais sensible aux rotations de marché. Peut subir des pull-backs violents lors de changements de régime.",
        "Piège de valeur": f"{_hi('Piège de valeur', '#f87171')} : prix bas sans catalyseur crédible de retournement — prudence extrême, coût d'opportunité potentiellement élevé.",
        "Sous pression": f"Profil {_hi('Sous pression', '#f87171')} structurelle — éviter d'anticiper un creux non confirmé par les fondamentaux.",
        "Spéculatif": f"Profil {_hi('Spéculatif', '#f87171')} : risque/récompense asymétrique, allouer avec parcimonie (position symbolique) et définir à l'avance un stop de thèse.",
        "Mixte": "Profil mixte : signaux contrastés, à étudier au cas par cas selon les axes dominants.",
    }
    if profile_ in profile_text:
        out.append(_h("Lecture de profil"))
        out.append(_p(profile_text[profile_]))

    # Synthèse
    out.append(_h("Synthèse moyen terme"))
    out.append(_p(
        f"Sur {_b('6 à 18 mois')}, la clé de lecture est la capacité de l'entreprise à délivrer (ou non) "
        f"la trajectoire bénéficiaire intégrée dans le consensus. Les prochaines publications trimestrielles "
        f"constituent les catalyseurs majeurs : un beat régulier soutient la ré-évaluation, un miss déclenche "
        f"souvent des corrections marquées. Compléter l'analyse par la lecture du rapport annuel et des guidance "
        f"management est indispensable avant engagement significatif."
    ))

    return "".join(out)


# ---------- Long terme ----------

def analyse_long_terme(row, info: dict | None = None) -> str:
    """Analyse détaillée sur 3 à 10 ans : moat, qualité business, secteur, composition."""
    info = info or {}
    sector = row.get("Secteur") or "—"
    industry = row.get("Industrie") or info.get("industry") or "—"
    profile_ = row.get("Profil") or "—"
    roe = _num(row.get("ROE") or info.get("returnOnEquity"))
    pm = _num(row.get("Marge_Profit") or info.get("profitMargins"))
    gm = _num(info.get("grossMargins"))
    cap = _num(row.get("Capitalisation") or info.get("marketCap"))
    beta = _num(row.get("Beta") or info.get("beta"))
    div_yield = _num(row.get("Dividende_Yield"))
    payout = _num(info.get("payoutRatio"))
    rev_g = _num(row.get("Revenue_Growth") or info.get("revenueGrowth"))
    company = row.get("Entreprise") or row.get("Ticker") or ""
    cap_cat = row.get("Cap_Catégorie") or "—"

    out = []

    # Intro
    out.append(_p(
        f"L'horizon {_b('3 à 10 ans')} pour {_b(str(company))} dépasse largement les cycles conjoncturels. "
        f"À cette échelle, la création de valeur dépend principalement de la qualité intrinsèque du business : "
        f"force de la franchise, barrières à l'entrée, capacité de réinvestissement à rendement élevé, et "
        f"positionnement face aux grandes tendances structurelles du secteur."
    ))

    # --- Capitalisation ---
    out.append(_h("Positionnement et taille"))
    pos = []
    if cap_cat == "Mega Cap":
        pos.append(
            f"Statut {_hi('mega-capitalisation', '#4ade80')} : généralement un {_b('leader mondial')} de son secteur, "
            f"bénéficiant d'effets d'échelle, de pricing power et d'une forte prime de liquidité. Profil typiquement "
            f"core holding de long terme, accès simplifié aux ETF / fonds, sensibilité moindre aux cycles isolés."
        )
    elif cap_cat == "Large Cap":
        pos.append(
            f"Statut {_b('large-capitalisation')} : acteur établi, ressources pour investir dans la R&D et l'international. "
            f"Le risque d'exécution est généralement contenu, mais la croissance organique plafonne parfois."
        )
    elif cap_cat == "Mid Cap":
        pos.append(
            f"Statut {_hi('mid-capitalisation', '#a78bfa')} : zone historiquement la plus rentable du marché sur le long terme "
            f"(entre la maturité des large caps et la volatilité des small caps). Potentiel de réévaluation supérieur, "
            f"mais exécution management déterminante."
        )
    elif cap_cat in ("Small Cap", "Micro Cap"):
        pos.append(
            f"Statut {_hi('small/micro-capitalisation', '#facc15')} : profil risque/rendement élevé. "
            f"Exposition aux cycles, à la liquidité et au risque idiosyncratique. Allocation à dimensionner "
            f"prudemment (souvent via un panier plutôt qu'une conviction isolée)."
        )
    out.append(_p(" ".join(pos)))

    # --- Moat / qualité ---
    out.append(_h("Qualité intrinsèque et moat économique"))
    q = []
    if roe and pm and gm:
        if roe > 0.18 and pm > 0.15 and gm > 0.40:
            q.append(
                f"Les trois marqueurs classiques de {_hi('qualité business', '#4ade80')} sont au vert : "
                f"marge brute élevée ({gm*100:.0f}%), marge nette robuste ({pm*100:.1f}%), ROE supérieur à 18% ({roe*100:.1f}%). "
                f"Cette combinaison suggère l'existence d'un {_b('moat économique durable')} — avantage concurrentiel "
                f"protégé par au moins un mécanisme parmi : marque forte, effets de réseau, switching costs, avantage de coût, "
                f"actifs intangibles (brevets, licences, régulation). Ce type de profil est typique des entreprises "
                f"capables de composer leur valeur sur plus de 10 ans."
            )
        elif roe > 0.12 and pm > 0.08:
            q.append(
                f"La rentabilité structurelle est {_b('correcte')} (ROE {roe*100:.1f}%, marge nette {pm*100:.1f}%), "
                f"sans moat évident mais sans faiblesse rédhibitoire. L'investissement long terme dépendra "
                f"principalement de la capacité à maintenir ce niveau face à la concurrence."
            )
        else:
            q.append(
                f"Les métriques de qualité long terme sont {_hi('en retrait', '#facc15')} — préférer une lecture tactique "
                f"plutôt que buy-and-hold, ou conditionner l'investissement à un catalyseur clair de redressement."
            )
    else:
        q.append("Métriques de qualité partiellement disponibles — compléter par la lecture du rapport annuel.")

    if rev_g is not None and rev_g > 0.10:
        q.append(f"La croissance récente à {_b(f'+{rev_g*100:.0f}%')} témoigne d'une dynamique structurelle active.")
    out.append(_p(" ".join(q)))

    # --- Secteur / tendances ---
    out.append(_h("Perspective sectorielle"))
    sector_outlook = {
        "Technologie": (
            f"Le secteur {_hi('technologique', '#a78bfa')} bénéficie de tailwinds structurels puissants : intelligence artificielle générative, "
            f"cloud computing, cybersécurité, digitalisation des entreprises, semi-conducteurs pour l'IA. "
            f"Les CAGR attendus sur 5-10 ans restent parmi les plus élevés du marché. Revers : valorisations souvent tendues, "
            f"cycles de capex intensifs, risque réglementaire croissant (antitrust, IA, data privacy)."
        ),
        "Santé": (
            f"Le secteur {_hi('santé', '#4ade80')} bénéficie du {_b('vieillissement démographique mondial')}, de l'innovation biotech "
            f"(thérapies géniques, GLP-1, oncologie ciblée) et de la montée en puissance de l'IA médicale. "
            f"Défensif et porteur sur le long terme. Risques : pression sur les prix (IRA aux USA, politiques européennes), "
            f"cycles de R&D longs, incertitude des phases cliniques."
        ),
        "Finance": (
            f"Le secteur {_b('financier')} reste sensible à la courbe des taux et au cycle du crédit. "
            f"Les leaders globaux bénéficient d'un rendement du capital attractif (rachats + dividendes). "
            f"Risques structurels : désintermédiation (fintech, crypto), réglementation, cycles de défaut. "
            f"Sur 5-10 ans, les banques fortement capitalisées et les gestionnaires d'actifs tendent à surperformer."
        ),
        "Énergie": (
            f"Le secteur {_b('énergie')} navigue la {_hi('transition énergétique', '#facc15')} : discipline capex, retour du capital aux actionnaires, "
            f"volatilité structurelle des prix du baril. Les majors intégrées investissent désormais autant dans les renouvelables que dans l'upstream. "
            f"Dividendes souvent attrayants, mais risque de stranded assets à surveiller sur les horizons > 10 ans."
        ),
        "Conso. de base": (
            f"Secteur {_hi('consommation de base', '#4ade80')} : résilience, visibilité des cash-flows, croissance limitée mais extrêmement stable. "
            f"Cœur défensif de portefeuille. Challenge actuel : pression sur les marges lié à l'inflation, "
            f"montée des marques distributeurs, changements de mix consommation (santé/premium)."
        ),
        "Conso. discrétionnaire": (
            f"Secteur {_hi('consommation discrétionnaire', '#facc15')} : cyclique, sensible au pouvoir d'achat, aux taux et à la confiance des ménages. "
            f"Dispersion forte entre luxe (résilient), e-commerce (disruptif), automobile (transition EV), retail traditionnel (sous pression)."
        ),
        "Industrie": (
            f"Le secteur {_b('industriel')} reflète la conjoncture économique globale. Tendances porteuses : {_hi('relocalisation', '#a78bfa')}, "
            f"automatisation, défense, infrastructure verte. Les leaders avec carnets de commandes longs bénéficient d'une visibilité supérieure."
        ),
        "Matériaux": (
            f"Secteur {_b('matériaux')} : exposition aux {_hi('cycles des commodities', '#facc15')}, infrastructure verte (cuivre, lithium, aluminium), "
            f"et demande chinoise. Volatilité forte, idéal pour allocation tactique plus que cœur de portefeuille."
        ),
        "Services publics": (
            f"Secteur {_hi('utilities', '#4ade80')} : revenus régulés, dividendes généreux, sensibles aux taux longs. "
            f"Transition énergétique et électrification massive (véhicules, data centers, chauffage) soutiennent la demande long terme."
        ),
        "Immobilier": (
            f"{_b('REITs')} : rendement distribué attractif, corrélation inverse aux taux longs. "
            f"Dispersion importante entre sous-secteurs : data centers (croissance IA), logistique (e-commerce), résidentiel, retail (en mutation), "
            f"bureaux (post-COVID difficile)."
        ),
        "Communication": (
            f"Secteur {_b('communication/média')} : entre télécoms matures (dividendes, dette élevée) et plateformes digitales "
            f"(Meta, Alphabet, Netflix...) en croissance forte. Dispersion extrême des profils et des valorisations."
        ),
    }
    if sector in sector_outlook:
        out.append(_p(sector_outlook[sector]))
    else:
        out.append(_p(f"Secteur : {_b(sector)}. Industrie : {_b(industry)}. Étudier les drivers structurels spécifiques avant conviction long terme."))

    # --- Dividende ---
    if div_yield and div_yield > 0.005:
        out.append(_h("Contribution du dividende au rendement total"))
        d = []
        d.append(
            f"Le rendement du dividende à {_hi(f'{div_yield*100:.2f}%', '#4ade80')} contribue mécaniquement "
            f"au rendement total. Sur un horizon 10 ans, un dividende réinvesti peut représenter 30 à 50% "
            f"du Total Return selon le titre."
        )
        if payout is not None:
            if 0 < payout < 0.4:
                d.append(f"Le taux de distribution ({payout*100:.0f}% du bénéfice) laisse une {_hi('marge de progression importante', '#4ade80')} du dividende.")
            elif payout < 0.7:
                d.append(f"Taux de distribution équilibré ({payout*100:.0f}%) — pérennité confortable.")
            elif payout < 1:
                d.append(f"Taux de distribution élevé ({payout*100:.0f}%) — moindre marge en cas de baisse du bénéfice.")
            else:
                d.append(f"Taux de distribution {_hi('supérieur à 100%', '#f87171')} — dividende non couvert par les résultats, risque de coupe.")
        out.append(_p(" ".join(d)))

    # --- Beta ---
    if beta is not None:
        out.append(_h("Comportement dans un portefeuille diversifié"))
        b = []
        if beta < 0.8:
            b.append(f"Beta de {_hi(f'{beta:.2f}', '#4ade80')} : {_b('faible corrélation')} au marché global — diversifiant intéressant, atténue la volatilité du portefeuille agrégé.")
        elif beta > 1.3:
            b.append(f"Beta de {_hi(f'{beta:.2f}', '#facc15')} : {_b('forte sensibilité')} au marché — amplifie les mouvements en tendance, à dimensionner en conséquence.")
        else:
            b.append(f"Beta de {_b(f'{beta:.2f}')} : réaction alignée sur le marché — pas de biais défensif ou agressif particulier.")
        out.append(_p(" ".join(b)))

    # --- Verdict ---
    out.append(_h("Verdict long terme"))
    v = []
    if profile_ == "Qualité":
        v.append(f"{_hi('Candidat sérieux pour une stratégie de compounding', '#4ade80')} via réinvestissement des résultats. Profil défensif-offensif historiquement parmi les plus rémunérateurs sur 10 ans glissants.")
    elif profile_ == "Qualité décotée":
        v.append(f"{_hi('Configuration value-quality', '#4ade80')} — fondamentaux solides à valorisation raisonnable. L'un des profils les plus performants statistiquement à moyen-long terme.")
    elif profile_ in ("Croissance", "Momentum"):
        v.append(f"{_b('Constructif')} si la trajectoire de croissance se confirme. Attention aux rotations de style (growth vs value) qui peuvent entraîner des drawdowns de 30-50% avant reprise.")
    elif profile_ == "Défensive":
        v.append(f"{_hi('Pilier défensif', '#4ade80')} recommandé pour stabiliser la volatilité globale du portefeuille long terme.")
    elif profile_ in ("Valeur", "Retournement"):
        v.append(f"{_b('Thèse de ré-évaluation')} — requiert de la patience (2-5 ans) et une conviction sur le catalyseur de normalisation.")
    elif profile_ in ("Piège de valeur", "Spéculatif", "Sous pression"):
        v.append(f"{_hi('Prudent', '#f87171')} : le dossier demande un catalyseur fondamental clair ou relève d'une gestion tactique plutôt que long terme. Allocation symbolique au mieux.")
    elif profile_ == "Survendue":
        v.append(f"Plutôt {_b('tactique')} que long terme. Vérifier que la survente est technique (et non structurelle) avant d'envisager un buy-and-hold.")
    else:
        v.append("Analyse long terme à compléter avec lecture du business model et stratégie management.")

    v.append(
        "Pour une conviction long terme robuste, compléter cette analyse par : (1) lecture du rapport annuel "
        "le plus récent, (2) analyse concurrentielle du secteur, (3) vérification de l'alignement management / actionnaires "
        "(détention d'actions par les dirigeants, politique de rémunération), (4) historique de création de valeur "
        "(progression du BPA, du dividende, du FCF sur 10 ans)."
    )
    out.append(_p(" ".join(v)))

    return "".join(out)
