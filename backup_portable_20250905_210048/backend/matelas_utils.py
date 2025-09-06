import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

TYPES_NOYAU = [
    "LATEX NATUREL",
    "LATEX MIXTE 7 ZONES",
    "MOUSSE RAINUREE 7 ZONES",
    "LATEX RENFORCE",
    "SELECT 43",
    "MOUSSE VISCO"
]

def detecter_noyau_matelas(matelas_articles):
    """
    Pour chaque matelas, retourne le type de noyau détecté (ou INCONNU).
    Exclut complètement les protège-matelas qui ne sont pas des matelas.
    Retourne une liste de dicts {index, noyau}
    """
    result = []
    for idx, article in enumerate(matelas_articles, 1):
        desc = normalize_str(article.get('description', '')) + ' ' + normalize_str(article.get('nom', ''))
        
        # Exclure complètement les protège-matelas et surmatelas (ne pas les ajouter au résultat)
        if ("protege matelas" in desc or "surmatelas" in desc):
            continue
            
        noyau = "INCONNU"
        
        # Détection prioritaire : CENTRE RENFORCÉ (prend le dessus sur tout)
        if ("RENFORCE" in desc or "RENFORCÉ" in desc) and "LATEX" in desc:
            noyau = "LATEX RENFORCE"
        # Détection prioritaire : LATEX NATUREL
        elif (("100% LATEX" in desc or "LATEX 100%" in desc) and "NATUREL" in desc):
            noyau = "LATEX NATUREL"
        # Détection LATEX MIXTE 7 ZONES (sans "NATUREL")
        elif ("LATEX 100% PERFORE 7 ZONES" in desc or "LATEX 100% PERFORÉ 7 ZONES" in desc or
              "100% LATEX PERFORE 7 ZONES" in desc or "100% LATEX PERFORÉ 7 ZONES" in desc):
            noyau = "LATEX MIXTE 7 ZONES"
        # Détection standard
        else:
            for type_noyau in TYPES_NOYAU:
                if type_noyau in desc:
                    noyau = type_noyau
                    break
            
            # Variantes de SELECT 43
            if "SELECT43" in desc:
                noyau = "SELECT 43"
        
        result.append({"index": idx, "noyau": noyau})
    return result

if __name__ == "__main__":
    matelas = [
        {"description": "Matelas 100% latex naturel"},
        {"description": "Matelas mousse visco"},
        {"description": "Matelas latex mixte 7 zones"},
        {"description": "Matelas mousse"}
    ]
    print(detecter_noyau_matelas(matelas)) 