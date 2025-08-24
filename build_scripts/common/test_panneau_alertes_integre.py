#!/usr/bin/env python3
"""
Script de test pour vérifier l'intégration du panneau d'alertes dans la fenêtre principale
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget
from PyQt6.QtCore import QTimer

# Import de l'application principale
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_panneau_alertes_integre():
    """Test de l'intégration du panneau d'alertes"""
    print("🧪 Test de l'intégration du panneau d'alertes")
    
    app = QApplication(sys.argv)
    
    try:
        # Importer et créer l'application principale
        from app_gui import MatelasApp
        
        # Créer l'application
        main_app = MatelasApp()
        main_app.show()
        
        print("✅ Application créée avec succès")
        
        # Vérifier que le panneau d'alertes est intégré
        if hasattr(main_app, 'alert_panel'):
            print("✅ Panneau d'alertes trouvé dans l'application")
            
            # Vérifier la position du panneau
            alert_panel = main_app.alert_panel
            print(f"   - Position: {alert_panel.geometry()}")
            print(f"   - Visible: {alert_panel.isVisible()}")
            print(f"   - Hauteur max: {alert_panel.maximumHeight()}")
            print(f"   - Hauteur min: {alert_panel.minimumHeight()}")
            
            # Vérifier que le panneau est dans le bon conteneur
            parent = alert_panel.parent()
            if parent:
                print(f"   - Parent: {parent.__class__.__name__}")
            else:
                print("   - ⚠️ Pas de parent trouvé")
                
        else:
            print("❌ Panneau d'alertes non trouvé dans l'application")
        
        # Vérifier le système d'alertes
        if hasattr(main_app, 'alert_system'):
            print("✅ Système d'alertes trouvé")
            
            # Ajouter quelques alertes de test
            def ajouter_alertes_test():
                print("📢 Ajout d'alertes de test...")
                
                # Alerte de test
                main_app.add_system_alert(
                    "Test d'intégration",
                    "Le panneau d'alertes est maintenant intégré dans la fenêtre principale",
                    main_app.alert_system.AlertType.SUCCESS
                )
                
                # Alerte d'avertissement
                main_app.add_processing_alert(
                    "Traitement en cours",
                    "Test du panneau d'alertes intégré",
                    main_app.alert_system.AlertType.INFO,
                    "Test"
                )
                
                print("✅ Alertes de test ajoutées")
            
            # Ajouter les alertes après un délai
            QTimer.singleShot(2000, ajouter_alertes_test)
            
        else:
            print("❌ Système d'alertes non trouvé")
        
        # Afficher les informations de l'interface
        print("\n📊 Informations de l'interface:")
        print(f"   - Fenêtre principale: {main_app.geometry()}")
        print(f"   - Titre: {main_app.windowTitle()}")
        
        # Vérifier les onglets
        if hasattr(main_app, 'tabs'):
            print(f"   - Nombre d'onglets: {main_app.tabs.count()}")
            for i in range(main_app.tabs.count()):
                tab_text = main_app.tabs.tabText(i)
                print(f"     Onglet {i}: {tab_text}")
        
        print("\n🎉 Test d'intégration terminé!")
        print("Le panneau d'alertes devrait maintenant être visible sous l'espace de visualisation")
        
        # Fermer l'application après 10 secondes
        QTimer.singleShot(10000, app.quit)
        
        return app.exec()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return 1

if __name__ == "__main__":
    test_panneau_alertes_integre() 