#!/usr/bin/env python3
"""
Script amélioré pour créer un exécutable Windows avec la dernière version
Utilise la version du fichier version.py et inclut toutes les optimisations récentes
"""

import os
import sys
import subprocess
from pathlib import Path

def get_current_version():
    """Récupère la version actuelle depuis version.py"""
    try:
        sys.path.insert(0, '.')
        from version import VERSION, BUILD_DATE, BUILD_NUMBER
        return VERSION, BUILD_DATE, BUILD_NUMBER
    except Exception as e:
        print(f"Erreur import version: {e}, utilisation version par défaut")
        return "3.9.0", "2025-08-31", "20250831"

def create_version_info():
    """Crée le fichier version_info.txt avec la version actuelle"""
    version, build_date, build_number = get_current_version()
    version_parts = version.split('.')
    major, minor, patch = int(version_parts[0]), int(version_parts[1]), int(version_parts[2])
    
    print(f"Création version_info.txt pour version {version}")
    
    version_content = f'''VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({major}, {minor}, {patch}, 0),
    prodvers=({major}, {minor}, {patch}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo([
      StringTable(u'040904B0', [
        StringStruct(u'CompanyName', u'Westelynck'),
        StringStruct(u'FileDescription', u'Processeur de Devis Literie'),
        StringStruct(u'FileVersion', u'{version}.0'),
        StringStruct(u'InternalName', u'MatelasProcessor'),
        StringStruct(u'LegalCopyright', u'© 2025 Westelynck. Tous droits réservés.'),
        StringStruct(u'OriginalFilename', u'MatelasProcessor.exe'),
        StringStruct(u'ProductName', u'Matelas Processor v{version}'),
        StringStruct(u'ProductVersion', u'{version}.0')
      ])
    ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)
'''
    
    with open('version_info.txt', 'w', encoding='utf-8') as f:
        f.write(version_content)
    
    print(f"[OK] Fichier version_info.txt créé pour version {version}")
    return True

