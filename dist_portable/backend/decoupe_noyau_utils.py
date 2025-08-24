# backend/decoupe_noyau_utils.py

DECOUPE_NOYAU_RULES = {
    "LATEX NATUREL": {
        "MEDIUM":    {"largeur": 1,  "longueur": 2},
        "FERME":     {"largeur": 0,  "longueur": 1},
    },
    "LATEX 7 ZONES": {
        "MEDIUM":    {"largeur": 0,  "longueur": 2},
        "FERME":     {"largeur": 0,  "longueur": 1},
    },
    "RAINURÉ": {
        "CONFORT":   {"largeur": 0,  "longueur": 2},
        "MEDIUM":    {"largeur": 0,  "longueur": 1},
        "MÉDIUM":    {"largeur": 0,  "longueur": 1},
        "FERME":     {"largeur": -1, "longueur": -0.5},
    },
    "LATEX 3 Z CENTRE RENFORCÉ": {
        "MEDIUM":    {"largeur": 0,  "longueur": 2},
        "FERME":     {"largeur": 0,  "longueur": 1},
    },
    "SELECT 43": {
        "MEDIUM":    {"largeur": 0,  "longueur": 2},
        "FERME":     {"largeur": 0,  "longueur": 1},
    },
    "VISCO": {
        "CONFORT":   {"largeur": 0,  "longueur": 2},
        "MEDIUM":    {"largeur": 0,  "longueur": 2},
    }
}

NOYAU_EQUIV = {
    "LATEX MIXTE 7 ZONES": "LATEX 7 ZONES",
    "LATEX 7 ZONES": "LATEX 7 ZONES",
    "LATEX NATUREL": "LATEX NATUREL",
    "RAINURÉ": "RAINURÉ",
    "RAINURE": "RAINURÉ",
    "RAINUREE": "RAINURÉ",
    "MOUSSE RAINURÉE 7 ZONES": "RAINURÉ",
    "MOUSSE RAINUREE 7 ZONES": "RAINURÉ",  # <-- ajout sans accent
    "LATEX 3 Z CENTRE RENFORCÉ": "LATEX 3 Z CENTRE RENFORCÉ",
    "SELECT 43": "SELECT 43",
    "VISCO": "VISCO",
    "MOUSSE VISCO": "VISCO",
    "MÉMOIRE DE FORME HYBRIDE MOUSSE VISCOÉLASTIQUE": "VISCO"
}

def calcul_decoupe_noyau(noyau, fermete, largeur, longueur):
    """
    Applique la règle de découpe noyau selon le type de noyau et la fermeté.
    Retourne (largeur_corrigée, longueur_corrigée) arrondies à l'entier le plus proche.
    """
    noyau = (noyau or "").upper().strip()
    fermete = (fermete or "").upper().strip()
    noyau_canon = NOYAU_EQUIV.get(noyau, noyau)
    
    # Debug logs
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"DEBUG DECOUPE: noyau='{noyau}' -> noyau_canon='{noyau_canon}'")
    logger.info(f"DEBUG DECOUPE: fermete='{fermete}'")
    
    rules = DECOUPE_NOYAU_RULES.get(noyau_canon)
    if not rules:
        logger.warning(f"DEBUG DECOUPE: Pas de règles trouvées pour noyau_canon='{noyau_canon}'")
        return largeur, longueur  # Pas de règle, pas de correction
    
    logger.info(f"DEBUG DECOUPE: Règles trouvées: {list(rules.keys())}")
    corrections = rules.get(fermete)
    if not corrections:
        logger.warning(f"DEBUG DECOUPE: Pas de correction trouvée pour fermeté='{fermete}' dans les règles: {list(rules.keys())}")
        return largeur, longueur
    
    logger.info(f"DEBUG DECOUPE: Correction appliquée: {corrections}")
    largeur_corr = largeur + corrections["largeur"]
    longueur_corr = longueur + corrections["longueur"]
    
    # Forcer l'utilisation du point décimal en convertissant en string avec format anglais
    largeur_finale = int(round(largeur_corr)) if largeur_corr.is_integer() else float(largeur_corr)
    longueur_finale = int(round(longueur_corr)) if longueur_corr.is_integer() else float(longueur_corr)
    
    return largeur_finale, longueur_finale 