#!/usr/bin/env python3
"""
Script de test pour vérifier que les recommandations sont plus précises
et correspondent à la réalité des commandes
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_recommandations_precises():
    """Test de la précision des recommandations"""
    print("🧪 Test de la précision des recommandations")
    
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
        print("   2. Vérifiez que l'analyse détecte correctement matelas/sommiers")
        print("   3. Les recommandations doivent correspondre au contenu réel")
        print("   4. Si l'analyse est incorrecte, vous pouvez la corriger manuellement")
        
        # Timer pour afficher les informations après 2 secondes
        def afficher_info():
            try:
                print(f"\n🎯 Test en cours...")
                print(f"   - Sélectionnez un fichier PDF de commande")
                print(f"   - Vérifiez que l'analyse est précise")
                print(f"   - Les recommandations doivent refléter la réalité")
                print(f"   - Si erreur, l'application ne fera plus d'hypothèses par défaut")
                
                print(f"\n🔧 Améliorations apportées :")
                print(f"   - Prompt LLM plus précis pour distinguer matelas/sommiers")
                print(f"   - Suppression des hypothèses par défaut")
                print(f"   - Analyse texte plus rigoureuse")
                print(f"   - Messages d'erreur plus clairs")
                
            except Exception as e:
                print(f"❌ Erreur lors de l'affichage des informations : {e}")
        
        # Programmer l'affichage des informations après 2 secondes
        QTimer.singleShot(2000, afficher_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du lancement de l'application : {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_recommandations_precises() 