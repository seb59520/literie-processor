import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

def detecter_matiere_housse(description):
    """
    Détecte la matière de la housse d'un matelas dans sa description.
    Retourne 'TENCEL LUXE 3D', 'TENCEL', 'POLYESTER' ou 'INCONNUE'.
    Note: TENCEL LUXE 3D doit être détecté avant TENCEL pour éviter la confusion.
    """
    desc_normalisee = normalize_str(description)
    
    # Recherche des matières de housse (ordre important pour TENCEL LUXE 3D)
    if 'TENCEL LUXE 3D' in desc_normalisee:
        return 'TENCEL LUXE 3D'
    elif 'TENCEL' in desc_normalisee:
        return 'TENCEL'
    elif 'POLYESTER' in desc_normalisee:
        return 'POLYESTER'
    else:
        return 'INCONNUE'

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "MATELAS LATEX HOUSSE TENCEL LUXE 3D LAVABLE",
        "MATELAS MOUSSE HOUSSE MATELASSÉE TENCEL",
        "MATELAS LATEX HOUSSE POLYESTER",
        "MATELAS CONFORT HOUSSE polyester",
        "MATELAS LATEX STANDARD"
    ]
    
    for desc in test_descriptions:
        matiere = detecter_matiere_housse(desc)
        print(f"'{desc}' -> Matière housse: {matiere}") 