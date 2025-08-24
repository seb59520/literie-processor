#!/usr/bin/env python3
"""
Script de test spécifique pour la taille de fenêtre 1220x800
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_1220x800():
    """Test spécifique pour la taille 1220x800"""
    print("🧪 Test spécifique pour la taille 1220x800")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        
        # Forcer la taille à 1220x800
        main_app.resize(1220, 800)
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Configuration spécifique :")
        print("   - Taille forcée : 1220x800")
        print("   - Catégorie : Petite fenêtre optimisée")
        print("   - Titre : 13px")
        print("   - Boutons : 10px")
        print("   - Labels : 9px")
        print("   - Logo : 55px")
        print("   - Espacements : 4px")
        print("   - Hauteur boutons : 25px")
        print("   - Titres groupes : 10px")
        
        print("🎯 Test en cours...")
        print("   - Vérifiez que tous les éléments sont visibles")
        print("   - Vérifiez que les polices sont lisibles")
        print("   - Vérifiez que le bouton Quitter est accessible")
        print("   - Vérifiez que la barre de statut est visible")
        print("   - Vérifiez que les groupes sont bien espacés")
        
        # Timer pour afficher les informations après 2 secondes
        def show_specific_info():
            window_width = main_app.width()
            window_height = main_app.height()
            
            print(f"\n📏 Informations spécifiques 1220x800 :")
            print(f"   Largeur actuelle : {window_width}px")
            print(f"   Hauteur actuelle : {window_height}px")
            
            # Vérifier la catégorie selon les nouveaux seuils
            if window_width < 1200:
                category = "Très petite fenêtre"
                expected_font = "Très petite (12px)"
            elif window_width < 1250:
                category = "Petite fenêtre optimisée (1220x800)"
                expected_font = "Petite optimisée (13px)"
            elif window_width < 1400:
                category = "Fenêtre moyenne-petite"
                expected_font = "Moyenne-petite (14px)"
            elif window_width < 1600:
                category = "Fenêtre moyenne"
                expected_font = "Moyenne (16px)"
            else:
                category = "Grande fenêtre"
                expected_font = "Grande (18px)"
            
            print(f"   Catégorie détectée : {category}")
            print(f"   Taille de police attendue : {expected_font}")
            
            # Vérifier la hauteur du logo
            if window_width < 1200:
                expected_logo = "50px"
            elif window_width < 1250:
                expected_logo = "55px"
            elif window_width < 1400:
                expected_logo = "65px"
            elif window_width < 1600:
                expected_logo = "80px"
            else:
                expected_logo = "100px"
            
            print(f"   Hauteur du logo attendue : {expected_logo}")
            
            # Vérifier les espacements
            if window_height < 750:
                expected_spacing = "Très réduit (3px)"
            elif window_height < 800:
                expected_spacing = "Réduit optimisé (4px)"
            elif window_height < 850:
                expected_spacing = "Moyen (6px)"
            else:
                expected_spacing = "Standard (8px)"
            
            print(f"   Espacements attendus : {expected_spacing}")
            
            # Vérifier la hauteur des boutons
            button_height = "25px" if window_height < 800 else "30px"
            print(f"   Hauteur des boutons : {button_height}")
            
            print("\n🔍 Vérifications spécifiques pour 1220x800 :")
            print("   - Le titre 'Configuration' doit être lisible (13px)")
            print("   - Le bouton '🚪 Quitter l'application' doit être visible")
            print("   - Les groupes doivent avoir des titres lisibles (10px)")
            print("   - Les boutons doivent avoir une hauteur appropriée (25px)")
            print("   - Les espacements doivent être optimisés (4px)")
            print("   - La barre de statut doit être visible en bas")
            print("   - Le panneau d'alertes doit être accessible")
            
            # Vérifier si la fenêtre est entièrement visible
            screen = app.primaryScreen()
            screen_geometry = screen.geometry()
            window_geometry = main_app.geometry()
            
            if (window_geometry.x() >= 0 and 
                window_geometry.y() >= 0 and
                window_geometry.right() <= screen_geometry.width() and
                window_geometry.bottom() <= screen_geometry.height()):
                print("✅ Fenêtre entièrement visible sur l'écran")
            else:
                print("⚠️  Fenêtre partiellement hors écran")
        
        QTimer.singleShot(2000, show_specific_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_1220x800() 