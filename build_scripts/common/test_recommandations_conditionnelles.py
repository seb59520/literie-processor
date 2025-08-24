#!/usr/bin/env python3
"""
Script de test pour vérifier que les recommandations de production 
ne s'affichent que quand il y a des matelas ou des sommiers
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_recommandations_conditionnelles():
    """Test des recommandations conditionnelles"""
    print("🧪 Test des recommandations conditionnelles")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application lancée avec succès")
        print("📋 Instructions de test :")
        print("   1. Sélectionnez un fichier PDF avec des matelas ET des sommiers")
        print("   2. Vérifiez que les contrôles de semaine matelas ET sommiers s'affichent")
        print("   3. Sélectionnez un fichier PDF avec seulement des matelas")
        print("   4. Vérifiez que seul le contrôle semaine matelas s'affiche")
        print("   5. Sélectionnez un fichier PDF avec seulement des sommiers")
        print("   6. Vérifiez que seul le contrôle semaine sommiers s'affiche")
        print("   7. Sélectionnez un fichier PDF sans matelas ni sommiers")
        print("   8. Vérifiez qu'aucun contrôle de semaine ne s'affiche")
        print("")
        print("🎯 Test en cours...")
        print("   - Testez différents types de commandes")
        print("   - Vérifiez que l'interface s'adapte au contenu")
        print("   - Contrôlez que les messages d'information sont clairs")
        print("")
        print("📊 Comportement attendu :")
        print("   ✅ Matelas + Sommiers → Contrôles semaine matelas ET sommiers")
        print("   ✅ Matelas uniquement → Contrôle semaine matelas seulement")
        print("   ✅ Sommiers uniquement → Contrôle semaine sommiers seulement")
        print("   ✅ Aucun article → Message 'Aucune recommandation nécessaire'")
        
        # Timer pour afficher les informations après 2 secondes
        def show_info():
            print("")
            print("🔍 Informations de debug :")
            print("   - Vérifiez que les contrôles de semaine n'apparaissent que si nécessaire")
            print("   - Le message d'information doit être visible quand il n'y a pas d'articles")
            print("   - Les boutons d'action doivent rester fonctionnels")
            print("")
            print("✅ Test terminé - Vérifiez manuellement le comportement conditionnel")
        
        QTimer.singleShot(2000, show_info)
        
        # Lancer l'application
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur lors du test : {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    test_recommandations_conditionnelles() 