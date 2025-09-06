import unicodedata

def normalize_str(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s or '')
        if unicodedata.category(c) != 'Mn'
    ).lower()

def mots_operation_trouves(articles, texte_complet=""):
    """
    Retourne la liste des mots-clés trouvés (LIVRAISON, ENLEVEMENT, EXPEDITION, FOURGON, TRANSPORTEUR) 
    dans les articles ET dans le texte complet du PDF.
    
    Args:
        articles: Liste des articles à analyser
        texte_complet: Texte complet du PDF pour recherche étendue
    """
    # Mots-clés étendus avec toutes les variantes
    patterns_livraison = [
        'livraison', 'livré', 'livre', 'delivery',
        'livraison par fourgon', 'livraison fourgon', 'fourgon',
        'livraison domicile', 'livraison a domicile'
    ]
    
    patterns_enlevement = [
        'enlevement', 'enlèvement', 'enleve', 'enlève',
        'retrait', 'retire', 'retiré',
        'enlevement par vos soins', 'enlèvement par vos soins',
        'retrait en magasin', 'retrait magasin'
    ]
    
    patterns_expedition = [
        'expedition', 'expédition', 'expedie', 'expédie',
        'transporteur', 'transport', 'transporte',
        'livraison par transporteur', 'transport par'
    ]
    
    trouves = set()
    
    # Recherche dans les articles (comportement existant)
    for article in articles:
        for champ in ['nom', 'description', 'conditions']:
            val = normalize_str(article.get(champ, ''))
            
            # Vérification des patterns
            if any(pattern in val for pattern in patterns_livraison):
                trouves.add('LIVRAISON')
            if any(pattern in val for pattern in patterns_enlevement):
                trouves.add('ENLEVEMENT')
            if any(pattern in val for pattern in patterns_expedition):
                trouves.add('EXPEDITION')
    
    # Recherche dans le texte complet du PDF (NOUVEAU)
    if texte_complet:
        texte_norm = normalize_str(texte_complet)
        
        if any(pattern in texte_norm for pattern in patterns_livraison):
            trouves.add('LIVRAISON')
        if any(pattern in texte_norm for pattern in patterns_enlevement):
            trouves.add('ENLEVEMENT')
        if any(pattern in texte_norm for pattern in patterns_expedition):
            trouves.add('EXPEDITION')
    
    return sorted(trouves)

if __name__ == "__main__":
    # Tests avec articles
    articles = [
        {"nom": "Livraison à domicile"},
        {"description": "Enlèvement sur place"},
        {"nom": "expédition express"},
        {"nom": "matelas"}
    ]
    print("Test articles:", mots_operation_trouves(articles))  
    
    # Tests avec texte complet
    texte_test = """
    COMMANDE CM00009573
    Client: Mr DUPONT
    
    Articles:
    - MATELAS 1 PIÈCE 160x200
    
    LIVRAISON PAR FOURGON DE L'ENTREPRISE
    5% enlèvement par vos soins
    Transport par transporteur agréé
    """
    print("Test texte complet:", mots_operation_trouves([], texte_test))
    print("Test combiné:", mots_operation_trouves(articles, texte_test)) 