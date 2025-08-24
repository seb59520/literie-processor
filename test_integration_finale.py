#!/usr/bin/env python3
"""
Test d'intégration finale après la réorganisation du projet
"""

import sys
import os
from pathlib import Path

def test_structure():
    """Teste que la structure est correcte"""
    print("📁 Test de la structure de fichiers...")
    
    required_dirs = [
        "build_scripts",
        "build_scripts/windows",
        "build_scripts/macos", 
        "build_scripts/linux",
        "build_scripts/common",
        "utilities",
        "utilities/admin",
        "utilities/launchers",
        "utilities/tests",
        "docs",
        "docs/build",
        "docs/admin",
        "docs/installation"
    ]
    
    for directory in required_dirs:
        if Path(directory).exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ manquant")
            return False
    
    return True

def test_key_files():
    """Teste que les fichiers clés sont présents"""
    print("\n🔑 Test des fichiers clés...")
    
    key_files = [
        "app_gui.py",
        "utilities/admin/admin_dialog.py",
        "utilities/admin/admin_builder_gui.py",
        "build_scripts/common/build_complet_avec_referentiels.py",
        "build_scripts/macos/build_mac_complet.py",
        "build_launcher.bat",
        "build_launcher.sh",
        "README_STRUCTURE.md"
    ]
    
    for file in key_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} manquant")
            return False
    
    return True

def test_imports():
    """Teste que les imports fonctionnent"""
    print("\n🧪 Test des imports...")
    
    try:
        # Test import de l'application principale
        sys.path.insert(0, str(Path.cwd()))
        from app_gui import MatelasApp
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

def test_build_scripts():
    """Teste que les scripts de build sont accessibles"""
    print("\n🔨 Test des scripts de build...")
    
    build_scripts = [
        "build_scripts/common/build_complet_avec_referentiels.py",
        "build_scripts/macos/build_mac_complet.py",
        "build_scripts/windows/build_windows_optimized.bat"
    ]
    
    for script in build_scripts:
        if Path(script).exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} manquant")
            return False
    
    return True

def test_launchers():
    """Teste que les lanceurs sont fonctionnels"""
    print("\n🚀 Test des lanceurs...")
    
    launchers = [
        "build_launcher.bat",
        "build_launcher.sh"
    ]
    
    for launcher in launchers:
        if Path(launcher).exists():
            print(f"✅ {launcher}")
        else:
            print(f"❌ {launcher} manquant")
            return False
    
    # Vérifier que le script shell est exécutable
    if os.access("build_launcher.sh", os.X_OK):
        print("✅ build_launcher.sh est exécutable")
    else:
        print("⚠️ build_launcher.sh n'est pas exécutable")
    
    return True

def test_documentation():
    """Teste que la documentation est présente"""
    print("\n📚 Test de la documentation...")
    
    doc_files = [
        "README_STRUCTURE.md",
        "docs/build/RESUME_REORGANISATION_PROJET.md"
    ]
    
    for doc in doc_files:
        if Path(doc).exists():
            print(f"✅ {doc}")
        else:
            print(f"❌ {doc} manquant")
            return False
    
    return True

def main():
    """Point d'entrée principal"""
    print("🔧 TEST D'INTÉGRATION FINALE - RÉORGANISATION")
    print("=" * 60)
    
    success = True
    
    # Test de la structure
    if not test_structure():
        success = False
    
    # Test des fichiers clés
    if not test_key_files():
        success = False
    
    # Test des imports
    if not test_imports():
        success = False
    
    # Test des scripts de build
    if not test_build_scripts():
        success = False
    
    # Test des lanceurs
    if not test_launchers():
        success = False
    
    # Test de la documentation
    if not test_documentation():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUS LES TESTS D'INTÉGRATION ONT RÉUSSI !")
        print("✅ La réorganisation est complète et fonctionnelle")
        print("\n📋 Utilisation :")
        print("   Windows : build_launcher.bat")
        print("   macOS/Linux : ./build_launcher.sh")
        print("   Application : python3 app_gui.py")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez la structure et les imports")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 