#!/usr/bin/env python3

import sys
sys.path.append('backend')

from matelas_utils import detecter_noyau_matelas, normalize_str

# Test avec le cas réel
matelas_articles = [
    {
        "quantite": 1,
        "description": "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°",
        "dimensions": "139/ 189/ 20",
        "pu_ttc": 940.0,
        "eco_part": 11.0,
        "pu_ht": 929.0
    }
]

print("=== TEST DÉTECTION NOYAU ===")

# Test de normalisation
description = matelas_articles[0]['description']
normalized = normalize_str(description)
print(f"Description originale: {description[:100]}...")
print(f"Description normalisée: {normalized[:100]}...")

# Test des conditions
print("\n=== TEST CONDITIONS ===")
print(f"'LATEX 100% NATUREL PERFORE 7 ZONES' in desc: {'LATEX 100% NATUREL PERFORE 7 ZONES' in normalized}")
print(f"'LATEX 100% NATUREL PERFORÉ 7 ZONES' in desc: {'LATEX 100% NATUREL PERFORÉ 7 ZONES' in normalized}")
print(f"'100% LATEX PERFORE 7 ZONES' in desc: {'100% LATEX PERFORE 7 ZONES' in normalized}")
print(f"'100% LATEX PERFORÉ 7 ZONES' in desc: {'100% LATEX PERFORÉ 7 ZONES' in normalized}")
print(f"'100% LATEX' in desc: {'100% LATEX' in normalized}")

# Test de détection complète
print("\n=== TEST DÉTECTION COMPLÈTE ===")
result = detecter_noyau_matelas(matelas_articles)
print(f"Résultat: {result}")

# Test avec différents types de noyaux
print("\n=== TEST DIFFÉRENTS TYPES ===")
test_cases = [
    "MATELAS 100% LATEX NATUREL",
    "MATELAS LATEX MIXTE 7 ZONES",
    "MATELAS MOUSSE RAINUREE 7 ZONES",
    "MATELAS LATEX RENFORCE",
    "MATELAS SELECT 43",
    "MATELAS MOUSSE VISCO",
    "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES MÉDIUM",
    "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME",
    "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME"
]

for test_case in test_cases:
    test_article = {"description": test_case}
    result = detecter_noyau_matelas([test_article])
    print(f"'{test_case[:50]}...' -> {result[0]['noyau']}")

print("\n✅ Test terminé !") 