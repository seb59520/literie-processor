#!/usr/bin/env python3
"""
Test de la règle spéciale : TENCEL LUXE 3D → poignées = NON
"""

import sys
import os
sys.path.append('backend')

from backend_interface import BackendInterface

def test_poignees_tencel_luxe3d():
    """Test de la règle spéciale pour TENCEL LUXE 3D"""
    
    backend = BackendInterface()
    
    # Cas de test
    test_cases = [
        {
            "description": "MATELAS LATEX HOUSSE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES",
            "expected_poignees": "NON",
            "expected_matiere": "TENCEL LUXE 3D",
            "comment": "TENCEL LUXE 3D avec poignées → doit retourner NON"
        },
        {
            "description": "MATELAS MOUSSE HOUSSE TENCEL LUXE 3D LAVABLE",
            "expected_poignees": "NON",
            "expected_matiere": "TENCEL LUXE 3D",
            "comment": "TENCEL LUXE 3D sans poignées → doit retourner NON"
        },
        {
            "description": "MATELAS LATEX HOUSSE TENCEL AVEC POIGNÉES",
            "expected_poignees": "OUI",
            "expected_matiere": "TENCEL",
            "comment": "TENCEL normal avec poignées → doit retourner OUI"
        },
        {
            "description": "MATELAS MOUSSE HOUSSE POLYESTER AVEC POIGNÉES",
            "expected_poignees": "OUI",
            "expected_matiere": "POLYESTER",
            "comment": "POLYESTER avec poignées → doit retourner OUI"
        },
        {
            "description": "MATELAS LATEX HOUSSE POLYESTER SANS POIGNÉES",
            "expected_poignees": "NON",
            "expected_matiere": "POLYESTER",
            "comment": "POLYESTER sans poignées → doit retourner NON"
        }
    ]
    
    print("🧪 Test de la règle spéciale TENCEL LUXE 3D")
    print("=" * 60)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test {i} ---")
        print(f"Description: {test_case['description']}")
        print(f"Attendu: Poignées = {test_case['expected_poignees']}, Matière = {test_case['expected_matiere']}")
        print(f"Commentaire: {test_case['comment']}")
        
        # Test de détection des poignées
        poignees_result = backend._detecter_poignees(test_case['description'])
        
        # Test de détection de la matière housse
        matiere_result = backend._detecter_matiere_housse(test_case['description'])
        
        # Vérification
        poignees_ok = poignees_result == test_case['expected_poignees']
        matiere_ok = matiere_result == test_case['expected_matiere']
        
        print(f"Résultat: Poignées = {poignees_result}, Matière = {matiere_result}")
        
        if poignees_ok and matiere_ok:
            print("✅ PASSÉ")
        else:
            print("❌ ÉCHOUÉ")
            if not poignees_ok:
                print(f"   Poignées attendues: {test_case['expected_poignees']}, obtenues: {poignees_result}")
            if not matiere_ok:
                print(f"   Matière attendue: {test_case['expected_matiere']}, obtenue: {matiere_result}")
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("✅ La règle spéciale TENCEL LUXE 3D fonctionne correctement")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("❌ La règle spéciale TENCEL LUXE 3D ne fonctionne pas comme attendu")
    
    return all_passed

def test_cas_reel():
    """Test avec le cas réel de Deversenne"""
    
    backend = BackendInterface()
    
    # Description exacte de Deversenne
    description = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°"
    
    print("\n🧪 Test du cas réel Deversenne")
    print("=" * 60)
    print(f"Description: {description}")
    
    # Test de détection
    poignees = backend._detecter_poignees(description)
    matiere = backend._detecter_matiere_housse(description)
    
    print(f"Résultat: Poignées = {poignees}, Matière = {matiere}")
    
    # Vérification
    if poignees == "NON" and matiere == "TENCEL LUXE 3D":
        print("✅ CAS RÉEL PASSÉ - La règle fonctionne pour Deversenne")
        return True
    else:
        print("❌ CAS RÉEL ÉCHOUÉ - La règle ne fonctionne pas pour Deversenne")
        return False

if __name__ == "__main__":
    print("🚀 Test de la règle spéciale TENCEL LUXE 3D")
    print("Règle: Si matière housse = TENCEL LUXE 3D, alors poignées = NON")
    print()
    
    # Tests généraux
    tests_ok = test_poignees_tencel_luxe3d()
    
    # Test cas réel
    cas_reel_ok = test_cas_reel()
    
    # Résumé final
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 60)
    
    if tests_ok and cas_reel_ok:
        print("🎉 SUCCÈS COMPLET")
        print("✅ Tous les tests sont passés")
        print("✅ La règle spéciale TENCEL LUXE 3D est opérationnelle")
        sys.exit(0)
    else:
        print("⚠️  ÉCHEC PARTIEL OU TOTAL")
        print("❌ Certains tests ont échoué")
        print("❌ La règle spéciale TENCEL LUXE 3D nécessite des corrections")
        sys.exit(1) 