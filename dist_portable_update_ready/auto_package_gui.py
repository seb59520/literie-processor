#!/usr/bin/env python3
"""
Interface graphique pour la génération automatique de packages correctifs
"""

import sys
import os
from datetime import datetime, timedelta
from typing import List, Dict

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QListWidget, 
                             QListWidgetItem, QCheckBox, QGroupBox, QScrollArea,
                             QMessageBox, QProgressBar, QFrame, QGridLayout,
                             QComboBox, QSpinBox, QTabWidget, QWidget,
                             QSplitter, QTableWidget, QTableWidgetItem,
                             QHeaderView, QAbstractItemView, QButtonGroup,
                             QRadioButton)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QSize
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import json

from auto_package_generator import AutoPackageGenerator, ChangeGroup, ChangeType
from package_builder import PackageBuilder


class AutoPackageThread(QThread):
    """Thread pour analyser et créer les packages automatiquement"""
    progress_updated = pyqtSignal(int)
    message_updated = pyqtSignal(str)
    analysis_completed = pyqtSignal(list)  # List[ChangeGroup]
    package_created = pyqtSignal(dict, int)  # result, group_index
    finished_all = pyqtSignal()
    
    def __init__(self, hours: int, groups_to_create: List[int] = None):
        super().__init__()
        self.hours = hours
        self.groups_to_create = groups_to_create or []
        self.generator = AutoPackageGenerator()
    
    def run(self):
        try:
            # Phase 1: Analyse
            self.progress_updated.emit(10)
            self.message_updated.emit("🔍 Analyse des modifications...")
            
            suggested_groups = self.generator.suggest_packages(since_hours=self.hours)
            
            self.progress_updated.emit(30)
            self.analysis_completed.emit(suggested_groups)
            
            # Phase 2: Création des packages sélectionnés
            if self.groups_to_create and suggested_groups:
                total_packages = len(self.groups_to_create)
                
                for i, group_index in enumerate(self.groups_to_create):
                    if 0 <= group_index < len(suggested_groups):
                        group = suggested_groups[group_index]
                        
                        progress = 30 + int((i / total_packages) * 60)
                        self.progress_updated.emit(progress)
                        self.message_updated.emit(f"📦 Création package {i+1}/{total_packages}...")
                        
                        result = self.generator.create_package_for_group(group)
                        self.package_created.emit(result, group_index)
                
                # Mettre à jour l'état
                self.message_updated.emit("💾 Mise à jour de l'état...")
                self.generator.update_state_after_scan()
            
            self.progress_updated.emit(100)
            self.message_updated.emit("✅ Terminé!")
            self.finished_all.emit()
            
        except Exception as e:
            self.message_updated.emit(f"❌ Erreur: {str(e)}")
            self.finished_all.emit()


