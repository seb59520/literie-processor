#!/usr/bin/env python3

import sys
sys.path.append('backend')

from client_utils import extraire_donnees_client, extraire_ville_adresse, valider_donnees_client

def test_extraction_client():
    """Test de l'extraction des données client"""
    
    print("=== TEST EXTRACTION DONNÉES CLIENT ===")
    
    # Test 1: Données client complètes
    llm_data_1 = {
        "client": {
            "nom": "Mr LOUCHART FREDERIC",
            "adresse": "7 RUE DU MILIEU 59190 HAZEBROUCK",
            "code_client": "LOUCFSE"
        }
    }
    
    print("\n📋 Test 1: Données client complètes")
    resultat_1 = extraire_donnees_client(llm_data_1)
    print(f"Résultat: {resultat_1}")
    print(f"Validation: {valider_donnees_client(resultat_1)}")
    
    # Test 2: Adresse avec code postal différent
    llm_data_2 = {
        "client": {
            "nom": "Mr DEVERSENNE CLAUDE",
            "adresse": "81 MEULENSTRAETE 59270 SAINT JANS CAPPEL",
            "code_client": "DEVECLA"
        }
    }
    
    print("\n📋 Test 2: Adresse avec code postal différent")
    resultat_2 = extraire_donnees_client(llm_data_2)
    print(f"Résultat: {resultat_2}")
    print(f"Validation: {valider_donnees_client(resultat_2)}")
    
    # Test 3: Adresse sans code postal
    llm_data_3 = {
        "client": {
            "nom": "Mr TEST SANS CODE",
            "adresse": "123 RUE DE LA PAIX PARIS",
            "code_client": "TESTSAN"
        }
    }
    
    print("\n📋 Test 3: Adresse sans code postal")
    resultat_3 = extraire_donnees_client(llm_data_3)
    print(f"Résultat: {resultat_3}")
    print(f"Validation: {valider_donnees_client(resultat_3)}")
    
    # Test 4: Données client incomplètes
    llm_data_4 = {
        "client": {
            "nom": "Mr INCOMPLET",
            "adresse": "",
            "code_client": "INCOMP"
        }
    }
    
    print("\n📋 Test 4: Données client incomplètes")
    resultat_4 = extraire_donnees_client(llm_data_4)
    print(f"Résultat: {resultat_4}")
    print(f"Validation: {valider_donnees_client(resultat_4)}")
    
    # Test 5: Données client manquantes
    llm_data_5 = {}
    
    print("\n📋 Test 5: Données client manquantes")
    resultat_5 = extraire_donnees_client(llm_data_5)
    print(f"Résultat: {resultat_5}")
    print(f"Validation: {valider_donnees_client(resultat_5)}")
    
    # Test 6: Test direct de l'extraction de ville
    print("\n📋 Test 6: Extraction directe de ville")
    adresses_test = [
        "7 RUE DU MILIEU 59190 HAZEBROUCK",
        "81 MEULENSTRAETE 59270 SAINT JANS CAPPEL",
        "123 RUE DE LA PAIX 75001 PARIS",
        "456 AVENUE DES CHAMPS 69001 LYON",
        "789 BOULEVARD DE LA LIBERTE 13001 MARSEILLE",
        "123 RUE SANS CODE POSTAL PARIS"
    ]
    
    for adresse in adresses_test:
        ville = extraire_ville_adresse(adresse)
        print(f"Adresse: '{adresse}' -> Ville: '{ville}'")

def test_integration_complete():
    """Test d'intégration complète avec un JSON LLM réel"""
    
    print("\n=== TEST INTÉGRATION COMPLÈTE ===")
    
    # Simulation d'un JSON LLM complet
    llm_result_complet = {
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
            "nom": "Mr LOUCHART FREDERIC",
            "adresse": "7 RUE DU MILIEU 59190 HAZEBROUCK",
            "code_client": "LOUCFSE"
        },
        "commande": {
            "numero": "CM00009467",
            "date": "30/05/2025",
            "date_validite": None,
            "commercial": "P. ALINE",
            "origine": "www.literie-westelynck.fr"
        },
        "articles": [
            {
                "quantite": 1,
                "description": "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES MÉDIUM - HOUSSE MATELASSÉE TENCEL SIMPLE AVEC POIGNÉES OREILLES DÉHOUSSABLE SUR 2 CÔTÉS ET LAVABLE A 40°",
                "dimensions": "89/ 198/ 20",
                "pu_ttc": 577.50,
                "eco_part": 5.50,
                "pu_ht": 572.00
            }
        ],
        "paiement": {
            "conditions": "ACOMPTE DE 148.90 € EN CHÈQUE CA N°4522969 A LA COMMANDE ET SOLDE DE 400 € A L'ENLÈVEMENT",
            "port_ht": 0.00,
            "base_ht": 452.84,
            "taux_tva": 20.00,
            "total_ttc": 548.90,
            "acompte": 148.90,
            "net_a_payer": 400.00
        }
    }
    
    print("📋 Test avec JSON LLM complet")
    resultat_complet = extraire_donnees_client(llm_result_complet)
    print(f"Résultat: {resultat_complet}")
    print(f"Validation: {valider_donnees_client(resultat_complet)}")
    
    # Affichage détaillé
    print("\n📊 Détails de l'extraction:")
    print(f"  - Nom: {resultat_complet.get('nom', 'N/A')}")
    print(f"  - Adresse (ville): {resultat_complet.get('adresse', 'N/A')}")
    print(f"  - Code client: {resultat_complet.get('code_client', 'N/A')}")

if __name__ == "__main__":
    test_extraction_client()
    test_integration_complete()
    print("\n✅ Tests terminés avec succès!") 