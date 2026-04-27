"""
Univers d'actions US (S&P 500) + Europe (Stoxx 600 sélection).
Liste statique pour performance — mise à jour périodique.
"""

# S&P 500 - sélection représentative et large (Top 500)
SP500 = [
    "AAPL","MSFT","NVDA","GOOGL","GOOG","AMZN","META","TSLA","BRK-B","LLY",
    "AVGO","JPM","V","XOM","UNH","MA","PG","COST","JNJ","HD",
    "ORCL","ABBV","BAC","KO","MRK","CVX","NFLX","AMD","PEP","CRM",
    "TMO","LIN","WMT","ADBE","ACN","MCD","ABT","CSCO","WFC","DHR",
    "IBM","TXN","DIS","GE","PM","QCOM","CAT","VZ","INTU","AXP",
    "NOW","ISRG","AMGN","SPGI","PFE","MS","UNP","GS","NEE","RTX",
    "T","COP","HON","LOW","SYK","BKNG","BLK","SCHW","ETN","C",
    "UBER","PGR","TJX","DE","VRTX","BSX","ELV","MDT","LMT","ADP",
    "BMY","MMC","CB","PLD","ADI","GILD","MDLZ","CI","SBUX","LRCX",
    "AMT","KLAC","NKE","MO","SO","REGN","FI","AMAT","INTC","SHW",
    "EQIX","DUK","ICE","CME","WM","ITW","SNPS","CDNS","AON","MCO",
    "TDG","MU","PH","CL","MSI","PYPL","CVS","FCX","USB","BDX",
    "EOG","MMM","APH","GD","CMG","PNC","EMR","ORLY","ZTS","CSX",
    "MCK","TGT","WELL","FDX","NSC","ECL","ROP","APD","MAR","OXY",
    "AJG","CARR","TT","COF","SLB","NXPI","PSX","HLT","AFL","AZO",
    "PSA","MET","AIG","SRE","DHI","HCA","SPG","PAYX","TRV","FTNT",
    "DXCM","F","O","KMB","BK","MPC","ROST","TEL","ALL","OKE",
    "CTAS","EW","A","WMB","GM","LEN","STZ","CMI","MSCI","VLO",
    "ODFL","IQV","IDXX","BIIB","KMI","HES","CPRT","URI","D","FANG",
    "NEM","PCAR","MNST","GIS","WDAY","DVN","NUE","SMCI","KHC","EXC",
    "KR","KDP","AEP","FIS","FAST","LHX","OTIS","GWW","HPQ","EA",
    "XEL","DD","VRSK","ACGL","HUM","ANSS","GEHC","CTSH","LULU","CNC",
    "MLM","ROK","VMC","HIG","EFX","ON","HAL","IT","DLR","CHTR",
    "BKR","VICI","YUM","IR","KEYS","PPG","RSG","DOW","MCHP","FICO",
    "CCI","GLW","TSCO","SYY","CBRE","WEC","WST","AWK","CAH","PWR",
    "EIX","DAL","PEG","MPWR","WAB","ES","DFS","ZBH","DLTR","STT",
    "LYB","HSY","MTD","VTR","AVB","WTW","ED","FTV","RCL","PRU",
    "TROW","CHD","EQR","ETR","PCG","BAX","STE","APTV","HPE","AEE",
    "DOV","RMD","TDY","ULTA","BRO","MKC","CDW","SWKS","GPN","BALL",
    "ROL","IP","WBD","DG","ENPH","CLX","CTRA","ALGN","LVS","MTB",
    "LUV","NDAQ","TRGP","WY","BR","FTV","HBAN","PKG","NVR","XYL",
    "TSN","NTAP","CF","RF","HOLX","FE","CMS","ZBRA","EBAY","GPC",
    "MOH","CINF","WRK","FOXA","FOX","EXPD","OMC","ATO","HUBB","BG",
    "TER","DPZ","MAS","AES","FSLR","PPL","K","HRL","MRNA","PODD",
    "CAG","PTC","SJM","DRI","TYL","AVY","J","SBAC","PAYC","BBY",
    "PFG","WAT","TXT","EXR","BBWI","SYF","IFF","NRG","CNP","ESS",
    "WRB","BEN","AKAM","CHRW","LH","NDSN","EXPE","INCY","ARE","LKQ",
    "KEY","TRMB","CTLT","JBHT","FMC","APA","STX","DGX","LDOS","LYV",
    "AMCR","EQT","MAA","PNR","SWK","KIM","JKHY","POOL","TECH","EPAM",
    "VTRS","CFG","MRO","IEX","TAP","UDR","BIO","L","MGM","TPR",
    "NI","REG","HST","LNT","EG","CPT","DOC","KMX","GEN","HAS",
    "ALB","NWSA","NWS","CRL","MOS","CZR","FFIV","PNW","TFX","CBOE",
    "HSIC","ALLE","SOLV","GL","EMN","JNPR","SNA","MTCH","CPB","RL",
    "WYNN","MKTX","AOS","ROV","CE","WBA","IVZ","AIZ","VFC","DAY",
    "FRT","AAL","NCLH","BWA","MHK","LW","HII","TNL","PARA","BXP",
    "MMC","HEI","EL","SOLV","ULTA","TFC",
]

