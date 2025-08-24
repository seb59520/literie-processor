import json
import os
import math

def get_mousse_visco_value(largeur, matiere_housse):
    """
    Retourne la valeur du référentiel MOUSSE VISCO selon la largeur et la matière housse.
    
    Args:
        largeur (float): Largeur du matelas (peut être décimal)
        matiere_housse (str): Matière de la housse (TENCEL uniquement pour ce référentiel)
    
    Returns:
        int: Valeur du référentiel ou None si non trouvé
    """
    try:
        # Arrondir la largeur à l'entier le plus proche pour la recherche dans le référentiel
        largeur_arrondie = round(largeur)
        
        # Chemin vers le fichier JSON
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"mousse_visco_dimensions_matelas.json")
        
        # Lecture du fichier JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Recherche de la valeur correspondant à la largeur arrondie
        largeur_str = str(largeur_arrondie)
        if "dimensions" in data and "TENCEL" in data["dimensions"]:
            if largeur_str in data["dimensions"]["TENCEL"]:
                return int(data["dimensions"]["TENCEL"][largeur_str])
            else:
                print(f"Largeur {largeur_arrondie} non trouvée dans le référentiel MOUSSE VISCO")
                return None
        else:
            print(f"Structure du référentiel MOUSSE VISCO invalide")
            return None
        
        print(f"Largeur {largeur_arrondie} (arrondie de {largeur}) non trouvée dans le référentiel MOUSSE VISCO")
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