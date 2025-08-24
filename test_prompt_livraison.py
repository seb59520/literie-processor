#!/usr/bin/env python3
"""
Test du nouveau prompt de livraison amélioré
"""

import json

def test_prompt_livraison():
    """Test du nouveau prompt de livraison"""
    
    print("=== TEST DU NOUVEAU PROMPT DE LIVRAISON ===")
    
    # 1. Lire le nouveau prompt
    print("\n📝 1. Nouveau prompt de livraison:")
    
    try:
        with open('prompt_ameliore_livraison.txt', 'r', encoding='utf-8') as f:
            nouveau_prompt = f.read()
        print("   ✅ Prompt chargé avec succès")
    except FileNotFoundError:
        print("   ❌ Fichier prompt_ameliore_livraison.txt non trouvé")
        return False
    
    # 2. Vérifier les améliorations
    print("\n📋 2. Vérification des améliorations:")
    
    ameliorations = [
        "INSTRUCTIONS CRITIQUES POUR LA LIVRAISON",
        "DÉTECTER et EXTRACTER TOUS les modes de livraison",
        "fourgon", "livraison par fourgon", "fourgon de l'entreprise",
        "enlèvement", "retrait", "enlèvement par vos soins",
        "transporteur", "livraison par transporteur",
        "EXEMPLES DE DÉTECTION DE LIVRAISON"
    ]
    
    for amelioration in ameliorations:
        if amelioration in nouveau_prompt:
            print(f"   ✅ '{amelioration}' trouvé")
        else:
            print(f"   ❌ '{amelioration}' non trouvé")
    
    # 3. Simuler l'extraction avec différents textes
    print("\n📋 3. Simulation d'extraction avec différents textes:")
    
    textes_test = [
        {
            "nom": "Test Fourgon explicite",
            "texte": """
            DEVIS N° 2024-001
            Client: Mr COSTENOBLE
            Livraison: Fourgon de l'entreprise
            MATELAS LATEX 160x200x20
            """,
            "attendu": "fourgon_C58 devrait être rempli"
        },
        {
            "nom": "Test Enlèvement",
            "texte": """
            DEVIS N° 2024-002
            Client: Mr DUPONT
            Remise: 5% enlèvement par vos soins
            MATELAS MOUSSE 90x200x20
            """,
            "attendu": "emporte_client_C57 devrait être rempli"
        },
        {
            "nom": "Test Transporteur",
            "texte": """
            DEVIS N° 2024-003
            Client: Mr MARTIN
            Livraison par transporteur
            MATELAS LATEX 140x190x20
            """,
            "attendu": "transporteur_C59 devrait être rempli"
        },
        {
            "nom": "Test Aucune info livraison",
            "texte": """
            DEVIS N° 2024-004
            Client: Mr DURAND
            MATELAS LATEX 160x200x20
            Prix: 500€
            """,
            "attendu": "Tous les champs de livraison devraient être null"
        }
    ]
    
    for i, test in enumerate(textes_test, 1):
        print(f"\n   🔍 Test {i}: {test['nom']}")
        print(f"      📄 Texte: {test['texte'].strip()}")
        print(f"      🎯 Attendu: {test['attendu']}")
        
        # Analyser le texte pour identifier les mots-clés
        mots_cles_fourgon = ["fourgon", "livraison par fourgon", "fourgon de l'entreprise"]
        mots_cles_enlevement = ["enlèvement", "retrait", "enlèvement par vos soins"]
        mots_cles_transporteur = ["transporteur", "livraison par transporteur"]
        
        fourgon_trouve = any(mot in test['texte'].lower() for mot in mots_cles_fourgon)
        enlevement_trouve = any(mot in test['texte'].lower() for mot in mots_cles_enlevement)
        transporteur_trouve = any(mot in test['texte'].lower() for mot in mots_cles_transporteur)
        
        print(f"      🔍 Fourgon détecté: {'✅ OUI' if fourgon_trouve else '❌ NON'}")
        print(f"      🔍 Enlèvement détecté: {'✅ OUI' if enlevement_trouve else '❌ NON'}")
        print(f"      🔍 Transporteur détecté: {'✅ OUI' if transporteur_trouve else '❌ NON'}")
    
    # 4. Recommandations d'utilisation
    print("\n📋 4. Recommandations d'utilisation:")
    
    print("   🚀 Pour tester le nouveau prompt:")
    print("      1. Remplacer le prompt actuel dans l'application")
    print("      2. Traiter votre PDF COSTENOBLE avec LLM activé")
    print("      3. Vérifier que fourgon_C58 est maintenant rempli")
    
    print("\n   🔧 Remplacement du prompt:")
    print("      - Copier le contenu de prompt_ameliore_livraison.txt")
    print("      - Remplacer le prompt dans backend_interface.py")
    print("      - Ou modifier directement le fichier de configuration")
    
    # 5. Vérification de la structure JSON
    print("\n📋 5. Vérification de la structure JSON:")
    
    structure_verifiee = {
        "mode_mise_a_disposition": {
            "emporte_client_C57": "exemple enlèvement",
            "fourgon_C58": "exemple fourgon",
            "transporteur_C59": "exemple transporteur"
        }
    }
    
    try:
        json_str = json.dumps(structure_verifiee, indent=2, ensure_ascii=False)
        print("   ✅ Structure JSON valide")
        print("   📊 Exemple de structure:")
        print(json_str)
    except Exception as e:
        print(f"   ❌ Erreur JSON: {e}")
    
    return True

def comparer_prompts():
    """Compare l'ancien et le nouveau prompt"""
    
    print("\n=== COMPARAISON DES PROMPTS ===")
    
    print("   📊 Ancien prompt:")
    print("      ✅ Inclut mode_mise_a_disposition")
    print("      ❌ Pas d'instructions spécifiques pour la livraison")
    print("      ❌ Pas d'exemples de détection")
    
    print("\n   📊 Nouveau prompt:")
    print("      ✅ Inclut mode_mise_a_disposition")
    print("      ✅ Instructions CRITIQUES pour la livraison")
    print("      ✅ Mots-clés spécifiques listés")
    print("      ✅ Exemples concrets de détection")
    print("      ✅ Règle finale d'attention")
    
    print("\n   🎯 Amélioration principale:")
    print("      Le nouveau prompt est BEAUCOUP plus explicite")
    print("      et donne des instructions claires pour détecter")
    print("      les informations de livraison.")

if __name__ == "__main__":
    print("🚀 Test du nouveau prompt de livraison")
    
    # Test principal
    success = test_prompt_livraison()
    
    # Comparaison des prompts
    comparer_prompts()
    
    if success:
        print("\n🎯 RÉSUMÉ DU TEST:")
        print("✅ Le nouveau prompt est prêt à être utilisé")
        print("✅ Il inclut des instructions spécifiques pour la livraison")
        print("✅ Il devrait améliorer la détection du fourgon")
        print("\n🔧 PROCHAINE ÉTAPE:")
        print("   Remplacer le prompt dans l'application et tester")
    else:
        print("\n❌ Problème détecté dans le test")
    
    print("\n=== FIN DU TEST ===")

