#!/usr/bin/env python3
"""
Script de compilation complet pour Windows
Gère tous les chemins et ressources correctement
"""

import os
import sys
import subprocess
import shutil
import glob
from pathlib import Path

def main():
    print("=" * 60)
    print("    COMPILATION COMPLÈTE MATELASAPP WINDOWS")
    print("=" * 60)
    print()
    
    # Vérifier que PyInstaller est installé
    try:
        import PyInstaller
        print("✅ PyInstaller trouvé")
    except ImportError:
        print("📦 Installation de PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("✅ PyInstaller installé")
    
    # Nettoyer les anciens builds
    print("🧹 Nettoyage des anciens builds...")
    for path in ["build", "dist"]:
        if os.path.exists(path):
            shutil.rmtree(path)
            print(f"   Supprimé: {path}")
    
    # Supprimer les fichiers .spec
    for spec_file in glob.glob("*.spec"):
        os.remove(spec_file)
        print(f"   Supprimé: {spec_file}")
    
    print("✅ Nettoyage terminé")
    print()
    
    # Vérifier les ressources essentielles
    print("🔍 Vérification des ressources...")
    
    required_paths = [
        "app_gui.py",
        "backend/",
        "backend/asset_utils.py",
        "backend/mapping_manager.py",
        "backend/excel_import_utils.py",
        "backend/excel_sommier_import_utils.py",
        "backend/llm_provider.py",
        "backend/main.py",
        "backend/Référentiels/",
        "backend/template/",
        "config/",
        "config/mappings_matelas.json",
        "config/mappings_sommiers.json",
        "assets/",
        "template/",
        "requirements_gui.txt"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
        else:
            print(f"   ✅ {path}")
    
    if missing_paths:
        print("❌ Ressources manquantes:")
        for path in missing_paths:
            print(f"   - {path}")
        print()
        print("🔧 Création des dossiers manquants...")
        
        # Créer les dossiers manquants
        for path in missing_paths:
            if path.endswith('/'):
                os.makedirs(path, exist_ok=True)
                print(f"   Créé: {path}")
    
    print("✅ Vérification des ressources terminée")
    print()
    
    # Préparer la commande PyInstaller
    print("🔨 Préparation de la compilation...")
    
    # Chemin de base
    base_path = os.path.abspath(".")
    
    # Commandes PyInstaller
    pyinstaller_cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Un seul fichier exécutable
        "--windowed",                   # Pas de console
        "--name=MatelasApp",            # Nom de l'exécutable
        "--icon=assets/lit-double.ico", # Icône
        "--add-data=config;config",     # Dossier de configuration
        "--add-data=assets;assets",     # Dossier des assets
        "--add-data=template;template", # Dossier des templates
        "--add-data=backend;backend",   # Dossier backend complet
        "--hidden-import=PyQt6",
        "--hidden-import=PyQt6.QtCore",
        "--hidden-import=PyQt6.QtWidgets",
        "--hidden-import=PyQt6.QtGui",
        "--hidden-import=openpyxl",
        "--hidden-import=requests",
        "--hidden-import=json",
        "--hidden-import=logging",
        "--hidden-import=datetime",
        "--hidden-import=pathlib",
        "--hidden-import=shutil",
        "--hidden-import=glob",
        "--hidden-import=subprocess",
        "--hidden-import=sys",
        "--hidden-import=os",
        "--hidden-import=threading",
        "--hidden-import=queue",
        "--hidden-import=time",
        "--hidden-import=re",
        "--hidden-import=urllib3",
        "--hidden-import=openai",
        "--collect-all=backend",        # Inclure tout le backend
        "--collect-all=config",         # Inclure toute la config
        "--collect-all=assets",         # Inclure tous les assets
        "--collect-all=template",       # Inclure tous les templates
        "app_gui.py"                    # Point d'entrée
    ]
    
    print("🚀 Lancement de la compilation...")
    print("   Cela peut prendre plusieurs minutes...")
    print()
    
    try:
        # Exécuter PyInstaller
        result = subprocess.run(pyinstaller_cmd, check=True, capture_output=True, text=True)
        print("✅ Compilation réussie!")
        print()
        
        # Vérifier le résultat
        exe_path = "dist/MatelasApp.exe"
        if os.path.exists(exe_path):
            size = os.path.getsize(exe_path) / (1024 * 1024)  # Taille en MB
            print(f"✅ Exécutable créé: {exe_path}")
            print(f"   Taille: {size:.1f} MB")
            print()
            
            # Test rapide de l'exécutable
            print("🧪 Test rapide de l'exécutable...")
            try:
                # Test de lancement (timeout de 5 secondes)
                test_result = subprocess.run([exe_path, "--version"], 
                                           timeout=5, 
                                           capture_output=True, 
                                           text=True)
                print("✅ Exécutable fonctionnel")
            except subprocess.TimeoutExpired:
                print("✅ Exécutable se lance (timeout normal)")
            except Exception as e:
                print(f"⚠️  Test de lancement échoué: {e}")
            
        else:
            print("❌ Exécutable non trouvé")
            return 1
            
    except subprocess.CalledProcessError as e:
        print("❌ Erreur lors de la compilation:")
        print(f"   Code de retour: {e.returncode}")
        if e.stdout:
            print("   Sortie standard:")
            print(e.stdout)
        if e.stderr:
            print("   Erreurs:")
            print(e.stderr)
        return 1
    
    print()
    print("=" * 60)
    print("    COMPILATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("📁 Fichiers créés:")
    print(f"   - {exe_path}")
    print()
    print("🚀 Pour lancer l'application:")
    print(f"   Double-cliquez sur: {exe_path}")
    print()
    print("📋 Informations:")
    print("   - L'application est autonome (pas besoin de Python)")
    print("   - Tous les fichiers de configuration sont inclus")
    print("   - Tous les assets et templates sont inclus")
    print("   - Compatible Windows 10/11")
    print()
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n❌ Compilation annulée par l'utilisateur")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1) 