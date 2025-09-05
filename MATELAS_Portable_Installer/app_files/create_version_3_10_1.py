#!/usr/bin/env python3
"""
Script pour créer la version 3.10.1 avec mise à jour automatique de version
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_version_3_10_1():
    """Crée la version 3.10.1 avec les améliorations de mise à jour de version"""
    
    print("🚀 CRÉATION DE LA VERSION 3.10.1")
    print("=" * 50)
    print("🆕 Nouvelle fonctionnalité: Mise à jour automatique du fichier version.py")
    print()
    
    version = "3.10.1"
    description = "Mise à jour automatique du numéro de version après patch"
    changelog = """Version 3.10.1 - Mise à jour automatique de version

🆕 Nouvelles fonctionnalités:
- Mise à jour automatique du fichier version.py après installation du patch
- Le numéro de version est maintenant correctement affiché après redémarrage
- Mise à jour automatique de BUILD_DATE et BUILD_NUMBER

🔧 Améliorations:
- Processus d'installation plus robuste avec logs détaillés
- Gestion des erreurs améliorée pendant la mise à jour de version
- Script de test pour valider la mise à jour de version

✅ Tests:
- Test de mise à jour de version.py
- Validation complète du processus de patch
- Vérification du redémarrage automatique"""
    
    # Répertoires
    app_dir = Path.cwd()
    storage_dir = Path("admin_update_storage")
    versions_dir = storage_dir / "versions"
    metadata_dir = storage_dir / "metadata"
    
    # Créer les répertoires si nécessaire
    versions_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    # Créer le fichier ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"matelas_v{version}_{timestamp}.zip"
    zip_path = versions_dir / zip_filename
    
    print(f"📦 Création du ZIP: {zip_filename}")
    
    # Fichiers à exclure du ZIP
    exclude_patterns = {
        '__pycache__', '.pyc', '.git', '.DS_Store', 'node_modules',
        'admin_update_storage', 'backup_*', 'temp_*', 'test_download.zip',
        '*.backup', 'updater_config.json'
    }
    
    files_added = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(app_dir):
            # Exclure certains répertoires
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            for file in files:
                # Exclure certains fichiers
                if any(pattern in file for pattern in exclude_patterns):
                    continue
                
                file_path = Path(root) / file
                arcname = file_path.relative_to(app_dir)
                
                try:
                    zipf.write(file_path, arcname)
                    files_added += 1
                    
                    if files_added <= 5:
                        print(f"  ✅ Ajouté: {arcname}")
                    elif files_added == 6:
                        print("  ... (plus de fichiers)")
                        
                except Exception as e:
                    print(f"  ⚠️ Ignoré {arcname}: {e}")
    
    print(f"📦 {files_added} fichiers ajoutés au ZIP")
    
    # Informations sur le fichier
    zip_size = zip_path.stat().st_size
    zip_date = datetime.now().isoformat()
    
    print(f"💾 Taille: {zip_size:,} bytes")
    
    # Charger le manifest existant
    manifest_file = metadata_dir / "manifest.json"
    
    if manifest_file.exists():
        with open(manifest_file, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = {
            "versions": [],
            "metadata": {},
            "statistics": {
                "total_downloads": 0,
                "storage_used": 0,
                "total_versions": 0,
                "active_versions": 0
            }
        }
    
    # Ajouter la nouvelle version
    new_version_info = {
        "version": version,
        "filename": zip_filename,
        "size": zip_size,
        "date": zip_date,
        "description": description,
        "changelog": changelog,
        "downloads": 0,
        "type": "patch"
    }
    
    manifest["versions"].append(new_version_info)
    
    # Trier les versions par ordre décroissant (plus récente en premier)
    def version_key(v):
        return tuple(map(int, v["version"].split('.')))
    
    manifest["versions"] = sorted(manifest["versions"], key=version_key, reverse=True)
    
    # Mettre à jour les métadonnées
    manifest["metadata"] = {
        "created": manifest.get("metadata", {}).get("created", zip_date),
        "last_update": zip_date,
        "total_versions": len(manifest["versions"])
    }
    
    # Mettre à jour les statistiques
    total_storage = sum(v["size"] for v in manifest["versions"])
    manifest["statistics"] = {
        "total_downloads": manifest["statistics"]["total_downloads"],
        "storage_used": total_storage,
        "total_versions": len(manifest["versions"]),
        "active_versions": len(manifest["versions"])
    }
    
    # Sauvegarder le manifest
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    
    print("✅ Manifest mis à jour")
    
    # Récapitulatif
    print()
    print("📊 RÉCAPITULATIF")
    print("-" * 30)
    print(f"🏷️ Version: {version}")
    print(f"📝 Description: {description}")
    print(f"📦 Fichier: {zip_filename}")
    print(f"💾 Taille: {zip_size:,} bytes")
    print(f"📁 Fichiers: {files_added}")
    print(f"📅 Date: {zip_date[:10]}")
    print()
    
    print("🎉 VERSION 3.10.1 CRÉÉE AVEC SUCCÈS!")
    print()
    print("🔍 Cette version inclut:")
    print("  ✅ Mise à jour automatique de version.py")
    print("  ✅ BUILD_DATE et BUILD_NUMBER mis à jour automatiquement")
    print("  ✅ Affichage correct de la version après redémarrage")
    print()
    print("📋 Pour tester:")
    print("  1. Votre client actuel affiche version 3.9.0")
    print("  2. Après mise à jour → version 3.10.1 affichée")
    print("  3. Vérifiez que le redémarrage fonctionne")
    
    return True

if __name__ == "__main__":
    success = create_version_3_10_1()
    
    if success:
        print("\n🚀 Prêt pour le test!")
        print("Le serveur de mise à jour va maintenant proposer la v3.10.1")
    else:
        print("\n❌ Échec de la création de version")
        sys.exit(1)