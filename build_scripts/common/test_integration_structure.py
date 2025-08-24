#!/usr/bin/env python3
"""
Test d'intégration pour la nouvelle structure du projet
"""

import sys
import os
from pathlib import Path

def test_imports():
    """Teste que tous les imports fonctionnent"""
    print("🧪 Test des imports...")
    
    try:
        # Test import app_gui
        from app_gui import LiterieApp
        print("✅ Import app_gui réussi")
    except ImportError as e:
        print(f"❌ Erreur import app_gui: {e}")
        return False
    
    try:
        # Test import admin_dialog
        from utilities.admin.admin_dialog import AdminDialog
        print("✅ Import admin_dialog réussi")
    except ImportError as e:
        print(f"❌ Erreur import admin_dialog: {e}")
        return False
    
    try:
        # Test import admin_builder_gui
        import utilities.admin.admin_builder_gui
        print("✅ Import admin_builder_gui réussi")
    except ImportError as e:
        print(f"❌ Erreur import admin_builder_gui: {e}")
        return False
    
    return True

def test_file_structure():
    """Teste que la structure de fichiers est correcte"""
    print("\n📁 Test de la structure de fichiers...")
    
    required_dirs = [
        "build_scripts",
        "build_scripts/windows",
        "build_scripts/macos",
        "build_scripts/linux",
        "build_scripts/common",
        "utilities",
        "utilities/tests",
        "utilities/admin",
        "utilities/launchers",
        "docs",
        "docs/build"
    ]
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ manquant")
            return False
    
    return True

def test_build_scripts():
    """Teste que les scripts de build sont accessibles"""
    print("\n🔨 Test des scripts de build...")
    
    build_scripts = [
        "build_scripts/common/build_complet_avec_referentiels.py",
        "build_scripts/macos/build_mac_complet.py",
        "utilities/admin/admin_builder_gui.py",
        "utilities/admin/admin_dialog.py"
    ]
    
    for script in build_scripts:
        if Path(script).exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} manquant")
            return False
    
    return True

def main():
    """Point d'entrée principal"""
    print("🔧 TEST D'INTÉGRATION - NOUVELLE STRUCTURE")
    print("=" * 50)
    
    success = True
    
    # Test de la structure
    if not test_file_structure():
        success = False
    
    # Test des scripts de build
    if not test_build_scripts():
        success = False
    
    # Test des imports
    if not test_imports():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Tous les tests d'intégration ont réussi !")
        print("✅ La nouvelle structure est opérationnelle")
    else:
        print("❌ Certains tests ont échoué")
        print("🔧 Vérifiez la structure et les imports")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
