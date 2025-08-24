#!/usr/bin/env python3
"""
Script de test pour vérifier le centrage des paramètres de production et la suppression du titre
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_centrage_parametres_production():
    """Test du centrage des paramètres de production et suppression du titre"""
    print("🧪 Test du centrage des paramètres de production")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le groupe des paramètres de production ne doit plus avoir de titre")
        print("   2. Les boutons semaine et année doivent être centrés dans leur partie")
        print("   3. Les labels '📆 Semaine actuelle' et '📅 Année actuelle' doivent être centrés")
        print("   4. L'interface doit être plus allégée sans le titre")
        print("   5. Les champs de saisie doivent être centrés")
        print("   6. L'espacement doit être équilibré")
        
        print("\n🎯 Test en cours...")
        print("   - Vérifiez que le titre a été supprimé")
        print("   - Vérifiez que les éléments sont centrés")
        print("   - Testez les champs de saisie (cliquez, utilisez les flèches)")
        print("   - Survolez les champs pour voir les tooltips")
        print("   - Vérifiez que l'interface est plus compacte")
        
        # Timer pour fermer automatiquement après 30 secondes
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(30000)  # 30 secondes
        
        print("\n⏰ L'application se fermera automatiquement dans 30 secondes")
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_centrage_parametres_production()) 