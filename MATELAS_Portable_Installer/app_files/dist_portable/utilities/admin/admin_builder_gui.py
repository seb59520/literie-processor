#!/usr/bin/env python3
"""
Mini-application d'administration pour la génération d'exécutables
Interface graphique simple pour configurer et lancer la construction
"""

import os
import sys
import subprocess
import threading
import platform
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTextEdit, QGroupBox, QComboBox,
    QCheckBox, QProgressBar, QFileDialog, QMessageBox, QTabWidget,
    QGridLayout, QSpinBox, QFrame, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QPixmap

class BuildWorker(QThread):
    """Thread de travail pour la construction en arrière-plan"""
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, build_config):
        super().__init__()
        self.build_config = build_config
    
    def run(self):
        """Exécute la construction"""
        try:
            self.progress.emit("🚀 Début de la construction...")
            
            # Changer vers le répertoire de construction
            os.chdir(self.build_config['source_dir'])
            self.progress.emit(f"📁 Répertoire de travail: {self.build_config['source_dir']}")
            
            # Vérifier les référentiels
            self.progress.emit("🔍 Vérification des référentiels...")
            result = subprocess.run([
                sys.executable, "test_referentiels_inclus.py"
            ], capture_output=True, text=True, timeout=60)
            
            if result.returncode != 0:
                self.finished.emit(False, f"❌ Erreur lors de la vérification des référentiels:\n{result.stderr}")
                return
            
            self.progress.emit("✅ Référentiels vérifiés avec succès")
            
            # Construire selon la plateforme
            if self.build_config['platform'] == 'mac':
                self.progress.emit("🍎 Construction pour macOS...")
                script = "build_mac_complet.py"
            else:
                self.progress.emit("🪟 Construction pour Windows/Linux...")
                script = "build_complet_avec_referentiels.py"
            
            # Lancer la construction
            self.progress.emit(f"⏳ Lancement de {script}...")
            result = subprocess.run([
                sys.executable, script
            ], capture_output=True, text=True, timeout=900)  # 15 minutes
            
            if result.returncode == 0:
                self.progress.emit("✅ Construction terminée avec succès!")
                self.finished.emit(True, "🎉 Construction réussie!\n\n" + result.stdout)
            else:
                error_msg = f"❌ Erreur lors de la construction:\n{result.stderr}\n\nLogs:\n{result.stdout}"
                self.finished.emit(False, error_msg)
                
        except subprocess.TimeoutExpired:
            self.finished.emit(False, "❌ Timeout: La construction a pris trop de temps (15 minutes)")
        except Exception as e:
            self.finished.emit(False, f"❌ Erreur inattendue: {str(e)}")


