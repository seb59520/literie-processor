#!/usr/bin/env python3
"""
Créer une version manuellement et l'ajouter à l'interface d'administration
"""

import sys
from pathlib import Path
import shutil

# Ajouter le backend au path
sys.path.insert(0, str(Path.cwd() / "backend"))

def create_and_publish_version():
    """Créer et publier une version dans l'admin storage"""
    print("🚀 Création et Publication Manuelle")
    print("=" * 40)
    
    try:
        from version_manager import VersionManager
        from update_server import create_update_package, UpdateServer
        from datetime import datetime
        import json
        
        # 1. Créer la version
        print("📋 Création de la version...")
        vm = VersionManager(".")
        current_version = vm.get_version_info().get('version', '1.0.0')
        print(f"Version actuelle: {current_version}")
        
        new_version = vm.update_version("patch", "Test manuel interface admin")
        print(f"✅ Nouvelle version: {new_version}")
        
        # 2. Créer le package dans un dossier temporaire
        print("📦 Création du package...")
        temp_dir = "temp_manual_package"
        package_path = create_update_package(".", new_version, temp_dir)
        print(f"✅ Package créé: {package_path}")
        
        # 3. Configurer l'admin storage
        admin_storage = Path("admin_update_storage")
        admin_storage.mkdir(exist_ok=True)
        (admin_storage / "versions").mkdir(exist_ok=True)
        (admin_storage / "metadata").mkdir(exist_ok=True)
        (admin_storage / "patches").mkdir(exist_ok=True)
        
        # 4. Déplacer le package vers l'admin storage
        package_file = Path(package_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_filename = f"matelas_v{new_version}_{timestamp}.zip"
        dest_path = admin_storage / "versions" / dest_filename
        
        shutil.move(str(package_file), str(dest_path))
        print(f"✅ Package déplacé vers: {dest_path}")
        
        # 5. Créer ou mettre à jour le manifest
        manifest_path = admin_storage / "metadata" / "manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        else:
            manifest = {"versions": [], "metadata": {"created": datetime.now().isoformat()}}
        
        # Ajouter la nouvelle version
        version_info = {
            "version": new_version,
            "filename": dest_filename,
            "size": dest_path.stat().st_size,
            "date": datetime.now().isoformat(),
            "description": "Test manuel interface admin",
            "changelog": f"Version {new_version} créée manuellement",
            "downloads": 0,
            "type": "patch"
        }
        
        manifest["versions"].insert(0, version_info)  # Plus récent en premier
        manifest["metadata"]["last_update"] = datetime.now().isoformat()
        manifest["metadata"]["total_versions"] = len(manifest["versions"])
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Manifest mis à jour: {manifest_path}")
        
        # 6. Nettoyer
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print("\n🎉 VERSION CRÉÉE ET PUBLIÉE AVEC SUCCÈS !")
        print(f"📦 Version: {new_version}")
        print(f"📁 Fichier: {dest_filename}")
        print(f"📊 Taille: {dest_path.stat().st_size:,} bytes")
        print("🌐 Visible dans l'interface admin à http://localhost:8081")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_and_publish_version()
    if success:
        print("\n✅ Succès ! Rechargez l'interface web pour voir la nouvelle version.")
    else:
        print("\n❌ Échec. Vérifiez les erreurs ci-dessus.")