#!/usr/bin/env python3
"""
Création du package de mise à jour version 3.11.9
Correction finale de l'indicateur de mise à jour
"""

import os
import zipfile
import json
from datetime import datetime
import shutil

def create_update_package():
    """Créer le package de mise à jour version 3.11.9"""
    
    print("🚀 CRÉATION DU PACKAGE DE MISE À JOUR v3.11.9")
    print("=" * 50)
    
    # Informations du package
    version = "3.11.9"
    description = "Correction finale de l'indicateur de mise à jour"
    changelog = """🔧 Corrections majeures:
- Résolution du problème d'affichage de l'indicateur de mise à jour
- Implémentation d'un système de récréation automatique des widgets Qt
- Correction des dialogues de mise à jour
- Amélioration de la stabilité de l'interface

✨ Améliorations:
- Auto-détection et recréation des widgets détruits
- Gestion robuste du cycle de vie des composants Qt
- Interface de mise à jour plus stable et fiable"""
    
    # Nom du fichier ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"matelas_v{version}_{timestamp}.zip"
    zip_path = f"online_admin_interface/update_storage/updates/{zip_filename}"
    
    # Créer le répertoire s'il n'existe pas
    os.makedirs("online_admin_interface/update_storage/updates", exist_ok=True)
    
    # Fichiers à inclure dans la mise à jour
    files_to_include = [
        ("app_gui.py", "app_gui.py"),
        ("version.py", "version.py"),
        ("backend/auto_updater.py", "backend/auto_updater.py"),
        ("real_time_alerts.py", "real_time_alerts.py"),
        ("backend_interface.py", "backend_interface.py"),
        ("ui_optimizations.py", "ui_optimizations.py"),
    ]
    
    print(f"📦 Création du package: {zip_filename}")
    print(f"📄 Description: {description}")
    print(f"📝 Fichiers à inclure: {len(files_to_include)} fichiers")
    
    try:
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for source_path, archive_path in files_to_include:
                if os.path.exists(source_path):
                    zipf.write(source_path, archive_path)
                    print(f"  ✅ Ajouté: {source_path} → {archive_path}")
                else:
                    print(f"  ⚠️ Fichier non trouvé: {source_path}")
            
            # Ajouter les métadonnées de mise à jour
            update_metadata = {
                "version": version,
                "description": description,
                "changelog": changelog,
                "timestamp": datetime.now().isoformat(),
                "files": [{"source": src, "target": tgt} for src, tgt in files_to_include]
            }
            
            zipf.writestr("update_metadata.json", json.dumps(update_metadata, indent=2, ensure_ascii=False))
            print(f"  ✅ Ajouté: update_metadata.json")
        
        # Obtenir la taille du fichier
        file_size = os.path.getsize(zip_path)
        
        print(f"\n✅ Package créé avec succès!")
        print(f"   📍 Emplacement: {zip_path}")
        print(f"   📏 Taille: {file_size:,} octets")
        
        # Mettre à jour le manifest
        update_manifest(zip_filename, file_size, description, changelog, version)
        
        return zip_path, file_size
        
    except Exception as e:
        print(f"❌ Erreur lors de la création du package: {e}")
        return None, 0

def update_manifest(filename, file_size, description, changelog, version):
    """Mettre à jour le manifest avec la nouvelle version"""
    
    print(f"\n🔄 Mise à jour du manifest...")
    
    manifest_path = "online_admin_interface/update_storage/metadata/manifest.json"
    
    try:
        # Charger le manifest existant
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
        
        # Vérifier si la version existe déjà
        version_exists = False
        for i, v in enumerate(manifest["versions"]):
            if v["version"] == version:
                # Mettre à jour la version existante
                manifest["versions"][i] = {
                    "version": version,
                    "filename": filename,
                    "description": description,
                    "changelog": changelog.replace('\n', '\\n').replace('\r', '\\r'),
                    "file_size": file_size,
                    "release_date": datetime.now().isoformat(),
                    "downloads": 0
                }
                version_exists = True
                print(f"  ✅ Version {version} mise à jour dans le manifest")
                break
        
        # Si la version n'existe pas, l'ajouter au début
        if not version_exists:
            new_version = {
                "version": version,
                "filename": filename,
                "description": description,
                "changelog": changelog.replace('\n', '\\n').replace('\r', '\\r'),
                "file_size": file_size,
                "release_date": datetime.now().isoformat(),
                "downloads": 0
            }
            manifest["versions"].insert(0, new_version)
            print(f"  ✅ Version {version} ajoutée au manifest")
        
        # Sauvegarder le manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Manifest sauvegardé: {manifest_path}")
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la mise à jour du manifest: {e}")

if __name__ == "__main__":
    create_update_package()