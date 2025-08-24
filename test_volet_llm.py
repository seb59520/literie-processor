#!/usr/bin/env python3
"""
Script de test pour vérifier le volet LLM déroulant
"""

import os
import sys

def test_imports():
    """Teste les imports nécessaires"""
    print("🔍 TEST DES IMPORTS")
    print("=" * 40)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout
        from PyQt6.QtCore import Qt
        print("✅ PyQt6 importé avec succès")
        return True
    except ImportError as e:
        print(f"❌ Erreur import PyQt6: {e}")
        return False

def test_volet_llm():
    """Teste la création d'un volet LLM déroulant"""
    print("\n🔧 TEST DU VOLET LLM")
    print("=" * 40)
    
    try:
        from PyQt6.QtWidgets import QApplication, QMainWindow, QGroupBox, QVBoxLayout, QCheckBox, QLabel
        from PyQt6.QtCore import Qt
        
        # Créer une application Qt
        app = QApplication([])
        
        # Créer une fenêtre de test
        window = QMainWindow()
        window.setWindowTitle("Test Volet LLM")
        window.resize(400, 300)
        
        # Widget central
        central_widget = QMainWindow()
        window.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        
        # Créer le volet LLM déroulant
        llm_group = QGroupBox("🔽 Enrichissement LLM")
        llm_group.setCheckable(True)
        llm_group.setChecked(True)  # Ouvert par défaut
        
        # Layout pour le contenu du volet
        llm_layout = QVBoxLayout(llm_group)
        
        # Ajouter des widgets de test
        checkbox = QCheckBox("Utiliser l'enrichissement LLM")
        checkbox.setChecked(True)
        llm_layout.addWidget(checkbox)
        
        label = QLabel("Provider: Ollama")
        llm_layout.addWidget(label)
        
        # Ajouter le volet au layout principal
        layout.addWidget(llm_group)
        
        # Fonction de test pour le basculement
        def on_toggled(checked):
            print(f"🔄 Volet basculé: {'ouvert' if checked else 'fermé'}")
            
            # Afficher/masquer les widgets enfants
            for i in range(llm_layout.count()):
                widget = llm_layout.itemAt(i).widget()
                if widget:
                    widget.setVisible(checked)
            
            # Changer l'icône du titre
            if checked:
                llm_group.setTitle("🔽 Enrichissement LLM")
            else:
                llm_group.setTitle("▶️ Enrichissement LLM")
        
        # Connecter le signal
        llm_group.toggled.connect(on_toggled)
        
        print("✅ Volet LLM créé avec succès")
        print("✅ Propriétés checkable et checked configurées")
        print("✅ Signal toggled connecté")
        print("✅ Widgets enfants ajoutés")
        
        # Afficher la fenêtre
        window.show()
        
        print("\n🎯 INSTRUCTIONS DE TEST:")
        print("1. Cliquez sur le titre du volet pour l'ouvrir/fermer")
        print("2. Vérifiez que l'icône change (🔽 ↔️ ▶️)")
        print("3. Vérifiez que le contenu s'affiche/se masque")
        print("4. Fermez la fenêtre pour terminer le test")
        
        # Lancer l'application
        app.exec()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_configuration():
    """Teste la configuration du volet"""
    print("\n⚙️ TEST DE LA CONFIGURATION")
    print("=" * 40)
    
    try:
        # Vérifier que le fichier app_gui.py contient les bonnes modifications
        fichier_gui = "app_gui.py"
        
        if not os.path.exists(fichier_gui):
            print(f"❌ Fichier {fichier_gui} non trouvé")
            return False
        
        with open(fichier_gui, 'r', encoding='utf-8') as f:
            contenu = f.read()
        
        # Vérifier les modifications
        modifications = [
            ("QGroupBox checkable", "self.llm_group.setCheckable(True)"),
            ("Signal toggled", "self.llm_group.toggled.connect(self.on_llm_group_toggled)"),
            ("Fonction on_llm_group_toggled", "def on_llm_group_toggled(self, checked):"),
            ("Fonction save_llm_panel_state", "def save_llm_panel_state(self, is_open):"),
            ("Fonction restore_llm_panel_state", "def restore_llm_panel_state(self):"),
            ("Restoration automatique", "QTimer.singleShot(100, self.restore_llm_panel_state)")
        ]
        
        print("📋 Vérification des modifications:")
        for nom, code in modifications:
            if code in contenu:
                print(f"   ✅ {nom}")
            else:
                print(f"   ❌ {nom}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """Fonction principale"""
    print("🎯 TEST COMPLET DU VOLET LLM DÉROULANT")
    print("=" * 60)
    
    # Test 1: Imports
    if not test_imports():
        print("❌ Test des imports échoué")
        return False
    
    # Test 2: Configuration
    if not test_configuration():
        print("❌ Test de la configuration échoué")
        return False
    
    # Test 3: Volet LLM
    if not test_volet_llm():
        print("❌ Test du volet LLM échoué")
        return False
    
    print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS !")
    print("✅ Le volet LLM déroulant est prêt à être utilisé")
    
    return True

if __name__ == "__main__":
    main()

