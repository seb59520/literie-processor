#!/usr/bin/env python3
"""
Build portable de l'application avec système de mise à jour automatique
Version prête pour récupération des mises à jour
"""

import os
import shutil
import json
from pathlib import Path
import zipfile
from datetime import datetime

def create_portable_build():
    """Créer une version portable avec système de mise à jour"""
    
    print("🚀 CRÉATION VERSION PORTABLE AVEC MISE À JOUR AUTOMATIQUE")
    print("=" * 60)
    
    # Configuration
    build_dir = "dist_portable_update_ready"
    app_name = "MatelasProcessor"
    version = "3.11.9"
    
    # Nettoyer et créer le répertoire
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    print(f"📁 Répertoire de build: {build_dir}")
    
    # === 1. FICHIERS PRINCIPAUX ===
    main_files = [
        "app_gui.py",
        "version.py",
        "backend_interface.py",
        "real_time_alerts.py",
        "ui_optimizations.py",
        "config.py",
    ]
    
    print("\n📋 Copie des fichiers principaux:")
    for file in main_files:
        if os.path.exists(file):
            shutil.copy2(file, f"{build_dir}/{file}")
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️ Fichier manquant: {file}")
    
    # === 2. RÉPERTOIRE BACKEND ===
    print("\n📋 Copie du répertoire backend:")
    if os.path.exists("backend"):
        shutil.copytree("backend", f"{build_dir}/backend")
        print(f"  ✅ backend/ (répertoire complet)")
    
    # === 3. RÉPERTOIRE CONFIG ===
    print("\n📋 Copie du répertoire config:")
    if os.path.exists("config"):
        shutil.copytree("config", f"{build_dir}/config")
        print(f"  ✅ config/ (répertoire complet)")
    
    # === 4. TEMPLATES ===
    print("\n📋 Copie des templates:")
    if os.path.exists("template"):
        shutil.copytree("template", f"{build_dir}/template")
        print(f"  ✅ template/ (répertoire complet)")
    
    # === 5. FICHIERS DE CONFIGURATION ===
    config_files = [
        "matelas_config.json",
        "matelas_config.json.template",
        "notion_config.json.template",
        "requirements.txt",
        "requirements_gui.txt"
    ]
    
    print("\n📋 Copie des fichiers de configuration:")
    for file in config_files:
        if os.path.exists(file):
            shutil.copy2(file, f"{build_dir}/{file}")
            print(f"  ✅ {file}")
    
    # === 6. CONFIGURATION SPÉCIALE POUR MISE À JOUR ===
    print("\n🔧 Configuration du système de mise à jour:")
    
    # Créer le fichier de configuration de mise à jour
    update_config = {
        "auto_update": {
            "enabled": True,
            "server_url": "https://edceecf7fdaf.ngrok-free.app",
            "check_interval_hours": 24,
            "auto_download": True,
            "auto_install": False,  # L'utilisateur doit confirmer
            "show_notifications": True
        },
        "client_info": {
            "client_id": "",  # Sera généré au premier lancement
            "installation_date": datetime.now().isoformat(),
            "build_type": "portable"
        }
    }
    
    with open(f"{build_dir}/update_config.json", "w", encoding="utf-8") as f:
        json.dump(update_config, f, indent=2, ensure_ascii=False)
    print("  ✅ update_config.json créé")
    
    # === 7. SCRIPT DE LANCEMENT ===
    print("\n📋 Création des scripts de lancement:")
    
    # Script Windows
    bat_content = f"""@echo off
title {app_name} v{version}
echo 🚀 Démarrage de {app_name} v{version}
echo 📡 Mise à jour automatique activée
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé ou pas dans le PATH
    echo Veuillez installer Python 3.8 ou plus récent
    pause
    exit /b 1
)

REM Installer les dépendances si nécessaire
echo 📦 Vérification des dépendances...
python -c "import PyQt6" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📥 Installation de PyQt6...
    pip install PyQt6
)

REM Lancer l'application
echo ▶️ Lancement de l'application...
python app_gui.py
if %errorlevel% neq 0 (
    echo.
    echo ❌ Erreur lors du lancement
    pause
)
"""
    
    with open(f"{build_dir}/lancer_matelas.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)
    print("  ✅ lancer_matelas.bat")
    
    # Script Linux/Mac
    sh_content = f"""#!/bin/bash
echo "🚀 Démarrage de {app_name} v{version}"
echo "📡 Mise à jour automatique activée"
echo

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    echo "Veuillez installer Python 3.8 ou plus récent"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python3 -c "import PyQt6" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📥 Installation de PyQt6..."
    pip3 install PyQt6
fi

# Lancer l'application
echo "▶️ Lancement de l'application..."
python3 app_gui.py
"""
    
    with open(f"{build_dir}/lancer_matelas.sh", "w", encoding="utf-8") as f:
        f.write(sh_content)
    
    # Rendre le script exécutable
    os.chmod(f"{build_dir}/lancer_matelas.sh", 0o755)
    print("  ✅ lancer_matelas.sh")
    
    # === 8. README POUR L'UTILISATEUR ===
    readme_content = f"""# {app_name} v{version} - Version Portable

## 🚀 Lancement rapide

### Windows
Double-cliquez sur `lancer_matelas.bat`

### Linux/Mac
```bash
./lancer_matelas.sh
```

## 📡 Système de mise à jour automatique

Cette version inclut un système de mise à jour automatique qui :

✅ **Vérifie automatiquement** les nouvelles versions
✅ **Affiche un indicateur** dans la barre de statut
✅ **Propose le téléchargement** des mises à jour
✅ **Préserve vos configurations** lors des mises à jour

### Fonctionnement

- 🔍 **Vérification** : Toutes les 24h + au démarrage
- 📊 **Indicateur** : Visible en bas à droite de l'application
- 🎯 **Cliquable** : Cliquez sur l'indicateur pour voir les détails
- 🔒 **Sécurisé** : Téléchargement depuis serveur officiel

### États de l'indicateur

- 🔄 **Bleu** : Vérification en cours
- ✅ **Vert** : Application à jour
- 🆕 **Rouge** : Nouvelle version disponible
- ⚠️ **Gris** : Erreur de connexion

## 📁 Structure

```
{app_name}/
├── app_gui.py              # Application principale
├── backend/                # Logique métier
├── config/                 # Configurations
├── template/               # Templates Excel
├── update_config.json      # Configuration mise à jour
├── lancer_matelas.bat      # Lanceur Windows
├── lancer_matelas.sh       # Lanceur Linux/Mac
└── README.md              # Ce fichier
```

## 🔧 Configuration

Le fichier `update_config.json` permet de configurer :

- **Activation/désactivation** des mises à jour automatiques
- **Fréquence** de vérification
- **Serveur** de mise à jour
- **Notifications**

## 🆘 Dépannage

### L'application ne démarre pas
1. Vérifiez que Python 3.8+ est installé
2. Lancez `pip install -r requirements_gui.txt`
3. Utilisez les scripts de lancement fournis

### L'indicateur de mise à jour ne s'affiche pas
1. Vérifiez votre connexion Internet
2. L'indicateur apparaît en bas à droite après quelques secondes
3. Redémarrez l'application si nécessaire

### Erreur de mise à jour
1. Vérifiez votre connexion Internet
2. L'application fonctionne normalement même sans mise à jour
3. Vous pouvez désactiver les mises à jour dans `update_config.json`

## 📞 Support

- Version : {version}
- Build : {datetime.now().strftime("%Y-%m-%d")}
- Type : Portable avec mise à jour automatique

---
🎯 **Conseil** : Gardez l'application à jour pour bénéficier des dernières améliorations !
"""
    
    with open(f"{build_dir}/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)
    print("  ✅ README.md")
    
    # === 9. INFORMATIONS FINALES ===
    build_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                     for dirpath, dirnames, filenames in os.walk(build_dir)
                     for filename in filenames) / (1024 * 1024)
    
    print(f"\n✅ BUILD PORTABLE TERMINÉ!")
    print(f"📍 Emplacement: ./{build_dir}/")
    print(f"📏 Taille totale: {build_size:.1f} MB")
    print(f"🔄 Mise à jour auto: ACTIVÉE")
    print(f"🌐 Serveur: https://edceecf7fdaf.ngrok-free.app")
    
    print(f"\n🎯 INSTRUCTIONS D'UTILISATION:")
    print(f"1. Copiez le dossier {build_dir} sur votre poste client")
    print(f"2. Windows: Double-cliquez sur lancer_matelas.bat")
    print(f"3. Linux/Mac: Lancez ./lancer_matelas.sh")
    print(f"4. L'indicateur de mise à jour apparaît en bas à droite")
    
    return build_dir

def create_portable_archive():
    """Créer une archive ZIP de la version portable"""
    
    build_dir = "dist_portable_update_ready"
    
    if not os.path.exists(build_dir):
        print("❌ Répertoire de build non trouvé. Lancez d'abord create_portable_build()")
        return None
    
    print(f"\n📦 CRÉATION DE L'ARCHIVE...")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_name = f"MatelasProcessor_v3.11.9_portable_{timestamp}.zip"
    
    with zipfile.ZipFile(archive_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(build_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, build_dir)
                zipf.write(file_path, f"MatelasProcessor/{arc_name}")
    
    archive_size = os.path.getsize(archive_name) / (1024 * 1024)
    
    print(f"✅ Archive créée: {archive_name}")
    print(f"📏 Taille archive: {archive_size:.1f} MB")
    print(f"\n🎯 PRÊT POUR DÉPLOIEMENT!")
    print(f"📤 Envoyez {archive_name} sur votre poste client")
    print(f"📂 Décompressez et lancez l'application")
    
    return archive_name

if __name__ == "__main__":
    # Créer le build portable
    build_dir = create_portable_build()
    
    # Créer l'archive
    archive = create_portable_archive()
    
    print(f"\n🎉 VERSION PORTABLE PRÊTE!")
    print(f"📁 Répertoire: {build_dir}")
    print(f"📦 Archive: {archive}")