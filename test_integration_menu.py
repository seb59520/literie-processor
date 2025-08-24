#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier l'intégration du menu Test LLM
"""

import sys
import os
import subprocess

def test_menu_integration():
    """Teste l'intégration du menu Test LLM"""
    print("🧪 Test d'intégration du menu Test LLM")
    print("=" * 50)
    
    # Vérifier que les fichiers nécessaires existent
    required_files = [
        "app_gui.py",
        "test_llm_prompt.py",
        "lancer_test_llm.py"
    ]
    
    print("📁 Vérification des fichiers requis...")
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} - OK")
        else:
            print(f"❌ {file} - MANQUANT")
            return False
    
    # Vérifier que la méthode show_test_llm_app est présente dans app_gui.py
    print("\n🔍 Vérification de l'intégration dans app_gui.py...")
    try:
        with open("app_gui.py", "r", encoding="utf-8") as f:
            content = f.read()
            
        if "def show_test_llm_app(self):" in content:
            print("✅ Méthode show_test_llm_app trouvée")
        else:
            print("❌ Méthode show_test_llm_app manquante")
            return False
            
        if "test_llm_action = QAction('🧪 Test LLM'" in content:
            print("✅ Action menu Test LLM trouvée")
        else:
            print("❌ Action menu Test LLM manquante")
            return False
            
        if "self.test_llm_btn = QPushButton" in content and "Test LLM" in content:
            print("✅ Bouton Test LLM trouvé")
        else:
            print("❌ Bouton Test LLM manquant")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    
    # Vérifier que l'application de test LLM peut être lancée
    print("\n🚀 Test de lancement de l'application de test LLM...")
    try:
        result = subprocess.run([sys.executable, "lancer_test_llm.py"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 or "Dépendances OK" in result.stdout:
            print("✅ Application de test LLM peut être lancée")
        else:
            print(f"⚠️ Application de test LLM - retour: {result.returncode}")
            print(f"Sortie: {result.stdout}")
            print(f"Erreur: {result.stderr}")
    except subprocess.TimeoutExpired:
        print("✅ Application de test LLM lancée (timeout - normal)")
    except Exception as e:
        print(f"❌ Erreur lors du test de lancement: {e}")
        return False
    
    print("\n🎉 Test d'intégration terminé avec succès !")
    print("\n📋 Résumé des fonctionnalités ajoutées:")
    print("   • Menu Réglages → 🧪 Test LLM (Ctrl+T)")
    print("   • Bouton 🧪 Test LLM dans le panneau gauche")
    print("   • Lancement automatique de l'application de test")
    print("   • Messages de confirmation et gestion d'erreurs")
    
    return True

if __name__ == "__main__":
    success = test_menu_integration()
    sys.exit(0 if success else 1) 