#!/usr/bin/env python3
"""
Script de lancement pour l'application graphique de traitement de devis matelas
"""

import sys
import os

# Ajout du répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def main():
    """Lance l'application graphique"""
    try:
        from app_gui import main as gui_main
        gui_main()
    except ImportError as e:
        print(f"Erreur d'import: {e}")
        print("Assurez-vous d'avoir installé PyQt6: pip install PyQt6")
        sys.exit(1)
    except Exception as e:
        print(f"Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 