#!/usr/bin/env python3
"""
Script pour tester la compilation PyInstaller avec la nouvelle gestion d'assets
"""

import os
import sys
import subprocess
import shutil

def test_pyinstaller_compilation():
    """Test de compilation PyInstaller avec gestion d'assets"""
    print("=== TEST COMPILATION PYINSTALLER ===")
    
    # Nettoyer les anciens fichiers
    print("Nettoyage des anciens fichiers...")
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
    
    # Supprimer les fichiers .spec existants
    for spec_file in ["*.spec"]:
        for file in os.listdir("."):
            if file.endswith(".spec"):
                os.remove(file)
    
    print("✅ Nettoyage terminé")
    print()
    
    # Commande PyInstaller avec gestion d'assets
    command = [
        "pyinstaller",
        "run_gui.py",
        "--onefile",
        "--windowed",
        "--name", "MatelasApp_Test",
        "--paths=backend",
        "--collect-all", "PyQt6",
        "--add-data", "backend/template/*;backend/template",
        "--add-data", "backend/templates/*;backend/templates", 
        "--add-data", "backend/Référentiels/*;backend/Référentiels",
        "--add-data", "template/*;template",
        "--add-data", "config/*;config",
        "--add-data", "assets/*;assets",
        "--hidden-import=backend.asset_utils"
    ]
    
    print("Commande PyInstaller:")
    print(" ".join(command))
    print()
    
    try:
        # Exécuter PyInstaller
        print("Compilation en cours...")
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Compilation réussie!")
            
            # Vérifier que l'exécutable existe
            exe_path = "dist/MatelasApp_Test"
            if sys.platform == "win32":
                exe_path += ".exe"
            
            if os.path.exists(exe_path):
                print(f"✅ Exécutable créé: {exe_path}")
                print(f"   Taille: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
                
                # Test de l'exécutable (optionnel)
                print("\nTest de l'exécutable (5 secondes)...")
                try:
                    test_process = subprocess.Popen([exe_path], 
                                                  stdout=subprocess.PIPE, 
                                                  stderr=subprocess.PIPE)
                    test_process.wait(timeout=5)
                    print("✅ Exécutable s'est lancé sans erreur")
                except subprocess.TimeoutExpired:
                    test_process.terminate()
                    print("✅ Exécutable s'est lancé (arrêté après 5s)")
                except Exception as e:
                    print(f"⚠️ Erreur lors du test: {e}")
            else:
                print(f"❌ Exécutable non trouvé: {exe_path}")
        else:
            print("❌ Erreur de compilation:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la compilation")
    except FileNotFoundError:
        print("❌ PyInstaller non trouvé. Installez-le avec: pip install pyinstaller")
    except Exception as e:
        print(f"❌ Erreur: {e}")


def test_asset_integration():
    """Test de l'intégration des assets dans l'exécutable"""
    print("\n=== TEST INTEGRATION ASSETS ===")
    
    # Créer un script de test simple
    test_script = '''#!/usr/bin/env python3
import sys
import os

# Simuler le mode PyInstaller
if len(sys.argv) > 1 and sys.argv[1] == "--pyinstaller":
    # Simuler sys._MEIPASS
    sys._MEIPASS = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path
sys.path.append('backend')

try:
    from backend.asset_utils import get_asset_path, is_pyinstaller_mode
    
    print(f"Mode PyInstaller: {is_pyinstaller_mode()}")
    
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
    
    with open("test_asset_integration.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("Script de test créé: test_asset_integration.py")
    print("Test en mode développement:")
    
    # Test en mode développement
    result = subprocess.run([sys.executable, "test_asset_integration.py"], 
                          capture_output=True, text=True)
    print(result.stdout)
    
    print("Test en mode PyInstaller simulé:")
    # Test en mode PyInstaller simulé
    result = subprocess.run([sys.executable, "test_asset_integration.py", "--pyinstaller"], 
                          capture_output=True, text=True)
    print(result.stdout)


if __name__ == "__main__":
    test_asset_integration()
    
    # Décommenter pour tester la compilation complète
    # test_pyinstaller_compilation() 