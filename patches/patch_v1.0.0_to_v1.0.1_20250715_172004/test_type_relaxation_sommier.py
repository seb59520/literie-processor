#!/usr/bin/env python3
"""
Test de détection du type relaxation des sommiers
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sommier_utils import detecter_type_relaxation_sommier

def test_detection_type_relaxation():
    """Test de la détection du type relaxation"""
    print("=== TEST DÉTECTION TYPE RELAXATION SOMMIERS ===")
    
    # Test avec la description fournie par l'utilisateur
    description_test = "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE EN HÊTRE LAQUÉ NOIR SATINÉ 99/ 199/ 19"
    
    print(f"Description test: {description_test}")
    
    # Détection du type relaxation
    type_relaxation = detecter_type_relaxation_sommier(description_test)
    print(f"✅ Type relaxation détecté: {type_relaxation}")
    
    # Vérification de la valeur attendue
    if type_relaxation == "RELAXATION":
        print("✅ Valeur correcte détectée")
    else:
        print("❌ Valeur incorrecte détectée")
        print(f"Attendu: RELAXATION")
        print(f"Obtenu: {type_relaxation}")
    
    print()

def test_cas_variés():
    """Test avec différents cas de figures"""
    print("=== TEST CAS VARIÉS ===")
    
    cas_tests = [
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER relaxation motorisée",
        "SOMMIER RELAXATIONS MOTORISÉES",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        "SOMMIER BOIS MASSIF FIXE",
        "SOMMIER MÉTALLIQUE À RESSORTS",
        "SOMMIER PLAT FIXE",
        "SOMMIER RELAXATION 160x200",
        "SOMMIER FIXE 140x190"
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        type_relaxation = detecter_type_relaxation_sommier(description)
        print(f"  Type relaxation: {type_relaxation}")
        
        # Vérification logique
        if "RELAXATION" in description.upper():
            expected = "RELAXATION"
        else:
            expected = "FIXE"
            
        if type_relaxation == expected:
            print(f"  ✅ Correct")
        else:
            print(f"  ❌ Incorrect (attendu: {expected})")

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
            },
            {
                "description": "SOMMIER À LATTES FIXE 160x200",
                "quantite": 1
            }
        ]
        
        types_sommiers = [
            {"index": 1, "type_sommier": "SOMMIER À LATTES"},
            {"index": 2, "type_sommier": "SOMMIER À LATTES"}
        ]
        
        interface = BackendInterface()
        configurations = interface._create_configurations_sommiers(
            types_sommiers, sommier_articles, 1, 2025, "TEST123"
        )
        
        if configurations:
            print(f"✅ Configurations créées: {len(configurations)}")
            for i, config in enumerate(configurations):
                print(f"  Sommier {i+1}:")
                print(f"    Type relaxation: {config.get('type_relaxation_sommier', 'Non trouvé')}")
                print(f"    Type sommier: {config.get('type_sommier', 'Non trouvé')}")
                print(f"    Dimension sommier: {config.get('dimension_sommier', 'Non trouvé')}")
        else:
            print("❌ Aucune configuration créée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")

def test_normalisation():
    """Test de la normalisation des caractères"""
    print("\n=== TEST NORMALISATION ===")
    
    cas_normalisation = [
        "SOMMIER RELAXATION",
        "SOMMIER RÉLAXATION",  # Avec accent
        "SOMMIER relaxation",  # Minuscules
        "SOMMIER Relaxation",  # Mixte
        "SOMMIER RELAXATIONS",  # Pluriel
    ]
    
    for i, description in enumerate(cas_normalisation, 1):
        print(f"\nTest {i}: {description}")
        
        type_relaxation = detecter_type_relaxation_sommier(description)
        print(f"  Type relaxation: {type_relaxation}")
        
        if type_relaxation == "RELAXATION":
            print(f"  ✅ Détecté correctement")
        else:
            print(f"  ❌ Non détecté")

if __name__ == "__main__":
    test_detection_type_relaxation()
    test_cas_variés()
    test_integration_backend()
    test_normalisation()
    
    print("\n✅ Tests terminés !") 