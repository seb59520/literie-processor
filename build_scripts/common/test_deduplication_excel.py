#!/usr/bin/env python3
"""
Script de test pour vérifier la déduplication des fichiers Excel
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_deduplication_excel():
    """Test de la déduplication des fichiers Excel"""
    print("🧪 Test de la déduplication des fichiers Excel")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Sélectionnez plusieurs fichiers PDF")
        print("   2. Lancez le traitement")
        print("   3. Vérifiez que dans le résumé, chaque fichier Excel n'apparaît qu'une seule fois")
        print("   4. Vérifiez que le compteur affiche 'X uniques' au lieu de 'X total'")
        print("   5. Vérifiez que les fichiers sont triés par ordre alphabétique")
        
        print("🎯 Test en cours...")
        print("   - Traitez plusieurs PDF qui génèrent le même fichier Excel")
        print("   - Vérifiez que les doublons sont éliminés dans l'affichage")
        print("   - Vérifiez que les liens fonctionnent toujours correctement")
        
        # Attendre que l'utilisateur ferme l'application
        app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_deduplication_excel() 