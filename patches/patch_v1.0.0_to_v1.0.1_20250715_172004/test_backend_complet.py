#!/usr/bin/env python3

import sys
sys.path.append('backend')
import math
import json

# Simulation du JSON LLM valide
llm_result = """{
  "articles": [
    {
      "quantite": 1,
      "description": "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°",
      "dimensions": "139/ 189/ 20",
      "pu_ttc": 940.0,
      "eco_part": 11.0,
      "pu_ht": 929.0
    }
  ]
}"""

print("=== TEST BACKEND COMPLET ===")

# Étape 1: Parsing JSON
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

print(f"Articles totaux: {len(articles_llm)}")
print(f"Matelas détectés: {len(matelas_articles)}")

# Étape 3: Détection du noyau
from matelas_utils import detecter_noyau_matelas
noyaux_matelas = detecter_noyau_matelas(matelas_articles)
print(f"Noyaux détectés: {noyaux_matelas}")

# Étape 4: Calcul des configurations (simulation du backend)
from dimensions_utils import detecter_dimensions
from matiere_housse_utils import detecter_matiere_housse

configurations_matelas = []

for i, noyau_info in enumerate(noyaux_matelas):
    if noyau_info['noyau'] != 'INCONNU':
        # Trouver l'article correspondant
        quantite = 1
        description = ""
        if noyau_info['index'] <= len(matelas_articles):
            article_matelas = matelas_articles[noyau_info['index'] - 1]
            quantite = article_matelas.get('quantite', 1)
            description = article_matelas.get('description', '')
        
        dimensions_str = article_matelas.get('dimensions') if article_matelas else None
        if dimensions_str:
            dimensions = detecter_dimensions(dimensions_str)
        else:
            dimensions = detecter_dimensions(description)
        
        config = {
            "matelas_index": noyau_info['index'],
            "noyau": noyau_info['noyau'],
            "quantite": quantite,
            "dimensions": dimensions,
            "matiere_housse": detecter_matiere_housse(description)
        }
        
        # Calcul de la dimension literie (logique corrigée)
        dimension_literie = None
        if dimensions:
            largeur = dimensions["largeur"]
            longueur = dimensions["longueur"]
            largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
            longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
            
            if quantite == 2:
                largeur_literie = largeur_arrondie * 2
            else:
                largeur_literie = largeur_arrondie
                
            dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
            config["dimension_literie"] = dimension_literie
        
        configurations_matelas.append(config)

# Affichage des résultats
print(f"\nConfigurations calculées: {len(configurations_matelas)}")

for i, config in enumerate(configurations_matelas):
    print(f"\n--- Configuration {i+1} ---")
    print(f"Noyau: {config['noyau']}")
    print(f"Quantité: {config['quantite']}")
    print(f"Dimensions: {config['dimensions']}")
    print(f"Matière housse: {config['matiere_housse']}")
    print(f"Dimension literie: {config.get('dimension_literie', 'Non calculée')}")
    
    # Vérification
    if config.get('dimension_literie') == "140x190":
        print("✅ Dimension literie correcte !")
    else:
        print("❌ Dimension literie incorrecte")

print("\n✅ Test terminé !") 