#!/usr/bin/env python3
"""
Script de compilation rapide pour Windows
Lance directement la compilation sans les checks détaillés
"""

import subprocess
import sys

def main():
    print("Compilation rapide Windows")
    print("=" * 40)
    
    # Installer PyInstaller si nécessaire
    try:
        import PyInstaller
        print("[OK] PyInstaller disponible")
    except ImportError:
        print("Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("[OK] PyInstaller installe")
    
    # Lancer la compilation complète
    print("Lancement de la compilation...")
    result = subprocess.run([sys.executable, "build_windows.py"], check=False)
    
    if result.returncode == 0:
        print("\n[OK] COMPILATION REUSSIE!")
        print("Executable cree: dist/MatelasProcessor.exe")
    else:
        print("\n[ERREUR] Erreur de compilation")
        print("Lancez 'python build_windows.py' pour plus de details")

if __name__ == "__main__":
    main()