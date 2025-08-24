#!/usr/bin/env python3
"""
Script d'installation automatique pour l'application Matelas
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def get_install_dir():
    """Détermine le répertoire d'installation selon l'OS"""
    system = platform.system()
    
    if system == "Windows":
        # Windows: Program Files ou répertoire utilisateur
        program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        return os.path.join(program_files, "MatelasProcessor")
    elif system == "Darwin":  # macOS
        return "/Applications/MatelasProcessor"
    else:  # Linux
        return "/opt/matelas-processor"

def create_desktop_shortcut(install_dir, app_name):
    """Crée un raccourci sur le bureau"""
    system = platform.system()
    
    if system == "Windows":
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop, f"{app_name}.lnk")
        
        # Créer un fichier .bat comme alternative
        bat_path = os.path.join(desktop, f"{app_name}.bat")
        with open(bat_path, 'w') as f:
            f.write(f'@echo off\ncd /d "{install_dir}"\npython3 run_gui.py\npause')
        
        print(f"✅ Raccourci créé: {bat_path}")
        
    elif system == "Darwin":  # macOS
        # Créer un .command file
        desktop = os.path.expanduser("~/Desktop")
        command_path = os.path.join(desktop, f"{app_name}.command")
        
        with open(command_path, 'w') as f:
            f.write(f'#!/bin/bash\ncd "{install_dir}"\npython3 run_gui.py\n')
        
        # Rendre exécutable
        os.chmod(command_path, 0o755)
        print(f"✅ Raccourci créé: {command_path}")
        
    else:  # Linux
        desktop = os.path.expanduser("~/Desktop")
        desktop_file = os.path.join(desktop, f"{app_name}.desktop")
        
        desktop_content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name={app_name}
Comment=Traitement automatique de commandes matelas
Exec={install_dir}/run_gui.py
Icon={install_dir}/icon.png
Terminal=false
Categories=Office;
"""
        
        with open(desktop_file, 'w') as f:
            f.write(desktop_content)
        
        os.chmod(desktop_file, 0o755)
        print(f"✅ Raccourci créé: {desktop_file}")

def install_dependencies():
    """Installe les dépendances Python"""
    print("📦 Installation des dépendances...")
    
    requirements_file = "requirements_gui.txt"
    if os.path.exists(requirements_file):
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_file], 
                         check=True, capture_output=True, text=True)
            print("✅ Dépendances installées avec succès")
        except subprocess.CalledProcessError as e:
            print(f"❌ Erreur lors de l'installation des dépendances: {e}")
            return False
    else:
        print("⚠️  Fichier requirements_gui.txt non trouvé")
    
    return True

def install_application():
    """Installe l'application"""
    print("=== Installation de Matelas Processor ===")
    
    # Déterminer le répertoire d'installation
    install_dir = get_install_dir()
    print(f"📁 Répertoire d'installation: {install_dir}")
    
    # Créer le répertoire d'installation
    try:
        os.makedirs(install_dir, exist_ok=True)
        print("✅ Répertoire d'installation créé")
    except Exception as e:
        print(f"❌ Erreur lors de la création du répertoire: {e}")
        return False
    
    # Copier les fichiers
    files_to_copy = [
        "run_gui.py",
        "backend_interface.py", 
        "config.py",
        "requirements_gui.txt",
        "README_GUI.md"
    ]
    
    dirs_to_copy = [
        "backend",
        "template"
    ]
    
    print("📋 Copie des fichiers...")
    
    # Copier les fichiers individuels
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, install_dir)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} non trouvé")
    
    # Copier les répertoires
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            dest_dir = os.path.join(install_dir, dir_name)
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            shutil.copytree(dir_name, dest_dir)
            print(f"  ✅ {dir_name}/")
        else:
            print(f"  ⚠️  {dir_name}/ non trouvé")
    
    # Créer un script de lancement
    launcher_content = f"""#!/usr/bin/env python3
import os
import sys

# Ajouter le répertoire d'installation au path
install_dir = "{install_dir}"
sys.path.insert(0, install_dir)

# Changer vers le répertoire d'installation
os.chdir(install_dir)

# Importer et lancer l'application
from run_gui import main
main()
"""
    
    launcher_path = os.path.join(install_dir, "launcher.py")
    with open(launcher_path, 'w', encoding='utf-8') as f:
        f.write(launcher_content)
    
    print("✅ Script de lancement créé")
    
    # Créer un raccourci sur le bureau
    create_desktop_shortcut(install_dir, "Matelas Processor")
    
    # Créer un fichier de configuration d'environnement
    env_file = os.path.join(install_dir, ".env")
    with open(env_file, 'w') as f:
        f.write(f"MATELAS_INSTALL_DIR={install_dir}\n")
        f.write("MATELAS_VERSION=1.0.0\n")
    
    print("✅ Fichier de configuration créé")
    
    # Créer un README d'installation
    readme_content = f"""# Matelas Processor - Installation

## Informations d'installation

- **Répertoire d'installation**: {install_dir}
- **Version**: 1.0.0
- **Python requis**: 3.8+

## Utilisation

1. Double-cliquez sur le raccourci "Matelas Processor" sur votre bureau
2. Ou lancez manuellement: `python3 {os.path.join(install_dir, 'run_gui.py')}`

## Désinstallation

Pour désinstaller, supprimez simplement le répertoire: {install_dir}

## Support

Pour toute question, contactez l'équipe de développement.
"""
    
    readme_path = os.path.join(install_dir, "README_INSTALL.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print("✅ README d'installation créé")
    
    print(f"\n🎉 Installation terminée avec succès!")
    print(f"📁 Application installée dans: {install_dir}")
    print(f"🖥️  Raccourci créé sur le bureau")
    print(f"📖 Consultez {readme_path} pour plus d'informations")
    
    return True

def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "--deps-only":
        # Installation des dépendances uniquement
        install_dependencies()
    else:
        # Installation complète
        if install_dependencies():
            install_application()
        else:
            print("❌ Échec de l'installation des dépendances")
            sys.exit(1)

if __name__ == "__main__":
    main() 