#!/usr/bin/env python3
"""
Script de lancement pour l'application graphique avec debug complet
"""

import sys
import os
import traceback
import logging

# Configuration du logging pour debug
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('debug.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Ajout du répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Lance l'application graphique avec debug complet"""
    try:
        logger.info("Début du lancement de l'application")
        
        # Vérifier les imports critiques
        logger.info("Vérification des imports...")
        
        try:
            from PyQt6.QtWidgets import QApplication
            logger.info("OK: PyQt6.QtWidgets importé")
        except ImportError as e:
            logger.error(f"ERREUR: PyQt6 non disponible: {e}")
            print(f"ERREUR: PyQt6 non disponible: {e}")
            print("Installez PyQt6: pip install PyQt6")
            return 1
        
        try:
            from app_gui import main as gui_main
            logger.info("OK: app_gui importé")
        except ImportError as e:
            logger.error(f"ERREUR: app_gui non disponible: {e}")
            print(f"ERREUR: app_gui non disponible: {e}")
            return 1
        
        # Vérifier les modules backend
        logger.info("Vérification des modules backend...")
        try:
            import backend_interface
            logger.info("OK: backend_interface importé")
        except ImportError as e:
            logger.warning(f"WARNING: backend_interface non disponible: {e}")
        
        try:
            import config
            logger.info("OK: config importé")
        except ImportError as e:
            logger.warning(f"WARNING: config non disponible: {e}")
        
        # Vérifier les fichiers de données
        logger.info("Vérification des fichiers de données...")
        data_dirs = ['backend', 'assets', 'template', 'config', 'Référentiels']
        for dir_name in data_dirs:
            if os.path.exists(dir_name):
                logger.info(f"OK: Dossier {dir_name} trouvé")
            else:
                logger.warning(f"WARNING: Dossier {dir_name} manquant")
        
        # Lancement de l'application
        logger.info("Lancement de l'application graphique...")
        gui_main()
        logger.info("Application fermée normalement")
        return 0
        
    except Exception as e:
        error_msg = f"ERREUR CRITIQUE lors du lancement: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        
        print("=" * 60)
        print("ERREUR CRITIQUE")
        print("=" * 60)
        print(error_msg)
        print()
        print("Détails complets:")
        print(traceback.format_exc())
        print("=" * 60)
        print("Consultez le fichier debug.log pour plus de détails")
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    if exit_code != 0:
        print(f"\nApplication terminée avec erreur (code: {exit_code})")
        input("Appuyez sur Entrée pour fermer...")
    sys.exit(exit_code) 