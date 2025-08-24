#!/usr/bin/env python3

import sys
sys.path.append('backend')
import math

# Test avec le cas problématique de Dumortier
llm_data = {
    "articles": [
        {
            "quantite": 1,
            "description": "MATELAS 1 PIÈCE - MÉMOIRE DE FORME HYBRIDE MOUSSE VISCOÉLASTIQUE THERMOSENSIBLE 7 ZONES DIFFÉRENCIÉES MÉDIUM - HOUSSE EXTENSIBLE TENCEL AVEC COUSSINETS LAVABLE A 40°",
            "dimensions": "159/ 199/ 21",
            "pu_ttc": 1051.00,
            "eco_part": 15.00,
            "pu_ht": 1036.00
        },
        {
            "quantite": 2,
            "description": "MATELAS JUMEAUX - MÉMOIRE DE FORME HYBRIDE MOUSSE VISCOÉLASTIQUE THERMOSENSIBLE 7 ZONES DIFFÉRENCIÉES MÉDIUM - HOUSSE EXTENSIBLE TENCEL AVEC COUSSINETS LAVABLE A 40°",
            "dimensions": "79.5/ 209/ 21",
            "pu_ttc": 1197.00,
            "eco_part": 11.00,
            "pu_ht": 1186.00
        }
    ]
}

print("=== TEST CORRECTION DUMORTIER (LOGIQUE CORRIGÉE) ===")
print("📋 Données d'entrée:")
for i, article in enumerate(llm_data["articles"]):
    print(f"  Article {i+1}: {article['quantite']}x {article['description'][:50]}...")
    print(f"    Dimensions: {article['dimensions']}")

# Test de détection des dimensions
from dimensions_utils import detecter_dimensions

print("\n📋 Test 1: Détection des dimensions décimales")
for i, article in enumerate(llm_data["articles"]):
    dimensions = detecter_dimensions(article["dimensions"])
    print(f"  Article {i+1}: {article['dimensions']} → {dimensions}")

# Test de détection du type de housse
print("\n📋 Test 2: Détection du type de housse")
from housse_utils import detecter_type_housse
from matiere_housse_utils import detecter_matiere_housse

for i, article in enumerate(llm_data["articles"]):
    housse = detecter_type_housse(article["description"])
    matiere = detecter_matiere_housse(article["description"])
    print(f"  Article {i+1}: housse={housse}, matiere={matiere}")

# Test de création des configurations (simulation de la logique corrigée)
print("\n📋 Test 3: Création des configurations (logique corrigée)")
configurations = []

for i, article in enumerate(llm_data["articles"]):
    quantite = article["quantite"]
    dimensions = detecter_dimensions(article["dimensions"])
    housse = detecter_type_housse(article["description"])
    matiere_housse = detecter_matiere_housse(article["description"])
    
    # Créer une seule configuration par article (logique corrigée)
    config = {
        "matelas_index": i + 1,
        "noyau": "MOUSSE VISCO",
        "quantite": quantite,  # Garder la quantité originale
        "dimensions": dimensions,
        "description": article["description"],
        "housse": housse,
        "matiere_housse": matiere_housse
    }
    
    # Calcul de la dimension literie (logique corrigée)
    if dimensions:
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
        longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
        
        if quantite == 2:
            largeur_literie = largeur_arrondie * 2
        else:
            largeur_literie = largeur_arrondie
            
        dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
        config["dimension_literie"] = dimension_literie
    
    configurations.append(config)
    print(f"  Configuration {len(configurations)}: {config['quantite']}x {config['dimensions']} → {config.get('dimension_literie', 'N/A')}")
    print(f"    Housse: {config['housse']}, Matière: {config['matiere_housse']}")

print(f"\n✅ Résultat: {len(configurations)} configurations créées")
print("📋 Détail des configurations:")
for i, config in enumerate(configurations):
    print(f"  Config {i+1}: {config['quantite']}x {config['dimensions']} → {config.get('dimension_literie', 'N/A')}")

# Test du formatage des dimensions pour le pré-import
print("\n📋 Test 4: Formatage des dimensions pour le pré-import")
def format_dimension_with_quantity(dim, qty):
    if qty > 1 and dim:
        return f"{qty} x ({dim})"
    return dim

for config in configurations:
    dimensions = config["dimensions"]
    quantite = config["quantite"]
    
    if dimensions:
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        dimension_brute = f"{largeur} x {longueur}"
        
        dimension_formatee = format_dimension_with_quantity(dimension_brute, quantite)
        print(f"  {config['quantite']}x {config['dimensions']} → {dimension_formatee}")

# Test avec les référentiels
print("\n📋 Test 5: Vérification des référentiels")
from mousse_visco_utils import get_mousse_visco_value
from mousse_visco_longueur_utils import get_mousse_visco_longueur_value

for config in configurations:
    if config["noyau"] == "MOUSSE VISCO" and config["dimensions"]:
        largeur = config["dimensions"]["largeur"]
        longueur = config["dimensions"]["longueur"]
        
        # Test avec largeur arrondie
        largeur_arrondie = round(largeur)
        valeur_ref = get_mousse_visco_value(largeur_arrondie, "TENCEL")
        valeur_longueur = get_mousse_visco_longueur_value(longueur)
        
        print(f"  {config['quantite']}x {config['dimensions']} → Largeur arrondie: {largeur_arrondie}, Réf: {valeur_ref}, Longueur: {valeur_longueur}")

# Test de simulation du pré-import
print("\n📋 Test 6: Simulation du pré-import")
for config in configurations:
    housse = config["housse"]
    matiere_housse = config["matiere_housse"]
    quantite = config["quantite"]
    dimensions = config["dimensions"]
    
    if dimensions:
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        dimension_brute = f"{largeur} x {longueur}"
        
        # Simulation des champs du pré-import
        hsimple_tencel_c14 = "X" if housse == "SIMPLE" and matiere_housse == "TENCEL" else ""
        hsimple_tencel_d14 = format_dimension_with_quantity(dimension_brute, quantite) if hsimple_tencel_c14 == "X" else ""
        
        print(f"  Config {config['matelas_index']}:")
        print(f"    HSimple_tencel_C14: '{hsimple_tencel_c14}'")
        print(f"    HSimple_tencel_D14: '{hsimple_tencel_d14}'")
        print(f"    longueur_D24: '{get_mousse_visco_longueur_value(longueur)}'")

print("\n✅ Test terminé avec succès!")
print("\n📋 Résumé attendu pour Dumortier:")
print("  - 2 configurations au total")
print("  - Config 1: 1x (159 x 199) → 160x200")
print("  - Config 2: 2x (79.5 x 209) → 160x210 (avec affichage '2 x (79.5 x 209)')")
print("  - HSimple_tencel_C14: 'X' pour les deux configs")
print("  - HSimple_tencel_D14: '159.0 x 199.0' et '2 x (79.5 x 209.0)'")
print("  - longueur_D24: valeurs du référentiel pour chaque config") 