#!/usr/bin/env python3
"""
Installateur portable MATELAS COMPACT v3.10.3
Installation autonome sans droits administrateur
"""

import os
import sys
import shutil
from pathlib import Path

def main():
    print("🚀 INSTALLATION PORTABLE MATELAS COMPACT v3.10.3")
    print("=" * 55)
    
    # Détecter l'OS
    import platform
    os_name = platform.system()
    print("💻 OS détecté: " + str(os_name))
    
    # Répertoire d'installation par défaut
    if os_name == "Windows":
        default_dir = Path.home() / "AppData" / "Local" / "MATELAS_Processor"
    elif os_name == "Darwin":
        default_dir = Path.home() / "Applications" / "MATELAS_Processor"
    else:
        default_dir = Path.home() / ".local" / "share" / "MATELAS_Processor"
    
    print("📁 Répertoire par défaut: " + str(default_dir))
    
    # Demander confirmation
    response = input("\nInstaller dans " + str(default_dir) + "? [O/n]: ").strip().lower()
    
    if response in ['n', 'no', 'non']:
        custom_path = input("Entrez le chemin d'installation: ").strip()
        if custom_path:
            install_dir = Path(custom_path) / "MATELAS_Processor"
        else:
            install_dir = default_dir
    else:
        install_dir = default_dir
    
    print("\n📦 Installation dans: " + str(install_dir))
    
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
    print("\n📂 Copie des fichiers...")
    
    try:
        for item in source_dir.rglob('*'):
            if item.is_file():
                rel_path = item.relative_to(source_dir)
                target_path = install_dir / rel_path
                
                target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target_path)
                files_copied += 1
                
                if files_copied % 50 == 0:
                    print("   " + str(files_copied) + " fichiers copiés...")
        
        print("✅ " + str(files_copied) + " fichiers installés")
        
        # Créer lanceur
        create_launcher(install_dir, os_name)
        
        print("\n🎉 INSTALLATION TERMINÉE!")
        print("📍 Application installée dans: " + str(install_dir))
        
        # Créer dossiers manquants si nécessaire
        (install_dir / "logs").mkdir(exist_ok=True)
        (install_dir / "output").mkdir(exist_ok=True)
        (install_dir / "temp_uploads").mkdir(exist_ok=True)
        
        print("📁 Dossiers de travail créés automatiquement")
        
        if os_name == "Windows":
            print("🚀 Pour démarrer: Double-cliquez sur " + str(install_dir / 'MATELAS.bat'))
        else:
            print("🚀 Pour démarrer: " + str(install_dir / 'start_matelas.sh'))
        
        print("\n💡 Note: L'application créera automatiquement les fichiers")
        print("    de logs et de cache au premier démarrage.")
        
    except Exception as e:
        print("❌ Erreur d'installation: " + str(e))

def create_launcher(install_dir, os_name):
    """Crée les lanceurs selon l'OS"""
    if os_name == "Windows":
        bat_content = '@echo off\ncd /d "' + str(install_dir) + '"\npython app_gui.py\npause'
        (install_dir / "MATELAS.bat").write_text(bat_content)
        
        # Tentative de raccourci bureau
        try:
            desktop = Path.home() / "Desktop"
            if desktop.exists():
                (desktop / "MATELAS.bat").write_text(bat_content)
                print("🖥️ Raccourci bureau créé")
        except:
            pass
    
    else:
        shell_content = '#!/bin/bash\ncd "' + str(install_dir) + '"\npython3 app_gui.py'
        shell_script = install_dir / "start_matelas.sh"
        shell_script.write_text(shell_content)
        try:
            shell_script.chmod(0o755)
        except:
            pass

if __name__ == "__main__":
    try:
        main()
        input("\nAppuyez sur Entrée pour fermer...")
    except KeyboardInterrupt:
        print("\n❌ Installation interrompue")
    except Exception as e:
        print("\n❌ Erreur: " + str(e))
        input("Appuyez sur Entrée pour fermer...")
