#!/usr/bin/env python3
"""
Test pour vérifier la détection du noyau MOUSSE RAINUREE 7 ZONES
"""

import sys
import os
sys.path.append('backend')

from matelas_utils import detecter_noyau_matelas, normalize_str

def test_detection_noyau():
    """Test la détection du noyau MOUSSE RAINUREE 7 ZONES"""
    
    # Test avec différentes variantes
    test_cases = [
        {
            "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°",
            "expected": "MOUSSE RAINUREE 7 ZONES"
        },
        {
            "description": "MATELAS 1 PIÈCE - MOUSSE RAINUREE 7 ZONES DIFFÉRENCIÉES FERME",
            "expected": "MOUSSE RAINUREE 7 ZONES"
        },
        {
            "description": "MOUSSE RAINURÉE 7 ZONES",
            "expected": "MOUSSE RAINUREE 7 ZONES"
        }
    ]
    
    print("=== Test détection noyau MOUSSE RAINUREE 7 ZONES ===")
    
    for i, test_case in enumerate(test_cases):
        print(f"\n--- Test {i+1} ---")
        description = test_case["description"]
        expected = test_case["expected"]
        
        print(f"Description originale: {description}")
        
        # Test de normalisation
        normalized = normalize_str(description)
        print(f"Description normalisée: {normalized}")
        
        # Test de détection
        articles = [{"description": description}]
        result = detecter_noyau_matelas(articles)
        
        if result:
            detected_noyau = result[0]["noyau"]
            print(f"Noyau détecté: {detected_noyau}")
            print(f"Noyau attendu: {expected}")
            
            if detected_noyau == expected:
                print("✅ SUCCÈS: Noyau correctement détecté")
            else:
                print("❌ ÉCHEC: Noyau mal détecté")
        else:
            print("❌ ÉCHEC: Aucun noyau détecté")
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_detection_noyau() 