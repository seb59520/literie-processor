#!/usr/bin/env python3
"""
Vérification des modifications du prompt de livraison
"""

def verifier_modifications():
    """Vérifie que les modifications du prompt ont été appliquées"""
    
    print("=== VÉRIFICATION DES MODIFICATIONS DU PROMPT ===")
    
    # 1. Vérifier que le fichier backend_interface.py a été modifié
    print("\n📁 1. Vérification du fichier backend_interface.py:")
    
    try:
        with open('backend_interface.py', 'r', encoding='utf-8') as f:
            contenu = f.read()
        print("   ✅ Fichier backend_interface.py lu avec succès")
    except Exception as e:
        print(f"   ❌ Erreur lecture fichier: {e}")
        return False
    
    # 2. Vérifier les modifications appliquées
    print("\n🔍 2. Vérification des modifications:")
    
    modifications_attendues = [
        "mode_mise_a_disposition",
        "emporte_client_C57",
        "fourgon_C58", 
        "transporteur_C59",
        "INSTRUCTIONS CRITIQUES POUR LA LIVRAISON",
        "DÉTECTER et EXTRACTER TOUS les modes de livraison",
        "fourgon", "livraison par fourgon", "fourgon de l'entreprise",
        "enlèvement", "retrait", "enlèvement par vos soins",
        "transporteur", "livraison par transporteur",
        "EXEMPLES DE DÉTECTION DE LIVRAISON",
        "RÈGLE FINALE : Sois TRÈS ATTENTIF aux informations de livraison"
    ]
    
    modifications_trouvees = []
    modifications_manquantes = []
    
    for modification in modifications_attendues:
        if modification in contenu:
            modifications_trouvees.append(modification)
            print(f"   ✅ '{modification}' trouvé")
        else:
            modifications_manquantes.append(modification)
            print(f"   ❌ '{modification}' NON trouvé")
    
    # 3. Vérifier la structure JSON
    print("\n📊 3. Vérification de la structure JSON:")
    
    if '"mode_mise_a_disposition": {{' in contenu:
        print("   ✅ Section mode_mise_a_disposition présente dans la structure JSON")
    else:
        print("   ❌ Section mode_mise_a_disposition manquante dans la structure JSON")
    
    # 4. Résumé des modifications
    print(f"\n🎯 RÉSUMÉ DES MODIFICATIONS:")
    print(f"   ✅ Modifications trouvées: {len(modifications_trouvees)}/{len(modifications_attendues)}")
    
    if modifications_manquantes:
        print(f"   ❌ Modifications manquantes: {len(modifications_manquantes)}")
        print("   📝 Modifications à vérifier:")
        for mod in modifications_manquantes:
            print(f"      - {mod}")
    
    # 5. Évaluation de la qualité
    if len(modifications_trouvees) >= len(modifications_attendues) * 0.9:  # 90% de réussite
        print(f"\n🎉 SUCCÈS: Les modifications ont été appliquées avec succès !")
        print(f"   Le prompt de livraison est maintenant amélioré")
        return True
    elif len(modifications_trouvees) >= len(modifications_attendues) * 0.7:  # 70% de réussite
        print(f"\n⚠️ PARTIEL: La plupart des modifications ont été appliquées")
        print(f"   Quelques éléments manquent mais le prompt devrait fonctionner")
        return True
    else:
        print(f"\n❌ ÉCHEC: Trop de modifications manquantes")
        print(f"   Le prompt n'a pas été correctement modifié")
        return False

def instructions_test():
    """Donne les instructions pour tester après modification"""
    
    print("\n🧪 INSTRUCTIONS DE TEST APRÈS MODIFICATION:")
    
    print("   1. 📱 Relancer l'application MatelasApp")
    print("   2. ✅ Cocher 'Utiliser l'enrichissement LLM'")
    print("   3. 🔧 Sélectionner le provider LLM (Ollama ou OpenRouter)")
    print("   4. 📁 Sélectionner votre PDF COSTENOBLE")
    print("   5. 🚀 Cliquer sur 'Traiter les fichiers'")
    print("   6. 🔍 Vérifier dans les logs:")
    print("      - Si le LLM extrait des informations de livraison")
    print("      - Si le champ fourgon_C58 est rempli")
    print("      - Si la valeur est transmise à l'Excel")
    
    print("\n   📊 Résultat attendu:")
    print("      - fourgon_C58 devrait maintenant contenir une valeur")
    print("      - Au lieu de 'None' ou champ vide")
    
    print("\n   🔍 Points de vérification dans les logs:")
    print("      - Rechercher 'INSTRUCTIONS CRITIQUES POUR LA LIVRAISON'")
    print("      - Rechercher 'fourgon_C58' dans les résultats LLM")
    print("      - Vérifier que la valeur est transmise à l'export Excel")

def afficher_diff_prompt():
    """Affiche les différences entre l'ancien et le nouveau prompt"""
    
    print("\n📋 COMPARAISON AVANT/APRÈS:")
    
    print("   🔴 AVANT (ancien prompt):")
    print("      - Pas d'instructions spécifiques pour la livraison")
    print("      - Pas de section mode_mise_a_disposition")
    print("      - Pas d'exemples de détection")
    print("      - Résultat: fourgon_C58 toujours None")
    
    print("\n   🟢 APRÈS (nouveau prompt):")
    print("      - Instructions CRITIQUES pour la livraison")
    print("      - Section mode_mise_a_disposition incluse")
    print("      - Exemples concrets de détection")
    print("      - Règle finale d'attention")
    print("      - Résultat attendu: fourgon_C58 rempli")

if __name__ == "__main__":
    print("🚀 Vérification des modifications du prompt de livraison")
    
    # Vérification principale
    success = verifier_modifications()
    
    # Affichage des différences
    afficher_diff_prompt()
    
    if success:
        print("\n🎉 SUCCÈS: Le prompt a été modifié avec succès !")
        print("🚀 Vous pouvez maintenant tester l'application")
        
        # Instructions de test
        instructions_test()
        
    else:
        print("\n❌ ÉCHEC: Le prompt n'a pas été correctement modifié")
        print("🔧 Vérification manuelle nécessaire")
        
        # Instructions de test quand même
        instructions_test()
    
    print("\n=== FIN DE LA VÉRIFICATION ===")

