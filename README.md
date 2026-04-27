# FinVision — Dashboard Boursier

Application Streamlit d'analyse de marché pour investisseurs et traders.

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

## Structure

```
finvision/
├── app.py                  # Application principale
├── data/
│   ├── universe.py         # Univers d'actions (US + Europe)
│   └── loader.py           # Chargement yfinance + cache
├── analysis/
│   ├── technical.py        # RSI, MM, supports/résistances
│   ├── fundamental.py      # Croissance, marges, dette
│   └── scoring.py          # Score, profil, recommandation
├── ui/
│   ├── styles.py           # CSS premium
│   └── components.py       # Composants UI réutilisables
└── requirements.txt
```

## Données

- Source: Yahoo Finance via `yfinance`
- Univers: ~500+ actions US (S&P 500) + Europe (Stoxx 600 principales)
- Rafraîchissement: toutes les heures (cache Streamlit)
- YTD calculé depuis le 1er janvier 2026

## Notes

Le premier chargement peut prendre plusieurs minutes (téléchargement massif de données).
Les chargements suivants sont instantanés grâce au cache.
