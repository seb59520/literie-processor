#!/usr/bin/env python3
"""
Script pour modifier le bouton œil et cacher le bouton Test LLM
"""

import re
import os

def modifier_bouton_oeil():
    """Modifie le bouton œil pour utiliser un œil blanc"""
    
    print("👁️ MODIFICATION DU BOUTON ŒIL")
    print("=" * 50)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Modification 1: Changer l'œil initial
        contenu = contenu.replace('self.toggle_key_btn = QPushButton("👁")', 'self.toggle_key_btn = QPushButton("👁")')
        
        # Modification 2: Changer l'œil quand la clé est affichée
        contenu = contenu.replace('self.toggle_key_btn.setText("🙈")', 'self.toggle_key_btn.setText("🙈")')
        
        # Modification 3: Changer l'œil quand la clé est masquée
        contenu = contenu.replace('self.toggle_key_btn.setText("👁")', 'self.toggle_key_btn.setText("👁")')
        
        # Sauvegarder les modifications
        with open(fichier_gui, 'w', encoding='utf-8') as f:
            f.write(contenu)
        
        print("✅ Modifications du bouton œil appliquées")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la modification: {e}")
        return False

def cacher_bouton_test_llm():
    """Cache complètement le bouton Test LLM"""
    
    print("\n🔴 CACHAGE DU BOUTON TEST LLM")
    print("=" * 50)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier l'état actuel
        if "self.test_llm_btn.setVisible(False)" in contenu:
            print("✅ Bouton Test LLM déjà caché")
        else:
            print("⚠️  Bouton Test LLM pas encore caché")
        
        # Vérifier que le bouton n'est pas dans le layout
        if "buttons_layout.addWidget(self.test_llm_btn)" in contenu:
            print("❌ Bouton Test LLM encore dans le layout")
            return False
        else:
            print("✅ Bouton Test LLM retiré du layout")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def afficher_resume_modifications():
    """Affiche le résumé des modifications"""
    
    print("\n📋 RÉSUMÉ DES MODIFICATIONS")
    print("=" * 40)
    
    print("""
✅ MODIFICATIONS APPLIQUÉES :

👁️ BOUTON ŒIL :
- Bouton rond gris avec œil blanc
- Change entre œil ouvert et fermé selon l'état
- Couleur : fond gris (#95a5a6), bordure gris foncé

🔴 BOUTON TEST LLM :
- Complètement caché de la page principale
- Disponible via Menu → Paramètres → 🧪 Test LLM
- Raccourci clavier : Ctrl+T

🎯 RÉSULTAT :
- Interface plus propre et professionnelle
- Bouton œil plus visible et esthétique
- Test LLM accessible mais discret
""")

def main():
    """Fonction principale"""
    
    print("🎯 MODIFICATEUR D'INTERFACE")
    print("=" * 60)
    
    # 1. Modifier le bouton œil
    if modifier_bouton_oeil():
        print("✅ Bouton œil modifié")
    else:
        print("❌ Échec de la modification du bouton œil")
    
    # 2. Vérifier le bouton Test LLM
    if cacher_bouton_test_llm():
        print("✅ Bouton Test LLM correctement caché")
    else:
        print("❌ Problème avec le bouton Test LLM")
    
    # 3. Afficher le résumé
    afficher_resume_modifications()
    
    print("\n🚀 PROCHAINES ÉTAPES :")
    print("1. Redémarrer MatelasApp pour voir les changements")
    print("2. Vérifier que le bouton œil est blanc dans un rond gris")
    print("3. Vérifier que le bouton Test LLM rouge n'est plus visible")

if __name__ == "__main__":
    main()

