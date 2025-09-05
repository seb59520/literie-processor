#!/usr/bin/env python3
"""
Créateur d'installateur portable pour MATELAS
Installation autonome sans droits administrateur
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_portable_installer():
    """Crée un installateur portable complet"""
    
    print("📦 CRÉATION D'INSTALLATEUR PORTABLE MATELAS")
    print("=" * 60)
    print("🎯 Installation autonome sans droits administrateur")
    print()
    
    version = "3.10.3"
    app_name = "MATELAS_Processor"
    
    # Créer le dossier d'installation portable
    installer_dir = Path("MATELAS_Portable_Installer")
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    print(f"📁 Création installateur: {installer_dir}")
    
    # Créer la structure portable
    app_files_dir = installer_dir / "app_files"
    app_files_dir.mkdir()
    
    print("🏗️ Structure d'installation portable:")
    
    # 1. Copier tous les fichiers de l'application
    source_dir = Path.cwd()
    files_copied = 0
    
    # Fichiers à exclure de l'installateur
    exclude_patterns = {
        '__pycache__', '.pyc', '.git', '.DS_Store', 'node_modules',
        'admin_update_storage', 'backup_*', 'temp_*', '*.backup',
        'MATELAS_Portable_Installer', 'dist', 'build', '*.spec'
    }
    
    print("   📂 Copie des fichiers application...")
    
    for root, dirs, files in os.walk(source_dir):
        # Exclure certains répertoires
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        for file in files:
            # Exclure certains fichiers
            if any(pattern in file for pattern in exclude_patterns):
                continue
            
            source_file = Path(root) / file
            rel_path = source_file.relative_to(source_dir)
            target_file = app_files_dir / rel_path
            
            # Créer répertoire parent
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(source_file, target_file)
                files_copied += 1
            except Exception as e:
                print(f"   ⚠️ Ignoré {rel_path}: {e}")
    
    print(f"   ✅ {files_copied} fichiers copiés")
    
    # 2. Créer script d'installation portable
    install_script = create_install_script(version, app_name)
    (installer_dir / "INSTALL.py").write_text(install_script, encoding='utf-8')
    
    # 3. Créer script de désinstallation
    uninstall_script = create_uninstall_script(app_name)
    (installer_dir / "UNINSTALL.py").write_text(uninstall_script, encoding='utf-8')
    
    # 4. Créer fichier de configuration d'installation
    install_config = {
        "app_name": app_name,
        "version": version,
        "description": "MATELAS Processor - Traitement automatisé des devis PDF",
        "created": datetime.now().isoformat(),
        "install_type": "portable",
        "requires_admin": False,
        "default_install_dir": f"~/Applications/{app_name}",
        "features": [
            "Interface PyQt6 moderne",
            "Traitement LLM automatique",
            "Export Excel intégré", 
            "Système de mise à jour automatique",
            "Gestion sécurisée des clés API",
            "Compatible Windows/Mac/Linux"
        ]
    }
    
    (installer_dir / "install_config.json").write_text(
        json.dumps(install_config, indent=2, ensure_ascii=False), 
        encoding='utf-8'
    )
    
    # 5. Créer README d'installation
    readme_content = create_readme_content(version, app_name)
    (installer_dir / "README.md").write_text(readme_content, encoding='utf-8')
    
    # 6. Créer fichiers batch/shell pour faciliter l'installation
    create_launcher_scripts(installer_dir, app_name)
    
    # 7. Créer ZIP complet
    create_installer_zip(installer_dir, version)
    
    print(f"\n📊 INSTALLATEUR PORTABLE CRÉÉ:")
    print(f"   📁 Dossier: {installer_dir}")
    print(f"   📦 Archive: MATELAS_Portable_v{version}.zip")
    print(f"   💾 Taille: {get_folder_size(installer_dir):.1f} MB")
    
    show_installation_instructions(version)
    
    return True

def create_install_script(version, app_name):
    """Crée le script d'installation Python"""
    return '''#!/usr/bin/env python3
"""
Installateur portable MATELAS v{version}
Installation autonome sans droits administrateur
"""

import os
import sys
import json
import shutil
from pathlib import Path

def install_matelas():
    """Installation portable de MATELAS"""
    print("🚀 INSTALLATION PORTABLE MATELAS v{version}")
    print("=" * 50)
    
    # Détecter l'OS
    import platform
    os_name = platform.system()
    
    # Définir le répertoire d'installation selon l'OS
    if os_name == "Windows":
        default_dir = Path.home() / "AppData" / "Local" / "{app_name}"
    elif os_name == "Darwin":  # macOS
        default_dir = Path.home() / "Applications" / "{app_name}"
    else:  # Linux
        default_dir = Path.home() / ".local" / "share" / "{app_name}"
    
    print(f"💻 OS détecté: {{os_name}}")
    print(f"📁 Répertoire par défaut: {{default_dir}}")
    
    # Demander confirmation du répertoire
    response = input(f"\\n📍 Installer dans {{default_dir}}? [O/n]: ").strip().lower()
    
    if response in ['n', 'no', 'non']:
        custom_path = input("📍 Entrez le chemin d'installation: ").strip()
        install_dir = Path(custom_path) / "{app_name}"
    else:
        install_dir = default_dir
    
    print(f"\\n📦 Installation dans: {{install_dir}}")
    
    # Créer le répertoire d'installation
    if install_dir.exists():
        response = input("⚠️ Le répertoire existe déjà. Écraser? [o/N]: ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Installation annulée")
            return False
        shutil.rmtree(install_dir)
    
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers
    source_dir = Path(__file__).parent / "app_files"
    files_copied = 0
    
    print("\\n📂 Copie des fichiers...")
    
    for item in source_dir.rglob('*'):
        if item.is_file():
            rel_path = item.relative_to(source_dir)
            target_path = install_dir / rel_path
            
            # Créer répertoire parent
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Copier fichier
            shutil.copy2(item, target_path)
            files_copied += 1
            
            if files_copied % 50 == 0:
                print(f"   📁 {{files_copied}} fichiers copiés...")
    
    print(f"✅ {{files_copied}} fichiers installés")
    
    # Créer raccourcis/lanceurs
    create_launchers(install_dir, os_name)
    
    # Créer script de mise à jour du PATH (optionnel)
    create_path_update_script(install_dir, os_name)
    
    # Créer fichier d'information d'installation
    install_info = {{
        "app_name": "{app_name}",
        "version": "{version}",
        "install_date": "{{datetime.now().isoformat()}}",
        "install_dir": str(install_dir),
        "os": os_name,
        "portable": True
    }}
    
    with open(install_dir / "install_info.json", 'w') as f:
        json.dump(install_info, f, indent=2)
    
    print(f"\\n🎉 INSTALLATION TERMINÉE!")
    print(f"📍 Application installée dans: {{install_dir}}")
    print(f"🚀 Lanceur créé sur le bureau (si possible)")
    print(f"\\n▶️ Pour démarrer MATELAS:")
    
    if os_name == "Windows":
        print(f"   Double-cliquez sur: {{install_dir / 'MATELAS.bat'}}")
    else:
        print(f"   Exécutez: {{install_dir / 'start_matelas.sh'}}")
    
    return True

def create_launchers(install_dir, os_name):
    """Crée les lanceurs selon l'OS"""
    from datetime import datetime
    
    if os_name == "Windows":
        # Créer fichier .bat
        bat_content = f'''@echo off
