#!/usr/bin/env python3
"""
Interface graphique PyQt6 pour l'application de traitement de devis matelas
"""

import sys
import os
import json
import tempfile
import shutil
import logging
import logging.handlers
import subprocess
from datetime import datetime
from typing import List, Dict, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, 
    QLineEdit, QCheckBox, QComboBox, QGroupBox, QScrollArea,
    QProgressBar, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter, QFrame, QMenuBar, QMenu, QTextBrowser, QGridLayout,
    QDialogButtonBox, QDialog, QHeaderView, QFormLayout,
    QListWidget, QListWidgetItem, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
import webbrowser

# Import des modules backend existants
sys.path.append('backend')
from backend_interface import backend_interface
from config import config

# Import du module de stockage sécurisé
try:
    from backend.secure_storage import secure_storage
    SECURE_STORAGE_AVAILABLE = True
except ImportError as e:
    print(f"Module de stockage sécurisé non disponible: {e}")
    SECURE_STORAGE_AVAILABLE = False

# Configuration du système de logs avancé
def setup_logging():
    """Configure le système de logging avancé avec rotation des fichiers"""
    # Créer le dossier logs s'il n'existe pas
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configuration du logger principal
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Formatter personnalisé
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler pour fichier avec rotation (max 5 fichiers de 5MB chacun)
    file_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'matelas_app.log'),
        maxBytes=5*1024*1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    
    # Handler pour erreurs critiques
    error_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'matelas_errors.log'),
        maxBytes=2*1024*1024,  # 2MB
        backupCount=3,
        encoding='utf-8'
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    # Handler pour console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    
    # Ajouter les handlers
    logger.addHandler(file_handler)
    logger.addHandler(error_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialiser le logging
logger = setup_logging()

class ProcessingThread(QThread):
    """Thread pour le traitement des fichiers PDF"""
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str, str)  # message, level
    
    def __init__(self, files, enrich_llm, llm_provider, openrouter_api_key, 
                 semaine_prod, annee_prod, commande_client):
        super().__init__()
        self.files = files
        self.enrich_llm = enrich_llm
        self.llm_provider = llm_provider
        self.openrouter_api_key = openrouter_api_key
        self.semaine_prod = semaine_prod
        self.annee_prod = annee_prod
        self.commande_client = commande_client
        
        # Logger spécifique pour ce thread
        self.thread_logger = logging.getLogger(f"ProcessingThread_{id(self)}")
    
    def run(self):
        try:
            total_files = len(self.files)
            self.log_message.emit(f"Début du traitement de {total_files} fichiers", "INFO")
            self.progress_updated.emit(5)
            
            # Initialisation et validation
            self.log_message.emit("Validation des fichiers et préparation...", "INFO")
            self.progress_updated.emit(10)
            
            # Appel du backend interface avec progression détaillée
            import asyncio
            self.log_message.emit("Appel du backend interface", "INFO")
            self.progress_updated.emit(15)
            
            # Simulation de progression pendant le traitement backend
            # (le backend ne fournit pas de progression en temps réel)
            progress_steps = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85]
            for i, progress in enumerate(progress_steps):
                # Attendre un peu pour simuler le traitement
                import time
                time.sleep(0.1)  # 100ms entre chaque étape
                
                # Messages informatifs selon l'étape
                if progress == 20:
                    self.log_message.emit("Extraction du texte des PDF...", "INFO")
                elif progress == 40:
                    self.log_message.emit("Analyse du contenu...", "INFO")
                elif progress == 60:
                    if self.enrich_llm:
                        self.log_message.emit("Enrichissement avec IA...", "INFO")
                    else:
                        self.log_message.emit("Traitement des données...", "INFO")
                elif progress == 80:
                    self.log_message.emit("Génération des configurations...", "INFO")
                
                self.progress_updated.emit(progress)
            
            # Appel réel du backend
            result = asyncio.run(backend_interface.process_pdf_files(
                self.files, self.enrich_llm, self.llm_provider, 
                self.openrouter_api_key, self.semaine_prod, 
                self.annee_prod, self.commande_client
            ))
            
            self.progress_updated.emit(90)
            self.log_message.emit("Traitement backend terminé", "INFO")
            
            # Traiter tous les résultats
            if result['results']:
                self.log_message.emit("Finalisation des résultats...", "INFO")
                self.progress_updated.emit(95)
                
                for i, individual_result in enumerate(result['results']):
                    self.result_ready.emit(individual_result)
                    # Progression finale pour chaque résultat
                    final_progress = 95 + (i + 1) * (5 // len(result['results']))
                    self.progress_updated.emit(min(final_progress, 99))
                
                self.log_message.emit(f"Traitement terminé avec {len(result['results'])} résultats", "INFO")
            else:
                self.error_occurred.emit("Aucun résultat obtenu")
                self.log_message.emit("Aucun résultat obtenu", "WARNING")
            
            self.progress_updated.emit(100)
            
        except Exception as e:
            error_msg = f"Erreur lors du traitement: {str(e)}"
            self.log_message.emit(error_msg, "ERROR")
            self.error_occurred.emit(error_msg)
            logger.exception("Erreur dans ProcessingThread")


class TestThread(QThread):
    """Thread pour l'exécution des tests automatisés"""
    test_progress = pyqtSignal(int)
    test_output = pyqtSignal(str, str)  # message, level
    test_finished = pyqtSignal(dict)  # résultats des tests
    test_error = pyqtSignal(str)


class BalanceThread(QThread):
    """Thread pour récupérer le solde OpenRouter"""
    balance_ready = pyqtSignal(dict)  # données du solde
    balance_error = pyqtSignal(str)   # message d'erreur
    
    def __init__(self, api_key):
        super().__init__()
        self.api_key = api_key
    
    def run(self):
        """Récupère le solde OpenRouter via l'API"""
        try:
            import requests
            import json
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Récupérer le solde
            response = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers)
            
            print(f"🔍 Debug OpenRouter API:")
            print(f"  - Status Code: {response.status_code}")
            print(f"  - Response Headers: {dict(response.headers)}")
            print(f"  - Response Text: {response.text[:500]}...")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  - JSON Data: {json.dumps(data, indent=2)}")
                    
                    # Essayer différents formats de réponse possibles
                    balance = 0
                    credits = 0
                    total_spent = 0
                    
                    # Format 1: champs directs
                    if "credits" in data:
                        credits = float(data["credits"])
                        balance = credits
                    if "balance" in data:
                        balance = float(data["balance"])
                    if "total_spent" in data:
                        total_spent = float(data["total_spent"])
                    
                    # Format 2: champs alternatifs
                    if "spent" in data:
                        total_spent = float(data["spent"])
                    if "remaining" in data:
                        balance = float(data["remaining"])
                    if "amount" in data:
                        balance = float(data["amount"])
                    
                    # Format 3: objets imbriqués (comme dans la réponse actuelle)
                    for key, value in data.items():
                        if isinstance(value, dict):
                            # Champs OpenRouter spécifiques pour les limites de clé
                            if "limit_remaining" in value:
                                balance = float(value["limit_remaining"])  # Limite restante
                            if "usage" in value:
                                credits = float(value["usage"])  # Utilisation actuelle
                            if "limit" in value:
                                total_spent = float(value["limit"])  # Limite totale
                            
                            # Champs génériques (fallback)
                            if "credits" in value and credits == 0:
                                credits = float(value["credits"])
                            if "balance" in value and balance == 0:
                                balance = float(value["balance"])
                            if "total_spent" in value and total_spent == 0:
                                total_spent = float(value["total_spent"])
                    
                    print(f"  - Extracted values: balance={balance}, credits={credits}, total_spent={total_spent}")
                    
                    balance_data = {
                        "balance": balance,
                        "credits": credits,
                        "total_spent": total_spent
                    }
                    self.balance_ready.emit(balance_data)
                    
                except json.JSONDecodeError as e:
                    self.balance_error.emit(f"Erreur de parsing JSON: {str(e)} - Réponse: {response.text[:200]}")
                    
            elif response.status_code == 401:
                self.balance_error.emit("Erreur d'authentification: Vérifiez votre clé API OpenRouter")
            elif response.status_code == 403:
                self.balance_error.emit("Accès refusé: Votre clé API n'a pas les permissions nécessaires")
            elif response.status_code == 404:
                self.balance_error.emit("Endpoint non trouvé: L'API OpenRouter a peut-être changé")
            else:
                self.balance_error.emit(f"Erreur API: {response.status_code} - {response.text}")
                
        except Exception as e:
            import traceback
            print(f"❌ Exception complète: {traceback.format_exc()}")
            self.balance_error.emit(f"Erreur lors de la récupération du solde: {str(e)}")


