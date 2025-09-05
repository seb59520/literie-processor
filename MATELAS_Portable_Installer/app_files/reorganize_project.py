#!/usr/bin/env python3
"""
Script de réorganisation du projet MatelasApp
Déplace tous les scripts de build et utilitaires dans des répertoires dédiés
"""

import os
import shutil
import sys
from pathlib import Path

def create_directory_structure():
    """Crée la nouvelle structure de répertoires"""
    directories = [
        "build_scripts/",
        "build_scripts/windows/",
        "build_scripts/macos/",
        "build_scripts/linux/",
        "build_scripts/common/",
        "utilities/",
        "utilities/tests/",
        "utilities/admin/",
        "utilities/launchers/",
        "docs/",
        "docs/build/",
        "docs/admin/",
        "docs/installation/"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Créé: {directory}")

def move_build_scripts():
    """Déplace les scripts de build dans les répertoires appropriés"""
    
    # Scripts Windows
    windows_scripts = [
        "build_*.bat",
        "build_windows_*.py",
        "build_standalone_*.py",
        "build_debug_*.py",
        "build_robust.py",
        "build_simple.bat",
        "build_ultra_simple.bat",
        "build_with_*.py",
        "build_with_*.bat",
        "fix_windows_*.py",
        "fix_windows_*.bat",
        "setup_windows.py",
        "setup_windows.bat",
        "install_windows.bat",
        "install_simple.bat",
        "install_simple_alt.bat",
        "prepare_dist.bat",
        "create_*.bat",
        "create_*.py",
        "debug_windows.bat",
        "debug_console.bat",
        "deep_debug.bat",
        "diagnostic_windows.bat",
        "fix_windows.bat",
        "fix.bat",
        "generer_documentation.bat",
        "launch_*.bat",
        "Lancer_*.bat"
    ]
    
    # Scripts macOS
    macos_scripts = [
        "build_mac_*.py",
        "build_matelas_optimized.sh",
        "generer_documentation.sh",
        "setup_custom.py",
        "setup_debug.py",
        "setup_simple.py",
        "setup.py",
        "install.py",
        "launch.py",
        "run_gui_*.py"
    ]
    
    # Scripts Linux
    linux_scripts = [
        "build_cross_platform.py",
        "build_universal.py"
    ]
    
    # Scripts communs
    common_scripts = [
        "build_complet_avec_referentiels.py",
        "build_test_rapide.py",
        "build_final_solution.py",
        "build_installer.py",
        "build_package_*.py",
        "create_package_*.py",
        "create_standalone_*.py",
        "deploy_patch.py",
        "migrer_cles_api.py",
        "reset_noyau_order.py",
        "fix_all_indentation.py",
        "fix_app_gui_imports.py",
        "fix_executable_*.py",
        "fix_imports_*.py",
        "fix_relative_imports.py",
        "fix_app_gui_imports.py",
        "corriger_*.py",
        "test_*.py",
        "diagnostic_*.py",
        "find_openrouter_balance.py"
    ]
    
    # Déplacer les scripts Windows
    for pattern in windows_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("build_scripts/windows") / file.name
                shutil.move(str(file), str(dest))
                print(f"📁 Déplacé: {file.name} → build_scripts/windows/")
    
    # Déplacer les scripts macOS
    for pattern in macos_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("build_scripts/macos") / file.name
                shutil.move(str(file), str(dest))
                print(f"🍎 Déplacé: {file.name} → build_scripts/macos/")
    
    # Déplacer les scripts Linux
    for pattern in linux_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("build_scripts/linux") / file.name
                shutil.move(str(file), str(dest))
                print(f"🐧 Déplacé: {file.name} → build_scripts/linux/")
    
    # Déplacer les scripts communs
    for pattern in common_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("build_scripts/common") / file.name
                shutil.move(str(file), str(dest))
                print(f"🔧 Déplacé: {file.name} → build_scripts/common/")

def move_utility_scripts():
    """Déplace les scripts utilitaires"""
    
    # Scripts de test
    test_scripts = [
        "test_*.py"
    ]
    
    # Scripts d'administration
    admin_scripts = [
        "admin_*.py",
        "mapping_config_dialog_qt.py"
    ]
    
    # Scripts de lancement
    launcher_scripts = [
        "build_launcher.*",
        "launch_*.py",
        "run_*.py"
    ]
    
    # Déplacer les scripts de test
    for pattern in test_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("utilities/tests") / file.name
                shutil.move(str(file), str(dest))
                print(f"🧪 Déplacé: {file.name} → utilities/tests/")
    
    # Déplacer les scripts d'administration
    for pattern in admin_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("utilities/admin") / file.name
                shutil.move(str(file), str(dest))
                print(f"🔐 Déplacé: {file.name} → utilities/admin/")
    
    # Déplacer les scripts de lancement
    for pattern in launcher_scripts:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("utilities/launchers") / file.name
                shutil.move(str(file), str(dest))
                print(f"🚀 Déplacé: {file.name} → utilities/launchers/")

def move_documentation():
    """Déplace la documentation"""
    
    # Documentation de build
    build_docs = [
        "GUIDE_*.md",
        "README_*.md",
        "RESUME_*.md",
        "SOLUTION_*.md",
        "SPECIFICATIONS_*.md",
        "SYNTHESE_*.md",
        "CAHIER_*.md",
        "CHANGELOG.md",
        "CORRECTION_*.md",
        "DEPANNAGE_*.md",
        "INSTRUCTIONS_*.md",
        "INFORMATIONS_*.md",
        "NOUVEAUX_*.md",
        "REGLE_*.md",
        "STOCKAGE_*.md",
        "TEST_*.md"
    ]
    
    # Déplacer la documentation de build
    for pattern in build_docs:
        for file in Path(".").glob(pattern):
            if file.is_file():
                dest = Path("docs/build") / file.name
                shutil.move(str(file), str(dest))
                print(f"📚 Déplacé: {file.name} → docs/build/")

def create_launcher_scripts():
    """Crée des scripts de lancement adaptés à la nouvelle structure"""
    
    # Script de lancement principal Windows
    main_launcher_windows = """@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    🔨 LANCEUR DE BUILD MATELAS APP
echo ========================================
echo.
echo 📁 Nouvelle structure organisée
echo.
echo Options disponibles :
echo 1. 🔨 Build complet (Windows)
echo 2. 🍎 Build Mac
echo 3. 🧪 Tests
echo 4. 🔧 Administration
echo 5. 📚 Documentation
echo 6. ❌ Quitter
echo.
set /p choice="Choisissez une option (1-6) : "

if "%choice%"=="1" (
    cd build_scripts\\windows
    call build_launcher.bat
) else if "%choice%"=="2" (
    cd build_scripts\\macos
    python3 build_mac_complet.py
) else if "%choice%"=="3" (
    cd utilities\\tests
    python3 test_eula_inclusion.py
) else if "%choice%"=="4" (
    cd utilities\\admin
    python3 admin_builder_gui.py
) else if "%choice%"=="5" (
    start docs\\build
) else if "%choice%"=="6" (
    echo Au revoir !
    exit /b 0
) else (
    echo Choix invalide
)
pause
"""
    
    with open("build_launcher.bat", "w", encoding="utf-8") as f:
        f.write(main_launcher_windows)
    
    # Script de lancement principal Unix
    main_launcher_unix = """#!/bin/bash

# Couleurs
RED='\\033[0;31m'
GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
NC='\\033[0m'

echo -e "${BLUE}"
echo "========================================"
echo "    🔨 LANCEUR DE BUILD MATELAS APP"
echo "========================================"
echo -e "${NC}"
echo
echo "📁 Nouvelle structure organisée"
echo
echo "Options disponibles :"
echo "1. 🔨 Build complet (Cross-platform)"
echo "2. 🍎 Build Mac"
echo "3. 🧪 Tests"
echo "4. 🔧 Administration"
echo "5. 📚 Documentation"
echo "6. ❌ Quitter"
echo
read -p "Choisissez une option (1-6) : " choice

case $choice in
    1) cd build_scripts/common && python3 build_complet_avec_referentiels.py ;;
    2) cd build_scripts/macos && python3 build_mac_complet.py ;;
    3) cd utilities/tests && python3 test_eula_inclusion.py ;;
    4) cd utilities/admin && python3 admin_builder_gui.py ;;
    5) open docs/build 2>/dev/null || xdg-open docs/build 2>/dev/null || echo "Ouvrez manuellement le dossier docs/build" ;;
    6) echo "Au revoir !"; exit 0 ;;
    *) echo "Choix invalide" ;;
esac
"""
    
    with open("build_launcher.sh", "w", encoding="utf-8") as f:
        f.write(main_launcher_unix)
    
    # Rendre le script Unix exécutable
    os.chmod("build_launcher.sh", 0o755)
    
    print("✅ Scripts de lancement créés")

def create_readme_structure():
    """Crée un README expliquant la nouvelle structure"""
    
    readme_content = """# Structure du Projet MatelasApp

## 📁 Organisation des répertoires

### 🔨 build_scripts/
Scripts de construction de l'application

- **windows/** - Scripts spécifiques à Windows (.bat, .py)
- **macos/** - Scripts spécifiques à macOS (.py, .sh)
- **linux/** - Scripts spécifiques à Linux (.py)
- **common/** - Scripts multi-plateformes

### 🛠️ utilities/
Scripts utilitaires

- **tests/** - Scripts de test et validation
- **admin/** - Scripts d'administration et configuration
- **launchers/** - Scripts de lancement spécialisés

### 📚 docs/
Documentation du projet

- **build/** - Documentation des builds et installation
- **admin/** - Documentation d'administration
- **installation/** - Guides d'installation

## 🚀 Utilisation

### Windows
```batch
build_launcher.bat
```

### macOS/Linux
```bash
./build_launcher.sh
```

## 📋 Scripts principaux

### Build
- `build_complet_avec_referentiels.py` - Build complet avec tous les référentiels
- `build_mac_complet.py` - Build package .app pour macOS
- `build_test_rapide.py` - Build de test rapide

### Administration
- `admin_builder_gui.py` - Interface d'administration
- `admin_dialog.py` - Dialogue d'administration

### Tests
- `test_eula_inclusion.py` - Test de l'inclusion EULA
- `test_integration_admin_builder.py` - Test d'intégration Admin Builder

## 🔧 Intégration dans l'application

L'application principale (`app_gui.py`) peut maintenant accéder aux scripts via :

```python
# Pour l'Admin Builder
from utilities.admin.admin_builder_gui import AdminBuilderGUI

# Pour les tests
from utilities.tests.test_eula_inclusion import test_eula_inclusion
```

## 📦 Build avec la nouvelle structure

Les scripts de build ont été mis à jour pour inclure les nouveaux répertoires dans l'exécutable final.
"""
    
    with open("README_STRUCTURE.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    
    print("✅ README de structure créé")

def update_build_scripts():
    """Met à jour les scripts de build pour la nouvelle structure"""
    
    # Mettre à jour les imports dans les scripts de build
    build_script_updates = {
        "build_complet_avec_referentiels.py": {
            "old_imports": [
                "from admin_dialog import show_admin_dialog",
                "import admin_builder_gui"
            ],
            "new_imports": [
                "from utilities.admin.admin_dialog import show_admin_dialog",
                "import utilities.admin.admin_builder_gui as admin_builder_gui"
            ]
        }
    }
    
    for script, updates in build_script_updates.items():
        script_path = Path("build_scripts/common") / script
        if script_path.exists():
            with open(script_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            for old_import, new_import in zip(updates["old_imports"], updates["new_imports"]):
                content = content.replace(old_import, new_import)
            
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(content)
            
            print(f"✅ Mis à jour: {script}")

def main():
    """Point d'entrée principal"""
    print("🔧 RÉORGANISATION DU PROJET MATELASAPP")
    print("=" * 50)
    print()
    
    # Créer la structure de répertoires
    print("📁 Création de la structure de répertoires...")
    create_directory_structure()
    print()
    
    # Déplacer les scripts de build
    print("🔨 Déplacement des scripts de build...")
    move_build_scripts()
    print()
    
    # Déplacer les scripts utilitaires
    print("🛠️ Déplacement des scripts utilitaires...")
    move_utility_scripts()
    print()
    
    # Déplacer la documentation
    print("📚 Déplacement de la documentation...")
    move_documentation()
    print()
    
    # Créer les scripts de lancement
    print("🚀 Création des scripts de lancement...")
    create_launcher_scripts()
    print()
    
    # Créer le README de structure
    print("📋 Création du README de structure...")
    create_readme_structure()
    print()
    
    # Mettre à jour les scripts de build
    print("🔧 Mise à jour des scripts de build...")
    update_build_scripts()
    print()
    
    print("🎉 Réorganisation terminée !")
    print()
    print("📁 Nouvelle structure créée :")
    print("   build_scripts/ - Scripts de construction")
    print("   utilities/ - Scripts utilitaires")
    print("   docs/ - Documentation")
    print()
    print("🚀 Utilisez build_launcher.bat (Windows) ou build_launcher.sh (Unix)")

if __name__ == "__main__":
    main() 