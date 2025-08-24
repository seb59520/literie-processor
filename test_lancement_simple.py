#!/usr/bin/env python3
"""
Test simple de lancement de l'application MatelasApp
"""

import sys
import os

def test_imports():
    """Test des imports principaux"""
    print("🧪 Test des imports...")
    
    try:
        # Test PyQt6
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtGui import QAction
        print("✅ PyQt6 importé avec succès")
    except ImportError as e:
        print(f"❌ Erreur PyQt6: {e}")
        return False
    
    try:
        # Test des modules backend
        from backend_interface import backend_interface
        print("✅ backend_interface importé")
    except ImportError as e:
        print(f"❌ Erreur backend_interface: {e}")
        return False
    
    try:
        from config import config
        print("✅ config importé")
    except ImportError as e:
        print(f"❌ Erreur config: {e}")
        return False
    
    return True

def test_application_creation():
    """Test de création de l'application"""
    print("\n🧪 Test de création de l'application...")
    
    try:
        from PyQt6.QtWidgets import QApplication
        from app_gui import MatelasApp
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        print("✅ QApplication créée")
        
        # Créer la fenêtre principale
        window = MatelasApp()
        print("✅ MatelasApp créée")
        
        # Fermer proprement
        window.close()
        app.quit()
        print("✅ Application fermée proprement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur création application: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("=" * 50)
    print("   TEST DE LANCEMENT MATELASAPP")
    print("=" * 50)
    
    # Test 1: Imports
    if not test_imports():
        print("\n❌ ÉCHEC: Problème avec les imports")
        return False
    
    # Test 2: Création de l'application
    if not test_application_creation():
        print("\n❌ ÉCHEC: Problème avec la création de l'application")
        return False
    
    print("\n✅ SUCCÈS: Tous les tests sont passés!")
    print("L'application devrait pouvoir se lancer correctement.")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 