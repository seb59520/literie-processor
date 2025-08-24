import re

def detecter_dimensions(description):
    """
    Détecte les dimensions dans la description d'un matelas.
    Formats acceptés: 
    - largeur/ longueur/ hauteur ou largeur/ longueur
    - largeurxlongueurxhauteur ou largeurxlongueur
    Retourne un dictionnaire avec les dimensions ou None si non trouvé.
    """
    # Pattern pour détecter les dimensions avec / ou x
    # Gère les espaces autour des séparateurs
    pattern = r'(\d+(?:[.,]\d+)?)\s*[\/xX]\s*(\d+(?:[.,]\d+)?)(?:\s*[\/xX]\s*(\d+(?:[.,]\d+)?))?'
    
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

if __name__ == "__main__":
    # Tests
    test_descriptions = [
        "MATELAS LATEX 79/ 198/ 20",
        "MATELAS MOUSSE 79/ 198",
        "MATELAS LATEX 90/200/22 CONFORTABLE",
        "MATELAS CONFORT 160/200/25 AVEC POIGNEES",
        "MATELAS LATEX STANDARD SANS DIMENSIONS",
        "MATELAS JUMEAUX 79.5/ 209/ 21",  # Test avec décimales
        "MATELAS 159/ 199/ 21",
        # Nouveaux formats avec x
        "MATELAS LATEX 79x198x20",
        "MATELAS MOUSSE 79x198",
        "MATELAS LATEX 90x200x22 CONFORTABLE",
        "MATELAS CONFORT 160x200x25 AVEC POIGNEES",
        "MATELAS 139x189x20",  # Format de votre test
        "MATELAS 139 x 189 x 20"  # Avec espaces
    ]
    
    for desc in test_descriptions:
        dimensions = detecter_dimensions(desc)
        if dimensions:
            print(f"'{desc}' -> Dimensions: {dimensions['largeur']}x{dimensions['longueur']}" + (f"x{dimensions['hauteur']}" if dimensions['hauteur'] else ""))
        else:
            print(f"'{desc}' -> Dimensions: Non trouvées") 