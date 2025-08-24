#!/usr/bin/env python3
"""
Interface graphique pour la gestion des mises à jour
"""

import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QTextEdit, QFileDialog, QMessageBox,
    QGroupBox, QGridLayout, QProgressBar, QListWidget, QListWidgetItem,
    QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QComboBox,
    QTabWidget, QTextBrowser, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon

from version_manager import version_manager

class UpdateWorker(QThread):
    """Thread pour les opérations de mise à jour"""
    progress_updated = pyqtSignal(int)
    status_updated = pyqtSignal(str)
    operation_finished = pyqtSignal(bool, str)
    
    def __init__(self, operation, **kwargs):
        super().__init__()
        self.operation = operation
        self.kwargs = kwargs
    
    def run(self):
        try:
            if self.operation == "create_patch":
                self.status_updated.emit("Création du patch...")
                self.progress_updated.emit(25)
                
                patch_path = version_manager.create_patch(
                    self.kwargs.get("target_version"),
                    self.kwargs.get("description", "")
                )
                
                self.progress_updated.emit(100)
                self.operation_finished.emit(True, f"Patch créé: {patch_path}")
                
            elif self.operation == "apply_patch":
                self.status_updated.emit("Application du patch...")
                self.progress_updated.emit(25)
                
                success = version_manager.apply_patch(self.kwargs.get("patch_path"))
                
                self.progress_updated.emit(100)
                if success:
                    self.operation_finished.emit(True, "Patch appliqué avec succès")
                else:
                    self.operation_finished.emit(False, "Erreur lors de l'application du patch")
                    
            elif self.operation == "update_version":
                self.status_updated.emit("Mise à jour de la version...")
                self.progress_updated.emit(25)
                
                new_version = version_manager.update_version(
                    self.kwargs.get("version_type", "patch"),
                    self.kwargs.get("description", "")
                )
                
                self.progress_updated.emit(100)
                self.operation_finished.emit(True, f"Version mise à jour: {new_version}")
                
        except Exception as e:
            self.operation_finished.emit(False, f"Erreur: {str(e)}")

