import json
import os

def get_mousse_rainuree7zones_longueur_housse_value(longueur, matiere_housse):
    """
    Retourne la valeur de longueur housse MOUSSE RAINUREE 7 ZONES selon la longueur détectée et la matière housse.
    Args:
        longueur (int): Longueur du matelas
        matiere_housse (str): Matière de la housse (LUXE_3D, TENCEL, POLYESTER)
    Returns:
        float|int|None: Valeur du référentiel ou None si non trouvé
    """
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        from backend.asset_utils import get_referentiel_path
        json_path = get_referentiel_path(r"mousse_rainuree7zones_longueur_housse.json")
        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        for entry in data:
            if entry["LONGUEUR"] == longueur:
                if matiere_housse == "LUXE 3D" or matiere_housse == "TENCEL LUXE 3D":
                    return entry["LUXE_3D"]
                elif matiere_housse == "TENCEL":
                    return entry["TENCEL"]
                elif matiere_housse == "POLYESTER":
                    return entry["POLYESTER"]
                else:
                    print(f"Matière housse non reconnue: {matiere_housse}")
                    return None
        print(f"Longueur {longueur} non trouvée dans le référentiel MOUSSE RAINUREE 7 ZONES LONGUEUR HOUSSE")
        return None
    except FileNotFoundError:
        print(f"Fichier référentiel MOUSSE RAINUREE 7 ZONES LONGUEUR HOUSSE non trouvé: {json_path}")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du référentiel MOUSSE RAINUREE 7 ZONES LONGUEUR HOUSSE: {e}")
        return None 