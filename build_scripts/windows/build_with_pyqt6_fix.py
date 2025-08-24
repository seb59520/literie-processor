#!/usr/bin/env python3
"""
Script de compilation avec correction PyQt6 et imports
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

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

def fix_imports():
    """Corrige les imports dans app_gui.py"""
    print("🔧 Correction des imports...")
    
    app_gui_path = 'app_gui.py'
    if not os.path.exists(app_gui_path):
        print("❌ app_gui.py non trouvé")
        return False
    
    with open(app_gui_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les imports relatifs par des imports absolus
    old_imports = [
        'from backend.',
        'import backend.',
        'sys.path.append("backend")',
        'sys.path.append(\'backend\')'
    ]
    
    new_imports = [
        'from .backend.',
        'import .backend.',
        '# sys.path.append("backend")  # Commenté pour PyInstaller',
        '# sys.path.append(\'backend\')  # Commenté pour PyInstaller'
    ]
    
    modified = False
    for old, new in zip(old_imports, new_imports):
        if old in content:
            content = content.replace(old, new)
            modified = True
            print(f"   Remplacé: {old} -> {new}")
    
    if modified:
        with open(app_gui_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Imports corrigés")
    else:
        print("ℹ️ Aucun import à corriger")
    
    return True

def create_spec_file():
    """Crée un fichier .spec personnalisé avec PyQt6"""
    print("📝 Création du fichier .spec...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
    hiddenimports=[
        'PyQt6',
        'PyQt6.QtCore',
        'PyQt6.QtGui',
        'PyQt6.QtWidgets',
        'PyQt6.sip',
        'backend',
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
        'backend.select43_longueur_housse_utils',
        'backend.select43_utils',
        'backend.sommier_analytics_utils',
        'backend.sommier_utils',
        'backend.secure_storage',
        'backend.version',
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
    
    with open('matelas_app.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec créé")

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    print("🔨 Compilation de l'exécutable...")
    
    try:
        # Compiler avec le fichier .spec
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'matelas_app.spec'
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
    print("🚀 Début de la compilation avec correction PyQt6")
    print("=" * 50)
    
    # Vérifier que PyQt6 est installé
    try:
        import PyQt6
        print("✅ PyQt6 installé")
    except ImportError:
        print("❌ PyQt6 non installé. Installation...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6'])
    
    # Étapes de compilation
    clean_build()
    fix_imports()
    create_spec_file()
    
    if build_executable():
        print("\n🎉 Compilation terminée avec succès!")
        print("💡 Pour tester l'exécutable:")
        print("   ./dist/MatelasApp")
    else:
        print("\n❌ Échec de la compilation")
        print("💡 Essayez de compiler avec console pour voir les erreurs:")
        print("   python build_debug_console.py")

if __name__ == "__main__":
    main() 