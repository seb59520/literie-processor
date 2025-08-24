#!/usr/bin/env python3
"""
Script de test pour vérifier que les éléments internes s'adaptent correctement à la taille de la fenêtre
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QSizePolicy
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_elements_responsive():
    """Test de l'adaptation des éléments internes"""
    print("🧪 Test de l'adaptation des éléments internes")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Les éléments doivent s'adapter automatiquement à la taille de la fenêtre")
        print("   2. Les polices doivent changer de taille selon la largeur de la fenêtre")
        print("   3. Le logo doit se redimensionner automatiquement")
        print("   4. Les espacements doivent s'ajuster selon la hauteur")
        print("   5. Le bouton Quitter doit rester visible et accessible")
        print("   6. La barre de statut doit rester visible")
        
        print("🎯 Test en cours...")
        print("   - Redimensionnez la fenêtre pour voir les changements")
        print("   - Vérifiez que les polices s'adaptent")
        print("   - Vérifiez que le logo se redimensionne")
        print("   - Vérifiez que tous les éléments restent visibles")
        
        # Timer pour afficher les informations après 2 secondes
        def show_element_info():
            window_width = main_app.width()
            window_height = main_app.height()
            
            print(f"\n📏 Informations des éléments :")
            print(f"   Largeur fenêtre : {window_width}px")
            print(f"   Hauteur fenêtre : {window_height}px")
            
            # Vérifier les tailles de police selon la largeur
            if window_width < 1300:
                expected_font = "Petite (10-14px)"
            elif window_width < 1600:
                expected_font = "Moyenne (11-16px)"
            else:
                expected_font = "Grande (12-18px)"
            
            print(f"   Taille de police attendue : {expected_font}")
            
            # Vérifier la hauteur du logo selon la largeur
            if window_width < 1300:
                expected_logo = "60px"
            elif window_width < 1600:
                expected_logo = "80px"
            else:
                expected_logo = "100px"
            
            print(f"   Hauteur du logo attendue : {expected_logo}")
            
            # Vérifier les espacements selon la hauteur
            if window_height < 800:
                expected_spacing = "Réduit (5px)"
            else:
                expected_spacing = "Standard (8-10px)"
            
            print(f"   Espacements attendus : {expected_spacing}")
            
            print("\n🔍 Vérifications à effectuer :")
            print("   - Le titre 'Configuration' doit être lisible")
            print("   - Le bouton '🚪 Quitter l'application' doit être visible")
            print("   - Les groupes doivent être bien espacés")
            print("   - La barre de statut doit être visible en bas")
            print("   - Le panneau d'alertes doit être accessible")
        
        QTimer.singleShot(2000, show_element_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_elements_responsive() 