class AdminBuilderGUI(QMainWindow):
    """Interface graphique pour l'administration de construction"""
    
    def __init__(self):
        super().__init__()
        self.build_worker = None
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("🔨 Admin Builder - Générateur d'Exécutables")
        self.setGeometry(100, 100, 900, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        
        # Titre
        title_label = QLabel("🔨 ADMIN BUILDER - GÉNÉRATEUR D'EXÉCUTABLES")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        main_layout.addWidget(title_label)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(separator)
        
        # Onglets
        tabs = QTabWidget()
        main_layout.addWidget(tabs)
        
        # Onglet Configuration
        config_tab = self.create_config_tab()
        tabs.addTab(config_tab, "⚙️ Configuration")
        
        # Onglet Construction
        build_tab = self.create_build_tab()
        tabs.addTab(build_tab, "🔨 Construction")
        
        # Onglet Logs
        logs_tab = self.create_logs_tab()
        tabs.addTab(logs_tab, "📋 Logs")
        
        # Barre de statut
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("color: #7f8c8d; padding: 5px;")
        main_layout.addWidget(self.status_label)
        
        # Initialiser les valeurs par défaut
        self.init_default_values()
        
    def create_config_tab(self):
        """Crée l'onglet de configuration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Groupe Répertoire source
        source_group = QGroupBox("📁 Répertoire source")
        source_layout = QGridLayout(source_group)
        
        self.source_path_edit = QLineEdit()
        self.source_path_edit.setPlaceholderText("Chemin vers le répertoire à compiler...")
        source_layout.addWidget(QLabel("Répertoire:"), 0, 0)
        source_layout.addWidget(self.source_path_edit, 0, 1)
        
        browse_btn = QPushButton("📂 Parcourir")
        browse_btn.clicked.connect(self.browse_source_directory)
        source_layout.addWidget(browse_btn, 0, 2)
        
        layout.addWidget(source_group)
        
        # Groupe Plateforme
        platform_group = QGroupBox("🖥️ Plateforme cible")
        platform_layout = QGridLayout(platform_group)
        
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["Windows/Linux", "macOS"])
        platform_layout.addWidget(QLabel("Plateforme:"), 0, 0)
        platform_layout.addWidget(self.platform_combo, 0, 1)
        
        # Détection automatique
        auto_detect_btn = QPushButton("🔍 Détecter automatiquement")
        auto_detect_btn.clicked.connect(self.auto_detect_platform)
        platform_layout.addWidget(auto_detect_btn, 0, 2)
        
        layout.addWidget(platform_group)
        
        # Groupe Options
        options_group = QGroupBox("⚙️ Options de construction")
        options_layout = QGridLayout(options_group)
        
        self.include_all_check = QCheckBox("Inclure tous les fichiers")
        self.include_all_check.setChecked(True)
        self.include_all_check.setToolTip("Inclut l'intégralité du dossier dans l'exécutable")
        options_layout.addWidget(self.include_all_check, 0, 0)
        
        self.verify_refs_check = QCheckBox("Vérifier les référentiels")
        self.verify_refs_check.setChecked(True)
        self.verify_refs_check.setToolTip("Vérifie que tous les référentiels sont présents")
        options_layout.addWidget(self.verify_refs_check, 0, 1)
        
        self.clean_build_check = QCheckBox("Nettoyer avant construction")
        self.clean_build_check.setChecked(True)
        self.clean_build_check.setToolTip("Supprime les anciens fichiers de build")
        options_layout.addWidget(self.clean_build_check, 1, 0)
        
        self.test_executable_check = QCheckBox("Tester l'exécutable")
        self.test_executable_check.setChecked(True)
        self.test_executable_check.setToolTip("Lance un test rapide de l'exécutable créé")
        options_layout.addWidget(self.test_executable_check, 1, 1)
        
        layout.addWidget(options_group)
        
        # Groupe Informations
        info_group = QGroupBox("ℹ️ Informations système")
        info_layout = QGridLayout(info_group)
        
        info_layout.addWidget(QLabel("Système:"), 0, 0)
        info_layout.addWidget(QLabel(platform.system()), 0, 1)
        
        info_layout.addWidget(QLabel("Python:"), 1, 0)
        info_layout.addWidget(QLabel(sys.version.split()[0]), 1, 1)
        
        info_layout.addWidget(QLabel("Architecture:"), 2, 0)
        info_layout.addWidget(QLabel(platform.machine()), 2, 1)
        
        layout.addWidget(info_group)
        
        layout.addStretch()
        return widget
    
    def create_build_tab(self):
        """Crée l'onglet de construction"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Groupe Actions
        actions_group = QGroupBox("🚀 Actions")
        actions_layout = QHBoxLayout(actions_group)
        
        self.build_btn = QPushButton("🔨 Lancer la construction")
        self.build_btn.setStyleSheet("""
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
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.build_btn.clicked.connect(self.start_build)
        actions_layout.addWidget(self.build_btn)
        
        self.stop_btn = QPushButton("⏹️ Arrêter")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 15px 30px;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_build)
        self.stop_btn.setEnabled(False)
        actions_layout.addWidget(self.stop_btn)
        
        actions_layout.addStretch()
        
        # Bouton de validation
        validate_btn = QPushButton("✅ Valider la configuration")
        validate_btn.clicked.connect(self.validate_configuration)
        actions_layout.addWidget(validate_btn)
        
        layout.addWidget(actions_group)
        
        # Barre de progression
        progress_group = QGroupBox("📊 Progression")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 0)  # Indéterminé
        self.progress_bar.setVisible(False)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_label = QLabel("En attente...")
        self.progress_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        progress_layout.addWidget(self.progress_label)
        
        layout.addWidget(progress_group)
        
        # Zone de logs en temps réel
        logs_group = QGroupBox("📋 Logs en temps réel")
        logs_layout = QVBoxLayout(logs_group)
        
        self.realtime_logs = QTextEdit()
        self.realtime_logs.setReadOnly(True)
        self.realtime_logs.setMaximumHeight(200)
        self.realtime_logs.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        logs_layout.addWidget(self.realtime_logs)
        
        layout.addWidget(logs_group)
        
        layout.addStretch()
        return widget
    
    def create_logs_tab(self):
        """Crée l'onglet des logs"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Groupe Logs complets
        logs_group = QGroupBox("📋 Logs complets")
        logs_layout = QVBoxLayout(logs_group)
        
        self.full_logs = QTextEdit()
        self.full_logs.setReadOnly(True)
        self.full_logs.setStyleSheet("""
            QTextEdit {
                background-color: #2c3e50;
                color: #ecf0f1;
                font-family: 'Courier New', monospace;
                font-size: 10px;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        logs_layout.addWidget(self.full_logs)
        
        # Boutons d'action
        logs_actions = QHBoxLayout()
        
        clear_logs_btn = QPushButton("🗑️ Effacer les logs")
        clear_logs_btn.clicked.connect(self.clear_logs)
        logs_actions.addWidget(clear_logs_btn)
        
        save_logs_btn = QPushButton("💾 Sauvegarder les logs")
        save_logs_btn.clicked.connect(self.save_logs)
        logs_actions.addWidget(save_logs_btn)
        
        logs_actions.addStretch()
        logs_layout.addLayout(logs_actions)
        
        layout.addWidget(logs_group)
        return widget
    
    def init_default_values(self):
        """Initialise les valeurs par défaut"""
        # Répertoire courant par défaut
        current_dir = os.getcwd()
        self.source_path_edit.setText(current_dir)
        
        # Détection automatique de la plateforme
        self.auto_detect_platform()
        
        # Ajouter un message de bienvenue
        self.add_log("🎉 Admin Builder initialisé")
        self.add_log(f"📁 Répertoire par défaut: {current_dir}")
        self.add_log(f"🖥️ Plateforme détectée: {platform.system()}")
    
    def browse_source_directory(self):
        """Ouvre un dialogue pour choisir le répertoire source"""
        directory = QFileDialog.getExistingDirectory(
            self, "Choisir le répertoire source", self.source_path_edit.text()
        )
        if directory:
            self.source_path_edit.setText(directory)
            self.add_log(f"📁 Répertoire sélectionné: {directory}")
    
    def auto_detect_platform(self):
        """Détecte automatiquement la plateforme"""
        if platform.system() == "Darwin":
            self.platform_combo.setCurrentText("macOS")
        else:
            self.platform_combo.setCurrentText("Windows/Linux")
        self.add_log(f"🔍 Plateforme détectée: {self.platform_combo.currentText()}")
    
    def validate_configuration(self):
        """Valide la configuration actuelle"""
        source_dir = self.source_path_edit.text().strip()
        
        if not source_dir:
            QMessageBox.warning(self, "Configuration invalide", "Veuillez spécifier un répertoire source.")
            return False
        
        if not os.path.exists(source_dir):
            QMessageBox.warning(self, "Configuration invalide", "Le répertoire source n'existe pas.")
            return False
        
        # Vérifier la présence des fichiers essentiels
        essential_files = ["app_gui.py", "backend", "config", "template"]
        missing_files = []
        
        for file in essential_files:
            if not os.path.exists(os.path.join(source_dir, file)):
                missing_files.append(file)
        
        if missing_files:
            QMessageBox.warning(
                self, "Configuration invalide", 
                f"Fichiers manquants dans le répertoire source:\n{', '.join(missing_files)}"
            )
            return False
        
        QMessageBox.information(self, "Configuration valide", "✅ La configuration est valide et prête pour la construction.")
        self.add_log("✅ Configuration validée avec succès")
        return True
    
    def start_build(self):
        """Lance la construction"""
        if not self.validate_configuration():
            return
        
        # Préparer la configuration
        build_config = {
            'source_dir': self.source_path_edit.text().strip(),
            'platform': 'mac' if self.platform_combo.currentText() == "macOS" else 'windows',
            'include_all': self.include_all_check.isChecked(),
            'verify_refs': self.verify_refs_check.isChecked(),
            'clean_build': self.clean_build_check.isChecked(),
            'test_executable': self.test_executable_check.isChecked()
        }
        
        # Démarrer le thread de construction
        self.build_worker = BuildWorker(build_config)
        self.build_worker.progress.connect(self.update_progress)
        self.build_worker.finished.connect(self.build_finished)
        
        # Mettre à jour l'interface
        self.build_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setVisible(True)
        self.progress_label.setText("Construction en cours...")
        self.status_label.setText("Construction en cours...")
        
        # Lancer la construction
        self.build_worker.start()
        
        self.add_log("🚀 Construction lancée...")
    
    def stop_build(self):
        """Arrête la construction"""
        if self.build_worker and self.build_worker.isRunning():
            self.build_worker.terminate()
            self.build_worker.wait()
            self.add_log("⏹️ Construction arrêtée par l'utilisateur")
        
        self.build_finished(False, "Construction arrêtée par l'utilisateur")
    
    def update_progress(self, message):
        """Met à jour la progression"""
        self.progress_label.setText(message)
        self.add_log(message)
    
    def build_finished(self, success, message):
        """Appelé quand la construction est terminée"""
        # Mettre à jour l'interface
        self.build_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setVisible(False)
        
        if success:
            self.progress_label.setText("✅ Construction terminée avec succès")
            self.status_label.setText("Construction réussie")
            QMessageBox.information(self, "Construction réussie", message)
        else:
            self.progress_label.setText("❌ Construction échouée")
            self.status_label.setText("Construction échouée")
            QMessageBox.critical(self, "Erreur de construction", message)
        
        self.add_log(message)
    
    def add_log(self, message):
        """Ajoute un message aux logs"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        # Ajouter aux logs en temps réel
        self.realtime_logs.append(log_entry)
        
        # Ajouter aux logs complets
        self.full_logs.append(log_entry)
        
        # Auto-scroll
        self.realtime_logs.verticalScrollBar().setValue(
            self.realtime_logs.verticalScrollBar().maximum()
        )
    
    def clear_logs(self):
        """Efface tous les logs"""
        self.realtime_logs.clear()
        self.full_logs.clear()
        self.add_log("🗑️ Logs effacés")
    
    def save_logs(self):
        """Sauvegarde les logs dans un fichier"""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder les logs", "admin_builder_logs.txt", "Fichiers texte (*.txt)"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.full_logs.toPlainText())
                self.add_log(f"💾 Logs sauvegardés: {filename}")
                QMessageBox.information(self, "Sauvegarde réussie", f"Logs sauvegardés dans:\n{filename}")
            except Exception as e:
                QMessageBox.critical(self, "Erreur de sauvegarde", f"Impossible de sauvegarder les logs:\n{str(e)}")


def main():
    """Point d'entrée principal"""
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle('Fusion')
    
    # Créer et afficher la fenêtre principale
    window = AdminBuilderGUI()
    window.show()
    
    # Lancer l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 