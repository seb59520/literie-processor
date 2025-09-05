import json
import os

def get_mousse_visco_longueur_value(longueur):
    """
    Retourne la valeur de longueur housse pour MOUSSE VISCO selon la longueur détectée.
    Args:
        longueur (float): Longueur du matelas (peut être décimal)
    Returns:
        int: Valeur du référentiel ou None si non trouvé
    """
    try:
        # Arrondir la longueur à l'entier le plus proche pour la recherche dans le référentiel
        longueur_arrondie = round(longueur)
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"mousse_visco_longueur_tencel.json")
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for entry in data:
            if entry["LONGUEUR"] == longueur_arrondie:
                return entry["TENCEL"]
        print(f"Longueur {longueur_arrondie} (arrondie de {longueur}) non trouvée dans le référentiel MOUSSE VISCO LONGUEUR")
        return None
    except FileNotFoundError:
        print(f"Fichier référentiel MOUSSE VISCO LONGUEUR non trouvé: {json_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel MOUSSE VISCO LONGUEUR: {e}")
        return None 