class CreatePatchDialog(QDialog):
    """Dialog pour créer un patch"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Créer un Patch")
        self.setModal(True)
        self.resize(500, 300)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Formulaire
        form_layout = QFormLayout()
        
        self.target_version = QLineEdit()
        self.target_version.setPlaceholderText("ex: 1.0.0")
        form_layout.addRow("Version cible:", self.target_version)
        
        self.version_type = QComboBox()
        self.version_type.addItems(["patch", "minor", "major"])
        form_layout.addRow("Type de version:", self.version_type)
        
        self.description = QTextEdit()
        self.description.setMaximumHeight(100)
        self.description.setPlaceholderText("Description des modifications...")
        form_layout.addRow("Description:", self.description)
        
        layout.addLayout(form_layout)
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def get_patch_info(self):
        return {
            "target_version": self.target_version.text(),
            "version_type": self.version_type.currentText(),
            "description": self.description.toPlainText()
        }

class UpdateManagerGUI(QMainWindow):
    """Interface principale de gestion des mises à jour"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestionnaire de Mises à Jour - Matelas App")
        self.setGeometry(100, 100, 1000, 700)
        self.init_ui()
        self.load_version_info()
        self.load_patches()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout()
        
        # Panneau gauche - Informations de version
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        main_layout.addWidget(separator)
        
        # Panneau droit - Actions et patches
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(main_layout)
        
        # Barre de statut
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Prêt")
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
    
    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Informations de version actuelle
        version_group = QGroupBox("Version Actuelle")
        version_layout = QFormLayout()
        
        self.version_label = QLabel()
        self.build_label = QLabel()
        self.date_label = QLabel()
        self.files_label = QLabel()
        self.deps_label = QLabel()
        
        version_layout.addRow("Version:", self.version_label)
        version_layout.addRow("Build:", self.build_label)
        version_layout.addRow("Date:", self.date_label)
        version_layout.addRow("Fichiers:", self.files_label)
        version_layout.addRow("Dépendances:", self.deps_label)
        
        version_group.setLayout(version_layout)
        layout.addWidget(version_group)
        
        # Actions de version
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        
        self.update_patch_btn = QPushButton("Mise à jour Patch")
        self.update_minor_btn = QPushButton("Mise à jour Mineure")
        self.update_major_btn = QPushButton("Mise à jour Majeure")
        
        self.update_patch_btn.clicked.connect(lambda: self.update_version("patch"))
        self.update_minor_btn.clicked.connect(lambda: self.update_version("minor"))
        self.update_major_btn.clicked.connect(lambda: self.update_version("major"))
        
        actions_layout.addWidget(self.update_patch_btn)
        actions_layout.addWidget(self.update_minor_btn)
        actions_layout.addWidget(self.update_major_btn)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Changelog
        changelog_group = QGroupBox("Changelog")
        changelog_layout = QVBoxLayout()
        
        self.changelog_browser = QTextBrowser()
        changelog_layout.addWidget(self.changelog_browser)
        
        changelog_group.setLayout(changelog_layout)
        layout.addWidget(changelog_group)
        
        panel.setLayout(layout)
        return panel
    
    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout()
        
        # Onglets
        tabs = QTabWidget()
        
        # Onglet Patches
        patches_tab = self.create_patches_tab()
        tabs.addTab(patches_tab, "Patches")
        
        # Onglet Mises à jour
        updates_tab = self.create_updates_tab()
        tabs.addTab(updates_tab, "Mises à jour")
        
        layout.addWidget(tabs)
        panel.setLayout(layout)
        return panel
    
    def create_patches_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Liste des patches
        patches_group = QGroupBox("Patches Disponibles")
        patches_layout = QVBoxLayout()
        
        self.patches_list = QListWidget()
        self.patches_list.itemDoubleClicked.connect(self.apply_selected_patch)
        patches_layout.addWidget(self.patches_list)
        
        # Boutons
        patches_buttons = QHBoxLayout()
        
        self.create_patch_btn = QPushButton("Créer Patch")
        self.apply_patch_btn = QPushButton("Appliquer Patch")
        self.refresh_patches_btn = QPushButton("Actualiser")
        
        self.create_patch_btn.clicked.connect(self.create_patch)
        self.apply_patch_btn.clicked.connect(self.apply_selected_patch)
        self.refresh_patches_btn.clicked.connect(self.load_patches)
        
        patches_buttons.addWidget(self.create_patch_btn)
        patches_buttons.addWidget(self.apply_patch_btn)
        patches_buttons.addWidget(self.refresh_patches_btn)
        
        patches_layout.addLayout(patches_buttons)
        patches_group.setLayout(patches_layout)
        layout.addWidget(patches_group)
        
        widget.setLayout(layout)
        return widget
    
    def create_updates_tab(self):
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Vérification des mises à jour
        check_group = QGroupBox("Vérification des Mises à jour")
        check_layout = QVBoxLayout()
        
        self.check_updates_btn = QPushButton("Vérifier les mises à jour")
        self.check_updates_btn.clicked.connect(self.check_for_updates)
        
        self.updates_info = QTextBrowser()
        self.updates_info.setMaximumHeight(200)
        
        check_layout.addWidget(self.check_updates_btn)
        check_layout.addWidget(self.updates_info)
        
        check_group.setLayout(check_layout)
        layout.addWidget(check_group)
        
        # Instructions
        instructions_group = QGroupBox("Instructions de Mise à Jour")
        instructions_layout = QVBoxLayout()
        
        instructions_text = """
        <h3>Guide de Mise à Jour</h3>
        
        <h4>Pour le Développeur :</h4>
        <ol>
        <li>Faites vos modifications dans le code</li>
        <li>Testez les changements</li>
        <li>Mettez à jour la version (patch/minor/major)</li>
        <li>Créez un patch pour la version cible</li>
        <li>Envoyez le fichier .zip au client</li>
        </ol>
        
        <h4>Pour le Client :</h4>
        <ol>
        <li>Fermez l'application Matelas</li>
        <li>Placez le fichier patch dans le dossier de l'application</li>
        <li>Lancez le gestionnaire de mises à jour</li>
        <li>Appliquez le patch</li>
        <li>Relancez l'application</li>
        </ol>
        
        <h4>Types de Versions :</h4>
        <ul>
        <li><strong>Patch</strong> : Corrections de bugs, améliorations mineures</li>
        <li><strong>Minor</strong> : Nouvelles fonctionnalités, compatibilité</li>
        <li><strong>Major</strong> : Changements majeurs, incompatibilités</li>
        </ul>
        """
        
        instructions_browser = QTextBrowser()
        instructions_browser.setHtml(instructions_text)
        instructions_layout.addWidget(instructions_browser)
        
        instructions_group.setLayout(instructions_layout)
        layout.addWidget(instructions_group)
        
        widget.setLayout(layout)
        return widget
    
    def load_version_info(self):
        """Charge les informations de version actuelle"""
        try:
            version_info = version_manager.get_version_info()
            
            self.version_label.setText(version_info.get("version", "N/A"))
            self.build_label.setText(version_info.get("build", "N/A"))
            self.date_label.setText(version_info.get("date", "N/A")[:10])
            self.files_label.setText(str(len(version_info.get("files", {}))))
            self.deps_label.setText(str(len(version_info.get("dependencies", {}))))
            
            # Charger le changelog
            changelog_file = Path("CHANGELOG.md")
            if changelog_file.exists():
                with open(changelog_file, 'r', encoding='utf-8') as f:
                    self.changelog_browser.setPlainText(f.read())
            else:
                self.changelog_browser.setPlainText("Aucun changelog disponible")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement des informations de version: {e}")
    
    def load_patches(self):
        """Charge la liste des patches disponibles"""
        try:
            self.patches_list.clear()
            patches = version_manager.list_patches()
            
            for patch_path in patches:
                patch_name = Path(patch_path).name
                item = QListWidgetItem(patch_name)
                item.setData(Qt.ItemDataRole.UserRole, patch_path)
                self.patches_list.addItem(item)
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement des patches: {e}")
    
    def update_version(self, version_type):
        """Met à jour la version"""
        description, ok = QMessageBox.getText(
            self, 
            "Description", 
            f"Description pour la mise à jour {version_type}:"
        )
        
        if ok:
            self.start_operation("update_version", version_type=version_type, description=description)
    
    def create_patch(self):
        """Crée un nouveau patch"""
        dialog = CreatePatchDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            patch_info = dialog.get_patch_info()
            self.start_operation("create_patch", **patch_info)
    
    def apply_selected_patch(self):
        """Applique le patch sélectionné"""
        current_item = self.patches_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Erreur", "Aucun patch sélectionné")
            return
        
        patch_path = current_item.data(Qt.ItemDataRole.UserRole)
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Voulez-vous appliquer le patch : {Path(patch_path).name} ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.start_operation("apply_patch", patch_path=patch_path)
    
    def check_for_updates(self):
        """Vérifie les mises à jour disponibles"""
        try:
            update_info = version_manager.check_for_updates()
            
            info_text = f"""
            <h3>Informations de Version</h3>
            <p><strong>Version actuelle :</strong> {update_info['current_version']}</p>
            <p><strong>Build :</strong> {update_info['current_build']}</p>
            <p><strong>Dernière mise à jour :</strong> {update_info['last_update'][:10]}</p>
            <p><strong>Nombre de fichiers :</strong> {update_info['files_count']}</p>
            <p><strong>Nombre de dépendances :</strong> {update_info['dependencies_count']}</p>
            """
            
            self.updates_info.setHtml(info_text)
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la vérification des mises à jour: {e}")
    
    def start_operation(self, operation, **kwargs):
        """Démarre une opération en arrière-plan"""
        self.worker = UpdateWorker(operation, **kwargs)
        self.worker.progress_updated.connect(self.progress_bar.setValue)
        self.worker.status_updated.connect(self.status_bar.showMessage)
        self.worker.operation_finished.connect(self.operation_finished)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Désactiver les boutons
        self.set_buttons_enabled(False)
        
        self.worker.start()
    
    def operation_finished(self, success, message):
        """Appelé quand une opération est terminée"""
        self.progress_bar.setVisible(False)
        self.set_buttons_enabled(True)
        
        if success:
            QMessageBox.information(self, "Succès", message)
            # Recharger les informations
            self.load_version_info()
            self.load_patches()
        else:
            QMessageBox.critical(self, "Erreur", message)
        
        self.status_bar.showMessage("Prêt")
    
    def set_buttons_enabled(self, enabled):
        """Active/désactive les boutons"""
        self.update_patch_btn.setEnabled(enabled)
        self.update_minor_btn.setEnabled(enabled)
        self.update_major_btn.setEnabled(enabled)
        self.create_patch_btn.setEnabled(enabled)
        self.apply_patch_btn.setEnabled(enabled)
        self.refresh_patches_btn.setEnabled(enabled)
        self.check_updates_btn.setEnabled(enabled)

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Gestionnaire de Mises à Jour - Matelas")
    
    window = UpdateManagerGUI()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 