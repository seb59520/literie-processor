#!/usr/bin/env python3
"""
Script de correction manuelle des imports pour PyInstaller
"""

import os
import shutil
import subprocess

def fix_imports_manual():
    """Corrige manuellement les imports et recompile"""
    
    print("=" * 50)
    print("CORRECTION MANUELLE DES IMPORTS")
    print("=" * 50)
    
    # 1. Vérifier que app_gui.py a été corrigé
    print("🔍 Vérification des imports dans app_gui.py...")
    
    with open('app_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "sys.path.append('backend')" in content:
        print("❌ Les imports n'ont pas été corrigés")
        print("   Exécutez d'abord: python fix_app_gui_imports.py")
        return False
    elif "hasattr(sys, '_MEIPASS')" in content:
        print("✅ Les imports ont été corrigés")
    else:
        print("⚠️ Imports non reconnus, vérification manuelle nécessaire")
    
    print()
    
    # 2. Vérifier que run_gui_fixed.py existe
    if not os.path.exists('run_gui_fixed.py'):
        print("❌ run_gui_fixed.py manquant")
        print("   Exécutez d'abord: python fix_app_gui_imports.py")
        return False
    
    print("✅ run_gui_fixed.py trouvé")
    print()
    
    # 3. Nettoyer les anciens fichiers
    print("🧹 Nettoyage des anciens fichiers...")
    
    for dir_to_clean in ["build", "dist"]:
        if os.path.exists(dir_to_clean):
            shutil.rmtree(dir_to_clean)
            print(f"   Supprimé: {dir_to_clean}")
    
    for file in os.listdir("."):
        if file.endswith(".spec") and file != "MatelasApp_Fixed.spec":
            os.remove(file)
            print(f"   Supprimé: {file}")
    
    print("✅ Nettoyage terminé")
    print()
    
    # 4. Recompiler avec la version corrigée
    print("🚀 Recompilation avec la version corrigée...")
    
    command = ["pyinstaller", "MatelasApp_Fixed.spec", "--clean"]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Recompilation réussie!")
            
            # Vérifier l'exécutable
            exe_path = "dist/MatelasApp_Fixed.exe"
            if os.path.exists(exe_path):
                size_mb = os.path.getsize(exe_path) / (1024*1024)
                print(f"✅ Exécutable créé: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                print()
                print("🎉 L'exécutable devrait maintenant fonctionner!")
                print("   Testez avec: dist/MatelasApp_Fixed.exe")
                
            else:
                print(f"❌ Exécutable non trouvé: {exe_path}")
                
        else:
            print("❌ Erreur de recompilation:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

def create_test_script():
    """Crée un script de test pour vérifier les imports"""
    
    print("🔧 Création d'un script de test...")
    
    test_script = '''#!/usr/bin/env python3
"""
Script de test pour vérifier les imports
"""

import sys
import os

print("Test des imports...")
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Current dir: {os.getcwd()}")

# Configuration du path pour PyInstaller
if hasattr(sys, '_MEIPASS'):
    print("Mode PyInstaller détecté")
    base_path = sys._MEIPASS
else:
    print("Mode développement détecté")
    base_path = os.path.dirname(os.path.abspath(__file__))

print(f"Base path: {base_path}")

# Ajouter le backend au path
backend_path = os.path.join(base_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)
    print(f"Backend path ajouté: {backend_path}")

print(f"Python path: {sys.path[:3]}...")

# Test des imports
try:
    from backend_interface import backend_interface
    print("✅ backend_interface importé")
except Exception as e:
    print(f"❌ backend_interface: {e}")

try:
    from config import config
    print("✅ config importé")
except Exception as e:
    print(f"❌ config: {e}")

try:
    from version import get_version
    print("✅ version importé")
except Exception as e:
    print(f"❌ version: {e}")

try:
    from backend.asset_utils import get_asset_path
    print("✅ asset_utils importé")
except Exception as e:
    print(f"❌ asset_utils: {e}")

print("Test terminé")
input("Appuyez sur Entrée...")
'''
    
    with open("test_imports.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Script de test créé: test_imports.py")
    print("   Lancez: python test_imports.py")

def main():
    """Fonction principale"""
    
    # Corriger et recompiler
    if fix_imports_manual():
        print()
        create_test_script()
        print()
        print("📋 Prochaines étapes:")
        print("1. Testez l'exécutable: dist/MatelasApp_Fixed.exe")
        print("2. Si ça ne marche pas, lancez: python test_imports.py")
        print("3. Si ça marche, l'exécutable est prêt!")
    else:
        print("❌ Correction échouée")

if __name__ == "__main__":
    main() 