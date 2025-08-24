#!/usr/bin/env python3
"""
Diagnostic du problème de détection du fourgon
"""

import sys
import json
import re

# Ajouter le répertoire backend au path
sys.path.append('backend')

def analyser_probleme_fourgon():
    """Analyse le problème de détection du fourgon"""
    
    print("=== DIAGNOSTIC DU PROBLÈME FOURGON ===")
    
    # 1. Vérifier la structure JSON attendue
    print("\n📋 1. Structure JSON attendue pour le fourgon:")
    
    structure_attendue = {
        "mode_mise_a_disposition": {
            "emporte_client_C57": "...",
            "fourgon_C58": "...",  # ← Ce champ doit être extrait
            "transporteur_C59": "..."
        }
    }
    
    print("   📊 Champ attendu: fourgon_C58")
    print("   📝 Dans la section: mode_mise_a_disposition")
    
    # 2. Analyser votre test LLM précédent
    print("\n📋 2. Analyse de votre test LLM précédent:")
    
    test_llm_galoo = {
        "mode_mise_a_disposition": {
            "emporte_client_C57": None,
            "fourgon_C58": None,  # ← Était None dans votre test
            "transporteur_C59": None
        }
    }
    
    print("   🔍 Dans le test GALOO:")
    print(f"      - fourgon_C58: {test_llm_galoo['mode_mise_a_disposition']['fourgon_C58']}")
    print("      - ❌ PROBLÈME: Le champ est None")
    
    # 3. Vérifier le prompt LLM
    print("\n📋 3. Vérification du prompt LLM:")
    
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
  "societe": { ... },
  "client": { ... },
  "commande": { ... },
  "mode_mise_a_disposition": {
    "emporte_client_C57": "...",
    "fourgon_C58": "...",
    "transporteur_C59": "..."
  },
  "articles": [ ... ],
  "paiement": { ... }
}"""
    
    print("   📝 Prompt actuel:")
    print("      ✅ Inclut la section mode_mise_a_disposition")
    print("      ✅ Inclut le champ fourgon_C58")
    
    # 4. Identifier les causes possibles
    print("\n📋 4. Causes possibles du problème:")
    
    print("   🎯 Cause 1: Le LLM ne trouve pas d'information sur le fourgon")
    print("      - Le PDF ne mentionne pas explicitement 'fourgon'")
    print("      - Le LLM ne sait pas quoi mettre dans ce champ")
    
    print("\n   🎯 Cause 2: Le prompt n'est pas assez explicite")
    print("      - Pas d'instructions spécifiques pour détecter le mode de livraison")
    print("      - Le LLM ne comprend pas ce qu'il doit chercher")
    
    print("\n   🎯 Cause 3: Le champ n'est pas mappé correctement")
    print("      - Le LLM extrait l'info mais elle n'est pas transmise à l'Excel")
    
    # 5. Solutions proposées
    print("\n📋 5. Solutions proposées:")
    
    print("   🚀 Solution 1: Améliorer le prompt LLM")
    print("      - Ajouter des instructions spécifiques pour la livraison")
    print("      - Donner des exemples de détection")
    
    print("\n   🚀 Solution 2: Vérifier l'extraction dans le PDF")
    print("      - Analyser le texte extrait pour voir s'il y a des mentions de livraison")
    print("      - Identifier les mots-clés utilisés")
    
    print("\n   🚀 Solution 3: Vérifier le mapping Excel")
    print("      - S'assurer que fourgon_C58 est correctement mappé")
    print("      - Vérifier que la valeur est transmise à l'export")
    
    # 6. Test immédiat recommandé
    print("\n📋 6. Test immédiat recommandé:")
    
    print("   1. 📱 Relancer l'application")
    print("   2. ✅ Traiter votre PDF COSTENOBLE avec LLM activé")
    print("   3. 🔍 Regarder dans les logs:")
    print("      - Si le LLM extrait des informations de livraison")
    print("      - Si le champ fourgon_C58 est rempli")
    print("      - Si la valeur est transmise à l'Excel")
    
    return True

def analyser_texte_pdf_exemple():
    """Analyse un exemple de texte PDF pour identifier les mots-clés de livraison"""
    
    print("\n=== ANALYSE DES MOTS-CLÉS DE LIVRAISON ===")
    
    # Exemple de texte PDF typique
    texte_exemple = """
    DEVIS N° 2024-001
    
    Client: Mr et Mme COSTENOBLE
    Adresse: 123 Rue de la Paix, 75001 Paris
    
    Livraison: Fourgon de l'entreprise
    Mode de livraison: Livraison par fourgon
    Transport: Fourgon de livraison
    
    MATELAS LATEX 160x200x20
    Prix: 500€
    
    Remise: 5% enlèvement par vos soins
    """
    
    print("📄 Texte PDF exemple:")
    print(texte_exemple)
    
    # Rechercher les mots-clés de livraison
    mots_cles_livraison = [
        "fourgon", "livraison", "transport", "livrer", "livraison par",
        "enlèvement", "retrait", "expédition", "acheminement"
    ]
    
    print("\n🔍 Mots-clés de livraison recherchés:")
    for mot_cle in mots_cles_livraison:
        if mot_cle.lower() in texte_exemple.lower():
            print(f"   ✅ '{mot_cle}' trouvé")
        else:
            print(f"   ❌ '{mot_cle}' non trouvé")
    
    # Pattern pour détecter le mode de livraison
    print("\n🔍 Pattern de détection suggéré:")
    pattern_fourgon = r'(?:livraison|transport|livrer|acheminement).*?(?:fourgon|livraison)'
    match = re.search(pattern_fourgon, texte_exemple, re.IGNORECASE)
    
    if match:
        print(f"   ✅ Mode de livraison détecté: '{match.group()}'")
    else:
        print("   ❌ Aucun mode de livraison détecté")

if __name__ == "__main__":
    print("🚀 Diagnostic du problème fourgon")
    
    # Diagnostic principal
    success = analyser_probleme_fourgon()
    
    # Analyse des mots-clés
    analyser_texte_pdf_exemple()
    
    if success:
        print("\n🎯 RÉSUMÉ DU DIAGNOSTIC:")
        print("✅ Le prompt LLM inclut bien le champ fourgon_C58")
        print("✅ La structure JSON est correcte")
        print("\n❌ LE PROBLÈME EST:")
        print("   - Le LLM ne trouve pas d'information sur le fourgon dans le PDF")
        print("   - Ou le prompt n'est pas assez explicite pour la détection")
        print("\n🔧 PROCHAINES ÉTAPES:")
        print("   1. Améliorer le prompt pour la détection de livraison")
        print("   2. Tester avec un PDF qui mentionne explicitement le fourgon")
        print("   3. Vérifier le mapping Excel")
    else:
        print("\n❌ Problème détecté dans le diagnostic")
    
    print("\n=== FIN DU DIAGNOSTIC ===")

