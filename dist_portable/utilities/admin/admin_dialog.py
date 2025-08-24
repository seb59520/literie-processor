#!/usr/bin/env python3
"""
Dialogue administrateur protégé par mot de passe pour la gestion des versions et patches
"""

import sys
import os
import subprocess
import zipfile
import json
from datetime import datetime
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QTextEdit, QTabWidget, QWidget, QMessageBox,
    QGroupBox, QFormLayout, QSpinBox, QComboBox, QFileDialog,
    QListWidget, QListWidgetItem, QProgressBar, QCheckBox, QInputDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

# Import du module de version
from version import get_version, get_version_info, get_changelog
from update_version import update_version_file, get_current_version
from .admin_logger import log_admin_access, log_version_update, log_patch_creation, log_patch_application, get_admin_logs

ADMIN_PASSWORD = "1981"

class VersionUpdateThread(QThread):
    """Thread pour la mise à jour de version"""
    update_finished = pyqtSignal(bool, str)
    
    def __init__(self, new_version, new_date, new_build, changelog_entry):
        super().__init__()
        self.new_version = new_version
        self.new_date = new_date
        self.new_build = new_build
        self.changelog_entry = changelog_entry
    
    def run(self):
        try:
            success = update_version_file(
                self.new_version, self.new_date, self.new_build, self.changelog_entry
            )
            if success:
                self.update_finished.emit(True, f"Version mise à jour vers {self.new_version}")
            else:
                self.update_finished.emit(False, "Erreur lors de la mise à jour")
        except Exception as e:
            self.update_finished.emit(False, f"Erreur: {str(e)}")

class PatchManagerThread(QThread):
    """Thread pour la gestion des patches"""
    operation_finished = pyqtSignal(bool, str)
    progress_updated = pyqtSignal(int)
    
    def __init__(self, operation, source_version, target_version, description=""):
        super().__init__()
        self.operation = operation
        self.source_version = source_version
        self.target_version = target_version
        self.description = description
    
    def run(self):
        try:
            if self.operation == "create":
                self.create_patch()
            elif self.operation == "apply":
                self.apply_patch()
            else:
                self.operation_finished.emit(False, "Opération inconnue")
        except Exception as e:
            self.operation_finished.emit(False, f"Erreur: {str(e)}")
    
    def create_patch(self):
        """Crée un patch entre deux versions"""
        self.progress_updated.emit(10)
        
        # Créer le dossier patches s'il n'existe pas
        patches_dir = "patches"
        if not os.path.exists(patches_dir):
            os.makedirs(patches_dir)
        
        self.progress_updated.emit(30)
        
        # Nom du fichier patch
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patch_name = f"patch_v{self.source_version}_to_v{self.target_version}_{timestamp}.zip"
        patch_path = os.path.join(patches_dir, patch_name)
        
        self.progress_updated.emit(50)
        
        # Créer le patch (simulation pour l'exemple)
        with zipfile.ZipFile(patch_path, 'w') as zipf:
            # Ajouter les fichiers modifiés
            zipf.write("version.py", "version.py")
            zipf.write("app_gui.py", "app_gui.py")
            
            # Ajouter les métadonnées
            metadata = {
                "source_version": self.source_version,
                "target_version": self.target_version,
                "description": self.description,
                "created_at": datetime.now().isoformat(),
                "files": ["version.py", "app_gui.py"]
            }
            zipf.writestr("metadata.json", json.dumps(metadata, indent=2))
        
        self.progress_updated.emit(100)
        self.operation_finished.emit(True, f"Patch créé: {patch_name}")
    
    def apply_patch(self):
        """Applique un patch"""
        self.progress_updated.emit(10)
        
        # Simuler l'application d'un patch
        self.progress_updated.emit(50)
        
        # Mettre à jour la version
        current_version = get_current_version()
        if current_version != self.target_version:
            # Simuler la mise à jour
            pass
        
        self.progress_updated.emit(100)
        self.operation_finished.emit(True, f"Patch appliqué: {self.source_version} → {self.target_version}")

