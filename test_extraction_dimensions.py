#!/usr/bin/env python3
"""
Test de l'extraction des dimensions depuis le PDF
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from dimensions_utils import detecter_dimensions

def detecter_noyau_simple(description):
    """Version simplifiée de détection de noyau"""
    desc = description.upper()
    
    if "LATEX NATUREL" in desc or "100% LATEX" in desc:
        return "LATEX NATUREL"
    elif "LATEX MIXTE 7 ZONES" in desc:
        return "LATEX MIXTE 7 ZONES"
    elif "MOUSSE RAINUREE 7 ZONES" in desc or "MOUSSE RAINURÉE 7 ZONES" in desc:
        return "MOUSSE RAINUREE 7 ZONES"
    elif "LATEX RENFORCE" in desc:
        return "LATEX RENFORCE"
    elif "SELECT 43" in desc:
        return "SELECT 43"
    elif "MOUSSE VISCO" in desc:
        return "MOUSSE VISCO"
    else:
        return "INCONNU"

def detecter_matiere_housse_simple(description):
    """Version simplifiée de détection de matière housse"""
    desc = description.upper()
    
    if "TENCEL LUXE 3D" in desc:
        return "TENCEL LUXE 3D"
    elif "TENCEL" in desc:
        return "TENCEL"
    elif "POLYESTER" in desc:
        return "POLYESTER"
    elif "COTON" in desc:
        return "COTON"
    else:
        return "INCONNUE"

def test_extraction_dimensions():
    """Test de l'extraction des dimensions"""
    
    print("=== TEST EXTRACTION DIMENSIONS ===")
    
    # 1. Test des formats de dimensions
    print("\n📋 1. Test des formats de dimensions:")
    
    test_descriptions = [
        "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES 89/198/20",
        "MATELAS JUMEAUX - LATEX NATUREL 160x200",
        "MATELAS SELECT 43 - 140 / 190 / 18",
        "MATELAS MOUSSE VISCO - 90 x 200 x 15",
        "MATELAS LATEX RENFORCE - 180/200",
        "MATELAS 7 ZONES - 160x200x20",
        "MATELAS STANDARD - 90 / 200",
        "MATELAS PREMIUM - 140x190x18"
    ]
    
    for desc in test_descriptions:
        dimensions = detecter_dimensions(desc)
        if dimensions:
            print(f"   ✅ '{desc}' → {dimensions}")
        else:
            print(f"   ❌ '{desc}' → Aucune dimension détectée")
    
    # 2. Test de détection des noyaux
    print("\n📋 2. Test de détection des noyaux:")
    
    noyau_tests = [
        "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME",
        "MATELAS JUMEAUX - LATEX 100% NATUREL",
        "MATELAS SELECT 43 - MOUSSE VISCOELASTIQUE",
        "MATELAS LATEX RENFORCE - NATUREL",
        "MATELAS STANDARD - MOUSSE ORTHOPÉDIQUE"
    ]
    
    for desc in noyau_tests:
        noyau = detecter_noyau_simple(desc)
        print(f"   📝 '{desc}' → {noyau}")
    
    # 3. Test de détection des matières housse
    print("\n📋 3. Test de détection des matières housse:")
    
    housse_tests = [
        "HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES",
        "HOUSSE COTON 100% LAVABLE",
        "HOUSSE POLYESTER ANTI-ACARIENS",
        "HOUSSE TENCEL NATUREL",
        "HOUSSE STANDARD COTON-POLYESTER"
    ]
    
    for desc in housse_tests:
        matiere = detecter_matiere_housse_simple(desc)
        print(f"   📝 '{desc}' → {matiere}")
    
    # 4. Test complet d'extraction
    print("\n📋 4. Test complet d'extraction:")
    
    # Exemple de description complète
    description_complete = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40° - 89/198/20"
    
    print(f"   📝 Description: {description_complete}")
    
    # Extraire les dimensions
    dimensions = detecter_dimensions(description_complete)
    if dimensions:
        print(f"   📏 Dimensions: {dimensions}")
        
        # Extraire le noyau
        noyau = detecter_noyau_simple(description_complete)
        print(f"   🛏️ Noyau: {noyau}")
        
        # Extraire la matière housse
        matiere = detecter_matiere_housse_simple(description_complete)
        print(f"   🧵 Matière housse: {matiere}")
        
        # Calculer les dimensions arrondies
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        hauteur = dimensions.get("hauteur", 0)
        
        largeur_arrondie = int(round(largeur / 10.0) * 10)
        longueur_arrondie = int(round(longueur / 10.0) * 10)
        
        print(f"   📐 Dimensions arrondies: {largeur_arrondie} x {longueur_arrondie}")
        
        # Formatage pour Excel
        dimension_excel = f"{largeur_arrondie} x {longueur_arrondie}"
        print(f"   📊 Format Excel: {dimension_excel}")
        
    else:
        print("   ❌ Aucune dimension détectée dans la description")
    
    # 5. Test avec des formats problématiques
    print("\n📋 5. Test avec des formats problématiques:")
    
    problematiques = [
        "MATELAS 89/198/20",  # Format simple
        "MATELAS 89 / 198 / 20",  # Avec espaces
        "MATELAS 89,198,20",  # Avec virgules
        "MATELAS 89.198.20",  # Avec points
        "MATELAS 89x198x20",  # Avec x
        "MATELAS 89 X 198 X 20",  # Avec X majuscule
        "MATELAS 89*198*20",  # Avec astérisque
        "MATELAS 89-198-20"   # Avec tirets
    ]
    
    for desc in problematiques:
        dimensions = detecter_dimensions(desc)
        if dimensions:
            print(f"   ✅ '{desc}' → {dimensions}")
        else:
            print(f"   ❌ '{desc}' → Aucune dimension détectée")
    
    # 6. Recommandations
    print("\n📋 6. Recommandations:")
    print("   🔍 Le format le plus fiable est: 'largeur/longueur/hauteur'")
    print("   📝 Exemple: '89/198/20' ou '89 / 198 / 20'")
    print("   ⚠️ Les formats avec 'x' ou autres séparateurs peuvent ne pas être détectés")
    print("   💡 Vérifiez que le PDF contient bien les dimensions au bon format")

