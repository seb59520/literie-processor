#!/usr/bin/env python3
"""
Script de test pour vérifier la modernisation de la partie des paramètres de production
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_parametres_production_modernes():
    """Test de la modernisation de la partie des paramètres de production"""
    print("🧪 Test de la modernisation des paramètres de production")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le groupe '📅 Paramètres de production' doit avoir un style moderne")
        print("   2. La semaine et l'année doivent être sur la même ligne")
        print("   3. Les labels doivent avoir des icônes (📆 et 📅)")
        print("   4. Les champs de saisie doivent avoir un style amélioré")
        print("   5. Les tooltips doivent être fonctionnels")
        print("   6. L'interface doit être plus compacte et moderne")
        
        print("\n🎯 Test en cours...")
        print("   - Vérifiez que le groupe a un style moderne avec bordures")
        print("   - Vérifiez que semaine et année sont sur la même ligne")
        print("   - Testez les champs de saisie (cliquez, utilisez les flèches)")
        print("   - Survolez les champs pour voir les tooltips")
        print("   - Vérifiez que les valeurs par défaut sont correctes")
        
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
    sys.exit(test_parametres_production_modernes()) 