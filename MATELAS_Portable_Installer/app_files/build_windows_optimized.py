#!/usr/bin/env python3
"""
Script optimisé pour créer un exécutable Windows plus compact
"""

import os
import sys
import subprocess
from pathlib import Path

def create_optimized_spec():
    """Crée un fichier .spec optimisé pour réduire la taille"""
    print("Creation du fichier .spec optimise...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Seulement les fichiers essentiels
datas = [
    ('matelas_config.json', '.'),
    ('config.py', '.'),
]

# Modules cachés minimaux
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui', 
    'PyQt6.QtWidgets',
    'requests',
    'pandas',
    'openpyxl',
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
        'matplotlib', 'scipy', 'numpy.distutils', 
        'tcl', 'tk', 'tkinter',  # Interface graphique non utilisée
        'PIL', 'Pillow',  # Si non utilisé
        'jupyter', 'notebook',  # Développement
        'pytest', 'unittest',  # Tests
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
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    version='version_info.txt',
    icon='assets/lit-double.ico' if os.path.exists('assets/lit-double.ico') else 'assets/app_icon.ico'
)
'''
    
    with open('matelas_processor_optimized.spec', 'w') as f:
        f.write(spec_content)
    
    print("[OK] Fichier .spec optimise cree")
    return True

def build_optimized():
    """Compilation optimisée"""
    print("Compilation de l'executable optimise...")
    
    try:
        # Compilation avec optimisations
        cmd = [
            sys.executable, '-m', 'PyInstaller',
            '--clean',              # Nettoyer avant compilation
            '--noconfirm',          # Pas de confirmation
            '--log-level=WARN',     # Moins de logs
            'matelas_processor_optimized.spec'
        ]
        
        print(f"Commande: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("[OK] Compilation reussie!")
            
            # Vérifier la taille du fichier
            exe_path = Path('dist/MatelasProcessor.exe')
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"[INFO] Taille de l'executable: {size_mb:.1f} MB")
                
                if size_mb > 500:  # Si plus de 500MB
                    print("[!] ATTENTION: Fichier volumineux!")
                    print("Considérez utiliser la version portable à la place")
                
                return True
        else:
            print(f"[ERREUR] Compilation echouee: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERREUR] Exception durant la compilation: {e}")
        return False

def create_portable_version():
    """Crée une version portable (dossier + .bat)"""
    print("Creation de la version portable...")
    
    try:
        # Créer la structure portable
        portable_dir = Path('dist_portable')
        portable_dir.mkdir(exist_ok=True)
        
        # Script de lancement portable
        launcher_content = '''@echo off
echo ========================================
echo    Processeur de Devis Literie
echo           Version Portable
echo ========================================
echo.

REM Vérifier Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe
    echo Veuillez installer Python 3.8+ depuis python.org
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo Installation des dependances...
pip install PyQt6 requests pandas openpyxl psutil >nul 2>&1

REM Lancer l'application
echo Lancement de l'application...
python app_gui.py

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
            'matelas_config.json',
            'requirements.txt'
        ]
        
        for file in essential_files:
            if Path(file).exists():
                shutil.copy(file, portable_dir)
        
        # Copier les dossiers
        for folder in ['backend', 'utilities']:
            if Path(folder).exists():
                shutil.copytree(folder, portable_dir / folder, dirs_exist_ok=True)
        
        print(f"[OK] Version portable creee dans: {portable_dir}")
        print("Instructions:")
        print("1. Copiez le dossier 'dist_portable' sur la machine Windows")  
        print("2. Executez 'Lancer_Matelas.bat'")
        
        return True
        
    except Exception as e:
        print(f"[ERREUR] Creation portable echouee: {e}")
        return False

def main():
    """Fonction principale avec options"""
    print("=== COMPILATION WINDOWS OPTIMISEE ===")
    print("1. Version executable (.exe)")
    print("2. Version portable (dossier + .bat)")
    print("3. Les deux versions")
    
    choice = input("\nChoisissez (1/2/3): ").strip()
    
    success = False
    
    if choice in ['1', '3']:
        # Version exécutable
        if create_optimized_spec():
            success = build_optimized()
    
    if choice in ['2', '3']:
        # Version portable
        success = create_portable_version() or success
    
    if success:
        print("\n[OK] CREATION REUSSIE!")
        print("=" * 40)
        
        if choice in ['1', '3'] and Path('dist/MatelasProcessor.exe').exists():
            print("Version executable:")
            print("   - dist/MatelasProcessor.exe")
        
        if choice in ['2', '3'] and Path('dist_portable').exists():
            print("Version portable:")
            print("   - dist_portable/ (copiez ce dossier)")
            
        print("\nRecommandations:")
        print("- Si l'exe est trop volumineux: utilisez la version portable")
        print("- Testez sur Windows avant distribution")
        
    else:
        print("\n[ERREUR] CREATION ECHOUEE")

if __name__ == "__main__":
    main()