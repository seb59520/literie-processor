#!/usr/bin/env python3
"""
Test d'extraction des dimensions des sommiers
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from dimensions_sommiers import detecter_dimensions_sommier, calculer_dimensions_sommiers

def test_extraction_dimensions_sommier():
    """Test de l'extraction des dimensions des sommiers"""
    print("=== TEST EXTRACTION DIMENSIONS SOMMIERS ===")
    
    # Test avec la description fournie par l'utilisateur
    description_test = "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE EN HÊTRE LAQUÉ NOIR SATINÉ 99/ 199/ 19"
    
    print(f"Description test: {description_test}")
    
    # Extraction des dimensions
    dimensions = detecter_dimensions_sommier(description_test)
    
    if dimensions:
        print(f"✅ Dimensions extraites: {dimensions}")
        
        # Calcul de la dimension sommier formatée
        dimension_sommier = calculer_dimensions_sommiers(dimensions)
        print(f"✅ Dimension sommier calculée: {dimension_sommier}")
        
        # Vérification des valeurs attendues
        largeur_attendue = 99.0
        longueur_attendue = 199.0
        hauteur_attendue = 19.0
        
        if (dimensions['largeur'] == largeur_attendue and 
            dimensions['longueur'] == longueur_attendue and 
            dimensions['hauteur'] == hauteur_attendue):
            print("✅ Valeurs extraites correctes")
        else:
            print("❌ Valeurs extraites incorrectes")
            print(f"Attendu: {largeur_attendue}x{longueur_attendue}x{hauteur_attendue}")
            print(f"Obtenu: {dimensions['largeur']}x{dimensions['longueur']}x{dimensions['hauteur']}")
    else:
        print("❌ Aucune dimension extraite")
    
    print()

def test_cas_variés():
    """Test avec différents cas de figures"""
    print("=== TEST CAS VARIÉS ===")
    
    cas_tests = [
        "SOMMIER À LATTES 79/ 198/ 20",
        "SOMMIER TAPISSIER 90/200/22",
        "SOMMIER BOIS MASSIF 160/200/25",
        "SOMMIER MÉTALLIQUE 79.5/ 209/ 21",
        "SOMMIER À RESSORTS 159/ 199/ 21",
        "SOMMIER PLAT 80/190/18",
        "SOMMIER SANS DIMENSIONS",
        "SOMMIER 99/ 199/ 19 MOTORISÉ"
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        dimensions = detecter_dimensions_sommier(description)
        if dimensions:
            dimension_sommier = calculer_dimensions_sommiers(dimensions)
            print(f"  Dimensions: {dimensions}")
            print(f"  Dimension sommier: {dimension_sommier}")
        else:
            print(f"  ❌ Aucune dimension détectée")

def test_integration_backend():
    """Test d'intégration avec le backend"""
    print("\n=== TEST INTÉGRATION BACKEND ===")
    
    try:
        from backend_interface import BackendInterface
        
        # Simuler des données de sommier
        sommier_articles = [
            {
                "description": "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE EN HÊTRE LAQUÉ NOIR SATINÉ 99/ 199/ 19",
                "quantite": 1
            }
        ]
        
        types_sommiers = [{"index": 1, "type_sommier": "SOMMIER À LATTES"}]
        
        interface = BackendInterface()
        configurations = interface._create_configurations_sommiers(
            types_sommiers, sommier_articles, 1, 2025, "TEST123"
        )
        
        if configurations:
            config = configurations[0]
            print(f"✅ Configuration créée: {config}")
            print(f"  Dimension sommier: {config.get('dimension_sommier', 'Non trouvée')}")
        else:
            print("❌ Aucune configuration créée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")

if __name__ == "__main__":
    test_extraction_dimensions_sommier()
    test_cas_variés()
    test_integration_backend()
    
    print("\n✅ Tests terminés !") 