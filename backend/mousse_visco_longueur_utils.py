import json
import os

def get_mousse_visco_longueur_value(longueur):
    """
    Retourne la valeur de longueur housse pour MOUSSE VISCO selon la longueur détectée.
    Utilise une interpolation linéaire pour les valeurs décimales.
    Args:
        longueur (float): Longueur du matelas (peut être décimal)
    Returns:
        float: Valeur interpolée du référentiel ou None si non trouvé
    """
    try:
        import math
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"mousse_visco_longueur_tencel.json")
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Créer un dictionnaire pour faciliter la recherche
        longueur_dict = {entry["LONGUEUR"]: entry["TENCEL"] for entry in data}
        
        # Si la longueur est exacte
        longueur_int = int(longueur) if longueur == int(longueur) else None
        if longueur_int and longueur_int in longueur_dict:
            return float(longueur_dict[longueur_int])
        
        # Interpolation linéaire
        longueur_inf = int(math.floor(longueur))
        longueur_sup = int(math.ceil(longueur))
        
        # Vérifier que les deux valeurs existent
        if longueur_inf in longueur_dict and longueur_sup in longueur_dict:
            val_inf = float(longueur_dict[longueur_inf])
            val_sup = float(longueur_dict[longueur_sup])
            
            # Interpolation linéaire
            if longueur_inf == longueur_sup:
                return val_inf
            else:
                ratio = (longueur - longueur_inf) / (longueur_sup - longueur_inf)
                valeur_interpolee = val_inf + (val_sup - val_inf) * ratio
                return valeur_interpolee
        else:
            print(f"Longueur {longueur} hors limites du référentiel MOUSSE VISCO LONGUEUR")
            return None
    except FileNotFoundError:
        print(f"Fichier référentiel MOUSSE VISCO LONGUEUR non trouvé: {json_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel MOUSSE VISCO LONGUEUR: {e}")
        return None 