#!/usr/bin/env python3

import sys
sys.path.append('backend')

# Simulation du processus complet
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

print("=== TEST PROCESSUS COMPLET ===")

# Étape 1: Parsing JSON
import json
try:
    llm_data = json.loads(llm_result)
    print("✅ JSON parsé avec succès")
except Exception as e:
    print(f"❌ Erreur parsing JSON: {e}")
    exit(1)

# Étape 2: Extraction des articles
articles_llm = []
matelas_articles = []
conditions_paiement = []

for key in llm_data:
    if isinstance(llm_data[key], list):
        articles_llm.extend(llm_data[key])
        if key.lower() == "articles":
            for article in llm_data[key]:
                description = article.get('description', '').upper()
                if 'MATELAS' in description:
                    matelas_articles.append(article)
    elif key == "paiement" and isinstance(llm_data[key], dict):
        conditions_paiement.append(llm_data[key])

print(f"Articles totaux: {len(articles_llm)}")
print(f"Matelas détectés: {len(matelas_articles)}")
print(f"Conditions paiement: {len(conditions_paiement)}")

# Étape 3: Détection des noyaux
from matelas_utils import detecter_noyau_matelas
noyaux_matelas = detecter_noyau_matelas(matelas_articles)
print(f"Noyaux détectés: {noyaux_matelas}")

# Étape 4: Création des configurations
if noyaux_matelas:
    print("\n=== CONFIGURATIONS MATELAS ===")
    for i, noyau_info in enumerate(noyaux_matelas):
        if noyau_info['noyau'] != 'INCONNU':
            article_matelas = matelas_articles[noyau_info['index'] - 1]
            quantite = article_matelas.get('quantite', 1)
            description = article_matelas.get('description', '')
            
            print(f"Matelas {i+1}:")
            print(f"  Noyau: {noyau_info['noyau']}")
            print(f"  Quantité: {quantite}")
            print(f"  Description: {description[:80]}...")
            
            # Test des dimensions
            from dimensions_utils import detecter_dimensions
            dimensions_str = article_matelas.get('dimensions')
            if dimensions_str:
                dimensions = detecter_dimensions(dimensions_str)
                print(f"  Dimensions: {dimensions}")
                
                # Test de la matière housse
                from matiere_housse_utils import detecter_matiere_housse
                matiere_housse = detecter_matiere_housse(description)
                print(f"  Matière housse: {matiere_housse}")
                
                # Test de la longueur housse
                if noyau_info['noyau'] == 'LATEX NATUREL':
                    from latex_naturel_longueur_housse_utils import get_latex_naturel_longueur_housse_value
                    longueur_housse = get_latex_naturel_longueur_housse_value(dimensions["longueur"], matiere_housse)
                    print(f"  Longueur housse: {longueur_housse}")
else:
    print("❌ Aucun noyau détecté")

print("\n✅ Test terminé !") 