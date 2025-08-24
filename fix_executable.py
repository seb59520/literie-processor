#!/usr/bin/env python3
"""
Script de réparation rapide pour l'exécutable
"""

import os
import sys
import subprocess
import shutil

def clean_old_builds():
    """Nettoie les anciens builds"""
    print("Nettoyage des anciens builds...")
    
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
            print(f"Dossier {dir_to_clean} supprime")
    
    for file_to_clean in ["*.spec"]:
        import glob
        for file in glob.glob(file_to_clean):
            os.remove(file)
            print(f"Fichier {file} supprime")

def install_missing_dependencies():
    """Installe les dépendances manquantes"""
    print("Installation des dependances manquantes...")
    
    missing_packages = [
        "fastapi",
        "uvicorn",
        "python-multipart",
        "jinja2"
    ]
    
    for pkg in missing_packages:
        try:
            print(f"  Installation de {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        except:
            print(f"  WARNING: Probleme avec {pkg}")

def create_fixed_spec():
    """Crée un fichier spec corrigé"""
    print("Creation du fichier spec corrige...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('assets', 'assets'),
        ('template', 'template'),
        ('config', 'config'),
        ('Commandes', 'Commandes'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets', 
        'PyQt6.QtGui',
        'fitz',
        'openpyxl',
        'httpx',
        'jinja2',
        'cryptography',
        'pandas',
        'numpy',
        'requests',
        'jsonschema',
        'pydantic',
        'fastapi',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'fastapi.responses',
        'fastapi.templating',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'backend_interface',
        'config',
        'matelas_utils',
        'client_utils',
        'pre_import_utils',
        'secure_storage',
        'date_utils',
        'article_utils',
        'operation_utils',
        'hauteur_utils',
        'fermete_utils',
        'housse_utils',
        'matiere_housse_utils',
        'poignees_utils',
        'dimensions_utils',
        'latex_naturel_referentiel',
        'latex_mixte7zones_referentiel',
        'mousse_rainuree7zones_referentiel',
        'select43_utils',
        'select43_longueur_housse_utils',
        'latex_renforce_utils',
        'latex_renforce_longueur_utils',
        'mousse_visco_utils',
        'mousse_visco_longueur_utils',
        'latex_naturel_longueur_housse_utils',
        'latex_mixte7zones_longueur_housse_utils',
        'mousse_rainuree7zones_longueur_housse_utils',
        'decoupe_noyau_utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='MatelasApp_Fixed',
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
)
'''
    
    with open("matelas_fixed.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("OK: Fichier spec corrige cree")

def build_fixed_executable():
    """Compile l'exécutable corrigé"""
    print("Compilation de l'executable corrige...")
    
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "matelas_fixed.spec"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("OK: Executable corrige compile")
            return True
        else:
            print(f"ERREUR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"ERREUR: {e}")
        return False

def create_package():
    """Crée le package final"""
    print("Creation du package...")
    
    if not os.path.exists("dist/MatelasApp_Fixed.exe"):
        print("ERREUR: Executable non trouve")
        return False
    
    # Créer le dossier de distribution
    dist_dir = "dist/MatelasApp_Fixed"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir)
    shutil.copy2("dist/MatelasApp_Fixed.exe", dist_dir)
    
    # Créer le script d'installation
    install_script = '''@echo off
echo Creation du raccourci sur le bureau...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\MatelasApp_Fixed.lnk'); $Shortcut.TargetPath = '%~dp0MatelasApp_Fixed.exe'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
echo Installation terminee !
pause
'''
    
    with open(f"{dist_dir}/install.bat", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    print("OK: Package cree dans dist/MatelasApp_Fixed/")
    return True

def main():
    """Fonction principale"""
    print("Reparation de l'executable MatelasApp")
    print("=" * 50)
    
    clean_old_builds()
    install_missing_dependencies()
    create_fixed_spec()
    
    if build_fixed_executable():
        create_package()
        print("\nReparation terminee avec succes !")
        print("Votre application corrigee se trouve dans: dist/MatelasApp_Fixed/")
        print("Lancez install.bat pour creer un raccourci")
    else:
        print("\nERREUR: Echec de la reparation")

if __name__ == "__main__":
    main() 