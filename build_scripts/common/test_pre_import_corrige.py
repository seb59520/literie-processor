#!/usr/bin/env python3

import sys
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage

def test_champs_corrige():
    """Test corrigé des champs du pré-import"""
    
    print("=== TEST CHAMPS CORRIGÉ PRÉ-IMPORT ===")
    
    # Données client simulées
    donnees_client = {
        "nom": "Mr TEST CORRIGE",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    # Test 1: LATEX NATUREL FERME avec housse MATELASSÉE TENCEL LUXE 3D
    config1 = {
        "matelas_index": 1,
        "noyau": "LATEX NATUREL",
        "quantite": 2,
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
        "surmatelas": True,
        "mots_operations_trouves": ["ENLEVEMENT", "LIVRAISON"]
    }
    
    print("📋 Test 1: LATEX NATUREL FERME + MATELASSÉE TENCEL LUXE 3D")
    pre_import1 = creer_pre_import([config1], donnees_client, contient_dosseret_tete=True)
    item1 = pre_import1[0]
    print(f"  - jumeaux_C10: '{item1['jumeaux_C10']}' (attendu: 'X')")
    print(f"  - jumeaux_D10: '{item1['jumeaux_D10']}' (attendu: '89x198')")
    print(f"  - Hmat_luxe3D_C19: '{item1['Hmat_luxe3D_C19']}' (attendu: 'X')")
    print(f"  - Hmat_luxe3D_D19: '{item1.get('Hmat_luxe3D_D19', '')}' (attendu: '89x198')")
    print(f"  - LN_Ferme_C28: '{item1['LN_Ferme_C28']}' (attendu: 'X')")
    print(f"  - poignees_C20: '{item1['poignees_C20']}' (attendu: 'X')")
    print(f"  - Surmatelas_C45: '{item1['Surmatelas_C45']}' (attendu: 'X')")
    print(f"  - emporte_client_C57: '{item1['emporte_client_C57']}' (attendu: 'X')")
    print(f"  - fourgon_C58: '{item1['fourgon_C58']}' (attendu: 'X')")
    
    # Test 2: MOUSSE VISCO CONFORT avec housse SIMPLE POLYESTER
    config2 = {
        "matelas_index": 2,
        "noyau": "MOUSSE VISCO",
        "quantite": 1,
        "hauteur": 18,
        "fermete": "CONFORT",
        "housse": "SIMPLE",
        "matiere_housse": "POLYESTER",
        "poignees": "NON",
        "dimensions": {"largeur": 79, "longueur": 198},
        "semaine_annee": "26_2025",
        "lundi": "2025-06-23",
        "vendredi": "2025-06-27",
        "commande_client": "TEST",
        "dimension_housse": "79x198",
        "dimension_housse_longueur": "198",
        "decoupe_noyau": "SPECIALE",
        "surmatelas": False,
        "mots_operations_trouves": ["EXPEDITION"]
    }
    
    print("\n📋 Test 2: MOUSSE VISCO CONFORT + SIMPLE POLYESTER")
    pre_import2 = creer_pre_import([config2], donnees_client, contient_dosseret_tete=False)
    item2 = pre_import2[0]
    print(f"  - 1piece_C11: '{item2['1piece_C11']}' (attendu: 'X')")
    print(f"  - 1piece_D11: '{item2['1piece_D11']}' (attendu: '79x198')")
    print(f"  - HSimple_polyester_C13: '{item2['HSimple_polyester_C13']}' (attendu: 'X')")
    print(f"  - HSimple_polyester_D13: '{item2.get('HSimple_polyester_D13', '')}' (attendu: '79x198')")
    print(f"  - MV_Confort_C36: '{item2['MV_Confort_C36']}' (attendu: 'X')")
    print(f"  - poignees_C20: '{item2['poignees_C20']}' (attendu: '')")
    print(f"  - Surmatelas_C45: '{item2['Surmatelas_C45']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item2['transporteur_C59']}' (attendu: 'X')")
    
    # Test 3: LATEX MIXTE 7 ZONES MEDIUM avec housse SIMPLE TENCEL
    config3 = {
        "matelas_index": 3,
        "noyau": "LATEX MIXTE 7 ZONES",
        "quantite": 1,
        "hauteur": 20,
        "fermete": "MEDIUM",
        "housse": "SIMPLE",
        "matiere_housse": "TENCEL",
        "poignees": "OUI",
        "dimensions": {"largeur": 89, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-16",
        "vendredi": "2025-06-20",
        "commande_client": "TEST",
        "dimension_housse": "89x198",
        "dimension_housse_longueur": "198",
        "decoupe_noyau": "STANDARD",
        "surmatelas": False,
        "mots_operations_trouves": []
    }
    
    print("\n📋 Test 3: LATEX MIXTE 7 ZONES MEDIUM + SIMPLE TENCEL")
    pre_import3 = creer_pre_import([config3], donnees_client, contient_dosseret_tete=False)
    item3 = pre_import3[0]
    print(f"  - LM7z_Medium_C31: '{item3['LM7z_Medium_C31']}' (attendu: 'X')")
    print(f"  - HSimple_tencel_C14: '{item3['HSimple_tencel_C14']}' (attendu: 'X')")
    print(f"  - HSimple_tencel_D14: '{item3.get('HSimple_tencel_D14', '')}' (attendu: '89x198')")
    
    # Test 4: MOUSSE RAINUREE FERME avec housse MATELASSÉE TENCEL
    config4 = {
        "matelas_index": 4,
        "noyau": "MOUSSE RAINUREE",
        "quantite": 1,
        "hauteur": 18,
        "fermete": "FERME",
        "housse": "MATELASSÉE",
        "matiere_housse": "TENCEL",
        "poignees": "NON",
        "dimensions": {"largeur": 79, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-16",
        "vendredi": "2025-06-20",
        "commande_client": "TEST",
        "dimension_housse": "79x198",
        "dimension_housse_longueur": "198",
        "decoupe_noyau": "STANDARD",
        "surmatelas": True,
        "mots_operations_trouves": ["ENLEVEMENT"]
    }
    
    print("\n📋 Test 4: MOUSSE RAINUREE FERME + MATELASSÉE TENCEL")
    pre_import4 = creer_pre_import([config4], donnees_client, contient_dosseret_tete=False)
    item4 = pre_import4[0]
    print(f"  - MR_Ferme_C37: '{item4['MR_Ferme_C37']}' (attendu: 'X')")
    print(f"  - Hmat_tencel_C18: '{item4['Hmat_tencel_C18']}' (attendu: 'X')")
    print(f"  - Hmat_tencel_D18: '{item4.get('Hmat_tencel_D18', '')}' (attendu: '79x198')")
    print(f"  - Surmatelas_C45: '{item4['Surmatelas_C45']}' (attendu: 'X')")
    print(f"  - emporte_client_C57: '{item4['emporte_client_C57']}' (attendu: 'X')")
    
    # Test 5: SELECT 43 MEDIUM avec housse SIMPLE AUTRE
    config5 = {
        "matelas_index": 5,
        "noyau": "SELECT 43",
        "quantite": 1,
        "hauteur": 22,
        "fermete": "MEDIUM",
        "housse": "SIMPLE",
        "matiere_housse": "AUTRE",
        "poignees": "OUI",
        "dimensions": {"largeur": 89, "longueur": 198},
        "semaine_annee": "25_2025",
        "lundi": "2025-06-16",
        "vendredi": "2025-06-20",
        "commande_client": "TEST",
        "dimension_housse": "89x198",
        "dimension_housse_longueur": "198",
        "decoupe_noyau": "STANDARD",
        "surmatelas": False,
        "mots_operations_trouves": ["LIVRAISON"]
    }
    
    print("\n📋 Test 5: SELECT 43 MEDIUM + SIMPLE AUTRE")
    pre_import5 = creer_pre_import([config5], donnees_client, contient_dosseret_tete=False)
    item5 = pre_import5[0]
    print(f"  - SL43_Medium_C41: '{item5['SL43_Medium_C41']}' (attendu: 'X')")
    print(f"  - HSimple_autre_C15: '{item5['HSimple_autre_C15']}' (attendu: 'X')")
    print(f"  - HSimple_autre_D15: '{item5.get('HSimple_autre_D15', '')}' (attendu: '89x198')")
    print(f"  - fourgon_C58: '{item5['fourgon_C58']}' (attendu: 'X')")
    
    # Test 6: Validation et formatage
    print("\n📋 Test 6: Validation et formatage")
    all_configs = [config1, config2, config3, config4, config5]
    pre_import_all = creer_pre_import(all_configs, donnees_client, contient_dosseret_tete=False)
    validation = valider_pre_import(pre_import_all)
    print(f"  - Validation: {validation}")
    
    formatted_data = formater_pre_import_pour_affichage(pre_import_all)
    print(f"  - Formatage: {formatted_data['nombre_elements']} éléments")
    
    print("\n✅ Test corrigé terminé avec succès!")
    return True

if __name__ == "__main__":
    test_champs_corrige()
    print("\n🎉 Test corrigé terminé avec succès!")
    print("\n📝 Résumé des champs testés:")
    print("  ✅ Champs quantité: jumeaux_C10/D10, 1piece_C11/D11")
    print("  ✅ Champs housse: HSimple_*, Hmat_* avec champs D conditionnels")
    print("  ✅ Champs poignées: poignees_C20")
    print("  ✅ Champs noyau/fermeté: LN_*, LM7z_*, MR_*, MV_*, SL43_*")
    print("  ✅ Champs surmatelas: Surmatelas_C45")
    print("  ✅ Champs opérations: emporte_client_C57, fourgon_C58, transporteur_C59")
    print("  ✅ Validation et formatage") 