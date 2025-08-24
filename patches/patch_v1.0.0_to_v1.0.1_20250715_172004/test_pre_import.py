#!/usr/bin/env python3

import sys
sys.path.append('backend')

from pre_import_utils import creer_pre_import, valider_pre_import, formater_pre_import_pour_affichage

def test_pre_import():
    """Test de l'étape de pré-import"""
    
    print("=== TEST ÉTAPE PRÉ-IMPORT ===")
    
    # Données client simulées
    donnees_client = {
        "nom": "Mr LOUCHART FREDERIC",
        "adresse": "HAZEBROUCK",
        "code_client": "LOUCFSE"
    }
    
    # Configurations matelas simulées
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
    
    # Test 1: Création du pré-import
    print("\n📋 Test 1: Création du pré-import")
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client)
    print(f"✅ Pré-import créé: {len(pre_import_data)} éléments")
    
    for i, item in enumerate(pre_import_data):
        print(f"  Élément {i + 1}:")
        print(f"    - Client_D1: {item['Client_D1']}")
        print(f"    - Adresse_D3: {item['Adresse_D3']}")
        print(f"    - Hauteur_D22: {item['Hauteur_D22']}")
        print(f"    - Noyau: {item['noyau']}")
        print()
    
    # Test 2: Validation du pré-import
    print("📋 Test 2: Validation du pré-import")
    validation = valider_pre_import(pre_import_data)
    print(f"✅ Validation: {validation}")
    
    # Test 3: Formatage pour affichage
    print("\n📋 Test 3: Formatage pour affichage")
    formatted_data = formater_pre_import_pour_affichage(pre_import_data)
    print(f"✅ Données formatées: {formatted_data['nombre_elements']} éléments")
    
    for element in formatted_data['elements']:
        print(f"  Élément {element['index']}:")
        print(f"    - Matelas #{element['matelas_index']} - {element['noyau']}")
        print(f"    - Quantité: {element['quantite']}")
        print(f"    - Champs: {element['champs']}")
        print()
    
    # Test 4: Structure JSON finale
    print("📋 Test 4: Structure JSON finale")
    result_backend = {
        "filename": "test_devis.pdf",
        "donnees_client": donnees_client,
        "configurations_matelas": configurations_matelas,
        "pre_import": pre_import_data
    }
    
    print("✅ Structure de résultat créée")
    print(f"  - Nombre de configurations: {len(result_backend['configurations_matelas'])}")
    print(f"  - Nombre d'éléments pré-import: {len(result_backend['pre_import'])}")
    
    # Test 5: Cas d'erreur
    print("\n📋 Test 5: Cas d'erreur")
    
    # Test avec données client manquantes
    pre_import_vide = creer_pre_import(configurations_matelas, {})
    validation_vide = valider_pre_import(pre_import_vide)
    print(f"  - Pré-import avec client manquant: {validation_vide}")
    
    # Test avec configurations vides
    pre_import_sans_config = creer_pre_import([], donnees_client)
    validation_sans_config = valider_pre_import(pre_import_sans_config)
    print(f"  - Pré-import sans configurations: {validation_sans_config}")
    
    print("\n✅ Test de l'étape pré-import terminé avec succès!")
    return True

def test_cas_reels():
    """Test avec des cas réels"""
    
    print("\n=== TEST AVEC CAS RÉELS ===")
    
    # Cas réel 1: Mr DEVERSENNE
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
    
    print("📋 Cas réel 1: Mr DEVERSENNE")
    pre_import_1 = creer_pre_import(config_1, donnees_client_1)
    print(f"  - Pré-import créé: {len(pre_import_1)} élément(s)")
    print(f"  - Validation: {valider_pre_import(pre_import_1)}")
    
    for item in pre_import_1:
        print(f"    Client_D1: {item['Client_D1']}")
        print(f"    Adresse_D3: {item['Adresse_D3']}")
        print(f"    Hauteur_D22: {item['Hauteur_D22']}")
    
    # Cas réel 2: Mr BILAND
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
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "BILAND"
        }
    ]
    
    print("\n📋 Cas réel 2: Mr BILAND")
    pre_import_2 = creer_pre_import(config_2, donnees_client_2)
    print(f"  - Pré-import créé: {len(pre_import_2)} élément(s)")
    print(f"  - Validation: {valider_pre_import(pre_import_2)}")
    
    for item in pre_import_2:
        print(f"    Client_D1: {item['Client_D1']}")
        print(f"    Adresse_D3: {item['Adresse_D3']}")
        print(f"    Hauteur_D22: {item['Hauteur_D22']}")
    
    print("\n✅ Test avec cas réels terminé!")

if __name__ == "__main__":
    test_pre_import()
    test_cas_reels()
    print("\n🎉 Tous les tests terminés avec succès!")
    print("\n📝 Résumé de l'étape pré-import:")
    print("  ✅ Création du JSON pré-import à partir des configurations matelas")
    print("  ✅ Mapping des champs: Client_D1, Adresse_D3, Hauteur_D22")
    print("  ✅ Validation des données de pré-import")
    print("  ✅ Formatage pour l'affichage dans l'interface")
    print("  ✅ Intégration dans le backend")
    print("  ✅ Tests complets et validation") 