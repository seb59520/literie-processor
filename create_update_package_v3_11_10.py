#!/usr/bin/env python3
"""
Création du package de mise à jour version 3.11.10
Version de test pour valider le système de mise à jour automatique
"""

import os
import zipfile
import json
from datetime import datetime
import shutil

def create_update_package():
    """Créer le package de mise à jour version 3.11.10"""
    
    print("🚀 CRÉATION DU PACKAGE DE MISE À JOUR v3.11.10")
    print("=" * 50)
    
    # Informations du package
    version = "3.11.10"
    description = "Version de test pour mise à jour automatique"
    changelog = """🧪 Version de test:
- Test du système de mise à jour automatique à distance
- Validation de la télémétrie et remontée d'informations client
- Vérification de l'indicateur de mise à jour en conditions réelles
- Test de la distribution et du processus complet de déploiement

🔧 Améliorations techniques:
- Système de mise à jour: Validation complète du cycle de vie
- Interface utilisateur: Test de l'indicateur en conditions réelles
- Serveur de distribution: Vérification de la robustesse du système

✨ Cette version permet de tester:
- La détection automatique de nouvelles versions
- L'affichage correct dans l'indicateur de statut
- Le téléchargement et l'installation depuis le serveur distant
- La préservation des configurations utilisateur"""
    
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
        ("config.py", "config.py"),
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
                "files": [{"source": src, "target": tgt} for src, tgt in files_to_include],
                "test_version": True,
                "test_notes": "Cette version est créée pour tester le système de mise à jour automatique en conditions réelles"
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
        
        # Ajouter la nouvelle version au début de la liste (la plus récente en premier)
        new_version = {
            "version": version,
            "filename": filename,
            "description": description,
            "changelog": changelog.replace('\n', '\\n').replace('\r', '\\r'),
            "file_size": file_size,
            "release_date": datetime.now().isoformat(),
            "downloads": 0,
            "test_version": True
        }
        
        # Vérifier si la version existe déjà
        version_exists = False
        for i, v in enumerate(manifest["versions"]):
            if v["version"] == version:
                # Mettre à jour la version existante
                manifest["versions"][i] = new_version
                version_exists = True
                print(f"  ✅ Version {version} mise à jour dans le manifest")
                break
        
        # Si la version n'existe pas, l'ajouter au début
        if not version_exists:
            manifest["versions"].insert(0, new_version)
            print(f"  ✅ Version {version} ajoutée au manifest")
        
        # Sauvegarder le manifest
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Manifest sauvegardé: {manifest_path}")
        print(f"  📊 Versions disponibles: {len(manifest['versions'])}")
        print(f"  🎯 Version la plus récente: {manifest['versions'][0]['version']}")
        
    except Exception as e:
        print(f"  ❌ Erreur lors de la mise à jour du manifest: {e}")

def test_update_api():
    """Tester l'API de mise à jour après création du package"""
    
    print(f"\n🧪 TEST DE L'API DE MISE À JOUR")
    print("=" * 40)
    
    import requests
    
    try:
        # Test avec version 3.11.9 (devrait détecter 3.11.10 disponible)
        url = "https://edceecf7fdaf.ngrok-free.app/api/v1/check-updates?current_version=3.11.9"
        headers = {"ngrok-skip-browser-warning": "true"}
        
        print("🔍 Test avec version 3.11.9...")
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"  ✅ Statut: {response.status_code}")
            print(f"  📊 Mise à jour disponible: {data.get('available')}")
            print(f"  📋 Version actuelle: {data.get('current_version')}")
            print(f"  🆕 Dernière version: {data.get('latest_version')}")
            print(f"  📄 Description: {data.get('description')}")
            
            if data.get('available'):
                print("  🎉 SUCCÈS: La nouvelle version 3.11.10 est détectée!")
            else:
                print("  ⚠️ ATTENTION: Aucune mise à jour détectée")
        else:
            print(f"  ❌ Erreur HTTP: {response.status_code}")
            print(f"  📝 Réponse: {response.text}")
            
    except Exception as e:
        print(f"  ❌ Erreur lors du test API: {e}")

if __name__ == "__main__":
    print("🧪 CRÉATION DE LA VERSION DE TEST 3.11.10")
    print("=" * 60)
    
    # Créer le package
    package_path, size = create_update_package()
    
    if package_path:
        print(f"\n🎯 PROCHAINES ÉTAPES POUR LE TEST:")
        print("1. 📱 Déployez la version portable 3.11.9 sur votre poste client")
        print("2. 🚀 Lancez l'application sur le poste distant")
        print("3. 👀 Observez l'indicateur de mise à jour (doit devenir rouge)")
        print("4. 🖱️ Cliquez sur l'indicateur pour voir les détails")
        print("5. ⬇️ Testez le téléchargement et l'installation")
        
        # Tester l'API
        test_update_api()
        
        print(f"\n🎉 VERSION 3.11.10 PRÊTE POUR TEST!")
        print(f"📦 Package: {package_path}")
        print(f"📏 Taille: {size:,} octets")
    else:
        print("\n❌ Échec de la création du package")