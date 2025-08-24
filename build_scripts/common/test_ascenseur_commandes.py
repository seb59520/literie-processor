#!/usr/bin/env python3
"""
Script de test pour vérifier l'ascenseur des commandes client
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ascenseur_commandes():
    """Test de l'ascenseur des commandes client"""
    print("🧪 Test de l'ascenseur des commandes client")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Cliquez sur 'Sélectionner des fichiers'")
        print("   2. Sélectionnez 4 fichiers PDF ou plus")
        print("   3. Vérifiez que seules 3 commandes client sont visibles")
        print("   4. Vérifiez qu'un ascenseur apparaît à droite")
        print("   5. Utilisez l'ascenseur pour voir les autres commandes")
        print("   6. Vérifiez que le message informatif s'affiche")
        print("")
        print("🎯 Test en cours...")
        print("   - Sélectionnez plusieurs fichiers pour tester l'ascenseur")
        print("   - Vérifiez que l'interface reste compacte")
        print("   - Testez le défilement avec l'ascenseur")
        
        # Timer pour afficher des informations supplémentaires
        def show_info():
            print("")
            print("📊 Comportement attendu :")
            print("   - Maximum 3 commandes visibles à la fois")
            print("   - Ascenseur vertical si plus de 3 fichiers")
            print("   - Message informatif sous l'ascenseur")
            print("   - Interface compacte et organisée")
            print("")
            print("🔧 Fonctionnalités testées :")
            print("   - Limitation d'affichage à 3 commandes")
            print("   - Ascenseur fonctionnel")
            print("   - Message informatif")
            print("   - Hauteur adaptative")
        
        QTimer.singleShot(3000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ascenseur_commandes() 