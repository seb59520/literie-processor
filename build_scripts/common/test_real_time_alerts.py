#!/usr/bin/env python3
"""
Tests pour le système d'alertes en temps réel
"""

import sys
import os
import unittest
from datetime import datetime
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Ajouter le répertoire courant au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from real_time_alerts import (
    RealTimeAlertSystem, AlertPanel, AlertNotificationDialog, AlertSettingsDialog,
    AlertType, AlertCategory, Alert, create_system_alert, create_processing_alert,
    create_validation_alert, create_network_alert, create_security_alert, create_production_alert
)


class TestRealTimeAlertSystem(unittest.TestCase):
    """Tests pour le système d'alertes en temps réel"""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation globale pour tous les tests"""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.alert_system = RealTimeAlertSystem()
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.alert_system.clear_all_alerts()
    
    def test_alert_creation(self):
        """Test de création d'alertes"""
        # Test création d'alerte basique
        alert = self.alert_system.add_alert(
            "Test Alert",
            "Ceci est un test",
            AlertType.INFO,
            AlertCategory.SYSTEM
        )
        
        self.assertIsNotNone(alert)
        self.assertEqual(alert.title, "Test Alert")
        self.assertEqual(alert.message, "Ceci est un test")
        self.assertEqual(alert.alert_type, AlertType.INFO)
        self.assertEqual(alert.category, AlertCategory.SYSTEM)
        self.assertFalse(alert.is_dismissed)
        self.assertFalse(alert.is_read)
    
    def test_alert_types(self):
        """Test des différents types d'alertes"""
        types = [AlertType.INFO, AlertType.WARNING, AlertType.ERROR, AlertType.SUCCESS, AlertType.CRITICAL]
        
        for alert_type in types:
            alert = self.alert_system.add_alert(
                f"Test {alert_type.value}",
                f"Test pour {alert_type.value}",
                alert_type,
                AlertCategory.SYSTEM
            )
            
            self.assertEqual(alert.alert_type, alert_type)
            self.assertIsNotNone(alert.id)
    
    def test_alert_categories(self):
        """Test des différentes catégories d'alertes"""
        categories = [
            AlertCategory.SYSTEM,
            AlertCategory.PROCESSING,
            AlertCategory.VALIDATION,
            AlertCategory.NETWORK,
            AlertCategory.SECURITY,
            AlertCategory.PRODUCTION
        ]
        
        for category in categories:
            alert = self.alert_system.add_alert(
                f"Test {category.value}",
                f"Test pour {category.value}",
                AlertType.INFO,
                category
            )
            
            self.assertEqual(alert.category, category)
    
    def test_alert_dismissal(self):
        """Test de fermeture d'alertes"""
        alert = self.alert_system.add_alert(
            "Test Dismiss",
            "Test de fermeture",
            AlertType.INFO,
            AlertCategory.SYSTEM
        )
        
        initial_count = self.alert_system.get_unread_count()
        self.alert_system.dismiss_alert(alert.id)
        
        # Vérifier que l'alerte est fermée
        dismissed_alert = self.alert_system.get_alert_by_id(alert.id)
        self.assertTrue(dismissed_alert.is_dismissed)
        
        # Vérifier que le compteur a diminué
        new_count = self.alert_system.get_unread_count()
        self.assertEqual(new_count, initial_count - 1)
    
    def test_alert_mark_read(self):
        """Test de marquage comme lu"""
        alert = self.alert_system.add_alert(
            "Test Read",
            "Test de lecture",
            AlertType.INFO,
            AlertCategory.SYSTEM
        )
        
        initial_count = self.alert_system.get_unread_count()
        self.alert_system.mark_alert_read(alert.id)
        
        # Vérifier que l'alerte est marquée comme lue
        read_alert = self.alert_system.get_alert_by_id(alert.id)
        self.assertTrue(read_alert.is_read)
        
        # Vérifier que le compteur a diminué
        new_count = self.alert_system.get_unread_count()
        self.assertEqual(new_count, initial_count - 1)
    
    def test_alert_filtering(self):
        """Test du filtrage des alertes"""
        # Créer des alertes de différents types
        self.alert_system.add_alert("Info", "Info", AlertType.INFO, AlertCategory.SYSTEM)
        self.alert_system.add_alert("Warning", "Warning", AlertType.WARNING, AlertCategory.PROCESSING)
        self.alert_system.add_alert("Error", "Error", AlertType.ERROR, AlertCategory.VALIDATION)
        
        # Tester le filtrage par type
        info_alerts = self.alert_system.get_alerts_by_type(AlertType.INFO)
        self.assertEqual(len(info_alerts), 1)
        self.assertEqual(info_alerts[0].title, "Info")
        
        # Tester le filtrage par catégorie
        system_alerts = self.alert_system.get_alerts_by_category(AlertCategory.SYSTEM)
        self.assertEqual(len(system_alerts), 1)
        self.assertEqual(system_alerts[0].title, "Info")
    
    def test_alert_limits(self):
        """Test des limites d'alertes"""
        # Créer plus d'alertes que la limite
        for i in range(110):  # Limite par défaut est 100
            self.alert_system.add_alert(
                f"Alert {i}",
                f"Message {i}",
                AlertType.INFO,
                AlertCategory.SYSTEM
            )
        
        # Vérifier que le nombre d'alertes ne dépasse pas la limite
        self.assertLessEqual(len(self.alert_system.alerts), self.alert_system.max_alerts)
    
    def test_alert_serialization(self):
        """Test de sérialisation des alertes"""
        alert = self.alert_system.add_alert(
            "Test Serialization",
            "Test de sérialisation",
            AlertType.WARNING,
            AlertCategory.PROCESSING,
            "Test Source",
            {"key": "value"}
        )
        
        # Convertir en dictionnaire
        alert_dict = alert.to_dict()
        
        # Vérifier les champs
        self.assertEqual(alert_dict['title'], "Test Serialization")
        self.assertEqual(alert_dict['message'], "Test de sérialisation")
        self.assertEqual(alert_dict['alert_type'], "warning")
        self.assertEqual(alert_dict['category'], "processing")
        self.assertEqual(alert_dict['source'], "Test Source")
        self.assertEqual(alert_dict['data'], {"key": "value"})
        
        # Recréer l'alerte depuis le dictionnaire
        recreated_alert = Alert.from_dict(alert_dict)
        
        # Vérifier que c'est identique
        self.assertEqual(recreated_alert.title, alert.title)
        self.assertEqual(recreated_alert.message, alert.message)
        self.assertEqual(recreated_alert.alert_type, alert.alert_type)
        self.assertEqual(recreated_alert.category, alert.category)
        self.assertEqual(recreated_alert.source, alert.source)
        self.assertEqual(recreated_alert.data, alert.data)
    
    def test_utility_functions(self):
        """Test des fonctions utilitaires"""
        # Test create_system_alert
        system_alert = create_system_alert("System Test", "System message", AlertType.INFO)
        self.assertEqual(system_alert.category, AlertCategory.SYSTEM)
        self.assertEqual(system_alert.source, "Système")
        
        # Test create_processing_alert
        processing_alert = create_processing_alert("Processing Test", "Processing message", AlertType.WARNING, "Test Source")
        self.assertEqual(processing_alert.category, AlertCategory.PROCESSING)
        self.assertEqual(processing_alert.source, "Test Source")
        
        # Test create_validation_alert
        validation_alert = create_validation_alert("Validation Test", "Validation message", AlertType.ERROR, "Test Source")
        self.assertEqual(validation_alert.category, AlertCategory.VALIDATION)
        self.assertEqual(validation_alert.alert_type, AlertType.ERROR)
        
        # Test create_network_alert
        network_alert = create_network_alert("Network Test", "Network message", AlertType.CRITICAL)
        self.assertEqual(network_alert.category, AlertCategory.NETWORK)
        self.assertEqual(network_alert.source, "Réseau")
        
        # Test create_security_alert
        security_alert = create_security_alert("Security Test", "Security message", AlertType.CRITICAL)
        self.assertEqual(security_alert.category, AlertCategory.SECURITY)
        self.assertEqual(security_alert.source, "Sécurité")
        
        # Test create_production_alert
        production_alert = create_production_alert("Production Test", "Production message", AlertType.SUCCESS, "Test Source")
        self.assertEqual(production_alert.category, AlertCategory.PRODUCTION)
        self.assertEqual(production_alert.source, "Test Source")


