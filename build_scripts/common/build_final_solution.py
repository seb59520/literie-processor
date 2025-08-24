#!/usr/bin/env python3
"""
Script de compilation final avec solution robuste pour tous les modules
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

def create_final_spec():
    """Crée un fichier .spec final avec tous les modules explicitement listés"""
    print("📝 Création du fichier .spec final...")
    
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
        'PyQt6.QtPrintSupport',
        'backend',
        'backend.article_utils',
        'backend.asset_utils',
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
        'backend.main',
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
        'config',
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
    
    with open('matelas_app_final.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec final créé")

def build_executable():
    """Compile l'exécutable avec le fichier .spec final"""
    print("🔨 Compilation de l'exécutable...")
    
    try:
        # Compiler avec le fichier .spec final
        result = subprocess.run([
            sys.executable, '-m', 'PyInstaller',
            '--clean',
            'matelas_app_final.spec'
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

def test_imports():
    """Teste les imports problématiques"""
    print("\n🧪 Test des imports problématiques...")
    
    problematic_modules = [
        'backend.latex_renforce_utils',
        'backend.select43_longueur_housse_utils',
        'backend.main',
        'backend.llm_provider'
    ]
    
    for module in problematic_modules:
        try:
            __import__(module)
            print(f"✅ {module} - OK")
        except ImportError as e:
            print(f"❌ {module} - ERREUR: {e}")

def main():
    print("🚀 Compilation finale avec solution robuste")
    print("=" * 50)
    
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
    create_final_spec()
    
    if build_executable():
        print("\n🎉 Compilation terminée avec succès!")
        print("💡 Pour tester l'exécutable:")
        print("   ./dist/MatelasApp")
    else:
        print("\n❌ Échec de la compilation")

if __name__ == "__main__":
    main() 