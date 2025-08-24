#!/usr/bin/env python3
"""
Script de test pour vérifier le système d'alertes dans l'application
"""

import sys
import time
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Import du système d'alertes
from real_time_alerts import (
    RealTimeAlertSystem, AlertPanel, AlertType, AlertCategory,
    create_system_alert, create_processing_alert, create_validation_alert
)

def test_alertes_application():
    """Test du système d'alertes dans l'application"""
    print("🚀 Test du système d'alertes dans l'application")
    
    app = QApplication(sys.argv)
    
    # Créer le système d'alertes
    alert_system = RealTimeAlertSystem()
    
    # Créer le panneau d'alertes
    alert_panel = AlertPanel(alert_system)
    alert_panel.show()
    
    def ajouter_alertes_test():
        """Ajoute des alertes de test"""
        print("📢 Ajout d'alertes de test...")
        
        # Alerte système
        alert_system.add_alert(
            "Système d'alertes activé",
            "Le système d'alertes en temps réel est maintenant opérationnel",
            AlertType.SUCCESS,
            AlertCategory.SYSTEM
        )
        
        # Alerte de traitement
        alert_system.add_alert(
            "Début du traitement",
            "Démarrage du traitement de 3 fichiers PDF avec OpenAI",
            AlertType.INFO,
            AlertCategory.PROCESSING,
            "Interface"
        )
        
        # Alerte d'avertissement
        alert_system.add_alert(
            "Noyau non détecté",
            "Le noyau du matelas n'a pas pu être identifié automatiquement",
            AlertType.WARNING,
            AlertCategory.VALIDATION,
            "Analyse LLM"
        )
        
        # Alerte d'erreur
        alert_system.add_alert(
            "Erreur de connexion",
            "Impossible de se connecter au service LLM",
            AlertType.ERROR,
            AlertCategory.NETWORK
        )
        
        # Alerte critique
        alert_system.add_alert(
            "Espace disque faible",
            "L'espace disque disponible est inférieur à 1 GB",
            AlertType.CRITICAL,
            AlertCategory.SYSTEM
        )
        
        print("✅ Alertes de test ajoutées")
    
    def afficher_statistiques():
        """Affiche les statistiques des alertes"""
        print("\n📊 Statistiques du système d'alertes:")
        print(f"   - Alertes totales: {len(alert_system.alerts)}")
        print(f"   - Alertes actives: {len(alert_system.get_active_alerts())}")
        print(f"   - Alertes non lues: {alert_system.get_unread_count()}")
        print(f"   - Alertes critiques: {alert_system.get_critical_count()}")
        
        # Afficher les alertes par type
        for alert_type in AlertType:
            count = len(alert_system.get_alerts_by_type(alert_type))
            if count > 0:
                print(f"   - {alert_type.value.title()}: {count}")
        
        print("\n🎉 Test terminé avec succès!")
        print("L'application va se fermer dans 3 secondes...")
    
    # Ajouter les alertes après 1 seconde
    QTimer.singleShot(1000, ajouter_alertes_test)
    
    # Afficher les statistiques après 3 secondes
    QTimer.singleShot(3000, afficher_statistiques)
    
    # Fermer l'application après 6 secondes
    QTimer.singleShot(6000, app.quit)
    
    return app.exec()

if __name__ == "__main__":
    test_alertes_application() 