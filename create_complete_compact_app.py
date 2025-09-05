#!/usr/bin/env python3
"""
Créateur d'application MATELAS complète et compacte
Pour nouvelle installation avec serveur Internet pré-configuré
"""

import os
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_complete_compact_app():
    """Créer une application complète compacte avec serveur Internet"""
    print("📦 CRÉATION APPLICATION MATELAS COMPLÈTE COMPACTE")
    print("=" * 60)
    
    # Configuration
    new_server_url = "https://edceecf7fdaf.ngrok-free.app"
    app_name = f"matelas_complete_v3_11_0_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    print(f"🌐 URL serveur pré-configurée: {new_server_url}")
    print(f"📁 Archive: {app_name}")
    
    # Créer le répertoire temporaire
    temp_dir = Path("temp_complete_app")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Fichiers essentiels à inclure
        essential_files = [
            # Application principale
            "app_gui.py",
            "backend_interface.py", 
            "version.py",
            
            # Configuration
            "config.py",
            "matelas_config.json.template",
            
            # Backend essentiel
            "backend/main.py",
            "backend/auto_updater.py",
            "backend/llm_provider.py",
            "backend/llm_cache.py",
            
            # Utilitaires backend critiques
            "backend/excel_import_utils.py",
            "backend/matelas_utils.py",
            "backend/sommier_utils.py",
            "backend/client_utils.py",
            "backend/mapping_manager.py",
            "backend/secure_storage.py",
            "backend/advanced_logging.py",
            "backend/retry_utils.py",
            "backend/file_validation.py",
            "backend/timeout_manager.py",
            
            # Requirements
            "requirements.txt",
            "requirements_gui.txt",
        ]
        
        # Dossiers critiques
        essential_dirs = [
            "config/",
            "backend/Référentiels/",
            "template/",
            "assets/",
        ]
        
        print("📋 Copie des fichiers essentiels...")
        files_copied = 0
        
        # Copier les fichiers essentiels
        for file_path in essential_files:
            source = Path(file_path)
            if source.exists():
                dest = temp_dir / file_path
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, dest)
                files_copied += 1
                print(f"  ✅ {file_path}")
            else:
                print(f"  ⚠️ {file_path} - non trouvé")
        
        # Copier les dossiers critiques
        for dir_path in essential_dirs:
            source_dir = Path(dir_path)
            if source_dir.exists():
                dest_dir = temp_dir / dir_path
                shutil.copytree(source_dir, dest_dir, dirs_exist_ok=True)
                print(f"  📁 {dir_path} - dossier copié")
        
        # Modifier auto_updater.py avec la nouvelle URL
        print("🔧 Configuration de l'URL serveur...")
        auto_updater_path = temp_dir / "backend/auto_updater.py"
        if auto_updater_path.exists():
            with open(auto_updater_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Remplacer toutes les URLs
            updated_content = content.replace(
                'server_url="http://localhost:8091"',
                f'server_url="{new_server_url}"'
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
            
            with open(auto_updater_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("  ✅ auto_updater.py configuré")
        
        # Modifier app_gui.py avec la nouvelle URL
        app_gui_path = temp_dir / "app_gui.py"
        if app_gui_path.exists():
            with open(app_gui_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            updated_content = content.replace(
                'check_for_updates_with_telemetry("http://localhost:8091")',
                f'check_for_updates_with_telemetry("{new_server_url}")'
            ).replace(
                '"http://localhost:8091"',
                f'"{new_server_url}"'
            )
            
            with open(app_gui_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
            print("  ✅ app_gui.py configuré")
        
        # Créer un script de première installation
        install_script = f'''#!/usr/bin/env python3
"""
Script de première installation MATELAS v3.11.0
Avec serveur de mise à jour Internet pré-configuré
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("🚀 INSTALLATION MATELAS v3.11.0")
    print("=" * 40)
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        return False
    
    print(f"✅ Python {{sys.version_info.major}}.{{sys.version_info.minor}} détecté")
    
    # Installer les dépendances
    print("📦 Installation des dépendances...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dépendances backend installées")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements_gui.txt"], check=True)  
        print("✅ Dépendances GUI installées")
    except subprocess.CalledProcessError:
        print("⚠️ Erreur installation dépendances - continuez manuellement")
    
    # Créer la configuration
    config_template = Path("matelas_config.json.template")
    config_file = Path("matelas_config.json")
    
    if config_template.exists() and not config_file.exists():
        import shutil
        shutil.copy2(config_template, config_file)
        print("✅ Configuration par défaut créée")
    
    # Créer les dossiers nécessaires
    folders_to_create = ["logs", "exports", "temp"]
    for folder in folders_to_create:
        Path(folder).mkdir(exist_ok=True)
    print("✅ Dossiers créés")
    
    print("\\n🎉 INSTALLATION TERMINÉE!")
    print(f"🌐 Serveur de mise à jour: {new_server_url}")
    print("\\n🚀 Pour démarrer l'application:")
    print("python3 app_gui.py")
    
    return True

if __name__ == "__main__":
    main()
'''
        
        install_path = temp_dir / "install.py"
        with open(install_path, 'w', encoding='utf-8') as f:
            f.write(install_script)
        
        # Créer un README complet
        readme_content = f'''# MATELAS Processor v3.11.0 - Application Complète

## 📋 Description
Application complète de traitement des devis PDF MATELAS avec système de mise à jour automatique.

## 🌐 Configuration
- Serveur de mise à jour pré-configuré: {new_server_url}
- Télémétrie activée pour le suivi des postes
- Système d'alertes intégré dans la barre de statut

## 🚀 Installation Rapide
```bash
python3 install.py
python3 app_gui.py
```

## 📦 Installation Manuelle
```bash
pip install -r requirements.txt
pip install -r requirements_gui.txt
python3 app_gui.py
```

## ⚙️ Configuration
1. Copiez matelas_config.json.template vers matelas_config.json
2. Configurez vos clés API dans l'interface
3. L'application est prête à utiliser

## 🔄 Mises à Jour
- Automatiques via l'indicateur dans la barre de statut
- Vérification toutes les 5 minutes
- Télémétrie envoyée automatiquement

## 📊 Fonctionnalités v3.11.0
- Système de télémétrie des postes clients
- Interface d'administration avec monitoring temps réel
- Indicateur de mise à jour intelligent
- Collecte automatique des informations système

## 📞 Support
L'application se connecte automatiquement au serveur de mise à jour
pour récupérer les nouvelles versions et envoyer la télémétrie.

Date de packaging: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Taille optimisée pour installation rapide.
'''
        
        readme_path = temp_dir / "README.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        # Créer l'archive
        print(f"\\n🗜️ Création de l'archive: {app_name}")
        
        total_size = 0
        file_count = 0
        
        with zipfile.ZipFile(app_name, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                # Exclure certains dossiers pour réduire la taille
                dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', '.pytest_cache', 'node_modules']]
                
                for file in files:
                    if file.endswith(('.pyc', '.pyo', '.pyd', '.DS_Store')):
                        continue
                        
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(temp_dir)
                    zipf.write(file_path, arcname)
                    total_size += file_path.stat().st_size
                    file_count += 1
        
        # Stats finales
        package_path = Path(app_name)
        compressed_size = package_path.stat().st_size
        compression_ratio = (1 - compressed_size / total_size) * 100 if total_size > 0 else 0
        
        print(f"\\n✅ APPLICATION COMPLÈTE CRÉÉE!")
        print(f"📦 Archive: {app_name}")
        print(f"📁 Fichiers: {file_count}")
        print(f"📏 Taille originale: {total_size:,} octets")
        print(f"📦 Taille compressée: {compressed_size:,} octets")
        print(f"🗜️ Compression: {compression_ratio:.1f}%")
        print(f"🌐 URL pré-configurée: {new_server_url}")
        
        return app_name, compressed_size
        
    finally:
        # Nettoyer
        if temp_dir.exists():
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    try:
        app_name, size = create_complete_compact_app()
        print(f"\\n🎯 UTILISATION:")
        print("1. Transférez cette archive sur le poste client")
        print("2. Décompressez dans un dossier")
        print("3. Exécutez: python3 install.py")
        print("4. Lancez: python3 app_gui.py")
        print("\\n✨ L'application sera automatiquement connectée au serveur Internet!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")