#!/usr/bin/env python3
"""
Interface graphique pour le générateur de packages correctifs MATELAS
Protégée par mot de passe pour éviter les modifications accidentelles
"""

import sys
import os
from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QTextEdit, QListWidget, 
                             QListWidgetItem, QCheckBox, QGroupBox, QScrollArea,
                             QMessageBox, QProgressBar, QFrame, QGridLayout,
                             QComboBox, QSpinBox, QTabWidget, QWidget,
                             QFileDialog, QSplitter)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPalette, QColor, QIcon
import json
from datetime import datetime

from package_builder import PackageBuilder, create_quick_correction_package


class PackageBuilderThread(QThread):
    """Thread pour créer les packages en arrière-plan"""
    progress_updated = pyqtSignal(int)
    message_updated = pyqtSignal(str)
    finished_with_result = pyqtSignal(dict)
    
    def __init__(self, description, files, changelog, custom_version=None):
        super().__init__()
        self.description = description
        self.files = files
        self.changelog = changelog
        self.custom_version = custom_version
    
    def run(self):
        try:
            self.progress_updated.emit(10)
            self.message_updated.emit("Initialisation du builder...")
            
            builder = PackageBuilder()
            
            self.progress_updated.emit(30)
            self.message_updated.emit("Création du package...")
            
            result = builder.create_correction_package(
                description=self.description,
                files_to_include=self.files,
                changelog=self.changelog,
                custom_version=self.custom_version
            )
            
            self.progress_updated.emit(100)
            self.message_updated.emit("Package créé avec succès!")
            
            self.finished_with_result.emit(result)
            
        except Exception as e:
            result = {
                "success": False,
                "error": str(e)
            }
            self.finished_with_result.emit(result)


