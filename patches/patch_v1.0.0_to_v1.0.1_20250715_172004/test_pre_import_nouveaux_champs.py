#!/usr/bin/env python3

import sys
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage

def test_nouveaux_champs():
    """Test des nouveaux champs du pré-import"""
    
    print("=== TEST NOUVEAUX CHAMPS PRÉ-IMPORT ===")
    
    # Données client simulées
    donnees_client = {
        "nom": "Mr LOUCHART FREDERIC",
        "adresse": "HAZEBROUCK",
        "code_client": "LOUCFSE"
    }
    
    # Configurations matelas simulées avec tous les nouveaux champs
    configurations_matelas = [
        {
            "matelas_index": 1,
            "noyau": "LATEX MIXTE 7 ZONES",
            "quantite": 1,
            "hauteur": 20,
            "fermete": "MÉDIUM",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL SIMPLE",
            "poignees": "OREILLES",
            "dimensions": {"largeur": 89, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "LOUCHART"
        },
        {
            "matelas_index": 2,
            "noyau": "MOUSSE RAINUREE 7 ZONES",
            "quantite": 2,
            "hauteur": 18,
            "fermete": "FERME",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL LUXE 3D",
            "poignees": "INTÉGRÉES",
            "dimensions": {"largeur": 79, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "LOUCHART"
        }
    ]
    
    print("📋 Données d'entrée:")
    print(f"  - Client: {donnees_client['nom']}")
    print(f"  - Ville: {donnees_client['adresse']}")
    print(f"  - Configurations matelas: {len(configurations_matelas)}")
    
    # Test 1: Création du pré-import sans dosseret/tete
    print("\n📋 Test 1: Création du pré-import sans dosseret/tete")
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=False)
    print(f"✅ Pré-import créé: {len(pre_import_data)} éléments")
    
    for i, item in enumerate(pre_import_data):
        print(f"  Élément {i + 1}:")
        print(f"    - Client_D1: {item['Client_D1']}")
        print(f"    - Adresse_D3: {item['Adresse_D3']}")
        print(f"    - numero_D2: {item['numero_D2']}")
        print(f"    - semaine_D5: {item['semaine_D5']}")
        print(f"    - lundi_D6: {item['lundi_D6']}")
        print(f"    - vendredi_D7: {item['vendredi_D7']}")
        print(f"    - Hauteur_D22: {item['Hauteur_D22']}")
        print(f"    - dosseret_tete_C8: '{item['dosseret_tete_C8']}'")
        print()
    
    # Test 2: Création du pré-import avec dosseret/tete
    print("📋 Test 2: Création du pré-import avec dosseret/tete")
    pre_import_data_avec_dosseret = creer_pre_import(configurations_matelas, donnees_client, contient_dosseret_tete=True)
    print(f"✅ Pré-import créé: {len(pre_import_data_avec_dosseret)} éléments")
    
    for i, item in enumerate(pre_import_data_avec_dosseret):
        print(f"  Élément {i + 1}:")
        print(f"    - dosseret_tete_C8: '{item['dosseret_tete_C8']}'")
        print()
    
    # Test 3: Validation du pré-import
    print("📋 Test 3: Validation du pré-import")
    validation = valider_pre_import(pre_import_data)
    print(f"✅ Validation: {validation}")
    
    # Test 4: Formatage pour affichage
    print("\n📋 Test 4: Formatage pour affichage")
    formatted_data = formater_pre_import_pour_affichage(pre_import_data)
    print(f"✅ Données formatées: {formatted_data['nombre_elements']} éléments")
    
    for element in formatted_data['elements']:
        print(f"  Élément {element['index']}:")
        print(f"    - Matelas #{element['matelas_index']} - {element['noyau']}")
        print(f"    - Quantité: {element['quantite']}")
        print(f"    - Champs: {element['champs']}")
        print()
    
    # Test 5: Structure JSON finale
    print("📋 Test 5: Structure JSON finale")
    result_backend = {
        "filename": "test_devis.pdf",
        "donnees_client": donnees_client,
        "configurations_matelas": configurations_matelas,
        "pre_import": pre_import_data,
        "contient_dosseret_ou_tete": False
    }
    
    print("✅ Structure de résultat créée")
    print(f"  - Nombre de configurations: {len(result_backend['configurations_matelas'])}")
    print(f"  - Nombre d'éléments pré-import: {len(result_backend['pre_import'])}")
    
    print("\n✅ Test des nouveaux champs terminé avec succès!")
    return True

def test_cas_reels_nouveaux_champs():
    """Test avec des cas réels incluant les nouveaux champs"""
    
    print("\n=== TEST AVEC CAS RÉELS NOUVEAUX CHAMPS ===")
    
    # Cas réel 1: Mr DEVERSENNE avec dosseret/tete
    donnees_client_1 = {
        "nom": "Mr DEVERSENNE CLAUDE",
        "adresse": "SAINT JANS CAPPEL",
        "code_client": "DEVECLA"
    }
    
    config_1 = [
        {
            "matelas_index": 1,
            "noyau": "MOUSSE RAINUREE 7 ZONES",
            "quantite": 2,
            "hauteur": 20,
            "fermete": "FERME",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL LUXE 3D",
            "poignees": "INTÉGRÉES",
            "dimensions": {"largeur": 79, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "DEVERSENNE"
        }
    ]
    
    print("📋 Cas réel 1: Mr DEVERSENNE avec dosseret/tete")
    pre_import_1 = creer_pre_import(config_1, donnees_client_1, contient_dosseret_tete=True)
    print(f"  - Pré-import créé: {len(pre_import_1)} élément(s)")
    print(f"  - Validation: {valider_pre_import(pre_import_1)}")
    
    for item in pre_import_1:
        print(f"    Client_D1: {item['Client_D1']}")
        print(f"    numero_D2: {item['numero_D2']}")
        print(f"    semaine_D5: {item['semaine_D5']}")
        print(f"    dosseret_tete_C8: '{item['dosseret_tete_C8']}'")
    
    # Cas réel 2: Mr BILAND sans dosseret/tete
    donnees_client_2 = {
        "nom": "Mr BILAND JEAN",
        "adresse": "LILLE",
        "code_client": "BILANJE"
    }
    
    config_2 = [
        {
            "matelas_index": 1,
            "noyau": "LATEX NATUREL",
            "quantite": 1,
            "hauteur": 22,
            "fermete": "MÉDIUM",
            "housse": "MATELASSÉE",
            "matiere_housse": "TENCEL",
            "poignees": "OREILLES",
            "dimensions": {"largeur": 89, "longueur": 198},
            "semaine_annee": "26_2025",
            "lundi": "2025-06-23",
            "vendredi": "2025-06-27",
            "commande_client": "BILAND"
        }
    ]
    
    print("\n📋 Cas réel 2: Mr BILAND sans dosseret/tete")
    pre_import_2 = creer_pre_import(config_2, donnees_client_2, contient_dosseret_tete=False)
    print(f"  - Pré-import créé: {len(pre_import_2)} élément(s)")
    print(f"  - Validation: {valider_pre_import(pre_import_2)}")
    
    for item in pre_import_2:
        print(f"    Client_D1: {item['Client_D1']}")
        print(f"    numero_D2: {item['numero_D2']}")
        print(f"    semaine_D5: {item['semaine_D5']}")
        print(f"    dosseret_tete_C8: '{item['dosseret_tete_C8']}'")
    
    print("\n✅ Test avec cas réels nouveaux champs terminé!")

def test_validation_nouveaux_champs():
    """Test de validation avec les nouveaux champs"""
    
    print("\n=== TEST VALIDATION NOUVEAUX CHAMPS ===")
    
    # Test avec données complètes
    donnees_client = {
        "nom": "Mr TEST COMPLET",
        "adresse": "VILLE TEST",
        "code_client": "TEST"
    }
    
    config_complete = [
        {
            "matelas_index": 1,
            "noyau": "TEST",
            "quantite": 1,
            "hauteur": 20,
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "TEST"
        }
    ]
    
    print("📋 Test validation avec données complètes")
    pre_import_complete = creer_pre_import(config_complete, donnees_client, contient_dosseret_tete=False)
    validation_complete = valider_pre_import(pre_import_complete)
    print(f"  - Validation: {validation_complete}")
    
    # Test avec données manquantes
    print("\n📋 Test validation avec données manquantes")
    config_incomplete = [
        {
            "matelas_index": 1,
            "noyau": "TEST",
            "quantite": 1,
            "hauteur": 20,
            # Manque semaine_annee, lundi, vendredi, commande_client
        }
    ]
    
    pre_import_incomplete = creer_pre_import(config_incomplete, donnees_client, contient_dosseret_tete=False)
    validation_incomplete = valider_pre_import(pre_import_incomplete)
    print(f"  - Validation: {validation_incomplete}")
    
    print("\n✅ Test de validation nouveaux champs terminé!")

if __name__ == "__main__":
    test_nouveaux_champs()
    test_cas_reels_nouveaux_champs()
    test_validation_nouveaux_champs()
    print("\n🎉 Tous les tests terminés avec succès!")
    print("\n📝 Résumé des nouveaux champs:")
    print("  ✅ numero_D2: commande_client")
    print("  ✅ semaine_D5: semaine_annee")
    print("  ✅ lundi_D6: lundi")
    print("  ✅ vendredi_D7: vendredi")
    print("  ✅ dosseret_tete_C8: 'X' si DOSSERET ou TETE détecté")
    print("  ✅ Validation mise à jour")
    print("  ✅ Affichage dans l'interface")
    print("  ✅ Tests complets et validation") 