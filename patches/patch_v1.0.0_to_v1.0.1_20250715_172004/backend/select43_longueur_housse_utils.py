import json
import os

def get_select43_longueur_housse_value(longueur, matiere_housse):
    """
    Retourne la valeur de longueur housse pour SELECT 43 selon la longueur et la matière housse.
    
    Args:
        longueur (int): Longueur du matelas
        matiere_housse (str): Matière de la housse (LUXE_3D, TENCEL, POLYESTER)
    
    Returns:
        float: Valeur de longueur housse ou None si non trouvé
    """
    try:
        # Chemin vers le fichier JSON
        script_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(script_dir, "Référentiels", "select43_longueur_housse.json")
        
        # Lecture du fichier JSON
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Recherche de la longueur correspondante
        for entry in data:
            if entry["LONGUEUR"] == longueur:
                # Retourne la valeur selon la matière housse
                if matiere_housse == "LUXE_3D" or matiere_housse == "TENCEL LUXE 3D":
                    return entry["LUXE_3D"]
                elif matiere_housse == "TENCEL":
                    return entry["TENCEL"]
                elif matiere_housse == "POLYESTER":
                    return entry["POLYESTER"]
                else:
                    return None
        
        return None
        
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel SELECT 43 longueur housse: {e}")
        return None

def get_select43_longueur_housse_formatted(longueur, matiere_housse):
    """
    Retourne la valeur de longueur housse formatée pour SELECT 43.
    
    Args:
        longueur (int): Longueur du matelas
        matiere_housse (str): Matière de la housse
    
    Returns:
        str: Valeur formatée ou "Non trouvé"
    """
    value = get_select43_longueur_housse_value(longueur, matiere_housse)
    if value is not None:
        return str(value)
    return "Non trouvé" 