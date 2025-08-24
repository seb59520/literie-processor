#!/usr/bin/env python3
"""
Script pour créer un package distributable complet
"""

import os
import sys
import shutil
import zipfile
import tarfile
import platform
import subprocess
from datetime import datetime

def create_distribution_package():
    """Crée un package distributable complet"""
    
    print("=== Création du package distributable ===")
    
    # Nom du package
    package_name = "MatelasProcessor"
    version = "1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Créer le répertoire de distribution
    dist_dir = f"dist/{package_name}_{version}_{timestamp}"
    os.makedirs(dist_dir, exist_ok=True)
    
    print(f"📁 Création du package: {dist_dir}")
    
    # Fichiers à inclure
    files_to_include = [
        "run_gui.py",
        "backend_interface.py",
        "config.py",
        "requirements_gui.txt",
        "README_GUI.md",
        "install.py",
        "build_installer.py",
        "setup.py",
        "uninstall.py",
        "test_installation.py"
    ]
    
    # Répertoires à inclure
    dirs_to_include = [
        "backend",
        "template"
    ]
    
    # Copier les fichiers
    print("📋 Copie des fichiers...")
    for file in files_to_include:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} non trouvé")
    
    # Copier les répertoires
    for dir_name in dirs_to_include:
        if os.path.exists(dir_name):
            dest_dir = os.path.join(dist_dir, dir_name)
            shutil.copytree(dir_name, dest_dir)
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ non trouvé")
    
    # Créer un script d'installation pour chaque OS
    create_install_scripts(dist_dir)
    
    # Créer un README principal
    create_main_readme(dist_dir, version)
    
    # Créer les archives
    create_archives(dist_dir, package_name, version, timestamp)
    
    print(f"\n🎉 Package créé avec succès!")
    print(f"📁 Répertoire: {dist_dir}")
    print(f"📦 Archives créées dans: dist/")

def create_install_scripts(dist_dir):
    """Crée les scripts d'installation pour chaque OS"""
    
    # Script Windows
    windows_install = f"""@echo off
echo Installation de Matelas Processor...
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

REM Installer les dépendances
echo Installation des dépendances...
pip install -r requirements_gui.txt
if errorlevel 1 (
    echo ERREUR: Échec de l'installation des dépendances
    pause
    exit /b 1
)

REM Créer le raccourci sur le bureau
echo Création du raccourci...
set DESKTOP=%USERPROFILE%\\Desktop
echo @echo off > "%DESKTOP%\\Matelas Processor.bat"
echo cd /d "%~dp0" >> "%DESKTOP%\\Matelas Processor.bat"
echo python run_gui.py >> "%DESKTOP%\\Matelas Processor.bat"
echo pause >> "%DESKTOP%\\Matelas Processor.bat"

echo.
echo ✅ Installation terminée!
echo 🖥️  Raccourci créé sur le bureau
echo.
pause
"""
    
    with open(os.path.join(dist_dir, "install_windows.bat"), 'w', encoding='utf-8') as f:
        f.write(windows_install)
    
    # Script macOS/Linux
    unix_install = f"""#!/bin/bash

echo "Installation de Matelas Processor..."
echo

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python 3 n'est pas installé"
    echo "Veuillez installer Python 3.8+"
    exit 1
fi

# Installer les dépendances
echo "Installation des dépendances..."
python3 -m pip install -r requirements_gui.txt
if [ $? -ne 0 ]; then
    echo "ERREUR: Échec de l'installation des dépendances"
    exit 1
fi

# Créer le raccourci sur le bureau
echo "Création du raccourci..."
DESKTOP="$HOME/Desktop"
SCRIPT_PATH="$(cd "$(dirname "$0")" && pwd)"

if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    cat > "$DESKTOP/Matelas Processor.command" << EOF
#!/bin/bash
cd "$SCRIPT_PATH"
python3 run_gui.py
EOF
    chmod +x "$DESKTOP/Matelas Processor.command"
else
    # Linux
    cat > "$DESKTOP/Matelas Processor.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Matelas Processor
Comment=Traitement automatique de commandes matelas
Exec=$SCRIPT_PATH/run_gui.py
Terminal=false
Categories=Office;
EOF
    chmod +x "$DESKTOP/Matelas Processor.desktop"
fi

echo
echo "✅ Installation terminée!"
echo "🖥️  Raccourci créé sur le bureau"
echo
"""
    
    with open(os.path.join(dist_dir, "install_unix.sh"), 'w', encoding='utf-8') as f:
        f.write(unix_install)
    
    # Rendre le script Unix exécutable
    os.chmod(os.path.join(dist_dir, "install_unix.sh"), 0o755)
    
    print("  ✅ Scripts d'installation créés")

def create_main_readme(dist_dir, version):
    """Crée le README principal du package"""
    
    readme_content = f"""# Matelas Processor v{version}

## Description

Application de traitement automatique de commandes matelas avec interface graphique.

## Installation

### Windows
1. Décompressez ce dossier
2. Double-cliquez sur `install_windows.bat`
3. Suivez les instructions

### macOS/Linux
1. Décompressez ce dossier
2. Ouvrez un terminal dans le dossier
3. Exécutez: `./install_unix.sh`

### Installation manuelle
1. Installez Python 3.8+
2. Installez les dépendances: `pip install -r requirements_gui.txt`
3. Lancez: `python run_gui.py`

## Utilisation

1. Lancez l'application
2. Sélectionnez vos fichiers PDF de commandes
3. Configurez les paramètres (semaine, année, etc.)
4. Cliquez sur "Traiter les fichiers"
5. Les fichiers Excel seront générés dans le dossier output/

## Structure du projet

```
MatelasProcessor/
├── run_gui.py              # Interface graphique principale
├── backend_interface.py    # Interface avec le backend
├── config.py              # Configuration
├── backend/               # Modules de traitement
├── template/              # Templates Excel
├── requirements_gui.txt   # Dépendances Python
└── README_GUI.md         # Documentation détaillée
```

## Support

Pour toute question, contactez l'équipe de développement.

## Version

{version} - {datetime.now().strftime("%d/%m/%Y")}
"""
    
    with open(os.path.join(dist_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✅ README principal créé")

def create_archives(dist_dir, package_name, version, timestamp):
    """Crée les archives distributables"""
    
    # Créer le répertoire dist s'il n'existe pas
    os.makedirs("dist", exist_ok=True)
    
    # Archive ZIP
    zip_filename = f"dist/{package_name}_{version}_{timestamp}.zip"
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_dir)
                zipf.write(file_path, arcname)
    
    print(f"  ✅ Archive ZIP créée: {zip_filename}")
    
    # Archive TAR.GZ (pour Unix)
    tar_filename = f"dist/{package_name}_{version}_{timestamp}.tar.gz"
    with tarfile.open(tar_filename, "w:gz") as tar:
        tar.add(dist_dir, arcname=os.path.basename(dist_dir))
    
    print(f"  ✅ Archive TAR.GZ créée: {tar_filename}")

def main():
    """Fonction principale"""
    create_distribution_package()

if __name__ == "__main__":
    main() 