def create_enhanced_spec():
    """Crée un fichier .spec optimisé avec toutes les dépendances"""
    print("Création du fichier .spec optimisé...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os

block_cipher = None

# Fichiers de données essentiels avec gestion conditionnelle
datas = [
    ('matelas_config.json', '.') if os.path.exists('matelas_config.json') else None,
    ('matelas_config.json.template', '.') if os.path.exists('matelas_config.json.template') else None,
    ('config.py', '.') if os.path.exists('config.py') else None,
    ('backend', 'backend') if os.path.exists('backend') else None,
    ('config', 'config') if os.path.exists('config') else None,
    ('template', 'template') if os.path.exists('template') else None,
    ('backend_interface.py', '.') if os.path.exists('backend_interface.py') else None,
    ('version.py', '.') if os.path.exists('version.py') else None,
    ('EULA.txt', '.') if os.path.exists('EULA.txt') else None,
    ('assets', 'assets') if os.path.exists('assets') else None,
]

# Filtrer les None
datas = [d for d in datas if d is not None]

# Modules cachés complets incluant les nouvelles optimisations
hiddenimports = [
    # PyQt6
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'PyQt6.QtNetwork',
    
    # Réseau et HTTP
    'requests',
    'urllib3',
    'urllib3.util.retry',
    'urllib3.exceptions',
    
    # Excel et données
    'openpyxl',
    'openpyxl.workbook',
    'openpyxl.worksheet',
    'openpyxl.styles',
    'openpyxl.styles.font',
    'openpyxl.styles.fill',
    'openpyxl.styles.border',
    'openpyxl.utils',
    'openpyxl.utils.cell',
    'pandas',
    
    # PDF
    'fitz',  # PyMuPDF
    
    # Standard library
    'json',
    'pathlib',
    'datetime',
    'logging',
    'logging.handlers',
    'csv',
    'hashlib',
    'base64',
    'tempfile',
    'shutil',
    'platform',
    'subprocess',
    'webbrowser',
    're',
    'sqlite3',
    'enum',
    'typing',
    'dataclasses',
    'functools',
    'itertools',
    
    # Cryptographie
    'cryptography',
    'cryptography.fernet',
    'cryptography.hazmat.primitives',
    'cryptography.hazmat.backends',
    
    # Threading et async
    'threading',
    'queue',
    'asyncio',
    'concurrent.futures',
    
    # Monitoring
    'psutil',
    
    # Markdown (optionnel)
    'markdown',
    
    # Cache et optimisations
    'pickle',
    'collections',
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
        'matplotlib', 
        'scipy', 
        'numpy.distutils', 
        'tcl', 
        'tk', 
        'tkinter',
        'PIL', 
        'Pillow',
        'jupyter', 
        'notebook',
        'pytest', 
        'unittest',
        'IPython',
        'sphinx',
        'pydoc',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Supprimer les fichiers non essentiels
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
    strip=True,  # Réduction de taille
    upx=True,    # Compression UPX si disponible
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Application GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt' if os.path.exists('version_info.txt') else None,
    icon='assets/lit-double.ico' if os.path.exists('assets/lit-double.ico') else 'assets/app_icon.ico' if os.path.exists('assets/app_icon.ico') else 'assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
'''
    
    with open('matelas_processor_enhanced.spec', 'w') as f:
        f.write(spec_content)
    
    print("[OK] Fichier .spec optimisé créé")
    return True

def build_executable():
    """Compilation optimisée avec gestion d'erreurs"""
    print("Compilation de l'exécutable en cours...")
    print("Cela peut prendre plusieurs minutes...")
    
    try:
        # Nettoyer les anciens builds
        if os.path.exists('dist'):
            import shutil
            shutil.rmtree('dist')
            print("Ancien dossier dist supprimé")
        
        if os.path.exists('build'):
            import shutil
            shutil.rmtree('build')
            print("Ancien dossier build supprimé")
        
        # Compilation avec optimisations
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',              # Nettoyer avant compilation
            '--noconfirm',          # Pas de confirmation
            '--log-level=WARN',     # Moins de logs
            'matelas_processor_enhanced.spec'
        ]
        
        print(f"Commande: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Compilation réussie!")
            
            # Vérifier la taille du fichier
            exe_path = Path('dist/MatelasProcessor.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"[INFO] Taille de l'exécutable: {size_mb:.1f} MB")
                print(f"[INFO] Fichier créé: {exe_path.absolute()}")
                
                if size_mb > 500:  # Si plus de 500MB
                    print("[!] ATTENTION: Fichier volumineux!")
                    print("Considérez utiliser la version portable à la place")
                
                return True
        else:
            print(f"[ERREUR] Compilation échouée:")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Exception durant la compilation: {e}")
        return False

def create_portable_version():
    """Crée une version portable améliorée"""
    print("Création de la version portable...")
    
    try:
        # Créer la structure portable
        portable_dir = Path('dist_portable')
        portable_dir.mkdir(exist_ok=True)
        
        # Script de lancement portable amélioré
        launcher_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo    Processeur de Devis Literie
echo           Version Portable
echo ========================================
echo.

REM Obtenir la version si possible
if exist version.py (
    for /f "tokens=3 delims= " %%a in ('findstr /c:"VERSION = " version.py') do (
        set VERSION=%%a
        set VERSION=!VERSION:"=!
    )
    echo Version: !VERSION!
    echo.
)

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    echo Veuillez installer Python 3.8+ depuis python.org
    pause
    exit /b 1
)

REM Vérifier pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] pip n'est pas disponible
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo Installation/verification des dependances...
pip install PyQt6 requests pandas openpyxl psutil PyMuPDF cryptography >nul 2>&1
if errorlevel 1 (
    echo [ATTENTION] Certaines dependances n'ont pas pu etre installees
    echo L'application pourrait ne pas fonctionner correctement
    pause
)

REM Vérifier les fichiers essentiels
if not exist app_gui.py (
    echo [ERREUR] Fichier app_gui.py manquant
    pause
    exit /b 1
)

if not exist config.py (
    echo [ERREUR] Fichier config.py manquant
    pause
    exit /b 1
)

REM Lancer l'application
echo Lancement de l'application...
python app_gui.py

if errorlevel 1 (
    echo.
    echo [ERREUR] L'application s'est fermee avec une erreur
    echo Verifiez les dependances et les fichiers de configuration
    pause
)

pause
'''
        
        # Créer le lanceur
        with open(portable_dir / 'Lancer_Matelas.bat', 'w', encoding='utf-8') as f:
            f.write(launcher_content)
        
        # Copier les fichiers essentiels
        import shutil
        essential_files = [
            'app_gui.py',
            'config.py', 
            'backend_interface.py',
            'version.py',
            'matelas_config.json',
            'matelas_config.json.template',
            'EULA.txt',
            'requirements.txt',
            'requirements_gui.txt'
        ]
        
        for file in essential_files:
            if Path(file).exists():
                shutil.copy(file, portable_dir)
                print(f"Copié: {file}")
        
        # Copier les dossiers essentiels
        essential_folders = ['backend', 'config', 'template', 'assets']
        for folder in essential_folders:
            if Path(folder).exists():
                shutil.copytree(folder, portable_dir / folder, dirs_exist_ok=True)
                print(f"Copié dossier: {folder}")
        
        # Créer un README pour la version portable
        readme_content = f"""# Matelas Processor - Version Portable

## Installation

1. Assurez-vous que Python 3.8+ est installé
2. Exécutez 'Lancer_Matelas.bat'

## Configuration

- Modifiez `matelas_config.json` pour vos paramètres
- Les templates Excel sont dans le dossier `template/`
- Les référentiels sont dans `backend/Référentiels/`

## Dépendances requises

- PyQt6
- requests
- pandas
- openpyxl
- psutil
- PyMuPDF
- cryptography

Version générée le: {Path(__file__).stat().st_mtime}
"""
        
        with open(portable_dir / 'README.txt', 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"[OK] Version portable créée dans: {portable_dir.absolute()}")
        print("Instructions:")
        print("1. Copiez le dossier 'dist_portable' sur la machine Windows")  
        print("2. Exécutez 'Lancer_Matelas.bat'")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Création portable échouée: {e}")
        return False

def create_installer_script():
    """Crée un script d'installation Windows avancé"""
    if not Path('dist/MatelasProcessor.exe').exists():
        return False
        
    print("Création du script d'installation...")
    
    version, build_date, build_number = get_current_version()
    
    installer_content = f'''@echo off
chcp 65001 >nul
echo ========================================
echo    Processeur de Devis Literie
echo         Version {version}
echo         Build {build_number}
echo ========================================
echo.

REM Vérifier les privilèges administrateur
net session >nul 2>&1
if errorlevel 1 (
    echo Ce script doit etre execute en tant qu'administrateur.
    echo Clic droit -> "Executer en tant qu'administrateur"
    pause
    exit /b 1
)

echo Installation en cours...

REM Créer le dossier de destination
set "INSTALL_DIR=%PROGRAMFILES%\\MatelasProcessor"
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    echo Dossier d'installation cree: %INSTALL_DIR%
)

REM Copier l'exécutable
echo Copie de l'executable...
copy "MatelasProcessor.exe" "%INSTALL_DIR%\\MatelasProcessor.exe" >nul
if errorlevel 1 (
    echo [ERREUR] Impossible de copier l'executable
    pause
    exit /b 1
)

REM Créer un raccourci sur le bureau
echo Creation du raccourci sur le bureau...
set "DESKTOP=%USERPROFILE%\\Desktop"
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP%\\Matelas Processor.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MatelasProcessor.exe'; $Shortcut.Description = 'Processeur de Devis Literie v{version}'; $Shortcut.Save()}}"

REM Créer un raccourci dans le menu Démarrer
echo Creation du raccourci dans le menu Demarrer...
set "STARTMENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%STARTMENU%\\Matelas Processor.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\\MatelasProcessor.exe'; $Shortcut.Description = 'Processeur de Devis Literie v{version}'; $Shortcut.Save()}}"

echo.
echo ========================================
echo [OK] Installation terminee avec succes !
echo ========================================
echo.
echo L'application peut etre lancee depuis :
echo - Le raccourci sur le bureau : "Matelas Processor"
echo - Le menu Demarrer : "Matelas Processor"  
echo - Le dossier : %INSTALL_DIR%\\
echo.
echo Version installee : {version}
echo Build : {build_number} ({build_date})
echo.
pause
'''
    
    with open('dist/install.bat', 'w', encoding='utf-8') as f:
        f.write(installer_content)
    
    print("Script d'installation créé: dist/install.bat")
    return True

def main():
    """Fonction principale améliorée"""
    version, build_date, build_number = get_current_version()
    
    print("=== COMPILATION WINDOWS OPTIMISEE ===")
    print(f"Application: Matelas Processor v{version}")
    print(f"Build: {build_number} ({build_date})")
    print("=" * 50)
    print()
    print("Options de compilation:")
    print("1. Version exécutable (.exe) - Recommandé")
    print("2. Version portable (dossier + .bat)")
    print("3. Les deux versions")
    print("4. Test rapide (vérifications uniquement)")
    
    choice = input("\nChoisissez (1/2/3/4): ").strip()
    
    if choice == '4':
        print("\n=== VERIFICATIONS ===")
        create_version_info()
        create_enhanced_spec()
        print("[OK] Fichiers de configuration créés")
        return
    
    success = False
    
    if choice in ['1', '3']:
        print("\n=== CREATION EXECUTABLE ===")
        if create_version_info() and create_enhanced_spec():
            if build_executable():
                create_installer_script()
                success = True
    
    if choice in ['2', '3']:
        print("\n=== CREATION VERSION PORTABLE ===")
        success = create_portable_version() or success
    
    print("\n" + "=" * 50)
    if success:
        print("[OK] CREATION REUSSIE!")
        print()
        
        if choice in ['1', '3'] and Path('dist/MatelasProcessor.exe').exists():
            exe_path = Path('dist/MatelasProcessor.exe')
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print("Version exécutable:")
            print(f"   - dist/MatelasProcessor.exe ({size_mb:.1f} MB)")
            print("   - dist/install.bat (installateur Windows)")
        
        if choice in ['2', '3'] and Path('dist_portable').exists():
            print("Version portable:")
            print("   - dist_portable/ (copiez ce dossier)")
            print("   - dist_portable/Lancer_Matelas.bat (lanceur)")
            
        print()
        print("Recommandations:")
        print(f"- Version {version} avec build {build_number}")
        print("- Testez sur Windows avant distribution")
        print("- Premier lancement peut être lent (extraction)")
        if choice in ['1', '3']:
            print("- Exécutez install.bat en tant qu'administrateur")
        
    else:
        print("[ERREUR] CREATION ECHOUEE")
        print("Vérifiez les erreurs ci-dessus")

if __name__ == "__main__":
    main()