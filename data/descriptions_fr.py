"""Descriptions d'entreprises en français pour les principales valeurs.

Utilisé pour afficher une présentation FR lors de l'ouverture d'un titre,
au lieu du `longBusinessSummary` anglais de Yahoo Finance.
"""

DESCRIPTIONS_FR: dict[str, str] = {
    # ---- US Mega / Large caps ----
    "AAPL": "Apple conçoit, fabrique et commercialise des smartphones (iPhone), ordinateurs personnels (Mac), tablettes (iPad), objets connectés (Apple Watch, AirPods) ainsi qu'un écosystème logiciel et de services (App Store, iCloud, Apple Music, Apple TV+, Apple Pay). Le groupe est l'une des plus grandes capitalisations mondiales et bénéficie d'une marque parmi les plus puissantes au monde.",
    "MSFT": "Microsoft est un leader mondial du logiciel et du cloud. Ses activités couvrent la suite Windows et Office (Microsoft 365), la plateforme cloud Azure (n°2 mondial), les jeux vidéo (Xbox, Activision Blizzard), le réseau professionnel LinkedIn et les solutions d'intelligence artificielle (partenariat avec OpenAI et Copilot).",
    "NVDA": "Nvidia conçoit des processeurs graphiques (GPU) devenus le standard mondial pour l'intelligence artificielle, le calcul haute performance, le gaming et les data centers. La société bénéficie d'un quasi-monopole sur les accélérateurs IA pour l'entraînement des grands modèles.",
    "GOOGL": "Alphabet, maison mère de Google, est le leader mondial de la recherche en ligne et de la publicité digitale. Le groupe possède également YouTube, Android, Google Cloud, Waymo (véhicules autonomes) et DeepMind (IA).",
    "GOOG": "Alphabet (Google) — leader mondial de la recherche en ligne, de la publicité digitale et du cloud (Google Cloud). Possède également YouTube, Android et des activités de pointe en IA (Gemini, DeepMind) et véhicules autonomes (Waymo).",
    "AMZN": "Amazon est le leader mondial du commerce en ligne et l'un des trois grands du cloud public (AWS, première source de profits du groupe). Le groupe est également actif dans la publicité, les services d'abonnement (Prime, Prime Video), la logistique et les dispositifs connectés.",
    "META": "Meta Platforms exploite Facebook, Instagram, WhatsApp et Messenger, avec plus de 3 milliards d'utilisateurs actifs quotidiens. Le groupe tire l'essentiel de ses revenus de la publicité ciblée et investit massivement dans l'intelligence artificielle et le métavers (Reality Labs).",
    "TSLA": "Tesla conçoit et fabrique des véhicules électriques (Model 3, Y, S, X, Cybertruck), des solutions de stockage d'énergie (Powerwall, Megapack) et des panneaux solaires. Le groupe investit dans la conduite autonome (FSD), la robotique humanoïde (Optimus) et l'intelligence artificielle.",
    "BRK-B": "Berkshire Hathaway, dirigée historiquement par Warren Buffett, est un conglomérat diversifié qui détient GEICO (assurance), BNSF (ferroviaire), Berkshire Hathaway Energy, See's Candies, ainsi qu'un vaste portefeuille coté (Apple, Coca-Cola, American Express, Bank of America…).",
    "LLY": "Eli Lilly est l'un des leaders mondiaux de la pharmacie. Le groupe connaît une forte croissance portée par ses médicaments anti-obésité et anti-diabète de type GLP-1 (Mounjaro, Zepbound) et son traitement contre la maladie d'Alzheimer (Kisunla).",
    "AVGO": "Broadcom conçoit des semi-conducteurs pour les réseaux, la connectivité sans fil, le stockage et l'industrie. La société a fortement diversifié son activité via l'acquisition de VMware dans les logiciels d'infrastructure cloud.",
    "JPM": "JPMorgan Chase est la première banque américaine par les actifs. Ses activités couvrent la banque de détail (Chase), la banque d'investissement, la gestion d'actifs et la banque privée. Réputée pour sa solidité et la qualité de son management (Jamie Dimon).",
    "V": "Visa est le n°1 mondial des réseaux de paiement par carte (devant Mastercard). La société perçoit une commission sur chaque transaction effectuée sur son réseau, un modèle à marges très élevées et effet de réseau puissant.",
    "XOM": "ExxonMobil est une major pétrolière intégrée, active dans l'exploration-production, le raffinage et la pétrochimie. Le groupe investit aussi dans les technologies bas carbone (CCS, hydrogène, biocarburants).",
    "UNH": "UnitedHealth Group est le premier assureur santé américain. Le groupe combine l'activité d'assurance (UnitedHealthcare) et les services de santé (Optum : pharmacie, soins primaires, analytics), formant un écosystème intégré unique.",
    "MA": "Mastercard est le n°2 mondial des réseaux de paiement par carte. Mêmes dynamiques que Visa : commissions sur transactions, effet de réseau, pricing power et marges très élevées.",
    "PG": "Procter & Gamble est un géant des produits de consommation courante, propriétaire de marques comme Gillette, Pampers, Ariel, Oral-B, Head & Shoulders, Tide, Olay. Défensif, générateur de cash-flow régulier, dividende en hausse depuis plus de 60 ans (Dividend King).",
    "COST": "Costco est le leader mondial des magasins-entrepôts à adhésion. Modèle basé sur des marges très faibles mais un volume énorme et une fidélité exceptionnelle des membres (taux de renouvellement > 90%).",
    "JNJ": "Johnson & Johnson est un groupe pharmaceutique diversifié (médicaments innovants, dispositifs médicaux). Après la scission de sa branche grand public (Kenvue), JNJ se concentre sur l'oncologie, l'immunologie, la neurologie et les dispositifs médicaux.",
    "HD": "The Home Depot est le leader mondial du bricolage et de l'amélioration de l'habitat. Plus de 2 300 magasins aux États-Unis, Canada et Mexique. Business model défensif (entretien habitat) avec cyclicité sur le segment rénovation.",
    "ORCL": "Oracle est un leader historique des bases de données et des logiciels d'entreprise. Le groupe transforme son modèle vers le cloud (OCI), avec un retour en force grâce aux contrats d'infrastructure IA.",
    "ABBV": "AbbVie est un laboratoire pharmaceutique américain, connu pour Humira (anti-inflammatoire) et ses successeurs Skyrizi et Rinvoq. Portefeuille diversifié en immunologie, oncologie, neurosciences (Allergan).",
    "KO": "The Coca-Cola Company est le leader mondial des boissons non alcoolisées (Coca-Cola, Sprite, Fanta, Minute Maid, Powerade, Costa Coffee). Défensif, dividende croissant depuis plus de 60 ans.",
    "NFLX": "Netflix est le leader mondial du streaming vidéo par abonnement, avec plus de 280 millions d'abonnés. Investit massivement dans les contenus originaux et développe la publicité et les jeux vidéo.",
    "AMD": "Advanced Micro Devices (AMD) conçoit des processeurs (CPU Ryzen/EPYC) et des GPU (Radeon, Instinct MI300). Principal challenger d'Intel dans les CPU serveurs et de Nvidia dans les accélérateurs IA.",
    "CRM": "Salesforce est le leader mondial du CRM cloud. Suite d'applications pour vente, service client, marketing, analytics et IA (Einstein, Agentforce). Propriétaire de Slack, Tableau et MuleSoft.",
    "ADBE": "Adobe est le leader mondial des logiciels créatifs (Photoshop, Illustrator, Premiere Pro) et de l'expérience digitale (Experience Cloud, Marketo). Modèle SaaS à marges élevées et croissance régulière.",
    "CSCO": "Cisco Systems est le leader mondial des équipements réseau pour entreprises (routeurs, switchs) et étend ses activités à la cybersécurité et aux logiciels d'observabilité (Splunk).",
    "INTC": "Intel est le leader historique des CPU x86 pour PC et serveurs, en cours de transformation industrielle (Intel Foundry) pour reconquérir un leadership en fonderie. Défi stratégique majeur face à TSMC, AMD et Nvidia.",
    "IBM": "IBM s'est recentré sur le cloud hybride (acquisition Red Hat) et l'IA d'entreprise (watsonx). Groupe mature qui combine services, logiciels et conseil (consulting).",
    "DIS": "The Walt Disney Company est un géant du divertissement : studios (Disney, Pixar, Marvel, Lucasfilm), parcs à thème, streaming (Disney+, Hulu, ESPN+) et télévision (ABC, ESPN).",
    "MCD": "McDonald's est le leader mondial de la restauration rapide, avec plus de 40 000 restaurants (majoritairement franchisés) dans 100+ pays. Génère des redevances récurrentes et un rendement du capital élevé.",
    "NKE": "Nike est le n°1 mondial des équipements et vêtements de sport, avec les marques Nike, Jordan et Converse. Distribution en partie directe (Nike Direct) et via les détaillants.",
    "SBUX": "Starbucks est le leader mondial des cafés spécialisés avec plus de 39 000 points de vente. Marque puissante, programme de fidélité performant (Rewards).",

    # ---- Tech / Growth ----
    "PLTR": "Palantir Technologies fournit des plateformes de fusion de données et d'analyse pour le gouvernement (Gotham) et les entreprises (Foundry, AIP). Acteur en forte croissance sur le marché de l'IA opérationnelle.",
    "SNOW": "Snowflake propose une plateforme de data cloud (Data Cloud) pour l'entreposage, le partage et l'analyse de données. Architecture séparant stockage et calcul, consommation à l'usage.",
    "DDOG": "Datadog est une plateforme SaaS d'observabilité unifiée (monitoring infrastructure, APM, logs, sécurité). Croissance rapide auprès des entreprises cloud-natives.",
    "NET": "Cloudflare est un leader des réseaux de diffusion de contenu (CDN), de la cybersécurité (DDoS, Zero Trust) et du edge computing (Workers). Mission : bâtir un Internet plus rapide et plus sûr.",
    "CRWD": "CrowdStrike est un leader de la cybersécurité endpoint basé sur l'IA (Falcon Platform). Croissance forte, concurrence intense avec SentinelOne et Microsoft Defender.",
    "SHOP": "Shopify fournit une plateforme e-commerce pour marchands (PME à grandes marques). Infrastructure complète : boutique, paiement, expédition, capital, marketing.",
    "COIN": "Coinbase est la principale plateforme américaine d'échange de cryptomonnaies cotée en bourse. Revenus très corrélés au cycle crypto (trading, staking, custody).",
    "UBER": "Uber Technologies exploite la principale plateforme mondiale de VTC et une activité de livraison de repas (Uber Eats). Expansion dans le fret (Uber Freight) et la publicité.",
    "ABNB": "Airbnb est la plateforme mondiale de location de logements et expériences de courte durée. Marque emblématique, effet de réseau puissant, haute profitabilité.",
    "SPOT": "Spotify est le leader mondial du streaming audio (musique, podcasts, livres audio) avec plus de 600 millions d'utilisateurs. Monétisation mixte : abonnement premium + publicité.",

    # ---- Healthcare / Pharma ----
    "MRK": "Merck & Co est un laboratoire pharmaceutique américain dont le produit phare est Keytruda (immuno-oncologie), parmi les médicaments les plus vendus au monde.",
    "PFE": "Pfizer est l'un des plus grands groupes pharmaceutiques mondiaux. Portefeuille diversifié après le pic Covid (vaccin Comirnaty, Paxlovid), avec un pipeline oncologique renforcé par l'acquisition de Seagen.",
    "TMO": "Thermo Fisher Scientific fournit instruments, réactifs et services aux laboratoires de recherche, hôpitaux et industries pharmaceutiques. Rôle d'infrastructure de la recherche biomédicale mondiale.",
    "ABT": "Abbott Laboratories est un groupe santé diversifié : diagnostics, dispositifs médicaux (cardiovasculaire, diabète avec FreeStyle Libre), nutrition et pharmaceutique générique.",
    "DHR": "Danaher est un conglomérat d'instrumentation scientifique et de diagnostics (Beckman Coulter, Cepheid, Leica). Fortement implanté dans les biosciences et le diagnostic moléculaire.",
    "AMGN": "Amgen est l'un des pionniers de la biotechnologie. Médicaments phares : Prolia, Repatha, Otezla, Tepezza. Investi dans l'obésité avec MariTide.",
    "NVO-OL": "Novo Nordisk est le leader mondial du diabète et de l'obésité, avec ses médicaments GLP-1 (Ozempic, Wegovy). Croissance exceptionnelle portée par la demande anti-obésité.",
    "NOVO-B.CO": "Novo Nordisk est le leader mondial du diabète et de l'obésité avec les GLP-1 Ozempic et Wegovy. Société danoise dont la valorisation a explosé avec la vague anti-obésité.",

    # ---- Financials ----
    "BAC": "Bank of America est l'une des quatre plus grandes banques américaines. Banque universelle : détail, entreprises, investissement (BofA Securities), gestion d'actifs (Merrill).",
    "WFC": "Wells Fargo est une grande banque américaine très implantée dans la banque de détail, les crédits immobiliers et les services aux entreprises. En phase de rationalisation post-scandales.",
    "MS": "Morgan Stanley est une banque d'investissement américaine avec une forte activité de gestion de fortune et d'actifs (E*Trade, Eaton Vance). Modèle plus stable que les purs broker-dealers.",
    "GS": "Goldman Sachs est l'une des principales banques d'investissement mondiales, dominante en conseil M&A et en trading. Efforts de diversification vers la gestion d'actifs et la banque privée.",
    "BLK": "BlackRock est le premier gestionnaire d'actifs mondial (plus de 10 000 milliards $ d'encours). Leader mondial des ETF avec la gamme iShares et de la gestion de risques (Aladdin).",
    "AXP": "American Express est un émetteur de cartes de crédit premium et un réseau de paiement. Modèle haut de gamme avec clientèle fidèle, revenus de commissions élevés.",

    # ---- Industrial / Energy ----
    "CVX": "Chevron est une major pétrolière intégrée américaine, active dans l'exploration-production, le raffinage et la chimie. Dividende solide, discipline capex, investissements dans l'hydrogène et le CCS.",
    "CAT": "Caterpillar est le leader mondial des engins de chantier, miniers et des moteurs diesel/gaz. Baromètre de l'activité d'infrastructure et minière mondiale.",
    "HON": "Honeywell est un conglomérat industriel diversifié (aérospatial, automatisation des bâtiments, technologies de performance, matériaux avancés). Mix d'activités long cycle et court cycle.",
    "GE": "GE Aerospace, issue de la scission de General Electric, est un leader mondial des moteurs d'avion (partenariat Safran via CFM) et de la défense aéronautique.",
    "LMT": "Lockheed Martin est le n°1 mondial de la défense aérospatiale (F-35, missiles, satellites). Visibilité exceptionnelle des carnets de commandes, porté par les budgets défense.",
    "RTX": "RTX Corporation (ex-Raytheon Technologies) est un leader de l'aérospatial et de la défense (Pratt & Whitney, Collins Aerospace, Raytheon). Diversification civile + défense.",
    "BA": "Boeing est l'un des deux duopoleurs mondiaux de l'aviation civile (avec Airbus) et un acteur majeur de la défense et de l'espace. Période difficile post-737 MAX et qualité production.",

    # ---- Consumer ----
    "WMT": "Walmart est le premier distributeur mondial, avec plus de 10 500 magasins et Walmart.com. Leader du discount physique aux États-Unis, en pleine montée en puissance e-commerce et publicité.",
    "PEP": "PepsiCo est un géant des boissons (Pepsi, Gatorade, Tropicana) et du snacking (Frito-Lay, Quaker). Modèle diversifié aliments + boissons, défensif, dividende croissant.",
    "PM": "Philip Morris International est le leader mondial du tabac (hors USA) et des produits à risque réduit (IQOS). Transition accélérée vers les produits sans combustion.",
    "MO": "Altria Group commercialise Marlboro aux États-Unis et investit dans les produits alternatifs (vape, tabac chauffé). Dividende très élevé mais volumes cigarettes en déclin.",

    # ---- Europe France ----
    "MC.PA": "LVMH Moët Hennessy Louis Vuitton est le n°1 mondial du luxe, avec 75 maisons réparties en 5 activités : mode et maroquinerie (Louis Vuitton, Dior), parfums et cosmétiques, vins et spiritueux, horlogerie-joaillerie (Tiffany, Bulgari), distribution sélective (Sephora).",
    "OR.PA": "L'Oréal est le leader mondial des cosmétiques avec 37 marques internationales (L'Oréal Paris, Lancôme, Garnier, Maybelline, Kiehl's, Yves Saint Laurent Beauté, Kérastase). Innovation, e-commerce et beauté de dermatologie moteurs de croissance.",
    "RMS.PA": "Hermès International est une maison de luxe française (sellier d'origine) emblématique de l'exclusivité : maroquinerie (Kelly, Birkin), soie, prêt-à-porter, parfums, horlogerie. Pricing power exceptionnel et patience stratégique.",
    "TTE.PA": "TotalEnergies est une major pétrolière et gazière intégrée française, en diversification vers l'électricité et les renouvelables (solaire, éolien, hydrogène, stockage). Dividende généreux et discipline capex.",
    "SAN.PA": "Sanofi est un laboratoire pharmaceutique français, leader en vaccins (Sanofi Pasteur) et spécialité pharmaceutique (Dupixent en immunologie, portefeuille oncologie). Scission de la branche santé grand public Opella prévue.",
    "AIR.PA": "Airbus est l'un des deux grands constructeurs aéronautiques mondiaux (avec Boeing). Activités civiles (A320neo, A350, A220), défense (Eurofighter) et hélicoptères. Carnet de commandes record (~8 500 avions).",
    "BNP.PA": "BNP Paribas est la première banque de la zone euro par les actifs. Banque universelle : détail France/Europe, banque de financement et d'investissement (CIB), International Financial Services (asset management, assurance).",
    "SU.PA": "Schneider Electric est un leader mondial de la gestion de l'énergie et de l'automatisation des bâtiments et industries. Forte exposition aux thématiques d'électrification et d'efficacité énergétique.",
    "AI.PA": "Air Liquide est un leader mondial des gaz industriels (oxygène, azote, hydrogène) pour l'industrie et la santé. Acteur central de la transition hydrogène.",
    "CS.PA": "AXA est l'un des premiers assureurs mondiaux, actif en IARD, vie-épargne, santé et gestion d'actifs. Modèle diversifié géographiquement et par lignes de métier.",
    "EL.PA": "EssilorLuxottica est le leader mondial des verres ophtalmiques (Essilor) et des montures de lunettes (Ray-Ban, Oakley, Persol, marques sous licence). Partenariat avec Meta sur les lunettes connectées.",
    "KER.PA": "Kering est un groupe de luxe français avec Gucci (maison phare), Saint Laurent, Bottega Veneta, Balenciaga, Alexander McQueen. Acquisition de Creed (parfumerie niche). Phase de réinvention stratégique.",
    "SAF.PA": "Safran est un équipementier aéronautique français. Partenariat 50/50 avec GE Aerospace pour les moteurs CFM (best-seller mondial sur les Airbus A320neo et Boeing 737 MAX).",
    "BN.PA": "Danone est un géant français de l'alimentation : produits laitiers (Actimel, Activia), eaux (Evian, Volvic), nutrition spécialisée (infantile, médicale). En recentrage sur la nutrition premium.",
    "STLAP.PA": "Stellantis est le 4e constructeur automobile mondial, né de la fusion PSA-FCA. Portefeuille de 14 marques : Peugeot, Citroën, Jeep, Ram, Fiat, Chrysler, Alfa Romeo, Maserati, Opel.",

    # ---- Europe Germany ----
    "SAP.DE": "SAP est le leader européen des logiciels d'entreprise (ERP). Transition vers le cloud (SAP S/4HANA Cloud, RISE with SAP) qui porte la croissance et l'amélioration des marges.",
    "SIE.DE": "Siemens est un conglomérat industriel allemand : automatisation (Digital Industries), bâtiments intelligents (Smart Infrastructure), mobilité (trains, signalisation) et santé (Siemens Healthineers).",
    "ALV.DE": "Allianz est l'un des premiers assureurs mondiaux (IARD, vie, santé) et un géant de la gestion d'actifs (PIMCO, Allianz GI). Dividende élevé et solide solvabilité.",
    "MBG.DE": "Mercedes-Benz Group est un constructeur premium allemand avec la marque Mercedes-Benz (voitures et utilitaires). Stratégie de montée en gamme et transition électrique.",
    "BMW.DE": "BMW est un constructeur automobile premium allemand (marques BMW, Mini, Rolls-Royce). Leader de la gamme premium avec une stratégie multi-énergie (électrique, hybride, thermique).",
    "ADS.DE": "Adidas est le n°2 mondial des articles de sport (derrière Nike). Marque emblématique allemande, redressement post-rupture Yeezy.",
    "BAYN.DE": "Bayer est un groupe allemand diversifié : pharmaceutique (Xarelto, Eylea), santé grand public et Crop Science (semences et produits phytosanitaires après Monsanto). Litiges glyphosate pesant sur la valorisation.",
    "BAS.DE": "BASF est le leader mondial de la chimie. Large portefeuille : chimie de base, matériaux, solutions industrielles, nutrition-soins, agriculture. Cyclicité forte.",

    # ---- Europe NL ----
    "ASML.AS": "ASML est le fournisseur mondial quasi-exclusif des machines de lithographie EUV indispensables à la fabrication des semi-conducteurs les plus avancés (TSMC, Samsung, Intel). Monopole technologique majeur, rôle critique dans la chaîne de valeur IA.",
    "PRX.AS": "Prosus détient des participations dans l'internet mondial (notamment Tencent) et dans des plateformes e-commerce, fintech et classifieds dans les marchés émergents.",
    "HEIA.AS": "Heineken est le n°2 mondial de la bière (après AB InBev). Portefeuille premium (Heineken, Amstel, Birra Moretti, Desperados, Lagunitas). Forte exposition émergents.",
    "UNA.AS": "Unilever est un géant néerlandais des produits de grande consommation : beauté et bien-être (Dove, Vaseline), soins personnels, soins ménagers, nutrition, glaces (scission prévue).",
    "ADYEN.AS": "Adyen est une plateforme de paiement néerlandaise fournissant aux grandes marques (Uber, Meta, eBay) une stack unifiée d'acquisition multi-canaux.",

    # ---- Europe UK ----
    "SHEL.L": "Shell est une major pétrolière et gazière anglo-néerlandaise, leader mondial du GNL. Stratégie d'équilibre entre hydrocarbures rentables et transition énergétique progressive.",
    "AZN.L": "AstraZeneca est un laboratoire pharmaceutique anglo-suédois en forte croissance. Leader en oncologie (Tagrisso, Imfinzi, Enhertu), pneumologie et maladies rares (acquisition Alexion).",
    "HSBA.L": "HSBC Holdings est la première banque européenne par les actifs. Très orientée Asie (Hong Kong, Chine, Singapour), elle tire l'essentiel de ses profits de cette région.",
    "ULVR.L": "Unilever (cotation Londres) — géant des produits de grande consommation : Dove, Knorr, Hellmann's, Axe, Magnum, Ben & Jerry's. Focus sur les marques premium à plus forte croissance.",
    "BP.L": "BP est une major pétrolière et gazière britannique. Stratégie de transformation en Integrated Energy Company, avec accent récent sur le retour aux hydrocarbures rentables.",
    "GSK.L": "GSK (GlaxoSmithKline) est un laboratoire pharmaceutique britannique, leader en vaccins (Shingrix, Arexvy) et en maladies infectieuses. Scission réussie de la branche santé grand public (Haleon).",
    "DGE.L": "Diageo est le leader mondial des spiritueux premium : Johnnie Walker, Smirnoff, Baileys, Guinness, Captain Morgan, Tanqueray. Exposition forte aux États-Unis.",

    # ---- Europe Swiss ----
    "NESN.SW": "Nestlé est le leader mondial de l'alimentation et des boissons. Portefeuille vaste : Nescafé, Nespresso, KitKat, Maggi, Purina, nutrition médicale, eaux minérales. Défensif, dividende régulier.",
    "ROG.SW": "Roche est un leader pharmaceutique suisse et n°1 mondial du diagnostic in vitro. Portefeuille oncologique de premier plan (Herceptin, Avastin, Tecentriq, nouvelles molécules en obésité).",
    "NOVN.SW": "Novartis est un laboratoire pharmaceutique suisse. Après la scission de Sandoz (génériques), recentrage sur les médicaments innovants : Entresto (cardiovasculaire), Cosentyx (immunologie), Pluvicto (oncologie radio-ligand).",
    "UBSG.SW": "UBS est la première banque suisse, dominante en gestion de fortune mondiale. Intégration complexe de Credit Suisse en cours (acquisition 2023).",
    "CFR.SW": "Richemont est un groupe de luxe suisse spécialisé dans l'horlogerie-joaillerie : Cartier (maison phare), Van Cleef & Arpels, IWC, Jaeger-LeCoultre, Montblanc.",

    # ---- Autres EU ----
    "SAN.MC": "Banco Santander est la première banque espagnole et l'une des plus diversifiées géographiquement en Europe (Espagne, Brésil, Mexique, Pologne, Royaume-Uni, USA).",
    "ITX.MC": "Industria de Diseño Textil (Inditex) est le leader mondial de la distribution de mode, maison mère de Zara, Pull&Bear, Massimo Dutti, Bershka, Stradivarius, Oysho, Zara Home. Modèle d'intégration verticale et de réassortiment rapide.",
    "ENEL.MI": "Enel est un leader européen de l'électricité, très présent en Italie, Espagne, Amérique Latine. Forte exposition renouvelables.",
    "ENI.MI": "Eni est une major pétrolière et gazière italienne intégrée, active dans l'exploration-production, le raffinage et la transition énergétique (renouvelables, biocarburants).",
    "ABI.BR": "Anheuser-Busch InBev est le n°1 mondial de la bière (Budweiser, Stella Artois, Corona, Leffe, Hoegaarden). Consolidation mondiale, focus sur le désendettement.",
}


def get_description_fr(ticker: str) -> str | None:
    """Retourne la description française d'un ticker, ou None si non disponible."""
    return DESCRIPTIONS_FR.get(ticker)
