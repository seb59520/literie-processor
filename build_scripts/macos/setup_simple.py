#!/usr/bin/env python3
"""
Version simplifiée du script d'installation pour Windows
"""

import os
import sys
import subprocess
import shutil

def check_python():
    """Vérifie Python"""
    if sys.version_info < (3, 8):
        print("ERREUR: Python 3.8+ requis")
        return False
    print(f"OK: Python {sys.version_info.major}.{sys.version_info.minor}")
    return True

def install_pyinstaller():
    """Installe PyInstaller"""
    try:
        import PyInstaller
        print("OK: PyInstaller deja installe")
        return True
    except ImportError:
        print("Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("OK: PyInstaller installe")
        return True

def install_dependencies():
    """Installe les dépendances"""
    print("Installation des dependances...")
    
    # Installer les packages principaux
    packages = [
        "PyQt6",
        "PyMuPDF", 
        "openpyxl",
        "httpx",
        "jinja2",
        "cryptography",
        "pandas",
        "numpy",
        "requests",
        "jsonschema",
        "pydantic",
        "fastapi",
        "uvicorn",
        "python-multipart"
    ]
    
    for pkg in packages:
        try:
            print(f"  Installation de {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])
        except:
            print(f"  WARNING: Probleme avec {pkg}")
    
    print("OK: Dependances installees")

def create_simple_spec():
    """Crée un fichier spec simple"""
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
)
'''
    
    with open("matelas_simple.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("OK: Fichier spec simple cree")

def build_executable():
    """Compile l'exécutable"""
    print("Compilation de l'executable...")
    
    # Nettoyer
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
    
    # Compiler
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "matelas_simple.spec"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("OK: Executable compile avec succes")
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
    
    if not os.path.exists("dist/MatelasApp.exe"):
        print("ERREUR: Executable non trouve")
        return False
    
    # Créer le dossier de distribution
    dist_dir = "dist/MatelasApp"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    
    os.makedirs(dist_dir)
    shutil.copy2("dist/MatelasApp.exe", dist_dir)
    
    # Créer le script d'installation
    install_script = '''@echo off
echo Creation du raccourci sur le bureau...
powershell "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%USERPROFILE%\\Desktop\\MatelasApp.lnk'); $Shortcut.TargetPath = '%~dp0MatelasApp.exe'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Save()"
echo Installation terminee !
pause
'''
    
    with open(f"{dist_dir}/install.bat", "w", encoding="utf-8") as f:
        f.write(install_script)
    
    print("OK: Package cree dans dist/MatelasApp/")
    return True

def main():
    """Fonction principale"""
    print("Installation simplifiee - Application Matelas")
    print("=" * 50)
    
    if not check_python():
        return False
    
    if not install_pyinstaller():
        return False
    
    install_dependencies()
    create_simple_spec()
    
    if not build_executable():
        return False
    
    if not create_package():
        return False
    
    print("\nInstallation terminee avec succes !")
    print("Votre application se trouve dans: dist/MatelasApp/")
    print("Lancez install.bat pour creer un raccourci")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nInstallation annulee")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur: {e}")
        sys.exit(1) 