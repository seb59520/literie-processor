#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de lancement rapide pour l'intégration Notion avec Cursor
"""

import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    try:
        import requests
        return True
    except ImportError:
        return False

def install_dependencies():
    """Installe les dépendances manquantes"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_notion.txt"])
        print("✅ Dépendances installées avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

def check_config():
    """Vérifie que la configuration Notion existe"""
    config_path = Path("notion_config.json")
    if not config_path.exists():
        print("⚠️  Configuration Notion manquante.")
        print("Lancement du script de configuration...")
        return False
    return True

def launch_setup():
    """Lance le script de configuration"""
    try:
        subprocess.run([sys.executable, "setup_notion_integration.py"])
        return True
    except Exception as e:
        print(f"❌ Erreur lancement configuration: {e}")
        return False

def launch_gui():
    """Lance l'interface graphique"""
    try:
        subprocess.run([sys.executable, "notion_manager_gui.py"])
        return True
    except Exception as e:
        print(f"❌ Erreur lancement interface: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Lancement de l'intégration Notion avec Cursor")
    print("=" * 50)
    
    # Vérifier les dépendances
    if not check_dependencies():
        print("❌ Dépendances manquantes.")
        if not install_dependencies():
            print("Impossible d'installer les dépendances. Arrêt.")
            return
    
    # Vérifier la configuration
    if not check_config():
        if not launch_setup():
            print("Impossible de lancer la configuration. Arrêt.")
            return
        
        # Vérifier à nouveau après configuration
        if not check_config():
            print("Configuration incomplète. Arrêt.")
            return
    
    print("✅ Configuration vérifiée.")
    print("🎯 Lancement de l'interface graphique...")
    
    # Lancer l'interface
    if not launch_gui():
        print("❌ Impossible de lancer l'interface graphique.")
        print("Vous pouvez essayer de lancer manuellement:")
        print("  python notion_manager_gui.py")

if __name__ == "__main__":
    main()


