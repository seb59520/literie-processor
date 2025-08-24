#!/usr/bin/env python3
"""
Script de test pour vérifier le compactage de la partie des paramètres de production
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_compactage_parametres_production():
    """Test du compactage de la partie des paramètres de production"""
    print("🧪 Test du compactage des paramètres de production")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le groupe '📅 Paramètres de production' doit être plus compact")
        print("   2. Les espaces haut et bas doivent être réduits")
        print("   3. La semaine et l'année doivent être sur la même ligne")
        print("   4. Les champs de saisie doivent être plus compacts")
        print("   5. L'espacement entre les éléments doit être optimisé")
        print("   6. L'interface doit prendre moins de place verticale")
        
        print("\n🎯 Test en cours...")
        print("   - Vérifiez que le groupe est plus compact")
        print("   - Vérifiez que les espaces sont réduits")
        print("   - Testez les champs de saisie (cliquez, utilisez les flèches)")
        print("   - Survolez les champs pour voir les tooltips")
        print("   - Vérifiez que l'interface prend moins de place")
        
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
    sys.exit(test_compactage_parametres_production()) 