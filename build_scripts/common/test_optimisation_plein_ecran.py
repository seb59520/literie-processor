#!/usr/bin/env python3
"""
Script de test pour vérifier l'optimisation plein écran de la colonne de gauche
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_optimisation_plein_ecran():
    """Test de l'optimisation plein écran"""
    print("🧪 Test de l'optimisation plein écran")
    
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
        print("   2. En plein écran (≥1400px), la colonne gauche doit avoir 40% de l'espace")
        print("   3. En fenêtre moyenne (1200-1400px), la colonne gauche doit avoir 35% de l'espace")
        print("   4. En petite fenêtre (<1200px), la colonne gauche doit avoir 30% de l'espace")
        print("   5. Les éléments doivent s'adapter avec des polices et espacements optimisés")
        print("")
        print("🎯 Test en cours...")
        print("   - Testez le redimensionnement de la fenêtre")
        print("   - Vérifiez que la colonne gauche s'adapte intelligemment")
        print("   - Contrôlez que les polices et espacements sont optimisés")
        print("")
        print("📊 Comportement attendu :")
        print("   ✅ Plein écran (≥1400px) → 40% gauche, polices grandes, espacements généreux")
        print("   ✅ Fenêtre moyenne (1200-1400px) → 35% gauche, polices moyennes")
        print("   ✅ Petite fenêtre (<1200px) → 30% gauche, polices petites")
        print("   ✅ Largeur minimale panneau gauche : 400px en plein écran")
        print("   ✅ Largeur maximale panneau gauche : 600px en plein écran")
        
        # Timer pour afficher les informations après 2 secondes
        def show_info():
            print("")
            print("🔍 Informations de debug :")
            print("   - Vérifiez que la colonne gauche utilise mieux l'espace en plein écran")
            print("   - Les polices doivent être plus grandes en plein écran")
            print("   - Les espacements doivent être plus généreux en plein écran")
            print("   - Le panneau gauche doit avoir une largeur minimale de 400px en plein écran")
            print("")
            print("✅ Test terminé - Vérifiez manuellement l'optimisation plein écran")
        
        QTimer.singleShot(2000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_optimisation_plein_ecran() 