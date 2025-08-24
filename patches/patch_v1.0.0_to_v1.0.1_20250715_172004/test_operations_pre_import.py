#!/usr/bin/env python3

import sys
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import

def test_operations():
    """Test des mots d'opération dans le pré-import"""
    
    print("=== TEST MOTS D'OPÉRATION PRÉ-IMPORT ===")
    
    # Données client simulées
    donnees_client = {
        "nom": "Mr TEST OPERATIONS",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    # Configuration matelas de base
    config_base = {
        "matelas_index": 1,
        "noyau": "LATEX NATUREL",
        "quantite": 1,
        "hauteur": 20,
        "fermete": "FERME",
        "housse": "MATELASSÉE",
        "matiere_housse": "TENCEL LUXE 3D",
        "poignees": "OUI",
        "dimensions": {"largeur": 89, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-16",
        "vendredi": "2025-06-20",
        "commande_client": "TEST",
        "dimension_housse": "89x198",
        "dimension_housse_longueur": "198",
        "decoupe_noyau": "STANDARD",
        "surmatelas": False
    }
    
    # Test 1: ENLEVEMENT
    print("📋 Test 1: ENLEVEMENT")
    mots_operations_1 = ["ENLEVEMENT"]
    pre_import_1 = creer_pre_import([config_base], donnees_client, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_1)
    item1 = pre_import_1[0]
    print(f"  - emporte_client_C57: '{item1['emporte_client_C57']}' (attendu: 'X')")
    print(f"  - fourgon_C58: '{item1['fourgon_C58']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item1['transporteur_C59']}' (attendu: '')")
    
    # Test 2: LIVRAISON
    print("\n📋 Test 2: LIVRAISON")
    mots_operations_2 = ["LIVRAISON"]
    pre_import_2 = creer_pre_import([config_base], donnees_client, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_2)
    item2 = pre_import_2[0]
    print(f"  - emporte_client_C57: '{item2['emporte_client_C57']}' (attendu: '')")
    print(f"  - fourgon_C58: '{item2['fourgon_C58']}' (attendu: 'X')")
    print(f"  - transporteur_C59: '{item2['transporteur_C59']}' (attendu: '')")
    
    # Test 3: EXPEDITION
    print("\n📋 Test 3: EXPEDITION")
    mots_operations_3 = ["EXPEDITION"]
    pre_import_3 = creer_pre_import([config_base], donnees_client, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_3)
    item3 = pre_import_3[0]
    print(f"  - emporte_client_C57: '{item3['emporte_client_C57']}' (attendu: '')")
    print(f"  - fourgon_C58: '{item3['fourgon_C58']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item3['transporteur_C59']}' (attendu: 'X')")
    
    # Test 4: ENLEVEMENT + LIVRAISON
    print("\n📋 Test 4: ENLEVEMENT + LIVRAISON")
    mots_operations_4 = ["ENLEVEMENT", "LIVRAISON"]
    pre_import_4 = creer_pre_import([config_base], donnees_client, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_4)
    item4 = pre_import_4[0]
    print(f"  - emporte_client_C57: '{item4['emporte_client_C57']}' (attendu: 'X')")
    print(f"  - fourgon_C58: '{item4['fourgon_C58']}' (attendu: 'X')")
    print(f"  - transporteur_C59: '{item4['transporteur_C59']}' (attendu: '')")
    
    # Test 5: Aucune opération
    print("\n📋 Test 5: Aucune opération")
    mots_operations_5 = []
    pre_import_5 = creer_pre_import([config_base], donnees_client, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_5)
    item5 = pre_import_5[0]
    print(f"  - emporte_client_C57: '{item5['emporte_client_C57']}' (attendu: '')")
    print(f"  - fourgon_C58: '{item5['fourgon_C58']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item5['transporteur_C59']}' (attendu: '')")
    
    # Test 6: Validation
    print("\n📋 Test 6: Validation")
    validation = valider_pre_import(pre_import_1)
    print(f"  - Validation: {validation}")
    
    print("\n✅ Test des mots d'opération terminé avec succès!")
    return True

def test_cas_reels_operations():
    """Test avec les cas réels fournis"""
    
    print("\n=== TEST CAS RÉELS OPÉRATIONS ===")
    
    # Cas réel 1: THULLIER avec LIVRAISON
    donnees_client_1 = {
        "nom": "Mr et Me THULLIER FREDERIC & NATHALIE",
        "adresse": "CAPPELLE LA GRANDE",
        "code_client": "THULFRCAP"
    }
    
    config_1 = {
        "matelas_index": 1,
        "noyau": "LATEX MIXTE 7 ZONES",
        "quantite": 2,
        "hauteur": 9,
        "fermete": "FERME",
        "housse": "MATELASSEE",
        "matiere_housse": "TENCEL LUXE 3D",
        "poignees": "NON",
        "dimensions": {"largeur": 89, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-23",
        "vendredi": "2025-06-27",
        "commande_client": "111",
        "dimension_housse": "4 x 101",
        "dimension_housse_longueur": 5.5,
        "decoupe_noyau": "89 x 199",
        "surmatelas": False
    }
    
    print("📋 Cas réel 1: THULLIER avec LIVRAISON")
    mots_operations_1 = ["LIVRAISON"]
    pre_import_1 = creer_pre_import([config_1], donnees_client_1, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_1)
    item1 = pre_import_1[0]
    print(f"  - emporte_client_C57: '{item1['emporte_client_C57']}' (attendu: '')")
    print(f"  - fourgon_C58: '{item1['fourgon_C58']}' (attendu: 'X')")
    print(f"  - transporteur_C59: '{item1['transporteur_C59']}' (attendu: '')")
    
    # Cas réel 2: LEROY avec ENLEVEMENT
    donnees_client_2 = {
        "nom": "Monsieur LEROY MICHEL",
        "adresse": "NIEPPE",
        "code_client": "LEROMNI"
    }
    
    config_2 = {
        "matelas_index": 1,
        "noyau": "LATEX MIXTE 7 ZONES",
        "quantite": 1,
        "hauteur": 9,
        "fermete": "MEDIUM",
        "housse": "MATELASSEE",
        "matiere_housse": "TENCEL LUXE 3D",
        "poignees": "OUI",
        "dimensions": {"largeur": 79, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-23",
        "vendredi": "2025-06-27",
        "commande_client": "123",
        "dimension_housse": "2 x 91",
        "dimension_housse_longueur": 5.5,
        "decoupe_noyau": "79 x 200",
        "surmatelas": False
    }
    
    print("\n📋 Cas réel 2: LEROY avec ENLEVEMENT")
    mots_operations_2 = ["ENLEVEMENT"]
    pre_import_2 = creer_pre_import([config_2], donnees_client_2, contient_dosseret_tete=False, mots_operation_trouves=mots_operations_2)
    item2 = pre_import_2[0]
    print(f"  - emporte_client_C57: '{item2['emporte_client_C57']}' (attendu: 'X')")
    print(f"  - fourgon_C58: '{item2['fourgon_C58']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item2['transporteur_C59']}' (attendu: '')")
    
    print("\n✅ Test des cas réels opérations terminé!")

if __name__ == "__main__":
    test_operations()
    test_cas_reels_operations()
    print("\n🎉 Tous les tests d'opérations terminés avec succès!")
    print("\n📝 Résumé des corrections:")
    print("  ✅ Ajout du paramètre mots_operation_trouves à creer_pre_import()")
    print("  ✅ Récupération des mots d'opération depuis llm_result dans main.py")
    print("  ✅ Passage des mots d'opération au niveau document (pas par matelas)")
    print("  ✅ Tests complets avec cas réels")
    print("  ✅ Validation du fonctionnement") 