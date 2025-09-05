#!/usr/bin/env python3
"""
Créateur d'installateur portable simplifié pour MATELAS
"""

import os
import sys
import json
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

def create_portable_installer():
    """Crée un installateur portable simple"""
    
    print("📦 CRÉATION INSTALLATEUR PORTABLE MATELAS")
    print("=" * 50)
    
    version = "3.10.3"
    app_name = "MATELAS_Processor"
    
    # Créer le dossier d'installation
    installer_dir = Path("MATELAS_Portable_Installer")
    if installer_dir.exists():
        shutil.rmtree(installer_dir)
    installer_dir.mkdir()
    
    print(f"📁 Créer installateur: {installer_dir}")
    
    # 1. Copier les fichiers de l'application
    app_files_dir = installer_dir / "app_files"
    app_files_dir.mkdir()
    
    source_dir = Path.cwd()
    files_copied = 0
    
    # Fichiers à exclure
    exclude_patterns = {
        '__pycache__', '.pyc', '.git', '.DS_Store', 
        'admin_update_storage', 'backup_*', 'temp_*', 
        'MATELAS_Portable_Installer', '*.backup'
    }
    
    print("📂 Copie des fichiers...")
    
    for root, dirs, files in os.walk(source_dir):
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        for file in files:
            if any(pattern in file for pattern in exclude_patterns):
                continue
            
            source_file = Path(root) / file
            rel_path = source_file.relative_to(source_dir)
            target_file = app_files_dir / rel_path
            
            target_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(source_file, target_file)
                files_copied += 1
                if files_copied % 100 == 0:
                    print(f"   {files_copied} fichiers...")
            except Exception as e:
                continue
    
    print(f"✅ {files_copied} fichiers copiés")
    
    # 2. Créer script d'installation simple
    install_script_content = create_simple_install_script(version, app_name)
    (installer_dir / "install.py").write_text(install_script_content, encoding='utf-8')
    
    # 3. Créer README
    readme_content = create_simple_readme(version, app_name)
    (installer_dir / "README.txt").write_text(readme_content, encoding='utf-8')
    
    # 4. Créer lanceurs
    # Windows
    windows_bat = f'''@echo off
echo MATELAS Portable Installer v{version}
echo.
python install.py
pause
'''
    (installer_dir / "INSTALL.bat").write_text(windows_bat, encoding='utf-8')
    
    # Unix
    unix_sh = f'''#!/bin/bash
echo "MATELAS Portable Installer v{version}"
echo ""
python3 install.py
read -p "Appuyez sur Entree pour fermer..."
'''
    install_sh = installer_dir / "install.sh"
    install_sh.write_text(unix_sh, encoding='utf-8')
    
    try:
        install_sh.chmod(0o755)
    except:
        pass
    
    # 5. Créer archive ZIP
    zip_name = f"MATELAS_Portable_v{version}.zip"
    print(f"📦 Création de {zip_name}...")
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file_path in installer_dir.rglob('*'):
            if file_path.is_file():
                arcname = file_path.relative_to(installer_dir.parent)
                zipf.write(file_path, arcname)
    
    zip_size = Path(zip_name).stat().st_size / (1024*1024)
    
    print(f"\n🎉 INSTALLATEUR CRÉÉ AVEC SUCCÈS!")
    print(f"📁 Dossier: {installer_dir}")
    print(f"📦 Archive: {zip_name} ({zip_size:.1f} MB)")
    
    show_usage_instructions(version)
    
    return True

