from datetime import datetime, timedelta

def get_week_dates(semaine: int, annee: int):
    """
    Retourne la date du lundi et du vendredi pour une semaine et une année données.
    Utilise la norme ISO 8601 pour la numérotation des semaines.
    - semaine : numéro de semaine (1-53)
    - annee : année (ex : 2025)
    Retourne (lundi, vendredi) au format français (DD-MM-YYYY)
    """
    # Trouver le 4 janvier de l'année (qui est toujours dans la semaine 1 selon ISO 8601)
    jan4 = datetime(annee, 1, 4)
    # Trouver le lundi de la semaine contenant le 4 janvier
    lundi_semaine1 = jan4 - timedelta(days=jan4.weekday())
    # Calculer la date du lundi de la semaine demandée
    lundi = lundi_semaine1 + timedelta(weeks=semaine - 1)
    vendredi = lundi + timedelta(days=4)
    
    # Format français : JJ-MM-AAAA
    lundi_str = lundi.strftime("%d-%m-%Y")
    vendredi_str = vendredi.strftime("%d-%m-%Y")
    
    return lundi_str, vendredi_str

def calculate_production_weeks(semaine_actuelle: int, annee_actuelle: int, 
                             has_matelas: bool, has_sommiers: bool) -> dict:
    """
    Calcule automatiquement les semaines de production en fonction du contenu de la commande.
    
    Règles :
    - Si seulement matelas : production S+1
    - Si seulement sommiers : production S+1  
    - Si matelas + sommiers : matelas S+1, sommiers S+1
    
    Args:
        semaine_actuelle: Semaine actuelle (1-53)
        annee_actuelle: Année actuelle
        has_matelas: True si la commande contient des matelas
        has_sommiers: True si la commande contient des sommiers
        
    Returns:
        Dict avec les semaines de production calculées
    """
    def next_week(semaine: int, annee: int) -> tuple:
        """Calcule la semaine suivante en gérant le passage d'année"""
        if semaine == 53:
            return 1, annee + 1
        else:
            return semaine + 1, annee
    
    # Initialiser les semaines par défaut
    semaine_matelas = semaine_actuelle
    semaine_sommiers = semaine_actuelle
    annee_matelas = annee_actuelle
    annee_sommiers = annee_actuelle
    
    if has_matelas and has_sommiers:
        # Cas : matelas + sommiers
        # Matelas ET sommiers en S+1 (modification demandée)
        semaine_matelas, annee_matelas = next_week(semaine_actuelle, annee_actuelle)
        semaine_sommiers, annee_sommiers = next_week(semaine_actuelle, annee_actuelle)
        
    elif has_matelas or has_sommiers:
        # Cas : seulement matelas OU seulement sommiers
        # Production en S+1
        semaine_matelas, annee_matelas = next_week(semaine_actuelle, annee_actuelle)
        semaine_sommiers, annee_sommiers = next_week(semaine_actuelle, annee_actuelle)
    
    # Calculer les dates pour chaque semaine
    lundi_matelas, vendredi_matelas = get_week_dates(semaine_matelas, annee_matelas)
    lundi_sommiers, vendredi_sommiers = get_week_dates(semaine_sommiers, annee_sommiers)
    
    return {
        'matelas': {
            'semaine': semaine_matelas,
            'annee': annee_matelas,
            'semaine_annee': f"{semaine_matelas}_{annee_matelas}",
            'lundi': lundi_matelas,
            'vendredi': vendredi_matelas
        },
        'sommiers': {
            'semaine': semaine_sommiers,
            'annee': annee_sommiers,
            'semaine_annee': f"{semaine_sommiers}_{annee_sommiers}",
            'lundi': lundi_sommiers,
            'vendredi': vendredi_sommiers
        },
        'recommandation': _generate_recommendation_text(has_matelas, has_sommiers, 
                                                       semaine_matelas, annee_matelas,
                                                       semaine_sommiers, annee_sommiers)
    }

def _generate_recommendation_text(has_matelas: bool, has_sommiers: bool,
                                semaine_matelas: int, annee_matelas: int,
                                semaine_sommiers: int, annee_sommiers: int) -> str:
    """Génère le texte de recommandation pour l'utilisateur"""
    
    if has_matelas and has_sommiers:
        return f"Recommandation : Matelas en S{semaine_matelas} ({annee_matelas}), Sommiers en S{semaine_sommiers} ({annee_sommiers})"
    elif has_matelas:
        return f"Recommandation : Matelas en S{semaine_matelas} ({annee_matelas})"
    elif has_sommiers:
        return f"Recommandation : Sommiers en S{semaine_sommiers} ({annee_sommiers})"
    else:
        return "Aucun article détecté"

if __name__ == "__main__":
    # Test rapide
    semaine = 29
    annee = 2025
    lundi, vendredi = get_week_dates(semaine, annee)
    print(f"Semaine {semaine} de {annee} : lundi = {lundi}, vendredi = {vendredi}")
    
    # Test avec semaine 30 pour vérifier
    semaine = 30
    annee = 2025
    lundi, vendredi = get_week_dates(semaine, annee)
    print(f"Semaine {semaine} de {annee} : lundi = {lundi}, vendredi = {vendredi}")
    
    # Test de la nouvelle fonction
    print("\n=== Tests de calcul automatique des semaines ===")
    
    # Test 1: Seulement matelas
    result = calculate_production_weeks(29, 2025, True, False)
    print(f"Seulement matelas: {result['recommandation']}")
    
    # Test 2: Seulement sommiers
    result = calculate_production_weeks(29, 2025, False, True)
    print(f"Seulement sommiers: {result['recommandation']}")
    
    # Test 3: Matelas + sommiers
    result = calculate_production_weeks(29, 2025, True, True)
    print(f"Matelas + sommiers: {result['recommandation']}")
    
    # Test 4: Passage d'année (semaine 53)
    result = calculate_production_weeks(53, 2024, True, True)
    print(f"Passage d'année: {result['recommandation']}") 