class AutoPackageSuggestionsDialog(QDialog):
    """Interface pour les suggestions automatiques de packages"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🤖 Suggestions Automatiques de Packages Correctifs")
        self.setMinimumSize(1000, 700)
        
        self.generator = AutoPackageGenerator()
        self.suggested_groups: List[ChangeGroup] = []
        self.selected_groups: List[int] = []
        
        self.setup_ui()
        
        # Style moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QGroupBox {
                font-weight: bold;
                color: #333;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: #f8f9fa;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QTableWidget {
                border: 1px solid #dee2e6;
                border-radius: 6px;
                background-color: white;
                gridline-color: #e9ecef;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #e9ecef;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                font-weight: bold;
                color: #495057;
            }
            QLabel {
                color: #495057;
            }
            QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 6px;
                background-color: white;
                padding: 10px;
            }
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Titre et description
        title = QLabel("🤖 Assistant de Création Automatique")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #007bff; margin: 15px; padding: 10px;")
        layout.addWidget(title)
        
        desc = QLabel("Analysez vos modifications récentes et créez automatiquement les packages correctifs adaptés")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; font-size: 11px; margin-bottom: 20px;")
        layout.addWidget(desc)
        
        # Configuration de l'analyse
        config_group = QGroupBox("⚙️ Configuration de l'Analyse")
        config_layout = QHBoxLayout()
        
        config_layout.addWidget(QLabel("Analyser les modifications des dernières :"))
        
        self.hours_combo = QComboBox()
        self.hours_combo.addItems([
            "6 heures", "12 heures", "24 heures", "48 heures", 
            "3 jours", "1 semaine", "2 semaines"
        ])
        self.hours_combo.setCurrentText("24 heures")
        config_layout.addWidget(self.hours_combo)
        
        self.analyze_btn = QPushButton("🔍 Analyser les Modifications")
        self.analyze_btn.clicked.connect(self.start_analysis)
        self.analyze_btn.setStyleSheet("background-color: #28a745; font-size: 13px;")
        config_layout.addWidget(self.analyze_btn)
        
        config_layout.addStretch()
        config_group.setLayout(config_layout)
        layout.addWidget(config_group)
        
        # Résultats de l'analyse
        self.results_group = QGroupBox("📊 Suggestions de Packages")
        results_layout = QVBoxLayout()
        
        # Tableau des suggestions
        self.suggestions_table = QTableWidget()
        self.suggestions_table.setColumnCount(6)
        self.suggestions_table.setHorizontalHeaderLabels([
            "Sélection", "Type", "Description", "Fichiers", "Priorité", "Détails"
        ])
        
        # Configuration du tableau
        header = self.suggestions_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)  # Sélection
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Type
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)  # Description
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)  # Fichiers
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Priorité
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)  # Détails
        
        self.suggestions_table.setColumnWidth(0, 80)
        self.suggestions_table.setColumnWidth(3, 80)
        self.suggestions_table.setColumnWidth(5, 80)
        self.suggestions_table.setMinimumHeight(300)
        
        results_layout.addWidget(self.suggestions_table)
        
        # Actions sur les suggestions
        actions_layout = QHBoxLayout()
        
        select_all_btn = QPushButton("☑️ Tout Sélectionner")
        select_all_btn.clicked.connect(self.select_all_suggestions)
        select_all_btn.setStyleSheet("background-color: #17a2b8;")
        
        select_critical_btn = QPushButton("🔴 Critiques Seulement")
        select_critical_btn.clicked.connect(self.select_critical_only)
        select_critical_btn.setStyleSheet("background-color: #dc3545;")
        
        clear_btn = QPushButton("🔄 Désélectionner")
        clear_btn.clicked.connect(self.clear_selection)
        clear_btn.setStyleSheet("background-color: #6c757d;")
        
        actions_layout.addWidget(select_all_btn)
        actions_layout.addWidget(select_critical_btn)
        actions_layout.addWidget(clear_btn)
        actions_layout.addStretch()
        
        results_layout.addLayout(actions_layout)
        self.results_group.setLayout(results_layout)
        layout.addWidget(self.results_group)
        
        # Aperçu du package sélectionné
        self.preview_group = QGroupBox("👁️ Aperçu du Package")
        preview_layout = QVBoxLayout()
        
        self.preview_text = QTextEdit()
        self.preview_text.setMaximumHeight(150)
        self.preview_text.setReadOnly(True)
        preview_layout.addWidget(self.preview_text)
        
        self.preview_group.setLayout(preview_layout)
        layout.addWidget(self.preview_group)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Messages de statut
        self.status_label = QLabel("Prêt à analyser")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Boutons finaux
        buttons_layout = QHBoxLayout()
        
        self.create_selected_btn = QPushButton("🚀 Créer les Packages Sélectionnés")
        self.create_selected_btn.clicked.connect(self.create_selected_packages)
        self.create_selected_btn.setEnabled(False)
        self.create_selected_btn.setStyleSheet("background-color: #28a745; font-size: 14px; padding: 12px 24px;")
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("background-color: #6c757d; font-size: 12px;")
        
        buttons_layout.addWidget(self.create_selected_btn)
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
        
        # Masquer les groupes non utilisés au départ
        self.results_group.hide()
        self.preview_group.hide()
    
    def get_hours_from_combo(self) -> int:
        """Convertir la sélection combo en heures"""
        text = self.hours_combo.currentText()
        
        mapping = {
            "6 heures": 6,
            "12 heures": 12,
            "24 heures": 24,
            "48 heures": 48,
            "3 jours": 72,
            "1 semaine": 168,
            "2 semaines": 336
        }
        
        return mapping.get(text, 24)
    
    def start_analysis(self):
        """Démarrer l'analyse des modifications"""
        hours = self.get_hours_from_combo()
        
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.analyze_btn.setEnabled(False)
        
        # Lancer l'analyse en arrière-plan
        self.analysis_thread = AutoPackageThread(hours)
        self.analysis_thread.progress_updated.connect(self.progress_bar.setValue)
        self.analysis_thread.message_updated.connect(self.status_label.setText)
        self.analysis_thread.analysis_completed.connect(self.display_suggestions)
        self.analysis_thread.finished_all.connect(self.analysis_finished)
        
        self.analysis_thread.start()
    
    def display_suggestions(self, groups: List[ChangeGroup]):
        """Afficher les suggestions dans le tableau"""
        self.suggested_groups = groups
        
        if not groups:
            self.status_label.setText("ℹ️ Aucune modification récente détectée")
            self.progress_bar.hide()
            self.analyze_btn.setEnabled(True)
            return
        
        # Afficher les groupes de résultats
        self.results_group.show()
        self.preview_group.show()
        
        # Remplir le tableau
        self.suggestions_table.setRowCount(len(groups))
        
        for i, group in enumerate(groups):
            # Colonne sélection
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_selection)
            self.suggestions_table.setCellWidget(i, 0, checkbox)
            
            # Type
            type_item = QTableWidgetItem(self.get_type_display(group.group_type))
            type_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.suggestions_table.setItem(i, 1, type_item)
            
            # Description
            desc_item = QTableWidgetItem(group.suggested_description)
            self.suggestions_table.setItem(i, 2, desc_item)
            
            # Nombre de fichiers
            files_item = QTableWidgetItem(str(len(group.files)))
            files_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.suggestions_table.setItem(i, 3, files_item)
            
            # Priorité
            priority_item = QTableWidgetItem(self.get_priority_display(group.priority))
            priority_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.suggestions_table.setItem(i, 4, priority_item)
            
            # Bouton détails
            details_btn = QPushButton("👁️")
            details_btn.setMaximumSize(QSize(30, 30))
            details_btn.clicked.connect(lambda checked, idx=i: self.show_group_details(idx))
            self.suggestions_table.setCellWidget(i, 5, details_btn)
        
        # Sélectionner automatiquement les critiques
        self.select_critical_only()
    
    def get_type_display(self, change_type: ChangeType) -> str:
        """Obtenir l'affichage du type de changement"""
        displays = {
            ChangeType.INTERFACE: "🎨 Interface",
            ChangeType.REFERENTIEL: "📊 Référentiel", 
            ChangeType.BACKEND: "⚙️ Backend",
            ChangeType.CONFIG: "🔧 Config",
            ChangeType.TEMPLATE: "📄 Template",
            ChangeType.SCRIPT: "🛠️ Script"
        }
        return displays.get(change_type, "📄 Autre")
    
    def get_priority_display(self, priority: int) -> str:
        """Obtenir l'affichage de la priorité"""
        if priority == 1:
            return "🔴 Critique"
        elif priority == 2:
            return "🟡 Important"
        else:
            return "🟢 Normal"
    
    def show_group_details(self, group_index: int):
        """Afficher les détails d'un groupe dans l'aperçu"""
        if 0 <= group_index < len(self.suggested_groups):
            group = self.suggested_groups[group_index]
            
            details = f"""📦 {group.suggested_description}

🏷️ Type: {self.get_type_display(group.group_type)}
⭐ Priorité: {self.get_priority_display(group.priority)}
📁 Fichiers ({len(group.files)}):
"""
            
            for change in group.files:
                modified_time = datetime.fromtimestamp(change.modified_time)
                details += f"   • {change.file_path} ({modified_time.strftime('%d/%m %H:%M')})\n"
            
            details += f"""

📋 Changelog prévu:
{group.suggested_changelog}

🎯 Version suggérée: {PackageBuilder().get_next_version()}-{group.package_name_suffix}"""
            
            self.preview_text.setText(details)
    
    def select_all_suggestions(self):
        """Sélectionner toutes les suggestions"""
        for i in range(self.suggestions_table.rowCount()):
            checkbox = self.suggestions_table.cellWidget(i, 0)
            if checkbox:
                checkbox.setChecked(True)
    
    def select_critical_only(self):
        """Sélectionner seulement les suggestions critiques"""
        self.clear_selection()
        for i, group in enumerate(self.suggested_groups):
            if group.priority == 1:  # Critique
                checkbox = self.suggestions_table.cellWidget(i, 0)
                if checkbox:
                    checkbox.setChecked(True)
    
    def clear_selection(self):
        """Désélectionner toutes les suggestions"""
        for i in range(self.suggestions_table.rowCount()):
            checkbox = self.suggestions_table.cellWidget(i, 0)
            if checkbox:
                checkbox.setChecked(False)
    
    def update_selection(self):
        """Mettre à jour la liste des groupes sélectionnés"""
        self.selected_groups = []
        
        for i in range(self.suggestions_table.rowCount()):
            checkbox = self.suggestions_table.cellWidget(i, 0)
            if checkbox and checkbox.isChecked():
                self.selected_groups.append(i)
        
        self.create_selected_btn.setEnabled(len(self.selected_groups) > 0)
        
        # Afficher le premier sélectionné dans l'aperçu
        if self.selected_groups:
            self.show_group_details(self.selected_groups[0])
    
    def create_selected_packages(self):
        """Créer les packages pour les groupes sélectionnés"""
        if not self.selected_groups:
            return
        
        # Confirmation
        message = f"""Créer {len(self.selected_groups)} package(s) correctif(s) ?

Packages sélectionnés:"""
        
        for i in self.selected_groups:
            if i < len(self.suggested_groups):
                group = self.suggested_groups[i]
                message += f"\n• {group.suggested_description}"
        
        reply = QMessageBox.question(
            self, 
            "Confirmer la création", 
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Lancer la création en arrière-plan
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.create_selected_btn.setEnabled(False)
        
        hours = self.get_hours_from_combo()
        self.creation_thread = AutoPackageThread(hours, self.selected_groups)
        self.creation_thread.progress_updated.connect(self.progress_bar.setValue)
        self.creation_thread.message_updated.connect(self.status_label.setText)
        self.creation_thread.package_created.connect(self.on_package_created)
        self.creation_thread.finished_all.connect(self.creation_finished)
        
        self.creation_thread.start()
    
    def on_package_created(self, result: Dict, group_index: int):
        """Gérer la création d'un package individuel"""
        if result["success"]:
            # Marquer comme créé dans le tableau
            if group_index < self.suggestions_table.rowCount():
                # Désactiver la sélection
                checkbox = self.suggestions_table.cellWidget(group_index, 0)
                if checkbox:
                    checkbox.setChecked(False)
                    checkbox.setEnabled(False)
                
                # Ajouter un indicateur de succès
                type_item = self.suggestions_table.item(group_index, 1)
                if type_item:
                    type_item.setText(type_item.text() + " ✅")
        else:
            # Marquer l'erreur
            if group_index < self.suggestions_table.rowCount():
                type_item = self.suggestions_table.item(group_index, 1)
                if type_item:
                    type_item.setText(type_item.text() + " ❌")
    
    def creation_finished(self):
        """Finaliser la création des packages"""
        self.progress_bar.hide()
        self.create_selected_btn.setEnabled(True)
        self.analyze_btn.setEnabled(True)
        
        created_count = sum(1 for i in range(self.suggestions_table.rowCount()) 
                           if "✅" in self.suggestions_table.item(i, 1).text())
        
        if created_count > 0:
            QMessageBox.information(
                self,
                "Création terminée",
                f"✅ {created_count} package(s) créé(s) avec succès!\n\n"
                "Les packages sont disponibles dans le répertoire de l'application "
                "et peuvent être déployés via le serveur de mise à jour."
            )
        
        # Réinitialiser les sélections
        self.selected_groups = []
        self.update_selection()
    
    def analysis_finished(self):
        """Finaliser l'analyse"""
        self.progress_bar.hide()
        self.analyze_btn.setEnabled(True)


def show_auto_package_dialog(parent=None):
    """Afficher l'interface de génération automatique avec protection par mot de passe"""
    from package_builder_gui import PasswordDialog
    
    # Vérification du mot de passe
    password_dialog = PasswordDialog(parent)
    if password_dialog.exec() != QDialog.DialogCode.Accepted:
        return False
    
    # Si le mot de passe est correct, afficher l'interface
    dialog = AutoPackageSuggestionsDialog(parent)
    return dialog.exec() == QDialog.DialogCode.Accepted


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test de l'interface
    show_auto_package_dialog()
    
    sys.exit()