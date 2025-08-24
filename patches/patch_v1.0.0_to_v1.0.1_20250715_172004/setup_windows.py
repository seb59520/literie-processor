#!/usr/bin/env python3
"""
Script d'installation automatique pour Windows
Crée un exécutable autonome de l'application matelas
"""

import os
import sys
import subprocess
import shutil
import tempfile
import zipfile
from pathlib import Path

def check_python_version():
    """Vérifie que Python 3.8+ est installé"""
    if sys.version_info < (3, 8):
        print("ERREUR: Python 3.8 ou superieur est requis")
        print(f"Version actuelle: {sys.version}")
        return False
    print(f"OK: Python {sys.version_info.major}.{sys.version_info.minor} detecte")
    return True

def install_pyinstaller():
    """Installe PyInstaller si nécessaire"""
    try:
        import PyInstaller
        print("OK: PyInstaller deja installe")
        return True
    except ImportError:
        print("Installation de PyInstaller...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
            print("OK: PyInstaller installe avec succes")
            return True
        except subprocess.CalledProcessError as e:
            print(f"ERREUR lors de l'installation de PyInstaller: {e}")
            return False

def install_dependencies():
    """Installe toutes les dépendances nécessaires"""
    print("Installation des dependances...")
    
    # Fusionner les requirements
    all_requirements = []
    
    # Requirements GUI
    if os.path.exists("requirements_gui.txt"):
        with open("requirements_gui.txt", "r") as f:
            all_requirements.extend([line.strip() for line in f if line.strip() and not line.startswith("#")])
    
    # Requirements backend
    if os.path.exists("backend/requirements.txt"):
        with open("backend/requirements.txt", "r") as f:
            all_requirements.extend([line.strip() for line in f if line.strip() and not line.startswith("#")])
    
    # Supprimer les doublons
    all_requirements = list(set(all_requirements))
    
    print(f"Installation de {len(all_requirements)} packages...")
    
    for req in all_requirements:
        try:
            print(f"  Installation de {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
        except subprocess.CalledProcessError as e:
            print(f"  WARNING: Erreur avec {req}: {e}")
            # Continue avec les autres packages
    
    print("OK: Installation des dependances terminee")

def create_spec_file():
    """Crée le fichier spec pour PyInstaller"""
    
    # Préparer les données
    datas = []
    
    # Dossiers à inclure
    data_dirs = [
        ('backend', 'backend'),
        ('assets', 'assets'),
        ('template', 'template'),
        ('config', 'config'),
        ('Référentiels', 'Référentiels'),
        ('Commandes', 'Commandes'),
    ]
    
    for src, dst in data_dirs:
        if os.path.exists(src):
            datas.append((src, dst))
            print(f"OK: Ajoute {src} -> {dst}")
        else:
            print(f"WARNING: Dossier manquant {src}")
    
    # Fichiers individuels
    data_files = [
        ('EULA.txt', '.'),
        ('README_GUI.md', '.'),
    ]
    
    for src, dst in data_files:
        if os.path.exists(src):
            datas.append((src, dst))
            print(f"OK: Ajoute {src} -> {dst}")
        else:
            print(f"WARNING: Fichier manquant {src}")
    
    # Créer le contenu du fichier spec
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas={datas},
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtPrintSupport',
        'fitz',
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'httpx',
        'jinja2',
        'uvicorn',
        'fastapi',
        'fastapi.responses',
        'fastapi.templating',
        'cryptography',
        'pandas',
        'numpy',
        'PIL',
        'PIL.Image',
        'requests',
        'jsonschema',
        'pydantic',
        'asyncio_mqtt',
        'python_dateutil',
        'colorlog',
        'psutil',
        'urllib3',
        'backend_interface',
        'config',
        'matelas_utils',
        'client_utils',
        'pre_import_utils',
        'secure_storage',
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='MatelasApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/lit-double.png' if os.path.exists('assets/lit-double.png') else None,
)
'''
    
    with open("matelas_app.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("OK: Fichier spec cree")

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    print("Compilation de l'executable...")
    
    try:
        # Test simple d'abord
        print("Test de PyInstaller...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller", "--version"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            print(f"ERREUR: PyInstaller ne fonctionne pas: {result.stderr}")
            return False
        
        print(f"PyInstaller version: {result.stdout.strip()}")
        
        # Nettoyer les anciens builds
        print("Nettoyage des anciens builds...")
        for dir_to_clean in ["build", "dist"]:
            if os.path.exists(dir_to_clean):
                shutil.rmtree(dir_to_clean)
                print(f"Dossier {dir_to_clean} supprime")
        
        # Compilation avec plus de détails
        print("Lancement de la compilation...")
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--log-level=INFO",
            "matelas_app.spec"
        ], capture_output=True, text=True, timeout=300)  # 5 minutes timeout
        
        if result.returncode != 0:
            print(f"ERREUR lors de la compilation:")
            print(f"Code de retour: {result.returncode}")
            print(f"Sortie d'erreur:")
            print(result.stderr)
            print(f"Sortie standard:")
            print(result.stdout)
            return False
        
        print("OK: Executable compile avec succes")
        return True
        
    except subprocess.TimeoutExpired:
        print("ERREUR: Timeout lors de la compilation (plus de 5 minutes)")
        return False
    except subprocess.CalledProcessError as e:
        print(f"ERREUR lors de la compilation: {e}")
        print(f"Code de retour: {e.returncode}")
        if hasattr(e, 'stderr') and e.stderr:
            print(f"Erreur: {e.stderr}")
        if hasattr(e, 'stdout') and e.stdout:
            print(f"Sortie: {e.stdout}")
        return False
    except Exception as e:
        print(f"ERREUR inattendue lors de la compilation: {e}")
        return False

def create_installer():
    """Crée un package d'installation simple"""
    print("Creation du package d'installation...")
    
    # Créer le dossier de distribution
    dist_dir = "dist/MatelasApp"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    # Copier l'exécutable et les fichiers nécessaires
    if os.path.exists("dist/MatelasApp.exe"):
        os.makedirs(dist_dir, exist_ok=True)
        shutil.copy2("dist/MatelasApp.exe", dist_dir)
        
        # Créer un raccourci sur le bureau
        create_shortcut_script = f'''@echo off
echo Creation du raccourci sur le bureau...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\MatelasApp.lnk'); $Shortcut.TargetPath = '%~dp0MatelasApp.exe'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
echo Installation terminee !
pause
'''
        
        with open(f"{dist_dir}/install.bat", "w", encoding="utf-8") as f:
            f.write(create_shortcut_script)
        
        # Créer un fichier README
        readme_content = """# Application Matelas

## Installation
1. Double-cliquez sur `install.bat` pour créer un raccourci sur le bureau
2. Ou lancez directement `MatelasApp.exe`

## Utilisation
- L'application traite les devis PDF de matelas
- Interface graphique intuitive
- Support des LLM (Ollama, OpenRouter)

## Support
Consultez les fichiers README_*.md pour plus d'informations.
"""
        
        with open(f"{dist_dir}/README.txt", "w", encoding="utf-8") as f:
            f.write(readme_content)
        
        print("OK: Package d'installation cree dans dist/MatelasApp/")
        return True
    else:
        print("ERREUR: Executable non trouve")
        return False

def main():
    """Fonction principale d'installation"""
    print("Installation de l'application Matelas pour Windows")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_python_version():
        return False
    
    # Installation des outils
    if not install_pyinstaller():
        return False
    
    # Installation des dépendances
    install_dependencies()
    
    # Création du fichier spec
    create_spec_file()
    
    # Compilation
    if not build_executable():
        return False
    
    # Création du package d'installation
    if not create_installer():
        return False
    
    print("\nInstallation terminee avec succes !")
    print("\nVotre application se trouve dans: dist/MatelasApp/")
    print("Pour installer sur un autre PC:")
    print("   1. Copiez le dossier dist/MatelasApp/")
    print("   2. Lancez install.bat pour creer un raccourci")
    print("   3. Ou lancez directement MatelasApp.exe")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInstallation annulee par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 