#!/usr/bin/env python3
"""
Script de test pour vérifier le bouton Quitter avec validation
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QMessageBox
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bouton_quitter():
    """Test du bouton Quitter avec validation"""
    print("🧪 Test du bouton Quitter avec validation")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le bouton '🚪 Quitter l'application' doit être visible dans le panneau de gauche")
        print("   2. Cliquer sur le bouton doit afficher une confirmation")
        print("   3. Le menu Fichier → Quitter doit aussi afficher la confirmation")
        print("   4. La fermeture de la fenêtre (X) doit aussi demander confirmation")
        print("   5. Si un traitement est en cours, une alerte supplémentaire doit s'afficher")
        
        # Timer pour afficher les instructions après 2 secondes
        def show_instructions():
            print("\n🎯 Test en cours...")
            print("   - Cliquez sur le bouton '🚪 Quitter l'application'")
            print("   - Ou utilisez le menu Fichier → Quitter")
            print("   - Ou fermez la fenêtre avec le bouton X")
            print("   - Vérifiez que les confirmations s'affichent correctement")
        
        QTimer.singleShot(2000, show_instructions)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        print("💡 Assurez-vous que app_gui.py est dans le même répertoire")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        return False

if __name__ == "__main__":
    test_bouton_quitter() 