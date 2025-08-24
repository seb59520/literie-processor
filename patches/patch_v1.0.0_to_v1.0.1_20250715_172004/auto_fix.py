#!/usr/bin/env python3
"""
Réparation automatique pour l'application Matelas
"""

import os
import sys
import subprocess
import shutil
import tempfile
from pathlib import Path

def check_python_version():
    """Vérifie la version de Python"""
    print("=== VERIFICATION VERSION PYTHON ===")
    
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ requis")
        return False
    
    print("✅ Version Python OK")
    return True

def install_missing_packages():
    """Installe les packages manquants"""
    print("\n=== INSTALLATION PACKAGES MANQUANTS ===")
    
    required_packages = [
        'PyQt6',
        'PyInstaller',
        'fastapi',
        'uvicorn',
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

def fix_encoding_issues():
    """Corrige les problèmes d'encodage"""
    print("\n=== CORRECTION ENCODAGE ===")
    
    # Vérifier et corriger les fichiers principaux
    files_to_check = [
        'run_gui.py',
        'app_gui.py',
        'backend_interface.py',
        'config.py',
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            try:
                # Lire avec détection d'encodage
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Réécrire en UTF-8
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"✅ {file_path} encodage corrigé")
            except Exception as e:
                print(f"⚠️  {file_path} erreur encodage: {e}")
    
    return True

def create_clean_spec():
    """Crée un fichier spec propre"""
    print("\n=== CREATION SPEC PROPRE ===")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['run_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('assets', 'assets'),
        ('template', 'template'),
        ('config', 'config'),
        ('Commandes', 'Commandes'),
        ('backend', 'backend'),
    ],
    hiddenimports=[
        'PyQt6.QtCore',
        'PyQt6.QtWidgets',
        'PyQt6.QtGui',
        'fastapi',
        'fastapi.middleware',
        'fastapi.middleware.cors',
        'uvicorn',
        'uvicorn.logging',
        'uvicorn.loops',
        'uvicorn.loops.auto',
        'uvicorn.protocols',
        'uvicorn.protocols.http',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets',
        'uvicorn.protocols.websockets.auto',
        'uvicorn.lifespan',
        'uvicorn.lifespan.on',
        'pandas',
        'openpyxl',
        'requests',
        'cryptography',
        'backend_interface',
        'config',
        'app_gui',
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
    name='MatelasApp_Clean',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('matelas_clean.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content)
    
    print("✅ Fichier spec propre créé")
    return True

def clean_build_directories():
    """Nettoie les répertoires de build"""
    print("\n=== NETTOYAGE REPERTOIRES BUILD ===")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"✅ {dir_name} supprimé")
            except Exception as e:
                print(f"⚠️  Erreur suppression {dir_name}: {e}")
    
    # Nettoyer les fichiers .spec anciens
    for file in os.listdir('.'):
        if file.endswith('.spec') and file != 'matelas_clean.spec':
            try:
                os.remove(file)
                print(f"✅ {file} supprimé")
            except Exception as e:
                print(f"⚠️  Erreur suppression {file}: {e}")
    
    return True

def build_clean_executable():
    """Compile un exécutable propre"""
    print("\n=== COMPILATION EXECUTABLE PROPRE ===")
    
    try:
        # Compiler avec le spec propre
        result = subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--noconfirm",
            "matelas_clean.spec"
        ], capture_output=True, text=True, timeout=600)
        
        if result.returncode == 0:
            print("✅ Exécutable propre créé")
            print("📁 Fichier: dist\\MatelasApp_Clean.exe")
            return True
        else:
            print(f"❌ Erreur compilation: {result.stderr}")
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
echo LANCEUR DE TEST - MATELAS APP
echo ========================================
echo.

echo Test de l'executable...
echo.

if exist "dist\\MatelasApp_Clean.exe" (
    echo Lancement de l'executable...
    dist\\MatelasApp_Clean.exe
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
    
    with open('test_launcher.bat', 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Lanceur de test créé")
    return True

def create_installation_package():
    """Crée un package d'installation"""
    print("\n=== CREATION PACKAGE INSTALLATION ===")
    
    if not os.path.exists('dist\\MatelasApp_Clean.exe'):
        print("❌ Exécutable non trouvé")
        return False
    
    # Créer le répertoire d'installation
    install_dir = 'MatelasApp_Installation'
    if os.path.exists(install_dir):
        shutil.rmtree(install_dir)
    
    os.makedirs(install_dir)
    
    # Copier l'exécutable
    shutil.copy2('dist\\MatelasApp_Clean.exe', install_dir)
    
    # Créer un script d'installation
    install_script = '''@echo off
chcp 65001 >nul
echo ========================================
echo INSTALLATION MATELAS APP
echo ========================================
echo.

echo Installation en cours...
echo.

if exist "MatelasApp_Clean.exe" (
    echo Lancement de l'application...
    MatelasApp_Clean.exe
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
2. Ou double-cliquez directement sur `MatelasApp_Clean.exe`

## Support

En cas de problème, vérifiez que:
- Windows 10/11 est installé
- Les droits administrateur sont accordés si nécessaire
- L'antivirus n'interfère pas avec l'exécutable

## Version

Application Matelas - Version propre
'''
    
    with open(os.path.join(install_dir, 'README.txt'), 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"✅ Package d'installation créé: {install_dir}")
    return True

def main():
    """Fonction principale"""
    print("REPARATION AUTOMATIQUE - MATELAS APP")
    print("=" * 50)
    
    steps = [
        ("Vérification Python", check_python_version),
        ("Installation packages", install_missing_packages),
        ("Correction encodage", fix_encoding_issues),
        ("Nettoyage build", clean_build_directories),
        ("Création spec propre", create_clean_spec),
        ("Compilation exécutable", build_clean_executable),
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
    print("\n" + "=" * 50)
    print("RESUME REPARATION")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for step_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} {step_name}")
        if result:
            passed += 1
    
    print(f"\nRésultat: {passed}/{total} étapes réussies")
    
    if passed == total:
        print("🎉 Réparation complète réussie !")
        print("\nFICHIERS CRÉÉS:")
        print("- dist\\MatelasApp_Clean.exe (exécutable)")
        print("- test_launcher.bat (lanceur de test)")
        print("- MatelasApp_Installation\\ (package d'installation)")
        print("\nPROCHAINES ÉTAPES:")
        print("1. Lancez test_launcher.bat pour tester")
        print("2. Ou utilisez le package d'installation")
    elif passed >= total - 2:
        print("⚠️  Réparation partiellement réussie")
        print("💡 Vérifiez les erreurs et relancez si nécessaire")
    else:
        print("❌ Réparation échouée")
        print("💡 Vérifiez les erreurs et corrigez manuellement")
    
    return passed >= total - 2

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nRéparation interrompue")
        sys.exit(1)
    except Exception as e:
        print(f"\nErreur inattendue: {e}")
        sys.exit(1) 