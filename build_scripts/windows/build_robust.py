#!/usr/bin/env python3
"""
Script de compilation robuste avec détection automatique des modules backend
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def get_backend_modules():
    """Détecte automatiquement tous les modules backend"""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        return []
    
    modules = []
    for py_file in backend_dir.glob("*.py"):
        if py_file.name != "__init__.py":
            module_name = f"backend.{py_file.stem}"
            modules.append(module_name)
    
    return modules

def clean_build():
    """Nettoie les dossiers de build précédents"""
    print("🧹 Nettoyage des dossiers de build...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Supprimé: {dir_name}")
    
    # Nettoyer les fichiers .spec
    for spec_file in Path('.').glob('*.spec'):
        spec_file.unlink()
        print(f"   Supprimé: {spec_file}")

def create_robust_spec():
    """Crée un fichier .spec robuste avec tous les modules backend"""
    print("📝 Création du fichier .spec robuste...")
    
    # Détecter tous les modules backend
    backend_modules = get_backend_modules()
    print(f"📦 Modules backend détectés: {len(backend_modules)}")
    
    # Créer la liste des hiddenimports
    hidden_imports = [
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'PyQt6.QtPrintSupport',
        'backend',
    ] + backend_modules
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('template', 'template'),
        ('config', 'config'),
        ('backend/Référentiels', 'backend/Référentiels'),
        ('backend/template', 'backend/template'),
        ('backend/templates', 'backend/templates'),
    ],
    hiddenimports={hidden_imports},
    hookspath=[],
    hooksconfig={{}},
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
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/lit-double.ico' if os.path.exists('assets/lit-double.ico') else None,
)
'''
    
    with open('matelas_app_robust.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec robuste créé")

def build_executable():
    """Compile l'exécutable avec le fichier .spec robuste"""
    print("🔨 Compilation de l'exécutable...")
    
    try:
        # Compiler avec le fichier .spec robuste
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'matelas_app_robust.spec'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Compilation réussie!")
            print(f"📁 Exécutable créé dans: dist/MatelasApp")
            return True
        else:
            print("❌ Erreur de compilation:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la compilation: {e}")
        return False

def main():
    print("🚀 Compilation robuste avec détection automatique des modules")
    print("=" * 60)
    
    # Vérifier que PyQt6 est installé
    try:
        import PyQt6
        print("✅ PyQt6 installé")
    except ImportError:
        print("❌ PyQt6 non installé. Installation...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6'])
    
    # Étapes de compilation
    clean_build()
    create_robust_spec()
    
    if build_executable():
        print("\n🎉 Compilation terminée avec succès!")
        print("💡 Pour tester l'exécutable:")
        print("   ./dist/MatelasApp")
    else:
        print("\n❌ Échec de la compilation")
        print("💡 Essayez de compiler avec console pour voir les erreurs:")
        print("   python3 build_debug_console_fixed.py")

if __name__ == "__main__":
    main() 