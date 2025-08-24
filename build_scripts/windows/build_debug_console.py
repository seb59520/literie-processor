#!/usr/bin/env python3
"""
Script de compilation avec console pour debug
"""

import os
import sys
import subprocess
import shutil
import platform

def create_debug_spec():
    """Crée un fichier .spec pour debug avec console"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui_fixed.py'],
    pathex=['backend'],
    binaries=[],
    datas=[
        ('backend/template', 'backend/template'),
        ('backend/templates', 'backend/templates'),
        ('backend/Référentiels', 'backend/Référentiels'),
        ('template', 'template'),
        ('config', 'config'),
        ('assets', 'assets'),
    ],
    hiddenimports=[
        'backend.asset_utils',
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'PyQt6.QtPrintSupport',
        'fastapi',
        'jinja2',
        'uvicorn',
        'pandas',
        'openpyxl',
        'requests',
        'cryptography',
        'backend_interface',
        'config',
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
    name='MatelasApp_DebugConsole',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Console activée pour voir les erreurs
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('MatelasApp_DebugConsole.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec debug créé: MatelasApp_DebugConsole.spec")

def build_debug_executable():
    """Compile l'exécutable debug avec console"""
    
    print("=" * 50)
    print("COMPILATION DEBUG AVEC CONSOLE")
    print("=" * 50)
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # Nettoyer les anciens fichiers
    print("🧹 Nettoyage...")
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
            print(f"   Supprimé: {dir_to_clean}")
    
    # Supprimer les anciens fichiers .spec
    for file in os.listdir("."):
        if file.endswith(".spec") and file != "MatelasApp_DebugConsole.spec":
            os.remove(file)
            print(f"   Supprimé: {file}")
    
    print("✅ Nettoyage terminé")
    print()
    
    # Vérifier que les fichiers corrigés existent
    if not os.path.exists('run_gui_fixed.py'):
        print("❌ run_gui_fixed.py manquant")
        print("   Exécutez d'abord: python fix_imports_manual.py")
        return False
    
    print("✅ run_gui_fixed.py trouvé")
    print()
    
    # Créer le fichier .spec debug
    print("📝 Création du fichier .spec debug...")
    create_debug_spec()
    print()
    
    # Commande PyInstaller
    command = ["pyinstaller", "MatelasApp_DebugConsole.spec", "--clean"]
    
    print("🚀 Commande PyInstaller:")
    print(" ".join(command))
    print()
    
    try:
        # Exécuter PyInstaller
        print("⏳ Compilation en cours...")
        print("   (Cela peut prendre plusieurs minutes)")
        
        result = subprocess.run(command, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Compilation réussie!")
            
            # Vérifier que l'exécutable existe
            exe_name = "MatelasApp_DebugConsole"
            if platform.system() == "Windows":
                exe_name += ".exe"
            
            exe_path = os.path.join("dist", exe_name)
            
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024*1024)
                print(f"✅ Exécutable créé: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print()
                print("🔍 Pour tester l'exécutable avec console:")
                print(f"   {exe_path}")
                print()
                print("💡 L'exécutable s'ouvrira avec une console")
                print("   Vous verrez exactement quelle erreur empêche le lancement")
                
            else:
                print(f"❌ Exécutable non trouvé: {exe_path}")
                print("Vérifiez les logs de compilation ci-dessus.")
        else:
            print("❌ Erreur de compilation:")
            print(result.stderr)
            print("\nLogs de compilation:")
            print(result.stdout)
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la compilation (10 minutes)")
        print("La compilation peut prendre plus de temps sur certains systèmes.")
    except FileNotFoundError:
        print("❌ PyInstaller non trouvé")
        print("Installez-le avec: pip install pyinstaller")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    build_debug_executable() 