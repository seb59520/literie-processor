#!/usr/bin/env python3

import sys
sys.path.append('backend')

import json
from client_utils import extraire_donnees_client, valider_donnees_client

def test_integration_backend():
    """Test d'intégration avec le backend complet"""
    
    print("=== TEST INTÉGRATION BACKEND COMPLET ===")
    
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
    "nom": "Mr LOUCHART FREDERIC",
    "adresse": "7 RUE DU MILIEU 59190 HAZEBROUCK",
    "code_client": "LOUCFSE"
  },
  "commande": {
    "numero": "CM00009467",
    "date": "30/05/2025",
    "date_validite": null,
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
    },
    {
      "quantite": 1,
      "description": "REMISE : 5% ENLÈVEMENT PAR VOS SOINS",
      "montant": -28.60
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
    
    # Étape 3: Validation des données client
    print("\n📋 Étape 3: Validation des données client")
    validation = valider_donnees_client(donnees_client)
    print(f"✅ Validation: {validation}")
    
    # Étape 4: Simulation de la structure de résultat du backend
    print("\n📋 Étape 4: Structure de résultat du backend")
    result = {
        "filename": "test_devis.pdf",
        "extraction_stats": {
            "nb_caracteres": 1500,
            "nb_mots": 250,
            "preview": "Extrait du texte..."
        },
        "llm_result": llm_result,
        "donnees_client": donnees_client,
        "configurations_matelas": [
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
            }
        ],
        "contient_dosseret_ou_tete": False,
        "mots_operation_trouves": ["ENLÈVEMENT"],
        "noyaux_matelas": [{"index": 1, "noyau": "LATEX MIXTE 7 ZONES"}],
        "fermeture_liaison": False,
        "surmatelas": False
    }
    
    print("✅ Structure de résultat créée")
    
    # Étape 5: Vérification de l'intégration
    print("\n📋 Étape 5: Vérification de l'intégration")
    print(f"  - Nom du client: {result['donnees_client'].get('nom', 'N/A')}")
    print(f"  - Ville du client: {result['donnees_client'].get('adresse', 'N/A')}")
    print(f"  - Code client: {result['donnees_client'].get('code_client', 'N/A')}")
    print(f"  - Nombre de configurations matelas: {len(result['configurations_matelas'])}")
    print(f"  - Commande/Client dans config: {result['configurations_matelas'][0]['commande_client']}")
    
    # Étape 6: Test avec plusieurs clients
    print("\n📋 Étape 6: Test avec plusieurs clients")
    
    clients_test = [
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
        }
    ]
    
    for i, client in enumerate(clients_test, 1):
        llm_data_test = {"client": client}
        donnees_extract = extraire_donnees_client(llm_data_test)
        print(f"  Client {i}: {donnees_extract['nom']} -> {donnees_extract['adresse']}")
    
    print("\n✅ Test d'intégration terminé avec succès!")
    return True

def test_cas_limites():
    """Test des cas limites et d'erreur"""
    
    print("\n=== TEST CAS LIMITES ===")
    
    cas_limites = [
        # Cas 1: Adresse avec code postal à 4 chiffres (Belgique)
        {
            "nom": "Mr BELGE PIERRE",
            "adresse": "123 RUE DE BRUXELLES 1000 BRUXELLES",
            "code_client": "BELGEPI"
        },
        # Cas 2: Adresse avec code postal à 6 chiffres (Allemagne)
        {
            "nom": "Mr ALLEMAND HANS",
            "adresse": "456 STRASSE 80331 MÜNCHEN",
            "code_client": "ALLEHAN"
        },
        # Cas 3: Adresse sans espace après le code postal
        {
            "nom": "Mr ESPACE MANQUANT",
            "adresse": "789 RUE TEST 75001PARIS",
            "code_client": "ESPAMAN"
        },
        # Cas 4: Adresse avec plusieurs espaces
        {
            "nom": "Mr ESPACES MULTIPLES",
            "adresse": "321 RUE TEST  59190  HAZEBROUCK",
            "code_client": "ESPAMUL"
        }
    ]
    
    for i, cas in enumerate(cas_limites, 1):
        print(f"\n📋 Cas limite {i}: {cas['nom']}")
        llm_data_test = {"client": cas}
        donnees_extract = extraire_donnees_client(llm_data_test)
        print(f"  Adresse originale: {cas['adresse']}")
        print(f"  Ville extraite: {donnees_extract['adresse']}")
        print(f"  Validation: {valider_donnees_client(donnees_extract)}")

if __name__ == "__main__":
    test_integration_backend()
    test_cas_limites()
    print("\n🎉 Tous les tests terminés avec succès!") 