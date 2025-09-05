#!/usr/bin/env python3
"""
Script de désinstallation pour l'application Matelas
"""

import os
import sys
import shutil
import platform
from pathlib import Path

def get_install_dir():
    """Détermine le répertoire d'installation selon l'OS"""
    system = platform.system()
    
    if system == "Windows":
        program_files = os.environ.get('PROGRAMFILES', 'C:\\Program Files')
        return os.path.join(program_files, "MatelasProcessor")
    elif system == "Darwin":  # macOS
        return "/Applications/MatelasProcessor"
    else:  # Linux
        return "/opt/matelas-processor"

def remove_desktop_shortcut():
    """Supprime le raccourci sur le bureau"""
    system = platform.system()
    
    if system == "Windows":
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_files = [
            "Matelas Processor.bat",
            "Matelas Processor.lnk"
        ]
        
        for shortcut in shortcut_files:
            shortcut_path = os.path.join(desktop, shortcut)
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    print(f"✅ Raccourci supprimé: {shortcut}")
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {shortcut}: {e}")
                    
    elif system == "Darwin":  # macOS
        desktop = os.path.expanduser("~/Desktop")
        shortcut_files = [
            "Matelas Processor.command"
        ]
        
        for shortcut in shortcut_files:
            shortcut_path = os.path.join(desktop, shortcut)
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    print(f"✅ Raccourci supprimé: {shortcut}")
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {shortcut}: {e}")
                    
    else:  # Linux
        desktop = os.path.expanduser("~/Desktop")
        shortcut_files = [
            "Matelas Processor.desktop"
        ]
        
        for shortcut in shortcut_files:
            shortcut_path = os.path.join(desktop, shortcut)
            if os.path.exists(shortcut_path):
                try:
                    os.remove(shortcut_path)
                    print(f"✅ Raccourci supprimé: {shortcut}")
                except Exception as e:
                    print(f"⚠️  Impossible de supprimer {shortcut}: {e}")

def uninstall_application():
    """Désinstalle l'application"""
    print("=== Désinstallation de Matelas Processor ===")
    
    # Déterminer le répertoire d'installation
    install_dir = get_install_dir()
    print(f"📁 Répertoire d'installation: {install_dir}")
    
    # Supprimer le raccourci sur le bureau
    print("🗑️  Suppression des raccourcis...")
    remove_desktop_shortcut()
    
    # Supprimer le répertoire d'installation
    if os.path.exists(install_dir):
        try:
            shutil.rmtree(install_dir)
            print(f"✅ Répertoire d'installation supprimé: {install_dir}")
        except Exception as e:
            print(f"❌ Erreur lors de la suppression: {e}")
            print("💡 Vous devrez supprimer manuellement le répertoire")
            return False
    else:
        print(f"⚠️  Répertoire d'installation non trouvé: {install_dir}")
    
    # Supprimer les fichiers de cache potentiels
    cache_dirs = [
        os.path.expanduser("~/.matelas_processor"),
        os.path.expanduser("~/Library/Caches/MatelasProcessor"),  # macOS
        os.path.expanduser("~/.cache/matelas-processor")  # Linux
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"✅ Cache supprimé: {cache_dir}")
            except Exception as e:
                print(f"⚠️  Impossible de supprimer le cache {cache_dir}: {e}")
    
    print(f"\n🎉 Désinstallation terminée!")
    print("📝 Note: Les dépendances Python ne sont pas supprimées automatiquement")
    print("💡 Pour supprimer les dépendances, exécutez:")
    print("   pip uninstall -r requirements_gui.txt")
    
    return True

def check_installation():
    """Vérifie si l'application est installée"""
    install_dir = get_install_dir()
    
    if os.path.exists(install_dir):
        print(f"✅ Application trouvée dans: {install_dir}")
        return True
    else:
        print(f"❌ Application non trouvée dans: {install_dir}")
        return False

def main():
    """Fonction principale"""
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Vérification uniquement
        check_installation()
    else:
        # Désinstallation complète
        if check_installation():
            response = input("\n⚠️  Êtes-vous sûr de vouloir désinstaller Matelas Processor? (o/N): ")
            if response.lower() in ['o', 'oui', 'y', 'yes']:
                uninstall_application()
            else:
                print("❌ Désinstallation annulée")
        else:
            print("❌ Aucune installation trouvée à désinstaller")

if __name__ == "__main__":
    main() 