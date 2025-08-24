#!/usr/bin/env python3

import sys
sys.path.append('backend')

# Simulation du JSON LLM pour le fichier THULLIER
llm_data = {
    "articles": [
        {
            "quantite": 2,
            "description": "MATELAS JUMEAUX - LATEX 100% NATUREL PERFORÉ 7 ZONES DIFFÉRENCIÉES FERME - HOUSSE MATELASSÉE TENCEL LUXE 3D LAVABLE A 40°",
            "dimensions": "89/ 198/ 22",
            "pu_ttc": 1733.00,
            "eco_part": 5.50,
            "pu_ht": 861.00
        }
    ]
}

print("=== TEST CORRECTION NOYAU ===")

# Test de la logique de filtrage des matelas (comme dans main.py)
print("\n=== TEST FILTRAGE MATELAS ===")
articles_llm = []
matelas_articles = []

for key in llm_data:
    if isinstance(llm_data[key], list):
        articles_llm.extend(llm_data[key])
        if key.lower() == "articles":
            for article in llm_data[key]:
                description = article.get('description', '').upper()
                print(f"Article: {description[:80]}...")
                print(f"  'MATELAS' in description: {'MATELAS' in description}")
                if 'MATELAS' in description:
                    matelas_articles.append(article)
                    print(f"  -> Matelas ajouté !")

print(f"\nArticles totaux: {len(articles_llm)}")
print(f"Matelas filtrés: {len(matelas_articles)}")

if matelas_articles:
    print(f"Description du premier matelas: {matelas_articles[0]['description']}")

# Test de détection du noyau
from matelas_utils import detecter_noyau_matelas, normalize_str
noyaux_matelas = detecter_noyau_matelas(matelas_articles)
print(f"Noyaux détectés: {noyaux_matelas}")

# Test détaillé de la fonction de détection
print("\n=== TEST DÉTAILLÉ DÉTECTION NOYAU ===")
for i, article in enumerate(matelas_articles):
    print(f"\nArticle {i+1}:")
    description = article.get('description', '')
    print(f"  Description originale: {description}")
    
    # Test de normalisation
    normalized = normalize_str(description)
    print(f"  Description normalisée: {normalized}")
    
    # Test des conditions une par une
    print(f"  'LATEX 100%' in desc: {'LATEX 100%' in normalized}")
    print(f"  '100% LATEX' in desc: {'100% LATEX' in normalized}")
    print(f"  'NATUREL' in desc: {'NATUREL' in normalized}")
    print(f"  Condition LATEX NATUREL: {('LATEX 100%' in normalized or '100% LATEX' in normalized) and 'NATUREL' in normalized}")
    
    # Test de la fonction complète
    result = detecter_noyau_matelas([article])
    print(f"  Résultat détection: {result[0]['noyau']}")

# Test du calcul de dimension_literie
print("\n=== TEST CALCUL DIMENSION LITERIE ===")
import math
from dimensions_utils import detecter_dimensions

dimensions_str = article.get('dimensions', '')
print(f"Dimensions string: {dimensions_str}")

if dimensions_str:
    dimensions = detecter_dimensions(dimensions_str)
    print(f"Dimensions détectées: {dimensions}")
    
    if dimensions:
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        quantite = article.get('quantite', 1)
        
        print(f"Largeur: {largeur}")
        print(f"Longueur: {longueur}")
        print(f"Quantité: {quantite}")
        
        largeur_arrondie = int(math.ceil(largeur / 10.0) * 10)
        longueur_arrondie = int(math.ceil(longueur / 10.0) * 10)
        
        print(f"Largeur arrondie: {largeur_arrondie}")
        print(f"Longueur arrondie: {longueur_arrondie}")
        
        if quantite == 2:
            largeur_literie = largeur_arrondie * 2
        else:
            largeur_literie = largeur_arrondie
            
        print(f"Largeur literie: {largeur_literie}")
        
        dimension_literie = f"{largeur_literie}x{longueur_arrondie}"
        print(f"Dimension literie calculée: {dimension_literie}")
    else:
        print("❌ Dimensions non détectées")
else:
    print("❌ Dimensions string vide")

# Debug de la normalisation
description = matelas_articles[0]['description']
normalized = normalize_str(description)
print(f"\nDescription originale: {description}")
print(f"Description normalisée: {normalized}")
print(f"'100% LATEX' in desc: {'100% LATEX' in normalized}")
print(f"'NATUREL' in desc: {'NATUREL' in normalized}")
print(f"'LATEX 100% PERFORE 7 ZONES' in desc: {'LATEX 100% PERFORE 7 ZONES' in normalized}")
print(f"'LATEX 100% PERFORÉ 7 ZONES' in desc: {'LATEX 100% PERFORÉ 7 ZONES' in normalized}")

# Test des calculs de dimensions housse
if noyaux_matelas and noyaux_matelas[0]['noyau'] == 'LATEX MIXTE 7 ZONES':
    print("\n✅ Correction réussie ! Le matelas est détecté comme LATEX MIXTE 7 ZONES")
    
    # Test des calculs de dimensions housse
    from dimensions_utils import detecter_dimensions
    from matiere_housse_utils import detecter_matiere_housse
    from latex_mixte7zones_referentiel import get_valeur_latex_mixte7zones
    from latex_mixte7zones_longueur_housse_utils import get_latex_mixte7zones_longueur_housse_value
    
    article = matelas_articles[0]
    description = article.get('description', '')
    dimensions_str = article.get('dimensions')
    
    if dimensions_str:
        dimensions = detecter_dimensions(dimensions_str)
        matiere_housse = detecter_matiere_housse(description)
        
        print(f"Dimensions: {dimensions}")
        print(f"Matière housse: {matiere_housse}")
        
        if dimensions and matiere_housse:
            try:
                # Calcul dimension housse largeur
                valeur_largeur = get_valeur_latex_mixte7zones(dimensions["largeur"], matiere_housse)
                print(f"Dimension housse largeur: {valeur_largeur}")
                
                # Calcul dimension housse longueur
                valeur_longueur = get_latex_mixte7zones_longueur_housse_value(dimensions["longueur"], matiere_housse)
                print(f"Dimension housse longueur: {valeur_longueur}")
                
                print("✅ Calculs de dimensions housse réussis !")
            except Exception as e:
                print(f"❌ Erreur dans les calculs: {e}")
        else:
            print("❌ Dimensions ou matière housse non détectées")
    else:
        print("❌ Dimensions non trouvées")
else:
    print("❌ Le matelas n'est pas détecté comme LATEX MIXTE 7 ZONES")

print("\n✅ Test terminé !") 