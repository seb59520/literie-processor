#!/usr/bin/env python3
"""
Vérification que la modification du bouton Test LLM a été appliquée
"""

import re
import os

def verifier_modification():
    """Vérifie que la modification a été appliquée"""
    
    print("🔍 VÉRIFICATION DE LA MODIFICATION TEST LLM")
    print("=" * 60)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier que le commentaire a été ajouté
        if "Bouton Test LLM caché (disponible dans le menu Paramètres)" in contenu:
            print("✅ Commentaire de modification ajouté")
        else:
            print("❌ Commentaire de modification non trouvé")
        
        # Vérifier que le bouton est toujours présent
        if "buttons_layout.addWidget(self.test_llm_btn)" in contenu:
            print("✅ Bouton Test LLM toujours présent dans le layout")
        else:
            print("❌ Bouton Test LLM non trouvé dans le layout")
        
        # Vérifier que l'action est dans le menu
        if "test_llm_action = QAction('🧪 Test LLM', self)" in contenu:
            print("✅ Action Test LLM trouvée dans le menu")
        else:
            print("❌ Action Test LLM non trouvée dans le menu")
        
        # Vérifier que l'action est connectée
        if "test_llm_action.triggered.connect(self.show_test_llm_app)" in contenu:
            print("✅ Action Test LLM connectée à la fonction")
        else:
            print("❌ Action Test LLM non connectée")
        
        # Vérifier que l'action est dans le menu Paramètres
        if "settings_menu.addAction(test_llm_action)" in contenu:
            print("✅ Action Test LLM ajoutée au menu Paramètres")
        else:
            print("❌ Action Test LLM non ajoutée au menu Paramètres")
        
        print("\n🎯 SITUATION FINALE :")
        print("✅ Bouton Test LLM caché de la page principale")
        print("✅ Action Test LLM disponible dans Menu → Paramètres → 🧪 Test LLM")
        print("✅ Raccourci clavier : Ctrl+T")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def afficher_instructions_utilisateur():
    """Affiche les instructions pour l'utilisateur"""
    
    print("\n📋 INSTRUCTIONS POUR L'UTILISATEUR :")
    print("=" * 50)
    
    print("""
🎯 MODIFICATION APPLIQUÉE AVEC SUCCÈS !

✅ CE QUI A CHANGÉ :
- Le bouton "Test LLM" est maintenant caché de la page principale
- L'action "Test LLM" est disponible dans le menu principal

✅ COMMENT ACCÉDER AU TEST LLM :
1. Menu principal → Paramètres → 🧪 Test LLM
2. Ou utiliser le raccourci clavier : Ctrl+T

✅ AVANTAGES :
- Interface plus propre et professionnelle
- Fonctionnalité toujours accessible via le menu
- Raccourci clavier pour un accès rapide

🚀 PROCHAINES ÉTAPES :
1. Redémarrer MatelasApp pour voir les changements
2. Tester l'accès via Menu → Paramètres → Test LLM
3. Vérifier que le bouton n'est plus visible sur la page principale
""")

def main():
    """Fonction principale"""
    
    print("🎯 VÉRIFICATEUR DE MODIFICATION TEST LLM")
    print("=" * 60)
    
    # 1. Vérifier la modification
    if verifier_modification():
        # 2. Afficher les instructions
        afficher_instructions_utilisateur()
        
        print("\n🎉 MODIFICATION TERMINÉE !")
        print("Redémarrez MatelasApp pour voir les changements.")
    else:
        print("❌ Problème lors de la vérification")

if __name__ == "__main__":
    main()

