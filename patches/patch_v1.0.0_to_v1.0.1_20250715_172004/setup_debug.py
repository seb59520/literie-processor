#!/usr/bin/env python3
"""
Script pour créer un exécutable avec console pour déboguer
"""

import os
import sys
import subprocess
import shutil

def create_debug_spec():
    """Crée un fichier spec avec console pour déboguer"""
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
    name='MatelasApp_Debug',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # CONSOLE ACTIVEE POUR DEBOGUER
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open("matelas_debug.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("OK: Fichier spec debug cree")

def build_debug_executable():
    """Compile l'exécutable de débogage"""
    print("Compilation de l'executable debug...")
    
    # Nettoyer
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
    
    # Compiler
    try:
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "matelas_debug.spec"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("OK: Executable debug compile")
            return True
        else:
            print(f"ERREUR: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"ERREUR: {e}")
        return False

def main():
    """Fonction principale"""
    print("Creation de l'executable debug...")
    print("=" * 50)
    
    create_debug_spec()
    
    if build_debug_executable():
        print("\nOK: Executable debug cree!")
        print("Lancez: dist\\MatelasApp_Debug.exe")
        print("Vous verrez les erreurs dans la console")
    else:
        print("\nERREUR: Echec de la compilation")

if __name__ == "__main__":
    main() 