# Europe — grandes capitalisations (Stoxx 600 sélection)
# Tickers Yahoo Finance avec suffixe de place (.PA, .L, .AS, .DE, etc.)
EUROPE = [
    # France (.PA)
    "MC.PA","OR.PA","RMS.PA","TTE.PA","SAN.PA","AIR.PA","BNP.PA","SU.PA","AI.PA",
    "CDI.PA","DG.PA","CS.PA","EL.PA","KER.PA","SAF.PA","BN.PA","ML.PA","ACA.PA",
    "CAP.PA","STM.PA","GLE.PA","VIE.PA","ORA.PA","PUB.PA","STLAP.PA","CA.PA",
    "RI.PA","ATO.PA","LR.PA","VIV.PA","HO.PA","URW.PA","EN.PA","ENGI.PA","WLN.PA",
    "ERF.PA","FR.PA","EDEN.PA","SCR.PA","BVI.PA","ALO.PA","BIM.PA","RNO.PA",
    # Allemagne (.DE)
    "SAP.DE","SIE.DE","ALV.DE","DTE.DE","MUV2.DE","MBG.DE","BMW.DE","ADS.DE",
    "BAS.DE","BAYN.DE","DBK.DE","DB1.DE","IFX.DE","VOW3.DE","MRK.DE","EOAN.DE",
    "RWE.DE","HEN3.DE","BEI.DE","LIN.DE","CON.DE","1COV.DE","FRE.DE","HEI.DE",
    "PAH3.DE","SY1.DE","QIA.DE","ENR.DE","MTX.DE","AIR.DE","ZAL.DE","SHL.DE",
    "BNR.DE","RHM.DE","P911.DE","HFG.DE","DHL.DE","CBK.DE","DWNI.DE",
    # Pays-Bas (.AS)
    "ASML.AS","PRX.AS","HEIA.AS","INGA.AS","PHIA.AS","AD.AS","ADYEN.AS","UNA.AS",
    "RAND.AS","WKL.AS","ASM.AS","REN.AS","KPN.AS","DSFIR.AS","AKZA.AS","ABN.AS",
    "MT.AS","NN.AS","AGN.AS","BESI.AS",
    # Royaume-Uni (.L)
    "SHEL.L","AZN.L","HSBA.L","ULVR.L","BP.L","GSK.L","RIO.L","DGE.L","GLEN.L",
    "BATS.L","REL.L","LSEG.L","VOD.L","PRU.L","NG.L","BARC.L","LLOY.L","TSCO.L",
    "NWG.L","AAL.L","STAN.L","CPG.L","IMB.L","BT-A.L","EXPN.L","SGE.L","WTB.L",
    "ABF.L","FLTR.L","CRDA.L","INF.L","SMIN.L","LGEN.L","AV.L","III.L","MNDI.L",
    "ANTO.L","BNZL.L","FERG.L","PSON.L","ITRK.L","WPP.L","HLMA.L","SGRO.L",
    # Suisse (.SW)
    "NESN.SW","ROG.SW","NOVN.SW","UBSG.SW","ZURN.SW","ABBN.SW","CFR.SW","SIKA.SW",
    "GIVN.SW","LONN.SW","GEBN.SW","ALC.SW","HOLN.SW","PGHN.SW","SREN.SW","KNIN.SW",
    "SLHN.SW","LOGN.SW","SCMN.SW","STMN.SW",
    # Espagne (.MC)
    "IBE.MC","ITX.MC","SAN.MC","BBVA.MC","TEF.MC","FER.MC","CLNX.MC","REP.MC",
    "AENA.MC","AMS.MC","ELE.MC","IAG.MC","CABK.MC","MAP.MC","ACS.MC","NTGY.MC",
    "RED.MC","GRF.MC",
    # Italie (.MI)
    "ENEL.MI","ENI.MI","ISP.MI","STLAM.MI","UCG.MI","RACE.MI","G.MI","MB.MI",
    "MONC.MI","TIT.MI","FBK.MI","PST.MI","PRY.MI","SPM.MI","LDO.MI","TEN.MI",
    # Belgique / Luxembourg
    "ABI.BR","KBC.BR","UCB.BR","SOLB.BR","GBLB.BR","ACKB.BR","UMI.BR","AGS.BR",
    # Danemark / Suède / Norvège / Finlande
    "NOVO-B.CO","MAERSK-B.CO","DSV.CO","ORSTED.CO","CARL-B.CO","GN.CO","DANSKE.CO",
    "ATCO-A.ST","INVE-B.ST","VOLV-B.ST","HM-B.ST","ERIC-B.ST","SEB-A.ST","SAND.ST",
    "ASSA-B.ST","SKF-B.ST","SWED-A.ST","EQNR.OL","DNB.OL","TEL.OL","YAR.OL",
    "NOKIA.HE","SAMPO.HE","UPM.HE","FORTUM.HE","NESTE.HE","KNEBV.HE",
]