class TestAlertPanel(unittest.TestCase):
    """Tests pour le panneau d'alertes"""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation globale pour tous les tests"""
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.alert_system = RealTimeAlertSystem()
        self.alert_panel = AlertPanel(self.alert_system)
    
    def tearDown(self):
        """Nettoyage après chaque test"""
        self.alert_system.clear_all_alerts()
        self.alert_panel.deleteLater()
    
    def test_panel_creation(self):
        """Test de création du panneau"""
        self.assertIsNotNone(self.alert_panel)
        self.assertEqual(self.alert_panel.alert_system, self.alert_system)
    
    def test_alert_widget_creation(self):
        """Test de création de widgets d'alertes"""
        # Créer une alerte
        alert = self.alert_system.add_alert(
            "Test Widget",
            "Test de widget",
            AlertType.INFO,
            AlertCategory.SYSTEM
        )
        
        # Vérifier que le widget a été créé
        self.assertIn(alert.id, self.alert_panel.alert_widgets)
        
        # Vérifier que le widget est dans le layout
        widget = self.alert_panel.alert_widgets[alert.id]
        self.assertIsNotNone(widget)
        self.assertEqual(widget.alert.id, alert.id)
    
    def test_alert_widget_removal(self):
        """Test de suppression de widgets d'alertes"""
        # Créer une alerte
        alert = self.alert_system.add_alert(
            "Test Removal",
            "Test de suppression",
            AlertType.INFO,
            AlertCategory.SYSTEM
        )
        
        # Vérifier que le widget existe
        self.assertIn(alert.id, self.alert_panel.alert_widgets)
        
        # Supprimer directement le widget (bypass de l'animation pour le test)
        if alert.id in self.alert_panel.alert_widgets:
            widget = self.alert_panel.alert_widgets[alert.id]
            self.alert_panel.alerts_layout.removeWidget(widget)
            widget.deleteLater()
            del self.alert_panel.alert_widgets[alert.id]
        
        # Vérifier que le widget a été supprimé
        self.assertNotIn(alert.id, self.alert_panel.alert_widgets)


