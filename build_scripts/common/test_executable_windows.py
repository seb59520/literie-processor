#!/usr/bin/env python3
"""
Script de test pour l'exécutable Windows
"""

import os
import sys
import subprocess
import platform

def test_executable():
    """Teste l'exécutable Windows"""
    
    print("=" * 50)
    print("TEST EXÉCUTABLE WINDOWS")
    print("=" * 50)
    
    # Vérifier qu'on est sur Windows
    if platform.system() != "Windows":
        print("❌ Ce script est conçu pour Windows")
        return
    
    # Vérifier l'exécutable
    exe_path = "dist/MatelasApp_Fixed.exe"
    
    if not os.path.exists(exe_path):
        print(f"❌ Exécutable non trouvé: {exe_path}")
        print("Compilez d'abord avec: pyinstaller MatelasApp_Fixed.spec --clean")
        return
    
    print(f"✅ Exécutable trouvé: {exe_path}")
    size_mb = os.path.getsize(exe_path) / (1024*1024)
    print(f"   Taille: {size_mb:.1f} MB")
    print()
    
    # Test 1: Lancement direct
    print("🧪 Test 1: Lancement direct...")
    try:
        result = subprocess.run([exe_path], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print("Sortie standard:")
            print(result.stdout)
        if result.stderr:
            print("Erreurs:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("✅ Exécutable s'est lancé (arrêté après 10s)")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 2: Lancement avec cmd pour voir les erreurs
    print("🧪 Test 2: Lancement avec cmd...")
    try:
        cmd = f'cmd /c "{exe_path}" 2>&1'
        result = subprocess.run(cmd, 
                              shell=True,
                              capture_output=True, 
                              text=True, 
                              timeout=15)
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print("Sortie:")
            print(result.stdout)
        if result.stderr:
            print("Erreurs:")
            print(result.stderr)
            
    except subprocess.TimeoutExpired:
        print("✅ Exécutable s'est lancé (arrêté après 15s)")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print()
    
    # Test 3: Vérifier les dépendances
    print("🧪 Test 3: Vérification des dépendances...")
    
    # Vérifier les DLLs système
    system_dlls = [
        "msvcp140.dll",
        "vcruntime140.dll",
        "python311.dll"
    ]
    
    for dll in system_dlls:
        try:
            import ctypes
            ctypes.windll.LoadLibrary(dll)
            print(f"✅ {dll}")
        except:
            print(f"❌ {dll} manquant")
    
    print()
    
    # Test 4: Vérifier les dossiers de données
    print("🧪 Test 4: Vérification des dossiers de données...")
    
    data_dirs = [
        "backend",
        "assets", 
        "template",
        "config"
    ]
    
    for dir_name in data_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/")
        else:
            print(f"❌ {dir_name}/ manquant")
    
    print()
    
    # Test 5: Vérifier les imports Python
    print("🧪 Test 5: Vérification des imports Python...")
    
    try:
        import PyQt6
        print("✅ PyQt6")
    except ImportError as e:
        print(f"❌ PyQt6: {e}")
    
    try:
        import pandas
        print("✅ pandas")
    except ImportError as e:
        print(f"❌ pandas: {e}")
    
    try:
        import openpyxl
        print("✅ openpyxl")
    except ImportError as e:
        print(f"❌ openpyxl: {e}")
    
    print()
    
    # Test 6: Créer un script de test simple
    print("🧪 Test 6: Création d'un script de test...")
    
    test_script = '''import sys
import os

print("Test de l'environnement...")
print(f"Python: {sys.version}")
print(f"Executable: {sys.executable}")
print(f"Current dir: {os.getcwd()}")

try:
    import PyQt6
    print("PyQt6 OK")
except Exception as e:
    print(f"PyQt6 ERROR: {e}")

try:
    from backend_interface import backend_interface
    print("backend_interface OK")
except Exception as e:
    print(f"backend_interface ERROR: {e}")

try:
    from config import config
    print("config OK")
except Exception as e:
    print(f"config ERROR: {e}")

print("Test terminé")
input("Appuyez sur Entrée...")
'''
    
    with open("test_simple.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Script de test créé: test_simple.py")
    print("   Lancez: python test_simple.py")
    
    print()
    print("💡 Solutions possibles:")
    print("1. Lancez: python test_simple.py")
    print("2. Vérifiez que tous les dossiers sont présents")
    print("3. Essayez de lancer l'exécutable en tant qu'administrateur")
    print("4. Vérifiez les logs dans le dossier logs/")
    print("5. Essayez de lancer depuis le dossier dist/")

if __name__ == "__main__":
    test_executable() 