#!/usr/bin/env python3
"""
Test de détection du type télécommande des sommiers
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sommier_utils import detecter_type_telecommande_sommier

def test_detection_type_telecommande():
    """Test de la détection du type télécommande"""
    print("=== TEST DÉTECTION TYPE TÉLÉCOMMANDE SOMMIERS ===")
    
    # Test avec la description fournie par l'utilisateur
    description_test = "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE - 2 MOTEURS RENFORCES (2X6000N) - DOUBLES LATTES ( HÊTRE MULTIPLIS ) - STRUCTURE EN HÊTRE LAQUÉ NOIR SATINÉ 99/ 199/ 19"
    
    print(f"Description test: {description_test}")
    
    # Détection du type télécommande
    type_telecommande = detecter_type_telecommande_sommier(description_test)
    print(f"✅ Type télécommande détecté: {type_telecommande}")
    
    # Vérification de la valeur attendue
    if type_telecommande == "NON":
        print("✅ Valeur correcte détectée (pas de télécommande mentionnée)")
    else:
        print("❌ Valeur incorrecte détectée")
        print(f"Attendu: NON")
        print(f"Obtenu: {type_telecommande}")
    
    print()

def test_cas_variés():
    """Test avec différents cas de figures"""
    print("=== TEST CAS VARIÉS ===")
    
    cas_tests = [
        # Cas sans télécommande
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        "SOMMIER BOIS MASSIF FIXE",
        
        # Cas avec télécommande filaire
        "SOMMIER RELAXATION AVEC TELECOMMANDE",
        "SOMMIER MOTORISÉ TELECOMMANDE FILAIRE",
        "SOMMIER RELAXATION TELECOMMANDES",
        "SOMMIER AVEC TELECOMMANDE ET MOTEURS",
        
        # Cas avec télécommande sans fil (radio)
        "SOMMIER RELAXATION TELECOMMANDE RADIO",
        "SOMMIER MOTORISÉ TELECOMMANDE SANS FIL RADIO",
        "SOMMIER RELAXATION AVEC TELECOMMANDES RADIO",
        "SOMMIER TELECOMMANDE RADIO MOTORISÉ",
        
        # Cas mixtes
        "SOMMIER RELAXATION TELECOMMANDE RADIO ET FILAIRE",
        "SOMMIER AVEC RADIO ET TELECOMMANDE",
        "SOMMIER RADIO TELECOMMANDE MOTORISÉ"
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        type_telecommande = detecter_type_telecommande_sommier(description)
        print(f"  Type télécommande: {type_telecommande}")
        
        # Vérification logique
        desc_upper = description.upper()
        has_telecommande = "TELECOMMANDE" in desc_upper or "TELECOMMANDES" in desc_upper
        has_radio = "RADIO" in desc_upper
        
        if not has_telecommande:
            expected = "NON"
        elif has_telecommande and has_radio:
            expected = "TELECOMMANDE SANS FIL"
        else:  # has_telecommande and not has_radio
            expected = "TELECOMMANDE FILAIRE"
            
        if type_telecommande == expected:
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
                "description": "SOMMIER RELAXATION AVEC TELECOMMANDE RADIO",
                "quantite": 1
            },
            {
                "description": "SOMMIER MOTORISÉ TELECOMMANDE FILAIRE",
                "quantite": 1
            }
        ]
        
        types_sommiers = [
            {"index": 1, "type_sommier": "SOMMIER À LATTES"},
            {"index": 2, "type_sommier": "SOMMIER À LATTES"},
            {"index": 3, "type_sommier": "SOMMIER À LATTES"}
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
                print(f"    Type télécommande: {config.get('type_telecommande_sommier', 'Non trouvé')}")
                print(f"    Dimension sommier: {config.get('dimension_sommier', 'Non trouvé')}")
        else:
            print("❌ Aucune configuration créée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")

def test_normalisation():
    """Test de la normalisation des caractères"""
    print("\n=== TEST NORMALISATION ===")
    
    cas_normalisation = [
        "SOMMIER TELECOMMANDE",
        "SOMMIER TÉLÉCOMMANDE",  # Avec accents
        "SOMMIER telecommande",  # Minuscules
        "SOMMIER Telecommande",  # Mixte
        "SOMMIER TELECOMMANDES",  # Pluriel
        "SOMMIER RADIO",
        "SOMMIER radio",  # Minuscules
        "SOMMIER Radio",  # Mixte
    ]
    
    for i, description in enumerate(cas_normalisation, 1):
        print(f"\nTest {i}: {description}")
        
        type_telecommande = detecter_type_telecommande_sommier(description)
        print(f"  Type télécommande: {type_telecommande}")
        
        # Vérification logique
        desc_upper = description.upper()
        has_telecommande = "TELECOMMANDE" in desc_upper or "TELECOMMANDES" in desc_upper
        has_radio = "RADIO" in desc_upper
        
        if not has_telecommande:
            expected = "NON"
        elif has_telecommande and has_radio:
            expected = "TELECOMMANDE SANS FIL"
        else:
            expected = "TELECOMMANDE FILAIRE"
            
        if type_telecommande == expected:
            print(f"  ✅ Détecté correctement")
        else:
            print(f"  ❌ Non détecté (attendu: {expected})")

if __name__ == "__main__":
    test_detection_type_telecommande()
    test_cas_variés()
    test_integration_backend()
    test_normalisation()
    
    print("\n✅ Tests terminés !") 