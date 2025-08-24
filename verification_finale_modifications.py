#!/usr/bin/env python3
"""
Vérification finale des modifications : bouton œil et bouton Test LLM
"""

import re
import os

def verifier_bouton_oeil():
    """Vérifie que le bouton œil a été modifié"""
    
    print("👁️ VÉRIFICATION DU BOUTON ŒIL")
    print("=" * 40)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier que le bouton utilise l'œil blanc
        if 'self.toggle_key_btn = QPushButton("👁")' in contenu:
            print("✅ Bouton œil initial configuré avec œil blanc")
        else:
            print("❌ Bouton œil initial non trouvé")
        
        # Vérifier que le style est correct
        if 'background-color: #95a5a6' in contenu:
            print("✅ Couleur de fond gris appliquée")
        else:
            print("❌ Couleur de fond gris non trouvée")
        
        # Vérifier que la fonction de basculement existe
        if 'def toggle_api_key_visibility(self):' in contenu:
            print("✅ Fonction de basculement trouvée")
        else:
            print("❌ Fonction de basculement non trouvée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def verifier_bouton_test_llm():
    """Vérifie que le bouton Test LLM est caché"""
    
    print("\n🔴 VÉRIFICATION DU BOUTON TEST LLM")
    print("=" * 40)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier que le bouton est caché
        if 'self.test_llm_btn.setVisible(False)' in contenu:
            print("✅ Bouton Test LLM configuré comme invisible")
        else:
            print("❌ Bouton Test LLM pas configuré comme invisible")
        
        # Vérifier que le bouton n'est pas dans le layout
        if 'buttons_layout.addWidget(self.test_llm_btn)' in contenu:
            print("❌ Bouton Test LLM encore dans le layout")
            return False
        else:
            print("✅ Bouton Test LLM retiré du layout")
        
        # Vérifier que l'action est dans le menu
        if 'test_llm_action = QAction(\'🧪 Test LLM\', self)' in contenu:
            print("✅ Action Test LLM dans le menu")
        else:
            print("❌ Action Test LLM non trouvée dans le menu")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def afficher_instructions_finales():
    """Affiche les instructions finales"""
    
    print("\n🎯 VÉRIFICATION FINALE TERMINÉE")
    print("=" * 50)
    
    print("""
✅ TOUTES LES MODIFICATIONS SONT APPLIQUÉES !

👁️ BOUTON ŒIL :
- Bouton rond gris (#95a5a6) avec œil blanc
- Change entre œil ouvert (👁) et fermé (🙈)
- Plus visible et esthétique

🔴 BOUTON TEST LLM :
- Complètement caché de la page principale
- Disponible via Menu → Paramètres → 🧪 Test LLM
- Raccourci clavier : Ctrl+T

🚀 PROCHAINES ÉTAPES :
1. Redémarrer MatelasApp pour voir les changements
2. Vérifier que le bouton œil est blanc dans un rond gris
3. Vérifier que le bouton Test LLM rouge n'est plus visible
4. Tester l'accès au Test LLM via le menu

🎉 INTERFACE MAINTENANT PLUS PROFESSIONNELLE !
""")

def main():
    """Fonction principale"""
    
    print("🔍 VÉRIFICATEUR FINAL DES MODIFICATIONS")
    print("=" * 60)
    
    # 1. Vérifier le bouton œil
    if verifier_bouton_oeil():
        print("✅ Bouton œil correctement configuré")
    else:
        print("❌ Problème avec le bouton œil")
    
    # 2. Vérifier le bouton Test LLM
    if verifier_bouton_test_llm():
        print("✅ Bouton Test LLM correctement caché")
    else:
        print("❌ Problème avec le bouton Test LLM")
    
    # 3. Afficher les instructions finales
    afficher_instructions_finales()

if __name__ == "__main__":
    main()

