#!/usr/bin/env python3
"""
Script pour déplacer le bouton "Test LLM" dans le menu principal
au lieu de l'afficher sur la page principale
"""

import re
import os

def deplacer_test_llm_menu():
    """Déplace le bouton Test LLM dans le menu principal"""
    
    print("🔄 DÉPLACEMENT DU BOUTON TEST LLM DANS LE MENU")
    print("=" * 60)
    
    fichier_gui = "app_gui.py"
    
    if not os.path.exists(fichier_gui):
        print(f"❌ Fichier {fichier_gui} non trouvé")
        return False
    
    try:
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        print("📋 Analyse du fichier app_gui.py...")
        
        # Vérifier si le bouton Test LLM existe sur la page principale
        if 'test_llm_button' in contenu:
            print("✅ Bouton Test LLM trouvé sur la page principale")
        else:
            print("⚠️  Bouton Test LLM non trouvé sur la page principale")
        
        # Vérifier si le menu principal existe
        if 'QMenuBar' in contenu or 'menuBar()' in contenu:
            print("✅ Menu principal trouvé")
        else:
            print("⚠️  Menu principal non trouvé")
        
        # Chercher la création du bouton Test LLM
        pattern_bouton = r'(test_llm_button\s*=\s*QPushButton\([^)]+\))'
        match_bouton = re.search(pattern_bouton, contenu)
        
        if match_bouton:
            print("✅ Création du bouton Test LLM trouvée")
            bouton_creation = match_bouton.group(1)
            print(f"   📝 {bouton_creation[:50]}...")
        else:
            print("❌ Création du bouton Test LLM non trouvée")
        
        # Chercher l'ajout du bouton au layout principal
        pattern_layout = r'(self\.test_llm_button\.setParent\([^)]+\)|self\.test_llm_button\.setGeometry\([^)]+\)|layout.*addWidget.*test_llm_button)'
        match_layout = re.search(pattern_layout, contenu)
        
        if match_layout:
            print("✅ Positionnement du bouton Test LLM trouvé")
            layout_info = match_layout.group(1)
            print(f"   📝 {layout_info[:50]}...")
        else:
            print("❌ Positionnement du bouton Test LLM non trouvé")
        
        # Chercher le menu principal
        pattern_menu = r'(menuBar\(\)|QMenuBar|self\.menuBar)'
        match_menu = re.search(pattern_menu, contenu)
        
        if match_menu:
            print("✅ Menu principal trouvé")
            menu_info = match_menu.group(1)
            print(f"   📝 {menu_info}")
        else:
            print("❌ Menu principal non trouvé")
        
        print("\n🎯 PLAN DE MODIFICATION :")
        print("1. Créer un menu 'Outils' ou 'Développement'")
        print("2. Ajouter une action 'Test LLM' dans ce menu")
        print("3. Cacher le bouton de la page principale")
        print("4. Connecter l'action du menu à la fonction de test")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {e}")
        return False

def afficher_modifications_suggestees():
    """Affiche les modifications suggérées"""
    
    print("\n📝 MODIFICATIONS SUGGÉRÉES :")
    print("=" * 40)
    
    print("""
🔧 MODIFICATION 1 - Créer le menu Outils :
```python
# Dans __init__ ou setup_ui
self.menu_bar = self.menuBar()
self.outils_menu = self.menu_bar.addMenu('Outils')
self.test_llm_action = self.outils_menu.addAction('Test LLM')
self.test_llm_action.triggered.connect(self.test_llm)
```

🔧 MODIFICATION 2 - Cacher le bouton principal :
```python
# Remplacer l'affichage du bouton par :
self.test_llm_button.hide()  # ou .setVisible(False)
```

🔧 MODIFICATION 3 - Optionnel : Condition d'affichage :
```python
# Pour afficher seulement en mode développeur
if self.debug_mode:
    self.outils_menu.setVisible(True)
else:
    self.outils_menu.setVisible(False)
```
""")

def main():
    """Fonction principale"""
    
    print("🎯 GESTIONNAIRE DU BOUTON TEST LLM")
    print("=" * 60)
    
    # 1. Analyser le fichier actuel
    if deplacer_test_llm_menu():
        # 2. Afficher les modifications suggérées
        afficher_modifications_suggestees()
        
        print("\n🎯 PROCHAINES ÉTAPES :")
        print("1. Voulez-vous que j'applique ces modifications ?")
        print("2. Ou préférez-vous les faire manuellement ?")
        print("3. Souhaitez-vous d'abord voir le code actuel ?")
    else:
        print("❌ Impossible d'analyser le fichier")

if __name__ == "__main__":
    main()

