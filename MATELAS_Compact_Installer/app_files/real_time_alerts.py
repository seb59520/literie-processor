#!/usr/bin/env python3
"""
Système d'alertes en temps réel pour l'application Literie Processor
"""

import sys
import os
import json
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from enum import Enum

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QDialog, QSystemTrayIcon, QMenu, QSlider, QCheckBox,
    QGroupBox, QFormLayout, QSpinBox, QComboBox
)
from PyQt6.QtCore import Qt, QObject, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette, QIcon, QAction
import webbrowser


# Enum pour les types d'alertes
class AlertType(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"
    CRITICAL = "critical"


# Enum pour les catégories d'alertes
class AlertCategory(Enum):
    SYSTEM = "system"
    PROCESSING = "processing"
    VALIDATION = "validation"
    NETWORK = "network"
    SECURITY = "security"
    PRODUCTION = "production"


class Alert:
    """Classe représentant une alerte"""
    
    def __init__(self, title: str, message: str, alert_type: AlertType, 
                 category: AlertCategory, source: str = "", data: Dict = None,
                 auto_dismiss: bool = True, dismiss_timeout: int = 5000):
        self.id = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        self.title = title
        self.message = message
        self.alert_type = alert_type
        self.category = category
        self.source = source
        self.data = data or {}
        self.timestamp = datetime.now()
        self.auto_dismiss = auto_dismiss
        self.dismiss_timeout = dismiss_timeout
        self.is_dismissed = False
        self.is_read = False
        
    def to_dict(self):
        """Convertit l'alerte en dictionnaire pour sérialisation"""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'alert_type': self.alert_type.value,
            'category': self.category.value,
            'source': self.source,
            'data': self.data,
            'timestamp': self.timestamp.isoformat(),
            'auto_dismiss': self.auto_dismiss,
            'dismiss_timeout': self.dismiss_timeout,
            'is_dismissed': self.is_dismissed,
            'is_read': self.is_read
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        """Crée une alerte à partir d'un dictionnaire"""
        alert = cls(
            title=data['title'],
            message=data['message'],
            alert_type=AlertType(data['alert_type']),
            category=AlertCategory(data['category']),
            source=data.get('source', ''),
            data=data.get('data', {}),
            auto_dismiss=data.get('auto_dismiss', True),
            dismiss_timeout=data.get('dismiss_timeout', 5000)
        )
        alert.id = data['id']
        alert.timestamp = datetime.fromisoformat(data['timestamp'])
        alert.is_dismissed = data.get('is_dismissed', False)
        alert.is_read = data.get('is_read', False)
        return alert


class RealTimeAlertSystem(QObject):
    """Système d'alertes en temps réel"""
    
    # Signaux pour les alertes
    alert_added = pyqtSignal(Alert)
    alert_updated = pyqtSignal(Alert)
    alert_dismissed = pyqtSignal(str)  # alert_id
    alert_read = pyqtSignal(str)  # alert_id
    alert_count_changed = pyqtSignal(int)  # nombre d'alertes non lues
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.alerts: List[Alert] = []
        self.max_alerts = 100  # Nombre maximum d'alertes conservées
        self.alert_timers: Dict[str, QTimer] = {}
        
        # Configuration des alertes par défaut
        self.alert_config = {
            AlertType.INFO: {'timeout': 3000, 'sound': False, 'notification': False},
            AlertType.WARNING: {'timeout': 5000, 'sound': True, 'notification': True},
            AlertType.ERROR: {'timeout': 8000, 'sound': True, 'notification': True},
            AlertType.SUCCESS: {'timeout': 3000, 'sound': False, 'notification': False},
            AlertType.CRITICAL: {'timeout': 0, 'sound': True, 'notification': True}  # Pas d'auto-dismiss
        }
        
        # Timer pour nettoyer les anciennes alertes
        self.cleanup_timer = QTimer()
        self.cleanup_timer.timeout.connect(self._cleanup_old_alerts)
        self.cleanup_timer.start(60000)  # Nettoyage toutes les minutes
        
        self.logger = logging.getLogger("AlertSystem")
    
    def add_alert(self, title: str, message: str, alert_type: AlertType = AlertType.INFO,
                  category: AlertCategory = AlertCategory.SYSTEM, source: str = "",
                  data: Dict = None, auto_dismiss: bool = None, dismiss_timeout: int = None):
        """Ajoute une nouvelle alerte"""
        try:
            # Configuration par défaut selon le type
            config = self.alert_config.get(alert_type, {})
            if auto_dismiss is None:
                auto_dismiss = alert_type != AlertType.CRITICAL
            if dismiss_timeout is None:
                dismiss_timeout = config.get('timeout', 5000)
            
            alert = Alert(
                title=title,
                message=message,
                alert_type=alert_type,
                category=category,
                source=source,
                data=data or {},
                auto_dismiss=auto_dismiss,
                dismiss_timeout=dismiss_timeout
            )
            
            # Ajouter l'alerte à la liste
            self.alerts.append(alert)
            
            # Limiter le nombre d'alertes
            if len(self.alerts) > self.max_alerts:
                self.alerts.pop(0)
            
            # Configurer l'auto-dismiss si activé
            if alert.auto_dismiss and alert.dismiss_timeout > 0:
                timer = QTimer()
                timer.setSingleShot(True)
                timer.timeout.connect(lambda: self.dismiss_alert(alert.id))
                timer.start(alert.dismiss_timeout)
                self.alert_timers[alert.id] = timer
            
            # Émettre les signaux
            self.alert_added.emit(alert)
            self.alert_count_changed.emit(self.get_unread_count())
            
            # Log de l'alerte
            self.logger.info(f"Alerte ajoutée: {alert_type.value} - {title}")
            
            return alert
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'ajout d'alerte: {e}")
            return None
    
    def dismiss_alert(self, alert_id: str):
        """Marque une alerte comme fermée"""
        try:
            alert = self.get_alert_by_id(alert_id)
            if alert and not alert.is_dismissed:
                alert.is_dismissed = True
                
                # Arrêter le timer si il existe
                if alert_id in self.alert_timers:
                    self.alert_timers[alert_id].stop()
                    del self.alert_timers[alert_id]
                
                self.alert_dismissed.emit(alert_id)
                self.alert_count_changed.emit(self.get_unread_count())
                
                self.logger.debug(f"Alerte fermée: {alert_id}")
                
        except Exception as e:
            self.logger.error(f"Erreur lors de la fermeture d'alerte: {e}")
    
    def mark_alert_read(self, alert_id: str):
        """Marque une alerte comme lue"""
        try:
            alert = self.get_alert_by_id(alert_id)
            if alert and not alert.is_read:
                alert.is_read = True
                self.alert_read.emit(alert_id)
                self.alert_count_changed.emit(self.get_unread_count())
                
        except Exception as e:
            self.logger.error(f"Erreur lors du marquage d'alerte comme lue: {e}")
    
    def get_alert_by_id(self, alert_id: str) -> Optional[Alert]:
        """Récupère une alerte par son ID"""
        for alert in self.alerts:
            if alert.id == alert_id:
                return alert
        return None
    
    def get_active_alerts(self, include_dismissed: bool = False) -> List[Alert]:
        """Récupère les alertes actives (non fermées)"""
        if include_dismissed:
            return self.alerts
        return [alert for alert in self.alerts if not alert.is_dismissed]
    
    def get_alerts_by_type(self, alert_type: AlertType) -> List[Alert]:
        """Récupère les alertes par type"""
        return [alert for alert in self.alerts if alert.alert_type == alert_type]
    
    def get_alerts_by_category(self, category: AlertCategory) -> List[Alert]:
        """Récupère les alertes par catégorie"""
        return [alert for alert in self.alerts if alert.category == category]
    
    def get_unread_count(self) -> int:
        """Récupère le nombre d'alertes non lues"""
        return len([alert for alert in self.alerts if not alert.is_read and not alert.is_dismissed])
    
    def get_critical_count(self) -> int:
        """Récupère le nombre d'alertes critiques"""
        return len([alert for alert in self.alerts 
                   if alert.alert_type == AlertType.CRITICAL and not alert.is_dismissed])
    
    def clear_all_alerts(self):
        """Efface toutes les alertes"""
        try:
            # Arrêter tous les timers
            for timer in self.alert_timers.values():
                timer.stop()
            self.alert_timers.clear()
            
            # Effacer les alertes
            self.alerts.clear()
            self.alert_count_changed.emit(0)
            
            self.logger.info("Toutes les alertes ont été effacées")
            
        except Exception as e:
            self.logger.error(f"Erreur lors de l'effacement des alertes: {e}")
    
    def _cleanup_old_alerts(self):
        """Nettoie les anciennes alertes (plus de 24h)"""
        try:
            cutoff_time = datetime.now() - timedelta(hours=24)
            initial_count = len(self.alerts)
            
            # Garder seulement les alertes récentes ou critiques
            self.alerts = [alert for alert in self.alerts 
                          if alert.timestamp > cutoff_time or 
                          alert.alert_type == AlertType.CRITICAL]
            
            if len(self.alerts) < initial_count:
                self.logger.debug(f"Nettoyage: {initial_count - len(self.alerts)} alertes supprimées")
                
        except Exception as e:
            self.logger.error(f"Erreur lors du nettoyage des alertes: {e}")


class AlertWidget(QWidget):
    """Widget pour afficher une alerte individuelle"""
    
    def __init__(self, alert: Alert, parent=None):
        super().__init__(parent)
        self.alert = alert
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Icône selon le type d'alerte
        icon_label = QLabel()
        icon_map = {
            AlertType.INFO: "ℹ️",
            AlertType.WARNING: "⚠️",
            AlertType.ERROR: "❌",
            AlertType.SUCCESS: "✅",
            AlertType.CRITICAL: "🚨"
        }
        icon_label.setText(icon_map.get(self.alert.alert_type, "ℹ️"))
        icon_label.setFixedSize(24, 24)
        layout.addWidget(icon_label)
        
        # Contenu de l'alerte
        content_layout = QVBoxLayout()
        
        # Titre
        title_label = QLabel(self.alert.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        content_layout.addWidget(title_label)
        
        # Message
        message_label = QLabel(self.alert.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 11px; color: #666;")
        content_layout.addWidget(message_label)
        
        # Horodatage
        time_label = QLabel(self.alert.timestamp.strftime("%H:%M:%S"))
        time_label.setStyleSheet("font-size: 10px; color: #999;")
        content_layout.addWidget(time_label)
        
        layout.addLayout(content_layout)
        layout.addStretch()
        
        # Bouton de fermeture
        close_btn = QPushButton("×")
        close_btn.setFixedSize(20, 20)
        close_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                font-weight: bold;
                color: #999;
            }
            QPushButton:hover {
                color: #666;
            }
        """)
        close_btn.clicked.connect(self.dismiss_alert)
        layout.addWidget(close_btn)
        
        # Style selon le type d'alerte
        self.set_alert_style()
    
    def set_alert_style(self):
        """Applique le style selon le type d'alerte"""
        base_style = """
            QWidget {
                border: 1px solid #ddd;
                border-radius: 6px;
                padding: 4px;
                margin: 2px;
            }
        """
        
        type_styles = {
            AlertType.INFO: "background-color: #e3f2fd; border-color: #2196f3;",
            AlertType.WARNING: "background-color: #fff3e0; border-color: #ff9800;",
            AlertType.ERROR: "background-color: #ffebee; border-color: #f44336;",
            AlertType.SUCCESS: "background-color: #e8f5e8; border-color: #4caf50;",
            AlertType.CRITICAL: "background-color: #ffebee; border-color: #d32f2f; border-width: 2px;"
        }
        
        style = base_style + type_styles.get(self.alert.alert_type, "")
        self.setStyleSheet(style)
    
    def dismiss_alert(self):
        """Ferme l'alerte"""
        if hasattr(self.parent(), 'dismiss_alert'):
            self.parent().dismiss_alert(self.alert.id)


class AlertPanel(QWidget):
    """Panneau d'affichage des alertes"""
    
    def __init__(self, alert_system: RealTimeAlertSystem, parent=None):
        super().__init__(parent)
        self.alert_system = alert_system
        self.alert_widgets: Dict[str, AlertWidget] = {}
        self.init_ui()
        self.connect_signals()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # En-tête
        header_layout = QHBoxLayout()
        
        title_label = QLabel("Alertes en temps réel")
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Bouton pour effacer toutes les alertes
        clear_btn = QPushButton("Effacer tout")
        clear_btn.setStyleSheet("""
            QPushButton {
                background: #f44336;
                color: white;
                border: none;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 11px;
            }
            QPushButton:hover {
                background: #d32f2f;
            }
        """)
        clear_btn.clicked.connect(self.clear_all_alerts)
        header_layout.addWidget(clear_btn)
        
        layout.addLayout(header_layout)
        
        # Zone de défilement pour les alertes
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Widget conteneur pour les alertes
        self.alerts_container = QWidget()
        self.alerts_layout = QVBoxLayout(self.alerts_container)
        self.alerts_layout.setContentsMargins(0, 0, 0, 0)
        self.alerts_layout.addStretch()  # Espaceur en bas
        
        self.scroll_area.setWidget(self.alerts_container)
        layout.addWidget(self.scroll_area)
        
        # Message si aucune alerte
        self.no_alerts_label = QLabel("Aucune alerte active")
        self.no_alerts_label.setStyleSheet("color: #999; font-style: italic; text-align: center;")
        self.no_alerts_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.no_alerts_label)
        
        # Initialiser l'affichage
        self.update_display()
    
    def connect_signals(self):
        """Connecte les signaux du système d'alertes"""
        self.alert_system.alert_added.connect(self.add_alert_widget)
        self.alert_system.alert_dismissed.connect(self.remove_alert_widget)
        self.alert_system.alert_count_changed.connect(self.update_display)
    
    def add_alert_widget(self, alert: Alert):
        """Ajoute un widget d'alerte"""
        try:
            # Créer le widget d'alerte
            alert_widget = AlertWidget(alert, self)
            self.alert_widgets[alert.id] = alert_widget
            
            # Insérer avant l'espaceur
            self.alerts_layout.insertWidget(self.alerts_layout.count() - 1, alert_widget)
            
            # Animation d'apparition
            alert_widget.setMaximumHeight(0)
            animation = QPropertyAnimation(alert_widget, b"maximumHeight")
            animation.setDuration(300)
            animation.setStartValue(0)
            animation.setEndValue(alert_widget.sizeHint().height())
            animation.setEasingCurve(QEasingCurve.Type.OutCubic)
            animation.start()
            
            self.update_display()
            
        except Exception as e:
            print(f"Erreur lors de l'ajout du widget d'alerte: {e}")
    
    def remove_alert_widget(self, alert_id: str):
        """Supprime un widget d'alerte"""
        try:
            if alert_id in self.alert_widgets:
                widget = self.alert_widgets[alert_id]
                
                # Animation de disparition
                animation = QPropertyAnimation(widget, b"maximumHeight")
                animation.setDuration(200)
                animation.setStartValue(widget.height())
                animation.setEndValue(0)
                animation.setEasingCurve(QEasingCurve.Type.InCubic)
                animation.finished.connect(lambda: self._remove_widget_complete(alert_id))
                animation.start()
                
        except Exception as e:
            print(f"Erreur lors de la suppression du widget d'alerte: {e}")
    
    def _remove_widget_complete(self, alert_id: str):
        """Termine la suppression du widget d'alerte"""
        try:
            if alert_id in self.alert_widgets:
                widget = self.alert_widgets[alert_id]
                self.alerts_layout.removeWidget(widget)
                widget.deleteLater()
                del self.alert_widgets[alert_id]
                self.update_display()
                
        except Exception as e:
            print(f"Erreur lors de la suppression complète du widget: {e}")
    
    def update_display(self):
        """Met à jour l'affichage du panneau"""
        active_count = len([w for w in self.alert_widgets.values() if not w.alert.is_dismissed])
        
        # Afficher/masquer le message "aucune alerte"
        self.no_alerts_label.setVisible(active_count == 0)
        
        # Ajuster la hauteur du panneau
        if active_count > 0:
            self.setMaximumHeight(300)
        else:
            self.setMaximumHeight(100)
    
    def clear_all_alerts(self):
        """Efface toutes les alertes"""
        self.alert_system.clear_all_alerts()
    
    def dismiss_alert(self, alert_id: str):
        """Ferme une alerte spécifique"""
        self.alert_system.dismiss_alert(alert_id)


class AlertNotificationDialog(QDialog):
    """Dialog de notification d'alerte"""
    
    def __init__(self, alert: Alert, parent=None):
        super().__init__(parent)
        self.alert = alert
        self.init_ui()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle(f"Alerte - {self.alert.title}")
        self.setModal(False)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        
        layout = QVBoxLayout(self)
        
        # En-tête avec icône
        header_layout = QHBoxLayout()
        
        icon_label = QLabel()
        icon_map = {
            AlertType.INFO: "ℹ️",
            AlertType.WARNING: "⚠️",
            AlertType.ERROR: "❌",
            AlertType.SUCCESS: "✅",
            AlertType.CRITICAL: "🚨"
        }
        icon_label.setText(icon_map.get(self.alert.alert_type, "ℹ️"))
        icon_label.setFixedSize(32, 32)
        header_layout.addWidget(icon_label)
        
        title_label = QLabel(self.alert.title)
        title_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        header_layout.addWidget(title_label)
        
        layout.addLayout(header_layout)
        
        # Message
        message_label = QLabel(self.alert.message)
        message_label.setWordWrap(True)
        message_label.setStyleSheet("font-size: 12px; margin: 10px 0;")
        layout.addWidget(message_label)
        
        # Horodatage
        time_label = QLabel(f"Reçu le {self.alert.timestamp.strftime('%d/%m/%Y à %H:%M:%S')}")
        time_label.setStyleSheet("font-size: 10px; color: #999;")
        layout.addWidget(time_label)
        
        # Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        if self.alert.data.get('action_url'):
            action_btn = QPushButton("Voir détails")
            action_btn.clicked.connect(self.open_action_url)
            button_layout.addWidget(action_btn)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Style selon le type d'alerte
        self.set_alert_style()
        
        # Auto-fermeture pour les alertes non critiques
        if self.alert.alert_type != AlertType.CRITICAL and self.alert.auto_dismiss:
            QTimer.singleShot(self.alert.dismiss_timeout, self.accept)
    
    def set_alert_style(self):
        """Applique le style selon le type d'alerte"""
        type_styles = {
            AlertType.INFO: "background-color: #e3f2fd;",
            AlertType.WARNING: "background-color: #fff3e0;",
            AlertType.ERROR: "background-color: #ffebee;",
            AlertType.SUCCESS: "background-color: #e8f5e8;",
            AlertType.CRITICAL: "background-color: #ffebee; border: 2px solid #d32f2f;"
        }
        
        self.setStyleSheet(type_styles.get(self.alert.alert_type, ""))
    
    def open_action_url(self):
        """Ouvre l'URL d'action si définie"""
        url = self.alert.data.get('action_url')
        if url:
            webbrowser.open(url)
        self.accept()


class AlertSettingsDialog(QDialog):
    """Dialog de configuration des alertes"""
    
    def __init__(self, alert_system: RealTimeAlertSystem, parent=None):
        super().__init__(parent)
        self.alert_system = alert_system
        self.init_ui()
        self.load_settings()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Configuration des alertes")
        self.setModal(True)
        self.resize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Configuration générale
        general_group = QGroupBox("Configuration générale")
        general_layout = QFormLayout()
        
        self.enable_notifications = QCheckBox("Activer les notifications")
        general_layout.addRow("Notifications:", self.enable_notifications)
        
        self.enable_sounds = QCheckBox("Activer les sons")
        general_layout.addRow("Sons:", self.enable_sounds)
        
        self.max_alerts = QSpinBox()
        self.max_alerts.setRange(10, 500)
        self.max_alerts.setValue(100)
        general_layout.addRow("Max alertes:", self.max_alerts)
        
        general_group.setLayout(general_layout)
        layout.addWidget(general_group)
        
        # Configuration par type d'alerte
        types_group = QGroupBox("Configuration par type")
        types_layout = QFormLayout()
        
        self.type_timeouts = {}
        for alert_type in AlertType:
            timeout_spin = QSpinBox()
            timeout_spin.setRange(0, 30000)
            timeout_spin.setSuffix(" ms")
            timeout_spin.setValue(self.alert_system.alert_config.get(alert_type, {}).get('timeout', 5000))
            self.type_timeouts[alert_type] = timeout_spin
            types_layout.addRow(f"{alert_type.value.title()}:", timeout_spin)
        
        types_group.setLayout(types_layout)
        layout.addWidget(types_group)
        
        # Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        reset_btn = QPushButton("Réinitialiser")
        reset_btn.clicked.connect(self.reset_settings)
        button_layout.addWidget(reset_btn)
        
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """Charge les paramètres actuels"""
        # Charger depuis un fichier de configuration si disponible
        # Pour l'instant, utiliser les valeurs par défaut
        pass
    
    def save_settings(self):
        """Sauvegarde les paramètres"""
        try:
            # Mettre à jour la configuration du système d'alertes
            self.alert_system.max_alerts = self.max_alerts.value()
            
            for alert_type, timeout_spin in self.type_timeouts.items():
                if alert_type not in self.alert_system.alert_config:
                    self.alert_system.alert_config[alert_type] = {}
                self.alert_system.alert_config[alert_type]['timeout'] = timeout_spin.value()
            
            # Sauvegarder dans un fichier de configuration
            # TODO: Implémenter la sauvegarde
            
            self.accept()
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des paramètres: {e}")
    
    def reset_settings(self):
        """Réinitialise les paramètres par défaut"""
        self.max_alerts.setValue(100)
        
        default_timeouts = {
            AlertType.INFO: 3000,
            AlertType.WARNING: 5000,
            AlertType.ERROR: 8000,
            AlertType.SUCCESS: 3000,
            AlertType.CRITICAL: 0
        }
        
        for alert_type, timeout in default_timeouts.items():
            if alert_type in self.type_timeouts:
                self.type_timeouts[alert_type].setValue(timeout)


# Fonctions utilitaires pour créer des alertes spécifiques
def create_system_alert(title: str, message: str, alert_type: AlertType = AlertType.INFO):
    """Crée une alerte système"""
    return Alert(title, message, alert_type, AlertCategory.SYSTEM, "Système")


def create_processing_alert(title: str, message: str, alert_type: AlertType = AlertType.INFO, source: str = ""):
    """Crée une alerte de traitement"""
    return Alert(title, message, alert_type, AlertCategory.PROCESSING, source)


def create_validation_alert(title: str, message: str, alert_type: AlertType = AlertType.WARNING, source: str = ""):
    """Crée une alerte de validation"""
    return Alert(title, message, alert_type, AlertCategory.VALIDATION, source)


def create_network_alert(title: str, message: str, alert_type: AlertType = AlertType.ERROR):
    """Crée une alerte réseau"""
    return Alert(title, message, alert_type, AlertCategory.NETWORK, "Réseau")


def create_security_alert(title: str, message: str, alert_type: AlertType = AlertType.CRITICAL):
    """Crée une alerte de sécurité"""
    return Alert(title, message, alert_type, AlertCategory.SECURITY, "Sécurité")


def create_production_alert(title: str, message: str, alert_type: AlertType = AlertType.INFO, source: str = ""):
    """Crée une alerte de production"""
    return Alert(title, message, alert_type, AlertCategory.PRODUCTION, source) 