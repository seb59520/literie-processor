import json
import os
import math

def get_mousse_visco_value(largeur, matiere_housse):
    """
    Retourne la valeur du référentiel MOUSSE VISCO selon la largeur et la matière housse.
    Utilise une interpolation linéaire pour les valeurs décimales.
    
    Args:
        largeur (float): Largeur du matelas (peut être décimal)
        matiere_housse (str): Matière de la housse (TENCEL uniquement pour ce référentiel)
    
    Returns:
        float: Valeur interpolée du référentiel ou None si non trouvé
    """
    try:
        # Chemin vers le fichier JSON
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"mousse_visco_dimensions_matelas.json")
        
        # Lecture du fichier JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        if "dimensions" not in data or "TENCEL" not in data["dimensions"]:
            print(f"Structure du référentiel MOUSSE VISCO invalide")
            return None
        
        tencel_data = data["dimensions"]["TENCEL"]
        
        # Si la largeur est exacte dans le référentiel
        largeur_str = str(int(largeur)) if largeur == int(largeur) else None
        if largeur_str and largeur_str in tencel_data:
            return float(tencel_data[largeur_str])
        
        # Interpolation linéaire
        largeur_inf = int(math.floor(largeur))
        largeur_sup = int(math.ceil(largeur))
        
        # Vérifier que les deux valeurs existent
        if str(largeur_inf) in tencel_data and str(largeur_sup) in tencel_data:
            val_inf = float(tencel_data[str(largeur_inf)])
            val_sup = float(tencel_data[str(largeur_sup)])
            
            # Interpolation linéaire
            if largeur_inf == largeur_sup:
                return val_inf
            else:
                ratio = (largeur - largeur_inf) / (largeur_sup - largeur_inf)
                valeur_interpolee = val_inf + (val_sup - val_inf) * ratio
                return valeur_interpolee
        else:
            print(f"Largeur {largeur} hors limites du référentiel MOUSSE VISCO")
            return None
        
    except FileNotFoundError:
        print(f"Fichier référentiel MOUSSE VISCO non trouvé: {json_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel MOUSSE VISCO: {e}")
        return None

def get_mousse_visco_display_value(largeur, matiere_housse, quantite):
    """
    Retourne la valeur d'affichage pour MOUSSE VISCO avec le préfixe approprié.
    
    Args:
        largeur (float): Largeur du matelas
        matiere_housse (str): Matière de la housse
        quantite (int): Quantité du matelas
    
    Returns:
        str: Valeur formatée pour l'affichage
    """
    value = get_mousse_visco_value(largeur, matiere_housse)
    if value is None:
        return "Non trouvé"
    
    # Logique de préfixe selon la quantité (TENCEL uniquement)
    if quantite == 2:
        return f"4 x {value}"
    elif quantite == 1:
        return f"2 x {value}"
    else:
        return str(value) 