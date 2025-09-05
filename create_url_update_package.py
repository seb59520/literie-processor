#!/usr/bin/env python3
"""
Créateur de mise à jour "bootstrap" pour changer l'URL du serveur
Permet aux anciens clients de basculer vers le serveur Internet
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_url_update_package():
    """Créer un package de mise à jour pour changer l'URL du serveur"""
    print("🔄 CRÉATION D'UNE MISE À JOUR BOOTSTRAP - CHANGEMENT D'URL")
    print("=" * 65)
    
    # Configuration
    new_server_url = "https://edceecf7fdaf.ngrok-free.app"
    package_name = f"matelas_url_bootstrap_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    print(f"🌐 Nouvelle URL serveur: {new_server_url}")
    
    # Créer le répertoire temporaire
    temp_dir = Path("temp_url_update")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # 1. Créer une version modifiée d'auto_updater.py avec la nouvelle URL
        print("📝 Création d'auto_updater.py avec nouvelle URL...")
        
        original_auto_updater = Path("backend/auto_updater.py")
        if not original_auto_updater.exists():
            print("❌ Fichier backend/auto_updater.py non trouvé")
            return False
        
        # Lire le fichier original
        with open(original_auto_updater, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer les URLs localhost par la nouvelle URL
        updated_content = content.replace(
            'server_url="http://localhost:8091"',
            f'server_url="{new_server_url}"'
        ).replace(
            'server_url="https://edceecf7fdaf.ngrok-free.app"',
            f'server_url="{new_server_url}"'
        ).replace(
            'check_for_updates_with_telemetry("http://localhost:8091")',
            f'check_for_updates_with_telemetry("{new_server_url}")'
        ).replace(
            'def __init__(self, server_url="http://localhost:8091"):',
            f'def __init__(self, server_url="{new_server_url}"):'
        ).replace(
            'def check_for_updates_with_telemetry(server_url="http://localhost:8091")',
            f'def check_for_updates_with_telemetry(server_url="{new_server_url}")'
        ).replace(
            'def show_update_dialog_with_telemetry(server_url="http://localhost:8091")',
            f'def show_update_dialog_with_telemetry(server_url="{new_server_url}")'
        ).replace(
            'def check_for_updates(server_url="http://localhost:8091")',
            f'def check_for_updates(server_url="{new_server_url}")'
        ).replace(
            'def show_update_dialog(server_url="http://localhost:8091")',
            f'def show_update_dialog(server_url="{new_server_url}")'
        )
        
        # Créer la structure dans le temp
        backend_dir = temp_dir / "backend"
        backend_dir.mkdir(exist_ok=True)
        
        # Sauvegarder le fichier modifié
        updated_auto_updater = backend_dir / "auto_updater.py"
        with open(updated_auto_updater, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"  ✅ auto_updater.py mis à jour")
        
        # 2. Créer une version modifiée d'app_gui.py avec la nouvelle URL
        print("📝 Création d'app_gui.py avec nouvelle URL...")
        
        original_app_gui = Path("app_gui.py")
        if original_app_gui.exists():
            with open(original_app_gui, 'r', encoding='utf-8') as f:
                app_gui_content = f.read()
            
            # Remplacer l'URL dans app_gui.py
            updated_app_gui_content = app_gui_content.replace(
                'check_for_updates_with_telemetry("http://localhost:8091")',
                f'check_for_updates_with_telemetry("{new_server_url}")'
            ).replace(
                '"http://localhost:8091"',
                f'"{new_server_url}"'
            )
            
            # Sauvegarder
            updated_app_gui = temp_dir / "app_gui.py"
            with open(updated_app_gui, 'w', encoding='utf-8') as f:
                f.write(updated_app_gui_content)
            
            print(f"  ✅ app_gui.py mis à jour")
        
        # 3. Créer un script d'installation automatique
        install_script_content = '''#!/usr/bin/env python3
"""
Script d'installation automatique pour changement d'URL serveur
"""

import shutil
from pathlib import Path
import os
import json
from datetime import datetime

def main():
    print("🔄 Installation de la nouvelle URL serveur...")
    
    try:
        # Sauvegarder les anciens fichiers
        backup_dir = Path("backup_url_change")
        backup_dir.mkdir(exist_ok=True)
        
        # Sauvegarder auto_updater.py
        old_auto_updater = Path("backend/auto_updater.py")
        if old_auto_updater.exists():
            shutil.copy2(old_auto_updater, backup_dir / "auto_updater.py.bak")
            print("  📦 Sauvegarde de auto_updater.py")
        
        # Sauvegarder app_gui.py
        old_app_gui = Path("app_gui.py")
        if old_app_gui.exists():
            shutil.copy2(old_app_gui, backup_dir / "app_gui.py.bak")
            print("  📦 Sauvegarde de app_gui.py")
        
        # Installer les nouveaux fichiers
        new_auto_updater = Path("backend/auto_updater.py")
        if Path("backend/auto_updater.py").exists():
            # Le fichier est déjà dans le ZIP à la bonne place
            print("  ✅ auto_updater.py installé")
        
        new_app_gui = Path("app_gui.py") 
        if new_app_gui.exists():
            print("  ✅ app_gui.py installé")
        
        # Créer un fichier de config pour indiquer le changement
        timestamp = datetime.now().isoformat()
        config_data = {
            "url_update": {
                "old_url": "http://localhost:8091",
                "new_url": "''' + new_server_url + '''",
                "updated_at": timestamp,
                "version": "bootstrap"
            }
        }
        
        with open("server_url_config.json", 'w') as f:
            json.dump(config_data, f, indent=2)
        
        print("\\n🎉 Mise à jour de l'URL terminée!")
        print("🌐 Nouvelle URL: ''' + new_server_url + '''")
        print("📦 Sauvegardes dans: backup_url_change/")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'installation: {e}")
        return False

if __name__ == "__main__":
    main()
'''
        
        install_script = temp_dir / "install_url_update.py"
        with open(install_script, 'w', encoding='utf-8') as f:
            f.write(install_script_content)
        
        print("  ✅ Script d'installation créé")
        
        # 4. Créer un README
        readme_content = f'''# Mise à Jour Bootstrap - Changement URL Serveur

## Description
Cette mise à jour change l'URL du serveur de mise à jour de:
- Ancien: http://localhost:8091
- Nouveau: {new_server_url}

## Installation Automatique
Le fichier `install_url_update.py` sera exécuté automatiquement par le système de mise à jour.

## Fichiers Modifiés
- backend/auto_updater.py - URLs mises à jour
- app_gui.py - URLs mises à jour  
- server_url_config.json - Configuration créée

## Sauvegardes
Les anciens fichiers sont sauvés dans le dossier `backup_url_change/`

## Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
'''
        
        readme_file = temp_dir / "README_URL_UPDATE.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print("  ✅ README créé")
        
        # 5. Créer le fichier ZIP
        print(f"\\n🗜️ Création de l'archive: {package_name}")
        
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
        
        # Informations du package
        package_path = Path(package_name)
        package_size = package_path.stat().st_size
        
        print(f"\\n✅ PACKAGE BOOTSTRAP CRÉÉ!")
        print(f"📦 Nom: {package_name}")
        print(f"📏 Taille: {package_size:,} octets")
        print(f"🌐 Nouvelle URL: {new_server_url}")
        
        return package_name, package_size
        
    finally:
        # Nettoyer
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    try:
        package_name, size = create_url_update_package()
        print(f"\\n🎯 UTILISATION:")
        print("1. Uploadez ce package sur votre serveur LOCAL (port 8091)")
        print("2. Les clients v3.10.3 pourront le télécharger")
        print("3. Après installation, ils utiliseront le serveur Internet")
        print("4. Créez ensuite la vraie mise à jour v3.11.0")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")