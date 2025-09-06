#!/usr/bin/env python3
"""
Lanceur simplifié MATELAS - Pour tests et dépannage
"""

import sys
import os
from pathlib import Path

def main():
    print("🚀 MATELAS v3.11.12 - Lanceur Simplifié")
    print("=" * 40)
    
    # Vérifications de base
    print(f"📂 Répertoire: {Path.cwd()}")
    print(f"🐍 Python: {sys.version}")
    
    # Test des imports critiques
    try:
        print("🔍 Test des imports...")
        import PyQt6
        print("  ✅ PyQt6")
        
        import requests
        print("  ✅ requests")
        
        import config
        print("  ✅ config")
        
        import version
        print("  ✅ version")
        
    except ImportError as e:
        print(f"  ❌ Import manquant: {e}")
        print("\n🔧 Exécutez: python install.py")
        input("Appuyez sur Entrée...")
        return False
    
    # Lancer l'application
    print("\n🚀 Lancement de l'application...")
    
    try:
        # Import et lancement
        from PyQt6.QtWidgets import QApplication
        
        # Créer l'application Qt
        app = QApplication(sys.argv)
        
        # Import de l'interface principale
        import app_gui
        
        # Lancer l'interface
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur de lancement: {e}")
        print("\n📋 Informations de débogage:")
        print(f"   • Répertoire: {os.getcwd()}")
        print(f"   • Python: {sys.executable}")
        
        # Afficher la trace complète
        import traceback
        traceback.print_exc()
        
        input("\nAppuyez sur Entrée pour fermer...")
        return False

if __name__ == "__main__":
    main()
