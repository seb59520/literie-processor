import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

def detecter_type_housse(description):
    """
    Détecte le type de housse d'un matelas dans sa description.
    Retourne 'MATELASSEE', 'SIMPLE' ou 'INCONNUE'.
    """
    desc_normalisee = normalize_str(description)
    
    # Recherche des mots-clés de housse
    if 'MATELASSEE' in desc_normalisee or 'MATELASSÉE' in desc_normalisee:
        return 'MATELASSEE'
    elif 'SIMPLE' in desc_normalisee or 'EXTENSIBLE' in desc_normalisee:
        return 'SIMPLE'
    else:
        return 'INCONNUE'

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "MATELAS LATEX HOUSSE MATELASSEE",
        "MATELAS MOUSSE HOUSSE MATELASSÉE TENCEL",
        "MATELAS LATEX HOUSSE SIMPLE",
        "MATELAS CONFORT HOUSSE simple",
        "MATELAS LATEX HOUSSE EXTENSIBLE TENCEL",
        "MATELAS LATEX STANDARD"
    ]
    
    for desc in test_descriptions:
        housse = detecter_type_housse(desc)
        print(f"'{desc}' -> Housse: {housse}") 