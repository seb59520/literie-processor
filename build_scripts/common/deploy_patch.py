#!/usr/bin/env python3
"""
Script de déploiement automatique de patches
"""

import os
import sys
import json
import shutil
import zipfile
import argparse
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from version_manager import version_manager

class PatchDeployer:
    """Gestionnaire de déploiement de patches"""
    
    def __init__(self):
        self.patches_dir = Path("patches")
        self.dist_dir = Path("dist")
        self.patches_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
    
    def create_patch_package(self, target_version: str, description: str = "", 
                           include_instructions: bool = True) -> str:
        """Crée un package de patch complet pour distribution"""
        
        print(f"🔧 Création du patch pour la version {target_version}...")
        
        # 1. Mettre à jour la version si nécessaire
        current_version = version_manager.get_version_info()["version"]
        if current_version == target_version:
            print("⚠️  La version actuelle correspond à la version cible")
            print("   Mise à jour automatique de la version...")
            version_manager.update_version("patch", description)
        
        # 2. Créer le patch
        patch_path = version_manager.create_patch(target_version, description)
        
        # 3. Créer le package de distribution
        package_name = f"matelas_patch_v{target_version}_to_v{version_manager.get_version_info()['version']}"
        package_path = self.dist_dir / f"{package_name}.zip"
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter le patch
            zipf.write(patch_path, Path(patch_path).name)
            
            # Ajouter les instructions
            if include_instructions:
                instructions = self._create_instructions(target_version, version_manager.get_version_info()['version'])
                zipf.writestr("INSTRUCTIONS_MAJ.txt", instructions)
            
            # Ajouter le gestionnaire de mises à jour
            if Path("update_manager_gui.py").exists():
                zipf.write("update_manager_gui.py", "update_manager_gui.py")
            
            # Ajouter le gestionnaire de version
            if Path("version_manager.py").exists():
                zipf.write("version_manager.py", "version_manager.py")
            
            # Ajouter les métadonnées
            metadata = {
                "from_version": target_version,
                "to_version": version_manager.get_version_info()['version'],
                "date": datetime.now().isoformat(),
                "description": description,
                "files_included": [
                    Path(patch_path).name,
                    "INSTRUCTIONS_MAJ.txt",
                    "update_manager_gui.py",
                    "version_manager.py"
                ]
            }
            zipf.writestr("patch_metadata.json", json.dumps(metadata, indent=2, ensure_ascii=False))
        
        print(f"✅ Package créé: {package_path}")
        return str(package_path)
    
    def _create_instructions(self, from_version: str, to_version: str) -> str:
        """Crée les instructions de mise à jour"""
        instructions = f"""
INSTRUCTIONS DE MISE À JOUR - MATELAS APP
=========================================

Version: {from_version} → {to_version}
Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}

ÉTAPES D'INSTALLATION:
=====================

1. FERMEZ l'application Matelas si elle est ouverte

2. PLACEZ ce fichier ZIP dans le dossier de l'application Matelas
   (même dossier que app_gui.py)

3. EXTRACTEZ le contenu du ZIP dans ce dossier

4. LANCEZ le gestionnaire de mises à jour:
   python update_manager_gui.py

5. Dans l'interface:
   - Allez dans l'onglet "Patches"
   - Sélectionnez le patch dans la liste
   - Cliquez sur "Appliquer Patch"

6. RELANCEZ l'application Matelas normalement

EN CAS DE PROBLÈME:
==================

- Vérifiez que vous avez les droits d'écriture dans le dossier
- Assurez-vous que Python est installé
- Contactez le support technique si nécessaire

FICHIERS INCLUS:
===============

- Patch de mise à jour
- Gestionnaire de mises à jour
- Instructions détaillées
- Métadonnées du patch

VERSION PRÉCÉDENTE: {from_version}
NOUVELLE VERSION: {to_version}

© Matelas App - Support technique disponible
        """
        return instructions.strip()
    
    def create_full_package(self, version: str, description: str = "") -> str:
        """Crée un package complet de l'application"""
        print(f"📦 Création du package complet version {version}...")
        
        # Mettre à jour la version
        version_manager.update_version("major" if version != version_manager.get_version_info()["version"] else "patch", description)
        
        package_name = f"matelas_app_v{version_manager.get_version_info()['version']}_complete"
        package_path = self.dist_dir / f"{package_name}.zip"
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Inclure tous les fichiers de l'application
            include_patterns = [
                "*.py",
                "*.json",
                "*.md",
                "*.txt",
                "*.bat",
                "*.ico",
                "*.png",
                "backend/*",
                "config/*",
                "assets/*",
                "template/*",
                "requirements_gui.txt"
            ]
            
            exclude_patterns = [
                "__pycache__",
                "*.pyc",
                ".git",
                "logs",
                "output",
                "backups",
                "patches",
                "dist",
                "build",
                ".DS_Store"
            ]
            
            for pattern in include_patterns:
                for file_path in Path(".").rglob(pattern):
                    if file_path.is_file():
                        # Vérifier les exclusions
                        should_exclude = False
                        for exclude in exclude_patterns:
                            if exclude in str(file_path):
                                should_exclude = True
                                break
                        
                        if not should_exclude:
                            zipf.write(file_path, file_path)
            
            # Ajouter les instructions d'installation
            install_instructions = self._create_install_instructions()
            zipf.writestr("INSTRUCTIONS_INSTALLATION.txt", install_instructions)
            
            # Ajouter les métadonnées
            metadata = {
                "version": version_manager.get_version_info()['version'],
                "build": version_manager.get_version_info()['build'],
                "date": datetime.now().isoformat(),
                "description": description,
                "type": "complete_package"
            }
            zipf.writestr("package_metadata.json", json.dumps(metadata, indent=2, ensure_ascii=False))
        
        print(f"✅ Package complet créé: {package_path}")
        return str(package_path)
    
    def _create_install_instructions(self) -> str:
        """Crée les instructions d'installation complète"""
        instructions = f"""
INSTRUCTIONS D'INSTALLATION COMPLÈTE - MATELAS APP
==================================================

Version: {version_manager.get_version_info()['version']}
Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}

PRÉREQUIS:
==========

- Python 3.8 ou supérieur
- Windows 10/11 ou macOS ou Linux
- Connexion Internet (pour les dépendances)

ÉTAPES D'INSTALLATION:
======================

1. EXTRACTEZ ce fichier ZIP dans un dossier de votre choix

2. OUVREZ un terminal/invite de commande dans ce dossier

3. INSTALLEZ les dépendances:
   pip install -r requirements_gui.txt

4. LANCEZ l'application:
   python app_gui.py

   OU utilisez le script de lancement:
   python launch.py

CONFIGURATION INITIALE:
======================

1. À la première utilisation, configurez vos clés API
2. Testez la connexion aux services LLM
3. Configurez le répertoire de sortie Excel

FICHIERS IMPORTANTS:
===================

- app_gui.py : Interface principale
- launch.py : Script de lancement
- requirements_gui.txt : Dépendances Python
- config/ : Configuration de l'application
- backend/ : Modules de traitement

SUPPORT:
========

En cas de problème, consultez:
- Les fichiers README_*.md
- Les logs dans le dossier logs/
- Le support technique

© Matelas App - Version {version_manager.get_version_info()['version']}
        """
        return instructions.strip()
    
    def list_packages(self) -> List[str]:
        """Liste tous les packages disponibles"""
        packages = []
        for package_file in self.dist_dir.glob("*.zip"):
            packages.append(str(package_file))
        return sorted(packages, reverse=True)
    
    def clean_old_packages(self, keep_count: int = 5):
        """Nettoie les anciens packages en gardant les plus récents"""
        packages = self.list_packages()
        if len(packages) > keep_count:
            for package in packages[keep_count:]:
                try:
                    os.remove(package)
                    print(f"🗑️  Supprimé: {Path(package).name}")
                except Exception as e:
                    print(f"❌ Erreur suppression {package}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Déploiement de patches Matelas App")
    parser.add_argument("action", choices=["patch", "full", "list", "clean"], 
                       help="Action à effectuer")
    parser.add_argument("--target-version", "-t", default="1.0.0",
                       help="Version cible pour le patch")
    parser.add_argument("--description", "-d", default="",
                       help="Description des modifications")
    parser.add_argument("--keep", "-k", type=int, default=5,
                       help="Nombre de packages à conserver (pour clean)")
    
    args = parser.parse_args()
    
    deployer = PatchDeployer()
    
    if args.action == "patch":
        package_path = deployer.create_patch_package(args.target_version, args.description)
        print(f"\n📤 Package prêt pour envoi: {package_path}")
        
    elif args.action == "full":
        package_path = deployer.create_full_package(args.target_version, args.description)
        print(f"\n📦 Package complet créé: {package_path}")
        
    elif args.action == "list":
        packages = deployer.list_packages()
        if packages:
            print("📋 Packages disponibles:")
            for package in packages:
                print(f"  - {Path(package).name}")
        else:
            print("📋 Aucun package disponible")
            
    elif args.action == "clean":
        deployer.clean_old_packages(args.keep)
        print(f"🧹 Nettoyage terminé (conservé {args.keep} packages)")

if __name__ == "__main__":
    main() 