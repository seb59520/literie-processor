#!/usr/bin/env python3
"""
Script de mise à jour de la version portable MATELAS
Met à jour dist_portable_update_ready avec tous les nouveaux composants
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime
import zipfile

class PortableUpdater:
    """Gestionnaire de mise à jour de la version portable"""
    
    def __init__(self):
        self.base_path = Path.cwd()
        self.portable_path = self.base_path / "dist_portable_update_ready"
        self.consolidated_path = self.base_path / "online_admin_interface" / "update_storage" / "updates" / "consolidated"
        
        # Nouveaux fichiers à copier
        self.new_files = [
            "package_builder.py",
            "package_builder_gui.py", 
            "auto_package_generator.py",
            "auto_package_gui.py",
            "package_consolidator.py",
            "test_package_builder.py",
            "test_consolidation.py"
        ]
        
        # Fichiers à mettre à jour
        self.update_files = [
            "app_gui.py",
            "config.py",
            "version.py",
            "matelas_config.json"
        ]
    
    def backup_portable(self):
        """Créer une sauvegarde de la version portable"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.base_path / f"backup_portable_{timestamp}"
        
        print(f"💾 Création sauvegarde: {backup_path.name}")
        
        if self.portable_path.exists():
            shutil.copytree(self.portable_path, backup_path)
            print(f"✅ Sauvegarde créée: {backup_path}")
            return backup_path
        else:
            print("⚠️ Répertoire portable non trouvé")
            return None
    
    def copy_new_files(self):
        """Copier les nouveaux fichiers vers la version portable"""
        print("📁 Copie des nouveaux fichiers...")
        
        copied_files = []
        
        for file_name in self.new_files:
            source_file = self.base_path / file_name
            dest_file = self.portable_path / file_name
            
            if source_file.exists():
                try:
                    shutil.copy2(source_file, dest_file)
                    copied_files.append(file_name)
                    print(f"   ✅ {file_name}")
                except Exception as e:
                    print(f"   ❌ {file_name}: {e}")
            else:
                print(f"   ⚠️ {file_name}: fichier source non trouvé")
        
        return copied_files
    
    def update_existing_files(self):
        """Mettre à jour les fichiers existants"""
        print("🔄 Mise à jour des fichiers existants...")
        
        updated_files = []
        
        for file_name in self.update_files:
            source_file = self.base_path / file_name
            dest_file = self.portable_path / file_name
            
            if source_file.exists():
                try:
                    shutil.copy2(source_file, dest_file)
                    updated_files.append(file_name)
                    print(f"   ✅ {file_name}")
                except Exception as e:
                    print(f"   ❌ {file_name}: {e}")
            else:
                print(f"   ⚠️ {file_name}: fichier source non trouvé")
        
        return updated_files
    
    def copy_consolidated_package(self):
        """Copier le package consolidé vers la version portable"""
        print("📦 Copie du package consolidé...")
        
        # Créer le répertoire consolidated dans portable
        portable_consolidated = self.portable_path / "consolidated_packages"
        portable_consolidated.mkdir(exist_ok=True)
        
        # Trouver le dernier package consolidé
        consolidated_files = list(self.consolidated_path.glob("*.zip"))
        
        if consolidated_files:
            # Prendre le plus récent
            latest_package = max(consolidated_files, key=lambda x: x.stat().st_mtime)
            dest_package = portable_consolidated / latest_package.name
            
            try:
                shutil.copy2(latest_package, dest_package)
                print(f"   ✅ {latest_package.name}")
                return dest_package
            except Exception as e:
                print(f"   ❌ Erreur copie package: {e}")
                return None
        else:
            print("   ⚠️ Aucun package consolidé trouvé")
            return None
    
    def update_portable_config(self):
        """Mettre à jour les configurations pour la version portable"""
        print("⚙️ Mise à jour des configurations...")
        
        # Mettre à jour matelas_config.json
        config_file = self.portable_path / "matelas_config.json"
        
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                # S'assurer que l'URL du serveur est correcte
                config['server_url'] = 'http://72.60.47.183/'
                
                # Ajouter des métadonnées de mise à jour
                config['portable_updated'] = datetime.now().isoformat()
                config['portable_version'] = '3.11.12_portable'
                
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                
                print("   ✅ matelas_config.json mis à jour")
                
            except Exception as e:
                print(f"   ❌ Erreur mise à jour config: {e}")
    
    def create_installation_script(self):
        """Créer un script d'installation pour autre poste"""
        install_script = """#!/usr/bin/env python3
\"\"\"
Script d'installation MATELAS Portable v3.11.12
Installation automatique sur un nouveau poste
\"\"\"

import os
import sys
import subprocess
import json
from pathlib import Path

def install_dependencies():
    \"\"\"Installer les dépendances requises\"\"\"
    print("📦 Installation des dépendances...")
    
    requirements = [
        "PyQt6",
        "requests", 
        "PyMuPDF",
        "openpyxl",
        "paramiko",
        "cryptography"
    ]
    
    for req in requirements:
        try:
            print(f"   📥 Installation de {req}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"   ✅ {req} installé")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erreur installation {req}: {e}")
            return False
    
    return True

def setup_directories():
    \"\"\"Créer les répertoires nécessaires\"\"\"
    print("📁 Création des répertoires...")
    
    directories = [
        "output",
        "temp_uploads", 
        "logs",
        "config",
        "data"
    ]
    
    for dir_name in directories:
        try:
            Path(dir_name).mkdir(exist_ok=True)
            print(f"   ✅ {dir_name}/")
        except Exception as e:
            print(f"   ❌ Erreur création {dir_name}: {e}")

def configure_application():
    \"\"\"Configuration initiale de l'application\"\"\"
    print("⚙️ Configuration de l'application...")
    
    # Vérifier la configuration
    config_file = Path("matelas_config.json")
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("   ✅ Configuration chargée")
            print(f"   🌐 Serveur: {config.get('server_url', 'Non configuré')}")
        except Exception as e:
            print(f"   ⚠️ Erreur lecture config: {e}")

def test_installation():
    \"\"\"Tester l'installation\"\"\"
    print("🧪 Test de l'installation...")
    
    try:
        # Test d'import des modules principaux
        import PyQt6
        print("   ✅ PyQt6")
        
        import requests
        print("   ✅ requests")
        
        import fitz  # PyMuPDF
        print("   ✅ PyMuPDF") 
        
        import openpyxl
        print("   ✅ openpyxl")
        
        # Test des modules de l'application
        import config
        print("   ✅ config")
        
        import version
        print("   ✅ version")
        
        print("\\n🎉 Installation réussie!")
        print("\\n🚀 Pour lancer l'application:")
        print("   python3 app_gui.py")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Erreur d'import: {e}")
        return False

def main():
    print("🚀 INSTALLATION MATELAS PORTABLE v3.11.12")
    print("=" * 50)
    
    print(f"📂 Répertoire d'installation: {Path.cwd()}")
    
    # Vérifier Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        sys.exit(1)
    
    print(f"✅ Python {sys.version}")
    
    # Installation
    steps = [
        ("Installation des dépendances", install_dependencies),
        ("Création des répertoires", setup_directories),
        ("Configuration", configure_application),
        ("Test", test_installation)
    ]
    
    for step_name, step_func in steps:
        print(f"\\n📋 {step_name}...")
        try:
            result = step_func()
            if result is False:
                print(f"❌ Échec: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"❌ Erreur {step_name}: {e}")
            sys.exit(1)
    
    print("\\n" + "=" * 50)
    print("✅ INSTALLATION TERMINÉE AVEC SUCCÈS!")
    print("\\n📖 Aide:")
    print("   • Lancer: python3 app_gui.py")  
    print("   • Guide: Ouvrir README.md")
    print("   • Support: Vérifier les logs/ en cas de problème")

if __name__ == "__main__":
    main()
"""
        
        install_file = self.portable_path / "install.py"
        
        try:
            with open(install_file, 'w', encoding='utf-8') as f:
                f.write(install_script)
            
            # Rendre exécutable sur Unix
            if os.name != 'nt':
                os.chmod(install_file, 0o755)
            
            print(f"   ✅ Script d'installation créé: {install_file.name}")
            return install_file
            
        except Exception as e:
            print(f"   ❌ Erreur création script: {e}")
            return None
    
    def create_readme_portable(self):
        """Créer un README pour la version portable"""
        readme_content = """# MATELAS Application Portable v3.11.12

## 🚀 Installation Rapide

### Prérequis
- Python 3.8+
- Connexion Internet (pour l'installation des dépendances)

### Installation Automatique
```bash
python3 install.py
```

### Installation Manuelle
```bash
pip install PyQt6 requests PyMuPDF openpyxl paramiko cryptography
python3 app_gui.py
```

## 📁 Structure du Projet

```
MATELAS_PORTABLE/
├── app_gui.py                    # Application principale
├── install.py                    # Script d'installation
├── config.py                     # Configuration système
├── version.py                     # Gestion des versions
├── package_builder.py            # Générateur de packages
├── package_builder_gui.py        # Interface générateur manuel
├── auto_package_generator.py     # Générateur automatique
├── auto_package_gui.py          # Interface générateur auto
├── package_consolidator.py      # Consolidateur de packages
├── backend/                     # Modules de traitement
├── config/                      # Configurations
├── template/                    # Templates Excel
└── consolidated_packages/       # Packages consolidés
```

## 🎯 Nouvelles Fonctionnalités v3.11.12

### 📦 Générateur de Packages Correctifs
- **Création manuelle** : Menu Diagnostic → Créer Package Correctif
- **Suggestions automatiques** : Menu Diagnostic → Suggestions Automatiques
- **Consolidation** : Menu Diagnostic → Consolidation & Upload VPS
- **Protection** : Accès protégé par mot de passe développeur

### 🌐 Configuration Serveur
- **VPS intégré** : Serveur de mise à jour sur VPS dédié
- **Upload automatique** : Envoi des packages vers le serveur
- **Configuration** : Menu Configuration → Configuration Serveur

## 🔧 Configuration

### Premier Lancement
1. Lancer `python3 app_gui.py`
2. Configurer les clés API (Menu Configuration)
3. Vérifier l'URL du serveur (72.60.47.183)
4. Tester avec un PDF exemple

### URLs et Serveurs
- **Serveur principal** : http://72.60.47.183/
- **Interface admin** : http://72.60.47.183/admin
- **API** : http://72.60.47.183/api/v1/

## 🛠️ Outils Développeur

### Générateur de Packages
- **Mot de passe** : `matelas_dev_2025`
- **Packages manuels** : Sélection de fichiers personnalisée
- **Packages automatiques** : Détection des modifications récentes
- **Consolidation** : Fusion de packages par version

### Types de Packages Détectés
- 🖥️ **Interface** : Modifications GUI et interfaces
- ⚙️ **Backend** : Utilitaires et traitement
- 📋 **Configuration** : Paramètres système
- 🛠️ **Scripts** : Outils et utilitaires
- 📊 **Référentiels** : Données métier
- 📄 **Templates** : Modèles Excel

## 🚨 Dépannage

### Problèmes Courants
- **Erreur PyQt6** : `pip install --upgrade PyQt6`
- **Connexion serveur** : Vérifier l'URL dans Configuration
- **Permissions** : Exécuter en tant qu'administrateur si nécessaire
- **Dépendances** : Relancer `python3 install.py`

### Logs
Les logs sont dans le répertoire `logs/` :
- `app.log` : Log principal de l'application
- `errors.log` : Erreurs système
- `processing.log` : Traitement des PDFs

### Support
- Consulter les logs en cas de problème
- Vérifier la configuration réseau
- Tester avec un PDF simple d'abord

## 📋 Changelog v3.11.12

### ⚙️ Backend/Traitement
- Améliorations des utilitaires de traitement
- Optimisations des performances
- Corrections de bugs système

### 📋 Configuration  
- Mise à jour des paramètres système
- Correction des URLs de serveur
- Optimisation des configurations LLM

### 🖥️ Interface Utilisateur
- Nouvelles fonctionnalités GUI
- Générateur de packages correctifs
- Améliorations ergonomiques

### 🛠️ Scripts/Utilitaires
- Nouveaux outils de maintenance
- Scripts d'automatisation
- Utilitaires de diagnostic

## 📞 Contact
- Documentation complète dans l'application
- Aide contextuelle via F1
- Support technique via les logs système
"""
        
        readme_file = self.portable_path / "README.md"
        
        try:
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(readme_content)
            
            print(f"   ✅ README portable créé: {readme_file.name}")
            return readme_file
            
        except Exception as e:
            print(f"   ❌ Erreur création README: {e}")
            return None
    
    def create_launcher_scripts(self):
        """Créer les scripts de lancement"""
        print("🚀 Création des scripts de lancement...")
        
        # Script Windows
        bat_script = """@echo off
echo Lancement MATELAS Application v3.11.12...
cd /d "%~dp0"
python app_gui.py
if errorlevel 1 (
    echo.
    echo Erreur de lancement. Tentative avec python3...
    python3 app_gui.py
)
if errorlevel 1 (
    echo.
    echo Erreur: Python non trouve ou dependances manquantes
    echo Executez d'abord: python install.py
    pause
)
"""
        
        bat_file = self.portable_path / "lancer_matelas.bat"
        
        try:
            with open(bat_file, 'w', encoding='cp1252') as f:
                f.write(bat_script)
            print(f"   ✅ Script Windows: {bat_file.name}")
        except Exception as e:
            print(f"   ❌ Erreur script Windows: {e}")
        
        # Script Unix/Mac
        sh_script = """#!/bin/bash
echo "Lancement MATELAS Application v3.11.12..."
cd "$(dirname "$0")"

# Essayer python3 d'abord, puis python
if command -v python3 &> /dev/null; then
    python3 app_gui.py
elif command -v python &> /dev/null; then
    python app_gui.py
else
    echo "Erreur: Python non trouvé"
    echo "Installez Python 3.8+ et exécutez: python3 install.py"
    exit 1
fi
"""
        
        sh_file = self.portable_path / "lancer_matelas.sh"
        
        try:
            with open(sh_file, 'w', encoding='utf-8') as f:
                f.write(sh_script)
            
            # Rendre exécutable
            if os.name != 'nt':
                os.chmod(sh_file, 0o755)
            
            print(f"   ✅ Script Unix/Mac: {sh_file.name}")
        except Exception as e:
            print(f"   ❌ Erreur script Unix: {e}")
    
    def run_full_update(self):
        """Exécuter la mise à jour complète"""
        print("🚀 MISE À JOUR VERSION PORTABLE MATELAS v3.11.12")
        print("=" * 60)
        
        # Étape 1: Sauvegarde
        backup_path = self.backup_portable()
        
        # Étape 2: Copie des nouveaux fichiers
        copied = self.copy_new_files()
        print(f"📁 {len(copied)} nouveaux fichiers copiés")
        
        # Étape 3: Mise à jour des fichiers existants
        updated = self.update_existing_files()
        print(f"🔄 {len(updated)} fichiers mis à jour")
        
        # Étape 4: Package consolidé
        package = self.copy_consolidated_package()
        if package:
            print(f"📦 Package consolidé: {package.name}")
        
        # Étape 5: Configuration
        self.update_portable_config()
        
        # Étape 6: Scripts d'installation et lancement
        install_script = self.create_installation_script()
        readme = self.create_readme_portable() 
        self.create_launcher_scripts()
        
        print("\n" + "=" * 60)
        print("✅ MISE À JOUR PORTABLE TERMINÉE!")
        print(f"📂 Version portable: {self.portable_path}")
        
        if backup_path:
            print(f"💾 Sauvegarde: {backup_path}")
        
        print("\n📋 Fichiers prêts pour installation sur autre poste:")
        print("   • Copier tout le dossier dist_portable_update_ready/")
        print("   • Sur le nouveau poste: python3 install.py")
        print("   • Puis lancer: python3 app_gui.py")
        
        return True


if __name__ == "__main__":
    updater = PortableUpdater()
    updater.run_full_update()