class TestThread(QThread):
    """Thread pour l'exécution des tests automatisés"""
    test_progress = pyqtSignal(int)
    test_output = pyqtSignal(str, str)  # message, level
    test_finished = pyqtSignal(dict)  # résultats des tests
    test_error = pyqtSignal(str)
    
    def __init__(self, test_type, verbose=False, coverage=False):
        super().__init__()
        self.test_type = test_type
        self.verbose = verbose
        self.coverage = coverage
        self.results = {}
        
        # Logger spécifique pour ce thread
        self.thread_logger = logging.getLogger(f"TestThread_{id(self)}")
    
    def run(self):
        try:
            self.test_output.emit("Début de l'exécution des tests", "INFO")
            self.test_progress.emit(10)
            
            # Construire la commande selon le type de test
            if self.test_type == "install_deps":
                self._run_install_dependencies()
            elif self.test_type == "all":
                self._run_all_tests()
            elif self.test_type == "unit":
                self._run_unit_tests()
            elif self.test_type == "integration":
                self._run_integration_tests()
            elif self.test_type == "performance":
                self._run_performance_tests()
            elif self.test_type == "regression":
                self._run_regression_tests()
            else:
                raise ValueError(f"Type de test inconnu: {self.test_type}")
            
            self.test_progress.emit(100)
            self.test_output.emit("Tests terminés avec succès", "INFO")
            self.test_finished.emit(self.results)
            
        except Exception as e:
            error_msg = f"Erreur lors de l'exécution des tests: {str(e)}"
            self.test_output.emit(error_msg, "ERROR")
            self.test_error.emit(error_msg)
            self.thread_logger.exception("Erreur dans TestThread")
    
    def _run_install_dependencies(self):
        """Installe les dépendances de test"""
        self.test_output.emit("Installation des dépendances de test...", "INFO")
        
        dependencies = [
            "pytest", "pytest-asyncio", "pytest-cov", "pytest-html", 
            "pytest-xdist", "pytest-mock", "pytest-benchmark"
        ]
        
        for dep in dependencies:
            self.test_output.emit(f"Installation de {dep}...", "INFO")
            try:
                result = subprocess.run(
                    ["pip", "install", dep],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode == 0:
                    self.test_output.emit(f"✅ {dep} installé avec succès", "INFO")
                else:
                    self.test_output.emit(f"⚠️ Échec de l'installation de {dep}", "WARNING")
            except Exception as e:
                self.test_output.emit(f"❌ Erreur lors de l'installation de {dep}: {e}", "ERROR")
    
    def _run_all_tests(self):
        """Exécute tous les tests"""
        self.test_output.emit("Exécution de tous les tests...", "INFO")
        
        command = ["python3", "tests/run_all_tests.py", "--all"]
        if self.verbose:
            command.append("--verbose")
        if self.coverage:
            command.append("--coverage")
            command.append("--report")
        
        self._execute_test_command(command, "Tous les tests")
    
    def _run_unit_tests(self):
        """Exécute les tests unitaires"""
        self.test_output.emit("Exécution des tests unitaires...", "INFO")
        
        command = ["python3", "-m", "pytest", "tests/test_unitaires.py"]
        if self.verbose:
            command.append("-v")
        if self.coverage:
            command.extend(["--cov=backend", "--cov=config", "--cov-report=term-missing"])
        
        self._execute_test_command(command, "Tests unitaires")
    
    def _run_integration_tests(self):
        """Exécute les tests d'intégration"""
        self.test_output.emit("Exécution des tests d'intégration...", "INFO")
        
        command = ["python3", "-m", "pytest", "tests/test_integration.py"]
        if self.verbose:
            command.append("-v")
        
        self._execute_test_command(command, "Tests d'intégration")
    
    def _run_performance_tests(self):
        """Exécute les tests de performance"""
        self.test_output.emit("Exécution des tests de performance...", "INFO")
        
        command = ["python3", "-m", "pytest", "tests/test_performance.py"]
        if self.verbose:
            command.append("-v")
        
        self._execute_test_command(command, "Tests de performance")
    
    def _run_regression_tests(self):
        """Exécute les tests de régression"""
        self.test_output.emit("Exécution des tests de régression...", "INFO")
        
        command = ["python3", "-m", "pytest", "tests/test_regression.py"]
        if self.verbose:
            command.append("-v")
        
        self._execute_test_command(command, "Tests de régression")
    
    def _execute_test_command(self, command, test_name):
        """Exécute une commande de test et capture la sortie"""
        self.test_output.emit(f"Commande: {' '.join(command)}", "INFO")
        
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes max
            )
            
            # Capturer la sortie
            if result.stdout:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.test_output.emit(line, "INFO")
            
            if result.stderr:
                for line in result.stderr.split('\n'):
                    if line.strip():
                        self.test_output.emit(line, "WARNING")
            
            # Enregistrer le résultat
            self.results[test_name] = {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
            if result.returncode == 0:
                self.test_output.emit(f"✅ {test_name} terminés avec succès", "INFO")
            else:
                self.test_output.emit(f"❌ {test_name} ont échoué (code: {result.returncode})", "ERROR")
                
        except subprocess.TimeoutExpired:
            error_msg = f"Timeout lors de l'exécution de {test_name}"
            self.test_output.emit(error_msg, "ERROR")
            self.results[test_name] = {
                'success': False,
                'error': 'Timeout'
            }
        except Exception as e:
            error_msg = f"Erreur lors de l'exécution de {test_name}: {e}"
            self.test_output.emit(error_msg, "ERROR")
            self.results[test_name] = {
                'success': False,
                'error': str(e)
            }


class ApiKeyManagerDialog(QDialog):
    """Dialogue pour la gestion des clés API"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔐 Gestionnaire de Clés API")
        self.setModal(True)
        self.resize(600, 500)
        
        # Vérifier si le stockage sécurisé est disponible
        if not SECURE_STORAGE_AVAILABLE:
            QMessageBox.warning(
                self, 
                "Stockage Sécurisé Non Disponible",
                "Le module de stockage sécurisé n'est pas disponible.\n"
                "Installez la dépendance 'cryptography' pour activer cette fonctionnalité."
            )
            self.reject()
            return
        
        self.init_ui()
        self.load_api_keys()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🔐 Gestionnaire de Clés API Sécurisées")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Gérez vos clés API de manière sécurisée. Les clés sont chiffrées "
            "et stockées localement sur votre machine."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(desc)
        
        # Tableau des clés existantes
        self.keys_table = QTableWidget()
        self.keys_table.setColumnCount(4)
        self.keys_table.setHorizontalHeaderLabels([
            "Service", "Description", "Créée le", "Actions"
        ])
        # Configuration du redimensionnement des colonnes pour PyQt6
        header = self.keys_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        layout.addWidget(self.keys_table)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.add_btn = QPushButton("➕ Ajouter une Clé")
        self.add_btn.clicked.connect(self.add_api_key)
        self.add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        buttons_layout.addWidget(self.add_btn)
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.load_api_keys)
        self.refresh_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        buttons_layout.addWidget(self.refresh_btn)
        
        self.test_btn = QPushButton("🧪 Tester Chiffrement")
        self.test_btn.clicked.connect(self.test_encryption)
        self.test_btn.setStyleSheet("background-color: #FF9800; color: white; padding: 8px;")
        buttons_layout.addWidget(self.test_btn)
        
        buttons_layout.addStretch()
        
        self.close_btn = QPushButton("Fermer")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        buttons_layout.addWidget(self.close_btn)
        
        layout.addLayout(buttons_layout)
    
    def load_api_keys(self):
        """Charge et affiche les clés API existantes"""
        try:
            services = secure_storage.list_services()
            self.keys_table.setRowCount(len(services))
            
            for row, service in enumerate(services):
                info = secure_storage.get_api_key_info(service)
                
                # Service
                service_item = QTableWidgetItem(service)
                service_item.setFlags(service_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 0, service_item)
                
                # Description
                desc_item = QTableWidgetItem(info.get('description', ''))
                desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 1, desc_item)
                
                # Date de création
                created = info.get('created_at', '')
                if created:
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                        created = dt.strftime('%d/%m/%Y %H:%M')
                    except:
                        pass
                created_item = QTableWidgetItem(created)
                created_item.setFlags(created_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(row, 2, created_item)
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                actions_layout.setContentsMargins(2, 2, 2, 2)
                
                edit_btn = QPushButton("✏️")
                edit_btn.setToolTip("Modifier")
                edit_btn.clicked.connect(lambda checked, s=service: self.edit_api_key(s))
                edit_btn.setStyleSheet("background-color: #2196F3; color: white; border: none; padding: 4px;")
                actions_layout.addWidget(edit_btn)
                
                delete_btn = QPushButton("🗑️")
                delete_btn.setToolTip("Supprimer")
                delete_btn.clicked.connect(lambda checked, s=service: self.delete_api_key(s))
                delete_btn.setStyleSheet("background-color: #f44336; color: white; border: none; padding: 4px;")
                actions_layout.addWidget(delete_btn)
                
                actions_layout.addStretch()
                self.keys_table.setCellWidget(row, 3, actions_widget)
            
            if not services:
                self.keys_table.setRowCount(1)
                no_keys_item = QTableWidgetItem("Aucune clé API sauvegardée")
                no_keys_item.setFlags(no_keys_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                self.keys_table.setItem(0, 0, no_keys_item)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement des clés API: {str(e)}")
    
    def add_api_key(self):
        """Ouvre le dialogue d'ajout de clé API"""
        dialog = ApiKeyEditDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_api_keys()
    
    def edit_api_key(self, service_name):
        """Ouvre le dialogue de modification de clé API"""
        dialog = ApiKeyEditDialog(self, service_name)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.load_api_keys()
    
    def delete_api_key(self, service_name):
        """Supprime une clé API"""
        reply = QMessageBox.question(
            self, 
            "Confirmation de suppression",
            f"Êtes-vous sûr de vouloir supprimer la clé API pour '{service_name}' ?\n\n"
            "Cette action est irréversible.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                if secure_storage.delete_api_key(service_name):
                    QMessageBox.information(self, "Succès", f"Clé API '{service_name}' supprimée avec succès.")
                    self.load_api_keys()
                else:
                    QMessageBox.warning(self, "Erreur", "Erreur lors de la suppression de la clé API.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {str(e)}")
    
    def test_encryption(self):
        """Teste le système de chiffrement"""
        try:
            if secure_storage.test_encryption():
                QMessageBox.information(
                    self, 
                    "Test Réussi", 
                    "✅ Le système de chiffrement fonctionne correctement.\n\n"
                    "Vos clés API sont protégées de manière sécurisée."
                )
            else:
                QMessageBox.warning(
                    self, 
                    "Test Échoué", 
                    "❌ Le test de chiffrement a échoué.\n\n"
                    "Vérifiez la configuration du stockage sécurisé."
                )
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du test: {str(e)}")


class ApiKeyEditDialog(QDialog):
    """Dialogue pour l'édition d'une clé API"""
    
    def __init__(self, parent=None, service_name=None):
        super().__init__(parent)
        self.service_name = service_name
        self.is_edit = service_name is not None
        
        self.setWindowTitle("🔑 Édition de Clé API" if self.is_edit else "➕ Nouvelle Clé API")
        self.setModal(True)
        self.resize(500, 300)
        
        self.init_ui()
        if self.is_edit:
            self.load_existing_key()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Formulaire
        form_layout = QFormLayout()
        
        # Service
        self.service_combo = QComboBox()
        self.service_combo.addItems([
            "openrouter", "ollama", "anthropic", "openai", "google", "custom"
        ])
        self.service_combo.setEditable(True)
        self.service_combo.setCurrentText(self.service_name or "")
        form_layout.addRow("Service:", self.service_combo)
        
        # Description
        self.desc_edit = QLineEdit()
        self.desc_edit.setPlaceholderText("Description optionnelle de cette clé API")
        form_layout.addRow("Description:", self.desc_edit)
        
        # Clé API
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_edit.setPlaceholderText("sk-... ou votre clé API")
        form_layout.addRow("Clé API:", self.api_key_edit)
        
        # Bouton pour afficher/masquer la clé
        show_key_btn = QPushButton("👁️ Afficher")
        show_key_btn.setCheckable(True)
        show_key_btn.toggled.connect(self.toggle_key_visibility)
        form_layout.addRow("", show_key_btn)
        
        layout.addLayout(form_layout)
        
        # Boutons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def toggle_key_visibility(self, show):
        """Affiche ou masque la clé API"""
        if show:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Normal)
            self.sender().setText("🙈 Masquer")
        else:
            self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
            self.sender().setText("👁️ Afficher")
    
    def load_existing_key(self):
        """Charge les données de la clé existante"""
        try:
            info = secure_storage.get_api_key_info(self.service_name)
            if info:
                self.service_combo.setCurrentText(self.service_name)
                self.desc_edit.setText(info.get('description', ''))
                self.api_key_edit.setText(info.get('api_key', ''))
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def accept(self):
        """Valide et sauvegarde la clé API"""
        service = self.service_combo.currentText().strip()
        description = self.desc_edit.text().strip()
        api_key = self.api_key_edit.text().strip()
        
        if not service:
            QMessageBox.warning(self, "Erreur", "Le nom du service est obligatoire.")
            return
        
        if not api_key:
            QMessageBox.warning(self, "Erreur", "La clé API est obligatoire.")
            return
        
        try:
            if secure_storage.save_api_key(service, api_key, description):
                QMessageBox.information(
                    self, 
                    "Succès", 
                    f"Clé API '{service}' sauvegardée avec succès.\n\n"
                    "La clé est maintenant chiffrée et stockée de manière sécurisée."
                )
                super().accept()
            else:
                QMessageBox.critical(self, "Erreur", "Erreur lors de la sauvegarde de la clé API.")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sauvegarde: {str(e)}")


class LLMProviderDialog(QDialog):
    """Dialogue unifié pour la gestion des providers LLM et clés API"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🔧 Configuration des Providers LLM")
        self.setModal(True)
        self.resize(700, 600)
        self.provider_widgets = {}  # Initialisation du dictionnaire avant tout
        self.setup_ui()
        self.load_current_settings()
    
    def setup_ui(self):
        """Configure l'interface utilisateur"""
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("🔧 Configuration des Providers LLM")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "Configurez vos providers LLM et leurs clés API. "
            "Sélectionnez le provider actuel et gérez les modèles pour chaque service."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet("color: #666; margin: 5px;")
        layout.addWidget(desc)
        
        # Provider actuel
        current_group = QGroupBox("Provider LLM actuel")
        current_layout = QHBoxLayout(current_group)
        current_layout.addWidget(QLabel("Provider :"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["openrouter", "openai", "anthropic", "gemini", "mistral"])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        current_layout.addWidget(self.provider_combo)
        layout.addWidget(current_group)
        
        # Onglets pour chaque provider
        self.tab_widget = QTabWidget()
        
        # Onglet OpenRouter
        self.openrouter_tab = self.create_provider_tab("OpenRouter", "sk-or-v1-...")
        self.tab_widget.addTab(self.openrouter_tab, "OpenRouter")
        
        # Onglet OpenAI
        self.openai_tab = self.create_provider_tab("OpenAI", "sk-...")
        self.tab_widget.addTab(self.openai_tab, "OpenAI")
        
        # Onglet Anthropic
        self.anthropic_tab = self.create_provider_tab("Anthropic", "sk-ant-...")
        self.tab_widget.addTab(self.anthropic_tab, "Anthropic")
        
        # Onglet Gemini
        self.gemini_tab = self.create_provider_tab("Gemini", "AIza...")
        self.tab_widget.addTab(self.gemini_tab, "Gemini")
        
        # Onglet Mistral
        self.mistral_tab = self.create_provider_tab("Mistral", "mist-...")
        self.tab_widget.addTab(self.mistral_tab, "Mistral")
        
        # Onglet Ollama
        self.ollama_tab = self.create_provider_tab("Ollama", "(optionnel)")
        self.tab_widget.addTab(self.ollama_tab, "Ollama")
        
        layout.addWidget(self.tab_widget)
        
        # Boutons
        buttons = QHBoxLayout()
        
        save_button = QPushButton("💾 Sauvegarder")
        save_button.clicked.connect(self.save_settings)
        save_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px;")
        buttons.addWidget(save_button)
        
        test_all_button = QPushButton("🧪 Tester toutes les connexions")
        test_all_button.clicked.connect(self.test_all_connections)
        test_all_button.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        buttons.addWidget(test_all_button)
        
        buttons.addStretch()
        
        cancel_button = QPushButton("Annuler")
        cancel_button.clicked.connect(self.reject)
        cancel_button.setStyleSheet("background-color: #f44336; color: white; padding: 8px;")
        buttons.addWidget(cancel_button)
        
        layout.addLayout(buttons)
    
    def create_provider_tab(self, provider_name, api_key_placeholder=""):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        if provider_name.lower() == "ollama":
            title = QLabel("<b>Ollama (local)</b>")
            layout.addWidget(title)
            # ComboBox modèle + bouton refresh
            model_label = QLabel("Modèle :")
            model_combo = QComboBox()
            model_combo.setEditable(True)
            model_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            refresh_btn = QPushButton("🔄")
            refresh_btn.setToolTip("Rafraîchir la liste des modèles Ollama")
            refresh_btn.setFixedWidth(32)
            def refresh_ollama_models():
                import requests
                try:
                    resp = requests.get("http://localhost:11434/api/tags", timeout=2)
                    if resp.status_code == 200:
                        data = resp.json()
                        tags = [m["name"] for m in data.get("models", []) if "name" in m]
                        model_combo.clear()
                        model_combo.addItems(tags)
                    else:
                        model_combo.clear()
                except Exception:
                    model_combo.clear()
            refresh_btn.clicked.connect(refresh_ollama_models)
            # Layout horizontal modèle
            model_layout = QHBoxLayout()
            model_layout.addWidget(model_label)
            model_layout.addWidget(model_combo)
            model_layout.addWidget(refresh_btn)
            layout.addLayout(model_layout)
            # Bouton tester
            test_btn = QPushButton("✏️ Tester la connexion Ollama")
            test_btn.setStyleSheet("background-color: orange; color: white; font-weight: bold;")
            test_btn.clicked.connect(lambda: self.test_connection(provider_name))
            layout.addWidget(test_btn)
            # Message d'aide
            help_label = QLabel("<i>Aucune clé API requise. Ollama doit être lancé localement (commande : <b>ollama serve</b>).</i>")
            help_label.setStyleSheet("color: #555; margin-top: 8px;")
            layout.addWidget(help_label)
            api_key_input = None
            model_input = model_combo
        else:
            title = QLabel(f"<b>{provider_name} (cloud)</b>")
            layout.addWidget(title)
            # Champ clé API
            api_key_label = QLabel("Clé API :")
            api_key_input = QLineEdit()
            api_key_input.setPlaceholderText(api_key_placeholder)
            api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
            api_key_input.setObjectName(f"key_{provider_name.lower()}")
            show_key_btn = QPushButton("👁️")
            show_key_btn.setCheckable(True)
            show_key_btn.setFixedWidth(40)
            def toggle_echo():
                api_key_input.setEchoMode(QLineEdit.EchoMode.Normal if show_key_btn.isChecked() else QLineEdit.EchoMode.Password)
            show_key_btn.clicked.connect(toggle_echo)
            test_btn = QPushButton("✏️ Tester la connexion")
            test_btn.setStyleSheet("background-color: orange; color: white; font-weight: bold;")
            test_btn.clicked.connect(lambda: self.test_connection(provider_name))
            def update_test_btn():
                test_btn.setEnabled(bool(api_key_input.text().strip()))
            api_key_input.textChanged.connect(update_test_btn)
            update_test_btn()
            api_layout = QHBoxLayout()
            api_layout.addWidget(api_key_label)
            api_layout.addWidget(api_key_input)
            api_layout.addWidget(show_key_btn)
            api_layout.addWidget(test_btn)
            layout.addLayout(api_layout)
            # ComboBox modèle pour chaque provider
            model_label = QLabel("Modèle :")
            model_combo = QComboBox()
            model_combo.setEditable(True)
            model_combo.setInsertPolicy(QComboBox.InsertPolicy.NoInsert)
            
            if provider_name.lower() == "openrouter":
                # Modèles populaires OpenRouter
                models = [
                    "gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo", "mistral-medium", "mistral-small",
                    "llama-3-70b-instruct", "llama-3-8b-instruct", "mixtral-8x7b-instruct",
                    "gemini-pro", "claude-3-haiku", "claude-3-sonnet"
                ]
            elif provider_name.lower() == "openai":
                # Modèles populaires OpenAI
                models = [
                    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
                ]
            elif provider_name.lower() == "anthropic":
                # Modèles populaires Anthropic
                models = [
                    "claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229",
                    "claude-3-haiku-20240307"
                ]
            elif provider_name.lower() == "gemini":
                # Modèles populaires Gemini
                models = [
                    "models/gemini-1.5-pro", "models/gemini-1.5-flash", "models/gemini-pro"
                ]
            elif provider_name.lower() == "mistral":
                # Modèles populaires Mistral
                models = [
                    "mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"
                ]
            else:
                # Modèles par défaut pour les autres providers
                models = ["modèle-par-défaut"]
            
            model_combo.addItems(models)
            model_layout = QHBoxLayout()
            model_layout.addWidget(model_label)
            model_layout.addWidget(model_combo)
            layout.addLayout(model_layout)
            model_input = model_combo
            help_label = QLabel("<i>Clé API obligatoire pour ce provider cloud.</i>")
            help_label.setStyleSheet("color: #555; margin-top: 8px;")
            layout.addWidget(help_label)
        status_label = QLabel()
        status_label.setWordWrap(True)
        layout.addWidget(status_label)
        self.provider_widgets[provider_name] = {
            "api_key_input": api_key_input if provider_name.lower() != "ollama" else None,
            "model_input": model_input,
            "status_label": status_label,
        }
        tab.setLayout(layout)
        return tab
    
    def get_model_suggestions(self, provider):
        """Retourne les suggestions de modèles pour un provider"""
        suggestions = {
            "openai": ["gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-sonnet-20240229"],
            "gemini": ["models/gemini-1.5-pro", "models/gemini-1.5-flash", "models/gemini-pro"],
            "mistral": ["mistral-large-latest", "mistral-medium-latest", "mistral-small-latest"],
            "openrouter": ["openai/gpt-4o", "anthropic/claude-3-5-sonnet", "google/gemini-1.5-pro"]
        }
        return suggestions.get(provider, [])
    
    def on_model_suggestion_changed(self, text, input_field):
        """Appelé quand une suggestion de modèle est sélectionnée"""
        if text:
            input_field.setText(text)
    
    def toggle_key_visibility(self, show, input_field, button):
        """Affiche ou masque la clé API"""
        if show:
            input_field.setEchoMode(QLineEdit.EchoMode.Normal)
            button.setText("🙈")
        else:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
            button.setText("👁️")
    
    def on_provider_changed(self, provider):
        """Appelé quand le provider actuel change"""
        # Mettre à jour l'onglet actif
        provider_tabs = {
            "openrouter": 0,
            "openai": 1,
            "anthropic": 2,
            "gemini": 3,
            "mistral": 4,
            "ollama": 5
        }
        if provider in provider_tabs:
            self.tab_widget.setCurrentIndex(provider_tabs[provider])
    
    def load_current_settings(self):
        """Charge les paramètres actuels"""
        # Provider actuel
        current_provider = config.get_current_llm_provider()
        index = self.provider_combo.findText(current_provider)
        if index >= 0:
            self.provider_combo.setCurrentIndex(index)
        
        # Clés API et modèles
        providers = ["openrouter", "openai", "anthropic", "gemini", "mistral", "ollama"]
        for provider in providers:
            # Clé API
            key_input = self.findChild(QLineEdit, f"key_{provider}")
            if key_input:
                api_key = config.get_llm_api_key(provider)
                key_input.setText(api_key)
            
            # Modèle
            model_input = self.findChild(QLineEdit, f"model_{provider}")
            if model_input:
                model = config.get_llm_model(provider)
                model_input.setText(model)
    
    def test_connection(self, provider):
        widgets = self.provider_widgets[provider]
        status_label = widgets["status_label"]
        if provider.lower() == "ollama":
            import requests
            try:
                resp = requests.get("http://localhost:11434/api/tags", timeout=2)
                if resp.status_code == 200:
                    status_label.setText("✅ Ollama disponible sur localhost:11434")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Ollama ne répond pas (code {resp.status_code})")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText("❌ Ollama non disponible. Lancez-le avec 'ollama serve'.")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        # Pour OpenRouter et autres
        api_key_input = widgets.get("api_key_input")
        api_key = api_key_input.text().strip() if api_key_input else ""
        if provider.lower() == "openrouter":
            if not api_key:
                status_label.setText("❌ Clé API manquante pour OpenRouter")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
                return
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            try:
                resp = requests.get("https://openrouter.ai/api/v1/auth/key", headers=headers, timeout=5)
                if resp.status_code == 200 and resp.json().get("data"):
                    status_label.setText("✅ Connexion OpenRouter OK")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Erreur OpenRouter: {resp.status_code}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText(f"❌ Erreur de connexion: {e}")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        elif provider.lower() == "mistral":
            if not api_key:
                status_label.setText("❌ Clé API manquante pour Mistral")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
                return
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            try:
                resp = requests.get("https://api.mistral.ai/v1/models", headers=headers, timeout=5)
                if resp.status_code == 200:
                    status_label.setText("✅ Connexion Mistral OK")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Erreur Mistral: {resp.status_code}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText(f"❌ Erreur de connexion: {e}")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        elif provider.lower() == "openai":
            if not api_key:
                status_label.setText("❌ Clé API manquante pour OpenAI")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
                return
            import requests
            headers = {"Authorization": f"Bearer {api_key}"}
            try:
                resp = requests.get("https://api.openai.com/v1/models", headers=headers, timeout=5)
                if resp.status_code == 200:
                    status_label.setText("✅ Connexion OpenAI OK")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Erreur OpenAI: {resp.status_code}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText(f"❌ Erreur de connexion: {e}")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        elif provider.lower() == "anthropic":
            if not api_key:
                status_label.setText("❌ Clé API manquante pour Anthropic")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
                return
            import requests
            headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
            try:
                resp = requests.get("https://api.anthropic.com/v1/models", headers=headers, timeout=5)
                if resp.status_code == 200:
                    status_label.setText("✅ Connexion Anthropic OK")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Erreur Anthropic: {resp.status_code}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText(f"❌ Erreur de connexion: {e}")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        elif provider.lower() == "gemini":
            if not api_key:
                status_label.setText("❌ Clé API manquante pour Gemini")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
                return
            import requests
            try:
                resp = requests.get(f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}", timeout=5)
                if resp.status_code == 200:
                    status_label.setText("✅ Connexion Gemini OK")
                    status_label.setStyleSheet("color: green; padding: 5px; border-radius: 3px; background-color: #e8f5e8;")
                else:
                    status_label.setText(f"❌ Erreur Gemini: {resp.status_code}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            except Exception as e:
                status_label.setText(f"❌ Erreur de connexion: {e}")
                status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
            return
        # ... autres providers ...
        else:
            # Provider non géré
            status_label.setText(f"❌ Test non implémenté pour {provider}")
            status_label.setStyleSheet("color: orange; padding: 5px; border-radius: 3px; background-color: #fff3e0;")
    
    def test_all_connections(self):
        """Teste toutes les connexions"""
        providers = ["openrouter", "openai", "anthropic", "gemini", "mistral", "ollama"]
        for provider in providers:
            try:
                self.test_connection(provider)
            except Exception as e:
                # Gestion d'erreur pour chaque test
                if provider in self.provider_widgets:
                    status_label = self.provider_widgets[provider]["status_label"]
                    status_label.setText(f"❌ Erreur lors du test: {str(e)}")
                    status_label.setStyleSheet("color: red; padding: 5px; border-radius: 3px; background-color: #ffebee;")
    
    def save_settings(self):
        """Sauvegarde les paramètres"""
        # Provider actuel
        current_provider = self.provider_combo.currentText()
        config.set_current_llm_provider(current_provider)
        
        # Clés API et modèles
        providers = ["openrouter", "openai", "anthropic", "gemini", "mistral", "ollama"]
        for provider in providers:
            # Clé API
            key_input = self.findChild(QLineEdit, f"key_{provider}")
            if key_input:
                api_key = key_input.text().strip()
                config.set_llm_api_key(provider, api_key)
            
            # Modèle
            model_input = self.findChild(QLineEdit, f"model_{provider}")
            if model_input:
                model = model_input.text().strip()
                config.set_llm_model(provider, model)
        
        QMessageBox.information(self, "Succès", "Configuration sauvegardée avec succès!")
        self.accept()


class MatelasApp(QMainWindow):
    """Application principale pour le traitement de devis matelas"""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.processing_thread = None
        self.test_thread = None
        # Variables pour accumuler les résultats
        self.all_results = []
        self.all_configurations = []
        self.all_configurations_sommiers = []
        self.all_preimport = []
        self.all_excel_files = []
        self.eula_accepted_file = os.path.join(os.path.expanduser('~'), '.matelas_eula_accepted')
        
        # Logger spécifique pour l'application
        try:
            self.app_logger = logging.getLogger("MatelasApp")
            self.app_logger.info("Initialisation de l'application MatelasApp")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du logger: {e}")
            self.app_logger = None
        
        try:
            self.check_eula_acceptance()
            self.init_ui()
            
            # Timer pour mettre à jour la barre de statut
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.update_status_bar)
            self.status_timer.start(1000)  # Mise à jour toutes les secondes
            
            if self.app_logger:
                self.app_logger.info("Application initialisée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de l'interface: {e}")
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Application Traitement Devis Matelas")
        self.setGeometry(100, 100, 1400, 900)
        
        # Définir l'icône de la fenêtre avec le logo
        self.setWindowIcon(QIcon("assets/lit-double.png"))
        
        # Création de la barre de menu
        self.create_menu_bar()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter pour diviser l'interface
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panneau de gauche (configuration)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panneau de droite (résultats)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Proportions du splitter
        splitter.setSizes([400, 1000])
        
        # Style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #cccccc;
                border-radius: 5px;
                margin-top: 1ex;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
            QPushButton:pressed {
                background-color: #005a9e;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
            QTextEdit {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
            }
            QTableWidget {
                border: 1px solid #cccccc;
                border-radius: 4px;
                gridline-color: #e0e0e0;
            }
            QTextBrowser {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background-color: #fafafa;
                font-family: 'Courier New', monospace;
                font-size: 10px;
            }
        """)
        
        self.app_logger.info("Interface utilisateur initialisée")
    
    def create_left_panel(self):
        """Crée le panneau de configuration à gauche"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Affichage du logo en haut du panneau
        logo_label = QLabel()
        logo_pixmap = QPixmap("assets/lit-double.png").scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
        logo_label.setPixmap(logo_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        
        # Titre
        title = QLabel("Configuration")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Groupe fichiers
        file_group = QGroupBox("Fichiers PDF")
        file_layout = QVBoxLayout(file_group)
        
        self.file_label = QLabel("Aucun fichier sélectionné")
        self.file_label.setWordWrap(True)
        file_layout.addWidget(self.file_label)
        
        file_buttons_layout = QHBoxLayout()
        self.select_files_btn = QPushButton("Sélectionner fichiers")
        self.select_files_btn.clicked.connect(self.select_files)
        file_buttons_layout.addWidget(self.select_files_btn)
        
        self.clear_files_btn = QPushButton("Effacer")
        self.clear_files_btn.clicked.connect(self.clear_files)
        self.clear_files_btn.setEnabled(False)
        file_buttons_layout.addWidget(self.clear_files_btn)
        
        file_layout.addLayout(file_buttons_layout)

        # Ajout d'un layout pour les champs commande par fichier
        self.commande_fields_layout = QVBoxLayout()
        file_layout.addLayout(self.commande_fields_layout)

        layout.addWidget(file_group)
        
        # Groupe LLM
        llm_group = QGroupBox("Enrichissement LLM")
        llm_layout = QVBoxLayout(llm_group)
        
        self.enrich_llm_checkbox = QCheckBox("Utiliser l'enrichissement LLM")
        llm_layout.addWidget(self.enrich_llm_checkbox)
        
        # Provider LLM
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider:"))

        # Récupérer les providers avec une clé API
        from config import config
        providers_with_key = [p for p, key in config.get_all_llm_providers().items() if key.strip()]
        provider_list = ["ollama"] + [p for p in providers_with_key if p != "ollama"]

        self.llm_provider_combo = QComboBox()
        self.llm_provider_combo.addItems(provider_list)
        self.llm_provider_combo.currentTextChanged.connect(self.on_provider_changed)
        provider_layout.addWidget(self.llm_provider_combo)
        llm_layout.addLayout(provider_layout)

        # Synchronisation avec la config globale
        current_provider = config.get_current_llm_provider()
        if current_provider not in provider_list:
            current_provider = "ollama"
        index = self.llm_provider_combo.findText(current_provider)
        if index >= 0:
            self.llm_provider_combo.setCurrentIndex(index)
        
        # API Key OpenRouter
        self.api_key_label = QLabel("Clé API OpenRouter:")
        self.api_key_label.setVisible(False)
        llm_layout.addWidget(self.api_key_label)
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setVisible(False)
        self.api_key_input.setText(config.get_openrouter_api_key())
        llm_layout.addWidget(self.api_key_input)
        
        layout.addWidget(llm_group)
        
        # Groupe production
        prod_group = QGroupBox("Paramètres de production")
        prod_layout = QVBoxLayout(prod_group)
        
        # Semaine
        semaine_layout = QHBoxLayout()
        semaine_layout.addWidget(QLabel("Semaine:"))
        self.semaine_spin = QSpinBox()
        self.semaine_spin.setRange(1, 53)
        self.semaine_spin.setValue(config.get_last_semaine())
        semaine_layout.addWidget(self.semaine_spin)
        prod_layout.addLayout(semaine_layout)
        
        # Année
        annee_layout = QHBoxLayout()
        annee_layout.addWidget(QLabel("Année:"))
        self.annee_spin = QSpinBox()
        self.annee_spin.setRange(2020, 2030)
        self.annee_spin.setValue(config.get_last_annee())
        annee_layout.addWidget(self.annee_spin)
        prod_layout.addLayout(annee_layout)
        
        layout.addWidget(prod_group)
        
        # Groupe commande client
        cmd_group = QGroupBox("Commande client")
        self.cmd_layout = QVBoxLayout(cmd_group)
        
        layout.addWidget(cmd_group)
        
        # Bouton traitement
        self.process_btn = QPushButton("Traiter les fichiers")
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Barre de progression
        progress_group = QGroupBox("Progression")
        progress_layout = QVBoxLayout(progress_group)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setFormat("Traitement en cours... %p%")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        progress_layout.addWidget(self.progress_bar)
        
        # Label pour le statut détaillé
        self.progress_status_label = QLabel("Prêt")
        self.progress_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_status_label.setStyleSheet("color: green; font-weight: bold;")
        self.progress_status_label.setVisible(False)
        progress_layout.addWidget(self.progress_status_label)
        
        layout.addWidget(progress_group)
        
        # Espace flexible
        layout.addStretch()
        
        return left_widget
    
    def create_menu_bar(self):
        """Crée la barre de menu de l'application"""
        menubar = self.menuBar()
        
        # Menu Fichier
        file_menu = menubar.addMenu('&Fichier')
        
        # Action Ouvrir fichiers
        open_action = QAction('&Ouvrir fichiers PDF...', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Ouvrir des fichiers PDF pour traitement')
        open_action.triggered.connect(self.select_files)
        file_menu.addAction(open_action)
        
        # Séparateur
        file_menu.addSeparator()
        
        # Action Quitter
        quit_action = QAction('&Quitter', self)
        quit_action.setShortcut('Ctrl+Q')
        quit_action.setStatusTip('Quitter l\'application')
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Menu Traitement
        process_menu = menubar.addMenu('&Traitement')
        
        # Action Traiter les fichiers
        process_action = QAction('&Traiter les fichiers', self)
        process_action.setShortcut('F5')
        process_action.setStatusTip('Lancer le traitement des fichiers sélectionnés')
        process_action.triggered.connect(self.process_files)
        process_menu.addAction(process_action)
        
        # Action Arrêter le traitement
        self.stop_action = QAction('&Arrêter le traitement', self)
        self.stop_action.setShortcut('F6')
        self.stop_action.setStatusTip('Arrêter le traitement en cours')
        self.stop_action.triggered.connect(self.stop_processing)
        self.stop_action.setEnabled(False)
        process_menu.addAction(self.stop_action)
        
        # Menu Aide
        help_menu = menubar.addMenu('&Aide')
        
        # Action Guide d'aide complet
        help_action = QAction('&Guide d\'aide complet', self)
        help_action.setShortcut('F1')
        help_action.setStatusTip('Ouvrir le guide d\'aide complet')
        help_action.triggered.connect(self.show_help_guide)
        help_menu.addAction(help_action)
        

        
        # Action Gestionnaire de clés API (supprimé car doublon avec Réglages)
        # if SECURE_STORAGE_AVAILABLE:
        #     api_keys_action = QAction('🔐 &Gestionnaire de Clés API', self)
        #     api_keys_action.setShortcut('F3')
        #     api_keys_action.setStatusTip('Gérer les clés API de manière sécurisée')
        #     api_keys_action.triggered.connect(self.show_api_key_manager)
        #     help_menu.addAction(api_keys_action)
        
        # Action Contrat d'utilisation
        eula_action = QAction("&Contrat d'utilisation", self)
        eula_action.setStatusTip("Afficher le contrat d'utilisation (EULA)")
        eula_action.triggered.connect(self.show_eula)
        help_menu.addAction(eula_action)
        
        # Action À propos
        about_action = QAction('&À propos', self)
        about_action.setStatusTip('Informations sur l\'application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
        # Barre de statut avancée
        self.create_advanced_status_bar()
        
        # Menu Réglages
        settings_menu = menubar.addMenu('&Réglages')
        
        # Action Paramètres généraux
        general_settings_action = QAction('⚙️ Paramètres généraux', self)
        general_settings_action.setStatusTip('Configurer les paramètres généraux de l\'application')
        general_settings_action.triggered.connect(self.show_general_settings_dialog)
        settings_menu.addAction(general_settings_action)
        
        # Séparateur
        settings_menu.addSeparator()
        
        # Action Classement des noyaux
        noyau_order_action = QAction('Classer l\'ordre des noyaux', self)
        noyau_order_action.setStatusTip('Définir l\'ordre d\'écriture des noyaux dans Excel')
        noyau_order_action.triggered.connect(self.show_noyau_order_dialog)
        settings_menu.addAction(noyau_order_action)
        
        # Action Configuration des Providers LLM
        api_keys_action = QAction('🔧 Configuration des Providers LLM', self)
        api_keys_action.setStatusTip('Configurer les providers LLM et leurs clés API')
        api_keys_action.triggered.connect(self.show_api_keys_dialog)
        settings_menu.addAction(api_keys_action)
        
        # Séparateur
        settings_menu.addSeparator()
        
        # Action Tests automatisés
        tests_action = QAction('🧪 Tests automatisés', self)
        tests_action.setStatusTip('Accéder aux tests automatisés')
        tests_action.triggered.connect(self.show_tests_dialog)
        settings_menu.addAction(tests_action)
        
        # Action Coût OpenRouter
        cost_action = QAction('💰 Coût OpenRouter', self)
        cost_action.setStatusTip('Surveiller les coûts et limites OpenRouter')
        cost_action.triggered.connect(self.show_cost_dialog)
        settings_menu.addAction(cost_action)
        
        # Séparateur
        settings_menu.addSeparator()
        
        # Action Maintenance - Documentation
        maintenance_action = QAction('📚 Maintenance - Documentation', self)
        maintenance_action.setStatusTip('Accéder à la documentation de maintenance (fichiers Markdown)')
        maintenance_action.triggered.connect(self.show_maintenance_dialog)
        settings_menu.addAction(maintenance_action)
        
        # Séparateur
        settings_menu.addSeparator()
        
        # Action Configuration des mappings Excel
        mapping_action = QAction('📊 Configuration des mappings Excel', self)
        mapping_action.setStatusTip('Configurer les mappings entre champs pré-import et cellules Excel')
        mapping_action.triggered.connect(self.show_mapping_config_dialog)
        settings_menu.addAction(mapping_action)
        
        # Action Gestionnaire de mises à jour
        update_action = QAction('🔄 Gestionnaire de mises à jour', self)
        update_action.setStatusTip('Gérer les versions et appliquer les patches')
        update_action.triggered.connect(self.show_update_manager)
        settings_menu.addAction(update_action)
    
    def create_advanced_status_bar(self):
        status_bar = QStatusBar(self)
        self.setStatusBar(status_bar)
        
        # Informations sur les fichiers et résultats
        self.files_info = QLabel("Fichiers: 0")
        self.results_info = QLabel("Résultats: 0 config, 0 pré-import, 0 Excel")
        status_bar.addWidget(self.files_info)
        status_bar.addWidget(self.results_info)
        
        # Séparateur
        separator1 = QLabel(" | ")
        separator1.setStyleSheet("color: gray;")
        status_bar.addWidget(separator1)
        
        # État de la connexion internet
        self.internet_status_label = QLabel()
        status_bar.addWidget(self.internet_status_label)
        
        # Séparateur
        separator2 = QLabel(" | ")
        separator2.setStyleSheet("color: gray;")
        status_bar.addWidget(separator2)
        
        # Répertoire de sortie Excel
        self.excel_output_label = QLabel()
        status_bar.addWidget(self.excel_output_label)
        
        # Séparateur
        separator3 = QLabel(" | ")
        separator3.setStyleSheet("color: gray;")
        status_bar.addWidget(separator3)
        
        # Provider LLM
        self.provider_status_label = QLabel()
        status_bar.addPermanentWidget(self.provider_status_label)
        
        # Initialisation des statuts
        self.update_provider_status()
        self.update_internet_status()
        self.update_excel_output_status()
        
        # Timer pour mettre à jour l'état de la connexion internet
        self.internet_timer = QTimer()
        self.internet_timer.timeout.connect(self.update_internet_status)
        self.internet_timer.start(30000)  # Vérifier toutes les 30 secondes
        
        return status_bar

    def update_provider_status(self):
        from config import config
        provider = config.get_current_llm_provider()
        provider_display = {
            "openai": "OpenAI",
            "anthropic": "Anthropic",
            "gemini": "Gemini",
            "mistral": "Mistral",
            "openrouter": "OpenRouter",
            "ollama": "Ollama"
        }.get(provider, provider)
        self.provider_status_label.setText(f"Provider LLM : {provider_display}")
    
    def update_internet_status(self):
        """Met à jour l'état de la connexion internet"""
        try:
            import urllib.request
            import socket
            
            # Test de connexion avec timeout
            socket.setdefaulttimeout(5)
            
            # Test avec un serveur fiable
            urllib.request.urlopen('http://www.google.com', timeout=5)
            
            self.internet_status_label.setText("🌐 Internet: Connecté")
            self.internet_status_label.setStyleSheet("color: green; font-weight: bold;")
            
        except Exception as e:
            self.internet_status_label.setText("🌐 Internet: Déconnecté")
            self.internet_status_label.setStyleSheet("color: red; font-weight: bold;")
    
    def update_excel_output_status(self):
        """Met à jour l'affichage du répertoire de sortie Excel"""
        try:
            from config import config
            output_dir = config.get_excel_output_directory()
            
            # Raccourcir le chemin pour l'affichage
            if len(output_dir) > 40:
                # Prendre le début et la fin du chemin
                parts = output_dir.split(os.sep)
                if len(parts) > 3:
                    shortened = os.sep.join(parts[:2] + ['...'] + parts[-2:])
                else:
                    shortened = output_dir
            else:
                shortened = output_dir
            
            # Compter les fichiers Excel existants
            excel_count = 0
            if os.path.exists(output_dir):
                excel_files = [f for f in os.listdir(output_dir) if f.endswith('.xlsx')]
                excel_count = len(excel_files)
            
            self.excel_output_label.setText(f"📁 Excel: {shortened} ({excel_count} fichiers)")
            self.excel_output_label.setStyleSheet("color: blue;")
            
        except Exception as e:
            self.excel_output_label.setText("📁 Excel: Erreur de configuration")
            self.excel_output_label.setStyleSheet("color: red;")
    
    def update_status_info(self):
        """Met à jour les informations de la barre de statut"""
        try:
            if not hasattr(self, 'files_info') or not hasattr(self, 'results_info'):
                return
                
            # Mise à jour des informations sur les fichiers
            files_count = len(self.selected_files)
            self.files_info.setText(f"Fichiers: {files_count}")
            
            # Mise à jour des informations sur les résultats
            config_count = len(self.all_configurations)
            preimport_count = len(self.all_preimport)
            excel_count = len(self.all_excel_files)
            self.results_info.setText(f"Résultats: {config_count} config, {preimport_count} pré-import, {excel_count} Excel")
            
            # Mise à jour du répertoire Excel
            self.update_excel_output_status()
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.debug(f"Erreur lors de la mise à jour du statut: {e}")
            else:
                print(f"Erreur lors de la mise à jour du statut: {e}")
    
    def update_status_indicator(self, status, color="green"):
        """Met à jour l'indicateur de statut"""
        try:
            if not hasattr(self, 'status_indicator'):
                return
                
            status_icons = {
                "ready": "🟢",
                "processing": "🟡", 
                "error": "🔴",
                "warning": "🟠",
                "success": "🟢"
            }
            
            status_colors = {
                "ready": "#e8f5e8",
                "processing": "#fff3cd",
                "error": "#f8d7da", 
                "warning": "#fff3cd",
                "success": "#d4edda"
            }
            
            icon = status_icons.get(status, "⚪")
            bg_color = status_colors.get(status, "#f8f9fa")
            
            self.status_indicator.setText(f"{icon} {status.title()}")
            self.status_indicator.setStyleSheet(f"font-weight: bold; padding: 2px 8px; border-radius: 3px; background-color: {bg_color};")
            
        except Exception as e:
            print(f"Erreur lors de la mise à jour de l'indicateur: {e}")
    
    def create_right_panel(self):
        """Crée le panneau de résultats à droite"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Titre
        title = QLabel("Résultats")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Onglets pour les résultats
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Onglet Résumé
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_tab)
        self.summary_text = QTextBrowser()  # QTextBrowser supporte nativement les liens hypertextes
        self.summary_text.setOpenExternalLinks(False)  # Désactiver l'ouverture automatique
        self.summary_text.anchorClicked.connect(self.open_excel_file)
        
        # Améliorer le style du texte
        self.summary_text.setStyleSheet("""
            QTextBrowser {
                font-family: Arial, sans-serif;
                font-size: 11px;
                line-height: 1.4;
                color: #333333;
                background-color: #ffffff;
            }
            QTextBrowser a {
                color: #0066cc;
                text-decoration: underline;
                font-weight: bold;
                font-size: 12px;
            }
            QTextBrowser a:hover {
                color: #003366;
                text-decoration: underline;
            }
        """)
        
        self.summary_layout.addWidget(self.summary_text)
        self.tabs.addTab(self.summary_tab, "Résumé")
        
        # Onglet Configurations avec sous-onglets
        self.config_tab = QWidget()
        self.config_layout = QVBoxLayout(self.config_tab)
        
        # Bouton pour effacer les résultats
        clear_btn = QPushButton("Effacer tous les résultats")
        clear_btn.clicked.connect(self.clear_results)
        self.config_layout.addWidget(clear_btn)
        
        # Sous-onglets pour matelas et sommiers
        self.config_subtabs = QTabWidget()
        self.config_layout.addWidget(self.config_subtabs)
        
        # Sous-onglet Matelas
        self.matelas_config_tab = QWidget()
        self.matelas_config_layout = QVBoxLayout(self.matelas_config_tab)
        self.matelas_config_table = QTableWidget()
        self.matelas_config_layout.addWidget(self.matelas_config_table)
        self.config_subtabs.addTab(self.matelas_config_tab, "Matelas")
        
        # Sous-onglet Sommiers
        self.sommiers_config_tab = QWidget()
        self.sommiers_config_layout = QVBoxLayout(self.sommiers_config_tab)
        self.sommiers_config_table = QTableWidget()
        self.sommiers_config_layout.addWidget(self.sommiers_config_table)
        self.config_subtabs.addTab(self.sommiers_config_tab, "Sommiers")
        
        self.tabs.addTab(self.config_tab, "Configurations")
        
        # Onglet Pré-import
        self.preimport_tab = QWidget()
        self.preimport_layout = QVBoxLayout(self.preimport_tab)
        self.preimport_table = QTableWidget()
        self.preimport_layout.addWidget(self.preimport_table)
        self.tabs.addTab(self.preimport_tab, "Pré-import")
        
        # Onglet JSON brut
        self.json_tab = QWidget()
        self.json_layout = QVBoxLayout(self.json_tab)
        self.json_text = QTextEdit()
        self.json_text.setReadOnly(True)
        self.json_layout.addWidget(self.json_text)
        self.tabs.addTab(self.json_tab, "JSON")
        
        # Onglet Fichiers Excel
        self.excel_tab = QWidget()
        self.excel_layout = QVBoxLayout(self.excel_tab)
        self.excel_text = QTextEdit()
        self.excel_text.setReadOnly(True)
        self.excel_layout.addWidget(self.excel_text)
        self.tabs.addTab(self.excel_tab, "Fichiers Excel")
        
        return right_widget
    
    def filter_logs(self):
        """Filtre les logs selon le niveau sélectionné"""
        level = getattr(logging, self.log_level_combo.currentText())
        self.log_handler.setLevel(level)
    
    def clear_logs(self):
        """Efface l'affichage des logs"""
        self.logs_browser.clear()
        self.app_logger.info("Logs effacés par l'utilisateur")
    

    

    
    def run_tests(self, test_type):
        """Lance l'exécution des tests"""
        try:
            if self.test_thread and self.test_thread.isRunning():
                QMessageBox.warning(self, "Tests en cours", "Des tests sont déjà en cours d'exécution")
                return
            
            # Récupération des options
            verbose = self.verbose_checkbox.isChecked()
            coverage = self.coverage_checkbox.isChecked()
            
            # Mise à jour de l'interface
            self.test_progress_bar.setVisible(True)
            self.test_progress_bar.setValue(0)
            self.tests_status_label.setText("Tests en cours d'exécution...")
            self.tests_status_label.setStyleSheet("color: orange; font-weight: bold;")
            
            # Désactiver les boutons
            self._set_test_buttons_enabled(False)
            
            # Créer et lancer le thread de test
            self.test_thread = TestThread(test_type, verbose, coverage)
            self.test_thread.test_progress.connect(self.on_test_progress)
            self.test_thread.test_output.connect(self.on_test_output)
            self.test_thread.test_finished.connect(self.on_test_finished)
            self.test_thread.test_error.connect(self.on_test_error)
            
            self.test_thread.start()
            
            if self.app_logger:
                self.app_logger.info(f"Démarrage des tests: {test_type}")
                
        except Exception as e:
            error_msg = f"Erreur lors du lancement des tests: {e}"
            self.tests_output.append(f"❌ {error_msg}")
            self.tests_status_label.setText("Erreur lors du lancement")
            self.tests_status_label.setStyleSheet("color: red; font-weight: bold;")
            self._set_test_buttons_enabled(True)
            if self.app_logger:
                self.app_logger.error(error_msg)
    
    def on_test_progress(self, value):
        """Gère la mise à jour de la progression des tests"""
        self.test_progress_bar.setValue(value)
    
    def on_test_output(self, message, level):
        """Gère la sortie des tests"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Couleurs selon le niveau
        color_map = {
            "INFO": "black",
            "WARNING": "orange",
            "ERROR": "red",
            "SUCCESS": "green"
        }
        color = color_map.get(level, "black")
        
        # Formatage du message
        formatted_message = f'<span style="color: {color}">[{timestamp}] {message}</span>'
        self.tests_output.append(formatted_message)
        
        # Auto-scroll vers le bas
        scrollbar = self.tests_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_test_finished(self, results):
        """Gère la fin des tests"""
        self.test_progress_bar.setVisible(False)
        self._set_test_buttons_enabled(True)
        
        # Analyser les résultats
        total_tests = len(results)
        successful_tests = sum(1 for r in results.values() if r.get('success', False))
        failed_tests = total_tests - successful_tests
        
        if failed_tests == 0:
            self.tests_status_label.setText(f"✅ Tests terminés: {successful_tests}/{total_tests} réussis")
            self.tests_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.on_test_output("🎉 Tous les tests ont réussi !", "SUCCESS")
        else:
            self.tests_status_label.setText(f"⚠️ Tests terminés: {successful_tests}/{total_tests} réussis, {failed_tests} échecs")
            self.tests_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.on_test_output(f"⚠️ {failed_tests} test(s) ont échoué", "WARNING")
        
        # Afficher un résumé des résultats
        self.on_test_output("", "INFO")
        self.on_test_output("=== RÉSUMÉ DES TESTS ===", "INFO")
        for test_name, result in results.items():
            status = "✅" if result.get('success', False) else "❌"
            self.on_test_output(f"{status} {test_name}", "INFO")
        
        if self.app_logger:
            self.app_logger.info(f"Tests terminés: {successful_tests}/{total_tests} réussis")
    
    def on_test_error(self, error_msg):
        """Gère les erreurs des tests"""
        self.test_progress_bar.setVisible(False)
        self._set_test_buttons_enabled(True)
        self.tests_status_label.setText("❌ Erreur lors des tests")
        self.tests_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.on_test_output(f"❌ Erreur: {error_msg}", "ERROR")
        
        if self.app_logger:
            self.app_logger.error(f"Erreur lors des tests: {error_msg}")
    
    def _set_test_buttons_enabled(self, enabled):
        """Active/désactive les boutons de test"""
        buttons = [
            self.install_deps_btn, self.all_tests_btn, self.unit_tests_btn,
            self.integration_tests_btn, self.performance_tests_btn, self.regression_tests_btn
        ]
        for btn in buttons:
            btn.setEnabled(enabled)
    
    def clear_tests_output(self):
        """Efface la sortie des tests"""
        self.tests_output.clear()
        self.on_test_output("Sortie des tests effacée", "INFO")
    
    def save_tests_output(self):
        """Sauvegarde la sortie des tests"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder la sortie des tests", "", "Fichiers texte (*.txt)"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.tests_output.toPlainText())
                self.on_test_output(f"Sortie des tests sauvegardée dans {filename}", "INFO")
                if self.app_logger:
                    self.app_logger.info(f"Sortie des tests sauvegardée dans {filename}")
        except Exception as e:
            error_msg = f"Erreur lors de la sauvegarde: {e}"
            self.on_test_output(f"❌ {error_msg}", "ERROR")
            if self.app_logger:
                self.app_logger.error(error_msg)
    
    def load_api_key_from_config(self):
        """Charge la clé API depuis la configuration ou le stockage sécurisé"""
        try:
            # Essayer d'abord le stockage sécurisé
            if SECURE_STORAGE_AVAILABLE:
                api_key = secure_storage.load_api_key("openrouter")
                if api_key:
                    self.api_key_input.setText(api_key)
                    if self.app_logger:
                        self.app_logger.info("Clé API OpenRouter chargée depuis le stockage sécurisé")
                    return
            
            # Fallback vers la configuration classique
            if hasattr(self, 'openrouter_api_key_input'):
                api_key = self.openrouter_api_key_input.text()
                if api_key:
                    self.api_key_input.setText(api_key)
                    if self.app_logger:
                        self.app_logger.info("Clé API OpenRouter chargée depuis la configuration")
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors du chargement de la clé API: {str(e)}")
    
    def refresh_openrouter_balance(self):
        """Récupère et affiche le solde OpenRouter"""
        try:
            api_key = self.api_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(self, "Clé API manquante", 
                                   "Veuillez entrer votre clé API OpenRouter")
                return
            
            self.cost_status_label.setText("Récupération du solde en cours...")
            self.cost_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.refresh_balance_btn.setEnabled(False)
            
            # Créer un thread pour la requête API
            self.balance_thread = BalanceThread(api_key)
            self.balance_thread.balance_ready.connect(self.on_balance_ready)
            self.balance_thread.balance_error.connect(self.on_balance_error)
            self.balance_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération du solde: {str(e)}")
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de la récupération du solde: {str(e)}")
    
    def on_balance_ready(self, balance_data):
        """Appelé quand le solde est récupéré avec succès"""
        try:
            print(f"💰 Balance data received: {balance_data}")
            
            # Mettre à jour l'interface avec gestion des valeurs None/0
            balance = balance_data.get('balance', 0)
            credits = balance_data.get('credits', 0)
            total_spent = balance_data.get('total_spent', 0)
            
            # Formatage des valeurs
            if balance is not None:
                self.balance_value.setText(f"{balance:.2f} crédits")
                if balance > 20:
                    self.balance_value.setStyleSheet("font-weight: bold; color: green;")
                elif balance > 5:
                    self.balance_value.setStyleSheet("font-weight: bold; color: orange;")
                else:
                    self.balance_value.setStyleSheet("font-weight: bold; color: red;")
            else:
                self.balance_value.setText("Non disponible")
                self.balance_value.setStyleSheet("font-weight: bold; color: orange;")
            
            if credits is not None:
                self.credits_value.setText(f"{credits:.2f} crédits")
                if credits < 50:
                    self.credits_value.setStyleSheet("font-weight: bold; color: green;")
                elif credits < 80:
                    self.credits_value.setStyleSheet("font-weight: bold; color: orange;")
                else:
                    self.credits_value.setStyleSheet("font-weight: bold; color: red;")
            else:
                self.credits_value.setText("Non disponible")
                self.credits_value.setStyleSheet("font-weight: bold; color: orange;")
            
            if total_spent is not None:
                self.total_spent_value.setText(f"{total_spent:.0f} crédits")
                self.total_spent_value.setStyleSheet("font-weight: bold; color: blue;")
            else:
                self.total_spent_value.setText("Non disponible")
                self.total_spent_value.setStyleSheet("font-weight: bold; color: orange;")
            
            # Message de statut
            if balance > 0 or credits > 0:
                self.cost_status_label.setText("Solde récupéré avec succès")
                self.cost_status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.cost_status_label.setText("Solde récupéré mais montant à 0")
                self.cost_status_label.setStyleSheet("color: orange; font-weight: bold;")
            
            self.refresh_balance_btn.setEnabled(True)
            
            if self.app_logger:
                self.app_logger.info(f"Solde OpenRouter récupéré: balance=${balance:.4f}, credits={credits:.2f}, spent=${total_spent:.4f}")
                
        except Exception as e:
            print(f"❌ Erreur dans on_balance_ready: {str(e)}")
            import traceback
            traceback.print_exc()
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage du solde: {str(e)}")
    
    def on_balance_error(self, error_msg):
        """Appelé en cas d'erreur lors de la récupération du solde"""
        QMessageBox.critical(self, "Erreur", f"Erreur lors de la récupération du solde: {error_msg}")
        self.cost_status_label.setText("Erreur lors de la récupération du solde")
        self.cost_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.refresh_balance_btn.setEnabled(True)
        
        if self.app_logger:
            self.app_logger.error(f"Erreur lors de la récupération du solde: {error_msg}")
    
    def calculate_cost(self):
        """Calcule le coût estimé pour un devis"""
        try:
            model = self.model_combo.currentText()
            tokens = self.tokens_input.value()
            
            # Prix par 1M tokens pour différents modèles (approximatifs)
            pricing = {
                "anthropic/claude-3.5-sonnet": {"input": 3.0, "output": 15.0},
                "anthropic/claude-3-opus": {"input": 15.0, "output": 75.0},
                "openai/gpt-4o": {"input": 5.0, "output": 15.0},
                "openai/gpt-4o-mini": {"input": 0.15, "output": 0.6},
                "meta-llama/llama-3.1-8b-instruct": {"input": 0.2, "output": 0.2},
                "meta-llama/llama-3.1-70b-instruct": {"input": 0.8, "output": 0.8}
            }
            
            if model in pricing:
                # Estimation: 70% input, 30% output
                input_tokens = int(tokens * 0.7)
                output_tokens = tokens - input_tokens
                
                input_cost = (input_tokens / 1_000_000) * pricing[model]["input"]
                output_cost = (output_tokens / 1_000_000) * pricing[model]["output"]
                total_cost = input_cost + output_cost
                
                self.cost_result_value.setText(f"${total_cost:.6f}")
                self.cost_result_value.setStyleSheet("font-weight: bold; color: purple;")
                
                # Ajouter à l'historique
                self.add_to_history(model, tokens, total_cost)
                
                if self.app_logger:
                    self.app_logger.info(f"Coût calculé pour {model}: ${total_cost:.6f} ({tokens} tokens)")
            else:
                QMessageBox.warning(self, "Modèle non supporté", 
                                   f"Le modèle {model} n'est pas dans la liste des prix connus")
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du calcul du coût: {str(e)}")
            if self.app_logger:
                self.app_logger.error(f"Erreur lors du calcul du coût: {str(e)}")
    
    def add_to_history(self, model, tokens, cost):
        """Ajoute une entrée à l'historique des coûts"""
        try:
            # Ajouter une nouvelle ligne au tableau
            row = self.history_table.rowCount()
            self.history_table.insertRow(row)
            
            # Remplir les colonnes
            self.history_table.setItem(row, 0, QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M")))
            self.history_table.setItem(row, 1, QTableWidgetItem(model))
            self.history_table.setItem(row, 2, QTableWidgetItem(str(tokens)))
            self.history_table.setItem(row, 3, QTableWidgetItem(f"${cost:.6f}"))
            
            # Calculer le total cumulé
            total = 0
            for i in range(self.history_table.rowCount()):
                cost_item = self.history_table.item(i, 3)
                if cost_item:
                    cost_text = cost_item.text().replace("$", "")
                    try:
                        total += float(cost_text)
                    except ValueError:
                        pass
            
            self.history_table.setItem(row, 4, QTableWidgetItem(f"${total:.6f}"))
            
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'ajout à l'historique: {str(e)}")
    
    def load_cost_history(self):
        """Charge l'historique des coûts depuis un fichier"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Charger l'historique des coûts", 
                "", "Fichiers CSV (*.csv);;Tous les fichiers (*)"
            )
            
            if filename:
                self.history_table.setRowCount(0)  # Vider le tableau
                
                with open(filename, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            parts = line.strip().split(',')
                            if len(parts) >= 4:
                                row = self.history_table.rowCount()
                                self.history_table.insertRow(row)
                                
                                for i, part in enumerate(parts[:4]):
                                    self.history_table.setItem(row, i, QTableWidgetItem(part))
                
                QMessageBox.information(self, "Historique chargé", 
                                       f"Historique des coûts chargé depuis {filename}")
                
                if self.app_logger:
                    self.app_logger.info(f"Historique des coûts chargé depuis {filename}")
                    
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement de l'historique: {str(e)}")
            if self.app_logger:
                self.app_logger.error(f"Erreur lors du chargement de l'historique: {str(e)}")
    
    def clear_cost_history(self):
        """Efface l'historique des coûts"""
        try:
            reply = QMessageBox.question(
                self, "Confirmation", 
                "Êtes-vous sûr de vouloir effacer tout l'historique des coûts ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.history_table.setRowCount(0)
                
                if self.app_logger:
                    self.app_logger.info("Historique des coûts effacé")
                    
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'effacement de l'historique: {str(e)}")
    
    def open_wallet(self):
        """Ouvre le portefeuille OpenRouter dans le navigateur"""
        try:
            import webbrowser
            
            # URL du portefeuille OpenRouter
            wallet_url = "https://openrouter.ai/account"
            
            # Ouvrir dans le navigateur par défaut
            webbrowser.open(wallet_url)
            
            if self.app_logger:
                self.app_logger.info("Portefeuille OpenRouter ouvert dans le navigateur")
                
            # Message de confirmation
            QMessageBox.information(
                self, 
                "Portefeuille Ouvert", 
                "Le portefeuille OpenRouter a été ouvert dans votre navigateur.\n\n"
                "Vous pouvez y voir votre vrai solde et gérer vos paiements."
            )
            
        except Exception as e:
            error_msg = f"Erreur lors de l'ouverture du portefeuille: {str(e)}"
            QMessageBox.critical(self, "Erreur", error_msg)
            if self.app_logger:
                self.app_logger.error(error_msg)
    
    def open_recharge(self):
        """Ouvre la page de recharge OpenRouter dans le navigateur"""
        try:
            import webbrowser
            
            # URL de recharge OpenRouter
            recharge_url = "https://openrouter.ai/account/billing"
            
            # Ouvrir dans le navigateur par défaut
            webbrowser.open(recharge_url)
            
            if self.app_logger:
                self.app_logger.info("Page de recharge OpenRouter ouverte dans le navigateur")
                
            # Message de confirmation
            QMessageBox.information(
                self, 
                "Recharge Ouverte", 
                "La page de recharge OpenRouter a été ouverte dans votre navigateur.\n\n"
                "Vous pouvez y ajouter des fonds à votre compte."
            )
            
        except Exception as e:
            error_msg = f"Erreur lors de l'ouverture de la page de recharge: {str(e)}"
            QMessageBox.critical(self, "Erreur", error_msg)
            if self.app_logger:
                self.app_logger.error(error_msg)
    
    def save_logs(self):
        """Sauvegarde les logs dans un fichier"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder les logs", "", "Fichiers texte (*.txt)"
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.logs_browser.toPlainText())
                self.app_logger.info(f"Logs sauvegardés dans {filename}")
                QMessageBox.information(self, "Succès", f"Logs sauvegardés dans {filename}")
        except Exception as e:
            self.app_logger.error(f"Erreur lors de la sauvegarde des logs: {e}")
            QMessageBox.critical(self, "Erreur", f"Impossible de sauvegarder les logs: {e}")
    
    def select_files(self):
        """Sélectionne les fichiers PDF"""
        try:
            files, _ = QFileDialog.getOpenFileNames(
                self,
                "Sélectionner les fichiers PDF",
                "",
                "PDF files (*.pdf)"
            )
            if files:
                self.selected_files = files
                self.file_label.setText(f"{len(files)} fichier(s) sélectionné(s):\n" + 
                                      "\n".join([os.path.basename(f) for f in files]))
                self.clear_files_btn.setEnabled(True)
                self.process_btn.setEnabled(True)
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info(f"Fichiers sélectionnés: {len(files)} fichiers")
                # Nettoyer les anciens champs commande dans cmd_layout
                if hasattr(self, 'commande_lineedits'):
                    self.commande_lineedits.clear()
                else:
                    self.commande_lineedits = []
                # Supprimer tous les widgets du layout commande client
                while self.cmd_layout.count():
                    item = self.cmd_layout.takeAt(0)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
                    else:
                        sublayout = item.layout()
                        if sublayout is not None:
                            while sublayout.count():
                                subitem = sublayout.takeAt(0)
                                subwidget = subitem.widget()
                                if subwidget is not None:
                                    subwidget.deleteLater()
                            del sublayout
                # Créer un champ par fichier dans cmd_layout
                for file in self.selected_files:
                    hbox = QHBoxLayout()
                    label = QLabel(f"Commande/Client pour {os.path.basename(file)} :")
                    lineedit = QLineEdit()
                    lineedit.setPlaceholderText("Nom du client")
                    hbox.addWidget(label)
                    hbox.addWidget(lineedit)
                    self.cmd_layout.addLayout(hbox)
                    self.commande_lineedits.append(lineedit)
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la sélection des fichiers: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la sélection des fichiers: {e}")
    
    def clear_files(self):
        """Efface la sélection de fichiers"""
        try:
            self.selected_files = []
            self.file_label.setText("Aucun fichier sélectionné")
            self.clear_files_btn.setEnabled(False)
            self.process_btn.setEnabled(False)
            # Nettoyer les champs commande
            if hasattr(self, 'commande_fields_layout'):
                for i in reversed(range(self.commande_fields_layout.count())):
                    item = self.commande_fields_layout.itemAt(i)
                    widget = item.widget()
                    if widget is not None:
                        widget.deleteLater()
            self.commande_lineedits = []
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info("Sélection de fichiers effacée")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'effacement des fichiers: {e}")
    
    def on_provider_changed(self, provider):
        """Gère le changement de provider LLM"""
        try:
            # Sauvegarder le provider dans la configuration
            config.set_current_llm_provider(provider)
            # Mettre à jour la barre de statut
            self.update_provider_status()
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Provider LLM changé: {provider}")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du changement de provider: {e}")
    
    def process_files(self):
        """Traite les fichiers sélectionnés"""
        try:
            if not self.selected_files:
                QMessageBox.warning(self, "Attention", "Aucun fichier sélectionné")
                return
            
            # Validation des fichiers
            for file_path in self.selected_files:
                if not os.path.exists(file_path):
                    raise FileNotFoundError(f"Fichier introuvable: {file_path}")
                if not file_path.lower().endswith('.pdf'):
                    raise ValueError(f"Fichier non PDF: {file_path}")
            
            # Récupération des paramètres
            enrich_llm = self.enrich_llm_checkbox.isChecked()
            llm_provider = self.llm_provider_combo.currentText()
            openrouter_api_key = self.api_key_input.text().strip() if llm_provider == "openrouter" else None
            semaine_prod = self.semaine_spin.value()
            annee_prod = self.annee_spin.value()
            # Récupérer un numéro de commande par fichier
            commande_client = [le.text().strip() for le in getattr(self, 'commande_lineedits', [])]
            if len(commande_client) != len(self.selected_files):
                raise ValueError("Veuillez saisir un numéro de commande pour chaque fichier.")
            if any(not cc for cc in commande_client):
                raise ValueError("Tous les champs Commande/Client doivent être remplis.")
            
            # Sauvegarde de la configuration
            try:
                config.set_last_semaine(semaine_prod)
                config.set_last_annee(annee_prod)
                config.set_last_commande_client(self.commande_input.text())
                if llm_provider == "openrouter" and openrouter_api_key:
                    config.set_openrouter_api_key(openrouter_api_key)
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Configuration sauvegardée")
            except Exception as e:
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.warning(f"Erreur lors de la sauvegarde de la configuration: {e}")
            
            # Validation LLM
            if llm_provider == "openrouter":
                if not openrouter_api_key:
                    raise ValueError("Clé API OpenRouter requise")
                # Nettoyer la clé API
                openrouter_api_key = openrouter_api_key.strip()
                if not openrouter_api_key.startswith("sk-or-"):
                    raise ValueError("Format de clé API OpenRouter invalide (doit commencer par 'sk-or-')")
            
            # Réinitialisation des résultats accumulés
            self.all_results = []
            self.all_configurations = []
            self.all_preimport = []
            self.all_excel_files = []
            
            # Désactivation de l'interface
            self.process_btn.setEnabled(False)
            self.stop_action.setEnabled(True)
            self.progress_bar.setVisible(True)
            self.progress_bar.setValue(0)
            self.progress_status_label.setVisible(True)
            self.progress_status_label.setText("Initialisation...")
            self.progress_status_label.setStyleSheet("color: blue; font-weight: bold;")
            
            # Mise à jour du statut
            self.update_status_indicator("processing")
            
            # Création et lancement du thread de traitement
            self.processing_thread = ProcessingThread(
                self.selected_files, enrich_llm, llm_provider, openrouter_api_key,
                semaine_prod, annee_prod, commande_client
            )
            self.processing_thread.progress_updated.connect(self.on_progress_updated)
            self.processing_thread.result_ready.connect(self.display_results)
            self.processing_thread.error_occurred.connect(self.handle_error)
            self.processing_thread.log_message.connect(self.log_message_to_text_browser)
            self.processing_thread.finished.connect(self.on_processing_finished)
            self.processing_thread.start()
            
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Début du traitement de {len(self.selected_files)} fichiers")
            
        except FileNotFoundError as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Fichier introuvable: {e}")
            QMessageBox.critical(self, "Erreur de fichier", str(e))
        except ValueError as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur de validation: {e}")
            QMessageBox.critical(self, "Erreur de validation", str(e))
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du lancement du traitement: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors du lancement du traitement:\n{str(e)}")
    
    def on_progress_updated(self, value):
        """Gère la mise à jour de la progression"""
        try:
            self.progress_bar.setValue(value)
            
            # Mise à jour du label de statut selon la progression
            if value <= 10:
                status_text = "Initialisation..."
                color = "blue"
            elif value <= 20:
                status_text = "Extraction du texte..."
                color = "orange"
            elif value <= 40:
                status_text = "Analyse du contenu..."
                color = "purple"
            elif value <= 60:
                if hasattr(self, 'enrich_llm_checkbox') and self.enrich_llm_checkbox.isChecked():
                    status_text = "Enrichissement IA..."
                    color = "magenta"
                else:
                    status_text = "Traitement des données..."
                    color = "purple"
            elif value <= 80:
                status_text = "Génération des configurations..."
                color = "darkgreen"
            elif value <= 95:
                status_text = "Finalisation..."
                color = "green"
            else:
                status_text = "Terminé !"
                color = "darkgreen"
            
            self.progress_status_label.setText(status_text)
            self.progress_status_label.setStyleSheet(f"color: {color}; font-weight: bold;")
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la mise à jour de la progression: {e}")
    
    def display_results(self, result):
        """Affiche les résultats du traitement"""
        try:
            # Validation du résultat
            if not isinstance(result, dict):
                raise ValueError("Format de résultat invalide")
            
            # Accumulation des résultats
            self.all_results.append(result)
            self.all_configurations.extend(result.get('configurations_matelas', []))
            self.all_configurations_sommiers.extend(result.get('configurations_sommiers', []))
            self.all_preimport.extend(result.get('pre_import', []))
            self.all_excel_files.extend(result.get('fichiers_excel', []))
            
            # Logs de débogage
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"DEBUG: Ajout du résultat pour {result.get('filename', 'N/A')}")
                self.app_logger.info(f"DEBUG: Configurations matelas dans ce résultat: {len(result.get('configurations_matelas', []))}")
                self.app_logger.info(f"DEBUG: Configurations sommiers dans ce résultat: {len(result.get('configurations_sommiers', []))}")
                self.app_logger.info(f"DEBUG: Total configurations matelas accumulées: {len(self.all_configurations)}")
                self.app_logger.info(f"DEBUG: Total configurations sommiers accumulées: {len(self.all_configurations_sommiers)}")
                self.app_logger.info(f"DEBUG: Total résultats accumulés: {len(self.all_results)}")
            
            # Mise à jour de l'affichage avec tous les résultats
            self.update_display()
            
            filename = result.get('filename', 'N/A')
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Résultats affichés pour {filename}")
            
        except ValueError as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Format de résultat invalide: {e}")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des résultats: {e}")
    
    def update_display(self):
        """Met à jour l'affichage avec tous les résultats accumulés"""
        try:
            # Logs de débogage
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"DEBUG: update_display appelé")
                self.app_logger.info(f"DEBUG: Nombre de résultats: {len(self.all_results)}")
                self.app_logger.info(f"DEBUG: Nombre de configurations matelas: {len(self.all_configurations)}")
                self.app_logger.info(f"DEBUG: Nombre de configurations sommiers: {len(self.all_configurations_sommiers)}")
                self.app_logger.info(f"DEBUG: Nombre de pré-import: {len(self.all_preimport)}")
                self.app_logger.info(f"DEBUG: Nombre de fichiers Excel: {len(self.all_excel_files)}")
            
            # Onglet Résumé
            summary = f"<h3>Résultats globaux ({len(self.all_results)} fichier(s) traité(s))</h3>"
            
            total_configs_matelas = len(self.all_configurations)
            total_configs_sommiers = len(self.all_configurations_sommiers)
            total_preimport = len(self.all_preimport)
            total_excel = len(self.all_excel_files)
            
            summary += f"<p><strong>📊 Total configurations matelas:</strong> {total_configs_matelas}</p>"
            summary += f"<p><strong>🛏️ Total configurations sommiers:</strong> {total_configs_sommiers}</p>"
            summary += f"<p><strong>📋 Total éléments pré-import:</strong> {total_preimport}</p>"
            summary += f"<p><strong>📁 Total fichiers Excel générés:</strong> {total_excel}</p>"
            
            summary += "<h4>Détail par fichier:</h4>"
            for i, result in enumerate(self.all_results, 1):
                filename = result.get('filename', 'N/A')
                status = result.get('status', 'N/A')
                configs = len(result.get('configurations_matelas', []))
                preimport = len(result.get('pre_import', []))
                excel = len(result.get('fichiers_excel', []))
                
                summary += f"<p><strong>{i}. {filename}</strong><br>"
                summary += f"   Statut: {status}<br>"
                summary += f"   Configurations: {configs}<br>"
                summary += f"   Pré-import: {preimport}<br>"
                summary += f"   Excel: {excel}</p>"
            
            # Ajouter les liens hypertextes dans l'onglet Résumé
            if self.all_excel_files:
                summary += "<h4>📁 Fichiers Excel générés:</h4>"
                for fichier in self.all_excel_files:
                    # Créer un lien cliquable
                    file_path = os.path.abspath(fichier)
                    if os.path.exists(file_path):
                        summary += f"<p>🔗 <a href='file://{file_path}'>{os.path.basename(fichier)}</a></p>"
                    else:
                        summary += f"<p>⚠️ {os.path.basename(fichier)} (fichier non trouvé)</p>"
                summary += "<p><em>💡 Cliquez sur les liens pour ouvrir les fichiers Excel directement.</em></p>"
            
            # Configurer le QTextBrowser pour supporter les liens hypertextes
            self.summary_text.setText(summary)
            
            # Onglet Configurations
            self.display_configurations_matelas(self.all_configurations)
            self.display_configurations_sommiers(self.all_configurations_sommiers)
            
            # Onglet Pré-import
            self.display_preimport(self.all_preimport)
            
            # Onglet JSON
            try:
                json_text = json.dumps(self.all_results, indent=2, ensure_ascii=False)
                self.json_text.setText(json_text)
            except Exception as e:
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.error(f"Erreur lors de la sérialisation JSON: {e}")
                self.json_text.setText("Erreur lors de la sérialisation JSON")
            
            # Onglet Fichiers Excel
            if self.all_excel_files:
                excel_info = f"Fichiers Excel générés ({len(self.all_excel_files)} total):\n\n"
                for fichier in self.all_excel_files:
                    excel_info += f"✅ {fichier}\n"
            else:
                excel_info = "Aucun fichier Excel généré"
            self.excel_text.setText(excel_info)
            
            # Sélection de l'onglet résumé
            self.tabs.setCurrentIndex(0)
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la mise à jour de l'affichage: {e}")
            QMessageBox.warning(self, "Attention", f"Erreur lors de la mise à jour de l'affichage: {e}")
    

    def open_excel_file(self, url):
        """Ouvre un fichier Excel quand on clique sur un lien hypertexte"""
        try:
            # Extraire le chemin du fichier depuis l'URL
            file_path = url.toString()
            if file_path.startswith('file://'):
                file_path = file_path[7:]  # Enlever le préfixe 'file://'
            
            # Vérifier que le fichier existe
            if not os.path.exists(file_path):
                QMessageBox.warning(self, "Fichier non trouvé", f"Le fichier {os.path.basename(file_path)} n'existe pas.")
                return
            
            # Ouvrir le fichier avec l'application par défaut
            import subprocess
            import platform
            
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            elif system == "Windows":
                os.startfile(file_path)
            else:  # Linux
                subprocess.run(["xdg-open", file_path])
            
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Fichier Excel ouvert: {file_path}")
                
            # S'assurer que l'affichage de l'onglet Résumé reste inchangé
            # en forçant une mise à jour de l'affichage
            self.update_display()
                
        except Exception as e:
            error_msg = f"Erreur lors de l'ouverture du fichier Excel: {e}"
            QMessageBox.warning(self, "Erreur", error_msg)
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(error_msg)
    
    def display_configurations_matelas(self, configurations):
        """Affiche les configurations matelas dans un tableau dédié"""
        try:
            if not configurations:
                self.matelas_config_table.setRowCount(0)
                self.matelas_config_table.setColumnCount(0)
                return
            
            # Headers spécifiques aux matelas
            headers = ["Fichier", "Index", "Noyau", "Quantité", "Dimensions", "Housse", "Matière", "Hauteur", "Fermeté", "Poignées"]
            self.matelas_config_table.setColumnCount(len(headers))
            self.matelas_config_table.setHorizontalHeaderLabels(headers)
            self.matelas_config_table.setRowCount(len(configurations))
            
            for i, config in enumerate(configurations):
                # Fichier source
                filename = "N/A"
                for result in getattr(self, 'all_results', []):
                    if config in result.get('configurations_matelas', []):
                        filename = os.path.basename(result.get('filename', 'N/A'))
                        break
                self.matelas_config_table.setItem(i, 0, QTableWidgetItem(filename))
                
                # Index
                idx = config.get('matelas_index', '')
                self.matelas_config_table.setItem(i, 1, QTableWidgetItem(str(idx)))
                
                # Noyau
                noyau = config.get('noyau', '')
                self.matelas_config_table.setItem(i, 2, QTableWidgetItem(noyau))
                
                # Quantité
                self.matelas_config_table.setItem(i, 3, QTableWidgetItem(str(config.get('quantite', ''))))
                
                # Dimensions
                dims = config.get('dimensions', {})
                dim_str = f"{dims.get('largeur', '')}x{dims.get('longueur', '')}" if dims else ""
                self.matelas_config_table.setItem(i, 4, QTableWidgetItem(dim_str))
                
                # Housse
                self.matelas_config_table.setItem(i, 5, QTableWidgetItem(config.get('housse', '')))
                
                # Matière housse
                self.matelas_config_table.setItem(i, 6, QTableWidgetItem(config.get('matiere_housse', '')))
                
                # Hauteur
                self.matelas_config_table.setItem(i, 7, QTableWidgetItem(str(config.get('hauteur', ''))))
                
                # Fermeté
                self.matelas_config_table.setItem(i, 8, QTableWidgetItem(config.get('fermete', '')))
                
                # Poignées
                self.matelas_config_table.setItem(i, 9, QTableWidgetItem(config.get('poignees', '')))
            
            self.matelas_config_table.resizeColumnsToContents()
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des configurations matelas: {e}")

    def display_configurations_sommiers(self, configurations):
        """Affiche les configurations sommiers dans un tableau dédié"""
        try:
            if not configurations:
                self.sommiers_config_table.setRowCount(0)
                self.sommiers_config_table.setColumnCount(0)
                return
            
            # Headers spécifiques aux sommiers
            headers = ["Fichier", "Index", "Type", "Quantité", "Dimensions", "Matériau", "Hauteur", "Dans un lit", "Pieds"]
            self.sommiers_config_table.setColumnCount(len(headers))
            self.sommiers_config_table.setHorizontalHeaderLabels(headers)
            self.sommiers_config_table.setRowCount(len(configurations))
            
            for i, config in enumerate(configurations):
                # Fichier source
                filename = "N/A"
                for result in getattr(self, 'all_results', []):
                    if config in result.get('configurations_sommiers', []):
                        filename = os.path.basename(result.get('filename', 'N/A'))
                        break
                self.sommiers_config_table.setItem(i, 0, QTableWidgetItem(filename))
                
                # Index
                idx = config.get('sommier_index', '')
                self.sommiers_config_table.setItem(i, 1, QTableWidgetItem(str(idx)))
                
                # Type
                type_sommier = config.get('type_sommier', '')
                self.sommiers_config_table.setItem(i, 2, QTableWidgetItem(type_sommier))
                
                # Quantité
                self.sommiers_config_table.setItem(i, 3, QTableWidgetItem(str(config.get('quantite', ''))))
                
                # Dimensions
                dims = config.get('dimensions', {})
                dim_str = f"{dims.get('largeur', '')}x{dims.get('longueur', '')}" if dims else ""
                self.sommiers_config_table.setItem(i, 4, QTableWidgetItem(dim_str))
                
                # Matériau
                self.sommiers_config_table.setItem(i, 5, QTableWidgetItem(config.get('materiau', '')))
                
                # Hauteur
                self.sommiers_config_table.setItem(i, 6, QTableWidgetItem(str(config.get('hauteur', ''))))
                
                # Dans un lit
                self.sommiers_config_table.setItem(i, 7, QTableWidgetItem(config.get('sommier_dansunlit', '')))
                
                # Pieds
                self.sommiers_config_table.setItem(i, 8, QTableWidgetItem(config.get('sommier_pieds', '')))
            
            self.sommiers_config_table.resizeColumnsToContents()
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des configurations sommiers: {e}")

    def display_preimport(self, preimport_data):
        """Affiche les données de pré-import dans un tableau combiné matelas + sommiers"""
        try:
            if not preimport_data:
                self.preimport_table.setRowCount(0)
                self.preimport_table.setColumnCount(0)
                return
            
            # Headers combinés pour matelas et sommiers
            headers = ["Type", "Client", "Commande", "Semaine", "Noyau/Type", "Quantité", "Dimensions", "Hauteur", "Housse/Matériau"]
            self.preimport_table.setColumnCount(len(headers))
            self.preimport_table.setHorizontalHeaderLabels(headers)
            
            # Données
            self.preimport_table.setRowCount(len(preimport_data))
            for i, item in enumerate(preimport_data):
                try:
                    # Type d'article
                    type_article = item.get('type_article', 'matelas')
                    self.preimport_table.setItem(i, 0, QTableWidgetItem("Matelas" if type_article == 'matelas' else "Sommier"))
                    
                    # Données client communes
                    self.preimport_table.setItem(i, 1, QTableWidgetItem(item.get('Client_D1', '')))
                    self.preimport_table.setItem(i, 2, QTableWidgetItem(item.get('numero_D2', '')))
                    self.preimport_table.setItem(i, 3, QTableWidgetItem(item.get('semaine_D5', '')))
                    
                    # Noyau (matelas) ou Type (sommier)
                    if type_article == 'matelas':
                        noyau_type = item.get('noyau', '')
                    else:
                        noyau_type = item.get('Type_Sommier_D20', '')
                    self.preimport_table.setItem(i, 4, QTableWidgetItem(noyau_type))
                    
                    # Quantité
                    quantite = item.get('quantite', '') or item.get('Quantite_D40', '')
                    self.preimport_table.setItem(i, 5, QTableWidgetItem(str(quantite)))
                    
                    # Dimensions
                    if type_article == 'matelas':
                        # Dimensions matelas (jumeaux ou 1 pièce)
                        dims = item.get('jumeaux_D10', '') or item.get('1piece_D11', '')
                    else:
                        # Dimensions sommiers
                        dims = item.get('Dimensions_D35', '')
                    self.preimport_table.setItem(i, 6, QTableWidgetItem(dims))
                    
                    # Hauteur
                    if type_article == 'matelas':
                        hauteur = item.get('Hauteur_D22', '')
                    else:
                        hauteur = item.get('Hauteur_D30', '')
                    self.preimport_table.setItem(i, 7, QTableWidgetItem(str(hauteur)))
                    
                    # Housse (matelas) ou Matériau (sommier)
                    if type_article == 'matelas':
                        # Type de housse pour matelas
                        housse_type = ""
                        if item.get('HSimple_polyester_C13') == 'X': housse_type = "Simple Polyester"
                        elif item.get('HSimple_tencel_C14') == 'X': housse_type = "Simple Tencel"
                        elif item.get('Hmat_polyester_C17') == 'X': housse_type = "Matelassée Polyester"
                        elif item.get('Hmat_tencel_C18') == 'X': housse_type = "Matelassée Tencel"
                        elif item.get('Hmat_luxe3D_C19') == 'X': housse_type = "Matelassée Luxe 3D"
                        self.preimport_table.setItem(i, 8, QTableWidgetItem(housse_type))
                    else:
                        # Matériau pour sommiers
                        materiau = item.get('Materiau_D25', '')
                        self.preimport_table.setItem(i, 8, QTableWidgetItem(materiau))
                    
                except Exception as e:
                    if hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.error(f"Erreur lors de l'affichage du pré-import {i}: {e}")
                    # Remplir avec des valeurs par défaut en cas d'erreur
                    for j in range(9):
                        self.preimport_table.setItem(i, j, QTableWidgetItem("Erreur"))
            
            self.preimport_table.resizeColumnsToContents()
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage du pré-import: {e}")
    
    def clear_results(self):
        """Efface tous les résultats affichés"""
        try:
            self.all_results = []
            self.all_configurations = []
            self.all_configurations_sommiers = []
            self.all_preimport = []
            self.all_excel_files = []
            
            # Effacer l'affichage
            self.summary_text.clear()
            self.matelas_config_table.setRowCount(0)
            self.matelas_config_table.setColumnCount(0)
            self.sommiers_config_table.setRowCount(0)
            self.sommiers_config_table.setColumnCount(0)
            self.preimport_table.setRowCount(0)
            self.preimport_table.setColumnCount(0)
            self.json_text.clear()
            self.excel_text.clear()
            
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info("Tous les résultats ont été effacés")
            QMessageBox.information(self, "Résultats effacés", "Tous les résultats ont été effacés.")
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'effacement des résultats: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'effacement des résultats: {e}")
    
    def handle_error(self, error_msg):
        """Gère les erreurs de traitement"""
        try:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur de traitement: {error_msg}")
            self.update_status_indicator("error")
            QMessageBox.critical(self, "Erreur", f"Erreur lors du traitement:\n{error_msg}")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la gestion d'erreur: {e}")
    
    def on_processing_finished(self):
        """Appelé quand le traitement est terminé"""
        try:
            self.progress_bar.setVisible(False)
            self.progress_status_label.setVisible(False)
            self.process_btn.setEnabled(True)
            self.stop_action.setEnabled(False)
            
            # Mise à jour du statut selon le résultat
            if self.all_results:
                self.update_status_indicator("success")
                self.statusBar().showMessage('Traitement terminé avec succès')
            else:
                self.update_status_indicator("warning")
                self.statusBar().showMessage('Traitement terminé sans résultats')
            
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info("Traitement terminé")
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la finalisation du traitement: {e}")
            else:
                print(f"Erreur lors de la finalisation du traitement: {e}")
    
    def stop_processing(self):
        """Arrête le traitement en cours"""
        try:
            if self.processing_thread and self.processing_thread.isRunning():
                self.processing_thread.terminate()
                self.processing_thread.wait()
                self.on_processing_finished()
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Traitement arrêté par l'utilisateur")
                QMessageBox.information(self, "Information", "Traitement arrêté")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'arrêt du traitement: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'arrêt du traitement: {e}")
    
    def show_tests_tab(self):
        """Affiche l'onglet des tests automatisés"""
        try:
            # Basculer vers l'onglet Tests
            tests_index = self.tabs.indexOf(self.tests_tab)
            if tests_index >= 0:
                self.tabs.setCurrentIndex(tests_index)
                self.on_test_output("Onglet Tests ouvert", "INFO")
                if self.app_logger:
                    self.app_logger.info("Onglet Tests ouvert via le menu")
            else:
                QMessageBox.warning(self, "Onglet Tests introuvable", 
                                  "L'onglet Tests n'a pas été trouvé.")
        except Exception as e:
            error_msg = f"Erreur lors de l'ouverture de l'onglet Tests: {e}"
            QMessageBox.critical(self, "Erreur", error_msg)
            if self.app_logger:
                self.app_logger.error(error_msg)
    
    def show_api_key_manager(self):
        """Affiche le gestionnaire de clés API"""
        try:
            if not SECURE_STORAGE_AVAILABLE:
                QMessageBox.warning(
                    self, 
                    "Stockage Sécurisé Non Disponible",
                    "Le module de stockage sécurisé n'est pas disponible.\n\n"
                    "Pour activer cette fonctionnalité, installez la dépendance 'cryptography' :\n"
                    "pip install cryptography"
                )
                return
            
            # Ouvrir le dialogue de gestion des clés API
            dialog = ApiKeyManagerDialog(self)
            dialog.exec()
            
            # Recharger la clé API depuis le stockage sécurisé si nécessaire
            self.load_api_key_from_secure_storage()
            
            if self.app_logger:
                self.app_logger.info("Gestionnaire de clés API affiché")
                
        except Exception as e:
            error_msg = f"Erreur lors de l'affichage du gestionnaire de clés API: {str(e)}"
            self.handle_error(error_msg)
    
    def load_api_key_from_secure_storage(self):
        """Charge la clé API OpenRouter depuis le stockage sécurisé"""
        try:
            if not SECURE_STORAGE_AVAILABLE:
                return
            
            # Charger la clé OpenRouter depuis le stockage sécurisé
            api_key = secure_storage.load_api_key("openrouter")
            if api_key:
                self.api_key_input.setText(api_key)
                if self.app_logger:
                    self.app_logger.info("Clé API OpenRouter chargée depuis le stockage sécurisé")
            else:
                if self.app_logger:
                    self.app_logger.debug("Aucune clé API OpenRouter trouvée dans le stockage sécurisé")
                    
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors du chargement de la clé API depuis le stockage sécurisé: {str(e)}")
    
    def show_help_guide(self):
        """Affiche le guide d'aide complet dans une fenêtre dédiée, incluant l'aide sur les tests automatisés"""
        help_text = """
        <h1>Guide d'Utilisation Complet - Matelas Processor</h1>
        
        <div class="info-box">
            <strong>Bienvenue dans Matelas Processor</strong><br>
            Cette application professionnelle vous permet de traiter automatiquement les commandes PDF de matelas, 
            d'extraire les données, de créer des configurations et de générer des fichiers Excel pour l'import.
        </div>

        <h2>📋 Table des Matières</h2>
        <ul>
            <li><a href="#installation">Installation et Démarrage</a></li>
            <li><a href="#interface">Interface Utilisateur</a></li>
            <li><a href="#onglets">Guide des Onglets</a></li>
            <li><a href="#json">Utilisation des Fichiers JSON</a></li>
            <li><a href="#traitement">Traitement des Commandes PDF</a></li>
            <li><a href="#configuration">Configuration et Paramètres</a></li>
            <li><a href="#llm">Intégration des LLM (Ollama & OpenRouter)</a></li>
            <li><a href="#resultats">Gestion des Résultats</a></li>
            <li><a href="#tests">Tests Automatisés</a></li>
            <li><a href="#cout">Gestion des Coûts OpenRouter</a></li>
            <li><a href="#api-keys">Gestionnaire de Clés API Sécurisé</a></li>
            <li><a href="#depannage">Dépannage et Support</a></li>
        </ul>

        <h2 id="installation">🚀 Installation et Démarrage</h2>
        
        <h3>Première Utilisation</h3>
        <ul>
            <li><strong>Contrat d'utilisation :</strong> Lors du premier lancement, vous devrez accepter le contrat d'utilisation (EULA)</li>
            <li><strong>Licence :</strong> L'application vérifie automatiquement votre clé de licence</li>
            <li><strong>Splash screen :</strong> Un écran de chargement s'affiche pendant l'initialisation</li>
        </ul>

        <h3>Démarrage de l'Application</h3>
        <ul>
            <li>Double-cliquez sur <code>run_gui.py</code> ou <code>launch.py</code></li>
            <li>L'interface principale se charge avec tous les onglets disponibles</li>
            <li>La barre de statut indique l'état de l'application</li>
        </ul>

        <h2 id="interface">🖥️ Interface Utilisateur</h2>

        <h3>Structure de l'Interface</h3>
        <div class="highlight">
            <strong>Panneau de Gauche :</strong> Configuration et paramètres de traitement<br>
            <strong>Panneau de Droite :</strong> Affichage des résultats et logs<br>
            <strong>Onglets :</strong> Traitement, Résultats, Pré-import, Tests, Logs
        </div>

        <h3>Menu Principal</h3>
        <ul>
            <li><strong>Fichier :</strong> Sauvegarde des logs, export des résultats</li>
            <li><strong>Traitement :</strong> Démarrer/arrêter le traitement</li>
            <li><strong>Aide :</strong> Guide d'aide, tests automatisés, contrat d'utilisation, à propos</li>
        </ul>

        <h3>Barre de Statut Avancée</h3>
        <ul>
            <li><strong>Indicateur de statut :</strong> Prêt, Traitement, Erreur</li>
            <li><strong>Informations système :</strong> Mémoire, CPU, espace disque</li>
            <li><strong>Messages de log :</strong> Derniers événements de l'application</li>
        </ul>

        <h2 id="onglets">📑 Guide des Onglets</h2>

        <div class="info-box">
            <strong>Navigation entre les onglets :</strong><br>
            L'interface utilise un système d'onglets pour organiser les différentes fonctionnalités. 
            Chaque onglet a un rôle spécifique dans le processus de traitement des commandes.
        </div>

        <h3>📋 Onglet "Traitement"</h3>
        
        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Onglet principal :</strong> Point d'entrée pour le traitement des commandes</li>
            <li><strong>Sélection des fichiers :</strong> Interface pour choisir les PDF à traiter</li>
            <li><strong>Configuration :</strong> Paramètres de production et LLM</li>
            <li><strong>Lancement :</strong> Bouton pour démarrer le traitement</li>
            <li><strong>Suivi :</strong> Barre de progression et statut en temps réel</li>
        </ul>

        <h4>Utilisation Détaillée</h4>
        <div class="highlight">
            <strong>Étapes d'utilisation :</strong>
            <ol>
                <li><strong>Sélection :</strong> Cliquez sur "Sélectionner des fichiers PDF"</li>
                <li><strong>Configuration :</strong> Remplissez semaine/année de production</li>
                <li><strong>LLM :</strong> Activez l'enrichissement et choisissez le fournisseur</li>
                <li><strong>Lancement :</strong> Cliquez sur "Traiter les fichiers"</li>
                <li><strong>Suivi :</strong> Surveillez la progression dans la barre</li>
            </ol>
        </div>

        <h4>Éléments de l'Interface</h4>
        <ul>
            <li><strong>Liste des fichiers :</strong> Affichage des PDF sélectionnés</li>
            <li><strong>Paramètres de production :</strong> Semaine, année, commande client</li>
            <li><strong>Configuration LLM :</strong> Case à cocher et sélection du fournisseur</li>
            <li><strong>Champ API :</strong> Saisie de la clé OpenRouter si nécessaire</li>
            <li><strong>Boutons d'action :</strong> Traiter, Arrêter, Effacer</li>
        </ul>

        <h3>📊 Onglet "Résultats"</h3>

        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Affichage des données :</strong> Résultats de l'extraction PDF</li>
            <li><strong>Validation :</strong> Vérification des informations extraites</li>
            <li><strong>Navigation :</strong> Parcours des différents résultats</li>
            <li><strong>Export :</strong> Sauvegarde des données traitées</li>
        </ul>

        <h4>Structure des Résultats</h4>
        <div class="success-box">
            <strong>Données affichées :</strong>
            <ul>
                <li><strong>Informations client :</strong> Nom, adresse, contact</li>
                <li><strong>Détails matelas :</strong> Type, dimensions, matériaux</li>
                <li><strong>Spécifications :</strong> Housse, fermeté, options</li>
                <li><strong>Prix et conditions :</strong> Montants, délais, garanties</li>
                <li><strong>Métadonnées :</strong> Date, numéro de commande, statut</li>
            </ul>
        </div>

        <h4>Actions Disponibles</h4>
        <ul>
            <li><strong>Navigation :</strong> Boutons précédent/suivant entre les résultats</li>
            <li><strong>Validation :</strong> Vérification visuelle des données</li>
            <li><strong>Correction :</strong> Modification manuelle si nécessaire</li>
            <li><strong>Export :</strong> Sauvegarde en format JSON ou Excel</li>
        </ul>

        <h3>📈 Onglet "Pré-import"</h3>

        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Formatage Excel :</strong> Préparation des données pour import</li>
            <li><strong>Validation :</strong> Vérification de la conformité des données</li>
            <li><strong>Optimisation :</strong> Structuration pour systèmes ERP</li>
            <li><strong>Prévisualisation :</strong> Aperçu avant export final</li>
        </ul>

        <h4>Données Pré-import</h4>
        <div class="info-box">
            <strong>Structure des données pré-import :</strong>
            <ul>
                <li><strong>Colonnes standardisées :</strong> Format compatible ERP</li>
                <li><strong>Données calculées :</strong> Dimensions, surfaces, volumes</li>
                <li><strong>Codes produits :</strong> Références normalisées</li>
                <li><strong>Prix calculés :</strong> Montants avec taxes et remises</li>
                <li><strong>Métadonnées :</strong> Informations de traçabilité</li>
            </ul>
        </div>

        <h4>Utilisation du Pré-import</h4>
        <ul>
            <li><strong>Vérification :</strong> Contrôle de la cohérence des données</li>
            <li><strong>Modification :</strong> Ajustement des valeurs si nécessaire</li>
            <li><strong>Validation :</strong> Confirmation avant export Excel</li>
            <li><strong>Export :</strong> Génération du fichier final</li>
        </ul>

        <h3>🧪 Onglet "Tests"</h3>

        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Tests automatisés :</strong> Validation du fonctionnement</li>
            <li><strong>Diagnostic :</strong> Détection des problèmes</li>
            <li><strong>Performance :</strong> Mesure des temps de traitement</li>
            <li><strong>Qualité :</strong> Vérification de la précision</li>
        </ul>

        <h4>Types de Tests Disponibles</h4>
        <ul>
            <li><strong>Tests unitaires :</strong> Vérification des fonctions individuelles</li>
            <li><strong>Tests d'intégration :</strong> Validation des interactions</li>
            <li><strong>Tests de performance :</strong> Mesure des performances</li>
            <li><strong>Tests de régression :</strong> Vérification de la stabilité</li>
        </ul>

        <h4>Interface des Tests</h4>
        <ul>
            <li><strong>Boutons de test :</strong> Lancement des différents types</li>
            <li><strong>Options :</strong> Mode verbeux, couverture de code</li>
            <li><strong>Progression :</strong> Barre de progression en temps réel</li>
            <li><strong>Résultats :</strong> Affichage coloré des résultats</li>
            <li><strong>Export :</strong> Sauvegarde des rapports de test</li>
        </ul>

        <h3>💰 Onglet "Coût OpenRouter"</h3>

        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Surveillance des coûts :</strong> Suivi des dépenses OpenRouter</li>
            <li><strong>Calcul de coûts :</strong> Estimation du coût par devis</li>
            <li><strong>Gestion du solde :</strong> Vérification du crédit disponible</li>
            <li><strong>Historique :</strong> Traçabilité des dépenses</li>
        </ul>

        <h4>Fonctionnalités Principales</h4>
        <div class="info-box">
            <strong>Configuration et Connexion :</strong>
            <ul>
                <li><strong>Clé API :</strong> Saisie sécurisée de la clé OpenRouter</li>
                <li><strong>Actualisation :</strong> Récupération en temps réel du solde</li>
                <li><strong>Synchronisation :</strong> Chargement automatique depuis la configuration</li>
            </ul>
        </div>

        <h4>Informations du Solde</h4>
        <ul>
            <li><strong>Limites de la Clé API :</strong> Limites restantes et utilisation de votre clé API</li>
            <li><strong>Solde Réel :</strong> Accès direct au portefeuille OpenRouter via le bouton "🏦 Voir Mon Portefeuille"</li>
            <li><strong>Recharge :</strong> Accès à la page de recharge via le bouton "💳 Recharger"</li>
            <li><strong>Note importante :</strong> Les limites affichées représentent les restrictions de votre clé API, pas votre solde réel</li>
        </ul>
        
        <h4>Accès au Portefeuille</h4>
        <div class="info-box">
            <strong>Pour voir votre vrai solde :</strong>
            <ul>
                <li><strong>Bouton "🏦 Voir Mon Portefeuille" :</strong> Ouvre directement votre compte OpenRouter dans le navigateur</li>
                <li><strong>Bouton "💳 Recharger" :</strong> Accès à la page de paiement pour ajouter des fonds</li>
                <li><strong>Lien direct :</strong> <a href="https://openrouter.ai/account" target="_blank">openrouter.ai/account</a></li>
                <li><strong>Sécurité :</strong> Le solde réel n'est pas accessible via l'API pour des raisons de sécurité</li>
            </ul>
        </div>

        <h4>Calcul de Coût par Devis</h4>
        <div class="success-box">
            <strong>Modèles supportés :</strong>
            <ul>
                <li><strong>Claude 3.5 Sonnet :</strong> $3.0/M tokens input, $15.0/M tokens output</li>
                <li><strong>Claude 3 Opus :</strong> $15.0/M tokens input, $75.0/M tokens output</li>
                <li><strong>GPT-4o :</strong> $5.0/M tokens input, $15.0/M tokens output</li>
                <li><strong>GPT-4o Mini :</strong> $0.15/M tokens input, $0.6/M tokens output</li>
                <li><strong>Llama 3.1 8B :</strong> $0.2/M tokens input/output</li>
                <li><strong>Llama 3.1 70B :</strong> $0.8/M tokens input/output</li>
            </ul>
        </div>

        <h4>Interface de Calcul</h4>
        <ul>
            <li><strong>Sélection du modèle :</strong> Choix dans la liste déroulante</li>
            <li><strong>Estimation des tokens :</strong> Saisie du nombre de tokens attendus</li>
            <li><strong>Calcul automatique :</strong> Estimation 70% input / 30% output</li>
            <li><strong>Résultat détaillé :</strong> Coût total en dollars</li>
        </ul>

        <h4>Historique des Coûts</h4>
        <ul>
            <li><strong>Tableau interactif :</strong> Affichage chronologique des calculs</li>
            <li><strong>Colonnes :</strong> Date, Modèle, Tokens, Coût, Total cumulé</li>
            <li><strong>Import/Export :</strong> Sauvegarde et chargement CSV</li>
            <li><strong>Gestion :</strong> Effacement sélectif ou complet</li>
        </ul>

        <h4>Utilisation Recommandée</h4>
        <div class="highlight">
            <strong>Workflow optimal :</strong>
            <ol>
                <li><strong>Configuration :</strong> Entrez votre clé API OpenRouter</li>
                <li><strong>Vérification :</strong> Actualisez votre solde</li>
                <li><strong>Estimation :</strong> Calculez le coût avant traitement</li>
                <li><strong>Surveillance :</strong> Suivez vos dépenses dans l'historique</li>
                <li><strong>Optimisation :</strong> Ajustez les paramètres selon le budget</li>
            </ol>
        </div>

        <h4>Conseils d'Optimisation</h4>
        <ul>
            <li><strong>Modèles économiques :</strong> Utilisez GPT-4o Mini pour les tests</li>
            <li><strong>Estimation précise :</strong> Ajustez le nombre de tokens selon vos PDF</li>
            <li><strong>Surveillance régulière :</strong> Vérifiez votre solde avant chaque lot</li>
            <li><strong>Historique :</strong> Gardez une trace pour optimiser les coûts</li>
        </ul>

        <h3>📝 Onglet "Logs"</h3>

        <h4>Rôle et Fonction</h4>
        <ul>
            <li><strong>Traçabilité :</strong> Historique complet des opérations</li>
            <li><strong>Debugging :</strong> Diagnostic des problèmes</li>
            <li><strong>Surveillance :</strong> Suivi de l'activité de l'application</li>
            <li><strong>Audit :</strong> Traçabilité pour la conformité</li>
        </ul>

        <h4>Types de Logs</h4>
        <div class="warning-box">
            <strong>Niveaux de log :</strong>
            <ul>
                <li><strong>INFO :</strong> Informations générales (vert)</li>
                <li><strong>WARNING :</strong> Avertissements (jaune)</li>
                <li><strong>ERROR :</strong> Erreurs (rouge)</li>
                <li><strong>DEBUG :</strong> Informations de débogage (gris)</li>
            </ul>
        </div>

        <h4>Fonctionnalités des Logs</h4>
        <ul>
            <li><strong>Filtrage :</strong> Par niveau de log (INFO, WARNING, ERROR)</li>
            <li><strong>Recherche :</strong> Recherche textuelle dans les logs</li>
            <li><strong>Export :</strong> Sauvegarde des logs en fichier texte</li>
            <li><strong>Rotation :</strong> Gestion automatique de l'espace disque</li>
            <li><strong>Temps réel :</strong> Affichage en direct des événements</li>
        </ul>

        <h2 id="json">📄 Utilisation des Fichiers JSON</h2>

        <div class="info-box">
            <strong>Qu'est-ce que JSON ?</strong><br>
            JSON (JavaScript Object Notation) est un format de données léger et lisible utilisé pour 
            stocker et échanger des informations structurées. Dans Matelas Processor, les fichiers JSON 
            servent de référentiels et de configuration.
        </div>

        <h3>🗂️ Structure des Fichiers JSON</h3>

        <h4>Référentiels de Dimensions</h4>
        <ul>
            <li><strong>Fichier :</strong> <code>backend/Référentiels/dimensions_matelas.json</code></li>
            <li><strong>Contenu :</strong> Dimensions standardisées par type de matelas</li>
            <li><strong>Utilisation :</strong> Validation et calcul automatique des dimensions</li>
        </ul>

        <h4>Référentiels de Longueurs</h4>
        <ul>
            <li><strong>Fichier :</strong> <code>backend/Référentiels/longueurs_matelas.json</code></li>
            <li><strong>Contenu :</strong> Longueurs disponibles par type de matelas</li>
            <li><strong>Utilisation :</strong> Calcul des housses et matériaux</li>
        </ul>

        <h4>Référentiels Spécialisés</h4>
        <div class="success-box">
            <strong>Fichiers par type de matelas :</strong>
            <ul>
                <li><strong>Latex Mixte 7 Zones :</strong> <code>latex_mixte7zones_*.json</code></li>
                <li><strong>Latex Naturel :</strong> <code>latex_naturel_*.json</code></li>
                <li><strong>Latex Renforcé :</strong> <code>latex_renforce_*.json</code></li>
                <li><strong>Mousse Viscoélastique :</strong> <code>mousse_visco_*.json</code></li>
                <li><strong>Mousse Rainurée 7 Zones :</strong> <code>mousse_rainuree7zones_*.json</code></li>
                <li><strong>Select 43 :</strong> <code>select43_*.json</code></li>
            </ul>
        </div>

        <h3>📋 Structure d'un Fichier JSON</h3>

        <h4>Exemple de Référentiel</h4>
        <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 5px; overflow-x: auto;">
{
    "type_matelas": "latex_mixte_7zones",
    "version": "1.0",
    "description": "Référentiel pour matelas latex mixte 7 zones",
    "dimensions": {
        "largeur": [80, 90, 100, 120, 140, 160, 180, 200],
        "longueur": [190, 200, 210, 220],
        "hauteur": [18, 20, 22, 24, 26, 28, 30]
    },
    "materiaux": {
        "housse": ["Tencel", "Luxe3D", "Tencel Polyester"],
        "densite": [65, 75, 85, 95],
        "fermete": ["Doux", "Moyen", "Ferme", "Très ferme"]
    },
    "calculs": {
        "surface_formule": "largeur * longueur / 10000",
        "volume_formule": "largeur * longueur * hauteur / 1000000",
        "poids_formule": "volume * densite / 1000"
    }
}</pre>

        <h3>🔧 Utilisation des JSON dans l'Application</h3>

        <h4>Chargement Automatique</h4>
        <ul>
            <li><strong>Détection du type :</strong> L'application identifie automatiquement le type de matelas</li>
            <li><strong>Chargement du référentiel :</strong> Le fichier JSON correspondant est chargé</li>
            <li><strong>Validation :</strong> Les données extraites sont validées contre le référentiel</li>
            <li><strong>Calculs :</strong> Les formules du JSON sont appliquées automatiquement</li>
        </ul>

        <h4>Validation des Données</h4>
        <div class="highlight">
            <strong>Processus de validation :</strong>
            <ol>
                <li><strong>Extraction :</strong> Données extraites du PDF</li>
                <li><strong>Référencement :</strong> Chargement du JSON correspondant</li>
                <li><strong>Validation :</strong> Vérification des valeurs autorisées</li>
                <li><strong>Correction :</strong> Ajustement automatique si nécessaire</li>
                <li><strong>Calculs :</strong> Application des formules de calcul</li>
            </ol>
        </div>

        <h4>Calculs Automatiques</h4>
        <ul>
            <li><strong>Surface :</strong> Calcul automatique en m²</li>
            <li><strong>Volume :</strong> Calcul automatique en m³</li>
            <li><strong>Poids :</strong> Estimation basée sur la densité</li>
            <li><strong>Prix :</strong> Calcul selon les tarifs de référence</li>
        </ul>

        <h3>📝 Modification des Fichiers JSON</h3>

        <h4>Quand Modifier</h4>
        <ul>
            <li><strong>Nouveaux produits :</strong> Ajout de nouveaux types de matelas</li>
            <li><strong>Évolution des gammes :</strong> Modification des dimensions disponibles</li>
            <li><strong>Changement de tarifs :</strong> Mise à jour des prix</li>
            <li><strong>Nouvelles options :</strong> Ajout de matériaux ou finitions</li>
        </ul>

        <h4>Comment Modifier</h4>
        <div class="warning-box">
            <strong>Précautions importantes :</strong>
            <ul>
                <li><strong>Sauvegarde :</strong> Toujours faire une copie avant modification</li>
                <li><strong>Syntaxe :</strong> Respecter strictement la syntaxe JSON</li>
                <li><strong>Validation :</strong> Tester les modifications avec des fichiers de test</li>
                <li><strong>Versioning :</strong> Documenter les changements apportés</li>
            </ul>
        </div>

        <h4>Structure Recommandée</h4>
        <ul>
            <li><strong>En-tête :</strong> Type, version, description</li>
            <li><strong>Données :</strong> Valeurs autorisées et contraintes</li>
            <li><strong>Formules :</strong> Calculs automatiques</li>
            <li><strong>Métadonnées :</strong> Informations de traçabilité</li>
        </ul>

        <h3>🔍 Outils de Gestion JSON</h3>

        <h4>Éditeurs Recommandés</h4>
        <ul>
            <li><strong>Visual Studio Code :</strong> Éditeur gratuit avec support JSON</li>
            <li><strong>Notepad++ :</strong> Éditeur simple et efficace</li>
            <li><strong>Éditeurs en ligne :</strong> JSONLint, JSON Editor Online</li>
        </ul>

        <h4>Validation JSON</h4>
        <ul>
            <li><strong>Vérification syntaxe :</strong> Utilisation d'outils de validation</li>
            <li><strong>Tests fonctionnels :</strong> Vérification avec l'application</li>
            <li><strong>Tests de régression :</strong> Validation des calculs</li>
        </ul>

        <h3>📊 Export et Import JSON</h3>

        <h4>Export des Données</h4>
        <ul>
            <li><strong>Format JSON :</strong> Export des résultats en JSON</li>
            <li><strong>Structure :</strong> Données organisées et validées</li>
            <li><strong>Métadonnées :</strong> Informations de traçabilité incluses</li>
        </ul>

        <h4>Import de Données</h4>
        <ul>
            <li><strong>Validation :</strong> Vérification de la structure JSON</li>
            <li><strong>Intégration :</strong> Fusion avec les données existantes</li>
            <li><strong>Calculs :</strong> Application des formules de référence</li>
        </ul>

        <h2 id="traitement">📄 Traitement des Commandes PDF</h2>

        <h3>Étape 1 : Sélection des Fichiers</h3>
        <ul>
            <li>Cliquez sur <strong>"Sélectionner des fichiers PDF"</strong></li>
            <li>Sélectionnez un ou plusieurs fichiers PDF de commandes</li>
            <li>Les fichiers sélectionnés apparaissent dans la liste</li>
            <li>Utilisez <strong>"Effacer la liste"</strong> pour recommencer</li>
        </ul>

        <h3>Étape 2 : Configuration des Paramètres</h3>
        
        <h4>Paramètres de Production</h4>
        <ul>
            <li><strong>Semaine de production :</strong> Numéro de semaine (1-53)</li>
            <li><strong>Année de production :</strong> Année en cours ou future</li>
            <li><strong>Commande client :</strong> Numéro de commande personnalisé</li>
        </ul>

        <h4>Configuration LLM</h4>
        <ul>
            <li><strong>Enrichissement LLM :</strong> Active l'analyse intelligente des PDF</li>
            <li><strong>Fournisseur LLM :</strong> Ollama (local) ou OpenRouter (cloud)</li>
            <li><strong>Clé API OpenRouter :</strong> Requise si OpenRouter est sélectionné</li>
        </ul>

        <h3>Étape 3 : Lancement du Traitement</h3>
        <ul>
            <li>Vérifiez que tous les paramètres sont corrects</li>
            <li>Cliquez sur <strong>"Traiter les fichiers"</strong></li>
            <li>La barre de progression indique l'avancement</li>
            <li>Les logs s'affichent en temps réel</li>
        </ul>

        <h3>Types de Matelas Supportés</h3>
        <div class="success-box">
            <strong>Matelas Traités Automatiquement :</strong>
            <ul>
                <li><strong>Latex Mixte 7 Zones :</strong> Calcul automatique des dimensions et housses</li>
                <li><strong>Latex Naturel :</strong> Traitement spécialisé avec référentiels</li>
                <li><strong>Latex Renforcé :</strong> Gestion des renforts et dimensions</li>
                <li><strong>Mousse Viscoélastique :</strong> Calculs de densité et dimensions</li>
                <li><strong>Mousse Rainurée 7 Zones :</strong> Gestion des rainures et zones</li>
                <li><strong>Select 43 :</strong> Traitement spécialisé avec housses</li>
            </ul>
        </div>

        <h2 id="configuration">⚙️ Configuration et Paramètres</h2>

        <h3>Paramètres Avancés</h3>
        <ul>
            <li><strong>Mode enrichissement :</strong> Améliore la précision de l'extraction</li>
            <li><strong>Fournisseur LLM :</strong> Choix entre traitement local et cloud</li>
            <li><strong>Gestion des erreurs :</strong> Traitement robuste des cas particuliers</li>
        </ul>

        <h3>Fichiers de Configuration</h3>
        <ul>
            <li><strong>Référentiels :</strong> Stockés dans <code>backend/Référentiels/</code></li>
            <li><strong>Templates Excel :</strong> Dans <code>template/</code></li>
            <li><strong>Logs :</strong> Rotation automatique dans <code>logs/</code></li>
        </ul>

        <h2 id="llm">🤖 Intégration des LLM (Large Language Models)</h2>

        <div class="info-box">
            <strong>Qu'est-ce qu'un LLM ?</strong><br>
            Les Large Language Models (LLM) sont des modèles d'intelligence artificielle qui permettent 
            d'analyser et de comprendre le contenu textuel des PDF de commandes avec une précision élevée. 
            Ils améliorent significativement l'extraction automatique des données par rapport aux méthodes traditionnelles.
        </div>

        <h3>Fonctionnement de l'Enrichissement LLM</h3>
        <ul>
            <li><strong>Analyse intelligente :</strong> Le LLM lit et comprend le contenu des PDF comme un humain</li>
            <li><strong>Extraction contextuelle :</strong> Reconnaissance des dimensions, matériaux, et spécifications</li>
            <li><strong>Gestion des ambiguïtés :</strong> Résolution automatique des cas particuliers et exceptions</li>
            <li><strong>Validation des données :</strong> Vérification de la cohérence des informations extraites</li>
            <li><strong>Amélioration continue :</strong> Apprentissage à partir des corrections utilisateur</li>
        </ul>

        <h3>Activation de l'Enrichissement LLM</h3>
        <div class="highlight">
            <strong>Étapes pour activer l'enrichissement LLM :</strong>
            <ol>
                <li>Cochez la case <strong>"Enrichissement LLM"</strong> dans l'interface</li>
                <li>Sélectionnez votre fournisseur LLM (Ollama ou OpenRouter)</li>
                <li>Configurez les paramètres spécifiques au fournisseur choisi</li>
                <li>Lancez le traitement - l'analyse LLM se fait automatiquement</li>
            </ol>
        </div>

        <h3>🖥️ Ollama - Traitement Local</h3>
        
        <div class="success-box">
            <strong>Avantages d'Ollama :</strong>
            <ul>
                <li><strong>Gratuit :</strong> Aucun coût par devis ou par utilisation</li>
                <li><strong>Confidentialité totale :</strong> Données traitées localement, jamais envoyées sur internet</li>
                <li><strong>Performance :</strong> Traitement rapide sans latence réseau</li>
                <li><strong>Disponibilité :</strong> Fonctionne même sans connexion internet</li>
                <li><strong>Contrôle total :</strong> Modèles personnalisables selon vos besoins</li>
            </ul>
        </div>

        <h4>Installation et Configuration d'Ollama</h4>
        <ul>
            <li><strong>Téléchargement :</strong> Rendez-vous sur <a href="https://ollama.ai" target="_blank">ollama.ai</a></li>
            <li><strong>Installation :</strong> Suivez les instructions pour votre système d'exploitation</li>
            <li><strong>Téléchargement du modèle :</strong> <code>ollama pull llama2:7b</code> (recommandé)</li>
            <li><strong>Démarrage :</strong> Lancez Ollama en arrière-plan</li>
            <li><strong>Vérification :</strong> L'application détecte automatiquement Ollama</li>
        </ul>

        <h4>Modèles Recommandés pour Ollama</h4>
        <ul>
            <li><strong>llama2:7b :</strong> Équilibré performance/ressources (recommandé)</li>
            <li><strong>llama2:13b :</strong> Plus précis, nécessite plus de RAM</li>
            <li><strong>codellama:7b :</strong> Spécialisé dans l'analyse de documents</li>
            <li><strong>mistral:7b :</strong> Bon compromis vitesse/précision</li>
        </ul>

        <h4>Exigences Système pour Ollama</h4>
        <ul>
            <li><strong>RAM :</strong> Minimum 8GB, recommandé 16GB+</li>
            <li><strong>Stockage :</strong> 4-8GB pour les modèles</li>
            <li><strong>CPU :</strong> Processeur moderne (Intel i5/AMD Ryzen 5+)</li>
            <li><strong>GPU :</strong> Optionnel mais améliore les performances</li>
        </ul>

        <h3>☁️ OpenRouter - Traitement Cloud</h3>

        <div class="warning-box">
            <strong>Avantages d'OpenRouter :</strong>
            <ul>
                <li><strong>Modèles avancés :</strong> Accès aux derniers modèles (GPT-4, Claude, etc.)</li>
                <li><strong>Pas d'installation :</strong> Utilisation immédiate sans configuration locale</li>
                <li><strong>Performance garantie :</strong> Infrastructure cloud optimisée</li>
                <li><strong>Mise à jour automatique :</strong> Toujours les dernières versions des modèles</li>
                <li><strong>Scalabilité :</strong> Gestion automatique de la charge</li>
            </ul>
        </div>

        <h4>Configuration d'OpenRouter</h4>
        <ol>
            <li><strong>Création de compte :</strong> Inscrivez-vous sur <a href="https://openrouter.ai" target="_blank">openrouter.ai</a></li>
            <li><strong>Génération de clé API :</strong> Créez une clé API dans votre dashboard</li>
            <li><strong>Saisie de la clé :</strong> Entrez votre clé API dans l'application</li>
            <li><strong>Test de connexion :</strong> L'application vérifie automatiquement la validité</li>
        </ol>

        <h4>Modèles Disponibles sur OpenRouter</h4>
        <ul>
            <li><strong>GPT-4 :</strong> Le plus précis, coût élevé</li>
            <li><strong>GPT-3.5-turbo :</strong> Bon rapport qualité/prix</li>
            <li><strong>Claude-3 :</strong> Excellente compréhension de documents</li>
            <li><strong>Llama-2 :</strong> Alternative économique</li>
        </ul>

        <h3>💰 Comparaison des Coûts</h3>

        <h4>Ollama - Coûts</h4>
        <div class="success-box">
            <strong>Coût par devis : GRATUIT</strong>
            <ul>
                <li><strong>Installation :</strong> Gratuit</li>
                <li><strong>Utilisation :</strong> Gratuit</li>
                <li><strong>Modèles :</strong> Gratuits</li>
                <li><strong>Coût total :</strong> 0€ par devis</li>
            </ul>
        </div>

        <h4>OpenRouter - Coûts</h4>
        <div class="info-box">
            <strong>Coûts par devis (estimations) :</strong>
            <ul>
                <li><strong>GPT-4 :</strong> ~0.15-0.30€ par devis (très précis)</li>
                <li><strong>GPT-3.5-turbo :</strong> ~0.02-0.05€ par devis (recommandé)</li>
                <li><strong>Claude-3 :</strong> ~0.10-0.20€ par devis (excellent)</li>
                <li><strong>Llama-2 :</strong> ~0.01-0.03€ par devis (économique)</li>
            </ul>
            <em>Note : Les coûts varient selon la complexité du devis et la longueur du texte analysé</em>
        </div>

        <h4>Recommandations de Choix</h4>
        <ul>
            <li><strong>Débutant / Petit volume :</strong> Ollama (gratuit, simple)</li>
            <li><strong>Volume moyen :</strong> OpenRouter avec GPT-3.5-turbo</li>
            <li><strong>Haute précision requise :</strong> OpenRouter avec GPT-4 ou Claude-3</li>
            <li><strong>Budget limité :</strong> Ollama ou OpenRouter avec Llama-2</li>
        </ul>

        <h3>🔄 Comparaison Technique</h3>

        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr style="background-color: #f8f9fa;">
                <th style="border: 1px solid #dee2e6; padding: 12px; text-align: left;">Critère</th>
                <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">Ollama</th>
                <th style="border: 1px solid #dee2e6; padding: 12px; text-align: center;">OpenRouter</th>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Coût</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Gratuit</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #dc3545;">Payant</td>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Confidentialité</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Totale</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #ffc107;">Partielle</td>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Vitesse</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Rapide</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #17a2b8;">Variable</td>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Précision</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #17a2b8;">Bonne</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Excellente</td>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Installation</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #ffc107;">Requis</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Aucune</td>
            </tr>
            <tr>
                <td style="border: 1px solid #dee2e6; padding: 12px;"><strong>Internet</strong></td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #28a745;">Optionnel</td>
                <td style="border: 1px solid #dee2e6; padding: 12px; text-align: center; color: #dc3545;">Requis</td>
            </tr>
        </table>

        <h3>🎯 Conseils d'Optimisation</h3>

        <h4>Pour Ollama</h4>
        <ul>
            <li><strong>Choisissez le bon modèle :</strong> llama2:7b pour la plupart des cas</li>
            <li><strong>Optimisez la RAM :</strong> Fermez les applications inutiles</li>
            <li><strong>Utilisez un SSD :</strong> Améliore les temps de chargement des modèles</li>
            <li><strong>GPU optionnel :</strong> Accélère significativement le traitement</li>
        </ul>

        <h4>Pour OpenRouter</h4>
        <ul>
            <li><strong>Testez différents modèles :</strong> Trouvez le meilleur rapport qualité/prix</li>
            <li><strong>Surveillez les coûts :</strong> Utilisez le dashboard OpenRouter</li>
            <li><strong>Optimisez les prompts :</strong> Des prompts clairs réduisent les coûts</li>
            <li><strong>Planifiez l'utilisation :</strong> Traitez les devis par lots</li>
        </ul>

        <h3>🔧 Dépannage LLM</h3>

        <h4>Problèmes avec Ollama</h4>
        <div class="warning-box">
            <strong>Solutions courantes :</strong>
            <ul>
                <li><strong>Modèle non trouvé :</strong> <code>ollama pull llama2:7b</code></li>
                <li><strong>Mémoire insuffisante :</strong> Utilisez un modèle plus petit</li>
                <li><strong>Ollama ne démarre pas :</strong> Vérifiez l'installation et les permissions</li>
                <li><strong>Traitement lent :</strong> Vérifiez l'utilisation CPU/RAM</li>
            </ul>
        </div>

        <h4>Problèmes avec OpenRouter</h4>
        <div class="warning-box">
            <strong>Solutions courantes :</strong>
            <ul>
                <li><strong>Clé API invalide :</strong> Vérifiez la clé dans le dashboard OpenRouter</li>
                <li><strong>Quota dépassé :</strong> Surveillez votre consommation</li>
                <li><strong>Erreur de connexion :</strong> Vérifiez votre connexion internet</li>
                <li><strong>Modèle indisponible :</strong> Choisissez un modèle alternatif</li>
            </ul>
        </div>

        <h2 id="resultats">📊 Gestion des Résultats</h2>

        <h3>Onglet Résultats</h3>
        <ul>
            <li><strong>Données extraites :</strong> Affichage structuré des informations</li>
            <li><strong>Configurations :</strong> Paramètres calculés automatiquement</li>
            <li><strong>Pré-import :</strong> Données formatées pour Excel</li>
        </ul>

        <h3>Export et Sauvegarde</h3>
        <ul>
            <li><strong>Fichiers Excel :</strong> Générés automatiquement dans <code>output/</code></li>
            <li><strong>Logs :</strong> Sauvegarde via menu Fichier > Sauvegarder les logs</li>
            <li><strong>Résultats :</strong> Export possible des données traitées</li>
        </ul>

        <h3>Format des Fichiers de Sortie</h3>
        <div class="info-box">
            <strong>Structure des fichiers Excel générés :</strong>
            <ul>
                <li>Onglet <strong>Données :</strong> Informations extraites du PDF</li>
                <li>Onglet <strong>Configuration :</strong> Paramètres calculés</li>
                <li>Onglet <strong>Pré-import :</strong> Données formatées pour import</li>
                <li>Nommage : <code>Matelas_[Type]_[Référence]_[Numéro].xlsx</code></li>
            </ul>
        </div>

        <h3>🎯 Centrage des Cellules Excel</h3>
        <div class="success-box">
            <strong>Fonctionnalité automatique :</strong> L'application centre automatiquement les valeurs dans les cellules Excel pour une présentation professionnelle.
        </div>
        
        <h4>Modes de Centrage Disponibles</h4>
        <ul>
            <li><strong>Mode Intelligent (par défaut) :</strong> Alignement spécifique par type de données</li>
            <li><strong>Mode Global :</strong> Centrage de toutes les cellules</li>
            <li><strong>Mode None :</strong> Respect du formatage du template</li>
        </ul>

        <h4>Types de Données Centrées</h4>
        <ul>
            <li><strong>En-têtes :</strong> Client, adresse, numéro de commande</li>
            <li><strong>Dates :</strong> Semaine, lundi, vendredi</li>
            <li><strong>Dimensions :</strong> Hauteur, longueur, dimensions housse</li>
            <li><strong>Quantités :</strong> Jumeaux, 1 pièce</li>
            <li><strong>Types :</strong> Housse, noyau, fermeté</li>
            <li><strong>Opérations :</strong> Détection, surmatelas, transport</li>
        </ul>

        <h4>Avantages du Centrage</h4>
        <ul>
            <li><strong>Lisibilité :</strong> Présentation claire et organisée</li>
            <li><strong>Professionnalisme :</strong> Aspect soigné et cohérent</li>
            <li><strong>Standards Excel :</strong> Respect des conventions d'affichage</li>
            <li><strong>Efficacité :</strong> Lecture rapide des informations</li>
        </ul>

        <h2 id="tests">🧪 Tests Automatisés</h2>

        <h3>Accès aux Tests</h3>
        <ul>
            <li>Menu <strong>Aide > Tests automatisés</strong> ou raccourci <strong>F2</strong></li>
            <li>Onglet dédié <strong>🧪 Tests</strong> dans l'interface principale</li>
        </ul>

        <h3>Types de Tests Disponibles</h3>
        <ul>
            <li><strong>Tests Unitaires :</strong> Vérification des fonctions individuelles</li>
            <li><strong>Tests d'Intégration :</strong> Validation des interactions entre modules</li>
            <li><strong>Tests de Performance :</strong> Mesure des temps de traitement</li>
            <li><strong>Tests de Régression :</strong> Vérification de la stabilité</li>
            <li><strong>Tous les Tests :</strong> Exécution complète de la suite de tests</li>
        </ul>

        <h3>Options de Test</h3>
        <ul>
            <li><strong>Mode verbeux :</strong> Affichage détaillé des résultats</li>
            <li><strong>Rapport de couverture :</strong> Analyse de la couverture de code</li>
            <li><strong>Progression en temps réel :</strong> Suivi de l'avancement</li>
        </ul>

        <h3>Résultats des Tests</h3>
        <ul>
            <li><strong>Affichage coloré :</strong> Vert (succès), Rouge (échec), Jaune (avertissement)</li>
            <li><strong>Export des résultats :</strong> Sauvegarde des rapports de test</li>
            <li><strong>Logs détaillés :</strong> Traçabilité complète des exécutions</li>
        </ul>

        <h2 id="cout">💰 Gestion des Coûts OpenRouter</h2>

        <div class="info-box">
            <strong>Surveillance des dépenses :</strong><br>
            L'onglet "Coût OpenRouter" vous permet de surveiller vos dépenses, calculer les coûts estimés 
            et gérer votre budget pour l'utilisation des modèles LLM via OpenRouter.
        </div>

        <h3>Accès à l'Onglet Coût</h3>
        <ul>
            <li><strong>Onglet dédié :</strong> "💰 Coût OpenRouter" dans l'interface principale</li>
            <li><strong>Navigation :</strong> Clic sur l'onglet dans le panneau de droite</li>
            <li><strong>Intégration :</strong> Synchronisation automatique avec la configuration LLM</li>
        </ul>

        <h3>Configuration et Connexion</h3>
        
        <h4>Saisie de la Clé API</h4>
        <ul>
            <li><strong>Champ sécurisé :</strong> Saisie masquée de la clé OpenRouter</li>
            <li><strong>Chargement automatique :</strong> Récupération depuis la configuration LLM</li>
            <li><strong>Validation :</strong> Vérification de la validité de la clé</li>
        </ul>

        <h4>Actualisation du Solde</h4>
        <div class="highlight">
            <strong>Processus d'actualisation :</strong>
            <ol>
                <li>Entrez votre clé API OpenRouter</li>
                <li>Cliquez sur "🔄 Actualiser le solde"</li>
                <li>L'application récupère les informations en temps réel</li>
                <li>Les données sont affichées dans l'interface</li>
            </ol>
        </div>

        <h3>Informations du Solde</h3>
        
        <h4>Données Affichées</h4>
        <ul>
            <li><strong>Solde actuel :</strong> Montant disponible en dollars (précision 4 décimales)</li>
            <li><strong>Crédits restants :</strong> Nombre de crédits disponibles</li>
            <li><strong>Total dépensé :</strong> Historique cumulé des dépenses</li>
            <li><strong>Statut de connexion :</strong> Indicateur visuel de l'état</li>
        </ul>

        <h4>Interprétation des Données</h4>
        <div class="success-box">
            <strong>Guide d'interprétation :</strong>
            <ul>
                <li><strong>Solde élevé :</strong> Vous pouvez traiter de nombreux devis</li>
                <li><strong>Solde faible :</strong> Surveillez vos dépenses ou rechargez</li>
                <li><strong>Total dépensé :</strong> Aide à planifier le budget mensuel</li>
                <li><strong>Crédits :</strong> Certains modèles utilisent des crédits plutôt que des dollars</li>
            </ul>
        </div>

        <h3>Calcul de Coût par Devis</h3>

        <h4>Modèles Supportés et Tarifs</h4>
        <div class="info-box">
            <strong>Tarifs par million de tokens (approximatifs) :</strong>
            <ul>
                <li><strong>Claude 3.5 Sonnet :</strong> $3.0 input / $15.0 output</li>
                <li><strong>Claude 3 Opus :</strong> $15.0 input / $75.0 output</li>
                <li><strong>GPT-4o :</strong> $5.0 input / $15.0 output</li>
                <li><strong>GPT-4o Mini :</strong> $0.15 input / $0.6 output</li>
                <li><strong>Llama 3.1 8B :</strong> $0.2 input/output</li>
                <li><strong>Llama 3.1 70B :</strong> $0.8 input/output</li>
            </ul>
            <em>Note : Les tarifs peuvent varier selon OpenRouter et les conditions du marché</em>
        </div>

        <h4>Processus de Calcul</h4>
        <ul>
            <li><strong>Sélection du modèle :</strong> Choix dans la liste déroulante</li>
            <li><strong>Estimation des tokens :</strong> Saisie du nombre de tokens attendus</li>
            <li><strong>Répartition automatique :</strong> 70% input / 30% output (standard)</li>
            <li><strong>Calcul en temps réel :</strong> Affichage immédiat du coût estimé</li>
        </ul>

        <h4>Optimisation des Coûts</h4>
        <div class="warning-box">
            <strong>Conseils pour réduire les coûts :</strong>
            <ul>
                <li><strong>Modèles économiques :</strong> GPT-4o Mini ou Llama pour les tests</li>
                <li><strong>Estimation précise :</strong> Ajustez selon la complexité de vos PDF</li>
                <li><strong>Traitement par lots :</strong> Optimisez le nombre de tokens par requête</li>
                <li><strong>Surveillance régulière :</strong> Vérifiez les coûts avant chaque lot</li>
            </ul>
        </div>

        <h3>Historique des Coûts</h3>

        <h4>Fonctionnalités de l'Historique</h4>
        <ul>
            <li><strong>Tableau interactif :</strong> Affichage chronologique des calculs</li>
            <li><strong>Colonnes détaillées :</strong> Date, Modèle, Tokens, Coût, Total cumulé</li>
            <li><strong>Calcul automatique :</strong> Total cumulé mis à jour en temps réel</li>
            <li><strong>Tri et filtrage :</strong> Organisation des données par critères</li>
        </ul>

        <h4>Gestion de l'Historique</h4>
        <div class="highlight">
            <strong>Actions disponibles :</strong>
            <ul>
                <li><strong>Chargement CSV :</strong> Import d'historique depuis un fichier</li>
                <li><strong>Sauvegarde :</strong> Export des données en format CSV</li>
                <li><strong>Effacement :</strong> Suppression sélective ou complète</li>
                <li><strong>Analyse :</strong> Visualisation des tendances de coûts</li>
            </ul>
        </div>

        <h3>Workflow Recommandé</h3>
        
        <h4>Processus Optimal</h4>
        <ol>
            <li><strong>Configuration initiale :</strong> Entrez votre clé API OpenRouter</li>
            <li><strong>Vérification du solde :</strong> Actualisez pour connaître votre budget</li>
            <li><strong>Estimation préalable :</strong> Calculez le coût avant le traitement</li>
            <li><strong>Traitement :</strong> Lancez le traitement des PDF</li>
            <li><strong>Surveillance :</strong> Suivez les dépenses dans l'historique</li>
            <li><strong>Optimisation :</strong> Ajustez les paramètres selon les résultats</li>
        </ol>

        <h4>Alertes et Recommandations</h4>
        <ul>
            <li><strong>Solde faible :</strong> L'application vous avertit si le solde est insuffisant</li>
            <li><strong>Coûts élevés :</strong> Suggestions de modèles plus économiques</li>
            <li><strong>Optimisation :</strong> Conseils pour réduire les dépenses</li>
            <li><strong>Planification :</strong> Aide à la budgétisation mensuelle</li>
        </ul>

        <h3>Intégration avec le Traitement</h3>
        
        <h4>Synchronisation Automatique</h4>
        <ul>
            <li><strong>Clé API partagée :</strong> Utilisation de la même clé que le traitement LLM</li>
            <li><strong>Modèles cohérents :</strong> Sélection des mêmes modèles</li>
            <li><strong>Suivi en temps réel :</strong> Mise à jour automatique des coûts</li>
        </ul>

        <h4>Optimisation du Workflow</h4>
        <div class="success-box">
            <strong>Bonnes pratiques :</strong>
            <ul>
                <li><strong>Test avec Ollama :</strong> Utilisez Ollama pour les tests (gratuit)</li>
                <li><strong>Production avec OpenRouter :</strong> Utilisez OpenRouter pour la production</li>
                <li><strong>Surveillance continue :</strong> Vérifiez régulièrement vos dépenses</li>
                <li><strong>Archivage :</strong> Sauvegardez l'historique pour analyse</li>
            </ul>
        </div>

        <h2 id="api-keys">🔑 Gestionnaire de Clés API Sécurisé</h2>

        <div class="info-box">
            <strong>Fonctionnalité avancée de sécurité</strong><br>
            Le gestionnaire de clés API sécurisé vous permet de stocker et gérer vos clés API de manière 
            chiffrée et sécurisée, évitant ainsi de les saisir à chaque utilisation.
        </div>

        <h3>🔐 Accès au Gestionnaire</h3>
        <ul>
            <li><strong>Menu Aide :</strong> Aide → Gestionnaire de Clés API</li>
            <li><strong>Raccourci clavier :</strong> F3</li>
            <li><strong>Interface dédiée :</strong> Fenêtre modale sécurisée</li>
        </ul>

        <h3>🛡️ Fonctionnalités de Sécurité</h3>
        
        <h4>Chiffrement Avancé</h4>
        <div class="success-box">
            <strong>Protection des données :</strong>
            <ul>
                <li><strong>Chiffrement AES-256 :</strong> Algorithme de chiffrement militaire</li>
                <li><strong>Dérivation de clé PBKDF2 :</strong> Protection contre les attaques par force brute</li>
                <li><strong>Stockage local :</strong> Aucune transmission réseau des clés</li>
                <li><strong>Mot de passe maître :</strong> Protection par mot de passe configurable</li>
            </ul>
        </div>

        <h4>Services Supportés</h4>
        <ul>
            <li><strong>OpenRouter :</strong> Accès aux modèles LLM payants</li>
            <li><strong>Ollama :</strong> Modèles locaux gratuits</li>
            <li><strong>Anthropic :</strong> Claude et autres modèles</li>
            <li><strong>OpenAI :</strong> GPT-4, GPT-3.5 et autres</li>
            <li><strong>Google :</strong> Gemini et autres modèles Google</li>
            <li><strong>Custom :</strong> Services personnalisés</li>
        </ul>

        <h3>📋 Interface du Gestionnaire</h3>

        <h4>Tableau des Clés</h4>
        <div class="highlight">
            <strong>Colonnes disponibles :</strong>
            <ul>
                <li><strong>Service :</strong> Nom du service (OpenRouter, Ollama, etc.)</li>
                <li><strong>Description :</strong> Description optionnelle de la clé</li>
                <li><strong>Créée le :</strong> Date et heure de création</li>
                <li><strong>Actions :</strong> Boutons de modification et suppression</li>
            </ul>
        </div>

        <h4>Boutons d'Action</h4>
        <ul>
            <li><strong>➕ Ajouter une Clé :</strong> Création d'une nouvelle clé API</li>
            <li><strong>🔄 Actualiser :</strong> Rechargement de la liste</li>
            <li><strong>🧪 Tester Chiffrement :</strong> Vérification du système de sécurité</li>
            <li><strong>Fermer :</strong> Fermeture du gestionnaire</li>
        </ul>

        <h3>➕ Ajout d'une Clé API</h3>

        <h4>Dialogue d'Édition</h4>
        <ul>
            <li><strong>Service :</strong> Sélection dans la liste ou saisie personnalisée</li>
            <li><strong>Description :</strong> Description optionnelle pour identifier la clé</li>
            <li><strong>Clé API :</strong> Saisie de la clé (masquée par défaut)</li>
            <li><strong>👁️ Afficher :</strong> Bouton pour afficher/masquer la clé</li>
        </ul>

        <h4>Processus de Sauvegarde</h4>
        <div class="info-box">
            <strong>Étapes de chiffrement :</strong>
            <ol>
                <li><strong>Validation :</strong> Vérification du format de la clé</li>
                <li><strong>Chiffrement :</strong> Application du chiffrement AES-256</li>
                <li><strong>Stockage :</strong> Sauvegarde dans le fichier sécurisé</li>
                <li><strong>Confirmation :</strong> Message de succès</li>
            </ol>
        </div>

        <h3>✏️ Modification et Suppression</h3>

        <h4>Modification d'une Clé</h4>
        <ul>
            <li><strong>Bouton ✏️ :</strong> Ouverture du dialogue d'édition</li>
            <li><strong>Pré-remplissage :</strong> Données existantes chargées</li>
            <li><strong>Modification :</strong> Changement de la clé ou description</li>
            <li><strong>Sauvegarde :</strong> Mise à jour sécurisée</li>
        </ul>

        <h4>Suppression d'une Clé</h4>
        <div class="warning-box">
            <strong>Processus de suppression :</strong>
            <ul>
                <li><strong>Confirmation :</strong> Dialogue de confirmation obligatoire</li>
                <li><strong>Suppression sécurisée :</strong> Écrasement des données chiffrées</li>
                <li><strong>Irréversible :</strong> Action définitive</li>
                <li><strong>Actualisation :</strong> Mise à jour immédiate de l'interface</li>
            </ul>
        </div>

        <h3>🧪 Test de Chiffrement</h3>

        <h4>Fonction de Test</h4>
        <ul>
            <li><strong>Vérification :</strong> Test du système de chiffrement</li>
            <li><strong>Validation :</strong> Contrôle de l'intégrité des données</li>
            <li><strong>Rapport :</strong> Affichage du statut de sécurité</li>
        </ul>

        <h4>Messages de Test</h4>
        <div class="success-box">
            <strong>Test réussi :</strong> "✅ Le système de chiffrement fonctionne correctement. Vos clés API sont protégées de manière sécurisée."
        </div>
        <div class="warning-box">
            <strong>Test échoué :</strong> "❌ Le test de chiffrement a échoué. Vérifiez la configuration du stockage sécurisé."
        </div>

        <h3>🔧 Configuration Avancée</h3>

        <h4>Mot de Passe Maître</h4>
        <ul>
            <li><strong>Variable d'environnement :</strong> MATELAS_MASTER_PASSWORD</li>
            <li><strong>Mot de passe par défaut :</strong> Utilisé si non configuré</li>
            <li><strong>Sécurité renforcée :</strong> Recommandé en production</li>
        </ul>

        <h4>Intégration Automatique</h4>
        <div class="info-box">
            <strong>Chargement automatique :</strong>
            <ul>
                <li><strong>Au démarrage :</strong> Chargement des clés depuis le stockage sécurisé</li>
                <li><strong>Fallback :</strong> Utilisation de la configuration classique si nécessaire</li>
                <li><strong>Transparence :</strong> Aucune modification du workflow utilisateur</li>
            </ul>
        </div>

        <h3>⚠️ Bonnes Pratiques</h3>

        <h4>Sécurité</h4>
        <ul>
            <li><strong>Mot de passe fort :</strong> Utilisez un mot de passe maître complexe</li>
            <li><strong>Sauvegarde :</strong> Sauvegardez le fichier de stockage sécurisé</li>
            <li><strong>Accès limité :</strong> Restreignez l'accès au dossier de l'application</li>
            <li><strong>Rotation :</strong> Changez régulièrement vos clés API</li>
        </ul>

        <h4>Utilisation</h4>
        <ul>
            <li><strong>Test régulier :</strong> Vérifiez le système de chiffrement</li>
            <li><strong>Descriptions claires :</strong> Utilisez des descriptions explicites</li>
            <li><strong>Organisation :</strong> Gardez une liste à jour de vos clés</li>
            <li><strong>Nettoyage :</strong> Supprimez les clés obsolètes</li>
        </ul>

        <h3>🚨 Dépannage</h3>

        <h4>Problèmes Courants</h4>
        <div class="warning-box">
            <strong>Solutions :</strong>
            <ul>
                <li><strong>Erreur de chiffrement :</strong> Vérifiez le mot de passe maître</li>
                <li><strong>Clé non trouvée :</strong> Vérifiez que la clé est bien sauvegardée</li>
                <li><strong>Accès refusé :</strong> Vérifiez les permissions du dossier</li>
                <li><strong>Corruption :</strong> Restaurez depuis une sauvegarde</li>
            </ul>
        </div>

        <h2 id="depannage">🔧 Dépannage et Support</h2>

        <h3>Problèmes Courants</h3>
        
        <h4>Erreurs de Traitement</h4>
        <div class="warning-box">
            <strong>Solutions :</strong>
            <ul>
                <li>Vérifiez que les fichiers PDF sont lisibles et non corrompus</li>
                <li>Assurez-vous que la clé API OpenRouter est valide (si utilisée)</li>
                <li>Consultez les logs détaillés dans l'onglet Logs</li>
                <li>Redémarrez l'application si nécessaire</li>
            </ul>
        </div>

        <h4>Problèmes de Performance</h4>
        <ul>
            <li><strong>Traitement lent :</strong> Utilisez Ollama en local pour de meilleures performances</li>
            <li><strong>Mémoire insuffisante :</strong> Fermez d'autres applications</li>
            <li><strong>Espace disque :</strong> Vérifiez l'espace disponible dans le dossier output</li>
        </ul>

        <h3>Logs et Diagnostic</h3>
        <ul>
            <li><strong>Onglet Logs :</strong> Affichage en temps réel des événements</li>
            <li><strong>Filtrage :</strong> Par niveau (INFO, WARNING, ERROR)</li>
            <li><strong>Sauvegarde :</strong> Export des logs pour analyse</li>
            <li><strong>Rotation automatique :</strong> Gestion de l'espace disque</li>
        </ul>

        <h3>Support Technique</h3>
        <div class="info-box">
            <strong>En cas de problème :</strong>
            <ul>
                <li>Consultez d'abord ce guide d'aide</li>
                <li>Exécutez les tests automatisés pour diagnostiquer</li>
                <li>Sauvegardez les logs et résultats d'erreur</li>
                <li>Contactez le support technique avec les informations collectées</li>
            </ul>
        </div>

        <h2>📞 Raccourcis Clavier</h2>
        <ul>
            <li><strong>F1 :</strong> Guide d'aide complet</li>
            <li><strong>F2 :</strong> Tests automatisés</li>
            <li><strong>F3 :</strong> Gestionnaire de Clés API Sécurisé</li>
            <li><strong>Ctrl+O :</strong> Ouvrir des fichiers PDF</li>
            <li><strong>Ctrl+S :</strong> Sauvegarder les logs</li>
            <li><strong>Ctrl+Q :</strong> Quitter l'application</li>
        </ul>

        <h2>📁 Structure des Dossiers</h2>
        <ul>
            <li><strong>backend/ :</strong> Modules de traitement et logique métier</li>
            <li><strong>output/ :</strong> Fichiers Excel générés</li>
            <li><strong>logs/ :</strong> Fichiers de logs avec rotation</li>
            <li><strong>template/ :</strong> Templates Excel de référence</li>
            <li><strong>tests/ :</strong> Suite de tests automatisés</li>
            <li><strong>Commandes/ :</strong> Fichiers PDF de commandes</li>
        </ul>

        <div class="success-box">
            <strong>🎉 Vous êtes maintenant prêt à utiliser Matelas Processor efficacement !</strong><br>
            Cette application vous accompagne dans le traitement automatisé de vos commandes de matelas 
            avec précision et fiabilité.
        </div>
        """
        self.show_help_in_window(help_text)
    
    def show_help_in_window(self, help_content):
        """Affiche le guide d'aide dans le navigateur web"""
        try:
            # Créer un fichier HTML temporaire avec le contenu d'aide
            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>Guide d'Aide - Matelas Processor</title>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        line-height: 1.6;
                        margin: 0;
                        padding: 20px;
                        background-color: #f5f5f5;
                    }}
                    .container {{
                        max-width: 1000px;
                        margin: 0 auto;
                        background-color: white;
                        padding: 30px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h1, h2, h3 {{
                        color: #2c3e50;
                        border-bottom: 2px solid #3498db;
                        padding-bottom: 10px;
                    }}
                    h1 {{
                        text-align: center;
                        color: #2980b9;
                        font-size: 2.5em;
                        margin-bottom: 30px;
                    }}
                    h2 {{
                        color: #34495e;
                        font-size: 1.8em;
                        margin-top: 30px;
                    }}
                    ul, ol {{
                        margin-left: 20px;
                    }}
                    li {{
                        margin-bottom: 8px;
                    }}
                    b {{
                        color: #2980b9;
                    }}
                    code {{
                        background-color: #ecf0f1;
                        padding: 2px 6px;
                        border-radius: 4px;
                        font-family: 'Courier New', monospace;
                    }}
                    .highlight {{
                        background-color: #fff3cd;
                        border: 1px solid #ffeaa7;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }}
                    .info-box {{
                        background-color: #d1ecf1;
                        border: 1px solid #bee5eb;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }}
                    .warning-box {{
                        background-color: #fff3cd;
                        border: 1px solid #ffeaa7;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }}
                    .success-box {{
                        background-color: #d4edda;
                        border: 1px solid #c3e6cb;
                        padding: 15px;
                        border-radius: 5px;
                        margin: 15px 0;
                    }}
                    a {{
                        color: #3498db;
                        text-decoration: none;
                        transition: color 0.3s ease;
                    }}
                    a:hover {{
                        color: #2980b9;
                        text-decoration: underline;
                    }}
                    .nav-link {{
                        cursor: pointer;
                        color: #3498db;
                        text-decoration: none;
                        transition: color 0.3s ease;
                    }}
                    .nav-link:hover {{
                        color: #2980b9;
                        text-decoration: underline;
                    }}
                    .back-to-top {{
                        position: fixed;
                        bottom: 20px;
                        right: 20px;
                        background-color: #3498db;
                        color: white;
                        padding: 10px 15px;
                        border-radius: 5px;
                        text-decoration: none;
                        cursor: pointer;
                        display: none;
                        z-index: 1000;
                    }}
                    .back-to-top:hover {{
                        background-color: #2980b9;
                    }}
                </style>
                <script>
                    // Gestion de la navigation interne
                    document.addEventListener('DOMContentLoaded', function() {{
                        // Gestion des liens de navigation
                        const navLinks = document.querySelectorAll('a[href^="#"]');
                        navLinks.forEach(link => {{
                            link.addEventListener('click', function(e) {{
                                e.preventDefault();
                                const targetId = this.getAttribute('href').substring(1);
                                const targetElement = document.getElementById(targetId);
                                if (targetElement) {{
                                    targetElement.scrollIntoView({{
                                        behavior: 'smooth',
                                        block: 'start'
                                    }});
                                }}
                            }});
                        }});

                        // Bouton "Retour en haut"
                        const backToTop = document.createElement('a');
                        backToTop.href = '#';
                        backToTop.className = 'back-to-top';
                        backToTop.textContent = '↑ Retour en haut';
                        backToTop.addEventListener('click', function(e) {{
                            e.preventDefault();
                            window.scrollTo({{
                                top: 0,
                                behavior: 'smooth'
                            }});
                        }});
                        document.body.appendChild(backToTop);

                        // Affichage/masquage du bouton "Retour en haut"
                        window.addEventListener('scroll', function() {{
                            if (window.pageYOffset > 300) {{
                                backToTop.style.display = 'block';
                            }} else {{
                                backToTop.style.display = 'none';
                            }}
                        }});

                        // Ajout d'un effet de surbrillance pour les sections
                        const sections = document.querySelectorAll('h2[id], h3[id]');
                        sections.forEach(section => {{
                            section.addEventListener('mouseenter', function() {{
                                this.style.backgroundColor = '#f8f9fa';
                                this.style.transition = 'background-color 0.3s ease';
                            }});
                            section.addEventListener('mouseleave', function() {{
                                this.style.backgroundColor = '';
                            }});
                        }});
                    }});
                </script>
            </head>
            <body>
                <div class="container">
                    {help_content}
                </div>
            </body>
            </html>
            """
            
            # Créer un fichier temporaire
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
                f.write(html_content)
                temp_file_path = f.name
            
            # Ouvrir le fichier dans le navigateur par défaut
            webbrowser.open(f'file://{temp_file_path}')
            
            # Nettoyer le fichier temporaire après un délai
            import threading
            import time
            def cleanup_temp_file():
                time.sleep(5)  # Attendre 5 secondes
                try:
                    os.unlink(temp_file_path)
                except:
                    pass  # Ignorer les erreurs de suppression
            
            cleanup_thread = threading.Thread(target=cleanup_temp_file, daemon=True)
            cleanup_thread.start()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le guide d'aide : {str(e)}")
    
    def show_about(self):
        """Affiche la boîte de dialogue À propos"""
        about_text = """
        <h2>Matelas Processor</h2>
        <p><b>Version :</b> 1.0.0</p>
        <p><b>Description :</b> Application de traitement automatisé de commandes de matelas</p>
        <p><b>Fonctionnalités :</b></p>
        <ul>
            <li>Extraction automatique des données PDF</li>
            <li>Analyse LLM pour extraction précise</li>
            <li>Calculs automatiques des dimensions</li>
            <li>Gestion des données clients</li>
            <li>Pré-import Excel</li>
            <li>Export des résultats</li>
        </ul>
        <p><b>Types de matelas supportés :</b></p>
        <ul>
            <li>Latex Mixte 7 Zones</li>
            <li>Latex Naturel</li>
            <li>Latex Renforcé</li>
            <li>Mousse Viscoélastique</li>
            <li>Mousse Rainurée 7 Zones</li>
            <li>Select 43</li>
        </ul>
        <p><b>Support :</b> Consultez le guide d'aide complet (F1)</p>
        """
        
        QMessageBox.about(self, "À propos de Matelas Processor", about_text)

    def show_eula(self):
        """Affiche le contrat d'utilisation (EULA)"""
        eula_file = "EULA.txt"
        if not os.path.exists(eula_file):
            QMessageBox.warning(self, "Fichier manquant", "Le contrat d'utilisation (EULA.txt) est introuvable.")
            return
        try:
            with open(eula_file, 'r', encoding='utf-8') as f:
                eula_content = f.read()
            # Affichage dans une boîte de dialogue
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Contrat d'utilisation (EULA)")
            dlg.setTextFormat(Qt.TextFormat.PlainText)
            dlg.setText(eula_content)
            dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
            dlg.setIcon(QMessageBox.Icon.Information)
            dlg.exec()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ouvrir le contrat d'utilisation : {str(e)}")

    def check_eula_acceptance(self):
        """Vérifie si l'utilisateur a accepté le contrat d'utilisation, sinon l'affiche et bloque l'accès."""
        if os.path.exists(self.eula_accepted_file):
            return
        eula_file = "EULA.txt"
        if not os.path.exists(eula_file):
            QMessageBox.critical(self, "Fichier manquant", "Le contrat d'utilisation (EULA.txt) est introuvable. L'application va se fermer.")
            sys.exit(1)
        try:
            with open(eula_file, 'r', encoding='utf-8') as f:
                eula_content = f.read()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de lire le contrat d'utilisation : {str(e)}")
            sys.exit(1)
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QCheckBox, QPushButton, QLabel
        dlg = QDialog(self)
        dlg.setWindowTitle("Contrat d'utilisation (EULA)")
        dlg.setModal(True)
        layout = QVBoxLayout(dlg)
        label = QLabel("Veuillez lire et accepter le contrat d'utilisation pour continuer :")
        layout.addWidget(label)
        text = QTextBrowser()
        text.setReadOnly(True)
        text.setPlainText(eula_content)
        layout.addWidget(text)
        accept_box = QCheckBox("J'accepte le contrat d'utilisation")
        layout.addWidget(accept_box)
        btn = QPushButton("Continuer")
        btn.setEnabled(False)
        layout.addWidget(btn)
        accept_box.stateChanged.connect(lambda state: btn.setEnabled(state == 2))
        btn.clicked.connect(dlg.accept)
        dlg.setMinimumSize(600, 500)
        if dlg.exec() == QDialog.DialogCode.Accepted and accept_box.isChecked():
            with open(self.eula_accepted_file, 'w') as f:
                f.write('accepted')
        else:
            QMessageBox.critical(self, "Refus du contrat", "Vous devez accepter le contrat d'utilisation pour utiliser l'application.")
            sys.exit(1)

    def log_message_to_text_browser(self, message, level):
        """Affiche un message de log dans la fenêtre de texte et met à jour le statut"""
        try:
            if not hasattr(self, 'app_logger') or self.app_logger is None:
                print(f"[{level}] {message}")
                return
                
            if level == "INFO":
                self.app_logger.info(message)
                self.update_status_indicator("ready")
                self.statusBar().showMessage(f"Info: {message}", 3000)
            elif level == "WARNING":
                self.app_logger.warning(message)
                self.update_status_indicator("warning")
                self.statusBar().showMessage(f"Attention: {message}", 5000)
            elif level == "ERROR":
                self.app_logger.error(message)
                self.update_status_indicator("error")
                self.statusBar().showMessage(f"Erreur: {message}", 8000)
            else:
                self.app_logger.debug(message)
                
        except Exception as e:
            print(f"Erreur dans log_message_to_text_browser: {e}")
    
    def update_status_bar(self):
        """Met à jour la barre de statut avec le message de log le plus récent"""
        # Cette méthode n'est plus nécessaire car les messages sont déjà affichés dans la fenêtre de texte
        # Elle est conservée pour éviter de casser le code existant, mais peut être retirée si elle n'est pas utilisée.
        pass

    def show_noyau_order_dialog(self):
        """Ouvre la fenêtre de classement des noyaux (modale drag&drop)"""
        # Récupérer tous les noyaux distincts rencontrés dans les résultats ou dans la config
        noyaux = set(config.get_noyau_order())
        for result in self.all_results:
            for conf in result.get('configurations_matelas', []):
                noyau = conf.get('Noyau') or conf.get('Type')
                if noyau:
                    noyaux.add(noyau)
        noyaux = list(noyaux)
        # Si aucun noyau trouvé, proposer une liste par défaut
        if not noyaux:
            noyaux = [
                "MOUSSE VISCO",
                "LATEX NATUREL",
                "LATEX MIXTE 7 ZONES",
                "MOUSSE RAINUREE 7 ZONES",
                "LATEX RENFORCÉ",
                "SELECT 43"
            ]
        
        dialog = NoyauOrderDialog(noyaux, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            ordered_noyaux = dialog.get_ordered_noyaux()
            config.set_noyau_order(ordered_noyaux)
            QMessageBox.information(self, "Succès", "Ordre des noyaux sauvegardé!")

    def show_api_keys_dialog(self):
        """Ouvre la fenêtre de gestion des clés API"""
        dialog = LLMProviderDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_provider_status()
            pass

    def show_general_settings_dialog(self):
        """Ouvre la fenêtre des paramètres généraux"""
        dialog = GeneralSettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Mettre à jour l'affichage du répertoire Excel dans la barre de statut
            self.update_excel_output_status()
    
    def show_tests_dialog(self):
        """Affiche le dialogue des tests automatisés"""
        dialog = TestsDialog(self)
        dialog.exec()
    
    def show_cost_dialog(self):
        """Affiche le dialogue de coût OpenRouter"""
        dialog = CostDialog(self)
        dialog.exec()
    
    def show_maintenance_dialog(self):
        """Affiche le dialogue de maintenance avec les fichiers Markdown"""
        dialog = MaintenanceDialog(self)
        dialog.exec()
    
    def show_mapping_config_dialog(self):
        """Affiche le dialogue de configuration des mappings Excel"""
        try:
            # Import du dialogue de configuration des mappings PyQt6
            from mapping_config_dialog_qt import MappingConfigDialog
            dialog = MappingConfigDialog(self)
            dialog.exec()
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", f"Module de configuration des mappings non disponible: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture du dialogue de configuration: {e}")
    
    def show_update_manager(self):
        """Affiche le gestionnaire de mises à jour"""
        try:
            from update_manager_gui import UpdateManagerGUI
            dialog = UpdateManagerGUI()
            dialog.show()
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", f"Gestionnaire de mises à jour non disponible: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du lancement du gestionnaire de mises à jour: {e}")




class TestsDialog(QDialog):
    """Dialogue pour les tests automatisés"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Tests automatisés")
        self.setModal(True)
        self.resize(800, 600)
        self.test_thread = None
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre de la section tests
        tests_title = QLabel("Système de Tests Automatisés")
        tests_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        tests_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(tests_title)
        
        # Description
        description = QLabel("Exécutez les tests pour vérifier la qualité et les performances de l'application")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: gray; margin-bottom: 10px;")
        layout.addWidget(description)
        
        # Groupe de configuration des tests
        config_group = QGroupBox("Configuration des Tests")
        config_layout = QGridLayout(config_group)
        
        # Options de test
        self.verbose_checkbox = QCheckBox("Mode verbeux")
        self.coverage_checkbox = QCheckBox("Générer rapport de couverture")
        config_layout.addWidget(self.verbose_checkbox, 0, 0)
        config_layout.addWidget(self.coverage_checkbox, 0, 1)
        
        layout.addWidget(config_group)
        
        # Groupe des boutons de test
        buttons_group = QGroupBox("Types de Tests")
        buttons_layout = QGridLayout(buttons_group)
        
        # Boutons pour différents types de tests
        self.install_deps_btn = QPushButton("📦 Installer Dépendances")
        self.install_deps_btn.clicked.connect(lambda: self.run_tests("install_deps"))
        buttons_layout.addWidget(self.install_deps_btn, 0, 0)
        
        self.all_tests_btn = QPushButton("🧪 Tous les Tests")
        self.all_tests_btn.clicked.connect(lambda: self.run_tests("all"))
        buttons_layout.addWidget(self.all_tests_btn, 0, 1)
        
        self.unit_tests_btn = QPushButton("🔧 Tests Unitaires")
        self.unit_tests_btn.clicked.connect(lambda: self.run_tests("unit"))
        buttons_layout.addWidget(self.unit_tests_btn, 1, 0)
        
        self.integration_tests_btn = QPushButton("🔗 Tests d'Intégration")
        self.integration_tests_btn.clicked.connect(lambda: self.run_tests("integration"))
        buttons_layout.addWidget(self.integration_tests_btn, 1, 1)
        
        self.performance_tests_btn = QPushButton("⚡ Tests de Performance")
        self.performance_tests_btn.clicked.connect(lambda: self.run_tests("performance"))
        buttons_layout.addWidget(self.performance_tests_btn, 2, 0)
        
        self.regression_tests_btn = QPushButton("🔄 Tests de Régression")
        self.regression_tests_btn.clicked.connect(lambda: self.run_tests("regression"))
        buttons_layout.addWidget(self.regression_tests_btn, 2, 1)
        
        layout.addWidget(buttons_group)
        
        # Barre de progression pour les tests
        self.test_progress_bar = QProgressBar()
        self.test_progress_bar.setVisible(False)
        layout.addWidget(self.test_progress_bar)
        
        # Zone de sortie des tests
        output_group = QGroupBox("Sortie des Tests")
        output_layout = QVBoxLayout(output_group)
        
        # Boutons pour la zone de sortie
        output_buttons_layout = QHBoxLayout()
        
        self.clear_tests_btn = QPushButton("🗑️ Effacer")
        self.clear_tests_btn.clicked.connect(self.clear_tests_output)
        output_buttons_layout.addWidget(self.clear_tests_btn)
        
        self.save_tests_btn = QPushButton("💾 Sauvegarder")
        self.save_tests_btn.clicked.connect(self.save_tests_output)
        output_buttons_layout.addWidget(self.save_tests_btn)
        
        output_layout.addLayout(output_buttons_layout)
        
        # Zone de texte pour la sortie des tests
        self.tests_output = QTextEdit()
        self.tests_output.setReadOnly(True)
        self.tests_output.setMaximumHeight(300)
        output_layout.addWidget(self.tests_output)
        
        layout.addWidget(output_group)
        
        # Statut des tests
        self.tests_status_label = QLabel("Prêt à exécuter les tests")
        self.tests_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.tests_status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.tests_status_label)
        
        # Boutons de dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def run_tests(self, test_type):
        """Lance l'exécution des tests"""
        try:
            if self.test_thread and self.test_thread.isRunning():
                QMessageBox.warning(self, "Tests en cours", "Des tests sont déjà en cours d'exécution")
                return
            
            # Récupération des options
            verbose = self.verbose_checkbox.isChecked()
            coverage = self.coverage_checkbox.isChecked()
            
            # Mise à jour de l'interface
            self.test_progress_bar.setVisible(True)
            self.test_progress_bar.setValue(0)
            self.tests_status_label.setText("Tests en cours d'exécution...")
            self.tests_status_label.setStyleSheet("color: orange; font-weight: bold;")
            
            # Désactiver les boutons
            self._set_test_buttons_enabled(False)
            
            # Créer et lancer le thread de test
            self.test_thread = TestThread(test_type, verbose, coverage)
            self.test_thread.test_progress.connect(self.on_test_progress)
            self.test_thread.test_output.connect(self.on_test_output)
            self.test_thread.test_finished.connect(self.on_test_finished)
            self.test_thread.test_error.connect(self.on_test_error)
            
            self.test_thread.start()
                
        except Exception as e:
            error_msg = f"Erreur lors du lancement des tests: {e}"
            self.tests_output.append(f"❌ {error_msg}")
            self.tests_status_label.setText("Erreur lors du lancement")
            self.tests_status_label.setStyleSheet("color: red; font-weight: bold;")
            self._set_test_buttons_enabled(True)
    
    def on_test_progress(self, value):
        """Gère la mise à jour de la progression des tests"""
        self.test_progress_bar.setValue(value)
    
    def on_test_output(self, message, level):
        """Gère la sortie des tests"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Couleurs selon le niveau
        color_map = {
            "INFO": "black",
            "WARNING": "orange",
            "ERROR": "red",
            "SUCCESS": "green"
        }
        color = color_map.get(level, "black")
        
        # Formatage du message
        formatted_message = f'<span style="color: {color}">[{timestamp}] {message}</span>'
        self.tests_output.append(formatted_message)
        
        # Auto-scroll vers le bas
        scrollbar = self.tests_output.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def on_test_finished(self, results):
        """Gère la fin des tests"""
        self.test_progress_bar.setVisible(False)
        self._set_test_buttons_enabled(True)
        
        # Analyser les résultats
        total_tests = len(results)
        successful_tests = sum(1 for r in results.values() if r.get('success', False))
        failed_tests = total_tests - successful_tests
        
        if failed_tests == 0:
            self.tests_status_label.setText(f"✅ Tests terminés: {successful_tests}/{total_tests} réussis")
            self.tests_status_label.setStyleSheet("color: green; font-weight: bold;")
            self.on_test_output("🎉 Tous les tests ont réussi !", "SUCCESS")
        else:
            self.tests_status_label.setText(f"⚠️ Tests terminés: {successful_tests}/{total_tests} réussis, {failed_tests} échecs")
            self.tests_status_label.setStyleSheet("color: orange; font-weight: bold;")
            self.on_test_output(f"⚠️ {failed_tests} test(s) ont échoué", "WARNING")
        
        # Afficher un résumé des résultats
        self.on_test_output("", "INFO")
        self.on_test_output("=== RÉSUMÉ DES TESTS ===", "INFO")
        for test_name, result in results.items():
            status = "✅" if result.get('success', False) else "❌"
            self.on_test_output(f"{status} {test_name}", "INFO")
    
    def on_test_error(self, error_msg):
        """Gère les erreurs des tests"""
        self.test_progress_bar.setVisible(False)
        self._set_test_buttons_enabled(True)
        self.tests_status_label.setText("❌ Erreur lors des tests")
        self.tests_status_label.setStyleSheet("color: red; font-weight: bold;")
        self.on_test_output(f"❌ Erreur: {error_msg}", "ERROR")
    
    def _set_test_buttons_enabled(self, enabled):
        """Active/désactive les boutons de test"""
        self.install_deps_btn.setEnabled(enabled)
        self.all_tests_btn.setEnabled(enabled)
        self.unit_tests_btn.setEnabled(enabled)
        self.integration_tests_btn.setEnabled(enabled)
        self.performance_tests_btn.setEnabled(enabled)
        self.regression_tests_btn.setEnabled(enabled)
    
    def clear_tests_output(self):
        """Efface la sortie des tests"""
        self.tests_output.clear()
    
    def save_tests_output(self):
        """Sauvegarde la sortie des tests dans un fichier"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder la sortie des tests", 
                f"tests_output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                "Fichiers texte (*.txt);;Tous les fichiers (*)"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.tests_output.toPlainText())
                QMessageBox.information(self, "Succès", f"Sortie des tests sauvegardée dans {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {e}")


class CostDialog(QDialog):
    """Dialogue pour le coût OpenRouter"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Coût OpenRouter")
        self.setModal(True)
        self.resize(700, 500)
        self.balance_thread = None
        self.init_ui()
        self.load_api_key_from_config()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre de la section coût
        cost_title = QLabel("Surveillance OpenRouter")
        cost_title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        cost_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(cost_title)
        
        # Description
        description = QLabel("Surveillez les limites de votre clé API et calculez le coût de vos requêtes")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setStyleSheet("color: gray; margin-bottom: 10px;")
        layout.addWidget(description)
        
        # Groupe de configuration
        config_group = QGroupBox("Configuration")
        config_layout = QGridLayout(config_group)
        
        # Clé API OpenRouter
        self.api_key_label = QLabel("Clé API OpenRouter:")
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Entrez votre clé API OpenRouter")
        config_layout.addWidget(self.api_key_label, 0, 0)
        config_layout.addWidget(self.api_key_input, 0, 1)
        
        # Bouton pour récupérer le solde
        self.refresh_balance_btn = QPushButton("🔄 Actualiser le solde")
        self.refresh_balance_btn.clicked.connect(self.refresh_openrouter_balance)
        config_layout.addWidget(self.refresh_balance_btn, 1, 0, 1, 2)
        
        layout.addWidget(config_group)
        
        # Groupe d'informations du solde
        balance_group = QGroupBox("Limites de la Clé API")
        balance_layout = QGridLayout(balance_group)
        
        # Labels pour afficher les informations
        self.balance_label = QLabel("Limite restante:")
        self.balance_value = QLabel("Non disponible")
        self.balance_value.setStyleSheet("font-weight: bold; color: blue;")
        balance_layout.addWidget(self.balance_label, 0, 0)
        balance_layout.addWidget(self.balance_value, 0, 1)
        
        self.credits_label = QLabel("Utilisation actuelle:")
        self.credits_value = QLabel("Non disponible")
        self.credits_value.setStyleSheet("font-weight: bold; color: green;")
        balance_layout.addWidget(self.credits_label, 1, 0)
        balance_layout.addWidget(self.credits_value, 1, 1)
        
        self.total_spent_label = QLabel("Limite totale:")
        self.total_spent_value = QLabel("Non disponible")
        self.total_spent_value.setStyleSheet("font-weight: bold; color: red;")
        balance_layout.addWidget(self.total_spent_label, 2, 0)
        balance_layout.addWidget(self.total_spent_value, 2, 1)
        
        # Note explicative
        note_label = QLabel("💡 Note: Ces valeurs représentent les limites de votre clé API, pas le solde de votre compte.")
        note_label.setStyleSheet("color: gray; font-style: italic; font-size: 10px;")
        note_label.setWordWrap(True)
        balance_layout.addWidget(note_label, 3, 0, 1, 2)
        
        # Boutons d'accès au portefeuille
        wallet_buttons_layout = QHBoxLayout()
        
        self.wallet_btn = QPushButton("🏦 Voir Mon Portefeuille")
        self.wallet_btn.clicked.connect(self.open_wallet)
        self.wallet_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; border-radius: 4px;")
        wallet_buttons_layout.addWidget(self.wallet_btn)
        
        self.recharge_btn = QPushButton("💳 Recharger")
        self.recharge_btn.clicked.connect(self.open_recharge)
        self.recharge_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; border-radius: 4px;")
        wallet_buttons_layout.addWidget(self.recharge_btn)
        
        balance_layout.addLayout(wallet_buttons_layout, 4, 0, 1, 2)
        
        layout.addWidget(balance_group)
        
        # Groupe d'informations sur le solde réel
        real_balance_group = QGroupBox("Solde Réel du Compte")
        real_balance_layout = QVBoxLayout(real_balance_group)
        
        # Message explicatif
        real_balance_info = QLabel(
            "🔍 <strong>Pour voir votre vrai solde :</strong><br>"
            "• Cliquez sur '🏦 Voir Mon Portefeuille' pour accéder à votre compte OpenRouter<br>"
            "• Ou connectez-vous directement sur <a href='https://openrouter.ai/account'>openrouter.ai/account</a><br>"
            "• Le solde réel n'est pas accessible via l'API pour des raisons de sécurité"
        )
        real_balance_info.setOpenExternalLinks(True)
        real_balance_info.setWordWrap(True)
        real_balance_info.setStyleSheet("color: #666; padding: 10px; background-color: #f9f9f9; border-radius: 5px;")
        real_balance_layout.addWidget(real_balance_info)
        
        layout.addWidget(real_balance_group)
        
        # Groupe de calcul de coût
        calc_group = QGroupBox("Calcul de Coût par Devis")
        calc_layout = QGridLayout(calc_group)
        
        # Modèle sélectionné
        self.model_label = QLabel("Modèle:")
        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "anthropic/claude-3.5-sonnet",
            "anthropic/claude-3-opus",
            "openai/gpt-4o",
            "openai/gpt-4o-mini",
            "meta-llama/llama-3.1-8b-instruct",
            "meta-llama/llama-3.1-70b-instruct"
        ])
        calc_layout.addWidget(self.model_label, 0, 0)
        calc_layout.addWidget(self.model_combo, 0, 1)
        
        # Nombre de tokens estimés
        self.tokens_label = QLabel("Tokens estimés:")
        self.tokens_input = QSpinBox()
        self.tokens_input.setRange(100, 100000)
        self.tokens_input.setValue(2000)
        self.tokens_input.setSuffix(" tokens")
        calc_layout.addWidget(self.tokens_label, 1, 0)
        calc_layout.addWidget(self.tokens_input, 1, 1)
        
        # Bouton de calcul
        self.calculate_cost_btn = QPushButton("🧮 Calculer le coût")
        self.calculate_cost_btn.clicked.connect(self.calculate_cost)
        calc_layout.addWidget(self.calculate_cost_btn, 2, 0, 1, 2)
        
        # Résultat du calcul
        self.cost_result_label = QLabel("Coût estimé:")
        self.cost_result_value = QLabel("Cliquez sur 'Calculer'")
        self.cost_result_value.setStyleSheet("font-weight: bold; color: purple;")
        calc_layout.addWidget(self.cost_result_label, 3, 0)
        calc_layout.addWidget(self.cost_result_value, 3, 1)
        
        layout.addWidget(calc_group)
        
        # Groupe d'historique
        history_group = QGroupBox("Historique des Coûts")
        history_layout = QVBoxLayout(history_group)
        
        # Boutons pour l'historique
        history_buttons_layout = QHBoxLayout()
        
        self.load_history_btn = QPushButton("📊 Charger l'historique")
        self.load_history_btn.clicked.connect(self.load_cost_history)
        history_buttons_layout.addWidget(self.load_history_btn)
        
        self.clear_history_btn = QPushButton("🗑️ Effacer l'historique")
        self.clear_history_btn.clicked.connect(self.clear_cost_history)
        history_buttons_layout.addWidget(self.clear_history_btn)
        
        history_layout.addLayout(history_buttons_layout)
        
        # Tableau d'historique
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(5)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Modèle", "Tokens", "Coût ($)", "Total"
        ])
        history_layout.addWidget(self.history_table)
        
        layout.addWidget(history_group)
        
        # Statut
        self.cost_status_label = QLabel("Prêt à calculer les coûts")
        self.cost_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cost_status_label.setStyleSheet("color: green; font-weight: bold;")
        layout.addWidget(self.cost_status_label)
        
        # Boutons de dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def load_api_key_from_config(self):
        """Charge la clé API depuis la configuration"""
        try:
            from config import config
            api_key = config.get_openrouter_api_key()
            if api_key:
                self.api_key_input.setText(api_key)
        except Exception as e:
            print(f"Erreur lors du chargement de la clé API: {e}")
    
    def refresh_openrouter_balance(self):
        """Récupère le solde OpenRouter"""
        try:
            api_key = self.api_key_input.text().strip()
            if not api_key:
                QMessageBox.warning(self, "Clé API manquante", "Veuillez entrer votre clé API OpenRouter")
                return
            
            # Désactiver le bouton pendant la requête
            self.refresh_balance_btn.setEnabled(False)
            self.refresh_balance_btn.setText("🔄 Récupération...")
            self.cost_status_label.setText("Récupération du solde...")
            self.cost_status_label.setStyleSheet("color: orange; font-weight: bold;")
            
            # Créer et lancer le thread de récupération
            self.balance_thread = BalanceThread(api_key)
            self.balance_thread.balance_ready.connect(self.on_balance_ready)
            self.balance_thread.balance_error.connect(self.on_balance_error)
            self.balance_thread.start()
            
        except Exception as e:
            error_msg = f"Erreur lors de la récupération du solde: {e}"
            self.cost_status_label.setText("Erreur lors de la récupération")
            self.cost_status_label.setStyleSheet("color: red; font-weight: bold;")
            self.refresh_balance_btn.setEnabled(True)
            self.refresh_balance_btn.setText("🔄 Actualiser le solde")
            QMessageBox.warning(self, "Erreur", error_msg)
    
    def on_balance_ready(self, balance_data):
        """Gère la réception des données de solde"""
        try:
            # Mettre à jour l'interface
            self.refresh_balance_btn.setEnabled(True)
            self.refresh_balance_btn.setText("🔄 Actualiser le solde")
            self.cost_status_label.setText("Solde récupéré avec succès")
            self.cost_status_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Afficher les données
            if 'remaining' in balance_data:
                self.balance_value.setText(f"${balance_data['remaining']:.2f}")
            else:
                self.balance_value.setText("Non disponible")
            
            if 'used' in balance_data:
                self.credits_value.setText(f"${balance_data['used']:.2f}")
            else:
                self.credits_value.setText("Non disponible")
            
            if 'total' in balance_data:
                self.total_spent_value.setText(f"${balance_data['total']:.2f}")
            else:
                self.total_spent_value.setText("Non disponible")
            
        except Exception as e:
            error_msg = f"Erreur lors de l'affichage du solde: {e}"
            self.cost_status_label.setText("Erreur d'affichage")
            self.cost_status_label.setStyleSheet("color: red; font-weight: bold;")
            QMessageBox.warning(self, "Erreur", error_msg)
    
    def on_balance_error(self, error_msg):
        """Gère les erreurs de récupération du solde"""
        self.refresh_balance_btn.setEnabled(True)
        self.refresh_balance_btn.setText("🔄 Actualiser le solde")
        self.cost_status_label.setText("Erreur lors de la récupération")
        self.cost_status_label.setStyleSheet("color: red; font-weight: bold;")
        QMessageBox.warning(self, "Erreur", error_msg)
    
    def calculate_cost(self):
        """Calcule le coût estimé pour un modèle et un nombre de tokens"""
        try:
            model = self.model_combo.currentText()
            tokens = self.tokens_input.value()
            
            # Tarifs OpenRouter (en $ par 1M tokens)
            rates = {
                "anthropic/claude-3.5-sonnet": 3.0,
                "anthropic/claude-3-opus": 15.0,
                "openai/gpt-4o": 5.0,
                "openai/gpt-4o-mini": 0.15,
                "meta-llama/llama-3.1-8b-instruct": 0.2,
                "meta-llama/llama-3.1-70b-instruct": 0.8
            }
            
            if model in rates:
                rate = rates[model]
                cost = (tokens / 1000000) * rate
                self.cost_result_value.setText(f"${cost:.6f}")
                
                # Ajouter à l'historique
                self.add_to_history(model, tokens, cost)
            else:
                self.cost_result_value.setText("Modèle non reconnu")
                
        except Exception as e:
            error_msg = f"Erreur lors du calcul: {e}"
            self.cost_result_value.setText("Erreur")
            QMessageBox.warning(self, "Erreur", error_msg)
    
    def add_to_history(self, model, tokens, cost):
        """Ajoute un calcul à l'historique"""
        try:
            # Charger l'historique existant
            history_file = "cost_history.json"
            history = []
            
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            
            # Ajouter le nouveau calcul
            new_entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "model": model,
                "tokens": tokens,
                "cost": cost
            }
            history.append(new_entry)
            
            # Sauvegarder l'historique
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, indent=2, ensure_ascii=False)
            
            # Mettre à jour l'affichage
            self.load_cost_history()
            
        except Exception as e:
            print(f"Erreur lors de l'ajout à l'historique: {e}")
    
    def load_cost_history(self):
        """Charge et affiche l'historique des coûts"""
        try:
            history_file = "cost_history.json"
            if not os.path.exists(history_file):
                self.history_table.setRowCount(0)
                return
            
            with open(history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
            
            # Afficher dans le tableau
            self.history_table.setRowCount(len(history))
            
            total_cost = 0
            for i, entry in enumerate(history):
                self.history_table.setItem(i, 0, QTableWidgetItem(entry.get('date', '')))
                self.history_table.setItem(i, 1, QTableWidgetItem(entry.get('model', '')))
                self.history_table.setItem(i, 2, QTableWidgetItem(str(entry.get('tokens', 0))))
                cost = entry.get('cost', 0)
                self.history_table.setItem(i, 3, QTableWidgetItem(f"${cost:.6f}"))
                total_cost += cost
            
            # Afficher le total
            if history:
                self.history_table.setItem(len(history)-1, 4, QTableWidgetItem(f"${total_cost:.6f}"))
            
            # Ajuster la largeur des colonnes
            self.history_table.resizeColumnsToContents()
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement de l'historique: {e}")
    
    def clear_cost_history(self):
        """Efface l'historique des coûts"""
        try:
            reply = QMessageBox.question(
                self, "Confirmation", 
                "Êtes-vous sûr de vouloir effacer tout l'historique des coûts ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                history_file = "cost_history.json"
                if os.path.exists(history_file):
                    os.remove(history_file)
                self.history_table.setRowCount(0)
                QMessageBox.information(self, "Succès", "Historique des coûts effacé")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'effacement: {e}")
    
    def open_wallet(self):
        """Ouvre le portefeuille OpenRouter dans le navigateur"""
        try:
            webbrowser.open("https://openrouter.ai/account")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir le navigateur: {e}")
    
    def open_recharge(self):
        """Ouvre la page de recharge OpenRouter dans le navigateur"""
        try:
            webbrowser.open("https://openrouter.ai/account/billing")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir le navigateur: {e}")


class GeneralSettingsDialog(QDialog):
    """Dialogue pour les paramètres généraux de l'application"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Paramètres généraux")
        self.setModal(True)
        self.resize(600, 400)
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Répertoire de sortie Excel
        excel_group = QGroupBox("Répertoire de sortie Excel")
        excel_layout = QFormLayout(excel_group)
        
        self.excel_output_dir = QLineEdit()
        self.excel_output_dir.setPlaceholderText("Chemin vers le répertoire de sortie des fichiers Excel")
        
        browse_btn = QPushButton("Parcourir...")
        browse_btn.clicked.connect(self.browse_excel_directory)
        
        excel_dir_layout = QHBoxLayout()
        excel_dir_layout.addWidget(self.excel_output_dir)
        excel_dir_layout.addWidget(browse_btn)
        
        excel_layout.addRow("Répertoire de sortie:", excel_dir_layout)
        layout.addWidget(excel_group)
        
        # Informations sur le répertoire
        self.dir_info = QLabel()
        self.dir_info.setWordWrap(True)
        self.dir_info.setStyleSheet("color: gray; font-size: 10px;")
        layout.addWidget(self.dir_info)
        
        # Boutons de dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def browse_excel_directory(self):
        """Ouvre un dialogue pour sélectionner le répertoire de sortie Excel"""
        current_dir = self.excel_output_dir.text()
        if not current_dir:
            current_dir = os.getcwd()
        
        directory = QFileDialog.getExistingDirectory(
            self, 
            "Sélectionner le répertoire de sortie Excel",
            current_dir
        )
        
        if directory:
            self.excel_output_dir.setText(directory)
            self.update_directory_info()
    
    def update_directory_info(self):
        """Met à jour les informations sur le répertoire sélectionné"""
        directory = self.excel_output_dir.text()
        if directory:
            if os.path.exists(directory):
                if os.path.isdir(directory):
                    # Compter les fichiers Excel existants
                    excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]
                    self.dir_info.setText(
                        f"✅ Répertoire valide\n"
                        f"📁 {len(excel_files)} fichier(s) Excel existant(s)\n"
                        f"📂 Chemin: {directory}"
                    )
                else:
                    self.dir_info.setText("❌ Le chemin spécifié n'est pas un répertoire")
            else:
                self.dir_info.setText("⚠️ Le répertoire sera créé automatiquement lors de la première utilisation")
        else:
            self.dir_info.setText("ℹ️ Utilisation du répertoire par défaut (output/)")
    
    def load_current_settings(self):
        """Charge les paramètres actuels"""
        try:
            from config import config
            current_dir = config.get_excel_output_directory()
            self.excel_output_dir.setText(current_dir)
            self.update_directory_info()
        except Exception as e:
            print(f"Erreur lors du chargement des paramètres: {e}")
    
    def accept(self):
        """Sauvegarde les paramètres et ferme le dialogue"""
        try:
            from config import config
            directory = self.excel_output_dir.text().strip()
            
            if directory:
                # Normaliser le chemin
                directory = os.path.abspath(directory)
                config.set_excel_output_directory(directory)
            
            super().accept()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde des paramètres: {e}")


class MaintenanceDialog(QDialog):
    """Dialog pour afficher les fichiers de maintenance (Markdown)"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("📚 Maintenance - Documentation")
        self.setModal(True)
        self.resize(1000, 700)
        self.md_files = []
        self.init_ui()
        self.scan_md_files()
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        layout = QVBoxLayout()
        
        # En-tête avec titre et bouton de rafraîchissement
        header_layout = QHBoxLayout()
        
        title_label = QLabel("📚 Documentation de Maintenance")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Bouton de rafraîchissement
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setToolTip("Actualiser la liste des fichiers de documentation")
        refresh_btn.clicked.connect(self.scan_md_files)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Zone principale avec liste et aperçu
        main_layout = QHBoxLayout()
        
        # Panneau gauche : liste des fichiers
        left_panel = QVBoxLayout()
        
        list_label = QLabel("📄 Fichiers de documentation disponibles :")
        list_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        left_panel.addWidget(list_label)
        
        # Liste des fichiers
        self.file_list = QListWidget()
        self.file_list.setMaximumWidth(400)
        self.file_list.itemClicked.connect(self.on_file_selected)
        left_panel.addWidget(self.file_list)
        
        # Informations sur le fichier sélectionné
        self.file_info_label = QLabel("Sélectionnez un fichier pour voir son contenu")
        self.file_info_label.setStyleSheet("color: gray; font-style: italic; padding: 5px;")
        self.file_info_label.setWordWrap(True)
        left_panel.addWidget(self.file_info_label)
        
        main_layout.addLayout(left_panel)
        
        # Séparateur vertical
        v_separator = QFrame()
        v_separator.setFrameShape(QFrame.Shape.VLine)
        v_separator.setFrameShadow(QFrame.Shadow.Sunken)
        main_layout.addWidget(v_separator)
        
        # Panneau droit : aperçu du contenu
        right_panel = QVBoxLayout()
        
        preview_label = QLabel("📖 Aperçu du contenu :")
        preview_label.setStyleSheet("font-weight: bold; margin-bottom: 5px;")
        right_panel.addWidget(preview_label)
        
        # Zone d'aperçu avec scroll
        self.preview_area = QTextBrowser()
        self.preview_area.setOpenExternalLinks(True)
        self.preview_area.setStyleSheet("""
            QTextBrowser {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 4px;
                padding: 10px;
                font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        right_panel.addWidget(self.preview_area)
        
        # Boutons d'action
        action_layout = QHBoxLayout()
        
        self.open_file_btn = QPushButton("📂 Ouvrir le fichier")
        self.open_file_btn.setEnabled(False)
        self.open_file_btn.clicked.connect(self.open_selected_file)
        action_layout.addWidget(self.open_file_btn)
        
        self.copy_path_btn = QPushButton("📋 Copier le chemin")
        self.copy_path_btn.setEnabled(False)
        self.copy_path_btn.clicked.connect(self.copy_file_path)
        action_layout.addWidget(self.copy_path_btn)
        
        action_layout.addStretch()
        
        # Bouton fermer
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(self.accept)
        action_layout.addWidget(close_btn)
        
        right_panel.addLayout(action_layout)
        main_layout.addLayout(right_panel)
        
        layout.addLayout(main_layout)
        
        # Barre de statut
        self.status_label = QLabel("Prêt")
        self.status_label.setStyleSheet("color: gray; font-style: italic; padding: 5px; border-top: 1px solid #dee2e6;")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def scan_md_files(self):
        """Scanne et charge tous les fichiers Markdown du projet"""
        try:
            self.status_label.setText("Scan en cours...")
            self.md_files = []
            self.file_list.clear()
            
            # Scanner le répertoire racine et les sous-répertoires
            for root, dirs, files in os.walk('.'):
                # Ignorer les répertoires système
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'env']]
                
                for file in files:
                    if file.lower().endswith('.md'):
                        file_path = os.path.join(root, file)
                        # Chemin relatif pour l'affichage
                        rel_path = os.path.relpath(file_path, '.')
                        
                        # Obtenir les informations du fichier
                        try:
                            stat = os.stat(file_path)
                            size = stat.st_size
                            modified = datetime.fromtimestamp(stat.st_mtime)
                            
                            # Lire les premières lignes pour extraire le titre
                            title = self.extract_title_from_md(file_path)
                            
                            file_info = {
                                'path': file_path,
                                'rel_path': rel_path,
                                'title': title,
                                'size': size,
                                'modified': modified
                            }
                            
                            self.md_files.append(file_info)
                            
                        except Exception as e:
                            logger.warning(f"Erreur lors de la lecture du fichier {file_path}: {e}")
            
            # Trier par date de modification (plus récent en premier)
            self.md_files.sort(key=lambda x: x['modified'], reverse=True)
            
            # Ajouter les fichiers à la liste
            for file_info in self.md_files:
                item = QListWidgetItem()
                
                # Créer le texte d'affichage
                display_text = f"{file_info['title']}\n"
                display_text += f"📁 {file_info['rel_path']}\n"
                display_text += f"📅 {file_info['modified'].strftime('%d/%m/%Y %H:%M')} • "
                display_text += f"📏 {self.format_file_size(file_info['size'])}"
                
                item.setText(display_text)
                item.setData(Qt.ItemDataRole.UserRole, file_info)
                
                self.file_list.addItem(item)
            
            self.status_label.setText(f"Scan terminé : {len(self.md_files)} fichiers trouvés")
            
        except Exception as e:
            error_msg = f"Erreur lors du scan des fichiers : {str(e)}"
            self.status_label.setText(error_msg)
            logger.error(error_msg)
    
    def extract_title_from_md(self, file_path):
        """Extrait le titre d'un fichier Markdown"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
                # Chercher le premier titre (# ou ##)
                for line in lines[:10]:  # Limiter aux 10 premières lignes
                    line = line.strip()
                    if line.startswith('# '):
                        return line[2:].strip()
                    elif line.startswith('## '):
                        return line[3:].strip()
                
                # Si pas de titre trouvé, utiliser le nom du fichier
                return os.path.splitext(os.path.basename(file_path))[0]
                
        except Exception:
            return os.path.splitext(os.path.basename(file_path))[0]
    
    def format_file_size(self, size_bytes):
        """Formate la taille d'un fichier en format lisible"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def on_file_selected(self, item):
        """Appelé quand un fichier est sélectionné dans la liste"""
        file_info = item.data(Qt.ItemDataRole.UserRole)
        if file_info:
            self.display_file_content(file_info)
            self.open_file_btn.setEnabled(True)
            self.copy_path_btn.setEnabled(True)
    
    def display_file_content(self, file_info):
        """Affiche le contenu d'un fichier Markdown"""
        try:
            self.status_label.setText(f"Chargement de {file_info['rel_path']}...")
            
            with open(file_info['path'], 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Convertir le Markdown en HTML pour un meilleur affichage
            html_content = self.markdown_to_html(content)
            
            # Ajouter des métadonnées
            html_header = f"""
            <div style="background-color: #e9ecef; padding: 10px; border-radius: 4px; margin-bottom: 15px;">
                <h3 style="margin: 0 0 10px 0; color: #495057;">{file_info['title']}</h3>
                <p style="margin: 5px 0; color: #6c757d; font-size: 12px;">
                    📁 <strong>Chemin :</strong> {file_info['rel_path']}<br>
                    📅 <strong>Modifié :</strong> {file_info['modified'].strftime('%d/%m/%Y à %H:%M')}<br>
                    📏 <strong>Taille :</strong> {self.format_file_size(file_info['size'])}
                </p>
            </div>
            <hr style="margin: 20px 0;">
            """
            
            self.preview_area.setHtml(html_header + html_content)
            self.file_info_label.setText(f"Fichier sélectionné : {file_info['rel_path']}")
            self.status_label.setText("Contenu chargé avec succès")
            
        except Exception as e:
            error_msg = f"Erreur lors de la lecture du fichier : {str(e)}"
            self.preview_area.setPlainText(error_msg)
            self.status_label.setText(error_msg)
            logger.error(error_msg)
    
    def markdown_to_html(self, markdown_text):
        """Convertit le Markdown en HTML basique"""
        try:
            # Import de markdown si disponible
            try:
                import markdown
                return markdown.markdown(markdown_text, extensions=['fenced_code', 'tables', 'codehilite'])
            except ImportError:
                # Conversion basique si markdown n'est pas disponible
                return self.simple_markdown_to_html(markdown_text)
        except Exception:
            # Fallback : afficher le texte brut
            return f"<pre>{markdown_text}</pre>"
    
    def simple_markdown_to_html(self, text):
        """Conversion Markdown vers HTML basique"""
        import re
        
        # Échapper les caractères spéciaux HTML
        text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        # Titres
        text = re.sub(r'^### (.*$)', r'<h3>\1</h3>', text, flags=re.MULTILINE)
        text = re.sub(r'^## (.*$)', r'<h2>\1</h2>', text, flags=re.MULTILINE)
        text = re.sub(r'^# (.*$)', r'<h1>\1</h1>', text, flags=re.MULTILINE)
        
        # Code inline
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        
        # Code blocks
        text = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', text, flags=re.DOTALL)
        
        # Liens
        text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
        
        # Gras
        text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
        
        # Italique
        text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
        
        # Listes
        text = re.sub(r'^\* (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
        text = re.sub(r'^- (.*$)', r'<li>\1</li>', text, flags=re.MULTILINE)
        
        # Paragraphes
        text = re.sub(r'\n\n', r'</p><p>', text)
        text = f'<p>{text}</p>'
        
        return text
    
    def open_selected_file(self):
        """Ouvre le fichier sélectionné avec l'application par défaut"""
        current_item = self.file_list.currentItem()
        if current_item:
            file_info = current_item.data(Qt.ItemDataRole.UserRole)
            if file_info:
                try:
                    import subprocess
                    import platform
                    
                    if platform.system() == 'Darwin':  # macOS
                        subprocess.run(['open', file_info['path']])
                    elif platform.system() == 'Windows':
                        subprocess.run(['start', file_info['path']], shell=True)
                    else:  # Linux
                        subprocess.run(['xdg-open', file_info['path']])
                    
                    self.status_label.setText(f"Fichier ouvert : {file_info['rel_path']}")
                    
                except Exception as e:
                    error_msg = f"Erreur lors de l'ouverture du fichier : {str(e)}"
                    self.status_label.setText(error_msg)
                    logger.error(error_msg)
    
    def copy_file_path(self):
        """Copie le chemin du fichier dans le presse-papiers"""
        current_item = self.file_list.currentItem()
        if current_item:
            file_info = current_item.data(Qt.ItemDataRole.UserRole)
            if file_info:
                try:
                    clipboard = QApplication.clipboard()
                    clipboard.setText(file_info['path'])
                    self.status_label.setText("Chemin copié dans le presse-papiers")
                    
                except Exception as e:
                    error_msg = f"Erreur lors de la copie : {str(e)}"
                    self.status_label.setText(error_msg)
                    logger.error(error_msg)


class NoyauOrderDialog(QDialog):
    """Dialogue pour classer l'ordre des noyaux par glisser-déposer"""
    def __init__(self, noyaux, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Classement des noyaux")
        self.setModal(True)
        self.resize(400, 500)
        layout = QVBoxLayout(self)
        label = QLabel("Classez les noyaux par glisser-déposer :")
        layout.addWidget(label)
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        for noyau in noyaux:
            item = QListWidgetItem(noyau)
            self.list_widget.addItem(item)
        layout.addWidget(self.list_widget)
        buttons = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Annuler")
        ok_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)
        buttons.addWidget(ok_button)
        buttons.addWidget(cancel_button)
        layout.addLayout(buttons)
    
    def get_ordered_noyaux(self):
        """Retourne la liste des noyaux dans l'ordre choisi"""
        return [self.list_widget.item(i).text() for i in range(self.list_widget.count())]


def main():
    """Point d'entrée de l'application"""
    from PyQt6.QtWidgets import QSplashScreen
    from PyQt6.QtCore import Qt
    from PyQt6.QtGui import QPixmap
    import time

    app = QApplication(sys.argv)
    
    # Splash screen avec le logo
    try:
        splash_pix = QPixmap("assets/lit-double.png").scaledToHeight(200, Qt.TransformationMode.SmoothTransformation)
        splash = QSplashScreen(splash_pix)
        splash.show()
        app.processEvents()
        time.sleep(2)  # Affiche le splash pendant 2 secondes
    except Exception as e:
        print(f"Erreur lors de l'affichage du splash screen: {e}")

    # Style global
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre principale
    try:
        window = MatelasApp()
        window.show()
        if 'splash' in locals():
            splash.finish(window)
    except Exception as e:
        print(f"Erreur lors de la création de la fenêtre principale: {e}")
        sys.exit(1)
    
    # Lancement de l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 