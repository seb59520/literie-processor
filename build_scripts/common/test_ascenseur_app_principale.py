#!/usr/bin/env python3
"""
Script de test pour vérifier l'ascenseur dans l'application principale
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_ascenseur_app_principale():
    """Test de l'ascenseur dans l'application principale"""
    print("🧪 Test de l'ascenseur dans l'application principale")
    
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
        print("   3. Vérifiez que l'ascenseur apparaît dans le groupe 'Commande client'")
        print("   4. Vérifiez que vous pouvez faire défiler pour voir tous les champs")
        print("   5. Vérifiez que le message informatif apparaît sous le groupe")
        print("")
        print("🎯 Test en cours...")
        print("   - Sélectionnez plusieurs fichiers pour tester")
        print("   - Vérifiez que l'ascenseur fonctionne")
        print("   - Testez le défilement")
        print("   - Vérifiez le positionnement du message")
        
        # Timer pour afficher des informations supplémentaires
        def show_info():
            print("")
            print("📊 Comportement attendu :")
            print("   - Ascenseur visible quand plus de 3 fichiers")
            print("   - Défilement fluide")
            print("   - Message sous le groupe commande client")
            print("   - Interface claire et organisée")
            print("")
            print("🔧 Paramètres ajustés :")
            print("   - Hauteur maximale : 105px (3 lignes)")
            print("   - Ascenseur forcé si > 3 fichiers")
            print("   - Message positionné correctement")
            print("   - Nettoyage automatique des anciens messages")
        
        QTimer.singleShot(3000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_ascenseur_app_principale() 