#!/usr/bin/env python3
"""
Diagnostic complet des dimensions manquantes
"""

import sys
import os
import json

# Ajouter le répertoire backend au path
sys.path.append('backend')

from dimensions_utils import detecter_dimensions

def diagnostic_complet():
    """Diagnostic complet du problème des dimensions"""
    
    print("=== DIAGNOSTIC COMPLET DES DIMENSIONS MANQUANTES ===")
    
    # 1. Vérifier la fonction detecter_dimensions
    print("\n📋 1. Test de la fonction detecter_dimensions:")
    
    test_description = "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40° 139/ 189/ 20"
    
    dimensions = detecter_dimensions(test_description)
    if dimensions:
        print(f"   ✅ Dimensions détectées: {dimensions}")
        print(f"   📏 Largeur: {dimensions['largeur']} cm")
        print(f"   📏 Longueur: {dimensions['longueur']} cm")
        print(f"   📏 Hauteur: {dimensions.get('hauteur', 0)} cm")
    else:
        print("   ❌ ERREUR: Aucune dimension détectée")
        return False
    
    # 2. Simuler le processus LLM
    print("\n📋 2. Simulation du processus LLM:")
    
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
    
    print("   📄 Texte extrait du PDF (simulation):")
    print("   " + texte_pdf.replace('\n', '\n   '))
    
    # 3. Simuler l'extraction LLM
    print("\n📋 3. Simulation de l'extraction LLM:")
    
    # Rechercher les dimensions dans le texte
    import re
    
    # Pattern pour détecter les dimensions
    pattern = r'(\d+(?:[.,]\d+)?)\s*[\/xX]\s*(\d+(?:[.,]\d+)?)(?:\s*[\/xX]\s*(\d+(?:[.,]\d+)?))?'
    
    matches = re.findall(pattern, texte_pdf)
    
    if matches:
        print("   ✅ Dimensions trouvées dans le texte:")
        for i, match in enumerate(matches):
            if len(match) == 3 and match[2]:  # Avec hauteur
                print(f"      {i+1}. {match[0]}/{match[1]}/{match[2]}")
            else:  # Sans hauteur
                print(f"      {i+1}. {match[0]}/{match[1]}")
    else:
        print("   ❌ Aucune dimension trouvée dans le texte")
        return False
    
    # 4. Simuler la création des configurations
    print("\n📋 4. Simulation de la création des configurations:")
    
    # Simuler l'extraction des articles
    lignes = texte_pdf.split('\n')
    articles = []
    
    for ligne in lignes:
        if 'MATELAS' in ligne:
            # Extraire les dimensions de cette ligne
            dim_match = re.search(pattern, ligne)
            if dim_match:
                if len(dim_match.groups()) == 3 and dim_match.group(3):
                    dimensions_str = f"{dim_match.group(1)}/{dim_match.group(2)}/{dim_match.group(3)}"
                else:
                    dimensions_str = f"{dim_match.group(1)}/{dim_match.group(2)}"
                
                articles.append({
                    "type": "MATELAS",
                    "description": ligne.strip(),
                    "dimensions": dimensions_str
                })
    
    print(f"   📝 {len(articles)} articles détectés:")
    for i, article in enumerate(articles):
        print(f"      {i+1}. {article['type']}: {article['dimensions']}")
    
    # 5. Simuler le traitement des dimensions
    print("\n📋 5. Simulation du traitement des dimensions:")
    
    for i, article in enumerate(articles):
        print(f"   🔄 Article {i+1}:")
        
        # Extraire les dimensions
        dimensions = detecter_dimensions(article['dimensions'])
        if dimensions:
            print(f"      ✅ Dimensions extraites: {dimensions}")
            
            # Calculer les dimensions arrondies
            largeur = dimensions["largeur"]
            longueur = dimensions["longueur"]
            
            largeur_arrondie = int(round(largeur / 10.0) * 10)
            longueur_arrondie = int(round(longueur / 10.0) * 10)
            
            print(f"      📐 Dimensions arrondies: {largeur_arrondie} x {longueur_arrondie}")
            
            # Formatage pour Excel
            dimension_excel = f"{largeur_arrondie} x {longueur_arrondie}"
            print(f"      📊 Format Excel: {dimension_excel}")
            
        else:
            print(f"      ❌ ERREUR: Impossible d'extraire les dimensions de '{article['dimensions']}'")
            return False
    
    # 6. Diagnostic du problème
    print("\n📋 6. Diagnostic du problème:")
    
    print("   🔍 Analyse des logs:")
    print("      ❌ Tous les champs Excel sont vides: 'Écriture: J17 = '")
    print("      ❌ Aucune donnée n'est écrite dans les cellules")
    
    print("\n   🎯 Causes possibles:")
    print("      1. ❌ Le LLM n'extrait pas les dimensions depuis le PDF")
    print("      2. ❌ La fonction detecter_dimensions() n'est pas appelée")
    print("      3. ❌ Les données ne sont pas transmises à l'export Excel")
    print("      4. ❌ Problème dans la génération du pré-import")
    
    # 7. Solutions à essayer
    print("\n📋 7. Solutions à essayer:")
    
    print("   🚀 Solution 1: Vérifier l'extraction LLM")
    print("      - Lancer l'application avec 'Enrichissement LLM' activé")
    print("      - Traiter votre PDF et vérifier les logs LLM")
    print("      - Rechercher si '139/ 189/ 20' est extrait")
    
    print("\n   🚀 Solution 2: Vérifier le prompt LLM")
    print("      - Le prompt doit demander explicitement les dimensions")
    print("      - Vérifier que le LLM retourne un JSON avec 'dimensions'")
    
    print("\n   🚀 Solution 3: Vérifier la chaîne de traitement")
    print("      - PDF → LLM → JSON → Dimensions → Excel")
    print("      - Identifier quelle étape échoue")
    
    print("\n   🚀 Solution 4: Vérifier les logs complets")
    print("      - Chercher les messages d'extraction LLM")
    print("      - Chercher les appels à detecter_dimensions()")
    print("      - Chercher la génération du pré-import")
    
    # 8. Test immédiat
    print("\n📋 8. Test immédiat à faire:")
    
    print("   1. 📱 Ouvrir l'application MatelasApp")
    print("   2. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   3. 🔧 Sélectionner le provider LLM (Ollama ou OpenRouter)")
    print("   4. 📁 Sélectionner votre PDF")
    print("   5. 🚀 Cliquer sur 'Traiter les fichiers'")
    print("   6. 📊 Vérifier les logs pour voir l'extraction LLM")
    
    return True

