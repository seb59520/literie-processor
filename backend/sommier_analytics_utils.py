import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).upper()

def detecter_sommier_dans_un_lit(description: str) -> str:
    """
    Détecte si le sommier est mentionné comme étant "dans un lit"
    Retourne "OUI" ou "NON"
    """
    desc = normalize_str(description)
    
    # Recherche des expressions "dans un lit" ou "DANS UN LIT"
    if "DANS UN LIT" in desc:
        return "OUI"
    
    return "NON"

def detecter_sommier_pieds(description: str) -> str:
    """
    Détecte si le sommier a des pieds mentionnés
    Retourne "OUI" ou "NON"
    """
    desc = normalize_str(description)
    
    # Recherche du mot "PIEDS" dans la description
    # Mais on exclut les cas négatifs comme "sans pieds", "pas de pieds", etc.
    if "PIEDS" in desc:
        # Vérifier s'il y a des mots négatifs avant ou après "PIEDS"
        negative_words = ["SANS", "PAS", "AUCUN", "AUCUNE", "NI"]
        words = desc.split()
        
        for i, word in enumerate(words):
            if word == "PIEDS":
                # Vérifier le mot précédent
                if i > 0 and words[i-1] in negative_words:
                    continue
                # Vérifier le mot suivant
                if i < len(words)-1 and words[i+1] in negative_words:
                    continue
                # Si on arrive ici, c'est un vrai pieds
                return "OUI"
    
    return "NON"

def analyser_caracteristiques_sommier(description: str) -> dict:
    """
    Analyse complète des caractéristiques d'un sommier
    Retourne un dictionnaire avec toutes les caractéristiques détectées
    """
    return {
        "sommier_dansunlit": detecter_sommier_dans_un_lit(description),
        "sommier_pieds": detecter_sommier_pieds(description)
    }

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "Sommier à lattes dans un lit 160x200",
        "Sommier tapissier avec pieds 180x200",
        "Sommier métallique standard 140x190",
        "Sommier DANS UN LIT avec PIEDS 200x200"
    ]
    
    for desc in test_descriptions:
        result = analyser_caracteristiques_sommier(desc)
        print(f"Description: {desc}")
        print(f"Résultat: {result}")
        print("-" * 50) 