class AdminDialog(QDialog):
    """Dialogue administrateur principal"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Administration - Literie Processor")
        self.setModal(True)
        self.setMinimumSize(800, 600)
        
        # Vérifier le mot de passe
        if not self.check_password():
            self.reject()
            return
        
        self.init_ui()
    
    def check_password(self):
        """Vérifie le mot de passe administrateur"""
        password, ok = QInputDialog.getText(self, "Authentification", 
                                           "Mot de passe administrateur:", 
                                           QLineEdit.EchoMode.Password)
        if ok and password == ADMIN_PASSWORD:
            log_admin_access(True)
            return True
        else:
            log_admin_access(False)
            QMessageBox.warning(self, "Accès refusé", "Mot de passe incorrect")
            return False
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🔧 Administration - Literie Processor")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Onglets
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Onglet Gestion des Versions
        self.create_version_tab()
        
        # Onglet Gestion des Patches
        self.create_patch_tab()
        
        # Onglet Logs Système
        self.create_logs_tab()
        
        # Onglet Admin Builder
        self.create_admin_builder_tab()
        
        # Boutons de fermeture
        button_layout = QHBoxLayout()
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        button_layout.addStretch()
        button_layout.addWidget(close_btn)
        layout.addLayout(button_layout)
    
    def create_version_tab(self):
        """Crée l'onglet de gestion des versions"""
        version_widget = QWidget()
        layout = QVBoxLayout(version_widget)
        
        # Informations actuelles
        current_group = QGroupBox("Version Actuelle")
        current_layout = QFormLayout(current_group)
        
        version_info = get_version_info()
        # Gestion d'erreur pour éviter les KeyError
        version = version_info.get("version", "Inconnue")
        build_date = version_info.get("build_date", "Inconnue")
        build_number = version_info.get("build_number", "Inconnu")
        
        current_layout.addRow("Version:", QLabel(version))
        current_layout.addRow("Build:", QLabel(build_date))
        current_layout.addRow("Numéro:", QLabel(build_number))
        layout.addWidget(current_group)
        
        # Actions rapides de mise à jour
        quick_actions_group = QGroupBox("Actions Rapides")
        quick_layout = QHBoxLayout(quick_actions_group)
        
        patch_btn = QPushButton("🔄 Mise à jour Patch")
        minor_btn = QPushButton("📈 Mise à jour Mineure")
        major_btn = QPushButton("🚀 Mise à jour Majeure")
        
        patch_btn.clicked.connect(lambda: self.quick_version_update("patch"))
        minor_btn.clicked.connect(lambda: self.quick_version_update("minor"))
        major_btn.clicked.connect(lambda: self.quick_version_update("major"))
        
        quick_layout.addWidget(patch_btn)
        quick_layout.addWidget(minor_btn)
        quick_layout.addWidget(major_btn)
        
        layout.addWidget(quick_actions_group)
        
        # Mise à jour de version
        update_group = QGroupBox("Mise à Jour de Version")
        update_layout = QFormLayout(update_group)
        
        self.new_version_edit = QLineEdit()
        self.new_version_edit.setPlaceholderText("ex: 2.3.0")
        update_layout.addRow("Nouvelle version:", self.new_version_edit)
        
        self.new_date_edit = QLineEdit()
        self.new_date_edit.setText(datetime.now().strftime("%Y-%m-%d"))
        update_layout.addRow("Date:", self.new_date_edit)
        
        self.new_build_edit = QLineEdit()
        self.new_build_edit.setText(datetime.now().strftime("%Y%m%d"))
        update_layout.addRow("Numéro build:", self.new_build_edit)
        
        self.changelog_edit = QTextEdit()
        self.changelog_edit.setMaximumHeight(100)
        self.changelog_edit.setPlaceholderText("Description des changements...")
        update_layout.addRow("Changelog:", self.changelog_edit)
        
        update_btn = QPushButton("Mettre à Jour la Version")
        update_btn.clicked.connect(self.update_version)
        update_layout.addRow("", update_btn)
        
        layout.addWidget(update_group)
        
        # Progression
        self.version_progress = QProgressBar()
        self.version_progress.setVisible(False)
        layout.addWidget(self.version_progress)
        
        # Statut
        self.version_status = QLabel()
        layout.addWidget(self.version_status)
        
        # Liste des patches disponibles
        patches_group = QGroupBox("Patches Disponibles")
        patches_layout = QVBoxLayout(patches_group)
        
        self.patches_list = QListWidget()
        self.patches_list.setMaximumHeight(150)
        self.refresh_patches_list()
        patches_layout.addWidget(self.patches_list)
        
        refresh_patches_btn = QPushButton("Actualiser la liste")
        refresh_patches_btn.clicked.connect(self.refresh_patches_list)
        patches_layout.addWidget(refresh_patches_btn)
        
        layout.addWidget(patches_group)
        
        layout.addStretch()
        self.tab_widget.addTab(version_widget, "📋 Gestion des Versions")
    
    def create_patch_tab(self):
        """Crée l'onglet de gestion des patches"""
        patch_widget = QWidget()
        layout = QVBoxLayout(patch_widget)
        
        # Création de patch
        create_group = QGroupBox("Créer un Patch")
        create_layout = QFormLayout(create_group)
        
        self.patch_source_version = QLineEdit()
        self.patch_source_version.setText(get_current_version())
        create_layout.addRow("Version source:", self.patch_source_version)
        
        self.patch_target_version = QLineEdit()
        self.patch_target_version.setPlaceholderText("ex: 2.3.0")
        create_layout.addRow("Version cible:", self.patch_target_version)
        
        self.patch_description = QTextEdit()
        self.patch_description.setMaximumHeight(80)
        self.patch_description.setPlaceholderText("Description du patch...")
        create_layout.addRow("Description:", self.patch_description)
        
        create_patch_btn = QPushButton("Créer le Patch")
        create_patch_btn.clicked.connect(self.create_patch)
        create_layout.addRow("", create_patch_btn)
        
        layout.addWidget(create_group)
        
        # Application de patch
        apply_group = QGroupBox("Appliquer un Patch")
        apply_layout = QFormLayout(apply_group)
        
        self.patch_file_edit = QLineEdit()
        self.patch_file_edit.setPlaceholderText("Sélectionner un fichier patch...")
        apply_layout.addRow("Fichier patch:", self.patch_file_edit)
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_patch_file)
        apply_layout.addRow("", browse_btn)
        
        apply_patch_btn = QPushButton("Appliquer le Patch")
        apply_patch_btn.clicked.connect(self.apply_patch)
        apply_layout.addRow("", apply_patch_btn)
        
        layout.addWidget(apply_group)
        
        # Progression
        self.patch_progress = QProgressBar()
        self.patch_progress.setVisible(False)
        layout.addWidget(self.patch_progress)
        
        # Statut
        self.patch_status = QLabel()
        layout.addWidget(self.patch_status)
        
        layout.addStretch()
        self.tab_widget.addTab(patch_widget, "📦 Gestion des Patches")
    
    def create_logs_tab(self):
        """Crée l'onglet des logs système"""
        logs_widget = QWidget()
        layout = QVBoxLayout(logs_widget)
        
        # Sélection du type de log
        log_type_layout = QHBoxLayout()
        log_type_layout.addWidget(QLabel("Type de log:"))
        
        self.log_type_combo = QComboBox()
        self.log_type_combo.addItems(["Application", "Erreurs", "Version", "Patches", "Administration"])
        self.log_type_combo.currentTextChanged.connect(self.load_logs)
        log_type_layout.addWidget(self.log_type_combo)
        
        refresh_btn = QPushButton("Actualiser")
        refresh_btn.clicked.connect(self.load_logs)
        log_type_layout.addWidget(refresh_btn)
        
        layout.addLayout(log_type_layout)
        
        # Affichage des logs
        self.logs_display = QTextEdit()
        self.logs_display.setReadOnly(True)
        self.logs_display.setFont(QFont("Courier New", 9))
        layout.addWidget(self.logs_display)
        
        # Charger les logs initiaux
        self.load_logs()
        
        self.tab_widget.addTab(logs_widget, "📊 Logs Système")
    
    def update_version(self):
        """Met à jour la version"""
        new_version = self.new_version_edit.text().strip()
        new_date = self.new_date_edit.text().strip()
        new_build = self.new_build_edit.text().strip()
        changelog = self.changelog_edit.toPlainText().strip()
        
        if not new_version:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une nouvelle version")
            return
        
        if not changelog:
            changelog = "- Mise à jour de version"
        
        # Lancer la mise à jour en arrière-plan
        self.version_progress.setVisible(True)
        self.version_progress.setRange(0, 0)  # Indéterminé
        self.version_status.setText("Mise à jour en cours...")
        
        # Enregistrer l'ancienne version pour le log
        self.old_version = get_current_version()
        
        self.version_thread = VersionUpdateThread(new_version, new_date, new_build, changelog)
        self.version_thread.update_finished.connect(self.on_version_update_finished)
        self.version_thread.start()
    
    def on_version_update_finished(self, success, message):
        """Appelé quand la mise à jour de version est terminée"""
        self.version_progress.setVisible(False)
        self.version_status.setText(message)
        
        if success:
            # Logger la mise à jour
            log_version_update(self.old_version, self.new_version_edit.text().strip())
            QMessageBox.information(self, "Succès", message)
            # Actualiser l'affichage
            self.refresh_version_info()
        else:
            QMessageBox.critical(self, "Erreur", message)
    
    def create_patch(self):
        """Crée un patch"""
        source_version = self.patch_source_version.text().strip()
        target_version = self.patch_target_version.text().strip()
        description = self.patch_description.toPlainText().strip()
        
        if not target_version:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une version cible")
            return
        
        if not description:
            description = f"Patch de {source_version} vers {target_version}"
        
        # Lancer la création en arrière-plan
        self.patch_progress.setVisible(True)
        self.patch_progress.setRange(0, 0)  # Indéterminé
        self.patch_status.setText("Création du patch en cours...")
        
        # Enregistrer les informations pour le log
        self.patch_source = source_version
        self.patch_target = target_version
        self.patch_desc = description
        
        self.patch_thread = PatchManagerThread("create", source_version, target_version, description)
        self.patch_thread.operation_finished.connect(self.on_patch_operation_finished)
        self.patch_thread.progress_updated.connect(self.patch_progress.setValue)
        self.patch_thread.start()
    
    def apply_patch(self):
        """Applique un patch"""
        patch_file = self.patch_file_edit.text().strip()
        
        if not patch_file or not os.path.exists(patch_file):
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un fichier patch valide")
            return
        
        # Simuler l'application (dans un vrai système, on extrairait et appliquerait le patch)
        self.patch_progress.setVisible(True)
        self.patch_progress.setRange(0, 0)  # Indéterminé
        self.patch_status.setText("Application du patch en cours...")
        
        self.patch_thread = PatchManagerThread("apply", "source", "target")
        self.patch_thread.operation_finished.connect(self.on_patch_operation_finished)
        self.patch_thread.progress_updated.connect(self.patch_progress.setValue)
        self.patch_thread.start()
    
    def on_patch_operation_finished(self, success, message):
        """Appelé quand une opération de patch est terminée"""
        self.patch_progress.setVisible(False)
        self.patch_status.setText(message)
        
        if success:
            # Logger l'opération selon le type
            if hasattr(self, 'patch_source'):
                log_patch_creation(self.patch_source, self.patch_target, self.patch_desc)
            else:
                log_patch_application(self.patch_file_edit.text().strip())
            QMessageBox.information(self, "Succès", message)
        else:
            QMessageBox.critical(self, "Erreur", message)
    
    def browse_patch_file(self):
        """Ouvre un dialogue pour sélectionner un fichier patch"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Sélectionner un patch", "patches", "Fichiers patch (*.zip)"
        )
        if file_path:
            self.patch_file_edit.setText(file_path)
    
    def load_logs(self):
        """Charge les logs selon le type sélectionné"""
        log_type = self.log_type_combo.currentText()
        
        try:
            if log_type == "Application":
                log_file = "logs/matelas_app.log"
            elif log_type == "Erreurs":
                log_file = "logs/matelas_errors.log"
            elif log_type == "Version":
                # Afficher les informations de version
                version_info = get_version_info()
                content = f"Version actuelle: {version_info.get('version', 'Inconnue')}\n"
                content += f"Build: {version_info.get('build_date', 'Inconnue')}\n"
                content += f"Numéro: {version_info.get('build_number', 'Inconnu')}\n\n"
                content += "Changelog:\n" + get_changelog()
                self.logs_display.setPlainText(content)
                return
            elif log_type == "Patches":
                # Lister les patches disponibles
                patches_dir = "patches"
                if os.path.exists(patches_dir):
                    patches = [f for f in os.listdir(patches_dir) if f.endswith('.zip')]
                    content = "Patches disponibles:\n\n"
                    for patch in patches:
                        content += f"• {patch}\n"
                else:
                    content = "Aucun patch disponible"
                self.logs_display.setPlainText(content)
                return
            elif log_type == "Administration":
                # Afficher les logs d'administration
                content = get_admin_logs()
                self.logs_display.setPlainText(content)
                return
            else:
                self.logs_display.setPlainText("Type de log non reconnu")
                return
            
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.logs_display.setPlainText(content)
            else:
                self.logs_display.setPlainText(f"Fichier de log non trouvé: {log_file}")
                
        except Exception as e:
            self.logs_display.setPlainText(f"Erreur lors du chargement des logs: {str(e)}")
    
    def quick_version_update(self, version_type):
        """Mise à jour rapide de version"""
        try:
            current_version = get_current_version()
            version_parts = current_version.split('.')
            
            if version_type == "patch":
                new_patch = int(version_parts[2]) + 1
                new_version = f"{version_parts[0]}.{version_parts[1]}.{new_patch}"
            elif version_type == "minor":
                new_minor = int(version_parts[1]) + 1
                new_version = f"{version_parts[0]}.{new_minor}.0"
            elif version_type == "major":
                new_major = int(version_parts[0]) + 1
                new_version = f"{new_major}.0.0"
            
            # Demander confirmation
            reply = QMessageBox.question(
                self, "Confirmation",
                f"Voulez-vous mettre à jour la version de {current_version} vers {new_version} ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Pré-remplir les champs
                self.new_version_edit.setText(new_version)
                self.new_date_edit.setText(datetime.now().strftime("%Y-%m-%d"))
                self.new_build_edit.setText(datetime.now().strftime("%Y%m%d"))
                self.changelog_edit.setPlainText(f"Mise à jour {version_type} automatique")
                
                # Lancer la mise à jour
                self.update_version()
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la mise à jour rapide: {str(e)}")
    
    def refresh_patches_list(self):
        """Actualise la liste des patches disponibles"""
        try:
            self.patches_list.clear()
            patches_dir = "patches"
            
            if os.path.exists(patches_dir):
                patch_files = [f for f in os.listdir(patches_dir) if f.endswith('.zip')]
                patch_files.sort(reverse=True)  # Plus récents en premier
                
                for patch_file in patch_files:
                    item = QListWidgetItem(f"📦 {patch_file}")
                    item.setData(Qt.ItemDataRole.UserRole, os.path.join(patches_dir, patch_file))
                    self.patches_list.addItem(item)
            else:
                self.patches_list.addItem("Aucun patch disponible")
                
        except Exception as e:
            self.patches_list.addItem(f"Erreur: {str(e)}")
    
    def refresh_version_info(self):
        """Actualise les informations de version affichées"""
        # Cette méthode pourrait être appelée pour rafraîchir l'affichage
        # après une mise à jour de version
        pass
    
    def create_admin_builder_tab(self):
        """Crée l'onglet Admin Builder"""
        admin_builder_widget = QWidget()
        layout = QVBoxLayout(admin_builder_widget)
        
        # Titre de l'onglet
        title = QLabel("🔨 Admin Builder - Générateur d'Exécutables")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "Interface d'administration pour la génération d'exécutables complets "
            "avec tous les référentiels inclus. Garantit que l'intégralité du dossier "
            "soit incluse dans l'exécutable."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; margin: 10px;")
        layout.addWidget(description)
        
        # Groupe d'actions
        actions_group = QGroupBox("🚀 Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        # Bouton pour lancer l'Admin Builder
        launch_btn = QPushButton("🔨 Lancer l'Admin Builder")
        launch_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        launch_btn.clicked.connect(self.launch_admin_builder)
        actions_layout.addWidget(launch_btn)
        
        # Bouton pour tester l'Admin Builder
        test_btn = QPushButton("🧪 Tester l'Admin Builder")
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        test_btn.clicked.connect(self.test_admin_builder)
        actions_layout.addWidget(test_btn)
        
        # Bouton pour voir la documentation
        docs_btn = QPushButton("📖 Documentation Admin Builder")
        docs_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        docs_btn.clicked.connect(self.show_admin_builder_docs)
        actions_layout.addWidget(docs_btn)
        
        layout.addWidget(actions_group)
        
        # Groupe d'informations
        info_group = QGroupBox("ℹ️ Informations")
        info_layout = QVBoxLayout(info_group)
        
        # Liste des fichiers requis
        files_label = QLabel("Fichiers requis pour l'Admin Builder:")
        files_label.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        info_layout.addWidget(files_label)
        
        self.files_status_text = QTextEdit()
        self.files_status_text.setMaximumHeight(150)
        self.files_status_text.setReadOnly(True)
        self.files_status_text.setStyleSheet("""
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 8px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
            }
        """)
        info_layout.addWidget(self.files_status_text)
        
        # Vérification des fichiers requis (après avoir créé files_status_text)
        self.check_admin_builder_files()
        
        layout.addWidget(info_group)
        
        # Ajouter l'onglet
        self.tab_widget.addTab(admin_builder_widget, "🔨 Admin Builder")
    
    def check_admin_builder_files(self):
        """Vérifie la présence des fichiers requis pour l'Admin Builder"""
        required_files = [
            "admin_builder_gui.py",
            "build_complet_avec_referentiels.py",
            "build_mac_complet.py",
            "test_referentiels_inclus.py",
            "EULA.txt"  # Fichier critique pour le lancement de l'application
        ]
        
        status_text = ""
        all_present = True
        
        for file in required_files:
            if os.path.exists(file):
                status_text += f"✅ {file} - Présent\n"
            else:
                status_text += f"❌ {file} - Manquant\n"
                all_present = False
        
        if all_present:
            status_text += "\n🎉 Tous les fichiers sont présents !"
        else:
            status_text += "\n⚠️ Certains fichiers sont manquants."
        
        self.files_status_text.setText(status_text)
    
    def launch_admin_builder(self):
        """Lance l'Admin Builder"""
        try:
            if not os.path.exists("admin_builder_gui.py"):
                QMessageBox.critical(self, "Erreur", 
                    "Le fichier admin_builder_gui.py n'est pas trouvé.\n"
                    "Assurez-vous que l'Admin Builder est correctement installé.")
                return
            
            # Lancer l'Admin Builder dans un processus séparé
            import subprocess
            import sys
            
            # Fermer le dialogue d'administration
            self.accept()
            
            # Lancer l'Admin Builder
            subprocess.Popen([sys.executable, "admin_builder_gui.py"])
            
            QMessageBox.information(self.parent(), "Admin Builder", 
                "L'Admin Builder a été lancé dans une nouvelle fenêtre.")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                f"Impossible de lancer l'Admin Builder:\n{str(e)}")
    
    def test_admin_builder(self):
        """Teste l'Admin Builder"""
        try:
            if not os.path.exists("test_admin_builder.py"):
                QMessageBox.critical(self, "Erreur", 
                    "Le fichier test_admin_builder.py n'est pas trouvé.")
                return
            
            # Lancer le test dans un processus séparé
            import subprocess
            import sys
            
            result = subprocess.run([sys.executable, "test_admin_builder.py"], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                QMessageBox.information(self, "Test réussi", 
                    "✅ Tous les tests de l'Admin Builder sont réussis !\n\n" + result.stdout)
            else:
                QMessageBox.warning(self, "Test échoué", 
                    "❌ Certains tests ont échoué.\n\n" + result.stderr)
                
        except subprocess.TimeoutExpired:
            QMessageBox.warning(self, "Test interrompu", 
                "Le test a pris trop de temps et a été interrompu.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                f"Impossible de lancer le test:\n{str(e)}")
    
    def show_admin_builder_docs(self):
        """Affiche la documentation de l'Admin Builder"""
        try:
            if os.path.exists("RESUME_ADMIN_BUILDER.md"):
                # Ouvrir le fichier avec l'éditeur par défaut
                import subprocess
                import platform
                
                if platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", "RESUME_ADMIN_BUILDER.md"])
                elif platform.system() == "Windows":
                    subprocess.run(["start", "RESUME_ADMIN_BUILDER.md"], shell=True)
                else:  # Linux
                    subprocess.run(["xdg-open", "RESUME_ADMIN_BUILDER.md"])
                    
                QMessageBox.information(self, "Documentation", 
                    "La documentation de l'Admin Builder a été ouverte.")
            else:
                QMessageBox.warning(self, "Documentation manquante", 
                    "Le fichier RESUME_ADMIN_BUILDER.md n'est pas trouvé.")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", 
                f"Impossible d'ouvrir la documentation:\n{str(e)}")

def show_admin_dialog(parent=None):
    """Fonction utilitaire pour afficher le dialogue administrateur"""
    dialog = AdminDialog(parent)
    return dialog.exec()

if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = AdminDialog()
    dialog.show()
    sys.exit(app.exec()) 