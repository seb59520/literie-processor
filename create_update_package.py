#!/usr/bin/env python3
"""
Créateur de package de mise à jour MATELAS
Script générique pour créer n'importe quelle version
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_update_package(version=None, description="", changelog=""):
    """Crée un package de mise à jour"""
    
    if not version:
        print("🔢 CRÉATION PACKAGE DE MISE À JOUR MATELAS")
        print("=" * 50)
        
        # Demander la version
        current_version = "3.10.3"  # Version actuelle
        print(f"📋 Version actuelle: {current_version}")
        version = input(f"➡️ Nouvelle version (ex: 3.10.4): ").strip()
        
        if not version:
            print("❌ Version requise")
            return False
            
        # Valider le format de version
        try:
            parts = version.split('.')
            if len(parts) != 3 or not all(p.isdigit() for p in parts):
                raise ValueError()
            major, minor, patch = map(int, parts)
        except:
            print("❌ Format de version invalide (ex: 3.10.4)")
            return False
        
        # Demander description et changelog
        if not description:
            description = input("📝 Description (optionnel): ").strip()
        if not changelog:
            changelog = input("📋 Changelog (optionnel): ").strip()
    
    print(f"\n📦 CRÉATION DU PACKAGE v{version}")
    print("=" * 40)
    
    # Dossiers et fichiers
    source_dir = Path.cwd()
    output_dir = Path("admin_update_storage")
    versions_dir = output_dir / "versions"
    metadata_dir = output_dir / "metadata"
    
    # Créer les dossiers si nécessaire
    versions_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    
    # Nom du fichier ZIP
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"matelas_v{version}_{timestamp}.zip"
    zip_path = versions_dir / zip_filename
    
    print(f"📁 Fichier de sortie: {zip_path}")
    
    # Fichiers à exclure du package
    exclude_patterns = {
        '__pycache__', '.pyc', '.git', '.DS_Store',
        'admin_update_storage', 'demo_update_storage', 'shared_update_storage',
        'backup_*', 'temp_*', 'logs', 'output', 'temp_uploads',
        'build', 'dist', 'dist_portable', 'backups', 'patches',
        'MATELAS_Portable_Installer', 'MATELAS_Compact_Installer',
        'online_admin_interface', 'rapport_*', 'test_*'
    }
    
    exclude_extensions = {'.log', '.pkl', '.db', '.backup', '.tmp'}
    
    files_added = 0
    files_skipped = 0
    
    print("📂 Création du package ZIP...")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
        for root, dirs, files in os.walk(source_dir):
            # Filtrer les dossiers
            dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
            
            for file in files:
                # Vérifier les patterns d'exclusion
                if any(pattern in file for pattern in exclude_patterns):
                    files_skipped += 1
                    continue
                    
                # Vérifier les extensions
                if any(file.endswith(ext) for ext in exclude_extensions):
                    files_skipped += 1
                    continue
                
                source_file = Path(root) / file
                
                # Vérifier la taille (ignorer les fichiers > 100MB)
                try:
                    if source_file.stat().st_size > 100 * 1024 * 1024:
                        print(f"   ⚠️ Fichier trop gros ignoré: {file}")
                        files_skipped += 1
                        continue
                except:
                    files_skipped += 1
                    continue
                
                # Ajouter au ZIP
                try:
                    rel_path = source_file.relative_to(source_dir)
                    zipf.write(source_file, rel_path)
                    files_added += 1
                    
                    if files_added % 100 == 0:
                        print(f"   ✅ {files_added} fichiers ajoutés...")
                        
                except Exception as e:
                    files_skipped += 1
                    continue
    
    zip_size = zip_path.stat().st_size / (1024 * 1024)
    print(f"✅ Package créé: {files_added} fichiers, {files_skipped} ignorés")
    print(f"📦 Taille: {zip_size:.1f} MB")
    
    # Mettre à jour le manifest
    update_manifest(version, zip_filename, description, changelog, zip_path.stat().st_size)
    
    print(f"\n🎉 PACKAGE DE MISE À JOUR CRÉÉ!")
    print(f"📁 Fichier: {zip_path}")
    print(f"📋 Version: {version}")
    
    # Proposer l'upload via l'interface admin
    print(f"\n💡 PROCHAINES ÉTAPES:")
    print(f"1. Le package a été automatiquement ajouté au manifest")
    print(f"2. Vos clients peuvent maintenant télécharger la v{version}")
    print(f"3. Ou uploadez via l'interface: http://localhost:8090/admin")
    
    return True

def update_manifest(version, filename, description, changelog, file_size):
    """Met à jour le manifest avec la nouvelle version"""
    manifest_path = Path("admin_update_storage/metadata/manifest.json")
    
    # Charger le manifest existant
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = {"versions": [], "statistics": {"total_downloads": 0}}
    
    # Vérifier que la version n'existe pas déjà
    existing_versions = [v["version"] for v in manifest["versions"]]
    if version in existing_versions:
        print(f"⚠️ Version {version} existe déjà dans le manifest")
        
        # Demander confirmation pour remplacer
        response = input("Voulez-vous remplacer la version existante? [o/N]: ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            return
        
        # Supprimer l'ancienne version
        manifest["versions"] = [v for v in manifest["versions"] if v["version"] != version]
    
    # Ajouter la nouvelle version
    new_version = {
        "version": version,
        "filename": filename,
        "description": description or f"Mise à jour vers la version {version}",
        "changelog": changelog or "Corrections et améliorations",
        "file_size": file_size,
        "release_date": datetime.now().isoformat(),
        "downloads": 0
    }
    
    manifest["versions"].append(new_version)
    
    # Trier les versions (plus récente en premier)
    manifest["versions"].sort(key=lambda x: tuple(map(int, x["version"].split('.'))), reverse=True)
    
    # Sauvegarder le manifest
    with open(manifest_path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Manifest mis à jour avec la version {version}")

def show_usage():
    """Affiche l'aide d'utilisation"""
    print("""
🚀 CRÉATEUR DE PACKAGE DE MISE À JOUR MATELAS

Usage:
  python3 create_update_package.py                    # Mode interactif
  python3 create_update_package.py 3.10.4            # Version spécifique
  
Exemples:
  python3 create_update_package.py 3.10.4 "Correction bugs" "- Fix upload\\n- Amélioration UI"
  
Le script va:
1. Créer un ZIP avec tous les fichiers nécessaires
2. Mettre à jour automatiquement le manifest
3. Rendre la version disponible pour vos clients

Fichiers générés dans:
  admin_update_storage/versions/matelas_v{version}_{timestamp}.zip
  admin_update_storage/metadata/manifest.json (mis à jour)
""")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
        sys.exit(0)
    
    # Paramètres en ligne de commande
    version = sys.argv[1] if len(sys.argv) > 1 else None
    description = sys.argv[2] if len(sys.argv) > 2 else ""
    changelog = sys.argv[3] if len(sys.argv) > 3 else ""
    
    success = create_update_package(version, description, changelog)
    
    if success:
        print(f"\n✅ Package créé avec succès!")
    else:
        print(f"\n❌ Erreur lors de la création")
        sys.exit(1)