# Mid / Small caps US additionnelles et actions populaires hors S&P 500
EXTRA_US = [
    # Growth / Tech mid-caps
    "PLTR","SNOW","DDOG","NET","CRWD","ZS","OKTA","MDB","TEAM","HUBS","DOCU","ZM",
    "TWLO","S","U","PATH","AI","BILL","ESTC","CFLT","GTLB","FROG","APP","RBLX",
    "COIN","HOOD","SOFI","AFRM","UPST","LCID","RIVN","NIO","XPEV","LI","BYD","PTON",
    "SHOP","SQ","ROKU","SPOT","PINS","SNAP","LYFT","DASH","ABNB","DKNG","ETSY","W",
    "TDOC","VEEV","WIX","DBX","CHWY","FVRR","UPWK","Z","OPEN","HOMB",
    # Biotech / pharma mid-caps
    "NVAX","BNTX","CRSP","BEAM","NTLA","EDIT","TWST","VRTX","BIIB","MRNA","SRPT","ALNY","EXAS",
    # Semi / hardware
    "ARM","WOLF","QRVO","SWKS","MCHP","ASML","TSM","STX","WDC","HPQ","DELL","IONQ","RGTI",
    # Finance / FinTech
    "MKL","LPLA","IBKR","RJF","EVR","SF","CG","KKR","APO","ARES","BX","CBOE","NDAQ",
    # Consumer / retail
    "LULU","UAA","UA","RL","TPR","CPRI","PVH","VFC","GRMN","HAS","MAT","HSY","K","SJM","CPB",
    "CLX","KMB","EL","COTY","NWL","WHR","LEG","TPX","SWBI","RGR","YETI",
    # Industrial / energy
    "PLUG","FCEL","BLDP","BE","CLNE","ENPH","SEDG","NOVA","RUN","FSLR","JKS","CSIQ","SPWR",
    "DVN","FANG","APA","MRO","HES","OXY","CHK","AR","RRC","SM","CRC","VAL",
    # REITs / Real estate
    "VNQ","MAA","AVB","EQR","UDR","CPT","ESS","AIV","BXP","SLG","VNO","DRE","EXR","CUBE","PSA",
    # Healthcare additional
    "CVS","WBA","RAD","DVA","HCA","UHS","THC","MOH","CNC","ANTM","CI",
    # ETFs populaires (pour comparaison)
    "SPY","QQQ","DIA","IWM","VOO","VTI","VTV","VUG","ARKK","XLK","XLF","XLE","XLV","XLY","XLP",
    "GLD","SLV","TLT","HYG","LQD","USO","UNG","UUP","FXE",
]

