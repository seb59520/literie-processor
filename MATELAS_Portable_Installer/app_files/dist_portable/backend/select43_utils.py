import json
import os

def get_select43_value(largeur, matiere_housse):
    """
    Retourne la valeur du référentiel SELECT 43 selon la largeur et la matière housse.
    
    Args:
        largeur (int): Largeur du matelas
        matiere_housse (str): Matière de la housse (LUXE 3D, TENCEL, POLYESTER)
    
    Returns:
        int: Valeur du référentiel ou None si non trouvé
    """
    try:
        # Chemin vers le fichier JSON
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"select43_tencel_luxe3d_tencel_polyester.json")
        
        # Lecture du fichier JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Recherche de la ligne correspondant à la largeur
        for entry in data:
            if entry["MATELAS"] == largeur:
                # Mapping des matières vers les colonnes du JSON
                if matiere_housse == "LUXE 3D":
                    return entry["LUXE_3D"]
                elif matiere_housse == "TENCEL":
                    return entry["TENCEL_S"]
                elif matiere_housse == "POLYESTER":
                    return entry["POLY_S"]
                else:
                    print(f"Matière housse non reconnue pour SELECT 43: {matiere_housse}")
                    return None
        
        print(f"Largeur {largeur} non trouvée dans le référentiel SELECT 43")
        return None
        
    except FileNotFoundError:
        print(f"Fichier référentiel SELECT 43 non trouvé: {json_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel SELECT 43: {e}")
        return None

def get_select43_display_value(largeur, matiere_housse, quantite):
    """
    Retourne la valeur d'affichage pour SELECT 43 avec le préfixe approprié.
    
    Args:
        largeur (int): Largeur du matelas
        matiere_housse (str): Matière de la housse
        quantite (int): Quantité du matelas
    
    Returns:
        str: Valeur formatée pour l'affichage
    """
    value = get_select43_value(largeur, matiere_housse)
    if value is None:
        return "Non trouvé"
    
    # Logique de préfixe selon la matière et la quantité
    if matiere_housse == "POLYESTER":
        return str(value)
    elif quantite == 2:
        return f"4 x {value}"
    elif quantite == 1:
        return f"2 x {value}"
    else:
        return str(value) 