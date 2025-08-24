import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).lower()

def mots_operation_trouves(articles):
    """
    Retourne la liste des mots-clés trouvés (LIVRAISON, ENLEVEMENT, EXPEDITION) dans les noms, descriptions ou conditions d'articles.
    """
    mots_cles = ['livraison', 'enlevement', 'expedition']
    trouves = set()
    for article in articles:
        for champ in ['nom', 'description', 'conditions']:
            val = normalize_str(article.get(champ, ''))
            for mot in mots_cles:
                if mot in val:
                    trouves.add(mot.upper())
    return sorted(trouves)

if __name__ == "__main__":
    articles = [
        {"nom": "Livraison à domicile"},
        {"description": "Enlèvement sur place"},
        {"nom": "expédition express"},
        {"nom": "matelas"}
    ]
    print(mots_operation_trouves(articles))  # Doit afficher ['ENLEVEMENT', 'EXPEDITION', 'LIVRAISON'] 