# Actions additionnelles US (2025-2026 trending + actions populaires retail)
EXTRA_US_2 = [
    # IA / Data / Cloud émergents
    "SMCI","CRDO","ANET","ALAB","NBIS","IOT","VST","TLN","OKLO","SMR","GEV","ETR","CEG",
    # Semi-conducteurs complémentaires
    "AMAT","LRCX","KLAC","MRVL","ON","TER","MPWR","COHR","IPGP","ACLS",
    # Cybersécurité
    "PANW","FTNT","ZS","CRWD","S","RBRK","VRNS","TENB","CYBR","QLYS","CHKP",
    # Software growth
    "NOW","WDAY","TEAM","HUBS","DDOG","ZS","OKTA","MDB","MNDY","BILL","CRWD","NET","ESTC","CFLT","GTLB","ASAN","SMAR",
    # Biotech / pharma ciblés
    "REGN","VRTX","NVAX","BNTX","CRSP","BEAM","NTLA","EDIT","MRNA","ALNY","IONS","SRPT","RARE","BMRN","EXAS","NTRA","TMDX","DXCM","PODD",
    # Consommation digitale
    "SHOP","MELI","PDD","BABA","JD","SE","GRAB","BIDU","NTES","TCOM","KWEB",
    # Fintech / crypto
    "COIN","HOOD","SOFI","AFRM","UPST","NU","PAGS","STNE","MQ","MARA","RIOT","CLSK","BITF","WULF","IREN","HUT","BTBT",
    # EV / mobilité
    "TSLA","RIVN","LCID","NIO","XPEV","LI","BYDDY","VFS","LAZR","INVZ","CHPT","EVGO","BLNK",
    # Industrie défense / aéro
    "LMT","GD","NOC","HII","BA","RTX","TDG","LHX","CW","KTOS","AVAV","PLL","HEI","AXON",
    # Consumer resilient
    "NFLX","DIS","ROKU","TTD","APP","PINS","SNAP","RDDT","META","ZM","DASH","LYFT","PINS","MTCH","BMBL",
    # Énergie classique + uranium + hydrogène
    "XOM","CVX","COP","EOG","FANG","OXY","SLB","BKR","HAL","UEC","CCJ","LEU","URA","NXE","DNN","BWXT","PLUG","BLDP","BE","FCEL",
    # Or et matériaux stratégiques
    "NEM","GOLD","AEM","KGC","AU","FNV","WPM","PAAS","HL","SCCO","FCX","TECK","MP","LAC","ALB",
    # Retail & discount
    "WMT","COST","TGT","TJX","DG","DLTR","BJ","FIVE","BURL","ROST","OLLI","ACI",
    # Food / beverage / staples
    "KO","PEP","MNST","KDP","STZ","BUD","TAP","CELH","HAIN","FRPT","CPB","SJM","CAG",
    # Luxe / premium
    "RL","TPR","CPRI","PVH","LVMUY","BRBY.L","CFR.SW","RMS.PA","MC.PA",
    # Actions meme / spéculatives
    "GME","AMC","BBBY","BB","NOK","MARA","RIOT","PLTR","SOFI","HOOD","DJT",
    # SaaS enterprise divers
    "CRM","ADBE","INTU","ADSK","ANSS","CDNS","SNPS","FTNT","PANW","WDAY","NOW","VEEV","DOCU","ZM","HUBS",
    # Travel / leisure
    "BKNG","EXPE","ABNB","MAR","HLT","RCL","CCL","NCLH","LYV","MSGE","MSGS","VIAC","PARA",
    # REITs diversifiés
    "PLD","AMT","EQIX","DLR","O","VICI","WELL","PSA","EXR","SPG","AVB","EQR","ESS","MAA","REXR","CPT","WPC","STAG","IRM","HST","WY","IRT",
]

# Small caps / mid caps Europe additionnelles
EXTRA_EUROPE_2 = [
    # France supplémentaires
    "SGO.PA","VIE.PA","SW.PA","ENGI.PA","EDF.PA","EN.PA","VIV.PA","TFI.PA","ICAD.PA",
    "COV.PA","SCR.PA","ATO.PA","DBV.PA","NANO.PA","MAU.PA","SOI.PA","ALO.PA","COFA.PA",
    "RUI.PA","ALD.PA","EUCAR.PA","CGG.PA","GFC.PA","BB.PA","ADP.PA","RXL.PA","KORIAN.PA",
    # Germany additionnelles
    "PUM.DE","BOSS.DE","HUGO.DE","NEM.DE","AIXA.DE","UTDI.DE","EVT.DE","JEN.DE","RKET.DE","HAB.DE","EVD.DE",
    "DUE.DE","GLJ.DE","KGX.DE","NDX1.DE","SHA.DE","HLAG.DE","RAA.DE","EVK.DE",
    # UK supplémentaires
    "AAF.L","AHT.L","AV.L","BA.L","BRBY.L","BT-A.L","CCL.L","CNA.L","DCC.L","ENT.L",
    "EZJ.L","GSK.L","HLMA.L","IHG.L","JMAT.L","LGEN.L","LSEG.L","MNG.L","MRO.L","PHNX.L",
    "POLY.L","SPX.L","ST.L","SVT.L","TATE.L","VOD.L","WEIR.L",
    # Scandinavia / Nordics
    "ASSB.ST","BILL-A.ST","ELUX-B.ST","GETI-B.ST","HEXA-B.ST","HOLM-B.ST","NDA-SE.ST","NIBE-B.ST",
    "SAND.ST","SEB-A.ST","SINCH.ST","SKA-B.ST","SWMA.ST","TELE2-B.ST","TREL-B.ST",
    "ORSTED.CO","CHR.CO","DEMANT.CO","ISS.CO","LUN.CO","RBREW.CO","SIM.CO","TRYG.CO",
    "AKER.OL","ADEA.OL","NHY.OL","ORK.OL","SCATC.OL","STB.OL","TOM.OL","SUBC.OL",
    "STERV.HE","METSO.HE","KONE-B.HE","OUT1V.HE","TIETO.HE","WRT1V.HE","NOKIA.HE",
    # Italy / Spain / Portugal
    "CPR.MI","DIA.MI","AMP.MI","PIRC.MI","MS.MI","BPE.MI","SRG.MI","A2A.MI","PST.MI","UNI.MI",
    "BBVA.MC","CLNX.MC","AENA.MC","ACS.MC","ELE.MC","ENG.MC","GRF.MC","MEL.MC","MAP.MC","MTS.MC",
    "EDP.LS","GALP.LS","JMT.LS","NOS.LS","SON.LS",
    # Netherlands / Belgium
    "ADYEN.AS","ASM.AS","BESI.AS","DSM.AS","IMCD.AS","NN.AS","UMG.AS","WKL.AS","AD.AS","BASM.AS","AKZA.AS",
    "AED.BR","ARGX.BR","COFB.BR","ELI.BR","FAGR.BR","GBLB.BR","KBC.BR","MELE.BR","PROX.BR","SOLB.BR","UCB.BR","UMI.BR",
]

