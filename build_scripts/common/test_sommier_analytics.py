#!/usr/bin/env python3
"""
Test des nouvelles fonctionnalités d'analyse des sommiers
"""

import sys
import os
sys.path.append('backend')

from sommier_analytics_utils import (
    detecter_sommier_dans_un_lit,
    detecter_sommier_pieds,
    analyser_caracteristiques_sommier
)

def test_detection_sommier_dans_un_lit():
    """Test de la détection 'dans un lit'"""
    print("=== Test détection 'dans un lit' ===")
    
    test_cases = [
        ("Sommier à lattes dans un lit 160x200", "OUI"),
        ("SOMMIER DANS UN LIT avec pieds", "OUI"),
        ("Sommier tapissier standard 180x200", "NON"),
        ("Sommier métallique dans un lit 140x190", "OUI"),
        ("Sommier plat sans pieds", "NON")
    ]
    
    for description, expected in test_cases:
        result = detecter_sommier_dans_un_lit(description)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{description}' -> {result} (attendu: {expected})")

def test_detection_sommier_pieds():
    """Test de la détection 'pieds'"""
    print("\n=== Test détection 'pieds' ===")
    
    test_cases = [
        ("Sommier à lattes avec pieds 160x200", "OUI"),
        ("SOMMIER PIEDS métalliques", "OUI"),
        ("Sommier tapissier standard 180x200", "NON"),
        ("Sommier métallique sans pieds 140x190", "NON"),
        ("Sommier plat avec PIEDS", "OUI")
    ]
    
    for description, expected in test_cases:
        result = detecter_sommier_pieds(description)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{description}' -> {result} (attendu: {expected})")

def test_analyse_complete():
    """Test de l'analyse complète"""
    print("\n=== Test analyse complète ===")
    
    test_cases = [
        {
            "description": "Sommier à lattes dans un lit avec pieds 160x200",
            "expected": {"sommier_dansunlit": "OUI", "sommier_pieds": "OUI"}
        },
        {
            "description": "SOMMIER DANS UN LIT standard",
            "expected": {"sommier_dansunlit": "OUI", "sommier_pieds": "NON"}
        },
        {
            "description": "Sommier tapissier avec PIEDS 180x200",
            "expected": {"sommier_dansunlit": "NON", "sommier_pieds": "OUI"}
        },
        {
            "description": "Sommier métallique standard 140x190",
            "expected": {"sommier_dansunlit": "NON", "sommier_pieds": "NON"}
        }
    ]
    
    for test_case in test_cases:
        description = test_case["description"]
        expected = test_case["expected"]
        result = analyser_caracteristiques_sommier(description)
        
        success = (result["sommier_dansunlit"] == expected["sommier_dansunlit"] and 
                  result["sommier_pieds"] == expected["sommier_pieds"])
        status = "✅" if success else "❌"
        
        print(f"{status} '{description}'")
        print(f"   Résultat: {result}")
        print(f"   Attendu:  {expected}")
        print()

def test_integration_backend():
    """Test d'intégration avec le backend"""
    print("=== Test intégration backend ===")
    
    # Simulation d'une configuration sommier
    config = {
        "sommier_index": 1,
        "type_sommier": "SOMMIER À LATTES",
        "quantite": 1,
        "hauteur": 8,
        "materiau": "BOIS",
        "dimensions": {"largeur": 160, "longueur": 200},
        "semaine_annee": "S01_2025",
        "lundi": "2025-01-06",
        "vendredi": "2025-01-10",
        "commande_client": "Test Client",
        "sommier_dansunlit": "OUI",
        "sommier_pieds": "OUI"
    }
    
    print("Configuration sommier avec nouvelles caractéristiques:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Test du mapping Excel
    print("\nTest mapping Excel:")
    excel_mapping = {
        "Sommier_DansUnLit_D45": config.get('sommier_dansunlit', 'NON'),
        "Sommier_Pieds_D50": config.get('sommier_pieds', 'NON')
    }
    
    for key, value in excel_mapping.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    print("Test des nouvelles fonctionnalités d'analyse des sommiers")
    print("=" * 60)
    
    test_detection_sommier_dans_un_lit()
    test_detection_sommier_pieds()
    test_analyse_complete()
    test_integration_backend()
    
    print("\n✅ Tests terminés!") 