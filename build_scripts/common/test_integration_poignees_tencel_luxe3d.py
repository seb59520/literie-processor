#!/usr/bin/env python3
"""
Test d'intégration de la règle spéciale TENCEL LUXE 3D
"""

import sys
import os
sys.path.append('backend')

from backend_interface import BackendInterface

def test_integration_poignees_tencel_luxe3d():
    """Test d'intégration de la règle spéciale"""
    
    backend = BackendInterface()
    
    # Cas de test avec descriptions réalistes
    test_cases = [
        {
            "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°",
            "expected": {
                "poignees": "NON",
                "matiere_housse": "TENCEL LUXE 3D",
                "type_housse": "MATELASSEE"
            },
            "comment": "Cas Deversenne - TENCEL LUXE 3D avec poignées → doit forcer NON"
        },
        {
            "description": "MATELAS LATEX NATUREL 100% - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 30°",
            "expected": {
                "poignees": "NON",
                "matiere_housse": "TENCEL LUXE 3D",
                "type_housse": "MATELASSEE"
            },
            "comment": "TENCEL LUXE 3D sans mention poignées → doit forcer NON"
        },
        {
            "description": "MATELAS LATEX MIXTE 7 ZONES - HOUSSE SIMPLE TENCEL AVEC POIGNÉES",
            "expected": {
                "poignees": "OUI",
                "matiere_housse": "TENCEL",
                "type_housse": "SIMPLE"
            },
            "comment": "TENCEL normal avec poignées → doit détecter OUI"
        },
        {
            "description": "MATELAS MOUSSE VISCO - HOUSSE MATELASSÉE POLYESTER AVEC POIGNÉES INTÉGRÉES",
            "expected": {
                "poignees": "OUI",
                "matiere_housse": "POLYESTER",
                "type_housse": "MATELASSEE"
            },
            "comment": "POLYESTER avec poignées → doit détecter OUI"
        }
    ]
    
    print("🧪 Test d'intégration de la règle spéciale TENCEL LUXE 3D")
    print("=" * 80)
    
    all_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n--- Test d'intégration {i} ---")
        print(f"Description: {test_case['description']}")
        print(f"Attendu: {test_case['expected']}")
        print(f"Commentaire: {test_case['comment']}")
        
        # Tests de détection
        poignees = backend._detecter_poignees(test_case['description'])
        matiere_housse = backend._detecter_matiere_housse(test_case['description'])
        type_housse = backend._detecter_type_housse(test_case['description'])
        
        result = {
            "poignees": poignees,
            "matiere_housse": matiere_housse,
            "type_housse": type_housse
        }
        
        print(f"Résultat: {result}")
        
        # Vérification
        poignees_ok = poignees == test_case['expected']['poignees']
        matiere_ok = matiere_housse == test_case['expected']['matiere_housse']
        type_ok = type_housse == test_case['expected']['type_housse']
        
        if poignees_ok and matiere_ok and type_ok:
            print("✅ PASSÉ")
        else:
            print("❌ ÉCHOUÉ")
            if not poignees_ok:
                print(f"   Poignées attendues: {test_case['expected']['poignees']}, obtenues: {poignees}")
            if not matiere_ok:
                print(f"   Matière attendue: {test_case['expected']['matiere_housse']}, obtenue: {matiere_housse}")
            if not type_ok:
                print(f"   Type housse attendu: {test_case['expected']['type_housse']}, obtenu: {type_housse}")
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 TOUS LES TESTS D'INTÉGRATION SONT PASSÉS !")
        print("✅ La règle spéciale TENCEL LUXE 3D fonctionne parfaitement")
    else:
        print("⚠️  CERTAINS TESTS D'INTÉGRATION ONT ÉCHOUÉ")
        print("❌ La règle spéciale TENCEL LUXE 3D nécessite des corrections")
    
    return all_passed

def test_simulation_configuration():
    """Test de simulation d'une configuration complète"""
    
    backend = BackendInterface()
    
    # Description réaliste
    description = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°"
    
    print("\n🧪 Test de simulation de configuration")
    print("=" * 80)
    print(f"Description: {description}")
    
    # Simulation d'une configuration
    config = {
        "matelas_index": 1,
        "noyau": "MOUSSE RAINUREE 7 ZONES",
        "quantite": 1,
        "hauteur": 10,
        "fermete": "FERME",
        "housse": backend._detecter_type_housse(description),
        "matiere_housse": backend._detecter_matiere_housse(description),
        "poignees": backend._detecter_poignees(description),
        "dimensions": {"largeur": 79, "longueur": 198},
        "semaine_annee": "12_2025",
        "lundi": "2025-03-24",
        "vendredi": "2025-03-28",
        "commande_client": "Deversenne"
    }
    
    print(f"Configuration générée:")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    # Vérification de la règle spéciale
    if config['matiere_housse'] == "TENCEL LUXE 3D" and config['poignees'] == "NON":
        print("\n✅ RÈGLE SPÉCIALE RESPECTÉE")
        print("   TENCEL LUXE 3D → poignées forcées à NON")
        return True
    else:
        print("\n❌ RÈGLE SPÉCIALE NON RESPECTÉE")
        print(f"   Matière: {config['matiere_housse']}, Poignées: {config['poignees']}")
        return False

if __name__ == "__main__":
    print("🚀 Test d'intégration de la règle spéciale TENCEL LUXE 3D")
    print("Règle: Si matière housse = TENCEL LUXE 3D, alors poignées = NON")
    print()
    
    # Tests d'intégration
    integration_ok = test_integration_poignees_tencel_luxe3d()
    
    # Test de simulation
    simulation_ok = test_simulation_configuration()
    
    # Résumé final
    print("\n" + "=" * 80)
    print("📊 RÉSUMÉ FINAL")
    print("=" * 80)
    
    if integration_ok and simulation_ok:
        print("🎉 SUCCÈS COMPLET")
        print("✅ Tous les tests d'intégration sont passés")
        print("✅ La règle spéciale TENCEL LUXE 3D est opérationnelle")
        print("✅ La configuration est correctement générée")
        sys.exit(0)
    else:
        print("⚠️  ÉCHEC PARTIEL OU TOTAL")
        print("❌ Certains tests ont échoué")
        print("❌ La règle spéciale TENCEL LUXE 3D nécessite des corrections")
        sys.exit(1) 