# Europe additionnelle : mid-caps
EXTRA_EUROPE = [
    # France
    "EDF.PA","DPAM.PA","PUB.PA","ALD.PA","RXL.PA","EDEN.PA","AMUN.PA","ICAD.PA",
    "URW.PA","NK.PA","NXI.PA","GTT.PA","CGG.PA","TFI.PA","M6.PA","EN.PA",
    # Germany
    "HEI.DE","MTX.DE","SY1.DE","EVK.DE","FME.DE","LEG.DE","HNR1.DE","LHA.DE","TKA.DE","BNR.DE",
    "SZU.DE","AFX.DE","SRT.DE","NEM.DE","VNA.DE","TUI1.DE","GYC.DE","WCH.DE","SDF.DE","G1A.DE",
    # UK
    "RR.L","TW.L","BKG.L","PSN.L","BDEV.L","LAND.L","BLND.L","SSE.L","SVT.L","UU.L",
    "ADM.L","HSX.L","JD.L","MKS.L","NXT.L","PRU.L","SBRY.L","RMV.L","OCDO.L","DPLM.L",
    # Netherlands / Nordics
    "KPN.AS","WKL.AS","BESI.AS","DSFIR.AS","AALB.AS","IMCD.AS","BAMNB.AS",
    "NOVO-B.CO","NZYM-B.CO","COLO-B.CO","DSV.CO","VWS.CO","GMAB.CO","ROCK-B.CO","PNDORA.CO",
    "BOL.ST","ESSITY-B.ST","EVO.ST","HEXA-B.ST","ALFA.ST","EPI-B.ST","LATO-B.ST","KINV-B.ST","TELIA.ST",
]

# Indices de marché pour l'en-tête
INDICES = {
    "S&P 500": "^GSPC",
    "Nasdaq 100": "^NDX",
    "Dow Jones": "^DJI",
    "Euro Stoxx 50": "^STOXX50E",
    "VIX": "^VIX",
}

# Mapping pays par suffixe
SUFFIX_COUNTRY = {
    ".PA": "FR", ".DE": "DE", ".AS": "NL", ".L": "UK", ".SW": "CH",
    ".MC": "ES", ".MI": "IT", ".BR": "BE", ".CO": "DK", ".ST": "SE",
    ".OL": "NO", ".HE": "FI", ".LS": "PT", ".VI": "AT", ".IR": "IE",
}


def get_universe() -> list[str]:
    """Retourne l'univers complet déduplicaté."""
    seen = set()
    out = []
    for t in SP500 + EUROPE + EXTRA_US + EXTRA_EUROPE + EXTRA_US_2 + EXTRA_EUROPE_2:
        if t not in seen:
            seen.add(t)
            out.append(t)
    return out


def country_from_ticker(ticker: str) -> str:
    """Déduit le pays à partir du suffixe du ticker."""
    for suf, country in SUFFIX_COUNTRY.items():
        if ticker.endswith(suf):
            return country
    return "US"
