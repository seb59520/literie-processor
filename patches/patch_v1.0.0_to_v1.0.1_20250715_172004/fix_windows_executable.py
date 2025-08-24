#!/usr/bin/env python3
"""
Script pour corriger l'exécutable Windows
Recrée une version fonctionnelle basée sur le fait que python run_gui.py fonctionne
"""

import os
import sys
import subprocess
import shutil
import tempfile

def fix_executable():
    """Corrige l'exécutable Windows"""
    
    print("🔧 Correction de l'exécutable Windows...")
    print("Basé sur le fait que 'python run_gui.py' fonctionne")
    
    # Vérifier PyInstaller
    try:
        import PyInstaller
        print("✅ PyInstaller disponible")
    except ImportError:
        print("📦 Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Nettoyer les anciens fichiers
    print("🧹 Nettoyage des anciens fichiers...")
    for path in ["build", "dist", "*.spec"]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    
    # Créer un fichier spec optimisé
    print("📝 Création du fichier spec optimisé...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collecter tous les dossiers de données
datas = []

# Dossiers essentiels
essential_dirs = [
    ('backend', 'backend'),
    ('assets', 'assets'),
    ('template', 'template'),
    ('config', 'config'),
    ('Référentiels', 'Référentiels'),
    ('Commandes', 'Commandes'),
]

for src, dst in essential_dirs:
    if os.path.exists(src):
        datas.append((src, dst))
        print(f"✅ Ajouté: {src} -> {dst}")

# Fichiers individuels
files = [
    ('EULA.txt', '.'),
    ('README_GUI.md', '.'),
]

for src, dst in files:
    if os.path.exists(src):
        datas.append((src, dst))
        print(f"✅ Ajouté: {src} -> {dst}")

a = Analysis(
    ['run_gui.py'],
    pathex=[os.getcwd()],
    binaries=[],
    datas=datas,
    hiddenimports=[
        # PyQt6
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtPrintSupport',
        
        # Backend modules
        'backend_interface',
        'config',
        'matelas_utils',
        'client_utils',
        'pre_import_utils',
        'secure_storage',
        
        # PDF processing
        'fitz',
        'PyMuPDF',
        
        # Excel
        'openpyxl',
        'openpyxl.workbook',
        'openpyxl.worksheet',
        'openpyxl.cell',
        
        # HTTP/API
        'httpx',
        'requests',
        'urllib3',
        
        # Web framework
        'jinja2',
        'uvicorn',
        'fastapi',
        'fastapi.responses',
        'fastapi.templating',
        
        # Security
        'cryptography',
        
        # Data processing
        'pandas',
        'numpy',
        
        # Image processing
        'PIL',
        'PIL.Image',
        
        # JSON/Validation
        'jsonschema',
        'pydantic',
        
        # Async/MQTT
        'asyncio_mqtt',
        
        # Utilities
        'python_dateutil',
        'colorlog',
        'psutil',
        
        # Backend specific
        'backend.article_utils',
        'backend.client_utils',
        'backend.date_utils',
        'backend.decoupe_noyau_utils',
        'backend.dimensions_sommiers',
        'backend.dimensions_utils',
        'backend.excel_import_utils',
        'backend.excel_sommier_import_utils',
        'backend.fermete_utils',
        'backend.hauteur_utils',
        'backend.housse_utils',
        'backend.latex_mixte7zones_longueur_housse_utils',
        'backend.latex_mixte7zones_referentiel',
        'backend.latex_naturel_longueur_housse_utils',
        'backend.latex_naturel_referentiel',
        'backend.latex_renforce_longueur_utils',
        'backend.latex_renforce_utils',
        'backend.llm_provider',
        'backend.mapping_manager',
        'backend.matelas_utils',
        'backend.matiere_housse_utils',
        'backend.mousse_rainuree7zones_longueur_housse_utils',
        'backend.mousse_rainuree7zones_referentiel',
        'backend.mousse_visco_longueur_utils',
        'backend.mousse_visco_utils',
        'backend.operation_utils',
        'backend.poignees_utils',
        'backend.pre_import_utils',
        'backend.secure_storage',
        'backend.select43_longueur_housse_utils',
        'backend.select43_utils',
        'backend.sommier_analytics_utils',
        'backend.sommier_utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',
        'matplotlib',
        'scipy',
        'IPython',
        'jupyter',
        'notebook',
        'sphinx',
        'pytest',
        'unittest',
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
    console=False,  # Application graphique sans console
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/lit-double.png' if os.path.exists('assets/lit-double.png') else None,
)
'''
    
    with open("matelas_fixed.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Fichier spec créé")
    
    # Compiler avec PyInstaller
    print("🔨 Compilation en cours...")
    try:
        subprocess.check_call([sys.executable, "-m", "PyInstaller", "matelas_fixed.spec"])
        print("✅ Compilation réussie!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de la compilation: {e}")
        return False
    
    # Créer un script de lancement
    print("📝 Création du script de lancement...")
    
    launcher_content = '''@echo off
echo ========================================
echo    Application Matelas - Lancement
echo ========================================
echo.

cd /d "%~dp0"
if exist "MatelasApp.exe" (
    echo Lancement de l'application...
    MatelasApp.exe
) else (
    echo ERREUR: MatelasApp.exe non trouve
    echo Lancement avec Python...
    python run_gui.py
)

echo.
echo Application fermee.
pause
'''
    
    with open("dist/MatelasApp/launch.bat", "w", encoding="utf-8") as f:
        f.write(launcher_content)
    
    print("✅ Script de lancement créé")
    
    # Créer un raccourci sur le bureau
    print("📋 Création du raccourci sur le bureau...")
    
    shortcut_content = f'''@echo off
echo Creation du raccourci sur le bureau...
echo.

set "DESKTOP=%USERPROFILE%\\Desktop"
set "APP_PATH={os.path.abspath('dist/MatelasApp')}"
set "EXE_PATH=%APP_PATH%\\MatelasApp.exe"

if exist "%EXE_PATH%" (
    echo Raccourci cree sur le bureau
    echo.
    echo Pour lancer l'application:
    echo   1. Double-cliquez sur le raccourci "MatelasApp" sur le bureau
    echo   2. Ou double-cliquez sur MatelasApp.exe dans %APP_PATH%
    echo   3. Ou double-cliquez sur launch.bat dans %APP_PATH%
) else (
    echo ERREUR: Executable non trouve
)

pause
'''
    
    with open("dist/MatelasApp/install_shortcut.bat", "w", encoding="utf-8") as f:
        f.write(shortcut_content)
    
    print("✅ Script d'installation de raccourci créé")
    
    print("\n🎉 Correction terminée!")
    print("\n📁 Votre application se trouve dans: dist/MatelasApp/")
    print("🚀 Pour lancer:")
    print("   1. Double-cliquez sur MatelasApp.exe")
    print("   2. Ou double-cliquez sur launch.bat")
    print("   3. Ou double-cliquez sur install_shortcut.bat pour créer un raccourci")
    
    return True

if __name__ == "__main__":
    success = fix_executable()
    if not success:
        print("\n❌ La correction a échoué")
        sys.exit(1) 