#!/usr/bin/env python3
"""
Créer directement une version 3.10.0 pour les clients en version 3.9.0
"""

import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Ajouter le backend au path
sys.path.insert(0, str(Path.cwd() / "backend"))

def create_version_3_10_0():
    """Créer la version 3.10.0 manuellement"""
    print("🚀 Création Version 3.10.0 pour Client v3.9.0")
    print("=" * 50)
    
    try:
        from update_server import create_update_package
        
        # 1. Mettre à jour VERSION.json directement
        print("📋 Mise à jour de VERSION.json vers 3.10.0...")
        version_file = Path("VERSION.json")
        
        if version_file.exists():
            with open(version_file, 'r', encoding='utf-8') as f:
                version_data = json.load(f)
        else:
            version_data = {"files": {}, "dependencies": {}}
        
        # Mise à jour vers 3.10.0
        version_data.update({
            "version": "3.10.0",
            "build": "13", 
            "date": datetime.now().isoformat(),
            "hash": "new_3_10_0_version_for_client_update"
        })
        
        with open(version_file, 'w', encoding='utf-8') as f:
            json.dump(version_data, f, indent=2, ensure_ascii=False)
        
        print("✅ VERSION.json mis à jour: 3.10.0")
        
        # 2. Créer le package
        print("📦 Création du package...")
        temp_dir = "temp_v3_10_0"
        package_path = create_update_package(".", "3.10.0", temp_dir)
        print(f"✅ Package créé: {package_path}")
        
        # 3. Configurer l'admin storage
        admin_storage = Path("admin_update_storage")
        admin_storage.mkdir(exist_ok=True)
        (admin_storage / "versions").mkdir(exist_ok=True)
        (admin_storage / "metadata").mkdir(exist_ok=True)
        
        # 4. Déplacer le package
        package_file = Path(package_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_filename = f"matelas_v3.10.0_{timestamp}.zip"
        dest_path = admin_storage / "versions" / dest_filename
        
        shutil.move(str(package_file), str(dest_path))
        print(f"✅ Package déplacé: {dest_path}")
        
        # 5. Mettre à jour le manifest
        manifest_path = admin_storage / "metadata" / "manifest.json"
        
        if manifest_path.exists():
            with open(manifest_path, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        else:
            manifest = {"versions": [], "metadata": {}, "statistics": {}}
        
        # Nouvelle version en premier
        new_version = {
            "version": "3.10.0",
            "filename": dest_filename,
            "size": dest_path.stat().st_size,
            "date": datetime.now().isoformat(),
            "description": "Mise à jour pour clients v3.9.0",
            "changelog": "Version 3.10.0 - Compatible avec clients existants",
            "downloads": 0,
            "type": "minor"
        }
        
        manifest["versions"].insert(0, new_version)
        manifest["metadata"]["last_update"] = datetime.now().isoformat() 
        manifest["metadata"]["total_versions"] = len(manifest["versions"])
        
        # Mettre à jour les statistiques
        total_storage = sum(v["size"] for v in manifest["versions"])
        manifest["statistics"] = {
            "total_downloads": sum(v["downloads"] for v in manifest["versions"]),
            "storage_used": total_storage,
            "total_versions": len(manifest["versions"]),
            "active_versions": len(manifest["versions"])
        }
        
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Manifest mis à jour")
        
        # 6. Nettoyer
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        print("\n🎉 VERSION 3.10.0 CRÉÉE AVEC SUCCÈS !")
        print(f"📦 Taille: {dest_path.stat().st_size:,} bytes")
        print("🔄 Votre client v3.9.0 pourra maintenant détecter cette mise à jour")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = create_version_3_10_0()
    if success:
        print("\n✅ Succès ! Redémarrez l'interface admin et testez votre client.")
    else:
        print("\n❌ Échec. Vérifiez les erreurs ci-dessus.")