def test_llm_extraction_simulation():
    """Simulation de l'extraction LLM"""
    
    print("\n=== SIMULATION EXTRACTION LLM ===")
    
    # Simuler le texte extrait du PDF
    texte_pdf = """
    DEVIS N° 2024-001
    
    Client: Mr GALOO
    Adresse: 123 Rue de la Paix, 75001 Paris
    
    Literie: 89/198
    
    MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES LAVABLE A 40° - 89/198/20    1,00
    
    SOMMIER À LATTES - BOIS MASSIF - 89/198/8    1,00
    
    Remise: 5% enlèvement par vos soins
    """
    
    print("📄 Texte extrait du PDF:")
    print(texte_pdf)
    
    # Simuler l'extraction des dimensions
    print("\n🔍 Extraction des dimensions:")
    
    # Rechercher les dimensions dans le texte
    import re
    
    # Pattern pour détecter les dimensions
    pattern = r'(\d+(?:[.,]\d+)?)\s*[\/xX]\s*(\d+(?:[.,]\d+)?)(?:\s*[\/xX]\s*(\d+(?:[.,]\d+)?))?'
    
    matches = re.findall(pattern, texte_pdf)
    
    if matches:
        print("   ✅ Dimensions trouvées:")
        for i, match in enumerate(matches):
            if len(match) == 3 and match[2]:  # Avec hauteur
                print(f"      {i+1}. {match[0]}/{match[1]}/{match[2]}")
            else:  # Sans hauteur
                print(f"      {i+1}. {match[0]}/{match[1]}")
    else:
        print("   ❌ Aucune dimension trouvée dans le texte")
    
    # Simuler l'extraction des articles
    print("\n📋 Extraction des articles:")
    
    # Détecter les lignes d'articles
    lignes = texte_pdf.split('\n')
    articles = []
    
    for ligne in lignes:
        if 'MATELAS' in ligne or 'SOMMIER' in ligne:
            # Extraire les dimensions de cette ligne
            dim_match = re.search(pattern, ligne)
            if dim_match:
                if len(dim_match.groups()) == 3 and dim_match.group(3):
                    dimensions = f"{dim_match.group(1)}/{dim_match.group(2)}/{dim_match.group(3)}"
                else:
                    dimensions = f"{dim_match.group(1)}/{dim_match.group(2)}"
                
                article_type = "MATELAS" if "MATELAS" in ligne else "SOMMIER"
                articles.append({
                    "type": article_type,
                    "description": ligne.strip(),
                    "dimensions": dimensions
                })
    
    print(f"   📝 {len(articles)} articles détectés:")
    for i, article in enumerate(articles):
        print(f"      {i+1}. {article['type']}: {article['dimensions']}")
    
    # 7. Résumé et diagnostic
    print("\n📋 7. Résumé et diagnostic:")
    
    if articles:
        print("   ✅ Articles détectés avec succès")
        print("   ✅ Dimensions extraites correctement")
        print("   ✅ Format compatible avec le système")
    else:
        print("   ❌ Aucun article détecté")
        print("   ❌ Problème d'extraction des dimensions")
        print("   🔧 Vérifiez le format du PDF source")
    
    print("\n💡 Si le fichier Excel est généré mais sans dimensions:")
    print("   1. Vérifiez que le PDF contient les dimensions au format '89/198/20'")
    print("   2. Vérifiez que le LLM extrait correctement ces informations")
    print("   3. Vérifiez que la fonction detecter_dimensions() fonctionne")
    print("   4. Vérifiez les logs de l'application pour les erreurs")

if __name__ == "__main__":
    print("🚀 Test de l'extraction des dimensions")
    
    # Test principal
    test_extraction_dimensions()
    
    # Test simulation LLM
    test_llm_extraction_simulation()
    
    print("\n=== FIN DES TESTS ===")
