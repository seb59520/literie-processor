import json
import os

# Chemin relatif vers le référentiel
REFERENTIEL_PATH = os.path.join(os.path.dirname(__file__), "Référentiels", "mousse_rainuree7zones_tencel_luxe3d_tencel_polyester.json")

MATIERE_MAP = {
    'LUXE 3D': 'LUXE_3D',
    'TENCEL LUXE 3D': 'LUXE_3D',
    'TENCEL': 'TENCEL_S',
    'POLYESTER': 'POLY_S',
}

def get_valeur_mousse_rainuree7zones(largeur, matiere):
    matiere_key = MATIERE_MAP.get(matiere.upper().replace('É','E').replace('È','E').replace('Ê','E'))
    if not matiere_key:
        raise ValueError(f"Matière inconnue : {matiere}")
    with open(REFERENTIEL_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for ligne in data:
        if ligne['MATELAS'] == largeur:
            return ligne[matiere_key]
    raise ValueError(f"Largeur {largeur} non trouvée dans le référentiel") 