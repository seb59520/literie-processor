#!/usr/bin/env python3
"""
Script pour appliquer le nouveau prompt de livraison dans l'application
"""

import os
import shutil
import re

def appliquer_prompt_livraison():
    """Applique le nouveau prompt de livraison dans l'application"""
    
    print("=== APPLICATION DU NOUVEAU PROMPT DE LIVRAISON ===")
    
    # 1. Vérifier que le nouveau prompt existe
    print("\n📝 1. Vérification du nouveau prompt:")
    
    if not os.path.exists('prompt_ameliore_livraison.txt'):
        print("   ❌ Fichier prompt_ameliore_livraison.txt non trouvé")
        return False
    
    print("   ✅ Nouveau prompt trouvé")
    
    # 2. Lire le nouveau prompt
    try:
        with open('prompt_ameliore_livraison.txt', 'r', encoding='utf-8') as f:
            nouveau_prompt = f.read()
        print("   ✅ Nouveau prompt lu avec succès")
    except Exception as e:
        print(f"   ❌ Erreur lecture prompt: {e}")
        return False
    
    # 3. Identifier les fichiers à modifier
    print("\n📁 2. Identification des fichiers à modifier:")
    
    fichiers_candidats = [
        'backend_interface.py',
        'backend/main.py',
        'config.py'
    ]
    
    fichiers_trouves = []
    for fichier in fichiers_candidats:
        if os.path.exists(fichier):
            fichiers_trouves.append(fichier)
            print(f"   ✅ {fichier} trouvé")
        else:
            print(f"   ❌ {fichier} non trouvé")
    
    if not fichiers_trouves:
        print("   ❌ Aucun fichier candidat trouvé")
        return False
    
    # 4. Rechercher le prompt actuel
    print("\n🔍 3. Recherche du prompt actuel:")
    
    prompt_actuel_trouve = False
    fichier_contenant_prompt = None
    
    for fichier in fichiers_trouves:
        try:
            with open(fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                
            # Rechercher des indices du prompt actuel
            indices_prompt = [
                "Tu es un assistant expert en extraction",
                "INSTRUCTIONS CRITIQUES POUR LES MATELAS",
                "mode_mise_a_disposition"
            ]
            
            if all(indice in contenu for indice in indices_prompt):
                print(f"   ✅ Prompt actuel trouvé dans {fichier}")
                prompt_actuel_trouve = True
                fichier_contenant_prompt = fichier
                break
                
        except Exception as e:
            print(f"   ❌ Erreur lecture {fichier}: {e}")
    
    if not prompt_actuel_trouve:
        print("   ❌ Prompt actuel non trouvé dans les fichiers candidats")
        print("   💡 Le prompt pourrait être dans un autre fichier")
        return False
    
    # 5. Créer une sauvegarde
    print(f"\n💾 4. Création de sauvegarde de {fichier_contenant_prompt}:")
    
    backup_file = f"{fichier_contenant_prompt}.backup"
    try:
        shutil.copy2(fichier_contenant_prompt, backup_file)
        print(f"   ✅ Sauvegarde créée: {backup_file}")
    except Exception as e:
        print(f"   ❌ Erreur création sauvegarde: {e}")
        return False
    
    # 6. Remplacer le prompt
    print(f"\n🔄 5. Remplacement du prompt dans {fichier_contenant_prompt}:")
    
    try:
        with open(fichier_contenant_prompt, 'r', encoding='utf-8') as f:
            contenu_actuel = f.read()
        
        # Rechercher le début et la fin du prompt actuel
        debut_prompt = "Tu es un assistant expert en extraction de données structurées à partir de documents PDF commerciaux."
        
        # Essayer de trouver la fin du prompt (après la structure JSON)
        fin_prompt_patterns = [
            "⚠️ RÈGLE FINALE : Sois TRÈS ATTENTIF aux informations de livraison",
            "⚠️ IMPORTANT : Tu dois répondre UNIQUEMENT avec du JSON valide",
            "Respecte exactement cette structure :"
        ]
        
        fin_prompt = None
        for pattern in fin_prompt_patterns:
            if pattern in contenu_actuel:
                # Chercher la fin après ce pattern
                pos = contenu_actuel.find(pattern)
                # Chercher la prochaine ligne vide ou la fin du fichier
                reste = contenu_actuel[pos:]
                lignes = reste.split('\n')
                for i, ligne in enumerate(lignes):
                    if ligne.strip() == "" or "}" in ligne:
                        fin_prompt = contenu_actuel[:pos + len('\n'.join(lignes[:i+1]))]
                        break
                if fin_prompt:
                    break
        
        if not fin_prompt:
            print("   ⚠️ Impossible de déterminer la fin exacte du prompt")
            print("   💡 Remplacement manuel recommandé")
            return False
        
        # Remplacer le prompt
        nouveau_contenu = contenu_actuel.replace(debut_prompt, nouveau_prompt)
        
        # Écrire le fichier modifié
        with open(fichier_contenant_prompt, 'w', encoding='utf-8') as f:
            f.write(nouveau_contenu)
        
        print("   ✅ Prompt remplacé avec succès")
        
    except Exception as e:
        print(f"   ❌ Erreur remplacement: {e}")
        return False
    
    # 7. Vérification
    print(f"\n✅ 6. Vérification du remplacement:")
    
    try:
        with open(fichier_contenant_prompt, 'r', encoding='utf-8') as f:
            contenu_verifie = f.read()
        
        if "INSTRUCTIONS CRITIQUES POUR LA LIVRAISON" in contenu_verifie:
            print("   ✅ Nouveau prompt détecté dans le fichier")
        else:
            print("   ❌ Nouveau prompt non détecté")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur vérification: {e}")
        return False
    
    return True

def instructions_manuelles():
    """Donne les instructions pour un remplacement manuel"""
    
    print("\n📋 INSTRUCTIONS POUR REMPLACEMENT MANUEL:")
    print("   Si le script automatique échoue, voici comment procéder manuellement:")
    
    print("\n   1. 📁 Ouvrir le fichier backend_interface.py")
    print("   2. 🔍 Rechercher la fonction qui contient le prompt LLM")
    print("   3. 📝 Remplacer tout le prompt actuel par le contenu de prompt_ameliore_livraison.txt")
    print("   4. 💾 Sauvegarder le fichier")
    print("   5. 🚀 Relancer l'application")
    
    print("\n   📍 Localisation probable du prompt:")
    print("      - Chercher 'Tu es un assistant expert en extraction'")
    print("      - Ou chercher 'INSTRUCTIONS CRITIQUES POUR LES MATELAS'")
    print("      - Ou chercher 'mode_mise_a_disposition'")

def test_apres_modification():
    """Instructions pour tester après modification"""
    
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

if __name__ == "__main__":
    print("🚀 Application du nouveau prompt de livraison")
    
    # Tentative de remplacement automatique
    success = appliquer_prompt_livraison()
    
    if success:
        print("\n🎉 SUCCÈS: Nouveau prompt appliqué automatiquement !")
        print("🔧 Le prompt de livraison est maintenant amélioré")
        print("🚀 Vous pouvez tester l'application")
        
        # Instructions de test
        test_apres_modification()
        
    else:
        print("\n⚠️ Le remplacement automatique a échoué")
        print("🔧 Remplacement manuel nécessaire")
        
        # Instructions manuelles
        instructions_manuelles()
        
        # Instructions de test
        test_apres_modification()
    
    print("\n=== FIN DE L'APPLICATION ===")

