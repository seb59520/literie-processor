import json
import os
from backend.asset_utils import get_referentiel_path
REFERENTIEL_PATH = get_referentiel_path(r"latex_mixte7zones_tencel_luxe3d_tencel_polyester.json")

MATIERE_MAP = {
    'LUXE 3D': 'LUXE_3D',
    'TENCEL LUXE 3D': 'LUXE_3D',
    'TENCEL': 'TENCEL_S',
    'POLYESTER': 'POLY_S',
}

def get_valeur_latex_mixte7zones(largeur, matiere):
    """
    Retourne la valeur du référentiel LATEX MIXTE 7 ZONES pour une largeur et une matière donnée.
    - largeur : int (première valeur de la dimension)
    - matiere : str ('LUXE 3D', 'TENCEL', 'POLYESTER')
    """
    matiere_key = MATIERE_MAP.get(matiere.upper().replace('É','E').replace('È','E').replace('Ê','E'))
    if not matiere_key:
        raise ValueError(f"Matière inconnue : {matiere}")
    with open(REFERENTIEL_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    for ligne in data:
        if ligne['MATELAS'] == largeur:
            return ligne[matiere_key]
    raise ValueError(f"Largeur {largeur} non trouvée dans le référentiel") 