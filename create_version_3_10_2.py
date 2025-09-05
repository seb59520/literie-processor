#!/usr/bin/env python3
"""
Script pour créer la version 3.10.2 avec correction du bug de backup
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_version_3_10_2():
    """Crée la version 3.10.2 avec correction du bug de backup"""
    
    print("🚀 CRÉATION DE LA VERSION 3.10.2")
    print("=" * 50)
    print("🐛 Correction: Bug de création des répertoires de backup")
    print()
    
    version = "3.10.2"
    description = "Correction du bug de sauvegarde des fichiers critiques"
    changelog = """Version 3.10.2 - Correction bug backup

🐛 Corrections:
- Correction du bug [Errno 2] lors de la sauvegarde des fichiers critiques
- Création automatique des répertoires parents dans le backup
- Amélioration des logs d'installation avec émojis
- Gestion robuste des chemins de fichiers

🔧 Améliorations:
- Logs plus détaillés pendant le processus de sauvegarde
- Validation de la structure des répertoires avant copie
- Messages informatifs pour chaque étape

✅ Tests:
- Test complet du processus de backup et restore
- Validation avec et sans répertoire config/
- Gestion des cas d'erreur améliorée"""
    
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
                    
                    if files_added <= 3:
                        print(f"  ✅ {arcname}")
                    elif files_added == 4:
                        print("  ... (fichiers supplémentaires)")
                        
                except Exception as e:
                    print(f"  ⚠️ Ignoré {arcname}: {e}")
    
    print(f"📦 {files_added} fichiers au total")
    
    # Informations sur le fichier
    zip_size = zip_path.stat().st_size
    zip_date = datetime.now().isoformat()
    
    print(f"💾 Taille finale: {zip_size / (1024*1024):.1f} MB")
    
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
    print()
    print("🎉 VERSION 3.10.2 CRÉÉE AVEC SUCCÈS!")
    print()
    print("🐛 Cette version corrige:")
    print("  ✅ Bug de création des répertoires de backup")
    print("  ✅ Gestion robuste des chemins de fichiers")
    print("  ✅ Messages d'erreur plus clairs")
    print()
    
    return True

if __name__ == "__main__":
    success = create_version_3_10_2()
    
    if success:
        print("🚀 Version 3.10.2 prête pour le test!")
    else:
        print("❌ Échec de la création")
        sys.exit(1)