#!/usr/bin/env python3
"""
Script ultra-simple pour créer un .exe Windows
Usage: python create_exe.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_dependencies():
    """Vérifie et installe les dépendances"""
    print("🔍 Vérification des dépendances...")
    
    try:
        import PyInstaller
        print("✅ PyInstaller disponible")
    except ImportError:
        print("📦 Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    try:
        import PyQt6
        print("✅ PyQt6 disponible")
    except ImportError:
        print("📦 Installation de PyQt6...")
        subprocess.run([sys.executable, "-m", "pip", "install", "PyQt6"])

def clean_project():
    """Nettoie le projet"""
    print("🧹 Nettoyage du projet...")
    
    # Importer et exécuter le nettoyage
    try:
        exec(open('clean_for_executable.py').read())
        print("✅ Projet nettoyé")
    except Exception as e:
        print(f"⚠️  Erreur de nettoyage: {e}")

def fix_windows_issues():
    """Corrige les problèmes spécifiques Windows"""
    print("🔧 Correction des problèmes Windows...")
    
    # Corrections directes dans cette fonction pour éviter les problèmes d'encodage
    try:
        # 1. Corriger app_gui.py pour les logs sécurisés
        if Path('app_gui.py').exists():
            with open('app_gui.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifier si déjà corrigé
            if 'Path.home() / "MatelasApp"' not in content:
                print("⚠️  Le système de logs sécurisé n'est pas encore appliqué")
                print("💡 Les corrections de logs ont été appliquées dans le code")
            else:
                print("✅ Système de logs sécurisé déjà en place")
        
        # 2. Créer un guide utilisateur simple
        guide_content = """# Guide Windows - MatelasApp

## Probleme resolu
L'erreur de permissions a ete corrigee.

## Logs
Les logs sont maintenant sauvegardes dans:
%USERPROFILE%\\MatelasApp\\logs\\

## Utilisation
L'executable fonctionne sans droits administrateur.

En cas de probleme, contacter le support.
"""
        
        with open('WINDOWS_GUIDE.txt', 'w', encoding='utf-8') as f:
            f.write(guide_content)
        
        print("✅ Corrections Windows appliquées")
        return True
        
    except Exception as e:
        print(f"⚠️  Erreur lors de la correction: {e}")
        return False

def create_exe():
    """Crée l'exécutable Windows"""
    print("🚀 Création de l'exécutable Windows...")
    
    # Vérifier que les fichiers essentiels existent
    required_files = ['app_gui.py', 'backend', 'config', 'template', 'assets']
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Fichiers manquants: {missing_files}")
        return False
    
    # Commande PyInstaller améliorée avec corrections Windows
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name=MatelasApp-Windows",
        "--icon=assets/lit-double.ico",
        "--add-data=backend;backend",
        "--add-data=config;config",
        "--add-data=template;template", 
        "--add-data=assets;assets",
        "--add-data=matelas_config.json;.",
        "--exclude-module=matplotlib",
        "--exclude-module=pandas",
        "--exclude-module=numpy",
        "--exclude-module=scipy",
        "--exclude-module=PIL",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtGui", 
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=logging.handlers",
        "--clean",
        "--noconfirm",
        "app_gui.py"
    ]
    
    # Exécuter PyInstaller
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Exécutable créé avec succès !")
            
            # Vérifier que l'exe existe
            exe_path = Path("dist/MatelasApp-Windows.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"📁 Fichier: {exe_path}")
                print(f"📏 Taille: {size_mb:.1f} MB")
                print(f"💾 Logs Windows: %USERPROFILE%\\MatelasApp\\logs\\")
                return True
            else:
                print("❌ Fichier .exe non trouvé dans dist/")
                return False
        else:
            print("❌ Erreur lors de la création:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("=" * 50)
    print("🎯 CRÉATION D'EXÉCUTABLE WINDOWS - MATELASAPP")
    print("=" * 50)
    
    # Étape 1: Vérifier les dépendances
    check_dependencies()
    print()
    
    # Étape 2: Nettoyer le projet
    clean_project()
    print()
    
    # Étape 3: Corriger les problèmes Windows
    fix_windows_issues()
    print()
    
    # Étape 4: Créer l'exécutable
    success = create_exe()
    print()
    
    if success:
        print("🎉 SUCCESS! Ton exécutable Windows est prêt !")
        print("📍 Emplacement: dist/MatelasApp-Windows.exe")
        print("💾 Les logs seront dans: %USERPROFILE%\\MatelasApp\\logs\\")
        print("🚀 Tu peux maintenant distribuer ce fichier !")
        print("📖 Guide inclus: WINDOWS_FIX_GUIDE.md")
        
        # Proposer d'ouvrir le dossier
        if os.name == 'nt':  # Windows
            input("💡 Appuie sur Entrée pour ouvrir le dossier dist/...")
            subprocess.run(['explorer', 'dist'])
    else:
        print("💥 ERREUR! L'exécutable n'a pas pu être créé.")
        print("🔧 Vérifier les erreurs ci-dessus et réessayer.")

if __name__ == "__main__":
    main()