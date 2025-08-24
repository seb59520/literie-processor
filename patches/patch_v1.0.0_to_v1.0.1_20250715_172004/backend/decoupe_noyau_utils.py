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
        "MEDIUM":    {"largeur": 0,  "longueur": 1},
    }
}

NOYAU_EQUIV = {
    "LATEX MIXTE 7 ZONES": "LATEX 7 ZONES",
    "LATEX 7 ZONES": "LATEX 7 ZONES",
    "LATEX NATUREL": "LATEX NATUREL",
    "RAINURÉ": "RAINURÉ",
    "RAINURE": "RAINURÉ",
    "LATEX 3 Z CENTRE RENFORCÉ": "LATEX 3 Z CENTRE RENFORCÉ",
    "SELECT 43": "SELECT 43",
    "VISCO": "VISCO"
}

def calcul_decoupe_noyau(noyau, fermete, largeur, longueur):
    """
    Applique la règle de découpe noyau selon le type de noyau et la fermeté.
    Retourne (largeur_corrigée, longueur_corrigée) arrondies à l'entier le plus proche.
    """
    noyau = (noyau or "").upper().strip()
    fermete = (fermete or "").upper().strip()
    noyau_canon = NOYAU_EQUIV.get(noyau, noyau)
    rules = DECOUPE_NOYAU_RULES.get(noyau_canon)
    if not rules:
        return largeur, longueur  # Pas de règle, pas de correction
    corrections = rules.get(fermete)
    if not corrections:
        return largeur, longueur
    largeur_corr = largeur + corrections["largeur"]
    longueur_corr = longueur + corrections["longueur"]
    return int(round(largeur_corr)), int(round(longueur_corr)) 