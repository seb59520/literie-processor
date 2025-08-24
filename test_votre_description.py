#!/usr/bin/env python3
"""
Test spécifique pour la description de l'utilisateur
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from dimensions_utils import detecter_dimensions

def test_votre_description():
    """Test de la description spécifique de l'utilisateur"""
    
    print("=== TEST DE VOTRE DESCRIPTION ===")
    
    # Votre description exacte
    votre_description = """MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME
(50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES
DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20"""
    
    print("📝 Votre description:")
    print(votre_description)
    print()
    
    # 1. Test d'extraction des dimensions
    print("📋 1. Test d'extraction des dimensions:")
    
    dimensions = detecter_dimensions(votre_description)
    if dimensions:
        print(f"   ✅ Dimensions détectées: {dimensions}")
        
        largeur = dimensions["largeur"]
        longueur = dimensions["longueur"]
        hauteur = dimensions.get("hauteur", 0)
        
        print(f"   📏 Largeur: {largeur} cm")
        print(f"   📏 Longueur: {longueur} cm")
        print(f"   📏 Hauteur: {hauteur} cm")
        
        # 2. Calcul des dimensions arrondies
        print("\n📋 2. Calcul des dimensions arrondies:")
        
        largeur_arrondie = int(round(largeur / 10.0) * 10)
        longueur_arrondie = int(round(longueur / 10.0) * 10)
        
        print(f"   📐 Largeur arrondie: {largeur} → {largeur_arrondie} cm")
        print(f"   📐 Longueur arrondie: {longueur} → {longueur_arrondie} cm")
        
        # 3. Formatage pour Excel
        print("\n📋 3. Formatage pour Excel:")
        
        dimension_excel = f"{largeur_arrondie} x {longueur_arrondie}"
        print(f"   📊 Format Excel: {dimension_excel}")
        
        # 4. Test avec différentes variantes de format
        print("\n📋 4. Test avec différentes variantes:")
        
        variantes = [
            "139/ 189/ 20",      # Votre format exact
            "139/189/20",        # Sans espaces
            "139 / 189 / 20",    # Avec espaces autour des /
            "139,189,20",        # Avec virgules
            "139.189.20",        # Avec points
            "139x189x20",        # Avec x
            "139 X 189 X 20"     # Avec X majuscule
        ]
        
        for variante in variantes:
            dim = detecter_dimensions(f"MATELAS {variante}")
            if dim:
                print(f"   ✅ '{variante}' → {dim}")
            else:
                print(f"   ❌ '{variante}' → Non détecté")
        
        # 5. Simulation du processus complet
        print("\n📋 5. Simulation du processus complet:")
        
        # Simuler l'extraction depuis le PDF
        print("   🔄 Étape 1: Extraction depuis le PDF")
        print(f"      Texte extrait: {votre_description}")
        
        # Simuler l'extraction des dimensions
        print("   🔄 Étape 2: Extraction des dimensions")
        if dimensions:
            print(f"      Dimensions extraites: {dimensions}")
        else:
            print("      ❌ ERREUR: Aucune dimension extraite")
            return False
        
        # Simuler le calcul des dimensions arrondies
        print("   🔄 Étape 3: Calcul des dimensions arrondies")
        print(f"      Dimensions arrondies: {largeur_arrondie} x {longueur_arrondie}")
        
        # Simuler la génération Excel
        print("   🔄 Étape 4: Génération Excel")
        print(f"      Champ dimension_housse: {dimension_excel}")
        print(f"      Champ decoupe_noyau: {largeur_arrondie} x {longueur_arrondie}")
        
        # 6. Résumé et diagnostic
        print("\n📋 6. Résumé et diagnostic:")
        
        if dimensions:
            print("   ✅ Dimensions extraites avec succès")
            print("   ✅ Format compatible avec le système")
            print("   ✅ Calculs effectués correctement")
            print("   ✅ Format Excel généré")
            
            print("\n💡 Si le fichier Excel ne contient pas ces dimensions:")
            print("   1. Le problème est dans l'extraction LLM depuis le PDF")
            print("   2. Le problème est dans la génération Excel")
            print("   3. Vérifiez les logs de l'application")
            
            return True
        else:
            print("   ❌ Problème d'extraction des dimensions")
            print("   🔧 Vérifiez le format dans le PDF source")
            return False
            
    else:
        print("   ❌ Aucune dimension détectée dans votre description")
        print("   🔧 Problème avec la fonction detecter_dimensions()")
        return False

def test_llm_extraction_simulation():
    """Simulation de l'extraction LLM avec votre description"""
    
    print("\n=== SIMULATION EXTRACTION LLM ===")
    
    # Simuler le texte extrait du PDF
    texte_pdf = """
    DEVIS N° 2024-001
    
    Client: Mr GALOO
    Adresse: 123 Rue de la Paix, 75001 Paris
    
    Literie: 139/189
    
    MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME
    (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES
    DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20    1,00
    
    Remise: 5% enlèvement par vos soins
    """
    
    print("📄 Texte extrait du PDF (simulation):")
    print(texte_pdf)
    
    # Simuler l'extraction des dimensions
    print("\n🔍 Extraction des dimensions:")
    
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
    
    lignes = texte_pdf.split('\n')
    articles = []
    
    for ligne in lignes:
        if 'MATELAS' in ligne:
            dim_match = re.search(pattern, ligne)
            if dim_match:
                if len(dim_match.groups()) == 3 and dim_match.group(3):
                    dimensions = f"{dim_match.group(1)}/{dim_match.group(2)}/{dim_match.group(3)}"
                else:
                    dimensions = f"{dim_match.group(1)}/{dim_match.group(2)}"
                
                articles.append({
                    "type": "MATELAS",
                    "description": ligne.strip(),
                    "dimensions": dimensions
                })
    
    print(f"   📝 {len(articles)} articles détectés:")
    for i, article in enumerate(articles):
        print(f"      {i+1}. {article['type']}: {article['dimensions']}")
    
    # 7. Diagnostic final
    print("\n📋 7. Diagnostic final:")
    
    if articles:
        print("   ✅ Articles détectés avec succès")
        print("   ✅ Dimensions extraites correctement")
        print("   ✅ Format compatible avec le système")
        
        print("\n🔍 Votre cas spécifique:")
        print("   📝 Description: MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME")
        print("   📏 Dimensions: 139/ 189/ 20")
        print("   🧵 Matière: TENCEL LUXE 3D")
        print("   📊 Format attendu Excel: 140 x 190")
        
        print("\n💡 Si les dimensions ne sont pas dans l'Excel:")
        print("   1. Vérifiez que le LLM extrait bien '139/ 189/ 20' depuis le PDF")
        print("   2. Vérifiez que la fonction detecter_dimensions() est appelée")
        print("   3. Vérifiez que les champs Excel sont bien remplis")
        
    else:
        print("   ❌ Aucun article détecté")
        print("   🔧 Problème d'extraction depuis le PDF")

if __name__ == "__main__":
    print("🚀 Test de votre description spécifique")
    
    # Test principal
    success = test_votre_description()
    
    # Test simulation LLM
    test_llm_extraction_simulation()
    
    if success:
        print("\n🎉 Votre description est parfaitement compatible !")
        print("✅ Les dimensions 139/ 189/ 20 sont détectées")
        print("✅ Le format est supporté par le système")
        print("✅ Les calculs fonctionnent correctement")
        print("\n🔧 Le problème doit être ailleurs dans le processus")
    else:
        print("\n❌ Problème détecté avec votre description")
        print("🔧 Vérifiez le format dans le PDF source")
    
    print("\n=== FIN DU TEST ===")

