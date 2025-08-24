#!/usr/bin/env python3
"""
Script de mise à jour de l'application principale pour la nouvelle structure
Met à jour les imports et chemins pour la structure réorganisée
"""

import os
import re
from pathlib import Path

def update_app_gui_imports():
    """Met à jour les imports dans app_gui.py"""
    
    if not Path("app_gui.py").exists():
        print("❌ app_gui.py non trouvé")
        return False
    
    with open("app_gui.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Mise à jour des imports pour la nouvelle structure
    import_updates = {
        # Admin Builder
        "from admin_dialog import show_admin_dialog": "from utilities.admin.admin_dialog import show_admin_dialog",
        "import admin_builder_gui": "import utilities.admin.admin_builder_gui as admin_builder_gui",
        
        # Tests
        "from test_eula_inclusion import": "from utilities.tests.test_eula_inclusion import",
        "from test_integration_admin_builder import": "from utilities.tests.test_integration_admin_builder import",
        
        # Configuration
        "from mapping_config_dialog_qt import": "from utilities.admin.mapping_config_dialog_qt import",
    }
    
    # Appliquer les mises à jour
    for old_import, new_import in import_updates.items():
        if old_import in content:
            content = content.replace(old_import, new_import)
            print(f"✅ Mis à jour: {old_import} → {new_import}")
    
    # Mise à jour des chemins de fichiers
    path_updates = {
        "admin_builder_gui.py": "utilities/admin/admin_builder_gui.py",
        "admin_dialog.py": "utilities/admin/admin_dialog.py",
        "test_eula_inclusion.py": "utilities/tests/test_eula_inclusion.py",
        "test_integration_admin_builder.py": "utilities/tests/test_integration_admin_builder.py",
        "mapping_config_dialog_qt.py": "utilities/admin/mapping_config_dialog_qt.py",
    }
    
    for old_path, new_path in path_updates.items():
        # Rechercher les références de fichiers dans les chaînes
        pattern = f'["\']{re.escape(old_path)}["\']'
        if re.search(pattern, content):
            content = re.sub(pattern, f'"{new_path}"', content)
            print(f"✅ Mis à jour chemin: {old_path} → {new_path}")
    
    # Sauvegarder les modifications
    with open("app_gui.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ app_gui.py mis à jour")
    return True

def update_admin_dialog_imports():
    """Met à jour les imports dans admin_dialog.py"""
    
    admin_dialog_path = Path("utilities/admin/admin_dialog.py")
    if not admin_dialog_path.exists():
        print("❌ utilities/admin/admin_dialog.py non trouvé")
        return False
    
    with open(admin_dialog_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Mise à jour des imports
    import_updates = {
        "import admin_builder_gui": "import utilities.admin.admin_builder_gui as admin_builder_gui",
        "from test_eula_inclusion import": "from utilities.tests.test_eula_inclusion import",
    }
    
    for old_import, new_import in import_updates.items():
        if old_import in content:
            content = content.replace(old_import, new_import)
            print(f"✅ Mis à jour: {old_import} → {new_import}")
    
    # Sauvegarder les modifications
    with open(admin_dialog_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("✅ admin_dialog.py mis à jour")
    return True

def update_build_scripts():
    """Met à jour les scripts de build pour inclure les nouveaux répertoires"""
    
    build_scripts = [
        "build_scripts/common/build_complet_avec_referentiels.py",
        "build_scripts/macos/build_mac_complet.py",
        "build_scripts/windows/build_windows_optimized.py"
    ]
    
    for script_path in build_scripts:
        if not Path(script_path).exists():
            continue
        
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Ajouter les nouveaux répertoires aux données à inclure
        new_data_dirs = [
            ("utilities", "utilities"),
            ("docs", "docs"),
            ("build_scripts", "build_scripts")
        ]
        
        # Rechercher la section data_dirs et ajouter les nouveaux répertoires
        if "data_dirs = [" in content:
            # Trouver la fin de la liste data_dirs
            start = content.find("data_dirs = [")
            end = content.find("]", start)
            
            if end != -1:
                # Extraire la liste existante
                existing_list = content[start:end+1]
                
                # Ajouter les nouveaux répertoires
                new_dirs_str = ""
                for src, dest in new_data_dirs:
                    new_dirs_str += f'        ("{src}", "{dest}"),\n'
                
                # Insérer les nouveaux répertoires avant la fermeture de la liste
                updated_list = existing_list.replace("]", f"{new_dirs_str}    ]")
                content = content.replace(existing_list, updated_list)
                
                print(f"✅ Mis à jour {script_path} avec les nouveaux répertoires")
        
        # Sauvegarder les modifications
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(content)

def create_integration_test():
    """Crée un script de test pour vérifier l'intégration"""
    
    test_content = """#!/usr/bin/env python3
\"\"\"
Test d'intégration pour la nouvelle structure du projet
\"\"\"

import sys
import os
from pathlib import Path

def test_imports():
    \"\"\"Teste que tous les imports fonctionnent\"\"\"
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
    \"\"\"Teste que la structure de fichiers est correcte\"\"\"
    print("\\n📁 Test de la structure de fichiers...")
    
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
    \"\"\"Teste que les scripts de build sont accessibles\"\"\"
    print("\\n🔨 Test des scripts de build...")
    
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
    \"\"\"Point d'entrée principal\"\"\"
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
    
    print("\\n" + "=" * 50)
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
"""
    
    with open("test_integration_structure.py", "w", encoding="utf-8") as f:
        f.write(test_content)
    
    print("✅ Script de test d'intégration créé")

def main():
    """Point d'entrée principal"""
    print("🔧 MISE À JOUR DE L'INTÉGRATION")
    print("=" * 40)
    print()
    
    # Mettre à jour app_gui.py
    print("📱 Mise à jour de app_gui.py...")
    if not update_app_gui_imports():
        print("⚠️ Impossible de mettre à jour app_gui.py")
    
    print()
    
    # Mettre à jour admin_dialog.py
    print("🔐 Mise à jour de admin_dialog.py...")
    if not update_admin_dialog_imports():
        print("⚠️ Impossible de mettre à jour admin_dialog.py")
    
    print()
    
    # Mettre à jour les scripts de build
    print("🔨 Mise à jour des scripts de build...")
    update_build_scripts()
    
    print()
    
    # Créer le script de test d'intégration
    print("🧪 Création du script de test d'intégration...")
    create_integration_test()
    
    print()
    print("🎉 Mise à jour de l'intégration terminée !")
    print()
    print("📋 Prochaines étapes :")
    print("1. Exécutez : python reorganize_project.py")
    print("2. Exécutez : python test_integration_structure.py")
    print("3. Testez l'application : python app_gui.py")

if __name__ == "__main__":
    main() 