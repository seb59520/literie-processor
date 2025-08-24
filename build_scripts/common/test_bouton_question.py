#!/usr/bin/env python3
"""
Script de test pour vérifier que le bouton "?" dans le groupe Enrichissement LLM fonctionne correctement
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_bouton_question():
    """Test du bouton "?" dans le groupe Enrichissement LLM"""
    print("🧪 Test du bouton '?' dans le groupe Enrichissement LLM")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le bouton '?' doit être visible à côté du sélecteur de Provider")
        print("   2. Le bouton doit être bleu et circulaire (24x24 pixels)")
        print("   3. Le bouton doit être plus compact que l'ancien '❓ Aide Clés API'")
        print("   4. Cliquer sur le bouton doit afficher l'aide pour les clés API")
        print("   5. L'espace dans le groupe Enrichissement LLM doit être optimisé")
        print("🎯 Test en cours...")
        print("   - Vérifiez que le bouton '?' est visible et bien positionné")
        print("   - Cliquez sur le bouton pour tester l'aide")
        print("   - Vérifiez que l'espace est mieux utilisé")
        
        # Attendre 2 secondes puis afficher les informations
        def print_info():
            print("📏 Informations du bouton '?' :")
            print("   Taille : 24x24 pixels")
            print("   Forme : Cercle parfait (border-radius: 12px)")
            print("   Couleur : Bleu (#3498db)")
            print("   Couleur hover : Bleu foncé (#2980b9)")
            print("   Position : À côté du sélecteur de Provider")
            print("   Fonction : Affiche l'aide pour les clés API")
            print("✅ Test terminé - Vérifiez manuellement le comportement")
        
        QTimer.singleShot(2000, print_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_bouton_question() 