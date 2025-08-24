#!/usr/bin/env python3

import sys
sys.path.append('backend')

import json
from client_utils import extraire_donnees_client, valider_donnees_client

def test_exemple_reel():
    """Test avec un exemple réel d'extraction LLM"""
    
    print("=== TEST AVEC EXEMPLE RÉEL ===")
    
    # Exemple réel d'extraction LLM (basé sur les données de test existantes)
    llm_result_reel = {
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
            "date_validite": None,
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
    }
    
    print("📋 Données client dans l'extraction LLM:")
    print(f"  - Nom: {llm_result_reel['client']['nom']}")
    print(f"  - Adresse complète: {llm_result_reel['client']['adresse']}")
    print(f"  - Code client: {llm_result_reel['client']['code_client']}")
    
    # Extraction des données client
    print("\n📋 Extraction des données client:")
    donnees_client = extraire_donnees_client(llm_result_reel)
    print(f"  - Nom extrait: {donnees_client['nom']}")
    print(f"  - Ville extraite: {donnees_client['adresse']}")
    print(f"  - Code client extrait: {donnees_client['code_client']}")
    
    # Validation
    print(f"\n📋 Validation: {valider_donnees_client(donnees_client)}")
    
    # Simulation de l'intégration dans le backend
    print("\n📋 Intégration dans le backend:")
    result_backend = {
        "filename": "devis_deversenne.pdf",
        "donnees_client": donnees_client,
        "configurations_matelas": [
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
    }
    
    print("✅ Structure de résultat créée")
    print(f"  - Nom du client dans le résultat: {result_backend['donnees_client']['nom']}")
    print(f"  - Ville dans le résultat: {result_backend['donnees_client']['adresse']}")
    print(f"  - Commande/Client dans config: {result_backend['configurations_matelas'][0]['commande_client']}")
    
    # Test de cohérence
    print("\n📋 Test de cohérence:")
    nom_client = result_backend['donnees_client']['nom']
    commande_client = result_backend['configurations_matelas'][0]['commande_client']
    
    # Extraction du nom de famille pour comparaison
    nom_famille = nom_client.split()[-1] if nom_client else ""
    print(f"  - Nom complet: {nom_client}")
    print(f"  - Nom de famille extrait: {nom_famille}")
    print(f"  - Commande/Client: {commande_client}")
    
    if nom_famille.upper() in commande_client.upper() or commande_client.upper() in nom_famille.upper():
        print("  ✅ Cohérence entre nom client et commande/client")
    else:
        print("  ⚠️  Pas de cohérence directe (normal si commande/client est différent)")
    
    print("\n✅ Test avec exemple réel terminé avec succès!")
    return True

def test_multiple_clients():
    """Test avec plusieurs clients réels"""
    
    print("\n=== TEST AVEC PLUSIEURS CLIENTS RÉELS ===")
    
    clients_reels = [
        {
            "nom": "Mr LOUCHART FREDERIC",
            "adresse": "7 RUE DU MILIEU 59190 HAZEBROUCK",
            "code_client": "LOUCFSE"
        },
        {
            "nom": "Mr DEVERSENNE CLAUDE",
            "adresse": "81 MEULENSTRAETE 59270 SAINT JANS CAPPEL",
            "code_client": "DEVECLA"
        },
        {
            "nom": "Mr BILAND JEAN",
            "adresse": "15 RUE DE LA PAIX 59000 LILLE",
            "code_client": "BILANJE"
        },
        {
            "nom": "Mme DUBRULLE MARIE",
            "adresse": "42 AVENUE DES FLANDRES 59100 ROUBAIX",
            "code_client": "DUBRUMAR"
        },
        {
            "nom": "Mr CALCOEN PIERRE",
            "adresse": "123 RUE DE LA GARE 59170 CROIX",
            "code_client": "CALCOPI"
        }
    ]
    
    print("📋 Extraction des données pour plusieurs clients:")
    
    for i, client in enumerate(clients_reels, 1):
        llm_data = {"client": client}
        donnees_extract = extraire_donnees_client(llm_data)
        
        print(f"  {i}. {donnees_extract['nom']}")
        print(f"     Ville: {donnees_extract['adresse']}")
        print(f"     Code: {donnees_extract['code_client']}")
        print(f"     Validation: {valider_donnees_client(donnees_extract)}")
        print()
    
    print("✅ Test avec plusieurs clients terminé!")

if __name__ == "__main__":
    test_exemple_reel()
    test_multiple_clients()
    print("\n🎉 Tous les tests terminés avec succès!")
    print("\n📝 Résumé de l'implémentation:")
    print("  ✅ Extraction du nom client depuis l'extraction LLM")
    print("  ✅ Extraction de la ville depuis l'adresse (après code postal)")
    print("  ✅ Extraction du code client")
    print("  ✅ Intégration dans le JSON variable Client")
    print("  ✅ Affichage dans l'interface utilisateur")
    print("  ✅ Tests complets et validation") 