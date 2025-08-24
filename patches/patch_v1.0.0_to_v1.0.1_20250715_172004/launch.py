#!/usr/bin/env python3
"""
Script de lancement rapide pour Matelas Processor
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Vérifie la version de Python"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ requis")
        print(f"   Version actuelle: {sys.version}")
        return False
    return True

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    required_packages = ['openpyxl', 'fitz', 'httpx']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Dépendances manquantes: {', '.join(missing)}")
        print("💡 Installez-les avec: pip install -r requirements_gui.txt")
        return False
    return True

def launch_application():
    """Lance l'application"""
    print("🚀 Lancement de Matelas Processor...")
    
    try:
        # Importer et lancer l'application
        from run_gui import main
        main()
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que tous les fichiers sont présents")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")
        return False
    
    return True

def main():
    """Fonction principale"""
    print("=== Matelas Processor - Lancement Rapide ===\n")
    
    # Vérifications préliminaires
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Lancement de l'application
    if not launch_application():
        sys.exit(1)

if __name__ == "__main__":
    main() 