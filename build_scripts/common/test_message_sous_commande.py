#!/usr/bin/env python3
"""
Script de test pour vérifier que le message informatif apparaît sous le groupe Commande client
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_message_sous_commande():
    """Test du positionnement du message informatif"""
    print("🧪 Test du positionnement du message informatif")
    
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
        print("   3. Vérifiez que le message informatif apparaît SOUS le groupe 'Commande client'")
        print("   4. Vérifiez que le message ne se superpose pas avec les champs de saisie")
        print("   5. Vérifiez que l'ascenseur fonctionne correctement")
        print("")
        print("🎯 Test en cours...")
        print("   - Sélectionnez plusieurs fichiers pour tester")
        print("   - Vérifiez le positionnement du message")
        print("   - Testez l'ascenseur")
        
        # Timer pour afficher des informations supplémentaires
        def show_info():
            print("")
            print("📊 Comportement attendu :")
            print("   - Message sous le groupe 'Commande client'")
            print("   - Pas de superposition avec les champs")
            print("   - Ascenseur fonctionnel")
            print("   - Interface claire et organisée")
            print("")
            print("🔧 Fonctionnalités testées :")
            print("   - Positionnement correct du message")
            print("   - Nettoyage des anciens messages")
            print("   - Interface non encombrée")
            print("   - Navigation fluide")
        
        QTimer.singleShot(3000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_message_sous_commande() 