#!/usr/bin/env python3
"""
Interface de gestion des workflows pour l'application
"""

import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, 
    QTableWidgetItem, QLabel, QProgressBar, QTabWidget, QTextEdit,
    QHeaderView, QMessageBox, QDialog, QFormLayout, QSpinBox,
    QCheckBox, QListWidget, QListWidgetItem, QSplitter, QFrame,
    QScrollArea, QGroupBox, QComboBox, QDateTimeEdit, QLineEdit
)
from PyQt6.QtCore import QTimer, Qt, pyqtSignal, QThread, QDateTime
from PyQt6.QtGui import QFont, QColor, QPalette

try:
    from backend.workflow_engine import get_workflow_engine, WorkflowStatus
    from backend.batch_processor import get_batch_processor
    from backend.workflow_monitor import get_workflow_monitor
    WORKFLOW_AVAILABLE = True
except ImportError:
    WORKFLOW_AVAILABLE = False

class WorkflowManagerWidget(QWidget):
    """Widget de gestion des workflows"""
    
    workflow_created = pyqtSignal(str)  # workflow_id
    workflow_cancelled = pyqtSignal(str)  # workflow_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.workflow_engine = None
        self.batch_processor = None
        self.workflow_monitor = None
        
        if WORKFLOW_AVAILABLE:
            self.workflow_engine = get_workflow_engine()
            self.batch_processor = get_batch_processor()
            self.workflow_monitor = get_workflow_monitor(self.workflow_engine)
        
        self.setup_ui()
        self.setup_timer()
        
        if WORKFLOW_AVAILABLE:
            self.workflow_monitor.start_monitoring()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🔄 Gestionnaire de Workflows")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Onglets principaux
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Onglet Dashboard
        self.setup_dashboard_tab()
        
        # Onglet Workflows Actifs
        self.setup_active_workflows_tab()
        
        # Onglet Historique
        self.setup_history_tab()
        
        # Onglet Création de Lots
        self.setup_batch_creation_tab()
        
        # Onglet Alertes
        self.setup_alerts_tab()
    
    def setup_dashboard_tab(self):
        """Configure l'onglet dashboard"""
        dashboard_widget = QWidget()
        layout = QVBoxLayout(dashboard_widget)
        
        # Métriques principales
        metrics_frame = QFrame()
        metrics_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        metrics_layout = QHBoxLayout(metrics_frame)
        
        # Workflows actifs
        self.active_workflows_metric = self.create_metric_widget("Workflows Actifs", "0", QColor(52, 152, 219))
        metrics_layout.addWidget(self.active_workflows_metric)
        
        # Workflows aujourd'hui
        self.workflows_today_metric = self.create_metric_widget("Workflows Aujourd'hui", "0", QColor(46, 204, 113))
        metrics_layout.addWidget(self.workflows_today_metric)
        
        # Taux de succès
        self.success_rate_metric = self.create_metric_widget("Taux de Succès", "0%", QColor(155, 89, 182))
        metrics_layout.addWidget(self.success_rate_metric)
        
        # Alertes
        self.alerts_metric = self.create_metric_widget("Alertes Actives", "0", QColor(231, 76, 60))
        metrics_layout.addWidget(self.alerts_metric)
        
        layout.addWidget(metrics_frame)
        
        # Graphique de progression (simulé avec des barres de progression)
        progress_group = QGroupBox("Workflows en Cours")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_scroll = QScrollArea()
        self.progress_container = QWidget()
        self.progress_container_layout = QVBoxLayout(self.progress_container)
        self.progress_scroll.setWidget(self.progress_container)
        self.progress_scroll.setWidgetResizable(True)
        self.progress_scroll.setMaximumHeight(200)
        
        progress_layout.addWidget(self.progress_scroll)
        layout.addWidget(progress_group)
        
        # Actions rapides
        actions_group = QGroupBox("Actions Rapides")
        actions_layout = QHBoxLayout(actions_group)
        
        create_batch_btn = QPushButton("📁 Créer un Lot")
        create_batch_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(3))  # Onglet création
        actions_layout.addWidget(create_batch_btn)
        
        view_history_btn = QPushButton("📊 Voir Historique")
        view_history_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(2))  # Onglet historique
        actions_layout.addWidget(view_history_btn)
        
        manage_alerts_btn = QPushButton("⚠️ Gérer Alertes")
        manage_alerts_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(4))  # Onglet alertes
        actions_layout.addWidget(manage_alerts_btn)
        
        layout.addWidget(actions_group)
        
        self.tabs.addTab(dashboard_widget, "📊 Dashboard")
    
    def create_metric_widget(self, title: str, value: str, color: QColor) -> QWidget:
        """Crée un widget de métrique"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {color.name()};
                border-radius: 8px;
                padding: 10px;
            }}
            QLabel {{
                color: white;
                border: none;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        
        value_label = QLabel(value)
        value_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 12))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        # Stocker les labels pour mise à jour
        widget.value_label = value_label
        widget.title_label = title_label
        
        return widget
    
    def setup_active_workflows_tab(self):
        """Configure l'onglet des workflows actifs"""
        active_widget = QWidget()
        layout = QVBoxLayout(active_widget)
        
        # Contrôles
        controls_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.clicked.connect(self.refresh_active_workflows)
        controls_layout.addWidget(refresh_btn)
        
        cancel_btn = QPushButton("❌ Annuler Sélectionné")
        cancel_btn.clicked.connect(self.cancel_selected_workflow)
        controls_layout.addWidget(cancel_btn)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # Table des workflows actifs
        self.active_workflows_table = QTableWidget()
        self.active_workflows_table.setColumnCount(6)
        self.active_workflows_table.setHorizontalHeaderLabels([
            "ID", "Nom", "Statut", "Progression", "Durée", "Tâches"
        ])
        
        header = self.active_workflows_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.active_workflows_table.setColumnWidth(3, 120)
        
        layout.addWidget(self.active_workflows_table)
        
        self.tabs.addTab(active_widget, "▶️ Actifs")
    
    def setup_history_tab(self):
        """Configure l'onglet historique"""
        history_widget = QWidget()
        layout = QVBoxLayout(history_widget)
        
        # Contrôles de filtrage
        filter_layout = QHBoxLayout()
        
        filter_layout.addWidget(QLabel("Période:"))
        
        self.history_period = QComboBox()
        self.history_period.addItems(["Dernière heure", "Dernières 24h", "Dernière semaine", "Dernier mois"])
        self.history_period.setCurrentIndex(1)  # 24h par défaut
        self.history_period.currentTextChanged.connect(self.refresh_history)
        filter_layout.addWidget(self.history_period)
        
        filter_layout.addStretch()
        
        export_btn = QPushButton("📤 Exporter")
        export_btn.clicked.connect(self.export_history)
        filter_layout.addWidget(export_btn)
        
        layout.addLayout(filter_layout)
        
        # Table de l'historique
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "ID", "Nom", "Statut", "Début", "Fin", "Durée", "Taux Succès"
        ])
        
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        layout.addWidget(self.history_table)
        
        self.tabs.addTab(history_widget, "📜 Historique")
    
    def setup_batch_creation_tab(self):
        """Configure l'onglet de création de lots"""
        batch_widget = QWidget()
        layout = QVBoxLayout(batch_widget)
        
        # Formulaire de création
        form_group = QGroupBox("Créer un Nouveau Lot")
        form_layout = QFormLayout(form_group)
        
        self.batch_name = QLineEdit()
        self.batch_name.setPlaceholderText("Nom du lot de traitement")
        form_layout.addRow("Nom du Lot:", self.batch_name)
        
        # Sélection des fichiers
        files_layout = QHBoxLayout()
        self.selected_files_list = QListWidget()
        self.selected_files_list.setMaximumHeight(150)
        files_layout.addWidget(self.selected_files_list)
        
        files_buttons_layout = QVBoxLayout()
        
        add_files_btn = QPushButton("➕ Ajouter Fichiers")
        add_files_btn.clicked.connect(self.add_files_to_batch)
        files_buttons_layout.addWidget(add_files_btn)
        
        remove_file_btn = QPushButton("➖ Retirer Sélectionné")
        remove_file_btn.clicked.connect(self.remove_file_from_batch)
        files_buttons_layout.addWidget(remove_file_btn)
        
        clear_files_btn = QPushButton("🗑️ Vider")
        clear_files_btn.clicked.connect(self.clear_batch_files)
        files_buttons_layout.addWidget(clear_files_btn)
        
        files_buttons_layout.addStretch()
        files_layout.addLayout(files_buttons_layout)
        
        form_layout.addRow("Fichiers:", files_layout)
        
        # Options de traitement
        self.batch_priority = QSpinBox()
        self.batch_priority.setRange(0, 10)
        self.batch_priority.setValue(5)
        form_layout.addRow("Priorité:", self.batch_priority)
        
        self.auto_retry = QCheckBox("Retry automatique en cas d'erreur")
        self.auto_retry.setChecked(True)
        form_layout.addRow("", self.auto_retry)
        
        # Programmation
        self.schedule_checkbox = QCheckBox("Programmer l'exécution")
        form_layout.addRow("", self.schedule_checkbox)
        
        self.schedule_datetime = QDateTimeEdit()
        self.schedule_datetime.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # +1h
        self.schedule_datetime.setEnabled(False)
        self.schedule_checkbox.toggled.connect(self.schedule_datetime.setEnabled)
        form_layout.addRow("Heure d'exécution:", self.schedule_datetime)
        
        layout.addWidget(form_group)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        create_batch_btn = QPushButton("🚀 Créer le Lot")
        create_batch_btn.clicked.connect(self.create_batch)
        create_batch_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        """)
        buttons_layout.addWidget(create_batch_btn)
        
        layout.addLayout(buttons_layout)
        
        layout.addStretch()
        
        self.tabs.addTab(batch_widget, "📁 Créer Lot")
    
    def setup_alerts_tab(self):
        """Configure l'onglet des alertes"""
        alerts_widget = QWidget()
        layout = QVBoxLayout(alerts_widget)
        
        # Contrôles
        controls_layout = QHBoxLayout()
        
        acknowledge_all_btn = QPushButton("✅ Acquitter Tout")
        acknowledge_all_btn.clicked.connect(self.acknowledge_all_alerts)
        controls_layout.addWidget(acknowledge_all_btn)
        
        controls_layout.addStretch()
        
        clear_old_btn = QPushButton("🗑️ Nettoyer Anciennes")
        clear_old_btn.clicked.connect(self.clear_old_alerts)
        controls_layout.addWidget(clear_old_btn)
        
        layout.addLayout(controls_layout)
        
        # Liste des alertes
        self.alerts_list = QListWidget()
        layout.addWidget(self.alerts_list)
        
        self.tabs.addTab(alerts_widget, "⚠️ Alertes")
    
    def setup_timer(self):
        """Configure le timer de mise à jour"""
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_dashboard)
        self.update_timer.start(5000)  # Mise à jour toutes les 5 secondes
    
    def update_dashboard(self):
        """Met à jour le dashboard"""
        if not WORKFLOW_AVAILABLE or not self.workflow_monitor:
            return
        
        try:
            dashboard_data = self.workflow_monitor.get_dashboard_data()
            
            # Mettre à jour les métriques
            self.active_workflows_metric.value_label.setText(str(dashboard_data["active_workflows"]))
            self.workflows_today_metric.value_label.setText(str(dashboard_data["workflows_today"]))
            self.success_rate_metric.value_label.setText(f"{dashboard_data['success_rate_today']:.1%}")
            self.alerts_metric.value_label.setText(str(dashboard_data["active_alerts"]))
            
            # Mettre à jour les barres de progression
            self.update_progress_bars(dashboard_data["workflow_details"])
            
            # Mettre à jour l'onglet actuel si c'est les workflows actifs
            if self.tabs.currentIndex() == 1:  # Onglet workflows actifs
                self.refresh_active_workflows()
                
        except Exception as e:
            print(f"Erreur mise à jour dashboard: {e}")
    
    def update_progress_bars(self, workflow_details: List[Dict[str, Any]]):
        """Met à jour les barres de progression"""
        # Nettoyer les anciennes barres
        for i in reversed(range(self.progress_container_layout.count())):
            child = self.progress_container_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        # Ajouter les nouvelles barres
        for workflow in workflow_details:
            progress_frame = QFrame()
            progress_layout = QVBoxLayout(progress_frame)
            progress_layout.setContentsMargins(5, 5, 5, 5)
            
            # Nom et statut
            name_label = QLabel(f"{workflow['name']} ({workflow['status']})")
            name_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            progress_layout.addWidget(name_label)
            
            # Barre de progression
            progress_bar = QProgressBar()
            progress_bar.setValue(int(workflow['progress']))
            progress_bar.setFormat(f"{workflow['tasks']} tâches - {workflow['progress']:.1f}%")
            progress_layout.addWidget(progress_bar)
            
            self.progress_container_layout.addWidget(progress_frame)
        
        if not workflow_details:
            no_workflows_label = QLabel("Aucun workflow actif")
            no_workflows_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_workflows_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
            self.progress_container_layout.addWidget(no_workflows_label)
    
    def refresh_active_workflows(self):
        """Actualise la liste des workflows actifs"""
        if not WORKFLOW_AVAILABLE or not self.workflow_monitor:
            return
        
        try:
            dashboard_data = self.workflow_monitor.get_dashboard_data()
            workflow_details = dashboard_data["workflow_details"]
            
            self.active_workflows_table.setRowCount(len(workflow_details))
            
            for row, workflow in enumerate(workflow_details):
                self.active_workflows_table.setItem(row, 0, QTableWidgetItem(workflow["id"]))
                self.active_workflows_table.setItem(row, 1, QTableWidgetItem(workflow["name"]))
                self.active_workflows_table.setItem(row, 2, QTableWidgetItem(workflow["status"]))
                
                # Barre de progression dans la cellule
                progress_bar = QProgressBar()
                progress_bar.setValue(int(workflow["progress"]))
                self.active_workflows_table.setCellWidget(row, 3, progress_bar)
                
                duration_str = f"{workflow['duration']:.0f}s"
                self.active_workflows_table.setItem(row, 4, QTableWidgetItem(duration_str))
                self.active_workflows_table.setItem(row, 5, QTableWidgetItem(workflow["tasks"]))
                
        except Exception as e:
            print(f"Erreur actualisation workflows: {e}")
    
    def refresh_history(self):
        """Actualise l'historique"""
        if not WORKFLOW_AVAILABLE or not self.workflow_monitor:
            return
        
        # Mapper la sélection à des heures
        period_map = {
            "Dernière heure": 1,
            "Dernières 24h": 24,
            "Dernière semaine": 168,
            "Dernier mois": 720
        }
        
        hours = period_map.get(self.history_period.currentText(), 24)
        
        try:
            history = self.workflow_monitor.get_workflow_history(hours)
            
            self.history_table.setRowCount(len(history))
            
            for row, workflow in enumerate(history):
                self.history_table.setItem(row, 0, QTableWidgetItem(workflow["workflow_id"]))
                self.history_table.setItem(row, 1, QTableWidgetItem(workflow["workflow_name"]))
                
                # Colorer le statut
                status_item = QTableWidgetItem(workflow["status"])
                if workflow["status"] == "completed":
                    status_item.setBackground(QColor(46, 204, 113, 100))
                elif workflow["status"] == "failed":
                    status_item.setBackground(QColor(231, 76, 60, 100))
                self.history_table.setItem(row, 2, status_item)
                
                # Formatage des dates
                start_time = datetime.fromisoformat(workflow["start_time"])
                self.history_table.setItem(row, 3, QTableWidgetItem(start_time.strftime("%H:%M:%S")))
                
                if workflow["end_time"]:
                    end_time = datetime.fromisoformat(workflow["end_time"])
                    self.history_table.setItem(row, 4, QTableWidgetItem(end_time.strftime("%H:%M:%S")))
                else:
                    self.history_table.setItem(row, 4, QTableWidgetItem("En cours"))
                
                duration_str = f"{workflow['duration']:.1f}s" if workflow['duration'] else "N/A"
                self.history_table.setItem(row, 5, QTableWidgetItem(duration_str))
                
                success_rate_str = f"{workflow['success_rate']:.1%}"
                self.history_table.setItem(row, 6, QTableWidgetItem(success_rate_str))
                
        except Exception as e:
            print(f"Erreur actualisation historique: {e}")
    
    def cancel_selected_workflow(self):
        """Annule le workflow sélectionné"""
        current_row = self.active_workflows_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aucune sélection", "Veuillez sélectionner un workflow à annuler.")
            return
        
        workflow_id = self.active_workflows_table.item(current_row, 0).text()
        workflow_name = self.active_workflows_table.item(current_row, 1).text()
        
        reply = QMessageBox.question(
            self, "Confirmer l'annulation",
            f"Êtes-vous sûr de vouloir annuler le workflow '{workflow_name}' ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes and self.workflow_engine:
            success = self.workflow_engine.cancel_workflow(workflow_id)
            if success:
                QMessageBox.information(self, "Succès", f"Workflow '{workflow_name}' annulé.")
                self.workflow_cancelled.emit(workflow_id)
            else:
                QMessageBox.warning(self, "Erreur", "Impossible d'annuler le workflow.")
    
    def add_files_to_batch(self):
        """Ajoute des fichiers au lot"""
        # Simuler une sélection de fichiers (dans la vraie app, utiliser QFileDialog)
        files = [
            "/path/to/file1.pdf",
            "/path/to/file2.pdf",
            "/path/to/file3.pdf"
        ]
        
        for file_path in files:
            item = QListWidgetItem(os.path.basename(file_path))
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.selected_files_list.addItem(item)
    
    def remove_file_from_batch(self):
        """Retire un fichier du lot"""
        current_row = self.selected_files_list.currentRow()
        if current_row >= 0:
            self.selected_files_list.takeItem(current_row)
    
    def clear_batch_files(self):
        """Vide la liste des fichiers"""
        self.selected_files_list.clear()
    
    def create_batch(self):
        """Crée un nouveau lot"""
        if not WORKFLOW_AVAILABLE or not self.batch_processor:
            QMessageBox.warning(self, "Non disponible", "Système de workflow non disponible.")
            return
        
        # Validation
        if not self.batch_name.text().strip():
            QMessageBox.warning(self, "Nom manquant", "Veuillez saisir un nom pour le lot.")
            return
        
        if self.selected_files_list.count() == 0:
            QMessageBox.warning(self, "Aucun fichier", "Veuillez ajouter des fichiers au lot.")
            return
        
        # Récupérer les fichiers
        files = []
        for i in range(self.selected_files_list.count()):
            item = self.selected_files_list.item(i)
            file_path = item.data(Qt.ItemDataRole.UserRole)
            files.append(file_path)
        
        # Configuration
        config = {
            "auto_retry": self.auto_retry.isChecked(),
            "priority": self.batch_priority.value()
        }
        
        try:
            if self.schedule_checkbox.isChecked():
                # Lot programmé
                schedule_time = self.schedule_datetime.dateTime().toPython()
                batch_id = self.batch_processor.create_scheduled_batch(
                    files, config, schedule_time, self.batch_name.text()
                )
                QMessageBox.information(
                    self, "Lot Programmé", 
                    f"Lot '{self.batch_name.text()}' programmé pour {schedule_time.strftime('%H:%M:%S')}"
                )
            else:
                # Lot immédiat
                workflow_id = self.batch_processor.create_pdf_processing_batch(
                    files, config, self.batch_name.text(), self.batch_priority.value()
                )
                QMessageBox.information(
                    self, "Lot Créé", 
                    f"Lot '{self.batch_name.text()}' créé et en cours de traitement."
                )
                self.workflow_created.emit(workflow_id)
            
            # Nettoyer le formulaire
            self.batch_name.clear()
            self.selected_files_list.clear()
            self.batch_priority.setValue(5)
            self.auto_retry.setChecked(True)
            self.schedule_checkbox.setChecked(False)
            
            # Basculer vers l'onglet des workflows actifs
            self.tabs.setCurrentIndex(1)
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création du lot: {str(e)}")
    
    def acknowledge_all_alerts(self):
        """Acquitte toutes les alertes"""
        if not WORKFLOW_AVAILABLE or not self.workflow_monitor:
            return
        
        # Simuler l'acquittement (dans une vraie implémentation)
        QMessageBox.information(self, "Alertes Acquittées", "Toutes les alertes ont été acquittées.")
    
    def clear_old_alerts(self):
        """Nettoie les anciennes alertes"""
        if not WORKFLOW_AVAILABLE or not self.workflow_monitor:
            return
        
        QMessageBox.information(self, "Nettoyage", "Anciennes alertes nettoyées.")
    
    def export_history(self):
        """Exporte l'historique"""
        QMessageBox.information(self, "Export", "Fonctionnalité d'export à implémenter.")

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    widget = WorkflowManagerWidget()
    widget.show()
    sys.exit(app.exec())