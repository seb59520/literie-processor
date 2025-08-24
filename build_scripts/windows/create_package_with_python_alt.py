#!/usr/bin/env python3
"""
Script pour créer un package distributable avec Python embarqué (version alternative)
"""

import os
import sys
import shutil
import zipfile
import tarfile
import platform
import subprocess
import ssl
import urllib.request
import tempfile
from datetime import datetime

def download_python_embedded():
    """Télécharge Python embarqué pour Windows avec gestion d'erreurs"""
    print("📥 Téléchargement de Python embarqué...")
    
    # URL de Python embarqué pour Windows
    python_version = "3.11.8"  # Version stable récente
    python_url = f"https://www.python.org/ftp/python/{python_version}/python-{python_version}-embed-amd64.zip"
    
    # Créer un dossier temporaire
    temp_dir = tempfile.mkdtemp()
    python_zip = os.path.join(temp_dir, "python-embedded.zip")
    
    try:
        # Créer un contexte SSL qui ignore les erreurs de certificat
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        # Télécharger Python embarqué
        print(f"Téléchargement depuis: {python_url}")
        with urllib.request.urlopen(python_url, context=ssl_context) as response:
            with open(python_zip, 'wb') as f:
                shutil.copyfileobj(response, f)
        
        print("✅ Python embarqué téléchargé")
        return python_zip, temp_dir
        
    except Exception as e:
        print(f"❌ Erreur lors du téléchargement: {e}")
        print("💡 Création du package sans Python embarqué...")
        return None, temp_dir

