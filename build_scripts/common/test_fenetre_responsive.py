#!/usr/bin/env python3
"""
Script de test pour vérifier que la fenêtre s'adapte automatiquement à la taille de l'écran
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QSizePolicy
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_fenetre_responsive():
    """Test de l'adaptation automatique de la taille de fenêtre"""
    print("🧪 Test de l'adaptation automatique de la taille de fenêtre")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. La fenêtre doit s'adapter automatiquement à votre écran")
        print("   2. La fenêtre doit être centrée sur l'écran")
        print("   3. Le bouton '🚪 Quitter l'application' doit être visible")
        print("   4. La barre de statut en bas doit être visible")
        print("   5. Vous devez pouvoir redimensionner la fenêtre")
        print("   6. Les proportions du splitter doivent s'ajuster automatiquement")
        
        print("🎯 Test en cours...")
        print("   - Vérifiez que toute l'interface est visible")
        print("   - Essayez de redimensionner la fenêtre")
        print("   - Vérifiez que le bouton Quitter est accessible")
        print("   - Vérifiez que la barre de statut est visible")
        
        # Timer pour afficher les informations de taille après 2 secondes
        def show_size_info():
            screen = app.primaryScreen()
            screen_geometry = screen.geometry()
            window_geometry = main_app.geometry()
            
            print(f"\n📏 Informations de taille :")
            print(f"   Écran : {screen_geometry.width()}x{screen_geometry.height()}")
            print(f"   Fenêtre : {window_geometry.width()}x{window_geometry.height()}")
            print(f"   Position : ({window_geometry.x()}, {window_geometry.y()})")
            print(f"   Taille minimale : {main_app.minimumSize().width()}x{main_app.minimumSize().height()}")
            print(f"   Taille maximale : {main_app.maximumSize().width()}x{main_app.maximumSize().height()}")
            
            # Vérifier si la fenêtre est bien visible
            if (window_geometry.x() >= 0 and 
                window_geometry.y() >= 0 and 
                window_geometry.right() <= screen_geometry.width() and 
                window_geometry.bottom() <= screen_geometry.height()):
                print("✅ Fenêtre entièrement visible sur l'écran")
            else:
                print("⚠️  Fenêtre partiellement hors écran")
        
        QTimer.singleShot(2000, show_size_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_fenetre_responsive() 