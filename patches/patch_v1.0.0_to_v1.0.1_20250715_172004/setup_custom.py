#!/usr/bin/env python3
"""
Script d'installation utilisant la commande PyInstaller spécifique
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_pyinstaller_path():
    """Vérifie le chemin de PyInstaller"""
    print("=== VERIFICATION PYINSTALLER ===")
    
    pyinstaller_path = r"C:\Users\SEBASTIEN\AppData\Local\Programs\Python\Python311\Scripts\pyinstaller.exe"
    
    if os.path.exists(pyinstaller_path):
        print(f"✅ PyInstaller trouvé: {pyinstaller_path}")
        return pyinstaller_path
    else:
        print(f"❌ PyInstaller non trouvé: {pyinstaller_path}")
        return None

def install_missing_packages():
    """Installe les packages manquants"""
    print("\n=== INSTALLATION PACKAGES ===")
    
    required_packages = [
        'fastapi',
        'jinja2',
        'PyQt6',
        'pandas',
        'openpyxl',
        'requests',
        'cryptography',
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} déjà installé")
        except ImportError:
            print(f"📦 Installation de {package}...")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install", package
                ], check=True, capture_output=True, text=True)
                print(f"✅ {package} installé")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur installation {package}: {e}")
                return False
    
    return True

def clean_build_directories():
    """Nettoie les répertoires de build"""
    print("\n=== NETTOYAGE BUILD ===")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ {dir_name} supprimé")
            except Exception as e:
                print(f"⚠️  Erreur suppression {dir_name}: {e}")
    
    return True

def build_executable():
    """Compile l'exécutable avec la commande spécifique"""
    print("\n=== COMPILATION EXECUTABLE ===")
    
    pyinstaller_path = check_pyinstaller_path()
    if not pyinstaller_path:
        print("❌ PyInstaller non trouvé, utilisation de la version système")
        pyinstaller_cmd = [sys.executable, "-m", "PyInstaller"]
    else:
        pyinstaller_cmd = [pyinstaller_path]
    
    # Commande complète avec tous les imports nécessaires
    command = pyinstaller_cmd + [
        "run_gui.py",
        "--onefile",
        "--hidden-import=fastapi",
        "--hidden-import=jinja2",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets", 
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=fastapi.middleware",
        "--hidden-import=fastapi.middleware.cors",
        "--hidden-import=uvicorn",
        "--hidden-import=uvicorn.logging",
        "--hidden-import=uvicorn.loops",
        "--hidden-import=uvicorn.loops.auto",
        "--hidden-import=uvicorn.protocols",
        "--hidden-import=uvicorn.protocols.http",
        "--hidden-import=uvicorn.protocols.http.auto",
        "--hidden-import=uvicorn.protocols.websockets",
        "--hidden-import=uvicorn.protocols.websockets.auto",
        "--hidden-import=uvicorn.lifespan",
        "--hidden-import=uvicorn.lifespan.on",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=requests",
        "--hidden-import=cryptography",
        "--hidden-import=backend_interface",
        "--hidden-import=config",
        "--hidden-import=app_gui",
        "--add-data=assets;assets",
        "--add-data=template;template",
        "--add-data=config;config",
        "--add-data=Commandes;Commandes",
        "--add-data=backend;backend",
        "--console",
        "--clean"
    ]
    
    print("Commande de compilation:")
    print(" ".join(command))
    print()
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Compilation réussie !")
            if result.stdout:
                print("Sortie:", result.stdout)
            return True
        else:
            print("❌ Erreur de compilation:")
            if result.stderr:
                print("Erreur:", result.stderr)
            if result.stdout:
                print("Sortie:", result.stdout)
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout lors de la compilation")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def create_test_launcher():
    """Crée un lanceur de test"""
    print("\n=== CREATION LANCEUR DE TEST ===")
    
    launcher_content = '''@echo off
chcp 65001 >nul
echo ========================================
echo TEST EXECUTABLE MATELAS APP
echo ========================================
echo.

echo Test de l'executable...
echo.

if exist "dist\\run_gui.exe" (
    echo Lancement de l'executable...
    dist\\run_gui.exe
) else (
    echo Executable non trouve!
    echo Verifiez que la compilation s'est bien passee.
)

echo.
echo ========================================
echo TEST TERMINE
echo ========================================
pause
'''
    
    with open('test_custom.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Lanceur de test créé: test_custom.bat")
    return True

def create_installation_package():
    """Crée un package d'installation"""
    print("\n=== CREATION PACKAGE INSTALLATION ===")
    
    if not os.path.exists('dist\\run_gui.exe'):
        print("❌ Exécutable non trouvé")
        return False
    
    # Créer le répertoire d'installation
    install_dir = 'MatelasApp_Custom_Installation'
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copier l'exécutable
    shutil.copy2('dist\\run_gui.exe', install_dir)
    
    # Créer un script d'installation
    install_script = '''@echo off
chcp 65001 >nul
echo ========================================
echo INSTALLATION MATELAS APP
echo ========================================
echo.

echo Installation en cours...
echo.

if exist "run_gui.exe" (
    echo Lancement de l'application...
    run_gui.exe
) else (
    echo Erreur: Executable non trouve!
    pause
    exit /b 1
)

echo.
echo ========================================
echo INSTALLATION TERMINEE
echo ========================================
'''
    
    with open(os.path.join(install_dir, 'install.bat'), 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    # Créer un README
    readme_content = '''# MatelasApp - Installation

## Instructions d'installation

1. Double-cliquez sur `install.bat` pour lancer l'application
2. Ou double-cliquez directement sur `run_gui.exe`

## Support

En cas de problème, vérifiez que:
- Windows 10/11 est installé
- Les droits administrateur sont accordés si nécessaire
- L'antivirus n'interfère pas avec l'exécutable

## Version

Application Matelas - Version personnalisée
Compilée avec PyInstaller personnalisé
'''
    
    with open(os.path.join(install_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Package d'installation créé: {install_dir}")
    return True

def main():
    """Fonction principale"""
    print("INSTALLATION MATELAS APP - VERSION PERSONNALISEE")
    print("=" * 60)
    
    steps = [
        ("Installation packages", install_missing_packages),
        ("Nettoyage build", clean_build_directories),
        ("Compilation exécutable", build_executable),
        ("Création lanceur test", create_test_launcher),
        ("Création package", create_installation_package),
    ]
    
    results = []
    for step_name, step_func in steps:
        try:
            print(f"\n{'='*20} {step_name} {'='*20}")
            result = step_func()
            results.append((step_name, result))
        except Exception as e:
            print(f"❌ Erreur lors de {step_name}: {e}")
            results.append((step_name, False))
    
    # Résumé
    print("\n" + "=" * 60)
    print("RESUME INSTALLATION")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for step_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} {step_name}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} étapes réussies")
    
    if passed == total:
        print("🎉 Installation complète réussie !")
        print("\nFICHIERS CRÉÉS:")
        print("- dist\\run_gui.exe (exécutable)")
        print("- test_custom.bat (lanceur de test)")
        print("- MatelasApp_Custom_Installation\\ (package d'installation)")
        print("\nPROCHAINES ÉTAPES:")
        print("1. Lancez test_custom.bat pour tester")
        print("2. Ou utilisez le package d'installation")
    elif passed >= total - 1:
        print("⚠️  Installation partiellement réussie")
        print("💡 Vérifiez les erreurs et relancez si nécessaire")
    else:
        print("❌ Installation échouée")
        print("💡 Vérifiez les erreurs et corrigez manuellement")
    
    return passed >= total - 1

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nInstallation interrompue")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 