import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

def detecter_poignees(description):
    """
    Détecte la présence de poignées dans la description d'un matelas.
    Retourne 'OUI' ou 'NON'.
    """
    desc_normalisee = normalize_str(description)
    
    # Recherche du mot-clé poignées (avec ou sans accent)
    if 'POIGNEES' in desc_normalisee or 'POIGNÉES' in desc_normalisee:
        return 'OUI'
    else:
        return 'NON'

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "MATELAS LATEX AVEC POIGNEES",
        "MATELAS MOUSSE AVEC POIGNÉES",
        "MATELAS LATEX SANS POIGNEES",
        "MATELAS CONFORT AVEC poignées",
        "MATELAS LATEX STANDARD"
    ]
    
    for desc in test_descriptions:
        poignees = detecter_poignees(desc)
        print(f"'{desc}' -> Poignées: {poignees}") 