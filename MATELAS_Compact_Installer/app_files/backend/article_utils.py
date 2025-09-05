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
    Retourne True si un article contient 'Fermeture de liaison' ou variantes (insensible à la casse), sinon False.
    """
    mots_cles = [
        'fermeture de liaison',
        'fermeture de liasion',  # Faute de frappe courante
        'fermeture liaison',
        'fermeture liasion',     # Faute de frappe courante
        'fdl'                    # Abréviation
    ]
    
    for article in articles:
        desc = normalize_str(article.get('description', ''))
        if any(mot in desc for mot in mots_cles):
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

def filtrer_articles_matelas(articles):
    """
    Filtre les articles pour exclure les PROTÈGE MATELAS et autres articles non-matelas.
    Retourne une liste d'articles filtrés.
    """
    articles_filtres = []
    
    for article in articles:
        desc = normalize_str(article.get('description', ''))
        nom = normalize_str(article.get('nom', ''))
        
        # Exclure explicitement les PROTÈGE MATELAS (normalisé en minuscules sans accents)
        if ('protege matelas' in desc or 'protege matelas' in nom):
            continue
            
        # Exclure les SURMATELAS
        if ('surmatelas' in desc or 'surmatelas' in nom):
            continue
            
        articles_filtres.append(article)
    
    return articles_filtres

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
    
    # Test du filtrage des PROTÈGE MATELAS
    articles_test = [
        {"description": "MATELAS 140x190"},
        {"description": "PROTÈGE MATELAS IMPERMÉABLE CP30 80/200/30"},
        {"description": "SURMATELAS 160x200"},
        {"nom": "PROTEGE MATELAS 90x190"},
    ]
    print(f"Articles avant filtrage: {len(articles_test)}")
    articles_filtres = filtrer_articles_matelas(articles_test)
    print(f"Articles après filtrage: {len(articles_filtres)}")  # Doit afficher 1 