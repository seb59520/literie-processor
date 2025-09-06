#!/usr/bin/env python3
"""
Installation robuste MATELAS v3.11.12 - Version finale
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python():
    """Vérifier Python et pip"""
    print("🐍 Vérification Python...")
    
    try:
        version_info = sys.version_info
        if version_info.major >= 3 and version_info.minor >= 8:
            print(f"   ✅ Python {version_info.major}.{version_info.minor}.{version_info.micro}")
        else:
            print(f"   ❌ Python trop ancien: {version_info.major}.{version_info.minor}")
            return False
    except Exception as e:
        print(f"   ❌ Erreur Python: {e}")
        return False
    
    # Vérifier pip
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"], 
                            stdout=subprocess.DEVNULL)
        print("   ✅ pip disponible")
        return True
    except subprocess.CalledProcessError:
        print("   ❌ pip non disponible")
        return False

def install_package(package_name, description=""):
    """Installer un package avec gestion d'erreurs"""
    try:
        print(f"   📥 {package_name} {description}...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package_name, "--user", "--quiet"
        ])
        print(f"   ✅ {package_name}")
        return True
    except subprocess.CalledProcessError:
        try:
            # Essayer sans --user
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package_name, "--quiet"
            ])
            print(f"   ✅ {package_name} (global)")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   ❌ {package_name}: {e}")
            return False

def main():
    print("🚀 INSTALLATION MATELAS v3.11.12 - ROBUSTE")
    print("=" * 50)
    
    # Vérifier Python
    if not check_python():
        print("\n❌ Python non compatible")
        input("Appuyez sur Entrée...")
        return False
    
    # Créer répertoires
    print("\n📁 Création répertoires...")
    for dir_name in ["logs", "output", "temp_uploads", "data"]:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"   ✅ {dir_name}/")
    
    # Installation packages
    print("\n📦 Installation dépendances...")
    packages = [
        ("PyQt6", "Interface graphique"),
        ("requests", "HTTP"),
        ("PyMuPDF", "PDF"),
        ("openpyxl", "Excel"),
        ("paramiko", "SFTP"),
        ("cryptography", "Sécurité")
    ]
    
    failed = []
    for package, desc in packages:
        if not install_package(package, desc):
            failed.append(package)
    
    # Résultats
    print(f"\n📊 Résultats: {len(packages)-len(failed)}/{len(packages)} installés")
    
    if failed:
        print(f"❌ Échecs: {', '.join(failed)}")
        print("\n🔧 Essayez:")
        print("   • Exécuter en tant qu'Administrateur")
        print("   • pip install --upgrade pip")
        for pkg in failed:
            print(f"   • pip install {pkg}")
    else:
        print("✅ Toutes les dépendances installées!")
    
    # Test final
    print("\n🧪 Tests...")
    try:
        import PyQt6
        import config
        import version
        print("✅ Tests réussis!")
        print("\n🚀 Pour lancer:")
        print("   python app_gui.py")
        print("   python launch_simple.py  (version dépannage)")
        print("   lancer_matelas.bat")
    except ImportError as e:
        print(f"❌ Test échoué: {e}")
    
    input("\nAppuyez sur Entrée...")
    return len(failed) == 0

if __name__ == "__main__":
    main()
