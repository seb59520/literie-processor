#!/usr/bin/env python3

import sys
sys.path.append('backend')

# Test avec le cas réel
llm_data = {
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
    ]
}

print("=== TEST DÉTECTION MATELAS ===")

# Test de l'ancienne logique
print("Ancienne logique (startswith):")
for article in llm_data["articles"]:
    description = article.get('description', '').upper()
    is_matelas_old = description.startswith('MATELAS')
    print(f"  '{description[:50]}...' -> {is_matelas_old}")

# Test de la nouvelle logique
print("\nNouvelle logique (in):")
for article in llm_data["articles"]:
    description = article.get('description', '').upper()
    is_matelas_new = 'MATELAS' in description
    print(f"  '{description[:50]}...' -> {is_matelas_new}")

# Test complet
print("\n=== TEST COMPLET ===")
articles_llm = []
matelas_articles = []

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

for i, matelas in enumerate(matelas_articles):
    print(f"Matelas {i+1}: {matelas['description'][:80]}...")

print("\n✅ Test terminé !") 