class PasswordDialog(QDialog):
    """Dialog de saisie du mot de passe"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Accès Générateur de Packages")
        self.setModal(True)
        self.setFixedSize(400, 200)
        
        # Mot de passe (à changer selon vos besoins)
        self.correct_password = "matelas_dev_2025"
        
        self.setup_ui()
        
        # Style moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
                border: 2px solid #007bff;
                border-radius: 10px;
            }
            QLabel {
                color: #333;
                font-weight: bold;
                font-size: 12px;
            }
            QLineEdit {
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
                background-color: white;
            }
            QPushButton {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        
        # Titre
        title = QLabel("🔒 Accès Développeur Requis")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #007bff; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Veuillez entrer le mot de passe développeur\npour accéder au générateur de packages correctifs.")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; font-size: 11px;")
        layout.addWidget(desc)
        
        # Champ mot de passe
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Mot de passe développeur")
        self.password_input.returnPressed.connect(self.validate_password)
        layout.addWidget(self.password_input)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #6c757d;")
        
        ok_btn = QPushButton("Valider")
        ok_btn.clicked.connect(self.validate_password)
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(ok_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Focus sur le champ mot de passe
        self.password_input.setFocus()
    
    def validate_password(self):
        if self.password_input.text() == self.correct_password:
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Mot de passe incorrect!")
            self.password_input.clear()
            self.password_input.setFocus()


class PackageBuilderDialog(QDialog):
    """Interface principale du générateur de packages"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🚀 Générateur de Packages Correctifs MATELAS v3.11.11")
        self.setMinimumSize(900, 700)
        self.builder = PackageBuilder()
        
        self.setup_ui()
        self.load_available_files()
        self.load_existing_packages()
        
        # Style moderne
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f9fa;
            }
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
            }
            QTabBar::tab:selected {
                background-color: #007bff;
                color: white;
                font-weight: bold;
            }
            QGroupBox {
                font-weight: bold;
                color: #333;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:disabled {
                background-color: #6c757d;
            }
            QLineEdit, QTextEdit {
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 8px;
                background-color: white;
            }
            QListWidget {
                border: 1px solid #dee2e6;
                border-radius: 4px;
                background-color: white;
            }
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Titre principal
        title = QLabel("🚀 Générateur de Packages Correctifs")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setStyleSheet("color: #007bff; margin: 10px; padding: 10px;")
        layout.addWidget(title)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Tab 1: Créer un package
        self.create_tab = QWidget()
        self.setup_create_tab()
        self.tabs.addTab(self.create_tab, "📦 Créer un Package")
        
        # Tab 2: Packages existants
        self.list_tab = QWidget()
        self.setup_list_tab()
        self.tabs.addTab(self.list_tab, "📋 Packages Existants")
        
        layout.addWidget(self.tabs)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Messages de statut
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        layout.addWidget(self.status_label)
        
        # Boutons
        button_layout = QHBoxLayout()
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.clicked.connect(self.refresh_data)
        
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("background-color: #6c757d;")
        
        button_layout.addStretch()
        button_layout.addWidget(refresh_btn)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def setup_create_tab(self):
        layout = QVBoxLayout()
        
        # Informations de base
        info_group = QGroupBox("📝 Informations du Package")
        info_layout = QGridLayout()
        
        # Version
        info_layout.addWidget(QLabel("Version :"), 0, 0)
        self.version_input = QLineEdit(self.builder.get_next_version())
        info_layout.addWidget(self.version_input, 0, 1)
        
        # Description
        info_layout.addWidget(QLabel("Description :"), 1, 0)
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Ex: Correction bug upload PDF")
        info_layout.addWidget(self.description_input, 1, 1)
        
        info_group.setLayout(info_layout)
        layout.addWidget(info_group)
        
        # Sélection des fichiers
        files_group = QGroupBox("📁 Sélection des Fichiers")
        files_layout = QVBoxLayout()
        
        # Boutons de sélection rapide
        quick_buttons = QHBoxLayout()
        
        critical_btn = QPushButton("🔧 Fichiers Critiques")
        critical_btn.clicked.connect(self.select_critical_files)
        
        all_btn = QPushButton("📂 Tous les Fichiers Python")
        all_btn.clicked.connect(self.select_all_python_files)
        
        custom_btn = QPushButton("➕ Ajouter Fichiers...")
        custom_btn.clicked.connect(self.add_custom_files)
        
        quick_buttons.addWidget(critical_btn)
        quick_buttons.addWidget(all_btn)
        quick_buttons.addWidget(custom_btn)
        quick_buttons.addStretch()
        
        files_layout.addLayout(quick_buttons)
        
        # Liste des fichiers sélectionnés
        self.files_list = QListWidget()
        self.files_list.setMinimumHeight(150)
        files_layout.addWidget(self.files_list)
        
        files_group.setLayout(files_layout)
        layout.addWidget(files_group)
        
        # Changelog
        changelog_group = QGroupBox("📋 Changelog (Optionnel)")
        changelog_layout = QVBoxLayout()
        
        self.changelog_input = QTextEdit()
        self.changelog_input.setMaximumHeight(100)
        self.changelog_input.setPlaceholderText("Décrivez les changements apportés...")
        changelog_layout.addWidget(self.changelog_input)
        
        changelog_group.setLayout(changelog_layout)
        layout.addWidget(changelog_group)
        
        # Bouton de création
        create_btn = QPushButton("🚀 Créer le Package Correctif")
        create_btn.setMinimumHeight(40)
        create_btn.clicked.connect(self.create_package)
        create_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(create_btn)
        
        self.create_tab.setLayout(layout)
    
    def setup_list_tab(self):
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("📋 Packages Correctifs Existants")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #333; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Liste des packages
        self.packages_list = QListWidget()
        self.packages_list.setMinimumHeight(400)
        layout.addWidget(self.packages_list)
        
        # Boutons d'actions
        actions_layout = QHBoxLayout()
        
        open_folder_btn = QPushButton("📂 Ouvrir Dossier")
        open_folder_btn.clicked.connect(self.open_packages_folder)
        
        refresh_packages_btn = QPushButton("🔄 Actualiser Liste")
        refresh_packages_btn.clicked.connect(self.load_existing_packages)
        
        actions_layout.addWidget(open_folder_btn)
        actions_layout.addWidget(refresh_packages_btn)
        actions_layout.addStretch()
        
        layout.addLayout(actions_layout)
        
        self.list_tab.setLayout(layout)
    
    def load_available_files(self):
        """Charger la liste des fichiers disponibles"""
        self.available_files = self.builder.get_critical_files()
        
        # Ajouter d'autres fichiers importants
        additional_files = [
            "real_time_alerts.py",
            "auto_fix.py",
            "backend_interface.py",
            "package_builder.py",
            "requirements.txt"
        ]
        
        for file_path in additional_files:
            if os.path.exists(file_path) and file_path not in self.available_files:
                self.available_files.append(file_path)
    
    def select_critical_files(self):
        """Sélectionner les fichiers critiques"""
        self.files_list.clear()
        critical_files = self.builder.get_critical_files()
        
        for file_path in critical_files:
            item = QListWidgetItem(f"🔧 {file_path}")
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.files_list.addItem(item)
        
        self.status_label.setText(f"✓ {len(critical_files)} fichiers critiques sélectionnés")
    
    def select_all_python_files(self):
        """Sélectionner tous les fichiers Python"""
        self.files_list.clear()
        python_files = []
        
        # Chercher tous les .py dans le répertoire courant
        for root, dirs, files in os.walk("."):
            # Ignorer certains dossiers
            dirs[:] = [d for d in dirs if d not in ['__pycache__', '.git', 'venv', 'node_modules']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)[2:]  # Enlever le "./"
                    python_files.append(file_path)
        
        for file_path in sorted(python_files):
            item = QListWidgetItem(f"🐍 {file_path}")
            item.setData(Qt.ItemDataRole.UserRole, file_path)
            self.files_list.addItem(item)
        
        self.status_label.setText(f"✓ {len(python_files)} fichiers Python sélectionnés")
    
    def add_custom_files(self):
        """Ajouter des fichiers personnalisés"""
        files, _ = QFileDialog.getOpenFileNames(
            self, 
            "Sélectionner des fichiers à inclure",
            ".",
            "Tous les fichiers (*.*)"
        )
        
        for file_path in files:
            # Convertir en chemin relatif
            relative_path = os.path.relpath(file_path)
            
            # Vérifier si déjà dans la liste
            already_exists = False
            for i in range(self.files_list.count()):
                if self.files_list.item(i).data(Qt.ItemDataRole.UserRole) == relative_path:
                    already_exists = True
                    break
            
            if not already_exists:
                item = QListWidgetItem(f"📄 {relative_path}")
                item.setData(Qt.ItemDataRole.UserRole, relative_path)
                self.files_list.addItem(item)
        
        if files:
            self.status_label.setText(f"✓ {len(files)} fichier(s) personnalisé(s) ajouté(s)")
    
    def create_package(self):
        """Créer le package correctif"""
        # Validation
        if not self.description_input.text().strip():
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une description pour le package.")
            return
        
        if self.files_list.count() == 0:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner au moins un fichier à inclure.")
            return
        
        # Collecter les fichiers sélectionnés
        selected_files = []
        for i in range(self.files_list.count()):
            file_path = self.files_list.item(i).data(Qt.ItemDataRole.UserRole)
            selected_files.append(file_path)
        
        # Lancer la création en arrière-plan
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        
        custom_version = self.version_input.text().strip() if self.version_input.text().strip() != self.builder.get_next_version() else None
        
        self.build_thread = PackageBuilderThread(
            description=self.description_input.text().strip(),
            files=selected_files,
            changelog=self.changelog_input.toPlainText().strip(),
            custom_version=custom_version
        )
        
        self.build_thread.progress_updated.connect(self.progress_bar.setValue)
        self.build_thread.message_updated.connect(self.status_label.setText)
        self.build_thread.finished_with_result.connect(self.on_package_created)
        
        self.build_thread.start()
    
    def on_package_created(self, result):
        """Gérer le résultat de la création de package"""
        self.progress_bar.hide()
        
        if result["success"]:
            message = f"""✅ Package créé avec succès !

📦 Nom: {result['package_name']}
📂 Version: {result['version']}
📏 Taille: {result['size'] / 1024:.1f} KB
📁 Fichiers: {result['files_count']}

Le package est disponible dans le répertoire de l'application et peut être déployé via le serveur de mise à jour."""
            
            QMessageBox.information(self, "Succès", message)
            
            # Actualiser la liste des packages
            self.load_existing_packages()
            
            # Réinitialiser le formulaire
            self.reset_form()
            
        else:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création du package:\n\n{result.get('error', 'Erreur inconnue')}")
        
        self.status_label.setText("Prêt")
    
    def reset_form(self):
        """Réinitialiser le formulaire"""
        self.version_input.setText(self.builder.get_next_version())
        self.description_input.clear()
        self.changelog_input.clear()
        self.files_list.clear()
    
    def load_existing_packages(self):
        """Charger la liste des packages existants"""
        self.packages_list.clear()
        packages = self.builder.list_available_packages()
        
        for package in packages:
            metadata = package["metadata"]
            created_date = datetime.fromtimestamp(package["created"]).strftime("%d/%m/%Y %H:%M")
            
            item_text = f"""📦 {package['filename']}
🏷️  Version: {metadata['version']}
📝 Description: {metadata['description']}
📅 Créé: {created_date}
📏 Taille: {package['size'] / 1024:.1f} KB
📁 Fichiers: {len(metadata.get('files', []))}"""
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, package)
            self.packages_list.addItem(item)
        
        if not packages:
            empty_item = QListWidgetItem("Aucun package correctif trouvé.")
            empty_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.packages_list.addItem(empty_item)
    
    def open_packages_folder(self):
        """Ouvrir le dossier des packages"""
        import subprocess
        import platform
        
        folder_path = str(self.builder.update_path)
        
        try:
            if platform.system() == "Windows":
                subprocess.run(f'explorer "{folder_path}"', shell=True)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir le dossier:\n{e}")
    
    def refresh_data(self):
        """Actualiser toutes les données"""
        self.load_available_files()
        self.load_existing_packages()
        self.status_label.setText("✓ Données actualisées")


def show_package_builder_dialog(parent=None):
    """Afficher le dialog du générateur de packages avec authentification"""
    
    # Authentification
    password_dialog = PasswordDialog(parent)
    if password_dialog.exec() != QDialog.DialogCode.Accepted:
        return False
    
    # Afficher l'interface principale
    builder_dialog = PackageBuilderDialog(parent)
    return builder_dialog.exec() == QDialog.DialogCode.Accepted


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    
    # Test de l'interface
    show_package_builder_dialog()
    
    sys.exit()