def create_package_with_python():
    """Crée un package distributable avec Python embarqué"""
    
    print("=== Création du package distributable avec Python embarqué ===")
    
    # Nom du package
    package_name = "MatelasProcessor_Standalone"
    version = "1.0.0"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Créer le répertoire de distribution
    dist_dir = f"dist/{package_name}_{version}_{timestamp}"
    os.makedirs(dist_dir, exist_ok=True)
    
    print(f"📁 Création du package: {dist_dir}")
    
    # Télécharger Python embarqué pour Windows
    python_zip, temp_dir = download_python_embedded()
    
    python_included = False
    if python_zip and os.path.exists(python_zip):
        # Extraire Python embarqué
        python_dir = os.path.join(dist_dir, "python")
        os.makedirs(python_dir, exist_ok=True)
        
        with zipfile.ZipFile(python_zip, 'r') as zip_ref:
            zip_ref.extractall(python_dir)
        
        print("✅ Python embarqué extrait")
        
        # Installer pip pour Python embarqué
        install_pip_for_embedded(python_dir)
        
        # Créer un script de lancement Windows avec Python embarqué
        create_windows_launcher(dist_dir, python_dir)
        python_included = True
    else:
        # Créer un script de lancement Windows sans Python embarqué
        create_windows_launcher_no_python(dist_dir)
    
    # Fichiers à inclure
    files_to_include = [
        "run_gui.py",
        "backend_interface.py",
        "config.py",
        "requirements_gui.txt",
        "README_GUI.md",
        "launch.py",
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
    
    # Créer les scripts d'installation
    create_install_scripts_with_python(dist_dir, python_included)
    
    # Créer un README principal
    create_main_readme_with_python(dist_dir, version, python_included)
    
    # Créer les archives
    create_archives_with_python(dist_dir, package_name, version, timestamp)
    
    # Nettoyer les fichiers temporaires
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    if python_included:
        print(f"\n🎉 Package avec Python embarqué créé avec succès!")
    else:
        print(f"\n🎉 Package créé (Python non inclus - téléchargement échoué)")
    print(f"📁 Répertoire: {dist_dir}")
    print(f"📦 Archives créées dans: dist/")

def install_pip_for_embedded(python_dir):
    """Installe pip pour Python embarqué"""
    print("📦 Installation de pip pour Python embarqué...")
    
    try:
        # Télécharger get-pip.py
        get_pip_url = "https://bootstrap.pypa.io/get-pip.py"
        get_pip_file = os.path.join(python_dir, "get-pip.py")
        
        # Créer un contexte SSL qui ignore les erreurs de certificat
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        with urllib.request.urlopen(get_pip_url, context=ssl_context) as response:
            with open(get_pip_file, 'wb') as f:
                shutil.copyfileobj(response, f)
        
        # Exécuter get-pip.py
        python_exe = os.path.join(python_dir, "python.exe")
        subprocess.run([python_exe, "get-pip.py"], cwd=python_dir, check=True)
        
        # Supprimer get-pip.py
        os.remove(get_pip_file)
        
        print("✅ pip installé pour Python embarqué")
        
    except Exception as e:
        print(f"⚠️  Impossible d'installer pip: {e}")

def create_windows_launcher(dist_dir, python_dir):
    """Crée un script de lancement Windows avec Python embarqué"""
    
    launcher_content = f"""@echo off
echo Lancement de Matelas Processor...
echo.

REM Vérifier si Python embarqué existe
if not exist "{os.path.basename(python_dir)}\\python.exe" (
    echo ERREUR: Python embarqué non trouvé
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
if not exist "requirements_installed.txt" (
    echo Installation des dépendances...
    {os.path.basename(python_dir)}\\python.exe -m pip install -r requirements_gui.txt
    if errorlevel 1 (
        echo ERREUR: Échec de l'installation des dépendances
        pause
        exit /b 1
    )
    echo. > requirements_installed.txt
)

REM Lancer l'application
echo Lancement de l'application...
{os.path.basename(python_dir)}\\python.exe run_gui.py

if errorlevel 1 (
    echo ERREUR: L'application s'est arrêtée avec une erreur
    pause
)
"""
    
    launcher_path = os.path.join(dist_dir, "launch_windows.bat")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Script de lancement Windows créé (avec Python embarqué)")

def create_windows_launcher_no_python(dist_dir):
    """Crée un script de lancement Windows sans Python embarqué"""
    
    launcher_content = f"""@echo off
echo Lancement de Matelas Processor...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo Veuillez installer Python 3.8+ depuis https://python.org
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
if not exist "requirements_installed.txt" (
    echo Installation des dépendances...
    python -m pip install -r requirements_gui.txt
    if errorlevel 1 (
        echo ERREUR: Échec de l'installation des dépendances
        pause
        exit /b 1
    )
    echo. > requirements_installed.txt
)

REM Lancer l'application
echo Lancement de l'application...
python run_gui.py

if errorlevel 1 (
    echo ERREUR: L'application s'est arrêtée avec une erreur
    pause
)
"""
    
    launcher_path = os.path.join(dist_dir, "launch_windows.bat")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Script de lancement Windows créé (sans Python embarqué)")

def create_install_scripts_with_python(dist_dir, python_included):
    """Crée les scripts d'installation avec ou sans Python embarqué"""
    
    if python_included:
        # Script Windows avec Python embarqué
        windows_install = f"""@echo off
echo Installation de Matelas Processor (avec Python embarqué)...
echo.

REM Créer le raccourci sur le bureau
echo Création du raccourci...
set DESKTOP=%USERPROFILE%\\Desktop
set SCRIPT_PATH=%~dp0

echo @echo off > "%DESKTOP%\\Matelas Processor.bat"
echo cd /d "%SCRIPT_PATH%" >> "%DESKTOP%\\Matelas Processor.bat"
echo call launch_windows.bat >> "%DESKTOP%\\Matelas Processor.bat"

echo.
echo ✅ Installation terminée!
echo 🖥️  Raccourci créé sur le bureau
echo 💡 Double-cliquez sur "Matelas Processor" pour lancer l'application
echo.
pause
"""
    else:
        # Script Windows sans Python embarqué
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

REM Créer le raccourci sur le bureau
echo Création du raccourci...
set DESKTOP=%USERPROFILE%\\Desktop
set SCRIPT_PATH=%~dp0

echo @echo off > "%DESKTOP%\\Matelas Processor.bat"
echo cd /d "%SCRIPT_PATH%" >> "%DESKTOP%\\Matelas Processor.bat"
echo call launch_windows.bat >> "%DESKTOP%\\Matelas Processor.bat"

echo.
echo ✅ Installation terminée!
echo 🖥️  Raccourci créé sur le bureau
echo 💡 Double-cliquez sur "Matelas Processor" pour lancer l'application
echo.
pause
"""
    
    with open(os.path.join(dist_dir, "install_windows.bat"), 'w', encoding='utf-8') as f:
        f.write(windows_install)
    
    # Script Unix (macOS/Linux) - utilise Python système
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

def create_main_readme_with_python(dist_dir, version, python_included):
    """Crée le README principal du package avec ou sans Python embarqué"""
    
    if python_included:
        readme_content = f"""# Matelas Processor v{version} (Standalone)

## Description

Application de traitement automatique de commandes matelas avec interface graphique.
**Ce package inclut Python 3.11 embarqué pour Windows - aucune installation de Python requise !**

## Installation

### Windows (Recommandé - Python inclus)
1. Décompressez ce dossier
2. Double-cliquez sur `install_windows.bat`
3. Suivez les instructions
4. **Aucune installation de Python requise !**

### macOS/Linux
1. Décompressez ce dossier
2. Ouvrez un terminal dans le dossier
3. Exécutez: `./install_unix.sh`
4. Python 3.8+ doit être installé sur le système

### Lancement Direct (Windows)
- Double-cliquez sur `launch_windows.bat` pour lancer directement

## Utilisation

1. Lancez l'application via le raccourci sur le bureau
2. Sélectionnez vos fichiers PDF de commandes
3. Configurez les paramètres (semaine, année, etc.)
4. Cliquez sur "Traiter les fichiers"
5. Les fichiers Excel seront générés dans le dossier output/

## Avantages de cette Version

### Windows
- ✅ **Python 3.11 inclus** - Aucune installation requise
- ✅ **Dépendances automatiques** - Installation automatique au premier lancement
- ✅ **Portable** - Fonctionne sur n'importe quel PC Windows
- ✅ **Simple** - Double-clic pour lancer

### macOS/Linux
- ✅ Installation standard avec Python système
- ✅ Gestion automatique des dépendances
- ✅ Raccourcis sur le bureau

## Structure du projet

```
MatelasProcessor_Standalone/
├── python/                 # Python 3.11 embarqué (Windows)
├── run_gui.py              # Interface graphique principale
├── backend_interface.py    # Interface avec le backend
├── config.py              # Configuration
├── backend/               # Modules de traitement
├── template/              # Templates Excel
├── requirements_gui.txt   # Dépendances Python
├── launch_windows.bat     # Lancement Windows avec Python embarqué
├── install_windows.bat    # Installation Windows
├── install_unix.sh        # Installation Unix
└── README.txt            # Ce fichier
```

## Support

Pour toute question, contactez l'équipe de développement.

## Version

{version} - {datetime.now().strftime("%d/%m/%Y")}
"""
    else:
        readme_content = f"""# Matelas Processor v{version} (Standard)

## Description

Application de traitement automatique de commandes matelas avec interface graphique.
**Python 3.8+ doit être installé sur le système.**

## Installation

### Windows
1. Décompressez ce dossier
2. Installez Python 3.8+ depuis https://python.org si nécessaire
3. Double-cliquez sur `install_windows.bat`
4. Suivez les instructions

### macOS/Linux
1. Décompressez ce dossier
2. Ouvrez un terminal dans le dossier
3. Exécutez: `./install_unix.sh`
4. Python 3.8+ doit être installé sur le système

### Lancement Direct
- Windows : Double-cliquez sur `launch_windows.bat`
- Unix : Exécutez `python3 run_gui.py`

## Utilisation

1. Lancez l'application via le raccourci sur le bureau
2. Sélectionnez vos fichiers PDF de commandes
3. Configurez les paramètres (semaine, année, etc.)
4. Cliquez sur "Traiter les fichiers"
5. Les fichiers Excel seront générés dans le dossier output/

## Prérequis

- **Python 3.8+** installé sur le système
- **Connexion internet** pour installer les dépendances

## Structure du projet

```
MatelasProcessor_Standalone/
├── run_gui.py              # Interface graphique principale
├── backend_interface.py    # Interface avec le backend
├── config.py              # Configuration
├── backend/               # Modules de traitement
├── template/              # Templates Excel
├── requirements_gui.txt   # Dépendances Python
├── launch_windows.bat     # Lancement Windows
├── install_windows.bat    # Installation Windows
├── install_unix.sh        # Installation Unix
└── README.txt            # Ce fichier
```

## Support

Pour toute question, contactez l'équipe de développement.

## Version

{version} - {datetime.now().strftime("%d/%m/%Y")}
"""
    
    with open(os.path.join(dist_dir, "README.txt"), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("  ✅ README principal créé")

def create_archives_with_python(dist_dir, package_name, version, timestamp):
    """Crée les archives distributables avec Python embarqué"""
    
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
    create_package_with_python()

if __name__ == "__main__":
    main() 