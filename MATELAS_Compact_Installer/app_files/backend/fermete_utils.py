import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

def detecter_fermete_matelas(description):
    """
    Détecte la fermeté d'un matelas dans sa description.
    Retourne 'FERME', 'MEDIUM', 'CONFORT' ou 'INCONNUE'.
    """
    desc_normalisee = normalize_str(description)
    
    # Recherche des mots-clés de fermeté
    if 'FERME' in desc_normalisee:
        return 'FERME'
    elif 'MEDIUM' in desc_normalisee or 'MÉDIUM' in desc_normalisee:
        return 'MEDIUM'
    elif 'CONFORT' in desc_normalisee:
        return 'CONFORT'
    else:
        return 'INCONNUE'

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "MATELAS LATEX FERME",
        "MATELAS MOUSSE MEDIUM",
        "MATELAS LATEX MÉDIUM CONFORTABLE",
        "MATELAS CONFORT",
        "MATELAS LATEX STANDARD"
    ]
    
    for desc in test_descriptions:
        fermete = detecter_fermete_matelas(desc)
        print(f"'{desc}' -> Fermeté: {fermete}") 