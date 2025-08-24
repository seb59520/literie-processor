#!/usr/bin/env python3
"""
Script pour créer un exécutable installable de l'application Matelas
"""

import os
import sys
import subprocess
import shutil

def build_executable():
    """Construit un exécutable avec PyInstaller"""
    
    print("=== Construction de l'exécutable Matelas ===")
    
    # Vérifier si PyInstaller est installé
    try:
        import PyInstaller
        print("✅ PyInstaller est installé")
    except ImportError:
        print("❌ PyInstaller n'est pas installé")
        print("Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Créer le fichier spec pour PyInstaller
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('template', 'template'),
        ('backend', 'backend'),
        ('config.py', '.'),
    ],
    hiddenimports=[
        'openpyxl',
        'fitz',
        'httpx',
        'tkinter',
        'tkinter.ttk',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'json',
        'logging',
        'os',
        'sys',
        'tempfile',
        'shutil',
        'pathlib',
        'typing',
        'asyncio',
        'threading',
        'queue',
        'datetime',
        'unicodedata',
        'math',
        're',
        'csv',
        'openpyxl.utils',
        'openpyxl.workbook',
        'openpyxl.worksheet',
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
    name='Matelas_Processor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
'''
    
    # Écrire le fichier spec
    with open('matelas.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier spec créé")
    
    # Construire l'exécutable
    print("Construction de l'exécutable...")
    result = subprocess.run(['pyinstaller', 'matelas.spec', '--clean'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Exécutable construit avec succès")
        print("📁 L'exécutable se trouve dans: dist/Matelas_Processor")
        
        # Créer un dossier d'installation
        install_dir = "Matelas_Processor_Install"
        if os.path.exists(install_dir):
            shutil.rmtree(install_dir)
        
        os.makedirs(install_dir)
        
        # Copier l'exécutable et les fichiers nécessaires
        shutil.copytree("dist/Matelas_Processor", f"{install_dir}/Matelas_Processor")
        
        # Créer un fichier README
        readme_content = """# Matelas Processor

## Installation

1. Décompressez ce dossier où vous voulez
2. Double-cliquez sur Matelas_Processor.exe pour lancer l'application

## Utilisation

1. Lancez l'application
2. Sélectionnez vos fichiers PDF de commandes
3. Configurez les paramètres (semaine, année, etc.)
4. Cliquez sur "Traiter les fichiers"
5. Les fichiers Excel seront générés dans le dossier output/

## Support

Pour toute question, contactez l'équipe de développement.
"""
        
        with open(f"{install_dir}/README.txt", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"✅ Package d'installation créé: {install_dir}")
        
    else:
        print("❌ Erreur lors de la construction:")
        print(result.stderr)

if __name__ == "__main__":
    build_executable() 