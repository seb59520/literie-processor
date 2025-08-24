#!/usr/bin/env python3
"""
Script de diagnostic pour l'exécutable qui ne se lance pas
"""

import os
import sys
import subprocess
import tempfile
from pathlib import Path

def check_executable_exists():
    """Vérifie si l'exécutable existe"""
    print("Verification de l'executable...")
    
    exe_path = "dist/MatelasApp.exe"
    if os.path.exists(exe_path):
        size = os.path.getsize(exe_path)
        print(f"OK: Executable trouve ({size} bytes)")
        return exe_path
    else:
        print(f"ERREUR: Executable non trouve: {exe_path}")
        return None

def test_executable_launch(exe_path):
    """Teste le lancement de l'exécutable"""
    print(f"\nTest de lancement: {exe_path}")
    
    try:
        # Test avec capture d'erreur
        result = subprocess.run(
            [exe_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print(f"Sortie standard: {result.stdout[:500]}...")
        if result.stderr:
            print(f"Erreur: {result.stderr}")
            
        return result.returncode == 0
        
    except subprocess.TimeoutExpired:
        print("OK: Executable se lance (timeout normal)")
        return True
    except Exception as e:
        print(f"ERREUR lors du lancement: {e}")
        return False

def test_executable_with_console(exe_path):
    """Teste l'exécutable avec console pour voir les erreurs"""
    print(f"\nTest avec console: {exe_path}")
    
    try:
        # Créer un exécutable temporaire avec console
        temp_exe = exe_path.replace(".exe", "_debug.exe")
        
        # Copier l'exécutable
        import shutil
        shutil.copy2(exe_path, temp_exe)
        
        # Lancer avec console
        result = subprocess.run(
            [temp_exe],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        print(f"Code de retour: {result.returncode}")
        if result.stdout:
            print(f"Sortie: {result.stdout}")
        if result.stderr:
            print(f"Erreur: {result.stderr}")
            
        # Nettoyer
        if os.path.exists(temp_exe):
            os.remove(temp_exe)
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"ERREUR test console: {e}")
        return False

def check_dependencies():
    """Vérifie les dépendances manquantes"""
    print("\nVerification des dependances...")
    
    # Vérifier les DLLs système
    system_dlls = [
        "msvcp140.dll",
        "vcruntime140.dll",
        "python311.dll"
    ]
    
    import ctypes
    from ctypes import wintypes
    
    for dll in system_dlls:
        try:
            ctypes.windll.LoadLibrary(dll)
            print(f"OK: {dll}")
        except:
            print(f"MANQUANT: {dll}")
    
    # Vérifier les dossiers de données
    data_dirs = [
        "backend",
        "assets", 
        "template",
        "config",
        "Commandes"
    ]
    
    for dir_name in data_dirs:
        if os.path.exists(dir_name):
            print(f"OK: {dir_name}/")
        else:
            print(f"MANQUANT: {dir_name}/")

def check_python_imports():
    """Teste les imports Python critiques"""
    print("\nTest des imports critiques...")
    
    try:
        import PyQt6
        print("OK: PyQt6")
    except ImportError as e:
        print(f"ERREUR PyQt6: {e}")
    
    try:
        import fitz
        print("OK: PyMuPDF")
    except ImportError as e:
        print(f"ERREUR PyMuPDF: {e}")
    
    try:
        import openpyxl
        print("OK: openpyxl")
    except ImportError as e:
        print(f"ERREUR openpyxl: {e}")
    
    try:
        import httpx
        print("OK: httpx")
    except ImportError as e:
        print(f"ERREUR httpx: {e}")

def create_test_script():
    """Crée un script de test simple"""
    print("\nCreation d'un script de test...")
    
    test_script = '''#!/usr/bin/env python3
import sys
import os

print("Test de l'environnement Python...")
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")
print(f"Current directory: {os.getcwd()}")

try:
    import PyQt6
    print("OK: PyQt6 importe")
except ImportError as e:
    print(f"ERREUR PyQt6: {e}")

try:
    import fitz
    print("OK: PyMuPDF importe")
except ImportError as e:
    print(f"ERREUR PyMuPDF: {e}")

try:
    from backend_interface import backend_interface
    print("OK: backend_interface importe")
except ImportError as e:
    print(f"ERREUR backend_interface: {e}")

try:
    from config import config
    print("OK: config importe")
except ImportError as e:
    print(f"ERREUR config: {e}")

print("Test termine")
input("Appuyez sur Entree pour continuer...")
'''
    
    with open("test_environment.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("OK: Script de test cree (test_environment.py)")
    print("Lancez: python test_environment.py")

def check_file_permissions():
    """Vérifie les permissions des fichiers"""
    print("\nVerification des permissions...")
    
    exe_path = "dist/MatelasApp.exe"
    if os.path.exists(exe_path):
        # Vérifier si le fichier est exécutable
        if os.access(exe_path, os.X_OK):
            print("OK: Permissions d'execution")
        else:
            print("ERREUR: Pas de permissions d'execution")
        
        # Vérifier la taille
        size = os.path.getsize(exe_path)
        if size > 1000000:  # Plus de 1MB
            print(f"OK: Taille normale ({size} bytes)")
        else:
            print(f"ERREUR: Taille suspecte ({size} bytes)")

def main():
    """Fonction principale de diagnostic"""
    print("Diagnostic de l'executable MatelasApp")
    print("=" * 50)
    
    # Vérifications de base
    exe_path = check_executable_exists()
    if not exe_path:
        return False
    
    # Tests de lancement
    if not test_executable_launch(exe_path):
        test_executable_with_console(exe_path)
    
    # Vérifications système
    check_dependencies()
    check_python_imports()
    check_file_permissions()
    
    # Créer un script de test
    create_test_script()
    
    print("\n" + "=" * 50)
    print("DIAGNOSTIC TERMINE")
    print("=" * 50)
    print("\nSOLUTIONS RECOMMANDEES:")
    print("1. Lancez: python test_environment.py")
    print("2. Vérifiez que tous les dossiers sont présents")
    print("3. Réinstallez les dépendances: pip install -r requirements_gui.txt")
    print("4. Recréez l'exécutable avec: python setup_simple.py")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERREUR: {e}")
        sys.exit(1) 