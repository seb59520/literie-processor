#!/usr/bin/env python3
"""
Script de compilation PyInstaller universel
Fonctionne sur Windows, macOS et Linux
"""

import os
import sys
import subprocess
import shutil
import platform

def build_executable():
    """Compile l'exécutable avec PyInstaller"""
    
    print("=" * 50)
    print("COMPILATION PYINSTALLER - MATELAS APP")
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
    
    # Supprimer les fichiers .spec existants
    for file in os.listdir("."):
        if file.endswith(".spec"):
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
        "config/mappings_sommiers.json"
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
    
    # Déterminer les séparateurs selon la plateforme
    is_windows = platform.system() == "Windows"
    path_sep = "\\" if is_windows else "/"
    data_sep = ";" if is_windows else ":"
    
    # Commande PyInstaller
    command = [
        "pyinstaller",
        "run_gui.py",
        "--onefile",
        "--windowed",
        "--name", "MatelasApp",
        "--paths=backend",
        "--collect-all", "PyQt6",
        f"--add-data", f"backend{path_sep}template{path_sep}*{data_sep}backend{path_sep}template",
        f"--add-data", f"backend{path_sep}templates{path_sep}*{data_sep}backend{path_sep}templates",
        f"--add-data", f"backend{path_sep}Référentiels{path_sep}*{data_sep}backend{path_sep}Référentiels",
        f"--add-data", f"template{path_sep}*{data_sep}template",
        f"--add-data", f"config{path_sep}*{data_sep}config",
        f"--add-data", f"assets{path_sep}*{data_sep}assets",
        "--hidden-import=backend.asset_utils",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=PyQt6.QtPrintSupport",
        "--hidden-import=fastapi",
        "--hidden-import=jinja2",
        "--hidden-import=uvicorn",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=requests",
        "--hidden-import=cryptography",
        "--hidden-import=backend_interface",
        "--hidden-import=config",
        "--hidden-import=backend.article_utils",
        "--hidden-import=backend.client_utils",
        "--hidden-import=backend.date_utils",
        "--hidden-import=backend.decoupe_noyau_utils",
        "--hidden-import=backend.dimensions_sommiers",
        "--hidden-import=backend.dimensions_utils",
        "--hidden-import=backend.excel_import_utils",
        "--hidden-import=backend.excel_sommier_import_utils",
        "--hidden-import=backend.fermete_utils",
        "--hidden-import=backend.hauteur_utils",
        "--hidden-import=backend.housse_utils",
        "--hidden-import=backend.latex_mixte7zones_longueur_housse_utils",
        "--hidden-import=backend.latex_mixte7zones_referentiel",
        "--hidden-import=backend.latex_naturel_longueur_housse_utils",
        "--hidden-import=backend.latex_naturel_referentiel",
        "--hidden-import=backend.latex_renforce_longueur_utils",
        "--hidden-import=backend.latex_renforce_utils",
        "--hidden-import=backend.llm_provider",
        "--hidden-import=backend.mapping_manager",
        "--hidden-import=backend.matelas_utils",
        "--hidden-import=backend.matiere_housse_utils",
        "--hidden-import=backend.mousse_rainuree7zones_longueur_housse_utils",
        "--hidden-import=backend.mousse_rainuree7zones_referentiel",
        "--hidden-import=backend.mousse_visco_longueur_utils",
        "--hidden-import=backend.mousse_visco_utils",
        "--hidden-import=backend.operation_utils",
        "--hidden-import=backend.poignees_utils",
        "--hidden-import=backend.pre_import_utils",
        "--hidden-import=backend.select43_longueur_housse_utils",
        "--hidden-import=backend.select43_utils",
        "--hidden-import=backend.sommier_analytics_utils",
        "--hidden-import=backend.sommier_utils",
        "--hidden-import=backend.secure_storage",
        "--clean"
    ]
    
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