cd /d "{{install_dir}}"
python app_gui.py
pause
'''
        (install_dir / "MATELAS.bat").write_text(bat_content)
        
        # Créer raccourci bureau (tentative)
        try:
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                shortcut_content = f'''[InternetShortcut]
URL=file://{{install_dir / "MATELAS.bat"}}
IconFile={{install_dir / "matelas_icon.ico"}}
'''
                (desktop / "MATELAS.url").write_text(shortcut_content)
        except:
            pass
    
    else:
        # Créer script shell
        shell_content = f'''#!/bin/bash
cd "{{install_dir}}"
python3 app_gui.py
'''
        shell_script = install_dir / "start_matelas.sh"
        shell_script.write_text(shell_content)
        shell_script.chmod(0o755)  # Rendre exécutable
        
        # Créer .desktop (Linux)
        if os_name == "Linux":
            try:
                desktop_file = Path.home() / ".local" / "share" / "applications" / "matelas.desktop"
                desktop_file.parent.mkdir(parents=True, exist_ok=True)
                
                desktop_content = f'''[Desktop Entry]
Name=MATELAS Processor
Comment=Traitement automatisé des devis PDF
Exec=bash "{{install_dir / "start_matelas.sh"}}"
Icon={{install_dir / "matelas_icon.ico"}}
Terminal=false
Type=Application
Categories=Office;
'''
                desktop_file.write_text(desktop_content)
            except:
                pass

def create_path_update_script(install_dir, os_name):
    """Crée un script optionnel pour ajouter au PATH"""
    if os_name == "Windows":
        path_script = f'''@echo off
echo Ajout de MATELAS au PATH utilisateur...
setx PATH "%PATH%;{{install_dir}}"
echo MATELAS ajouté au PATH. Redémarrez votre terminal.
pause
'''
        (install_dir / "add_to_path.bat").write_text(path_script)
    
    else:
        path_script = f'''#!/bin/bash