def test_llm_prompt():
    """Test du prompt LLM"""
    
    print("\n=== TEST DU PROMPT LLM ===")
    
    # Prompt actuel utilisé dans l'application
    prompt_actuel = """Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux.

Analyse le texte suivant : 

{text}

⚠️ INSTRUCTIONS CRITIQUES POUR LES MATELAS :
- Pour chaque matelas, tu dois extraire la description COMPLÈTE incluant TOUTES les informations (noyau, fermeté, housse, matière, poignées, caractéristiques spéciales...)
- NE TRONQUE JAMAIS la description d'un matelas !
- Si la description s'étend sur plusieurs lignes, combine-les en une seule description complète.
- Exemple de description complète : "MATELAS 1 PIÈCE - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES FERME (50KG/ M3) - HOUSSE MATELASSÉE TENCEL LUXE 3D AVEC POIGNÉES INTÉGRÉES DÉHOUSSABLE SUR 3 CÔTÉS ET LAVABLE A 40°"

⚠️ IMPORTANT : Tu dois répondre UNIQUEMENT avec du JSON valide, sans texte avant ou après.
Extrais les informations sous forme de **JSON**.  
Respecte exactement cette structure :

{
  "societe": {
    "nom": "...",
    "capital": "...",
    "adresse": "...",
    "telephone": "...",
    "fax": "...",
    "email": "...",
    "siret": "...",
    "APE": "...",
    "CEE": "...",
    "banque": "...",
    "IBAN": "..."
  },
  "client": {
    "nom": "...",
    "adresse": "...",
    "code_client": "..."
  },
  "commande": {
    "numero": "...",
    "date": "...",
    "date_validite": "...",
    "commercial": "...",
    "origine": "..."
  },
  "articles": [
    {
      "quantite": ...,
      "description": "...",
      "dimensions": "...",
      "pu_ttc": ...,
      "eco_part": ...,
      "pu_ht": ...
    }
  ],
  "paiement": {
    "conditions": "...",
    "port_ht": ...,
    "base_ht": ...,
    "taux_tva": ...,
    "total_ttc": ...,
    "acompte": ...,
    "net_a_payer": ...
  }
}"""
    
    print("📝 Prompt actuel utilisé:")
    print(prompt_actuel)
    
    print("\n🔍 Analyse du prompt:")
    
    # Vérifier si le prompt demande les dimensions
    if "dimensions" in prompt_actuel:
        print("   ✅ Le prompt demande les dimensions")
    else:
        print("   ❌ Le prompt ne demande pas les dimensions")
    
    # Vérifier si le prompt a des instructions spécifiques pour les matelas
    if "INSTRUCTIONS CRITIQUES POUR LES MATELAS" in prompt_actuel:
        print("   ✅ Le prompt a des instructions spécifiques pour les matelas")
    else:
        print("   ❌ Le prompt n'a pas d'instructions spécifiques pour les matelas")
    
    # Vérifier la structure JSON demandée
    if '"dimensions": "..."' in prompt_actuel:
        print("   ✅ La structure JSON inclut le champ 'dimensions'")
    else:
        print("   ❌ La structure JSON n'inclut pas le champ 'dimensions'")
    
    print("\n💡 Recommandations:")
    print("   1. Le prompt doit explicitement demander les dimensions")
    print("   2. Le prompt doit donner des exemples de format de dimensions")
    print("   3. Le prompt doit insister sur l'extraction complète des informations")

if __name__ == "__main__":
    print("🚀 Diagnostic complet des dimensions manquantes")
    
    # Diagnostic principal
    success = diagnostic_complet()
    
    # Test du prompt LLM
    test_llm_prompt()
    
    if success:
        print("\n🎯 RÉSUMÉ DU DIAGNOSTIC:")
        print("✅ La fonction detecter_dimensions() fonctionne parfaitement")
        print("✅ Votre description est compatible")
        print("✅ Le processus de calcul fonctionne")
        print("\n❌ LE PROBLÈME EST:")
        print("   - Dans l'extraction LLM depuis le PDF")
        print("   - Ou dans la transmission des données vers l'export Excel")
        print("\n🔧 PROCHAINES ÉTAPES:")
        print("   1. Vérifier l'extraction LLM avec l'option activée")
        print("   2. Vérifier les logs complets de l'application")
        print("   3. Identifier quelle étape de la chaîne échoue")
    else:
        print("\n❌ Problème détecté dans le diagnostic")
        print("🔧 Vérifiez les erreurs ci-dessus")
    
    print("\n=== FIN DU DIAGNOSTIC ===")

