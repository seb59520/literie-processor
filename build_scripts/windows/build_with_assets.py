#!/usr/bin/env python3
"""
Script de compilation PyInstaller optimisé avec gestion d'assets
"""

import os
import sys
import subprocess
import shutil
import platform

def build_executable():
    """Compile l'exécutable avec PyInstaller et gestion d'assets optimisée"""
    
    print("=== COMPILATION PYINSTALLER AVEC GESTION D'ASSETS ===")
    print(f"Plateforme: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print()
    
    # Nettoyer les anciens fichiers
    print("🧹 Nettoyage des anciens fichiers...")
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
    
    # Commande PyInstaller optimisée
    command = [
        "pyinstaller",
        "run_gui.py",
        "--onefile",
        "--windowed",
        "--name", "MatelasApp",
        "--paths=backend",
        "--collect-all", "PyQt6",
        "--add-data", "backend/template/*;backend/template",
        "--add-data", "backend/templates/*;backend/templates", 
        "--add-data", "backend/Référentiels/*;backend/Référentiels",
        "--add-data", "template/*;template",
        "--add-data", "config/*;config",
        "--add-data", "assets/*;assets",
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
        "--clean"
    ]
    
    # Ajouter l'icône si disponible
    icon_path = "assets/lit-double.ico"
    if os.path.exists(icon_path):
        command.extend(["--icon", icon_path])
        print(f"🎨 Icône utilisée: {icon_path}")
    else:
        print("⚠️ Icône non trouvée, utilisation de l'icône par défaut")
    
    print()
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
                    test_process = subprocess.Popen([exe_path], 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
                    test_process.wait(timeout=10)
                    print("✅ Exécutable s'est lancé sans erreur")
                except subprocess.TimeoutExpired:
                    test_process.terminate()
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


def test_assets_in_executable():
    """Test des assets dans l'exécutable compilé"""
    print("\n=== TEST DES ASSETS DANS L'EXECUTABLE ===")
    
    exe_name = "MatelasApp"
    if platform.system() == "Windows":
        exe_name += ".exe"
    
    exe_path = os.path.join("dist", exe_name)
    
    if not os.path.exists(exe_path):
        print("❌ Exécutable non trouvé. Compilez d'abord l'application.")
        return
    
    print(f"🧪 Test de l'exécutable: {exe_path}")
    
    # Créer un script de test pour l'exécutable
    test_script = '''#!/usr/bin/env python3
import sys
import os

# Simuler le mode PyInstaller
sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path
sys.path.append('backend')

try:
    from backend.asset_utils import get_asset_path, is_pyinstaller_mode
    
    print(f"Mode PyInstaller: {is_pyinstaller_mode()}")
    print(f"Base path: {sys._MEIPASS}")
    
    # Test des assets
    test_assets = ["lit-double.png", "logo_westelynck.png"]
    
    for asset in test_assets:
        path = get_asset_path(asset)
        if path:
            print(f"✅ {asset}: {path}")
            print(f"   Existe: {os.path.exists(path)}")
        else:
            print(f"❌ {asset}: Non trouvé")
        print()
        
except Exception as e:
    print(f"❌ Erreur: {e}")
'''
    
    with open("test_executable_assets.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("Script de test créé: test_executable_assets.py")
    print("Ce script simule le comportement de l'exécutable PyInstaller.")


if __name__ == "__main__":
    build_executable()
    test_assets_in_executable() 