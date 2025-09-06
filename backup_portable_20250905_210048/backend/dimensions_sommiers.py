import math
import re
from typing import Dict, Optional

def detecter_dimensions_sommier(description: str) -> Optional[Dict[str, float]]:
    """
    Détecte les dimensions dans la description d'un sommier.
    Format attendu: largeur/ longueur/ hauteur ou largeur/ longueur
    Retourne un dictionnaire avec les dimensions ou None si non trouvé.
    """
    # Pattern pour détecter les dimensions: nombre (avec décimales)/ nombre (avec décimales)/ nombre (avec décimales) ou nombre (avec décimales)/ nombre (avec décimales)
    # Gère les espaces autour des /
    pattern = r'(\d+(?:[.,]\d+)?)\s*/\s*(\d+(?:[.,]\d+)?)(?:\s*/\s*(\d+(?:[.,]\d+)?))?'
    
    match = re.search(pattern, description)
    if match:
        # Conversion en float puis en int pour gérer les décimales
        largeur = float(match.group(1).replace(',', '.'))
        longueur = float(match.group(2).replace(',', '.'))
        hauteur = float(match.group(3).replace(',', '.')) if match.group(3) else None
        
        return {
            "largeur": largeur,
            "longueur": longueur,
            "hauteur": hauteur
        }
    else:
        return None

def calculer_dimensions_sommiers(dimensions: Dict[str, float]) -> Optional[str]:
    """
    Calcule les dimensions des sommiers selon les spécifications :
    - largeur (arrondi à la dizaine supérieure) * 10
    - longueur (arrondi à la dizaine supérieure) * 10  
    - hauteur (multiplié par 10)
    
    Args:
        dimensions: Dictionnaire contenant 'largeur', 'longueur', 'hauteur'
        
    Returns:
        String au format "largeur_calculee x longueur_calculee x hauteur_calculee"
        ou None si les dimensions sont invalides
    """
    if not dimensions:
        return None
    
    largeur = dimensions.get('largeur')
    longueur = dimensions.get('longueur')
    hauteur = dimensions.get('hauteur')
    
    # Vérification que toutes les dimensions sont présentes
    if largeur is None or longueur is None or hauteur is None:
        return None
    
    # Calcul selon les spécifications
    # Largeur : arrondi à la dizaine supérieure * 10
    largeur_arrondie = math.ceil(largeur / 10.0) * 10
    largeur_calculee = largeur_arrondie * 10
    
    # Longueur : arrondi à la dizaine supérieure * 10
    longueur_arrondie = math.ceil(longueur / 10.0) * 10
    longueur_calculee = longueur_arrondie * 10
    
    # Hauteur : multiplié par 10
    hauteur_calculee = hauteur * 10
    
    return f"{int(largeur_calculee)} x {int(longueur_calculee)} x {int(hauteur_calculee)}"

def calculer_dimensions_sommiers_detaillees(dimensions: Dict[str, float]) -> Optional[Dict[str, int]]:
    """
    Calcule les dimensions des sommiers et retourne un dictionnaire détaillé
    
    Args:
        dimensions: Dictionnaire contenant 'largeur', 'longueur', 'hauteur'
        
    Returns:
        Dictionnaire avec les dimensions calculées ou None si invalide
    """
    if not dimensions:
        return None
    
    largeur = dimensions.get('largeur')
    longueur = dimensions.get('longueur')
    hauteur = dimensions.get('hauteur')
    
    # Vérification que toutes les dimensions sont présentes
    if largeur is None or longueur is None or hauteur is None:
        return None
    
    # Calcul selon les spécifications
    largeur_arrondie = math.ceil(largeur / 10.0) * 10
    largeur_calculee = largeur_arrondie * 10
    
    longueur_arrondie = math.ceil(longueur / 10.0) * 10
    longueur_calculee = longueur_arrondie * 10
    
    hauteur_calculee = hauteur * 10
    
    return {
        "largeur_originale": largeur,
        "longueur_originale": longueur,
        "hauteur_originale": hauteur,
        "largeur_arrondie": largeur_arrondie,
        "longueur_arrondie": longueur_arrondie,
        "largeur_calculee": int(largeur_calculee),
        "longueur_calculee": int(longueur_calculee),
        "hauteur_calculee": int(hauteur_calculee),
        "dimensions_finales": f"{int(largeur_calculee)} x {int(longueur_calculee)} x {int(hauteur_calculee)}"
    }

if __name__ == "__main__":
    # Tests de détection des dimensions
    print("=== TESTS DÉTECTION DIMENSIONS SOMMIERS ===")
    test_descriptions = [
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE EN HÊTRE LAQUÉ NOIR SATINÉ 99/ 199/ 19",
        "SOMMIER À LATTES 79/ 198/ 20",
        "SOMMIER TAPISSIER 90/200/22",
        "SOMMIER BOIS MASSIF 160/200/25",
        "SOMMIER MÉTALLIQUE 79.5/ 209/ 21",
        "SOMMIER À RESSORTS 159/ 199/ 21",
        "SOMMIER PLAT 80/190/18",
        "SOMMIER SANS DIMENSIONS",
        "SOMMIER 99/ 199/ 19 MOTORISÉ"
    ]
    
    for i, desc in enumerate(test_descriptions, 1):
        print(f"\nTest {i}: {desc}")
        dimensions = detecter_dimensions_sommier(desc)
        if dimensions:
            dimension_sommier = calculer_dimensions_sommiers(dimensions)
            print(f"  Dimensions extraites: {dimensions['largeur']}x{dimensions['longueur']}x{dimensions['hauteur']}")
            print(f"  Dimension sommier calculée: {dimension_sommier}")
        else:
            print(f"  ❌ Aucune dimension détectée")
    
    # Tests de calcul des dimensions
    print("\n=== TESTS CALCUL DIMENSIONS SOMMIERS ===")
    test_dimensions = [
        {"largeur": 79, "longueur": 198, "hauteur": 20},
        {"largeur": 90, "longueur": 200, "hauteur": 22},
        {"largeur": 160, "longueur": 200, "hauteur": 25},
        {"largeur": 79.5, "longueur": 209, "hauteur": 21},
        {"largeur": 159, "longueur": 199, "hauteur": 21},
        {"largeur": 80, "longueur": 190, "hauteur": 18}
    ]
    
    for i, dims in enumerate(test_dimensions, 1):
        resultat = calculer_dimensions_sommiers(dims)
        resultat_detaille = calculer_dimensions_sommiers_detaillees(dims)
        
        print(f"\nTest {i}:")
        print(f"  Dimensions originales: {dims['largeur']} x {dims['longueur']} x {dims['hauteur']}")
        print(f"  Résultat simple: {resultat}")
        if resultat_detaille:
            print(f"  Largeur arrondie: {dims['largeur']} -> {resultat_detaille['largeur_arrondie']} -> {resultat_detaille['largeur_calculee']}")
            print(f"  Longueur arrondie: {dims['longueur']} -> {resultat_detaille['longueur_arrondie']} -> {resultat_detaille['longueur_calculee']}")
            print(f"  Hauteur calculée: {dims['hauteur']} -> {resultat_detaille['hauteur_calculee']}")
            print(f"  Dimensions finales: {resultat_detaille['dimensions_finales']}") 