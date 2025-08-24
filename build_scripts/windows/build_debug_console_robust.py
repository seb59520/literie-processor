#!/usr/bin/env python3
"""
Script de compilation debug avec console pour diagnostiquer les problèmes d'imports
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
            print(f"   📄 {module_name}")
    
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

def create_debug_spec():
    """Crée un fichier .spec debug avec console"""
    print("📝 Création du fichier .spec debug...")
    
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
    name='MatelasApp_Debug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console visible pour debug
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/lit-double.ico' if os.path.exists('assets/lit-double.ico') else None,
)
'''
    
    with open('matelas_app_debug.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec debug créé")

def build_debug_executable():
    """Compile l'exécutable debug avec console"""
    print("🔨 Compilation de l'exécutable debug...")
    
    try:
        # Compiler avec le fichier .spec debug
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'matelas_app_debug.spec'
        ], capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print("✅ Compilation debug réussie!")
            print(f"📁 Exécutable debug créé dans: dist/MatelasApp_Debug")
            return True
        else:
            print("❌ Erreur de compilation debug:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la compilation debug: {e}")
        return False

def test_imports():
    """Teste les imports problématiques"""
    print("\n🧪 Test des imports problématiques...")
    
    try:
        import backend.select43_longueur_housse_utils
        print("✅ backend.select43_longueur_housse_utils - OK")
    except ImportError as e:
        print(f"❌ backend.select43_longueur_housse_utils - ERREUR: {e}")
    
    try:
        from backend.select43_longueur_housse_utils import get_select43_longueur_housse_value
        print("✅ get_select43_longueur_housse_value - OK")
    except ImportError as e:
        print(f"❌ get_select43_longueur_housse_value - ERREUR: {e}")

def main():
    print("🚀 Compilation debug avec console pour diagnostic")
    print("=" * 60)
    
    # Vérifier que PyQt6 est installé
    try:
        import PyQt6
        print("✅ PyQt6 installé")
    except ImportError:
        print("❌ PyQt6 non installé. Installation...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6'])
    
    # Test des imports problématiques
    test_imports()
    
    # Étapes de compilation
    clean_build()
    create_debug_spec()
    
    if build_debug_executable():
        print("\n🎉 Compilation debug terminée!")
        print("💡 Pour tester l'exécutable debug:")
        print("   ./dist/MatelasApp_Debug")
        print("   (La console restera ouverte pour voir les erreurs détaillées)")
    else:
        print("\n❌ Échec de la compilation debug")

if __name__ == "__main__":
    main() 