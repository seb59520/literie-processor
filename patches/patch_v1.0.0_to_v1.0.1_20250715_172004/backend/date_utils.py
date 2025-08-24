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