echo "Ajout de MATELAS au PATH..."
echo 'export PATH="$PATH:{{install_dir}}"' >> ~/.bashrc
echo "MATELAS ajouté au PATH. Redémarrez votre terminal ou exécutez: source ~/.bashrc"
'''
        path_file = install_dir / "add_to_path.sh"
        path_file.write_text(path_script)
        path_file.chmod(0o755)

if __name__ == "__main__":
    import datetime
    success = install_matelas()
    
    if success:
        input("\\n✅ Appuyez sur Entrée pour fermer...")
    else:
        input("\\n❌ Appuyez sur Entrée pour fermer...")
'''

def create_uninstall_script(app_name):
    """Crée le script de désinstallation"""
    return f'''#!/usr/bin/env python3
"""
Désinstallateur portable MATELAS
Suppression complète et propre
"""

import os
import sys
import json
import shutil
from pathlib import Path

def uninstall_matelas():
    """Désinstallation de MATELAS"""
    print("🗑️ DÉSINSTALLATION MATELAS")
    print("=" * 30)
    
    # Chercher l'installation
    possible_dirs = [
        Path.home() / "AppData" / "Local" / "{app_name}",
        Path.home() / "Applications" / "{app_name}",
        Path.home() / ".local" / "share" / "{app_name}"
    ]
    
    install_dir = None
    for dir_path in possible_dirs:
        if dir_path.exists() and (dir_path / "install_info.json").exists():
            install_dir = dir_path
            break
    
    if not install_dir:
        print("❌ Installation MATELAS non trouvée")
        custom_path = input("📍 Entrez le chemin d'installation à supprimer: ").strip()
        if custom_path:
            install_dir = Path(custom_path)
        else:
            return False
    
    print(f"📁 Installation trouvée: {{install_dir}}")
    
    # Lire les infos d'installation
    try:
        with open(install_dir / "install_info.json", 'r') as f:
            install_info = json.load(f)
        print(f"📋 Version: {{install_info.get('version', 'inconnue')}}")
        print(f"📅 Installé le: {{install_info.get('install_date', 'inconnu')[:10]}}")
    except:
        pass
    
    # Confirmation
    response = input(f"\\n⚠️ Supprimer MATELAS de {{install_dir}}? [o/N]: ").strip().lower()
    if response not in ['o', 'oui', 'y', 'yes']:
        print("❌ Désinstallation annulée")
        return False
    
    # Suppression
    print("🗑️ Suppression en cours...")
    
    try:
        # Supprimer raccourcis
        desktop = Path.home() / "Desktop"
        for shortcut in ["MATELAS.url", "MATELAS.lnk"]:
            shortcut_path = desktop / shortcut
            if shortcut_path.exists():
                shortcut_path.unlink()
                print(f"✅ Raccourci supprimé: {{shortcut}}")
        
        # Supprimer .desktop (Linux)
        desktop_file = Path.home() / ".local" / "share" / "applications" / "matelas.desktop"
        if desktop_file.exists():
            desktop_file.unlink()
            print("✅ Fichier .desktop supprimé")
        
        # Supprimer l'installation
        shutil.rmtree(install_dir)
        print(f"✅ Installation supprimée: {{install_dir}}")
        
        print("\\n🎉 DÉSINSTALLATION TERMINÉE!")
        print("MATELAS a été complètement supprimé de votre système.")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la suppression: {{e}}")
        return False

if __name__ == "__main__":
    success = uninstall_matelas()
    
    if success:
        input("\\n✅ Appuyez sur Entrée pour fermer...")
    else:
        input("\\n❌ Appuyez sur Entrée pour fermer...")
'''

