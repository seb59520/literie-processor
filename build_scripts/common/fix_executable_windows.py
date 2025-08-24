#!/usr/bin/env python3
"""
Script pour recréer l'exécutable Windows avec console visible pour debug
"""

import os
import sys
import subprocess
import shutil

def create_debug_executable():
    """Crée un exécutable avec console visible pour debug"""
    
    print("Création d'un exécutable de debug avec console visible...")
    
    # Vérifier que PyInstaller est installé
    try:
        import PyInstaller
        print("OK: PyInstaller disponible")
    except ImportError:
        print("Installation de PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Nettoyer les anciens fichiers
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists("dist"):
        shutil.rmtree("dist")
    
    # Créer le fichier spec pour debug
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
        ('Référentiels', 'Référentiels'),
        ('Commandes', 'Commandes'),
        ('EULA.txt', '.'),
    ],
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
    hooksconfig={},
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
    name='MatelasApp_Debug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # CONSOLE VISIBLE POUR DEBUG
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open("matelas_debug.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("Fichier spec de debug créé")
    
    # Compiler avec PyInstaller
    print("Compilation en cours...")
    subprocess.check_call([sys.executable, "-m", "PyInstaller", "matelas_debug.spec"])
    
    print("OK: Exécutable de debug créé dans dist/MatelasApp_Debug.exe")
    print("Lancez-le pour voir les erreurs en temps réel")

if __name__ == "__main__":
    create_debug_executable() 