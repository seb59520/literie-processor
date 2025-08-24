#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Application de test LLM pour MatelasApp
Permet de tester les prompts, providers et modèles LLM
"""

import sys
import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, Optional

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                QWidget, QTextEdit, QPushButton, QLabel, QComboBox, 
                                QLineEdit, QGroupBox, QSplitter, QTabWidget, QTableWidget,
                                QTableWidgetItem, QMessageBox, QFileDialog, QProgressBar,
                                QCheckBox, QSpinBox, QDoubleSpinBox, QTextBrowser, QDialog)
    from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
    from PyQt6.QtGui import QFont, QIcon, QPixmap
except ImportError:
    print("PyQt6 non trouvé, tentative avec PyQt5...")
    try:
        from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                    QWidget, QTextEdit, QPushButton, QLabel, QComboBox, 
                                    QLineEdit, QGroupBox, QSplitter, QTabWidget, QTableWidget,
                                    QTableWidgetItem, QMessageBox, QFileDialog, QProgressBar,
                                    QCheckBox, QSpinBox, QDoubleSpinBox, QTextBrowser, QDialog)
        from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
        from PyQt5.QtGui import QFont, QIcon, QPixmap
    except ImportError:
        print("Erreur: PyQt5 ou PyQt6 requis pour l'interface graphique")
        sys.exit(1)

# Imports backend
from config import config
from backend.llm_provider import llm_manager

# Configuration des logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaDownloadThread(QThread):
    """Thread pour télécharger des modèles Ollama"""
    progress_update = pyqtSignal(str)
    download_completed = pyqtSignal(str)
    download_error = pyqtSignal(str)
    
    def __init__(self, model_name):
        super().__init__()
        self.model_name = model_name
        
    def run(self):
        try:
            import subprocess
            import sys
            
            self.progress_update.emit(f"Début du téléchargement de {self.model_name}...")
            
            # Commande pour télécharger le modèle
            cmd = ["ollama", "pull", self.model_name]
            
            # Lancer le processus
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Lire la sortie en temps réel
            for line in process.stdout:
                if line.strip():
                    self.progress_update.emit(f"Ollama: {line.strip()}")
            
            # Attendre la fin du processus
            return_code = process.wait()
            
            if return_code == 0:
                self.download_completed.emit(self.model_name)
            else:
                self.download_error.emit(f"Erreur lors du téléchargement (code: {return_code})")
                
        except FileNotFoundError:
            self.download_error.emit("Ollama n'est pas installé ou n'est pas dans le PATH")
        except Exception as e:
            self.download_error.emit(f"Erreur: {str(e)}")

class LLMTestWorker(QThread):
    """Thread de travail pour les appels LLM asynchrones"""
    result_ready = pyqtSignal(dict)
    progress_update = pyqtSignal(str)
    
    def __init__(self, prompt: str, provider: str, api_key: str, model: str, 
                 temperature: float, max_tokens: int):
        super().__init__()
        self.prompt = prompt
        self.provider = provider
        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
    def run(self):
        try:
            self.progress_update.emit("Configuration du provider...")
            
            # Configuration du provider
            if self.provider == "ollama":
                api_key = None
            else:
                api_key = self.api_key
                
            llm_manager.set_provider(self.provider, api_key)
            
            self.progress_update.emit("Appel au LLM...")
            
            # Appel au LLM
            result = llm_manager.call_llm(
                self.prompt, 
                temperature=self.temperature, 
                max_tokens=self.max_tokens
            )
            
            self.progress_update.emit("Traitement terminé")
            self.result_ready.emit(result)
            
        except Exception as e:
            self.result_ready.emit({
                "success": False,
                "error": str(e),
                "content": f"Erreur: {str(e)}"
            })

class LLMTestApp(QMainWindow):
    """Application principale de test LLM"""
    
    def __init__(self):
        super().__init__()
        self.current_prompt = self.get_current_prompt()
        self.prompt_history = []
        self.test_results = []
        self.init_ui()
        self.load_config()
        
    def init_ui(self):
        """Initialisation de l'interface utilisateur"""
        self.setWindowTitle("Test LLM - MatelasApp")
        self.setGeometry(100, 100, 1400, 900)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter principal
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Panneau gauche (Configuration et Prompt)
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Panneau droit (Résultats et Tests)
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Proportions du splitter
        splitter.setSizes([600, 800])
        
        # Barre de statut
        self.statusBar().showMessage("Prêt")
        
    def create_left_panel(self):
        """Création du panneau gauche"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Configuration des providers
        provider_group = QGroupBox("Configuration Provider")
        provider_layout = QVBoxLayout(provider_group)
        
        # Sélection du provider
        provider_row = QHBoxLayout()
        provider_row.addWidget(QLabel("Provider:"))
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["ollama", "openrouter", "openai", "anthropic"])
        self.provider_combo.currentTextChanged.connect(self.on_provider_changed)
        provider_row.addWidget(self.provider_combo)
        provider_layout.addLayout(provider_row)
        
        # Clé API
        api_row = QHBoxLayout()
        api_row.addWidget(QLabel("Clé API:"))
        self.api_key_edit = QLineEdit()
        self.api_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        api_row.addWidget(self.api_key_edit)
        
        # Bouton de synchronisation des clés API
        self.sync_api_btn = QPushButton("🔄")
        self.sync_api_btn.setToolTip("Synchroniser la clé API depuis la configuration centrale")
        self.sync_api_btn.clicked.connect(self.sync_api_key)
        self.sync_api_btn.setFixedSize(30, 25)
        api_row.addWidget(self.sync_api_btn)
        
        provider_layout.addLayout(api_row)
        
        # Modèle
        model_row = QHBoxLayout()
        model_row.addWidget(QLabel("Modèle:"))
        self.model_combo = QComboBox()
        self.model_combo.addItems(["mistral:latest", "gpt-4-turbo", "gpt-3.5-turbo", "claude-3-sonnet"])
        model_row.addWidget(self.model_combo)
        
        # Boutons pour gérer les modèles Ollama
        ollama_buttons = QHBoxLayout()
        
        self.add_ollama_btn = QPushButton("➕")
        self.add_ollama_btn.setToolTip("Ajouter un modèle Ollama")
        self.add_ollama_btn.clicked.connect(self.add_ollama_model)
        self.add_ollama_btn.setFixedSize(30, 25)
        self.add_ollama_btn.setVisible(False)  # Visible seulement pour Ollama
        ollama_buttons.addWidget(self.add_ollama_btn)
        
        self.refresh_ollama_btn = QPushButton("🔄")
        self.refresh_ollama_btn.setToolTip("Rafraîchir la liste des modèles Ollama")
        self.refresh_ollama_btn.clicked.connect(self.refresh_ollama_models)
        self.refresh_ollama_btn.setFixedSize(30, 25)
        self.refresh_ollama_btn.setVisible(False)  # Visible seulement pour Ollama
        ollama_buttons.addWidget(self.refresh_ollama_btn)
        
        model_row.addLayout(ollama_buttons)
        
        provider_layout.addLayout(model_row)
        
        # Paramètres avec explications
        params_group = QGroupBox("Paramètres LLM")
        params_layout = QVBoxLayout(params_group)
        
        # Température avec explication
        temp_row = QHBoxLayout()
        temp_row.addWidget(QLabel("Température:"))
        self.temperature_spin = QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setValue(0.1)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.valueChanged.connect(self.on_temperature_changed)
        temp_row.addWidget(self.temperature_spin)
        
        # Label d'explication de la température
        self.temp_explanation = QLabel("Détermine la créativité (0.0 = déterministe, 2.0 = très créatif)")
        self.temp_explanation.setStyleSheet("color: #666; font-size: 10px; font-style: italic;")
        temp_row.addWidget(self.temp_explanation)
        
        params_layout.addLayout(temp_row)
        
        # Max Tokens
        tokens_row = QHBoxLayout()
        tokens_row.addWidget(QLabel("Max Tokens:"))
        self.max_tokens_spin = QSpinBox()
        self.max_tokens_spin.setRange(100, 4000)
        self.max_tokens_spin.setValue(2000)
        self.max_tokens_spin.setSingleStep(100)
        tokens_row.addWidget(self.max_tokens_spin)
        
        # Label d'explication des tokens
        tokens_explanation = QLabel("Nombre maximum de tokens dans la réponse")
        tokens_explanation.setStyleSheet("color: #666; font-size: 10px; font-style: italic;")
        tokens_row.addWidget(tokens_explanation)
        
        params_layout.addLayout(tokens_row)
        
        provider_layout.addWidget(params_group)
        
        layout.addWidget(provider_group)
        
        # Gestion du prompt
        prompt_group = QGroupBox("Prompt de Test")
        prompt_layout = QVBoxLayout(prompt_group)
        
        # Boutons de gestion du prompt
        prompt_buttons = QHBoxLayout()
        
        self.restore_prompt_btn = QPushButton("Restaurer Prompt Actuel")
        self.restore_prompt_btn.clicked.connect(self.restore_current_prompt)
        prompt_buttons.addWidget(self.restore_prompt_btn)
        
        self.save_prompt_btn = QPushButton("Sauvegarder Prompt")
        self.save_prompt_btn.clicked.connect(self.save_prompt)
        prompt_buttons.addWidget(self.save_prompt_btn)
        
        self.load_prompt_btn = QPushButton("Charger Prompt")
        self.load_prompt_btn.clicked.connect(self.load_prompt)
        prompt_buttons.addWidget(self.load_prompt_btn)
        
        self.load_model_btn = QPushButton("📋 Modèle Référence")
        self.load_model_btn.setToolTip("Charger le modèle d'extraction de référence")
        self.load_model_btn.clicked.connect(self.load_reference_model)
        prompt_buttons.addWidget(self.load_model_btn)
        
        prompt_layout.addLayout(prompt_buttons)
        
        # Éditeur de prompt
        self.prompt_edit = QTextEdit()
        self.prompt_edit.setFont(QFont("Courier", 10))
        self.prompt_edit.setPlaceholderText("Entrez votre prompt de test ici...")
        prompt_layout.addWidget(self.prompt_edit)
        
        layout.addWidget(prompt_group)
        
        # Texte de test
        test_text_group = QGroupBox("Texte de Test")
        test_text_layout = QVBoxLayout(test_text_group)
        
        # Boutons pour le texte de test
        text_buttons = QHBoxLayout()
        
        self.load_pdf_btn = QPushButton("📄 Charger PDF")
        self.load_pdf_btn.setToolTip("Charger et extraire le texte d'un fichier PDF")
        self.load_pdf_btn.clicked.connect(self.load_pdf_text)
        text_buttons.addWidget(self.load_pdf_btn)
        
        self.load_text_btn = QPushButton("📝 Charger Texte")
        self.load_text_btn.setToolTip("Charger un fichier texte (.txt)")
        self.load_text_btn.clicked.connect(self.load_text_file)
        text_buttons.addWidget(self.load_text_btn)
        
        self.preview_text_btn = QPushButton("👁️ Prévisualiser")
        self.preview_text_btn.setToolTip("Prévisualiser le texte extrait dans une fenêtre séparée")
        self.preview_text_btn.clicked.connect(self.preview_extracted_text)
        self.preview_text_btn.setEnabled(False)  # Activé seulement quand il y a du texte
        text_buttons.addWidget(self.preview_text_btn)
        
        self.clear_text_btn = QPushButton("Effacer")
        self.clear_text_btn.clicked.connect(self.clear_test_text)
        text_buttons.addWidget(self.clear_text_btn)
        
        self.generate_example_btn = QPushButton("🎲 Nouvel Exemple")
        self.generate_example_btn.setToolTip("Générer un nouvel exemple de devis aléatoire")
        self.generate_example_btn.clicked.connect(self.generate_new_example)
        text_buttons.addWidget(self.generate_example_btn)
        
        test_text_layout.addLayout(text_buttons)
        
        # Zone de texte de test
        self.test_text_edit = QTextEdit()
        self.test_text_edit.setPlaceholderText("Entrez le texte à analyser ou chargez un fichier...")
        self.test_text_edit.textChanged.connect(self.on_text_changed)
        test_text_layout.addWidget(self.test_text_edit)
        
        layout.addWidget(test_text_group)
        
        # Boutons de test
        test_buttons = QHBoxLayout()
        
        self.test_btn = QPushButton("Lancer Test LLM")
        self.test_btn.setStyleSheet("QPushButton { background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; }")
        self.test_btn.clicked.connect(self.run_llm_test)
        test_buttons.addWidget(self.test_btn)
        
        self.compare_btn = QPushButton("🔍 Comparer avec Référence")
        self.compare_btn.setStyleSheet("QPushButton { background-color: #2196F3; color: white; font-weight: bold; padding: 10px; }")
        self.compare_btn.clicked.connect(self.compare_with_reference)
        self.compare_btn.setVisible(False)  # Visible seulement après un test
        test_buttons.addWidget(self.compare_btn)
        
        layout.addLayout(test_buttons)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        return left_widget
        
    def create_right_panel(self):
        """Création du panneau droit"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Résultats
        results_tab = self.create_results_tab()
        self.tab_widget.addTab(results_tab, "Résultats")
        
        # Onglet Historique
        history_tab = self.create_history_tab()
        self.tab_widget.addTab(history_tab, "Historique Tests")
        
        # Onglet Configuration
        config_tab = self.create_config_tab()
        self.tab_widget.addTab(config_tab, "Configuration")
        
        layout.addWidget(self.tab_widget)
        
        return right_widget
        
    def create_results_tab(self):
        """Création de l'onglet résultats"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Informations du test
        info_group = QGroupBox("Informations du Test")
        info_layout = QVBoxLayout(info_group)
        
        self.test_info_label = QLabel("Aucun test effectué")
        info_layout.addWidget(self.test_info_label)
        
        layout.addWidget(info_group)
        
        # Résultat brut
        result_group = QGroupBox("Résultat Brut")
        result_layout = QVBoxLayout(result_group)
        
        self.result_text = QTextBrowser()
        self.result_text.setFont(QFont("Courier", 9))
        result_layout.addWidget(self.result_text)
        
        layout.addWidget(result_group)
        
        # JSON parsé
        json_group = QGroupBox("JSON Parsé")
        json_layout = QVBoxLayout(json_group)
        
        self.json_text = QTextBrowser()
        self.json_text.setFont(QFont("Courier", 9))
        json_layout.addWidget(self.json_text)
        
        layout.addWidget(json_group)
        
        return widget
        
    def create_history_tab(self):
        """Création de l'onglet historique"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tableau des résultats
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(6)
        self.history_table.setHorizontalHeaderLabels([
            "Date", "Provider", "Modèle", "Succès", "Durée", "Actions"
        ])
        layout.addWidget(self.history_table)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.clear_history_btn = QPushButton("Effacer Historique")
        self.clear_history_btn.clicked.connect(self.clear_history)
        buttons_layout.addWidget(self.clear_history_btn)
        
        self.export_history_btn = QPushButton("Exporter Historique")
        self.export_history_btn.clicked.connect(self.export_history)
        buttons_layout.addWidget(self.export_history_btn)
        
        layout.addLayout(buttons_layout)
        
        return widget
        
    def create_config_tab(self):
        """Création de l'onglet configuration"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Configuration actuelle
        current_config_group = QGroupBox("Configuration Actuelle")
        current_layout = QVBoxLayout(current_config_group)
        
        self.current_config_text = QTextEdit()
        self.current_config_text.setReadOnly(True)
        current_layout.addWidget(self.current_config_text)
        
        layout.addWidget(current_config_group)
        
        # Boutons de configuration
        config_buttons = QHBoxLayout()
        
        self.refresh_config_btn = QPushButton("Actualiser Config")
        self.refresh_config_btn.clicked.connect(self.refresh_config)
        config_buttons.addWidget(self.refresh_config_btn)
        
        self.test_config_btn = QPushButton("Tester Configuration")
        self.test_config_btn.clicked.connect(self.test_configuration)
        config_buttons.addWidget(self.test_config_btn)
        
        layout.addLayout(config_buttons)
        
        return widget
        
    def load_config(self):
        """Chargement de la configuration"""
        try:
            # Charger la configuration actuelle
            current_provider = config.get_current_llm_provider()
            self.provider_combo.setCurrentText(current_provider)
            
            # Charger la clé API si disponible
            if current_provider != "ollama":
                api_key = config.get_llm_api_key(current_provider)
                if api_key:
                    self.api_key_edit.setText(api_key)
            
            # Restaurer le prompt actuel
            self.restore_current_prompt()
            
            # Actualiser la configuration
            self.refresh_config()
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement de la configuration: {e}")
            
    def get_current_prompt(self):
        """Récupération du prompt actuel depuis main.py"""
        try:
            with open("backend/main.py", "r", encoding="utf-8") as f:
                content = f.read()
                
            # Rechercher le prompt dans le code
            start_marker = 'prompt = f"""'
            end_marker = '"""'
            
            start_idx = content.find(start_marker)
            if start_idx != -1:
                start_idx += len(start_marker)
                end_idx = content.find(end_marker, start_idx)
                if end_idx != -1:
                    return content[start_idx:end_idx]
                    
        except Exception as e:
            logger.error(f"Erreur lors de la récupération du prompt: {e}")
            
        return "Prompt non trouvé"
        
    def restore_current_prompt(self):
        """Restaurer le prompt actuel"""
        self.prompt_edit.setPlainText(self.current_prompt)
        self.statusBar().showMessage("Prompt actuel restauré")
        
    def save_prompt(self):
        """Sauvegarder le prompt actuel"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder le prompt", "", "Fichiers texte (*.txt);;Tous les fichiers (*)"
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(self.prompt_edit.toPlainText())
                self.statusBar().showMessage(f"Prompt sauvegardé dans {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {e}")
            
    def load_prompt(self):
        """Charger un prompt depuis un fichier"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Charger un prompt", "", "Fichiers texte (*.txt);;Tous les fichiers (*)"
            )
            if filename:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                self.prompt_edit.setPlainText(content)
                self.statusBar().showMessage(f"Prompt chargé depuis {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement: {e}")
            
    def load_pdf_text(self):
        """Charger le texte d'un PDF avec extraction améliorée"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Charger un PDF", "", "Fichiers PDF (*.pdf)"
            )
            if filename:
                self.statusBar().showMessage("Extraction du texte PDF en cours...")
                
                # Essayer d'abord avec PyMuPDF (plus rapide et fiable)
                try:
                    import fitz  # PyMuPDF
                    doc = fitz.open(filename)
                    text_parts = []
                    
                    for page_num in range(len(doc)):
                        page = doc.load_page(page_num)
                        page_text = page.get_text()
                        if page_text.strip():  # Ignorer les pages vides
                            text_parts.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
                    
                    doc.close()
                    extracted_text = "\n\n".join(text_parts)
                    
                    if not extracted_text.strip():
                        raise Exception("Aucun texte extrait du PDF")
                    
                    # Nettoyer le texte extrait
                    cleaned_text = self.clean_extracted_text(extracted_text)
                    
                    # Afficher le texte dans l'éditeur
                    self.test_text_edit.setPlainText(cleaned_text)
                    
                    # Activer le bouton de prévisualisation
                    self.preview_text_btn.setEnabled(True)
                    
                    # Afficher les statistiques d'extraction
                    char_count = len(cleaned_text)
                    word_count = len(cleaned_text.split())
                    page_count = len(doc)
                    
                    self.statusBar().showMessage(
                        f"PDF chargé: {filename} | {page_count} pages | {word_count} mots | {char_count} caractères"
                    )
                    
                    # Afficher un message de confirmation
                    QMessageBox.information(
                        self, 
                        "PDF Chargé", 
                        f"Texte extrait avec succès !\n\n"
                        f"📄 Pages: {page_count}\n"
                        f"📝 Mots: {word_count}\n"
                        f"🔤 Caractères: {char_count}\n\n"
                        f"Le texte est maintenant prêt pour les tests LLM.\n"
                        f"Utilisez le bouton '👁️ Prévisualiser' pour voir le texte extrait."
                    )
                    
                except ImportError:
                    # Fallback si PyMuPDF n'est pas installé
                    self.extract_pdf_with_pypdf2(filename)
                except Exception as e:
                    # Si PyMuPDF échoue, essayer avec PyPDF2
                    self.statusBar().showMessage(f"PyMuPDF échoué, tentative avec PyPDF2...")
                    self.extract_pdf_with_pypdf2(filename)
                    
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement du PDF: {e}")
            self.statusBar().showMessage("Erreur lors du chargement du PDF")
    
    def extract_pdf_with_pypdf2(self, filename):
        """Extraire le texte PDF avec PyPDF2 (fallback)"""
        try:
            import PyPDF2
            
            with open(filename, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text_parts = []
                
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_parts.append(f"--- PAGE {page_num + 1} ---\n{page_text}")
                
                extracted_text = "\n\n".join(text_parts)
                
                if not extracted_text.strip():
                    raise Exception("Aucun texte extrait du PDF")
                
                # Nettoyer le texte extrait
                cleaned_text = self.clean_extracted_text(extracted_text)
                
                # Afficher le texte dans l'éditeur
                self.test_text_edit.setPlainText(cleaned_text)
                
                # Activer le bouton de prévisualisation
                self.preview_text_btn.setEnabled(True)
                
                # Afficher les statistiques
                char_count = len(cleaned_text)
                word_count = len(cleaned_text.split())
                page_count = len(pdf_reader.pages)
                
                self.statusBar().showMessage(
                    f"PDF chargé (PyPDF2): {filename} | {page_count} pages | {word_count} mots | {char_count} caractères"
                )
                
        except ImportError:
            raise Exception("Aucune bibliothèque PDF disponible. Installez PyMuPDF ou PyPDF2")
        except Exception as e:
            raise Exception(f"Erreur PyPDF2: {e}")
    
    def clean_extracted_text(self, text):
        """Nettoyer le texte extrait du PDF"""
        if not text:
            return text
        
        # Supprimer les caractères de contrôle indésirables
        import re
        
        # Remplacer les sauts de ligne multiples par des sauts simples
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Supprimer les espaces en début et fin de ligne
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            # Nettoyer la ligne
            cleaned_line = line.strip()
            
            # Ignorer les lignes vides ou avec seulement des caractères spéciaux
            if cleaned_line and not re.match(r'^[\s\-_=*#]+$', cleaned_line):
                cleaned_lines.append(cleaned_line)
        
        # Rejoindre les lignes
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Supprimer les espaces en début et fin
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text
    
    def preview_extracted_text(self):
        """Prévisualiser le texte extrait dans une fenêtre séparée"""
        try:
            text = self.test_text_edit.toPlainText()
            if not text.strip():
                QMessageBox.warning(self, "Aucun texte", "Aucun texte à prévisualiser")
                return
            
            # Créer une fenêtre de prévisualisation
            preview_dialog = QDialog(self)
            preview_dialog.setWindowTitle("Prévisualisation du Texte Extrait")
            preview_dialog.setModal(True)
            preview_dialog.resize(800, 600)
            
            layout = QVBoxLayout(preview_dialog)
            
            # Zone de texte pour la prévisualisation
            preview_text = QTextEdit()
            preview_text.setPlainText(text)
            preview_text.setReadOnly(True)
            preview_text.setFont(QFont("Courier", 10))
            layout.addWidget(preview_text)
            
            # Statistiques du texte
            char_count = len(text)
            word_count = len(text.split())
            line_count = len(text.split('\n'))
            
            stats_label = QLabel(
                f"📊 Statistiques: {char_count} caractères | {word_count} mots | {line_count} lignes"
            )
            stats_label.setStyleSheet("color: #666; font-weight: bold; padding: 5px;")
            layout.addWidget(stats_label)
            
            # Boutons
            button_layout = QHBoxLayout()
            
            copy_btn = QPushButton("📋 Copier")
            copy_btn.clicked.connect(lambda: self.copy_text_to_clipboard(text))
            button_layout.addWidget(copy_btn)
            
            save_btn = QPushButton("💾 Sauvegarder")
            save_btn.clicked.connect(lambda: self.save_extracted_text(text))
            button_layout.addWidget(save_btn)
            
            close_btn = QPushButton("Fermer")
            close_btn.clicked.connect(preview_dialog.accept)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            
            preview_dialog.exec()
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la prévisualisation: {e}")
    
    def copy_text_to_clipboard(self, text):
        """Copier le texte dans le presse-papiers"""
        try:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            self.statusBar().showMessage("Texte copié dans le presse-papiers")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la copie: {e}")
    
    def save_extracted_text(self, text):
        """Sauvegarder le texte extrait dans un fichier"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Sauvegarder le texte extrait", "", "Fichiers texte (*.txt)"
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(text)
                self.statusBar().showMessage(f"Texte sauvegardé: {filename}")
                QMessageBox.information(self, "Succès", f"Texte sauvegardé dans {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {e}")
    
    def on_text_changed(self):
        """Gestionnaire de changement de texte"""
        text = self.test_text_edit.toPlainText()
        has_text = bool(text.strip())
        
        # Activer/désactiver le bouton de prévisualisation
        self.preview_text_btn.setEnabled(has_text)
        
        # Mettre à jour le statut
        if has_text:
            char_count = len(text)
            word_count = len(text.split())
            self.statusBar().showMessage(f"Texte prêt: {word_count} mots, {char_count} caractères")
        else:
            self.statusBar().showMessage("Prêt")
    
    def load_text_file(self):
        """Charger un fichier texte"""
        try:
            filename, _ = QFileDialog.getOpenFileName(
                self, "Charger un fichier texte", "", "Fichiers texte (*.txt);;Tous les fichiers (*)"
            )
            if filename:
                with open(filename, "r", encoding="utf-8") as f:
                    content = f.read()
                self.test_text_edit.setPlainText(content)
                
                # Activer le bouton de prévisualisation
                self.preview_text_btn.setEnabled(True)
                
                # Afficher les statistiques
                char_count = len(content)
                word_count = len(content.split())
                
                self.statusBar().showMessage(f"Fichier chargé: {filename} | {word_count} mots | {char_count} caractères")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement: {e}")
            
    def clear_test_text(self):
        """Effacer le texte de test"""
        self.test_text_edit.clear()
        
    def on_provider_changed(self, provider):
        """Gestion du changement de provider"""
        # Mettre à jour les modèles disponibles selon le provider
        self.model_combo.clear()
        
        if provider == "ollama":
            # Charger les modèles Ollama disponibles
            self.load_ollama_models()
        elif provider == "openrouter":
            self.model_combo.addItems(["openai/gpt-4-turbo", "openai/gpt-3.5-turbo", "anthropic/claude-3-sonnet"])
        elif provider == "openai":
            self.model_combo.addItems(["gpt-4-turbo", "gpt-3.5-turbo"])
        elif provider == "anthropic":
            self.model_combo.addItems(["claude-3-sonnet", "claude-3-haiku"])
        
        # Synchroniser la clé API depuis la configuration centrale
        if provider != "ollama":
            api_key = config.get_llm_api_key(provider)
            if api_key:
                self.api_key_edit.setText(api_key)
                self.statusBar().showMessage(f"Clé API {provider} chargée depuis la configuration")
            else:
                self.api_key_edit.clear()
                self.statusBar().showMessage(f"Aucune clé API configurée pour {provider}")
        else:
            self.api_key_edit.clear()
            self.statusBar().showMessage("Ollama ne nécessite pas de clé API")
        
        # Afficher/masquer les boutons de gestion Ollama
        self.add_ollama_btn.setVisible(provider == "ollama")
        self.refresh_ollama_btn.setVisible(provider == "ollama")
    
    def load_ollama_models(self):
        """Charger les modèles Ollama disponibles"""
        try:
            import subprocess
            import json
            
            self.statusBar().showMessage("Chargement des modèles Ollama...")
            
            # Commande pour lister les modèles (sans --json pour compatibilité)
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                try:
                    # Parser la sortie textuelle d'ollama list
                    lines = result.stdout.strip().split('\n')
                    model_names = []
                    
                    # Ignorer la première ligne (en-tête)
                    for line in lines[1:]:  # Skip header line
                        if line.strip():
                            # Nettoyer la ligne et extraire le nom du modèle
                            # Format: NAME                                  ID              SIZE      MODIFIED
                            line = line.strip()
                            
                            # Chercher l'ID (12 caractères hexadécimaux)
                            import re
                            id_match = re.search(r'([a-f0-9]{12})', line)
                            if id_match:
                                # Prendre tout ce qui est avant l'ID
                                id_pos = id_match.start()
                                model_name = line[:id_pos].strip()
                                if model_name:
                                    model_names.append(model_name)
                    
                    if model_names:
                        # Vider la liste actuelle
                        self.model_combo.clear()
                        self.model_combo.addItems(model_names)
                        self.statusBar().showMessage(f"{len(model_names)} modèles Ollama chargés: {', '.join(model_names[:3])}{'...' if len(model_names) > 3 else ''}")
                    else:
                        # Modèles par défaut si aucun modèle n'est trouvé
                        self.model_combo.clear()
                        self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
                        self.statusBar().showMessage("Aucun modèle Ollama trouvé, modèles par défaut chargés")
                        
                except Exception as e:
                    # En cas d'erreur de parsing, utiliser les modèles par défaut
                    self.model_combo.clear()
                    self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
                    self.statusBar().showMessage(f"Erreur de parsing: {str(e)}, modèles par défaut chargés")
            else:
                # En cas d'erreur, utiliser les modèles par défaut
                self.model_combo.clear()
                self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
                self.statusBar().showMessage(f"Erreur Ollama (code {result.returncode}): {result.stderr}")
                
        except subprocess.TimeoutExpired as e:
            # Timeout spécifique
            self.model_combo.clear()
            self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
            self.statusBar().showMessage("Timeout lors du chargement des modèles Ollama (60s), modèles par défaut chargés")
        except FileNotFoundError as e:
            # Ollama non installé
            self.model_combo.clear()
            self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
            self.statusBar().showMessage("Ollama non installé ou non trouvé dans le PATH")
        except Exception as e:
            # Erreur générale
            self.model_combo.clear()
            self.model_combo.addItems(["mistral:latest", "llama2:latest", "codellama:latest"])
            self.statusBar().showMessage(f"Erreur inattendue: {str(e)}")
    
    def on_temperature_changed(self, value):
        """Mise à jour de l'explication de la température"""
        if value == 0.0:
            explanation = "Déterministe - Réponses cohérentes et prévisibles"
        elif value <= 0.3:
            explanation = "Faible créativité - Réponses structurées et précises"
        elif value <= 0.7:
            explanation = "Créativité modérée - Équilibré entre précision et créativité"
        elif value <= 1.0:
            explanation = "Créativité élevée - Réponses variées et originales"
        else:
            explanation = "Très créatif - Réponses très variées et imprévisibles"
        
        self.temp_explanation.setText(f"Température {value}: {explanation}")
    
    def add_ollama_model(self):
        """Ajouter un modèle Ollama"""
        try:
            from PyQt6.QtWidgets import QInputDialog
            
            model_name, ok = QInputDialog.getText(
                self, 
                "Ajouter un modèle Ollama", 
                "Nom du modèle (ex: llama2:latest, codellama:7b):"
            )
            
            if ok and model_name.strip():
                model_name = model_name.strip()
                
                # Vérifier si le modèle existe déjà
                existing_models = [self.model_combo.itemText(i) for i in range(self.model_combo.count())]
                if model_name in existing_models:
                    QMessageBox.information(self, "Info", f"Le modèle '{model_name}' existe déjà")
                    return
                
                # Ajouter le modèle à la liste
                self.model_combo.addItem(model_name)
                self.model_combo.setCurrentText(model_name)
                
                # Demander si l'utilisateur veut télécharger le modèle
                reply = QMessageBox.question(
                    self, 
                    "Télécharger le modèle", 
                    f"Voulez-vous télécharger le modèle '{model_name}' maintenant ?\n\n"
                    "Cela peut prendre plusieurs minutes selon la taille du modèle.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.download_ollama_model(model_name)
                    
                self.statusBar().showMessage(f"Modèle '{model_name}' ajouté")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'ajout du modèle: {e}")
    
    def load_reference_model(self):
        """Charger le modèle d'extraction de référence"""
        try:
            # Charger le modèle de référence
            with open("modele_extraction_reference.json", "r", encoding="utf-8") as f:
                reference_model = json.load(f)
            
            # Créer un prompt basé sur le modèle de référence
            prompt_template = self.create_prompt_from_reference(reference_model)
            
            # Charger le prompt dans l'éditeur
            self.prompt_edit.setPlainText(prompt_template)
            
            # Créer un exemple de texte de test
            example_text = self.create_example_text_from_reference(reference_model)
            self.test_text_edit.setPlainText(example_text)
            
            self.statusBar().showMessage("Modèle de référence chargé avec succès")
            
            # Afficher une boîte de dialogue avec des informations
            QMessageBox.information(self, "Modèle de Référence", 
                "Modèle d'extraction de référence chargé !\n\n"
                "✅ Prompt adapté au format JSON exact\n"
                "✅ Exemple de texte de test généré\n"
                "✅ Structure complète avec tous les champs\n\n"
                "Vous pouvez maintenant tester l'extraction avec ce format optimisé.")
            
        except FileNotFoundError:
            QMessageBox.warning(self, "Erreur", 
                "Fichier modele_extraction_reference.json non trouvé.\n"
                "Assurez-vous que le fichier existe dans le répertoire.")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du chargement du modèle: {e}")
    
    def create_prompt_from_reference(self, reference_model):
        """Créer un prompt optimisé basé sur le modèle de référence"""
        prompt = f'''Tu es un assistant d'extraction spécialisé pour des devis de literie. Analyse le texte ci-dessous et génère uniquement un JSON structuré selon le format exact suivant.

TEXTE À ANALYSER :
{{text}}

RÈGLES D'EXTRACTION STRICTES :

1. STRUCTURE JSON OBLIGATOIRE :
{{
  "societe": {{
    "nom": "nom de l'entreprise",
    "capital": "capital social",
    "adresse": "adresse complète",
    "telephone": "numéro de téléphone",
    "email": "adresse email",
    "siret": "numéro SIRET",
    "APE": "code APE",
    "CEE": "numéro CEE",
    "banque": "nom de la banque",
    "IBAN": "numéro IBAN"
  }},
  "client": {{
    "nom": "nom du client",
    "adresse": "adresse du client",
    "code_client": "code client"
  }},
  "commande": {{
    "numero": "numéro de commande",
    "date": "date de commande",
    "date_validite": "date de validité",
    "commercial": "nom du commercial",
    "origine": "origine de la commande"
  }},
  "mode_mise_a_disposition": {{
    "emporte_client_C57": "texte si enlèvement client",
    "fourgon_C58": "texte si livraison fourgon",
    "transporteur_C59": "texte si transporteur"
  }},
  "articles": [
    {{
      "type": "matelas|sommier|accessoire|tête de lit|pieds|remise",
      "description": "description complète de l'article",
      "titre_cote": "Mr/Mme Gauche/Droit si applicable",
      "information": "en-tête comme '1/ CHAMBRE XYZ' si présent",
      "quantite": nombre,
      "dimensions": "format LxlxH",
      "noyau": "type de noyau pour matelas",
      "fermete": "niveau de fermeté",
      "housse": "type de housse",
      "matiere_housse": "matériau de la housse",
      "autres_caracteristiques": {{
        "caracteristique1": "valeur1",
        "caracteristique2": "valeur2"
      }}
    }}
  ],
  "paiement": {{
    "conditions": "conditions de paiement",
    "port_ht": montant_ht_port,
    "base_ht": montant_ht_total,
    "taux_tva": pourcentage_tva,
    "total_ttc": montant_ttc,
    "acompte": montant_acompte,
    "net_a_payer": montant_final
  }}
}}

2. RÈGLES SPÉCIFIQUES :
- Pour chaque article, extraire TOUS les champs disponibles
- Le champ "autres_caracteristiques" doit contenir les spécificités non standard
- Les remises sont des articles de type "remise" avec montant dans autres_caracteristiques
- Les dimensions doivent être au format "LxlxH" (ex: "159x199x19")
- Les montants doivent être des nombres (pas de texte)
- Si une information est absente : null pour les nombres, "" pour les textes

3. EXEMPLE DE RÉFÉRENCE :
{json.dumps(reference_model, indent=2, ensure_ascii=False)}

Réponds UNIQUEMENT avec un JSON valide selon cette structure exacte.'''
        
        return prompt
    
    def create_example_text_from_reference(self, reference_model):
        """Créer un exemple de texte basé sur le modèle de référence"""
        # Générer un exemple aléatoire
        return self.generate_random_devis_example()
    
    def generate_random_devis_example(self):
        """Générer un exemple de devis aléatoire pour les tests"""
        import random
        from datetime import datetime, timedelta
        
        # Données aléatoires pour varier les exemples
        clients = [
            ("Mr et Me LAGADEC HELENE", "25 RUE DE L'ÉGLISE, 59670 BAVINCHOVE", "LAGAHEBAV"),
            ("Mr DUPONT JEAN", "15 AVENUE DE LA PAIX, 59000 LILLE", "DUPOJEALIL"),
            ("Me MARTIN SOPHIE", "8 RUE DU COMMERCE, 59100 ROUBAIX", "MARTSOPROU"),
            ("Mr et Me DURAND PIERRE", "42 BOULEVARD VICTOR HUGO, 59200 TOURCOING", "DURAPIEVIC"),
            ("Mr LEROY ANTOINE", "3 PLACE DE LA RÉPUBLIQUE, 59300 VALENCIENNES", "LEROANTPLA")
        ]
        
        produits = [
            ("LITERIE 160/200/59 CM JUMEAUX SUR PIEDS", [
                "SOMMIERS JUMEAUX RELAXATION MOTORISÉE 5 PLIS PETITE TÊTIÈRE",
                "MÉTRAGE PVC SARANO CAMEL",
                "DOSSERET GALBÉ COINS VIFS 160/90 BASE SOMMIERS",
                "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + 2 PIEDS CENTRAUX + PATINS FEUTRES",
                "MATELAS JUMEAUX - MOUSSE RAINURÉE 7 ZONES DIFFÉRENCIÉES MÉDIUM (50KG/M3)"
            ]),
            ("LITERIE 140/190/59 CM DOUBLE SUR PIEDS", [
                "SOMMIER DOUBLE RELAXATION MOTORISÉE 5 PLIS GRANDE TÊTIÈRE",
                "MÉTRAGE PVC SARANO GRIS",
                "DOSSERET GALBÉ COINS VIFS 140/90 BASE SOMMIERS",
                "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + PATINS FEUTRES",
                "MATELAS DOUBLE - MOUSSE VISCOÉLASTIQUE 7 ZONES DIFFÉRENCIÉES FERME (60KG/M3)"
            ]),
            ("LITERIE 90/200/59 CM SIMPLE SUR PIEDS", [
                "SOMMIER SIMPLE RELAXATION MOTORISÉE 5 PLIS PETITE TÊTIÈRE",
                "MÉTRAGE PVC SARANO BLANC",
                "DOSSERET DROIT COINS VIFS 90/90 BASE SOMMIERS",
                "JEU DE 4 PIEDS CYLINDRE VERNI NATUREL 20 CM + PATINS FEUTRES",
                "MATELAS SIMPLE - LATEX NATUREL 7 ZONES DIFFÉRENCIÉES DOUX (70KG/M3)"
            ])
        ]
        
        remises = [
            ("REMISE 50% SOLDES MODÈLE D'EXPOSITION", -1295.00),
            ("REMISE 30% FIN DE SÉRIE", -850.00),
            ("REMISE 20% PREMIÈRE COMMANDE", -450.00),
            ("REMISE 15% CLIENT FIDÈLE", -320.00),
            ("REMISE 10% PAIEMENT COMPTANT", -180.00)
        ]
        
        # Sélection aléatoire
        client = random.choice(clients)
        produit = random.choice(produits)
        remise = random.choice(remises)
        
        # Date aléatoire dans les 30 derniers jours
        date_commande = datetime.now() - timedelta(days=random.randint(0, 30))
        
        # Numéro de commande aléatoire
        num_commande = f"CM{random.randint(100000, 999999)}"
        
        # Montants aléatoires
        base_ht = random.randint(1500, 3000)
        tva = base_ht * 0.20
        total_ttc = base_ht + tva
        acompte = random.randint(500, 1000)
        net_a_payer = total_ttc - acompte
        
        # Générer le devis
        example_text = f"""DEVIS LITERIE WESTELYNCK

SAS Literie Westelynck
Capital : 23 100 Euros
525 RD 642 - 59190 BORRE
Tél : 03.28.48.04.19
Email : contact@lwest.fr
SIRET : 429 352 891 00015
APE : 3103Z
CEE : FR50 429 352 891
Banque : Crédit Agricole d'Hazebrouck
IBAN : FR76 1670 6050 1650 4613 2602 341

CLIENT :
{client[0]}
{client[1]}
Code client : {client[2]}

COMMANDE N° {num_commande}
Date : {date_commande.strftime('%d/%m/%Y')}
Commercial : P. ALINE
Origine : COMMANDE

LIVRAISON : ENLÈVEMENT PAR VOS SOINS

{produit[0]}

"""
        
        # Ajouter les produits
        for i, prod in enumerate(produit[1], 1):
            example_text += f"{i}. {prod}\n   Quantité : {random.randint(1, 3)}\n\n"
        
        # Ajouter la remise
        example_text += f"{len(produit[1]) + 1}. {remise[0]}\n   Montant : {remise[1]:.2f}€\n\n"
        
        # Ajouter la remise enlèvement
        remise_enlevement = random.randint(20, 100)
        example_text += f"{len(produit[1]) + 2}. REMISE : 5% ENLÈVEMENT PAR VOS SOINS\n   Montant : -{remise_enlevement:.2f}€\n\n"
        
        # Conditions de paiement et totaux
        example_text += f"""CONDITIONS DE PAIEMENT :
ACOMPTE DE {acompte} € EN CB LA COMMANDE ET SOLDE DE {net_a_payer:.0f} € À L'ENLÈVEMENT

PORT HT : 0,00€
BASE HT : {base_ht:.2f}€
TVA 20% : {tva:.2f}€
TOTAL TTC : {total_ttc:.2f}€
ACOMPTE : {acompte:.2f}€
NET À PAYER : {net_a_payer:.2f}€"""
        
        return example_text
    
    def generate_new_example(self):
        """Générer un nouvel exemple de devis"""
        try:
            # Charger le modèle de référence pour la cohérence
            with open("modele_extraction_reference.json", "r", encoding="utf-8") as f:
                reference_model = json.load(f)
            
            # Générer un nouvel exemple
            new_example = self.generate_random_devis_example()
            
            # Mettre à jour le texte de test
            self.test_text_edit.setPlainText(new_example)
            
            self.statusBar().showMessage("Nouvel exemple de devis généré")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la génération d'exemple: {e}")
    
    def refresh_ollama_models(self):
        """Rafraîchir la liste des modèles Ollama"""
        try:
            # Sauvegarder le modèle actuellement sélectionné
            current_model = self.model_combo.currentText()
            
            # Recharger les modèles
            self.load_ollama_models()
            
            # Restaurer le modèle sélectionné s'il existe encore
            if current_model:
                index = self.model_combo.findText(current_model)
                if index >= 0:
                    self.model_combo.setCurrentIndex(index)
            
            self.statusBar().showMessage("Liste des modèles Ollama rafraîchie")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du rafraîchissement: {e}")
    
    def download_ollama_model(self, model_name):
        """Télécharger un modèle Ollama"""
        try:
            import subprocess
            import sys
            
            # Créer un thread pour le téléchargement
            self.download_thread = OllamaDownloadThread(model_name)
            self.download_thread.progress_update.connect(self.on_download_progress)
            self.download_thread.download_completed.connect(self.on_download_completed)
            self.download_thread.download_error.connect(self.on_download_error)
            self.download_thread.start()
            
            self.statusBar().showMessage(f"Téléchargement de '{model_name}' en cours...")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du téléchargement: {e}")
    
    def on_download_progress(self, message):
        """Mise à jour de la progression du téléchargement"""
        self.statusBar().showMessage(message)
    
    def on_download_completed(self, model_name):
        """Téléchargement terminé"""
        QMessageBox.information(self, "Succès", f"Modèle '{model_name}' téléchargé avec succès !")
        self.statusBar().showMessage(f"Modèle '{model_name}' prêt à utiliser")
    
    def on_download_error(self, error):
        """Erreur de téléchargement"""
        QMessageBox.warning(self, "Erreur", f"Erreur lors du téléchargement: {error}")
        self.statusBar().showMessage("Erreur de téléchargement")
    
    def sync_api_key(self):
        """Synchroniser la clé API depuis la configuration centrale"""
        try:
            provider = self.provider_combo.currentText()
            if provider == "ollama":
                self.api_key_edit.clear()
                self.statusBar().showMessage("Ollama ne nécessite pas de clé API")
                return
                
            api_key = config.get_llm_api_key(provider)
            if api_key:
                self.api_key_edit.setText(api_key)
                self.statusBar().showMessage(f"Clé API {provider} synchronisée depuis la configuration centrale")
            else:
                self.api_key_edit.clear()
                self.statusBar().showMessage(f"Aucune clé API configurée pour {provider}")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la synchronisation: {e}")
            
    def run_llm_test(self):
        """Lancer un test LLM"""
        try:
            # Récupération des paramètres
            provider = self.provider_combo.currentText()
            
            # Récupérer la clé API depuis la configuration centrale
            if provider == "ollama":
                api_key = None
            else:
                api_key = config.get_llm_api_key(provider)
                if not api_key:
                    # Fallback sur le champ de saisie
                    api_key = self.api_key_edit.text().strip()
            
            model = self.model_combo.currentText()
            temperature = self.temperature_spin.value()
            max_tokens = self.max_tokens_spin.value()
            
            # Récupération du prompt et du texte de test
            prompt_template = self.prompt_edit.toPlainText()
            test_text = self.test_text_edit.toPlainText()
            
            if not prompt_template.strip():
                QMessageBox.warning(self, "Erreur", "Le prompt ne peut pas être vide")
                return
                
            if not test_text.strip():
                QMessageBox.warning(self, "Erreur", "Le texte de test ne peut pas être vide")
                return
                
            # Vérification de la clé API
            if provider != "ollama" and not api_key:
                QMessageBox.warning(self, "Erreur", f"Clé API requise pour {provider}")
                return
                
            # Préparation du prompt final
            prompt = prompt_template.replace("{text}", test_text)
            
            # Désactiver le bouton pendant le test
            self.test_btn.setEnabled(False)
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indéterminé
            
            # Lancer le test dans un thread
            self.worker = LLMTestWorker(
                prompt, provider, api_key, model, temperature, max_tokens
            )
            self.worker.result_ready.connect(self.on_test_completed)
            self.worker.progress_update.connect(self.on_progress_update)
            self.worker.start()
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du lancement du test: {e}")
            self.test_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            
    def on_progress_update(self, message):
        """Mise à jour de la progression"""
        self.statusBar().showMessage(message)
        
    def on_test_completed(self, result):
        """Gestion de la fin du test"""
        try:
            # Réactiver le bouton
            self.test_btn.setEnabled(True)
            self.progress_bar.setVisible(False)
            
            # Affichage des résultats
            self.display_test_results(result)
            
            # Ajout à l'historique
            self.add_to_history(result)
            
            self.statusBar().showMessage("Test terminé")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du traitement des résultats: {e}")
    
    def compare_with_reference(self):
        """Comparer le résultat avec le modèle de référence"""
        try:
            # Récupérer le résultat actuel
            current_result = self.result_text.toPlainText().strip()
            if not current_result:
                QMessageBox.warning(self, "Erreur", "Aucun résultat à comparer")
                return
            
            # Charger le modèle de référence
            with open("modele_extraction_reference.json", "r", encoding="utf-8") as f:
                reference_model = json.load(f)
            
            # Parser le résultat actuel
            try:
                # Nettoyer le contenu
                cleaned_content = current_result
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                
                current_json = json.loads(cleaned_content)
            except json.JSONDecodeError as e:
                QMessageBox.warning(self, "Erreur", f"Résultat JSON invalide: {e}")
                return
            
            # Comparer les structures
            comparison_result = self.compare_json_structures(reference_model, current_json)
            
            # Afficher le résultat de comparaison
            self.show_comparison_dialog(comparison_result)
            
        except FileNotFoundError:
            QMessageBox.warning(self, "Erreur", "Fichier de référence non trouvé")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la comparaison: {e}")
    
    def compare_json_structures(self, reference, current, path=""):
        """Comparer deux structures JSON"""
        comparison = {
            "valid": True,
            "missing_fields": [],
            "extra_fields": [],
            "type_mismatches": [],
            "details": []
        }
        
        if isinstance(reference, dict) and isinstance(current, dict):
            # Vérifier les champs manquants
            for key in reference:
                full_path = f"{path}.{key}" if path else key
                if key not in current:
                    comparison["missing_fields"].append(full_path)
                    comparison["valid"] = False
                else:
                    # Comparer récursivement
                    sub_comparison = self.compare_json_structures(reference[key], current[key], full_path)
                    comparison["missing_fields"].extend(sub_comparison["missing_fields"])
                    comparison["extra_fields"].extend(sub_comparison["extra_fields"])
                    comparison["type_mismatches"].extend(sub_comparison["type_mismatches"])
                    comparison["details"].extend(sub_comparison["details"])
                    if not sub_comparison["valid"]:
                        comparison["valid"] = False
            
            # Vérifier les champs supplémentaires
            for key in current:
                if key not in reference:
                    full_path = f"{path}.{key}" if path else key
                    comparison["extra_fields"].append(full_path)
        
        elif isinstance(reference, list) and isinstance(current, list):
            # Pour les listes, vérifier au moins la structure du premier élément
            if reference and current:
                if isinstance(reference[0], dict) and isinstance(current[0], dict):
                    sub_comparison = self.compare_json_structures(reference[0], current[0], f"{path}[0]")
                    comparison["missing_fields"].extend(sub_comparison["missing_fields"])
                    comparison["extra_fields"].extend(sub_comparison["extra_fields"])
                    comparison["type_mismatches"].extend(sub_comparison["type_mismatches"])
                    comparison["details"].extend(sub_comparison["details"])
                    if not sub_comparison["valid"]:
                        comparison["valid"] = False
        
        elif type(reference) != type(current):
            comparison["type_mismatches"].append(f"{path}: {type(reference).__name__} vs {type(current).__name__}")
            comparison["valid"] = False
        
        return comparison
    
    def show_comparison_dialog(self, comparison):
        """Afficher le dialogue de comparaison"""
        dialog = QMessageBox()
        dialog.setWindowTitle("Comparaison avec le Modèle de Référence")
        
        if comparison["valid"]:
            dialog.setIcon(QMessageBox.Icon.Information)
            dialog.setText("✅ Structure JSON Valide")
            dialog.setInformativeText("Le résultat respecte parfaitement la structure de référence !")
        else:
            dialog.setIcon(QMessageBox.Icon.Warning)
            dialog.setText("⚠️ Différences Détectées")
            
            details = []
            if comparison["missing_fields"]:
                details.append(f"Champs manquants : {len(comparison['missing_fields'])}")
                for field in comparison["missing_fields"][:5]:  # Limiter à 5
                    details.append(f"  • {field}")
                if len(comparison["missing_fields"]) > 5:
                    details.append(f"  • ... et {len(comparison['missing_fields']) - 5} autres")
            
            if comparison["extra_fields"]:
                details.append(f"Champs supplémentaires : {len(comparison['extra_fields'])}")
                for field in comparison["extra_fields"][:5]:
                    details.append(f"  • {field}")
                if len(comparison["extra_fields"]) > 5:
                    details.append(f"  • ... et {len(comparison['extra_fields']) - 5} autres")
            
            if comparison["type_mismatches"]:
                details.append(f"Types incorrects : {len(comparison['type_mismatches'])}")
                for mismatch in comparison["type_mismatches"][:3]:
                    details.append(f"  • {mismatch}")
            
            dialog.setInformativeText("\n".join(details))
        
        dialog.exec()
            
    def display_test_results(self, result):
        """Affichage des résultats du test"""
        # Informations du test
        provider = self.provider_combo.currentText()
        model = self.model_combo.currentText()
        
        info_text = f"""
Provider: {provider}
Modèle: {model}
Température: {self.temperature_spin.value()}
Max Tokens: {self.max_tokens_spin.value()}
Succès: {'Oui' if result.get('success', False) else 'Non'}
"""
        
        if not result.get('success', False):
            info_text += f"Erreur: {result.get('error', 'Erreur inconnue')}"
            
        self.test_info_label.setText(info_text)
        
        # Résultat brut
        content = result.get('content', '')
        self.result_text.setPlainText(content)
        
        # Tentative de parsing JSON
        try:
            if content.strip():
                # Nettoyer le contenu
                cleaned_content = content.strip()
                if cleaned_content.startswith('```json'):
                    cleaned_content = cleaned_content[7:]
                
                # Ajouter un bouton pour comparer avec le modèle de référence
                if hasattr(self, 'compare_btn'):
                    self.compare_btn.setVisible(True)
                if cleaned_content.endswith('```'):
                    cleaned_content = cleaned_content[:-3]
                    
                parsed_json = json.loads(cleaned_content)
                formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                self.json_text.setPlainText(formatted_json)
            else:
                self.json_text.setPlainText("Aucun contenu à parser")
        except json.JSONDecodeError as e:
            self.json_text.setPlainText(f"Erreur de parsing JSON: {e}\n\nContenu reçu:\n{content}")
        except Exception as e:
            self.json_text.setPlainText(f"Erreur: {e}")
            
    def add_to_history(self, result):
        """Ajout du résultat à l'historique"""
        try:
            # Créer l'entrée d'historique
            history_entry = {
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'provider': self.provider_combo.currentText(),
                'model': self.model_combo.currentText(),
                'success': result.get('success', False),
                'error': result.get('error', ''),
                'content': result.get('content', ''),
                'temperature': self.temperature_spin.value(),
                'max_tokens': self.max_tokens_spin.value()
            }
            
            self.test_results.append(history_entry)
            
            # Mettre à jour le tableau
            self.update_history_table()
            
        except Exception as e:
            logger.error(f"Erreur lors de l'ajout à l'historique: {e}")
            
    def update_history_table(self):
        """Mise à jour du tableau d'historique"""
        try:
            self.history_table.setRowCount(len(self.test_results))
            
            for i, result in enumerate(self.test_results):
                # Date
                self.history_table.setItem(i, 0, QTableWidgetItem(result['date']))
                
                # Provider
                self.history_table.setItem(i, 1, QTableWidgetItem(result['provider']))
                
                # Modèle
                self.history_table.setItem(i, 2, QTableWidgetItem(result['model']))
                
                # Succès
                success_text = "✅" if result['success'] else "❌"
                self.history_table.setItem(i, 3, QTableWidgetItem(success_text))
                
                # Durée (placeholder pour l'instant)
                self.history_table.setItem(i, 4, QTableWidgetItem("N/A"))
                
                # Actions
                actions_widget = QWidget()
                actions_layout = QHBoxLayout(actions_widget)
                
                view_btn = QPushButton("Voir")
                view_btn.clicked.connect(lambda checked, idx=i: self.view_history_result(idx))
                actions_layout.addWidget(view_btn)
                
                actions_widget.setLayout(actions_layout)
                self.history_table.setCellWidget(i, 5, actions_widget)
                
        except Exception as e:
            logger.error(f"Erreur lors de la mise à jour du tableau: {e}")
            
    def view_history_result(self, index):
        """Voir un résultat de l'historique"""
        try:
            result = self.test_results[index]
            
            # Afficher dans l'onglet résultats
            self.tab_widget.setCurrentIndex(0)
            
            # Mettre à jour les informations
            info_text = f"""
Date: {result['date']}
Provider: {result['provider']}
Modèle: {result['model']}
Température: {result['temperature']}
Max Tokens: {result['max_tokens']}
Succès: {'Oui' if result['success'] else 'Non'}
"""
            if not result['success']:
                info_text += f"Erreur: {result['error']}"
                
            self.test_info_label.setText(info_text)
            
            # Afficher le contenu
            self.result_text.setPlainText(result['content'])
            
            # Parser le JSON si possible
            try:
                if result['content'].strip():
                    cleaned_content = result['content'].strip()
                    if cleaned_content.startswith('```json'):
                        cleaned_content = cleaned_content[7:]
                    if cleaned_content.endswith('```'):
                        cleaned_content = cleaned_content[:-3]
                        
                    parsed_json = json.loads(cleaned_content)
                    formatted_json = json.dumps(parsed_json, indent=2, ensure_ascii=False)
                    self.json_text.setPlainText(formatted_json)
                else:
                    self.json_text.setPlainText("Aucun contenu à parser")
            except:
                self.json_text.setPlainText("Impossible de parser le JSON")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'affichage du résultat: {e}")
            
    def clear_history(self):
        """Effacer l'historique"""
        reply = QMessageBox.question(
            self, "Confirmation", "Voulez-vous vraiment effacer tout l'historique ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.test_results.clear()
            self.update_history_table()
            self.statusBar().showMessage("Historique effacé")
            
    def export_history(self):
        """Exporter l'historique"""
        try:
            filename, _ = QFileDialog.getSaveFileName(
                self, "Exporter l'historique", "", "Fichiers JSON (*.json)"
            )
            if filename:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(self.test_results, f, indent=2, ensure_ascii=False)
                self.statusBar().showMessage(f"Historique exporté dans {filename}")
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de l'export: {e}")
            
    def refresh_config(self):
        """Actualiser la configuration"""
        try:
            config_info = {
                "provider_actuel": config.get_current_llm_provider(),
                "clés_configurées": {}
            }
            
            providers = ["ollama", "openrouter", "openai", "anthropic"]
            for provider in providers:
                if provider != "ollama":
                    api_key = config.get_llm_api_key(provider)
                    config_info["clés_configurées"][provider] = "Configurée" if api_key else "Non configurée"
                else:
                    config_info["clés_configurées"][provider] = "Pas de clé requise"
                    
            config_text = json.dumps(config_info, indent=2, ensure_ascii=False)
            self.current_config_text.setPlainText(config_text)
            
        except Exception as e:
            self.current_config_text.setPlainText(f"Erreur lors du chargement de la configuration: {e}")
            
    def test_configuration(self):
        """Tester la configuration actuelle"""
        try:
            provider = config.get_current_llm_provider()
            api_key = config.get_llm_api_key(provider) if provider != "ollama" else None
            
            test_prompt = "Réponds simplement 'Configuration OK'"
            
            # Lancer un test rapide
            self.worker = LLMTestWorker(
                test_prompt, provider, api_key, "test", 0.1, 100
            )
            self.worker.result_ready.connect(self.on_config_test_completed)
            self.worker.start()
            
            self.statusBar().showMessage("Test de configuration en cours...")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors du test de configuration: {e}")
            
    def on_config_test_completed(self, result):
        """Gestion de la fin du test de configuration"""
        if result.get('success', False):
            QMessageBox.information(self, "Succès", "Configuration testée avec succès !")
        else:
            QMessageBox.warning(self, "Erreur", f"Erreur de configuration: {result.get('error', 'Erreur inconnue')}")
            
        self.statusBar().showMessage("Test de configuration terminé")

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Style de l'application
    app.setStyle('Fusion')
    
    # Création de la fenêtre principale
    window = LLMTestApp()
    window.show()
    
    # Exécution de l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 