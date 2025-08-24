#!/usr/bin/env python3
"""
Script de test pour vérifier les tooltips des champs semaine et année
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_tooltips_semaine_annee():
    """Test des tooltips des champs semaine et année"""
    print("🧪 Test des tooltips des champs semaine et année")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Le texte explicatif sous l'année doit avoir disparu")
        print("   2. Survolez le champ 'Semaine actuelle' avec la souris")
        print("   3. Un tooltip doit s'afficher avec l'explication")
        print("   4. Survolez le champ 'Année actuelle' avec la souris")
        print("   5. Un tooltip doit s'afficher avec l'explication")
        print("   6. L'interface doit être plus compacte sans le texte")
        
        print("🎯 Test en cours...")
        print("   - Vérifiez que l'espace est gagné (pas de texte explicatif)")
        print("   - Testez les tooltips en survolant les champs")
        print("   - Vérifiez que les tooltips contiennent les bonnes explications")
        
        # Attendre que l'utilisateur ferme l'application
        app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_tooltips_semaine_annee() 