def create_simple_install_script(version, app_name):
    """Crée un script d'installation simple"""
    return f'''#!/usr/bin/env python3
"""
Installateur portable MATELAS v{version}
Installation autonome sans droits administrateur
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("🚀 INSTALLATION PORTABLE MATELAS v{version}")
    print("=" * 50)
    
    # Détecter l'OS
    import platform
    os_name = platform.system()
    print(f"💻 OS détecté: {{os_name}}")
    
    # Répertoire d'installation par défaut
    if os_name == "Windows":
        default_dir = Path.home() / "AppData" / "Local" / "{app_name}"
    elif os_name == "Darwin":
        default_dir = Path.home() / "Applications" / "{app_name}"
    else:
        default_dir = Path.home() / ".local" / "share" / "{app_name}"
    
    print(f"📁 Répertoire par défaut: {{default_dir}}")
    
    # Demander confirmation
    response = input(f"\\nInstaller dans {{default_dir}}? [O/n]: ").strip().lower()
    
    if response in ['n', 'no', 'non']:
        custom_path = input("Entrez le chemin d'installation: ").strip()
        if custom_path:
            install_dir = Path(custom_path) / "{app_name}"
        else:
            install_dir = default_dir
    else:
        install_dir = default_dir
    
    print(f"\\n📦 Installation dans: {{install_dir}}")
    
    # Vérifier si le répertoire existe
    if install_dir.exists():
        response = input("⚠️ Le répertoire existe déjà. Continuer? [o/N]: ").strip().lower()
        if response not in ['o', 'oui', 'y', 'yes']:
            print("❌ Installation annulée")
            return
        try:
            shutil.rmtree(install_dir)
        except:
            pass
    
    # Créer le répertoire
    install_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier les fichiers
    source_dir = Path(__file__).parent / "app_files"
    if not source_dir.exists():
        print("❌ Erreur: Fichiers d'installation non trouvés")
        return
    
    files_copied = 0
    print("\\n📂 Copie des fichiers...")
    
    try:
        for item in source_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(source_dir)
                target_path = install_dir / rel_path
                
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
                files_copied += 1
                
                if files_copied % 100 == 0:
                    print(f"   {{files_copied}} fichiers copiés...")
        
        print(f"✅ {{files_copied}} fichiers installés")
        
        # Créer lanceur
        create_launcher(install_dir, os_name)
        
        print(f"\\n🎉 INSTALLATION TERMINÉE!")
        print(f"📍 Application installée dans: {{install_dir}}")
        
        if os_name == "Windows":
            print(f"🚀 Pour démarrer: Double-cliquez sur {{install_dir / 'MATELAS.bat'}}")
        else:
            print(f"🚀 Pour démarrer: {{install_dir / 'start_matelas.sh'}}")
        
    except Exception as e:
        print(f"❌ Erreur d'installation: {{e}}")

def create_launcher(install_dir, os_name):
    """Crée les lanceurs selon l'OS"""
    if os_name == "Windows":
        bat_content = '@echo off\\ncd /d "' + str(install_dir) + '"\\npython app_gui.py\\npause'
        (install_dir / "MATELAS.bat").write_text(bat_content)
        
        # Tentative de raccourci bureau
        try:
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                (desktop / "MATELAS.bat").write_text(bat_content)
        except:
            pass
    
    else:
        shell_content = '#!/bin/bash\\ncd "' + str(install_dir) + '"\\npython3 app_gui.py'
        shell_script = install_dir / "start_matelas.sh"
        shell_script.write_text(shell_content)
        try:
            shell_script.chmod(0o755)
        except:
            pass

if __name__ == "__main__":
    try:
        main()
        input("\\nAppuyez sur Entrée pour fermer...")
    except KeyboardInterrupt:
        print("\\n❌ Installation interrompue")
    except Exception as e:
        print(f"\\n❌ Erreur: {{e}}")
        input("Appuyez sur Entrée pour fermer...")
'''

def create_simple_readme(version, app_name):
    """Crée un README simple"""
    return f'''MATELAS Portable Installer v{version}
=====================================

INSTALLATION AUTONOME SANS DROITS ADMINISTRATEUR

Instructions d'installation:
---------------------------

1. Windows:
   - Double-cliquez sur INSTALL.bat

2. Mac/Linux:
   - Ouvrez un terminal
   - Exécutez: ./install.sh
   - Ou: python3 install.py

3. Suivez les instructions à l'écran

Répertoires d'installation par défaut:
--------------------------------------
- Windows: %LOCALAPPDATA%\\{app_name}
- macOS: ~/Applications/{app_name}
- Linux: ~/.local/share/{app_name}

Fonctionnalités:
---------------
✓ Installation portable (aucun droit admin)
✓ Système de mise à jour automatique intégré
✓ Interface PyQt6 moderne
✓ Traitement LLM automatique
✓ Export Excel intégré
✓ Compatible Windows/Mac/Linux

Utilisation:
-----------
Après installation, lancez MATELAS via:
- Windows: MATELAS.bat (ou raccourci bureau)
- Mac/Linux: start_matelas.sh

Support:
--------
- Nécessite Python 3.8 ou supérieur
- Environ 1.2 GB d'espace disque
- Aucune connexion Internet requise pour l'installation

Version: {version}
Type: Installation portable
Créé: {datetime.now().strftime("%Y-%m-%d")}
'''

def show_usage_instructions(version):
    """Affiche les instructions d'utilisation"""
    print(f"\n📋 INSTRUCTIONS DE DÉPLOIEMENT:")
    print("=" * 40)
    print(f"1. Copiez MATELAS_Portable_v{version}.zip sur le poste cible")
    print("2. Décompressez l'archive")
    print("3. Exécutez selon l'OS:")
    print("   • Windows: INSTALL.bat")
    print("   • Mac/Linux: ./install.sh")
    print("4. Suivez les instructions")
    print()
    print("🎯 AVANTAGES:")
    print("• Aucun droit administrateur requis")
    print("• Installation dans le profil utilisateur")
    print("• Complètement autonome")
    print("• Système de mise à jour intégré")
    print("• Compatible tous OS")

if __name__ == "__main__":
    success = create_portable_installer()
    
    if success:
        print(f"\n✅ Installateur portable prêt!")
    else:
        print(f"\n❌ Erreur de création")
        sys.exit(1)