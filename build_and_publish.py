#!/usr/bin/env python3
"""
Script de build et publication automatique pour l'application MATELAS_FINAL
Compile l'EXE et le publie via le système de mise à jour
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Ajouter le backend au path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from version_manager import VersionManager
import requests

class BuildAndPublishSystem:
    """Système de build et publication automatique"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.build_dir = self.project_root / "dist"
        self.version_manager = VersionManager(".")
        self.admin_server_url = "http://localhost:8081"
        
    def build_executable(self):
        """Compile l'exécutable avec PyInstaller"""
        print("🔨 Compilation de l'exécutable...")
        
        # Nettoyer les anciens builds
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        # Commande PyInstaller (syntaxe adaptée selon l'OS)
        import platform
        separator = ";" if platform.system() == "Windows" else ":"
        
        build_command = [
            "pyinstaller",
            "--onefile",                                    # Un seul .exe
            "--windowed",                                   # Sans console (GUI)
            "--icon=matelas_icon.ico",                      # Icône
            "--name=MatelasProcessor",                      # Nom de l'exe
            f"--add-data=backend{separator}backend",        # Inclure backend
            f"--add-data=config{separator}config",          # Inclure config
            f"--add-data=assets{separator}assets",          # Inclure assets
            f"--add-data=template{separator}template",      # Inclure templates
            "--hidden-import=PyQt6",
            "--hidden-import=openpyxl",
            "--hidden-import=pymupdf",
            "--hidden-import=httpx",                        # Pour les mises à jour
            "app_gui.py"                                    # Script principal
        ]
        
        print(f"📋 Commande: {' '.join(build_command)}")
        
        try:
            result = subprocess.run(build_command, check=True, capture_output=True, text=True)
            print("✅ Compilation réussie !")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur de compilation: {e}")
            print(f"Sortie d'erreur: {e.stderr}")
            return False
    
    def create_update_package(self, version: str, description: str):
        """Crée le package de mise à jour avec l'EXE"""
        print(f"📦 Création du package de mise à jour v{version}...")
        
        # Vérifier que l'EXE existe
        exe_file = self.build_dir / "MatelasProcessor.exe"
        if not exe_file.exists():
            print(f"❌ EXE non trouvé: {exe_file}")
            return None
        
        # Créer le dossier de release
        release_dir = self.project_root / "releases"
        release_dir.mkdir(exist_ok=True)
        
        # Nom du package
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = f"MatelasProcessor_v{version}_{timestamp}.zip"
        package_path = release_dir / package_name
        
        # Créer le ZIP avec l'EXE et les métadonnées
        import zipfile
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter l'EXE
            zipf.write(exe_file, "MatelasProcessor.exe")
            print(f"  + MatelasProcessor.exe ({exe_file.stat().st_size:,} bytes)")
            
            # Ajouter les métadonnées d'installation
            install_metadata = {
                "version": version,
                "created_date": datetime.now().isoformat(),
                "package_type": "executable_update",
                "executable_name": "MatelasProcessor.exe",
                "requires_restart": True,
                "backup_current": True,
                "install_instructions": [
                    "Fermer l'application courante",
                    "Sauvegarder l'ancien exécutable", 
                    "Extraire le nouveau MatelasProcessor.exe",
                    "Remplacer l'ancien fichier",
                    "Redémarrer l'application"
                ],
                "description": description
            }
            
            import json
            zipf.writestr("update_metadata.json", json.dumps(install_metadata, indent=2))
            
            # Ajouter un script d'installation (optionnel)
            install_script = '''@echo off
echo Mise a jour de MATELAS Processor...
echo.

REM Sauvegarder l'ancien exe
if exist "MatelasProcessor.exe" (
    echo Sauvegarde de l'ancienne version...
    copy "MatelasProcessor.exe" "MatelasProcessor_backup.exe"
)

REM Le nouveau exe sera extrait automatiquement par le systeme de MAJ
echo Installation terminee !
echo Redemarrage de l'application...

REM Redemarrer l'application
start MatelasProcessor.exe
exit
'''
            zipf.writestr("install.bat", install_script)
        
        file_size = package_path.stat().st_size
        print(f"✅ Package créé: {package_path} ({file_size:,} bytes)")
        
        return {
            "path": str(package_path),
            "filename": package_name,
            "size": file_size,
            "version": version
        }
    
    def publish_to_admin_server(self, package_info: dict, description: str, changelog: str = ""):
        """Publie le package via l'interface d'administration"""
        print(f"📤 Publication vers le serveur admin...")
        
        try:
            upload_url = f"{self.admin_server_url}/admin/upload"
            
            files = {
                'file': open(package_info["path"], 'rb')
            }
            
            data = {
                'version': package_info["version"],
                'description': description,
                'changelog': changelog or f"Version {package_info['version']} - Exécutable mis à jour"
            }
            
            print(f"🌐 Upload vers: {upload_url}")
            response = requests.post(upload_url, files=files, data=data, timeout=300)
            
            files['file'].close()
            
            if response.status_code == 200:
                print("✅ Publication réussie !")
                print(f"🎉 Version {package_info['version']} disponible pour les clients")
                return True
            else:
                print(f"❌ Erreur de publication: {response.status_code}")
                print(f"Réponse: {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur de publication: {e}")
            return False
    
    def full_build_and_publish(self, version_type: str = "patch", description: str = ""):
        """Processus complet: build + publish"""
        print("🚀 PROCESSUS COMPLET DE BUILD ET PUBLICATION")
        print("=" * 60)
        
        # 1. Incrémenter la version
        print("📊 Mise à jour de la version...")
        new_version = self.version_manager.update_version(version_type, description)
        print(f"🔖 Nouvelle version: {new_version}")
        
        # 2. Compiler l'exécutable
        if not self.build_executable():
            print("❌ Échec de la compilation")
            return False
        
        # 3. Créer le package de mise à jour
        package_info = self.create_update_package(new_version, description)
        if not package_info:
            print("❌ Échec de la création du package")
            return False
        
        # 4. Publier via l'interface admin
        changelog = f"""🎯 Version {new_version}

📝 Description: {description}

🔧 Modifications:
- Exécutable mis à jour avec les dernières fonctionnalités
- Corrections de bugs et améliorations
- Système de mise à jour automatique intégré

💾 Taille: {package_info['size']:,} bytes
📅 Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """
        
        if self.publish_to_admin_server(package_info, description, changelog):
            print("\n🎊 SUCCÈS COMPLET !")
            print(f"✅ Version {new_version} compilée et publiée")
            print(f"📦 EXE disponible pour téléchargement")
            print(f"🔄 Les clients recevront automatiquement la mise à jour")
            print(f"🌐 Interface admin: {self.admin_server_url}")
            return True
        else:
            print("\n⚠️ Build réussi mais publication échouée")
            print(f"📦 Package disponible localement: {package_info['path']}")
            print("💡 Vous pouvez l'uploader manuellement via l'interface admin")
            return False

def main():
    """Interface en ligne de commande"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Build et publication automatique")
    parser.add_argument("--type", choices=["patch", "minor", "major"], default="patch",
                       help="Type de version (patch, minor, major)")
    parser.add_argument("--description", required=True,
                       help="Description de la version")
    parser.add_argument("--build-only", action="store_true",
                       help="Seulement compiler (pas de publication)")
    
    args = parser.parse_args()
    
    builder = BuildAndPublishSystem()
    
    if args.build_only:
        print("🔨 Mode build seulement")
        success = builder.build_executable()
    else:
        print("🚀 Mode build + publication")
        success = builder.full_build_and_publish(args.type, args.description)
    
    if success:
        print("\n🎉 Processus terminé avec succès !")
    else:
        print("\n❌ Erreur lors du processus")
        sys.exit(1)

if __name__ == "__main__":
    main()