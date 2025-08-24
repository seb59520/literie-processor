#!/usr/bin/env python3
"""
Script de compilation avec console pour diagnostiquer les erreurs PyQt6
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

def create_debug_spec():
    """Crée un fichier .spec avec console pour debug"""
    print("📝 Création du fichier .spec debug...")
    
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

def test_pyqt6_import():
    """Teste l'import de PyQt6"""
    print("🧪 Test des imports PyQt6...")
    
    try:
        import PyQt6
        print(f"✅ PyQt6: {PyQt6.__version__}")
        
        import PyQt6.QtCore
        print("✅ PyQt6.QtCore")
        
        import PyQt6.QtGui
        print("✅ PyQt6.QtGui")
        
        import PyQt6.QtWidgets
        print("✅ PyQt6.QtWidgets")
        
        import PyQt6.sip
        print("✅ PyQt6.sip")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur d'import PyQt6: {e}")
        return False

def main():
    print("🚀 Début de la compilation debug avec PyQt6")
    print("=" * 50)
    
    # Test des imports PyQt6
    if not test_pyqt6_import():
        print("❌ Problème avec PyQt6. Installation...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'PyQt6'])
        if not test_pyqt6_import():
            print("❌ Impossible d'installer PyQt6")
            return
    
    # Étapes de compilation
    clean_build()
    create_debug_spec()
    
    if build_debug_executable():
        print("\n🎉 Compilation debug terminée!")
        print("💡 Pour tester l'exécutable debug:")
        print("   ./dist/MatelasApp_Debug")
        print("   (La console restera ouverte pour voir les erreurs)")
    else:
        print("\n❌ Échec de la compilation debug")

if __name__ == "__main__":
    main() 