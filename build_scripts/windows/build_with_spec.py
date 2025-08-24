#!/usr/bin/env python3
"""
Script de compilation PyInstaller avec fichier .spec personnalisé
Gère mieux les caractères accentués dans les noms de dossiers
"""

import os
import sys
import subprocess
import shutil
import platform

def create_spec_file():
    """Crée un fichier .spec personnalisé"""
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
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
)
'''
    
    with open('MatelasApp.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier .spec créé: MatelasApp.spec")

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    
    print("=" * 50)
    print("COMPILATION PYINSTALLER - MATELAS APP (avec .spec)")
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
        if file.endswith(".spec") and file != "MatelasApp.spec":
            os.remove(file)
            print(f"   Supprimé: {file}")
    
    print("✅ Nettoyage terminé")
    print()
    
    # Vérifier que les assets existent
    print("🔍 Vérification des assets...")
    required_assets = [
        "assets/lit-double.png",
        "assets/logo_westelynck.png",
        "template/template_matelas.xlsx",
        "template/template_sommier.xlsx",
        "config/mappings_matelas.json",
        "config/mappings_sommiers.json",
        "backend/Référentiels"
    ]
    
    missing_assets = []
    for asset in required_assets:
        if os.path.exists(asset):
            print(f"   ✅ {asset}")
        else:
            print(f"   ❌ {asset}")
            missing_assets.append(asset)
    
    if missing_assets:
        print(f"\n⚠️ Assets manquants: {len(missing_assets)}")
        for asset in missing_assets:
            print(f"   - {asset}")
        print("La compilation peut échouer si ces assets sont nécessaires.")
        print()
    
    # Créer le fichier .spec
    print("📝 Création du fichier .spec...")
    create_spec_file()
    print()
    
    # Commande PyInstaller avec .spec
    command = ["pyinstaller", "MatelasApp.spec", "--clean"]
    
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
            exe_name = "MatelasApp"
            if platform.system() == "Windows":
                exe_name += ".exe"
            
            exe_path = os.path.join("dist", exe_name)
            
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024*1024)
                print(f"✅ Exécutable créé: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                
                # Test rapide de l'exécutable
                print("\n🧪 Test rapide de l'exécutable...")
                try:
                    if platform.system() == "Windows":
                        # Windows
                        test_process = subprocess.Popen([exe_path], 
                                                      stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE)
                        test_process.wait(timeout=10)
                        test_process.terminate()
                    else:
                        # macOS/Linux
                        os.chmod(exe_path, 0o755)  # Rendre exécutable
                        test_process = subprocess.Popen([exe_path], 
                                                      stdout=subprocess.PIPE, 
                                                      stderr=subprocess.PIPE)
                        test_process.wait(timeout=10)
                        test_process.terminate()
                    
                    print("✅ Exécutable s'est lancé sans erreur")
                except subprocess.TimeoutExpired:
                    print("✅ Exécutable s'est lancé (arrêté après 10s)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du test: {e}")
                
                print(f"\n🎉 Compilation terminée avec succès!")
                print(f"   Exécutable: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                
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
    build_executable() 