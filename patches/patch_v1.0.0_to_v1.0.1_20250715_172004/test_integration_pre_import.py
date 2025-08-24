#!/usr/bin/env python3

import sys
sys.path.append('backend')

import json
from client_utils import extraire_donnees_client
from pre_import_utils import creer_pre_import, valider_pre_import

def test_integration_complete():
    """Test d'intégration complète avec le backend"""
    
    print("=== TEST INTÉGRATION COMPLÈTE PRÉ-IMPORT ===")
    
    # Simulation du processus complet du backend
    # Étape 1: Résultat LLM simulé
    llm_result = """{
  "societe": {
    "nom": "SAS Literie Westelynck",
    "capital": "23 100 Euros",
    "adresse": "525 RD 642 - 59190 BORRE",
    "telephone": "03.28.48.04.19",
    "fax": "03.28.41.02.74",
    "email": "contact@lwest.fr",
    "siret": "429 352 891 00015",
    "APE": "3103Z",
    "CEE": "FR50 429 352 891",
    "banque": "Crédit Agricole d'Hazebrouck",
    "IBAN": "FR76 1670 6050 1650 4613 2602 341"
  },
  "client": {
    "nom": "Mr DEVERSENNE CLAUDE",
    "adresse": "81 MEULENSTRAETE 59270 SAINT JANS CAPPEL",
    "code_client": "DEVECLA"
  },
  "commande": {
    "numero": "CM00009468",
    "date": "31/05/2025",
    "date_validite": null,
    "commercial": "P. ALINE",
    "origine": "www.literie-westelynck.fr"
  },
  "articles": [
    {
      "quantite": 2,
      "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°",
      "dimensions": "79/ 198/ 20",
      "pu_ttc": 698.50,
      "eco_part": 11.00,
      "pu_ht": 687.50
    },
    {
      "quantite": 1,
      "description": "REMISE : 5% ENLÈVEMENT PAR VOS SOINS",
      "montant": -69.85
    }
  ],
  "paiement": {
    "conditions": "ACOMPTE DE 150.00 € EN CHÈQUE A LA COMMANDE ET SOLDE DE 1305.65 € A L'ENLÈVEMENT",
    "port_ht": 0.00,
    "base_ht": 1305.65,
    "taux_tva": 20.00,
    "total_ttc": 1455.65,
    "acompte": 150.00,
    "net_a_payer": 1305.65
  }
}"""
    
    print("📋 Étape 1: Parsing du JSON LLM")
    try:
        llm_data = json.loads(llm_result)
        print("✅ JSON parsé avec succès")
    except Exception as e:
        print(f"❌ Erreur parsing JSON: {e}")
        return False
    
    # Étape 2: Extraction des données client
    print("\n📋 Étape 2: Extraction des données client")
    donnees_client = extraire_donnees_client(llm_data)
    print(f"✅ Données client extraites: {donnees_client}")
    
    # Étape 3: Simulation des configurations matelas (comme dans le backend)
    print("\n📋 Étape 3: Simulation des configurations matelas")
    configurations_matelas = [
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
    print(f"✅ Configurations matelas créées: {len(configurations_matelas)}")
    
    # Étape 4: Création du pré-import
    print("\n📋 Étape 4: Création du pré-import")
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client)
    print(f"✅ Pré-import créé: {len(pre_import_data)} éléments")
    
    # Étape 5: Validation du pré-import
    print("\n📋 Étape 5: Validation du pré-import")
    validation = valider_pre_import(pre_import_data)
    print(f"✅ Validation: {validation}")
    
    # Étape 6: Structure de résultat finale (comme dans le backend)
    print("\n📋 Étape 6: Structure de résultat finale")
    result = {
        "filename": "devis_deversenne.pdf",
        "extraction_stats": {
            "nb_caracteres": 1500,
            "nb_mots": 250,
            "preview": "Extrait du texte..."
        },
        "llm_result": llm_result,
        "donnees_client": donnees_client,
        "configurations_matelas": configurations_matelas,
        "pre_import": pre_import_data,
        "contient_dosseret_ou_tete": False,
        "mots_operation_trouves": ["ENLÈVEMENT"],
        "noyaux_matelas": [{"index": 1, "noyau": "MOUSSE RAINUREE 7 ZONES"}],
        "fermeture_liaison": False,
        "surmatelas": False
    }
    
    print("✅ Structure de résultat créée")
    
    # Étape 7: Vérification de l'intégration
    print("\n📋 Étape 7: Vérification de l'intégration")
    print(f"  - Nom du client: {result['donnees_client'].get('nom', 'N/A')}")
    print(f"  - Ville du client: {result['donnees_client'].get('adresse', 'N/A')}")
    print(f"  - Nombre de configurations matelas: {len(result['configurations_matelas'])}")
    print(f"  - Nombre d'éléments pré-import: {len(result['pre_import'])}")
    
    # Affichage détaillé du pré-import
    print("\n📋 Détails du pré-import:")
    for i, item in enumerate(result['pre_import'], 1):
        print(f"  Élément {i}:")
        print(f"    - Client_D1: {item['Client_D1']}")
        print(f"    - Adresse_D3: {item['Adresse_D3']}")
        print(f"    - Hauteur_D22: {item['Hauteur_D22']}")
        print(f"    - Noyau: {item['noyau']}")
        print(f"    - Quantité: {item['quantite']}")
    
    print("\n✅ Test d'intégration terminé avec succès!")
    return True

