#!/usr/bin/env python3
"""
Script de test pour vérifier que la croix rouge en haut à droite fonctionne correctement
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_croix_rouge():
    """Test de la croix rouge en haut à droite"""
    print("🧪 Test de la croix rouge en haut à droite")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. La croix rouge (✕) doit être visible en haut à droite de la fenêtre")
        print("   2. La croix doit être rouge avec un effet hover")
        print("   3. Cliquer sur la croix doit afficher une confirmation de fermeture")
        print("   4. Le bouton 'Quitter' ne doit plus être présent dans la colonne de gauche")
        print("   5. L'espace libéré dans la colonne de gauche doit être utilisé pour les autres éléments")
        print("🎯 Test en cours...")
        print("   - Vérifiez que la croix rouge est visible en haut à droite")
        print("   - Cliquez sur la croix rouge pour tester la fermeture")
        print("   - Vérifiez que la colonne de gauche a plus d'espace")
        
        # Attendre 2 secondes puis afficher les informations
        def print_info():
            print("📏 Informations de la croix rouge :")
            print(f"   Position : ({main_app.width() - 35}, 5)")
            print(f"   Taille : 24x24 pixels")
            print(f"   Couleur : Rouge (#e74c3c)")
            print(f"   Tooltip : 'Fermer l'application'")
            print("✅ Test terminé - Vérifiez manuellement le comportement")
        
        QTimer.singleShot(2000, print_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_croix_rouge() 