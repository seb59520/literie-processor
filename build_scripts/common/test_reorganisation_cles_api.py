#!/usr/bin/env python3
"""
Script de test pour vérifier la réorganisation de l'interface des clés API
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_reorganisation_cles_api():
    """Test de la réorganisation de l'interface des clés API"""
    print("🧪 Test de la réorganisation de l'interface des clés API")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le bouton d'aide '🔑' doit être plus visible (32x32px)")
        print("   2. Le groupe '🔐 Clé API (cliquez pour afficher)' doit être masqué par défaut")
        print("   3. Cliquer sur le groupe doit l'ouvrir et afficher les champs")
        print("   4. Le bouton '👁' pour afficher/masquer la clé doit être plus grand (35x35px)")
        print("   5. Le champ de saisie de clé API doit avoir un style amélioré")
        print("   6. Le bouton d'aide '🔑' doit afficher l'aide quand on clique dessus")
        
        print("\n🎯 Test en cours...")
        print("   - Vérifiez que le bouton d'aide '🔑' est bien visible")
        print("   - Vérifiez que le groupe clé API est masqué par défaut")
        print("   - Cliquez sur le groupe pour l'ouvrir")
        print("   - Testez le bouton d'aide '🔑'")
        print("   - Testez le bouton '👁' pour afficher/masquer la clé")
        
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
    sys.exit(test_reorganisation_cles_api()) 