#!/usr/bin/env python3
"""
Test de détection des nouvelles caractéristiques des sommiers
"""

import sys
import os

# Ajouter le répertoire backend au path
script_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.join(script_dir, "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from sommier_utils import detecter_soufflet_mousse_sommier, detecter_facon_moderne_sommier, detecter_tapissier_a_lattes_sommier, detecter_lattes_francaises_sommier

def test_detection_soufflet_mousse():
    """Test de la détection du soufflet mousse"""
    print("=== TEST DÉTECTION SOUFFLET MOUSSE ===")
    
    cas_tests = [
        # Cas sans soufflet mousse
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        
        # Cas avec soufflet mousse
        "SOMMIER AVEC SOUFFLET MOUSSE",
        "SOMMIER SOUFFLET MOUSSE CONFORTABLE",
        "SOMMIER AVEC SOUFFLETS MOUSSE",
        "SOMMIER SOUFFLETS MOUSSE",
        "SOMMIER soufflet mousse",  # Minuscules
        "SOMMIER Soufflet Mousse",  # Mixte
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        resultat = detecter_soufflet_mousse_sommier(description)
        print(f"  Soufflet mousse: {resultat}")
        
        # Vérification logique
        desc_upper = description.upper()
        expected = "OUI" if ("SOUFFLET MOUSSE" in desc_upper or "SOUFFLETS MOUSSE" in desc_upper) else "NON"
        
        if resultat == expected:
            print(f"  ✅ Correct")
        else:
            print(f"  ❌ Incorrect (attendu: {expected})")

def test_detection_facon_moderne():
    """Test de la détection de façon moderne"""
    print("\n=== TEST DÉTECTION FAÇON MODERNE ===")
    
    cas_tests = [
        # Cas sans façon moderne
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        
        # Cas avec façon moderne
        "SOMMIER FAÇON MODERNE",
        "SOMMIER DE FAÇON MODERNE",
        "SOMMIER façon moderne",  # Minuscules
        "SOMMIER Façon Moderne",  # Mixte
        "SOMMIER FACON MODERNE",  # Sans accent
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        resultat = detecter_facon_moderne_sommier(description)
        print(f"  Façon moderne: {resultat}")
        
        # Vérification logique (après normalisation)
        import unicodedata
        desc_normalized = ''.join(
            c for c in unicodedata.normalize('NFD', description.upper())
            if unicodedata.category(c) != 'Mn'
        )
        expected = "OUI" if "FACON MODERNE" in desc_normalized else "NON"
        
        if resultat == expected:
            print(f"  ✅ Correct")
        else:
            print(f"  ❌ Incorrect (attendu: {expected})")

def test_detection_tapissier_a_lattes():
    """Test de la détection de tapissier à lattes"""
    print("\n=== TEST DÉTECTION TAPISSIER À LATTES ===")
    
    cas_tests = [
        # Cas sans tapissier à lattes
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        
        # Cas avec tapissier à lattes
        "SOMMIER TAPISSIER À LATTES",
        "SOMMIER TAPISSIER A LATTES",  # Sans accent
        "SOMMIER tapissier à lattes",  # Minuscules
        "SOMMIER Tapissier À Lattes",  # Mixte
        "SOMMIER TAPISSIER À LATTES CONFORTABLE",
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        resultat = detecter_tapissier_a_lattes_sommier(description)
        print(f"  Tapissier à lattes: {resultat}")
        
        # Vérification logique (après normalisation)
        import unicodedata
        desc_normalized = ''.join(
            c for c in unicodedata.normalize('NFD', description.upper())
            if unicodedata.category(c) != 'Mn'
        )
        expected = "OUI" if "TAPISSIER A LATTES" in desc_normalized else "NON"
        
        if resultat == expected:
            print(f"  ✅ Correct")
        else:
            print(f"  ❌ Incorrect (attendu: {expected})")

def test_detection_lattes_francaises():
    """Test de la détection de lattes françaises"""
    print("\n=== TEST DÉTECTION LATTES FRANÇAISES ===")
    
    cas_tests = [
        # Cas sans lattes françaises
        "SOMMIER RELAXATION MOTORISÉE 5 PLIS TÉLESCOPIQUE",
        "SOMMIER À LATTES FIXE",
        "SOMMIER TAPISSIER STANDARD",
        "SOMMIER LATTES STANDARD",
        
        # Cas avec lattes françaises
        "SOMMIER LATTES FRANÇAISES",
        "SOMMIER LATTES FRANCAISES",  # Sans accent
        "SOMMIER LATTE FRANÇAISE",  # Singulier
        "SOMMIER LATTE FRANCAISE",  # Singulier sans accent
        "SOMMIER lattes françaises",  # Minuscules
        "SOMMIER Lattes Françaises",  # Mixte
        "SOMMIER AVEC LATTES FRANÇAISES CONFORTABLES",
    ]
    
    for i, description in enumerate(cas_tests, 1):
        print(f"\nTest {i}: {description}")
        
        resultat = detecter_lattes_francaises_sommier(description)
        print(f"  Lattes françaises: {resultat}")
        
        # Vérification logique (après normalisation)
        import unicodedata
        desc_normalized = ''.join(
            c for c in unicodedata.normalize('NFD', description.upper())
            if unicodedata.category(c) != 'Mn'
        )
        expected = "OUI" if ("LATTES FRANCAISES" in desc_normalized or "LATTE FRANCAISE" in desc_normalized) else "NON"
        
        if resultat == expected:
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
                "description": "SOMMIER AVEC SOUFFLET MOUSSE ET FAÇON MODERNE",
                "quantite": 1
            },
            {
                "description": "SOMMIER TAPISSIER À LATTES CONFORTABLE",
                "quantite": 1
            }
        ]
        
        types_sommiers = [
            {"index": 1, "type_sommier": "SOMMIER À LATTES"},
            {"index": 2, "type_sommier": "SOMMIER À LATTES"},
            {"index": 3, "type_sommier": "SOMMIER TAPISSIER"}
        ]
        
        interface = BackendInterface()
        configurations = interface._create_configurations_sommiers(
            types_sommiers, sommier_articles, 1, 2025, "TEST123"
        )
        
        if configurations:
            print(f"✅ Configurations créées: {len(configurations)}")
            for i, config in enumerate(configurations):
                print(f"  Sommier {i+1}:")
                print(f"    Soufflet mousse: {config.get('soufflet_mousse', 'Non trouvé')}")
                print(f"    Façon moderne: {config.get('facon_moderne', 'Non trouvé')}")
                print(f"    Tapissier à lattes: {config.get('tapissier_a_lattes', 'Non trouvé')}")
                print(f"    Lattes françaises: {config.get('lattes_francaises', 'Non trouvé')}")
                print(f"    Type relaxation: {config.get('type_relaxation_sommier', 'Non trouvé')}")
                print(f"    Type télécommande: {config.get('type_telecommande_sommier', 'Non trouvé')}")
        else:
            print("❌ Aucune configuration créée")
            
    except Exception as e:
        print(f"❌ Erreur lors du test d'intégration: {e}")

def test_normalisation():
    """Test de la normalisation des caractères"""
    print("\n=== TEST NORMALISATION ===")
    
    cas_normalisation = [
        "SOMMIER SOUFFLET MOUSSE",
        "SOMMIER SOUFFLETS MOUSSE",  # Pluriel
        "SOMMIER FAÇON MODERNE",
        "SOMMIER FACON MODERNE",  # Sans accent
        "SOMMIER TAPISSIER À LATTES",
        "SOMMIER TAPISSIER A LATTES",  # Sans accent
    ]
    
    for i, description in enumerate(cas_normalisation, 1):
        print(f"\nTest {i}: {description}")
        
        soufflet = detecter_soufflet_mousse_sommier(description)
        facon = detecter_facon_moderne_sommier(description)
        tapissier = detecter_tapissier_a_lattes_sommier(description)
        lattes_fr = detecter_lattes_francaises_sommier(description)
        
        print(f"  Soufflet mousse: {soufflet}")
        print(f"  Façon moderne: {facon}")
        print(f"  Tapissier à lattes: {tapissier}")
        print(f"  Lattes françaises: {lattes_fr}")

def test_telecommande_avancee():
    """Test avancé de la détection de télécommande (cas complexes)"""
    print("\n=== TESTS AVANCÉS TÉLÉCOMMANDE ===")
    cas_tests = [
        ("TÉLÉCOMMANDE NOIRE RADIO FRÉQUENCE (x2) + ÉCLAIRAGE TORCHE", "TELECOMMANDE SANS FIL"),
        ("TELECOMMANDE NOIRE RADIO FREQUENCE (x2) + ECLAIRAGE TORCHE", "TELECOMMANDE SANS FIL"),
        ("TÉLÉCOMMANDE RADIO", "TELECOMMANDE SANS FIL"),
        ("TELECOMMANDE RADIO", "TELECOMMANDE SANS FIL"),
        ("TÉLÉCOMMANDE SANS RADIO", "TELECOMMANDE FILAIRE"),
        ("RADIO SANS TÉLÉCOMMANDE", "TELECOMMANDE SANS FIL"),
        ("TÉLÉCOMMANDE FILAIRE", "TELECOMMANDE FILAIRE"),
        ("TELECOMMANDE FILAIRE", "TELECOMMANDE FILAIRE"),
        ("SOMMIER SANS TELECOMMANDE", "NON"),
        ("SOMMIER RADIO", "NON"),
    ]
    from sommier_utils import detecter_type_telecommande_sommier
    for i, (desc, attendu) in enumerate(cas_tests, 1):
        resultat = detecter_type_telecommande_sommier(desc)
        print(f"Test {i}: '{desc}' -> {resultat} (attendu: {attendu})")
        if resultat == attendu:
            print("  ✅ Correct")
        else:
            print("  ❌ Incorrect")

if __name__ == "__main__":
    test_detection_soufflet_mousse()
    test_detection_facon_moderne()
    test_detection_tapissier_a_lattes()
    test_detection_lattes_francaises()
    test_telecommande_avancee()
    test_integration_backend()
    test_normalisation()
    
    print("\n✅ Tests terminés !") 