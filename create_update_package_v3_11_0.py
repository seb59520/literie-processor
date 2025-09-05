#!/usr/bin/env python3
"""
Créateur de package de mise à jour v3.11.0 avec système de télémétrie
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_update_package():
    """Créer le package de mise à jour v3.11.0"""
    print("📦 CRÉATION DU PACKAGE DE MISE À JOUR v3.11.0")
    print("=" * 60)
    
    # Nom du package
    package_name = f"matelas_v3.11.0_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    # Fichiers à inclure dans la mise à jour
    files_to_include = [
        # Fichier de version mis à jour
        "version.py",
        
        # Module auto_updater avec télémétrie
        "backend/auto_updater.py",
        
        # Scripts de serveur d'administration avec télémétrie
        "online_admin_interface/enhanced_admin_with_telemetry.py",
        
        # Templates pour l'interface d'administration
        "online_admin_interface/templates/admin_clients.html",
        
        # Scripts de test télémétrie
        "test_telemetry.py",
        "quick_check_telemetry.py",
        
        # Interface GUI mise à jour (si nécessaire)
        "app_gui.py",
        
        # Configuration et utilitaires
        "backend_interface.py",
    ]
    
    # Créer le répertoire temporaire pour le package
    temp_dir = Path("temp_update_package")
    temp_dir.mkdir(exist_ok=True)
    
    print(f"📁 Création du répertoire temporaire: {temp_dir}")
    
    try:
        # Copier les fichiers
        files_copied = 0
        for file_path in files_to_include:
            source_path = Path(file_path)
            
            if source_path.exists():
                # Créer la structure de répertoires dans le package
                dest_path = temp_dir / file_path
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Copier le fichier
                shutil.copy2(source_path, dest_path)
                files_copied += 1
                print(f"  ✅ {file_path}")
            else:
                print(f"  ⚠️ Fichier non trouvé: {file_path}")
        
        # Créer le dossier online_admin_interface/static s'il n'existe pas
        static_dir = temp_dir / "online_admin_interface" / "static"
        static_dir.mkdir(parents=True, exist_ok=True)
        print(f"  📁 Créé: online_admin_interface/static")
        
        # Ajouter un fichier README pour la mise à jour
        readme_content = f"""# Mise à jour MATELAS v3.11.0

## Nouvelles fonctionnalités
- Système de télémétrie des postes clients
- Interface d'administration avancée avec monitoring temps réel
- Collecte automatique des informations système
- Dashboard avec statistiques des connexions

## Installation
Cette mise à jour sera installée automatiquement par le système de mise à jour intégré.

## Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
## Fichiers inclus: {files_copied}
"""
        
        readme_path = temp_dir / "README_UPDATE.txt"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print(f"  📄 Créé: README_UPDATE.txt")
        
        # Créer le fichier ZIP
        print(f"\\n🗜️ Création de l'archive ZIP: {package_name}")
        
        with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Ajouter tous les fichiers du répertoire temporaire
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = Path(root) / file
                    # Chemin relatif dans le ZIP (sans le répertoire temporaire)
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
                    
        # Informations du package créé
        package_path = Path(package_name)
        package_size = package_path.stat().st_size
        
        print(f"\\n✅ PACKAGE CRÉÉ AVEC SUCCÈS!")
        print(f"📦 Nom: {package_name}")
        print(f"📏 Taille: {package_size:,} octets ({package_size/1024/1024:.2f} MB)")
        print(f"📁 Fichiers inclus: {files_copied + 1} (+ README)")
        print(f"🕒 Date de création: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return package_name, package_size
        
    finally:
        # Nettoyer le répertoire temporaire
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print(f"🧹 Nettoyage du répertoire temporaire terminé")

if __name__ == "__main__":
    try:
        package_name, size = create_update_package()
        print(f"\\n🎉 Package de mise à jour v3.11.0 prêt!")
        print(f"\\n📋 PROCHAINES ÉTAPES:")
        print(f"1. Uploadez le package via l'interface: http://localhost:8091/admin/upload")
        print(f"2. Utilisez le fichier: {package_name}")
        print(f"3. Version: 3.11.0")
        print(f"4. Testez avec un client pour vérifier l'installation")
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        raise