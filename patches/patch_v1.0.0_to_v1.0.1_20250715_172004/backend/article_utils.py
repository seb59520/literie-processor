import unicodedata

def normalize_str(s):
    """Supprime les accents et met en minuscules."""
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).lower()

def contient_dosseret_ou_tete(articles):
    """
    Retourne True si au moins un article a un nom contenant 'dosseret' ou 'tete' (toutes variantes).
    """
    mots_cles = ['dosseret', 'tete']
    for article in articles:
        nom = normalize_str(article.get('nom', ''))
        if any(mot in nom for mot in mots_cles):
            return True
    return False

def contient_fermeture_liaison(articles):
    """
    Retourne True si un article contient 'Fermeture de liaison' (insensible à la casse), sinon False.
    """
    for article in articles:
        desc = article.get('description', '').lower()
        if 'fermeture de liaison' in desc:
            return True
    return False

def contient_surmatelas(articles):
    """
    Retourne True si un article contient 'SURMATELAS' (insensible à la casse), sinon False.
    """
    for article in articles:
        desc = article.get('description', '').lower()
        if 'surmatelas' in desc:
            return True
    return False

if __name__ == "__main__":
    # Test rapide
    articles = [
        {"nom": "Dosseret capitonné"},
        {"nom": "Tête de lit"},
        {"nom": "Matelas"},
        {"nom": "dosséret"},
        {"nom": "têté"},
    ]
    print(contient_dosseret_ou_tete(articles))  # Doit afficher True 