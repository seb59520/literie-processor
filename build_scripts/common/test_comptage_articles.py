#!/usr/bin/env python3
"""
Script de test pour vérifier que le comptage des articles est correct
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_comptage_articles():
    """Test du comptage correct des articles"""
    print("🧪 Test du comptage correct des articles")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Sélectionnez un fichier PDF de commande")
        print("   2. Vérifiez que le comptage des articles est correct")
        print("   3. Le système doit compter uniquement les lignes commençant par 'Matelas' ou 'Sommier'")
        print("   4. Les autres articles ne doivent pas être comptés")
        print("")
        print("🎯 Test en cours...")
        print("   - Sélectionnez un fichier de commande")
        print("   - Vérifiez les recommandations de production")
        print("   - Le nombre d'articles doit correspondre à la réalité")
        print("")
        print("📊 Exemple de comptage correct :")
        print("   - Si la commande contient 1 ligne 'Matelas' → 1 matelas")
        print("   - Si la commande contient 1 ligne 'Sommier' → 1 sommier")
        print("   - Si la commande contient 2 lignes 'Matelas' → 2 matelas")
        print("   - Les autres articles (oreillers, couettes, etc.) ne sont pas comptés")
        
        # Timer pour afficher les informations après 2 secondes
        def show_info():
            print("")
            print("🔍 Informations de debug :")
            print("   - Vérifiez les logs pour voir le comptage détaillé")
            print("   - Le message 'Analyse texte: Matelas=X(Y), Sommiers=Z(W)' doit être visible")
            print("   - X et Z sont les booléens (True/False)")
            print("   - Y et W sont les compteurs exacts")
            print("")
            print("✅ Test terminé - Vérifiez manuellement le comptage")
        
        QTimer.singleShot(2000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_comptage_articles() 