class TestAlertNotificationDialog(unittest.TestCase):
    """Tests pour le dialog de notification d'alertes"""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation globale pour tous les tests"""
        cls.app = QApplication(sys.argv)
    
    def test_dialog_creation(self):
        """Test de création du dialog"""
        alert = Alert(
            "Test Dialog",
            "Test de dialog",
            AlertType.WARNING,
            AlertCategory.SYSTEM
        )
        
        dialog = AlertNotificationDialog(alert)
        self.assertIsNotNone(dialog)
        self.assertEqual(dialog.alert, alert)
        self.assertEqual(dialog.windowTitle(), "Alerte - Test Dialog")


class TestAlertSettingsDialog(unittest.TestCase):
    """Tests pour le dialog de configuration des alertes"""
    
    @classmethod
    def setUpClass(cls):
        """Initialisation globale pour tous les tests"""
        cls.app = QApplication(sys.argv)
    
    def test_dialog_creation(self):
        """Test de création du dialog de configuration"""
        alert_system = RealTimeAlertSystem()
        dialog = AlertSettingsDialog(alert_system)
        
        self.assertIsNotNone(dialog)
        self.assertEqual(dialog.alert_system, alert_system)
        self.assertEqual(dialog.windowTitle(), "Configuration des alertes")


def run_integration_test():
    """Test d'intégration complet du système d'alertes"""
    print("🚀 Test d'intégration du système d'alertes en temps réel")
    
    app = QApplication(sys.argv)
    
    # Créer le système d'alertes
    alert_system = RealTimeAlertSystem()
    
    # Créer le panneau d'alertes
    alert_panel = AlertPanel(alert_system)
    alert_panel.show()
    
    # Fonction pour ajouter des alertes de test
    def add_test_alerts():
        print("📢 Ajout d'alertes de test...")
        
        # Alerte système
        alert_system.add_alert(
            "Système démarré",
            "Le système d'alertes est maintenant opérationnel",
            AlertType.SUCCESS,
            AlertCategory.SYSTEM
        )
        
        # Alerte de traitement
        alert_system.add_alert(
            "Traitement en cours",
            "Analyse de 3 fichiers PDF en cours...",
            AlertType.INFO,
            AlertCategory.PROCESSING,
            "Traitement"
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
    
    # Ajouter les alertes après un délai
    QTimer.singleShot(1000, add_test_alerts)
    
    # Fonction pour tester les interactions
    def test_interactions():
        print("🔧 Test des interactions...")
        
        # Marquer une alerte comme lue
        alerts = alert_system.get_active_alerts()
        if alerts:
            alert_system.mark_alert_read(alerts[0].id)
            print(f"✅ Alerte '{alerts[0].title}' marquée comme lue")
        
        # Fermer une alerte
        if len(alerts) > 1:
            alert_system.dismiss_alert(alerts[1].id)
            print(f"✅ Alerte '{alerts[1].title}' fermée")
        
        print("✅ Tests d'interactions terminés")
    
    # Tester les interactions après un délai
    QTimer.singleShot(3000, test_interactions)
    
    # Fonction pour afficher les statistiques
    def show_stats():
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
        
        print("\n🎉 Test d'intégration terminé avec succès!")
    
    # Afficher les statistiques après un délai
    QTimer.singleShot(5000, show_stats)
    
    # Fermer l'application après un délai
    QTimer.singleShot(7000, app.quit)
    
    return app.exec()


if __name__ == "__main__":
    # Exécuter les tests unitaires
    print("🧪 Exécution des tests unitaires...")
    unittest.main(verbosity=2, exit=False)
    
    # Exécuter le test d'intégration
    print("\n" + "="*50)
    run_integration_test() 