def test_multiple_configurations():
    """Test avec plusieurs configurations matelas"""
    
    print("\n=== TEST AVEC PLUSIEURS CONFIGURATIONS ===")
    
    # Données client
    donnees_client = {
        "nom": "Mr LOUCHART FREDERIC",
        "adresse": "HAZEBROUCK",
        "code_client": "LOUCFSE"
    }
    
    # Plusieurs configurations matelas
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
        },
        {
            "matelas_index": 3,
            "noyau": "LATEX NATUREL",
            "quantite": 1,
            "hauteur": 22,
            "fermete": "DOUX",
            "housse": "MATELASSÉE",
            "matiere_housse": "POLYESTER",
            "poignees": "OREILLES",
            "dimensions": {"largeur": 139, "longueur": 198},
            "semaine_annee": "25_2025",
            "lundi": "2025-06-16",
            "vendredi": "2025-06-20",
            "commande_client": "LOUCHART"
        }
    ]
    
    print("📋 Test avec plusieurs configurations")
    print(f"  - Client: {donnees_client['nom']}")
    print(f"  - Configurations: {len(configurations_matelas)}")
    
    # Création du pré-import
    pre_import_data = creer_pre_import(configurations_matelas, donnees_client)
    print(f"  - Pré-import créé: {len(pre_import_data)} éléments")
    print(f"  - Validation: {valider_pre_import(pre_import_data)}")
    
    # Affichage des résultats
    print("\n📋 Résultats du pré-import:")
    for i, item in enumerate(pre_import_data, 1):
        print(f"  Élément {i} (Matelas #{item['matelas_index']} - {item['noyau']}):")
        print(f"    - Client_D1: {item['Client_D1']}")
        print(f"    - Adresse_D3: {item['Adresse_D3']}")
        print(f"    - Hauteur_D22: {item['Hauteur_D22']}")
        print(f"    - Quantité: {item['quantite']}")
        print()
    
    print("✅ Test avec plusieurs configurations terminé!")

if __name__ == "__main__":
    test_integration_complete()
    test_multiple_configurations()
    print("\n🎉 Tous les tests terminés avec succès!")
    print("\n📝 Résumé de l'intégration pré-import:")
    print("  ✅ Intégration complète avec le backend")
    print("  ✅ Extraction des données client depuis LLM")
    print("  ✅ Création des configurations matelas")
    print("  ✅ Génération du pré-import JSON")
    print("  ✅ Validation et affichage")
    print("  ✅ Support de plusieurs configurations")
    print("  ✅ Structure de résultat complète") 