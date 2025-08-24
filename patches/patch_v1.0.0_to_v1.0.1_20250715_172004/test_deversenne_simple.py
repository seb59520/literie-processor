#!/usr/bin/env python3
"""
Test simple pour la commande Deversenne
"""

import sys
import os
import json
sys.path.append('backend')

from main import call_openrouter
from client_utils import extraire_donnees_client
from matelas_utils import detecter_noyau_matelas
from pre_import_utils import creer_pre_import
from article_utils import contient_dosseret_ou_tete
from operation_utils import mots_operation_trouves

def test_deversenne_simple():
    """Test simple du traitement de la commande Deversenne"""
    
    # Données LLM simulées pour Deversenne
    llm_data = {
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
            "code_client": "DEVECSA"
        },
        "commande": {
            "numero": "CM00009480",
            "date": "06/06/2025",
            "date_validite": None,
            "commercial": "M. QUENTIN",
            "origine": "Devis N° DE00005520 du 06/ 06/ 2025"
        },
        "articles": [
            {
                "quantite": 2,
                "description": "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40°",
                "dimensions": "79/ 198/ 20",
                "pu_ttc": 518.00,
                "eco_part": 0.00,
                "pu_ht": None
            },
            {
                "quantite": 1,
                "description": "REMISE : 5% ENLÈVEMENT PAR VOS SOINS",
                "montant": -50.00
            }
        ],
        "paiement": {
            "conditions": "25% D ACOMPTE 75% A L ENLEVEMENT",
            "port_ht": 0.00,
            "base_ht": 821.66,
            "taux_tva": 20.00,
            "total_ttc": 986.00,
            "acompte": 986.00,
            "net_a_payer": 0.00
        }
    }
    
    print("=== Test simple Deversenne ===")
    
    try:
        # Extraction des données client
        donnees_client = extraire_donnees_client(llm_data)
        print(f"✅ Données client extraites: {donnees_client}")
        
        # Extraction des articles matelas
        articles_llm = llm_data.get("articles", [])
        matelas_articles = []
        for article in articles_llm:
            description = article.get('description', '').upper()
            if 'MATELAS' in description:
                matelas_articles.append(article)
        
        print(f"✅ Articles matelas trouvés: {len(matelas_articles)}")
        
        # Détection des noyaux
        noyaux_matelas = detecter_noyau_matelas(matelas_articles)
        print(f"✅ Noyaux détectés: {noyaux_matelas}")
        
        # Création des configurations (simplifiée)
        configurations_matelas = []
        for i, noyau in enumerate(noyaux_matelas):
            config = {
                "matelas_index": i + 1,
                "noyau": noyau.get("noyau", ""),
                "quantite": noyau.get("quantite", 1),
                "hauteur": 9,  # Valeur par défaut
                "fermete": "FERME",  # Détecté dans la description
                "housse": "MATELASSEE",
                "matiere_housse": "TENCEL LUXE 3D",
                "poignees": "OUI",
                "dimensions": {
                    "largeur": 79.0,
                    "longueur": 198.0,
                    "hauteur": 20.0
                },
                "semaine_annee": "6_2025",
                "lundi": "2025-02-10",
                "vendredi": "2025-02-14",
                "commande_client": "75",
                "dimension_housse_longueur": 5.5,
                "dimension_housse": "4 x 91",
                "dimension_literie": "160x200",
                "decoupe_noyau": "79.0 x 198.0"
            }
            configurations_matelas.append(config)
        
        print(f"✅ Configurations créées: {len(configurations_matelas)}")
        
        # Détection des opérations
        contient_dosseret_tete = contient_dosseret_ou_tete(articles_llm)
        mots_operation_list = mots_operation_trouves(articles_llm)
        
        print(f"✅ Dossert/tête: {contient_dosseret_tete}")
        print(f"✅ Mots opération: {mots_operation_list}")
        
        # Création du pré-import
        pre_import_data = creer_pre_import(
            configurations_matelas, donnees_client, 
            contient_dosseret_tete, mots_operation_list
        )
        
        if pre_import_data:
            config = pre_import_data[0]
            
            print(f"\n--- Configuration détectée ---")
            print(f"Noyau: {configurations_matelas[0].get('noyau', 'N/A')}")
            print(f"Fermeté: {configurations_matelas[0].get('fermete', 'N/A')}")
            print(f"Quantité: {configurations_matelas[0].get('quantite', 'N/A')}")
            
            print(f"\n--- Cases cochées ---")
            print(f"MR_Ferme_C37: '{config.get('MR_Ferme_C37', 'VIDE')}'")
            print(f"MR_Medium_C38: '{config.get('MR_Medium_C38', 'VIDE')}'")
            print(f"MR_Confort_C39: '{config.get('MR_Confort_C39', 'VIDE')}'")
            print(f"Hmat_luxe3D_C19: '{config.get('Hmat_luxe3D_C19', 'VIDE')}'")
            print(f"poignees_C20: '{config.get('poignees_C20', 'VIDE')}'")
            print(f"jumeaux_C10: '{config.get('jumeaux_C10', 'VIDE')}'")
            print(f"emporte_client_C57: '{config.get('emporte_client_C57', 'VIDE')}'")
            
            if config.get('MR_Ferme_C37') == 'X':
                print("\n✅ SUCCÈS: MR_Ferme_C37 est correctement coché")
            else:
                print("\n❌ ÉCHEC: MR_Ferme_C37 n'est pas coché")
                
        else:
            print("❌ ÉCHEC: Aucun pré-import généré")
            
    except Exception as e:
        print(f"❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test terminé ===")

if __name__ == "__main__":
    test_deversenne_simple() 