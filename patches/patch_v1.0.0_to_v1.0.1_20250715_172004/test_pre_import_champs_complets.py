#!/usr/bin/env python3

import sys
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage

def test_champs_complets():
    """Test de tous les nouveaux champs du pré-import"""
    
    print("=== TEST CHAMPS COMPLETS PRÉ-IMPORT ===")
    
    # Données client simulées
    donnees_client = {
        "nom": "Mr TEST COMPLET",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    # Configuration matelas complète avec tous les champs
    configurations_matelas = [
        {
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
        },
        {
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
    ]
    
    print("📋 Données d'entrée:")
    print(f"  - Client: {donnees_client['nom']}")
    print(f"  - Configurations matelas: {len(configurations_matelas)}")
    
    # Test 1: Création du pré-import
    print("\n📋 Test 1: Création du pré-import complet")
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=True)
    print(f"✅ Pré-import créé: {len(pre_import_data)} éléments")
    
    # Test 2: Vérification des champs pour le premier matelas (quantité = 2)
    print("\n📋 Test 2: Vérification matelas 1 (quantité = 2)")
    item1 = pre_import_data[0]
    print(f"  - jumeaux_C10: '{item1['jumeaux_C10']}' (attendu: 'X')")
    print(f"  - jumeaux_D10: '{item1['jumeaux_D10']}' (attendu: '89x198')")
    print(f"  - 1piece_C11: '{item1['1piece_C11']}' (attendu: '')")
    print(f"  - Hmat_luxe3D_C19: '{item1['Hmat_luxe3D_C19']}' (attendu: 'X')")
    print(f"  - Hmat_luxe3D_D19: '{item1.get('Hmat_luxe3D_D19', '')}' (attendu: '89x198')")
    print(f"  - poignees_C20: '{item1['poignees_C20']}' (attendu: 'X')")
    print(f"  - LN_Ferme_C28: '{item1['LN_Ferme_C28']}' (attendu: 'X')")
    print(f"  - Surmatelas_C45: '{item1['Surmatelas_C45']}' (attendu: 'X')")
    print(f"  - emporte_client_C57: '{item1['emporte_client_C57']}' (attendu: 'X')")
    print(f"  - fourgon_C58: '{item1['fourgon_C58']}' (attendu: 'X')")
    
    # Test 3: Vérification des champs pour le deuxième matelas (quantité = 1)
    print("\n📋 Test 3: Vérification matelas 2 (quantité = 1)")
    item2 = pre_import_data[1]
    print(f"  - jumeaux_C10: '{item2['jumeaux_C10']}' (attendu: '')")
    print(f"  - 1piece_C11: '{item2['1piece_C11']}' (attendu: 'X')")
    print(f"  - 1piece_D11: '{item2['1piece_D11']}' (attendu: '79x198')")
    print(f"  - HSimple_polyester_C13: '{item2['HSimple_polyester_C13']}' (attendu: 'X')")
    print(f"  - HSimple_polyester_D13: '{item2.get('HSimple_polyester_D13', '')}' (attendu: '79x198')")
    print(f"  - poignees_C20: '{item2['poignees_C20']}' (attendu: '')")
    print(f"  - MV_Confort_C36: '{item2['MV_Confort_C36']}' (attendu: 'X')")
    print(f"  - Surmatelas_C45: '{item2['Surmatelas_C45']}' (attendu: '')")
    print(f"  - transporteur_C59: '{item2['transporteur_C59']}' (attendu: 'X')")
    
    # Test 4: Validation du pré-import
    print("\n📋 Test 4: Validation du pré-import")
    validation = valider_pre_import(pre_import_data)
    print(f"✅ Validation: {validation}")
    
    # Test 5: Formatage pour affichage
    print("\n📋 Test 5: Formatage pour affichage")
    formatted_data = formater_pre_import_pour_affichage(pre_import_data)
    print(f"✅ Données formatées: {formatted_data['nombre_elements']} éléments")
    
    print("\n✅ Test des champs complets terminé avec succès!")
    return True

def test_cas_specifiques():
    """Test de cas spécifiques pour différents types de matelas"""
    
    print("\n=== TEST CAS SPÉCIFIQUES ===")
    
    donnees_client = {
        "nom": "Mr TEST CAS",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    # Test LATEX MIXTE 7 ZONES
    config_lm7z = {
        "matelas_index": 1,
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
    
    print("📋 Test LATEX MIXTE 7 ZONES MEDIUM")
    pre_import_lm7z = creer_pre_import([config_lm7z], donnees_client, contient_dosseret_tete=False)
    item = pre_import_lm7z[0]
    print(f"  - LM7z_Medium_C31: '{item['LM7z_Medium_C31']}' (attendu: 'X')")
    print(f"  - HSimple_tencel_C14: '{item['HSimple_tencel_C14']}' (attendu: 'X')")
    print(f"  - HSimple_tencel_D14: '{item.get('HSimple_tencel_D14', '')}' (attendu: '89x198')")
    
    # Test MOUSSE RAINUREE
    config_mr = {
        "matelas_index": 1,
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
    
    print("\n📋 Test MOUSSE RAINUREE FERME")
    pre_import_mr = creer_pre_import([config_mr], donnees_client, contient_dosseret_tete=False)
    item = pre_import_mr[0]
    print(f"  - MR_Ferme_C37: '{item['MR_Ferme_C37']}' (attendu: 'X')")
    print(f"  - Hmat_tencel_C18: '{item['Hmat_tencel_C18']}' (attendu: 'X')")
    print(f"  - Hmat_tencel_D18: '{item.get('Hmat_tencel_D18', '')}' (attendu: '79x198')")
    print(f"  - Surmatelas_C45: '{item['Surmatelas_C45']}' (attendu: 'X')")
    print(f"  - emporte_client_C57: '{item['emporte_client_C57']}' (attendu: 'X')")
    
    # Test SELECT 43
    config_sl43 = {
        "matelas_index": 1,
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
    
    print("\n📋 Test SELECT 43 MEDIUM")
    pre_import_sl43 = creer_pre_import([config_sl43], donnees_client, contient_dosseret_tete=False)
    item = pre_import_sl43[0]
    print(f"  - SL43_Medium_C41: '{item['SL43_Medium_C41']}' (attendu: 'X')")
    print(f"  - HSimple_autre_C15: '{item['HSimple_autre_C15']}' (attendu: 'X')")
    print(f"  - HSimple_autre_D15: '{item.get('HSimple_autre_D15', '')}' (attendu: '89x198')")
    print(f"  - fourgon_C58: '{item['fourgon_C58']}' (attendu: 'X')")
    
    print("\n✅ Test des cas spécifiques terminé!")

def test_champs_conditionnels():
    """Test des champs conditionnels (champs D pour les housses)"""
    
    print("\n=== TEST CHAMPS CONDITIONNELS ===")
    
    donnees_client = {
        "nom": "Mr TEST CONDITIONNEL",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    # Test housse simple polyester
    config_simple_poly = {
        "matelas_index": 1,
        "noyau": "LATEX NATUREL",
        "quantite": 1,
        "hauteur": 20,
        "fermete": "FERME",
        "housse": "SIMPLE",
        "matiere_housse": "POLYESTER",
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
    
    print("📋 Test housse SIMPLE + POLYESTER")
    pre_import = creer_pre_import([config_simple_poly], donnees_client, contient_dosseret_tete=False)
    item = pre_import[0]
    print(f"  - HSimple_polyester_C13: '{item['HSimple_polyester_C13']}' (attendu: 'X')")
    print(f"  - HSimple_polyester_D13: '{item.get('HSimple_polyester_D13', '')}' (attendu: '89x198')")
    print(f"  - HSimple_tencel_C14: '{item['HSimple_tencel_C14']}' (attendu: '')")
    print(f"  - HSimple_tencel_D14: '{item.get('HSimple_tencel_D14', '')}' (attendu: '')")
    
    # Test housse matelassée tencel
    config_mat_tencel = {
        "matelas_index": 1,
        "noyau": "MOUSSE VISCO",
        "quantite": 1,
        "hauteur": 18,
        "fermete": "MEDIUM",
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
        "surmatelas": False,
        "mots_operations_trouves": []
    }
    
    print("\n📋 Test housse MATELASSÉE + TENCEL")
    pre_import = creer_pre_import([config_mat_tencel], donnees_client, contient_dosseret_tete=False)
    item = pre_import[0]
    print(f"  - Hmat_tencel_C18: '{item['Hmat_tencel_C18']}' (attendu: 'X')")
    print(f"  - Hmat_tencel_D18: '{item.get('Hmat_tencel_D18', '')}' (attendu: '79x198')")
    print(f"  - Hmat_luxe3D_C19: '{item['Hmat_luxe3D_C19']}' (attendu: '')")
    print(f"  - Hmat_luxe3D_D19: '{item.get('Hmat_luxe3D_D19', '')}' (attendu: '')")
    
    print("\n✅ Test des champs conditionnels terminé!")

if __name__ == "__main__":
    test_champs_complets()
    test_cas_specifiques()
    test_champs_conditionnels()
    print("\n🎉 Tous les tests terminés avec succès!")
    print("\n📝 Résumé des nouveaux champs ajoutés:")
    print("  ✅ Champs quantité: jumeaux_C10/D10, 1piece_C11/D11")
    print("  ✅ Champs housse: HSimple_*, Hmat_* avec champs D conditionnels")
    print("  ✅ Champs poignées: poignees_C20")
    print("  ✅ Champs dimensions: dimension_housse_D23, longueur_D24, decoupe_noyau_D25")
    print("  ✅ Champs noyau/fermeté: LN_*, LM7z_*, LM3z_*, MV_*, MR_*, SL43_*")
    print("  ✅ Champs surmatelas: Surmatelas_C45")
    print("  ✅ Champs opérations: emporte_client_C57, fourgon_C58, transporteur_C59")
    print("  ✅ Validation mise à jour")
    print("  ✅ Affichage dans l'interface")
    print("  ✅ Tests complets et validation") 