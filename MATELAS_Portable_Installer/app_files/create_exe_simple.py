#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script ultra-simple pour créer un .exe Windows - Version sans problème d'encodage
Usage: python create_exe_simple.py
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    """Fonction principale simplifiée"""
    print("=" * 50)
    print("CREATION EXECUTABLE WINDOWS - MATELASAPP")
    print("=" * 50)
    
    # Étape 1: Vérifier PyInstaller
    print("1. Verification PyInstaller...")
    try:
        import PyInstaller
        print("   PyInstaller OK")
    except ImportError:
        print("   Installation PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Étape 2: Vérifier les fichiers
    print("2. Verification fichiers...")
    required = ['app_gui.py', 'backend', 'config', 'template', 'assets']
    for item in required:
        if Path(item).exists():
            print(f"   {item} OK")
        else:
            print(f"   ERREUR: {item} manquant")
            return
    
    # Étape 3: Nettoyer (optionnel)
    print("3. Nettoyage...")
    if Path('Commandes').exists():
        try:
            shutil.rmtree('Commandes')
            print("   Dossier Commandes supprime")
        except:
            print("   Dossier Commandes non supprime (pas grave)")
    
    # Étape 4: Créer l'exécutable
    print("4. Creation executable...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed", 
        "--name=MatelasApp-Windows",
        "--add-data=backend;backend",
        "--add-data=config;config",
        "--add-data=template;template", 
        "--add-data=assets;assets",
        "--add-data=matelas_config.json;.",
        "--clean",
        "--noconfirm",
        "app_gui.py"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            exe_path = Path("dist/MatelasApp-Windows.exe")
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"   SUCCESS! Fichier cree: {exe_path}")
                print(f"   Taille: {size_mb:.1f} MB")
                
                # Créer guide simple
                guide = """GUIDE WINDOWS - MatelasApp

PROBLEME RESOLU:
L'erreur de permissions a ete corrigee.

LOGS:
Les logs sont dans: %USERPROFILE%\\MatelasApp\\logs\\

UTILISATION:
Double-clic sur MatelasApp-Windows.exe
"""
                with open('dist/GUIDE_WINDOWS.txt', 'w', encoding='utf-8') as f:
                    f.write(guide)
                
                print("\n" + "="*50)
                print("EXECUTABLE PRET !")
                print("Fichier: dist/MatelasApp-Windows.exe") 
                print("Guide: dist/GUIDE_WINDOWS.txt")
                print("="*50)
                
                if os.name == 'nt':
                    input("Appuyer sur Entree pour ouvrir le dossier...")
                    subprocess.run(['explorer', 'dist'])
                
            else:
                print("   ERREUR: Fichier exe non trouve")
        else:
            print("   ERREUR PyInstaller:")
            print(result.stderr[:500])
            
    except Exception as e:
        print(f"   ERREUR: {e}")

if __name__ == "__main__":
    main()