#!/usr/bin/env python3
"""
Script pour créer un exécutable Windows de l'application Matelas
Utilise PyInstaller pour créer un fichier .exe autonome
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_requirements():
    """Vérifie que tous les outils nécessaires sont installés"""
    print("Verification des prerequis...")
    
    try:
        import PyInstaller
        print(f"[OK] PyInstaller trouve: {PyInstaller.__version__}")
    except ImportError:
        print("[!] PyInstaller non trouve. Installation...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("[OK] PyInstaller installe")
    
    # Vérifier les dépendances principales
    deps = ['PyQt6', 'requests', 'pandas', 'openpyxl']
    missing = []
    
    for dep in deps:
        try:
            __import__(dep.lower() if dep != 'PyQt6' else 'PyQt6.QtWidgets')
            print(f"[OK] {dep} disponible")
        except ImportError:
            missing.append(dep)
            print(f"[!] {dep} manquant")
    
    if missing:
        print(f"[!] Dependances manquantes: {', '.join(missing)}")
        print("Ces dependances seront incluses automatiquement si disponibles")
    
    return True

def create_spec_file():
    """Crée un fichier .spec personnalisé pour PyInstaller"""
    print("Creation du fichier de configuration PyInstaller...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Datas à inclure (fichiers de configuration, assets, etc.)
datas = [
    ('matelas_config.json', '.') if os.path.exists('matelas_config.json') else None,
    ('matelas_config.json.template', '.') if os.path.exists('matelas_config.json.template') else None,
    ('assets', 'assets') if os.path.exists('assets') else None,
    ('backend', 'backend') if os.path.exists('backend') else None,
    ('config', 'config') if os.path.exists('config') else None,
    ('template', 'template') if os.path.exists('template') else None,
    ('config.py', '.') if os.path.exists('config.py') else None,
    ('backend_interface.py', '.') if os.path.exists('backend_interface.py') else None,
    ('version.py', '.') if os.path.exists('version.py') else None,
    ('EULA.txt', '.') if os.path.exists('EULA.txt') else None,
]

# Filtrer les None
datas = [d for d in datas if d is not None]

# Modules cachés (dépendances qui ne sont pas détectées automatiquement)
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.QtNetwork',
    'requests',
    'urllib3',
    'json',
    'pathlib',
    'datetime',
    'logging',
    'logging.handlers',
    'csv',
    'openpyxl',
    'openpyxl.workbook',
    'openpyxl.styles',
    'openpyxl.utils',
    'pandas',
    'psutil',  # optionnel pour le monitoring
    'markdown',  # optionnel
    'webbrowser',
    'tempfile',
    'shutil',
    'platform',
    'subprocess',
    'concurrent.futures',
    'threading',
    'queue',
    're',
    'sqlite3',  # pour le cost tracking
    'hashlib',
    'base64',
    'cryptography',
    'cryptography.fernet',
    'fitz',  # PyMuPDF pour lire les PDF
    'asyncio',
    'typing',
    'enum',
    'dataclasses',
    'functools',
    'itertools',
]

a = Analysis(
    ['app_gui.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter',  # Exclure tkinter si non utilisé
        'matplotlib',  # Exclure si non utilisé
        'scipy',  # Exclure si non utilisé
        'numpy',  # Exclure si non utilisé pour réduire la taille
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
    name='MatelasProcessor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compression UPX si disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # False = application GUI (pas de console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/lit-double.ico' if os.path.exists('assets/lit-double.ico') else 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
)
'''
    
    with open('matelas_processor.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("[OK] Fichier matelas_processor.spec cree")

def create_version_info():
    """Crée un fichier de version pour l'exécutable Windows"""
    print("Creation des informations de version...")
    
    version_content = '''# UTF-8
#
# Pour plus d'infos sur ce fichier, voir:
# https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Executable-Version-Info
#
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(1, 0, 0, 0),
    prodvers=(1, 0, 0, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Westelynck'),
        StringStruct(u'FileDescription', u'Processeur de Devis Literie'),
        StringStruct(u'FileVersion', u'1.0.0.0'),
        StringStruct(u'InternalName', u'MatelasProcessor'),
        StringStruct(u'LegalCopyright', u'© 2025 Westelynck. Tous droits réservés.'),
        StringStruct(u'OriginalFilename', u'MatelasProcessor.exe'),
        StringStruct(u'ProductName', u'Matelas Processor'),
        StringStruct(u'ProductVersion', u'1.0.0.0')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print("[OK] Fichier version_info.txt cree")

def create_icon():
    """Crée un dossier assets avec une icône par défaut"""
    assets_dir = Path('assets')
    assets_dir.mkdir(exist_ok=True)
    
    # Si pas d'icône, on peut en créer une simple ou utiliser celle par défaut
    icon_path = assets_dir / 'icon.ico'
    if not icon_path.exists():
        print("[!] Pas d'icone personnalisee trouvee")
        print("[Info] Vous pouvez ajouter une icone 'assets/icon.ico' pour personnaliser l'executable")

def check_config_files():
    """Vérifie et crée les fichiers de configuration nécessaires"""
    print("Verification des fichiers de configuration...")
    
    # Vérifier matelas_config.json
    if not Path('matelas_config.json').exists():
        if Path('matelas_config.json.template').exists():
            print("Creation de matelas_config.json depuis le template...")
            shutil.copy('matelas_config.json.template', 'matelas_config.json')
        else:
            print("[!] Aucun fichier de configuration matelas trouvé")
            print("[!] L'application pourrait ne pas fonctionner correctement")
    
    # Vérifier config.py
    if not Path('config.py').exists():
        print("[!] Fichier config.py manquant - nécessaire pour le fonctionnement")
    
    # Vérifier backend_interface.py
    if not Path('backend_interface.py').exists():
        print("[!] Fichier backend_interface.py manquant - nécessaire pour le fonctionnement")
    
    print("[OK] Vérification des fichiers terminée")

def build_executable():
    """Lance la compilation avec PyInstaller"""
    print("Compilation en cours...")
    print("Cela peut prendre plusieurs minutes...")
    
    try:
        # Nettoyer les anciens builds
        if os.path.exists('dist'):
            shutil.rmtree('dist')
            print("Ancien dossier dist supprime")
        
        if os.path.exists('build'):
            shutil.rmtree('build')
            print("Ancien dossier build supprime")
        
        # Lancer PyInstaller
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'matelas_processor.spec'
        ]
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("[OK] Compilation terminee avec succes!")
        
        # Vérifier que l'exécutable a été créé
        exe_path = Path('dist/MatelasProcessor.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"[OK] Executable cree: {exe_path.absolute()}")
            print(f"Taille: {size_mb:.1f} MB")
            return True
        else:
            print("[ERREUR] Executable non trouve apres compilation")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"[ERREUR] Erreur de compilation:")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
        return False

def create_installer_script():
    """Crée un script batch pour faciliter la distribution"""
    print("Creation du script d'installation...")
    
    batch_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo    Processeur de Devis Literie
echo         Installation Windows
echo ========================================
echo.

REM Verifier si on est sur Windows
if not "%OS%"=="Windows_NT" (
    echo Ce script est concu pour Windows uniquement.
    pause
    exit /b 1
)

echo Installation en cours...

REM Creer le dossier de destination si necessaire
if not exist "%PROGRAMFILES%\\MatelasProcessor" (
    mkdir "%PROGRAMFILES%\\MatelasProcessor"
)

REM Copier l'executable
copy "MatelasProcessor.exe" "%PROGRAMFILES%\\MatelasProcessor\\MatelasProcessor.exe" >nul
if errorlevel 1 (
    echo Erreur: Impossible de copier l'executable.
    echo Essayez d'executer ce script en tant qu'administrateur.
    pause
    exit /b 1
)

REM Creer un raccourci sur le bureau (optionnel)
set "desktop=%USERPROFILE%\\Desktop"
if exist "%desktop%" (
    echo Creation du raccourci sur le bureau...
    powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%desktop%\\Matelas Processor.lnk'); $Shortcut.TargetPath = '%PROGRAMFILES%\\MatelasProcessor\\MatelasProcessor.exe'; $Shortcut.Save()"
)

echo.
echo [OK] Installation terminee avec succes !
echo.
echo L'application peut etre lancee depuis :
echo - Le raccourci sur le bureau : "Matelas Processor"  
echo - Le dossier : %PROGRAMFILES%\\MatelasProcessor\\
echo.
pause
'''
    
    with open('dist/install.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    print("Script d'installation cree: dist/install.bat")

def main():
    """Fonction principale de compilation"""
    print("=== CREATION D'EXECUTABLE WINDOWS ===")
    print("Application: Processeur de Devis Literie")
    print("=" * 50)
    
    try:
        # Étapes de compilation
        check_requirements()
        check_config_files()
        create_version_info()
        create_icon()
        create_spec_file()
        
        if build_executable():
            create_installer_script()
            
            print("\n[OK] COMPILATION REUSSIE!")
            print("=" * 50)
            print("Fichiers crees:")
            print("   - dist/MatelasProcessor.exe (executable principal)")
            print("   - dist/install.bat (script d'installation)")
            print("\nInstructions:")
            print("   1. Testez l'executable sur votre machine Windows")
            print("   2. Copiez le dossier 'dist' sur la machine Windows cible")
            print("   3. Executez install.bat en tant qu'administrateur pour installer")
            print("   4. Ou lancez directement MatelasProcessor.exe")
            print("\nNote: Premier lancement peut etre lent (extraction)")
            
        else:
            print("\n[ERREUR] COMPILATION ECHOUEE")
            print("Verifiez les erreurs ci-dessus")
            
    except Exception as e:
        print(f"\n[ERREUR] Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()