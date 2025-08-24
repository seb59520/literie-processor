#!/usr/bin/env python3

import sys
sys.path.append('backend')
import math

# Simulation du JSON LLM pour tester la dimension literie
llm_data = {
    "articles": [
        {
            "quantite": 1,
            "description": "MATELAS 1 PIÈCE - 100% LATEX PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°",
            "dimensions": "139/ 189/ 20",
            "pu_ttc": 940.0,
            "eco_part": 11.0,
            "pu_ht": 929.0
        },
        {
            "quantite": 2,
            "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
            "dimensions": "89/ 198/ 22",
            "pu_ttc": 1733.0,
            "eco_part": 5.5,
            "pu_ht": 861.0
        }
    ]
}

print("=== TEST DIMENSION LITERIE BACKEND ===")

# Test de la logique de traitement
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

print(f"Matelas détectés: {len(matelas_articles)}")

# Test de détection du noyau
from matelas_utils import detecter_noyau_matelas
noyaux_matelas = detecter_noyau_matelas(matelas_articles)
print(f"Noyaux détectés: {noyaux_matelas}")

# Test des calculs de dimensions literie
from dimensions_utils import detecter_dimensions

for i, article in enumerate(matelas_articles):
    print(f"\n--- Matelas {i+1} ---")
    description = article.get('description', '')
    quantite = article.get('quantite', 1)
    dimensions_str = article.get('dimensions')
    
    print(f"Description: {description[:80]}...")
    print(f"Quantité: {quantite}")
    print(f"Dimensions: {dimensions_str}")
    
    if dimensions_str:
        dimensions = detecter_dimensions(dimensions_str)
        print(f"Dimensions parsées: {dimensions}")
        
        if dimensions:
            largeur = dimensions["largeur"]
            longueur = dimensions["longueur"]
            
            # Calcul selon la logique corrigée
            largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
            longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
            
            if quantite == 2:
                largeur_literie = largeur_arrondie * 2
            else:
                largeur_literie = largeur_arrondie
                
            dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
            
            print(f"Largeur originale: {largeur} -> arrondie: {largeur_arrondie}")
            print(f"Longueur originale: {longueur} -> arrondie: {longueur_arrondie}")
            print(f"Largeur literie (avec quantité): {largeur_literie}")
            print(f"Dimension literie finale: {dimension_literie}")
            
            # Vérification des valeurs attendues
            if i == 0:  # Premier matelas: 139x189, qte 1
                expected = "140x190"
            else:  # Deuxième matelas: 89x198, qte 2
                expected = "180x200"
                
            success = dimension_literie == expected
            status = "✅" if success else "❌"
            print(f"Résultat: {dimension_literie} {status}")
            if not success:
                print(f"Attendu: {expected}")

print("\n✅ Test terminé !") 