def create_readme_content(version, app_name):
    """Crée le contenu du README"""
    return f'''# 📦 MATELAS Portable Installer v{version}

## 🎯 Installation Autonome Sans Droits Administrateur

Cet installateur portable permet d'installer MATELAS sur n'importe quel poste Windows, macOS ou Linux **sans nécessiter de droits administrateur**.

## 🚀 Installation Rapide

### 1️⃣ Méthode Simple (Recommandée)
- **Windows**: Double-cliquez sur `INSTALL.bat`
- **Mac/Linux**: Exécutez `install.sh`

### 2️⃣ Méthode Python
```bash
python INSTALL.py
```

## 📁 Répertoires d'Installation par Défaut

- **Windows**: `%LOCALAPPDATA%\\{app_name}`
- **macOS**: `~/Applications/{app_name}`
- **Linux**: `~/.local/share/{app_name}`

## ✨ Fonctionnalités

- ✅ **Installation portable** - Aucun droit admin requis
- ✅ **Auto-suffisant** - Tous les fichiers inclus
- ✅ **Système de mise à jour** - Mises à jour automatiques
- ✅ **Interface moderne** - PyQt6 avec thème adaptatif
- ✅ **Multi-OS** - Compatible Windows/Mac/Linux
- ✅ **Traitement LLM** - Support OpenAI, Anthropic, OpenRouter
- ✅ **Export Excel** - Génération automatique de fichiers

## 🛠️ Utilisation

Après installation, lancez MATELAS via :
- **Windows**: Raccourci bureau ou `MATELAS.bat`
- **Mac/Linux**: Script `start_matelas.sh`

## 🔄 Mise à Jour

L'application inclut un système de mise à jour automatique :
1. Menu Réglages → Vérifier les mises à jour
2. Installation automatique des patches
3. Redémarrage automatique

## 🗑️ Désinstallation

Pour désinstaller complètement :
```bash
python UNINSTALL.py
```

## 📋 Contenu du Package

- `app_files/` - Fichiers de l'application
- `INSTALL.py` - Script d'installation principal
- `UNINSTALL.py` - Script de désinstallation
- `install_config.json` - Configuration d'installation
- `README.md` - Ce fichier

## 🆔 Informations Version

- **Version**: {version}
- **Type**: Installation portable
- **Droits requis**: Aucun (utilisateur standard)
- **Taille**: ~1.2 GB
- **Python requis**: 3.8+ (inclus si nécessaire)

## 🔧 Support

En cas de problème :
1. Vérifiez que Python 3.8+ est installé
2. Vérifiez les permissions du répertoire d'installation
3. Consultez les logs d'installation

## 🎯 Avantages Installation Portable

- **Pas de pollution du système** - Installation isolée
- **Transportable** - Fonctionne depuis une clé USB
- **Suppression propre** - Désinstallation complète
- **Multi-utilisateur** - Chaque utilisateur a sa propre installation
'''

def create_launcher_scripts(installer_dir, app_name):
    """Crée les scripts de lancement pour chaque OS"""
    
    # Windows .bat
    windows_installer = f'''@echo off
echo 📦 MATELAS Portable Installer
echo.
python INSTALL.py
pause
'''
    (installer_dir / "INSTALL.bat").write_text(windows_installer)
    
    # Shell script pour Mac/Linux
    unix_installer = f'''#!/bin/bash
echo "📦 MATELAS Portable Installer"
echo ""
python3 INSTALL.py
read -p "Appuyez sur Entrée pour fermer..."
'''
    install_sh = installer_dir / "install.sh"
    install_sh.write_text(unix_installer)
    # Rendre exécutable si on est sur Unix
    try:
        install_sh.chmod(0o755)
    except:
        pass

def create_installer_zip(installer_dir, version):
    """Crée l'archive ZIP finale"""
    zip_path = f"MATELAS_Portable_v{version}.zip"
    
    print(f"📦 Création archive finale: {zip_path}")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in installer_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(installer_dir.parent)
                zipf.write(file_path, arcname)
    
    zip_size = Path(zip_path).stat().st_size / (1024*1024)
    print(f"✅ Archive créée: {zip_size:.1f} MB")

def get_folder_size(folder_path):
    """Calcule la taille d'un dossier en MB"""
    total_size = 0
    for file_path in folder_path.rglob('*'):
        if file_path.is_file():
            total_size += file_path.stat().st_size
    return total_size / (1024*1024)

def show_installation_instructions(version):
    """Affiche les instructions finales"""
    print(f"\n🎯 INSTRUCTIONS D'UTILISATION:")
    print("=" * 50)
    print(f"📦 Archive créée: MATELAS_Portable_v{version}.zip")
    print()
    print("📋 DÉPLOIEMENT SUR UN POSTE:")
    print("   1. Copiez MATELAS_Portable_v{version}.zip sur le poste cible")
    print("   2. Décompressez l'archive")
    print("   3. Exécutez:")
    print("      - Windows: INSTALL.bat")
    print("      - Mac/Linux: ./install.sh")
    print("   4. Suivez les instructions à l'écran")
    print()
    print("✅ AVANTAGES:")
    print("   • Aucun droit administrateur requis")
    print("   • Installation dans le profil utilisateur")
    print("   • Complètement portable et autonome")
    print("   • Système de mise à jour intégré")
    print("   • Désinstallation propre disponible")
    print()
    print("🚀 L'utilisateur pourra installer et utiliser MATELAS")
    print("   sans intervention IT et sans droits spéciaux!")

if __name__ == "__main__":
    success = create_portable_installer()
    
    if success:
        print(f"\n🎉 INSTALLATEUR PORTABLE CRÉÉ AVEC SUCCÈS!")
    else:
        print(f"\n❌ Erreur lors de la création de l'installateur")
        sys.exit(1)