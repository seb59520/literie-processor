#!/usr/bin/env python3
"""
Version de test simple de l'interface graphique sans LLM
"""

import sys
import os
import json
from datetime import datetime
from typing import List, Dict

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, 
    QLineEdit, QCheckBox, QComboBox, QGroupBox, QProgressBar, 
    QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont


class SimpleProcessingThread(QThread):
    """Thread simple pour le traitement des fichiers PDF"""
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, files, semaine_prod, annee_prod, commande_client):
        super().__init__()
        self.files = files
        self.semaine_prod = semaine_prod
        self.annee_prod = annee_prod
        self.commande_client = commande_client
    
    def run(self):
        try:
            self.progress_updated.emit(25)
            
            # Simulation simple du traitement
            result = {
                "filename": os.path.basename(self.files[0]) if self.files else "test.pdf",
                "status": "success",
                "extraction_stats": {
                    "nb_caracteres": 1500,
                    "nb_mots": 250,
                    "preview": "Extrait de texte simulé pour le test..."
                },
                "configurations_matelas": [
                    {
                        "matelas_index": 1,
                        "noyau": "LATEX NATUREL",
                        "quantite": 1,
                        "hauteur": 20,
                        "fermete": "MÉDIUM",
                        "housse": "MATELASSÉE",
                        "matiere_housse": "TENCEL",
                        "poignees": "OREILLES",
                        "dimensions": {"largeur": 140, "longueur": 190},
                        "dimension_literie": "140x190"
                    }
                ],
                "donnees_client": {
                    "nom": "Client Test",
                    "adresse": "Adresse Test",
                    "code_client": "TEST001"
                },
                "pre_import": [
                    {
                        "Client_D1": "Client Test",
                        "Adresse_D3": "Adresse Test",
                        "numero_D2": self.commande_client[0] if self.commande_client else "",
                        "semaine_D5": f"{self.semaine_prod}_{self.annee_prod}",
                        "noyau": "LATEX NATUREL",
                        "quantite": 1,
                        "1piece_D11": "140x190"
                    }
                ],
                "calcul_date": {
                    "semaine_annee": f"{self.semaine_prod}_{self.annee_prod}",
                    "lundi": "2025-01-20",
                    "vendredi": "2025-01-24",
                    "commande_client": self.commande_client[0] if self.commande_client else ""
                }
            }
            
            self.progress_updated.emit(100)
            self.result_ready.emit(result)
            
        except Exception as e:
            self.error_occurred.emit(str(e))


class SimpleMatelasApp(QMainWindow):
    """Application simple pour le test de l'interface"""
    
    def __init__(self):
        super().__init__()
        self.selected_files = []
        self.processing_thread = None
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Test Interface - Traitement Devis Matelas")
        self.setGeometry(100, 100, 1200, 800)
        
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
        splitter.setSizes([400, 800])
        
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
        """)
    
    def create_left_panel(self):
        """Crée le panneau de configuration à gauche"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Titre
        title = QLabel("Configuration (Test)")
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
        layout.addWidget(file_group)
        
        # Groupe production
        prod_group = QGroupBox("Paramètres de production")
        prod_layout = QVBoxLayout(prod_group)
        
        # Semaine
        semaine_layout = QHBoxLayout()
        semaine_layout.addWidget(QLabel("Semaine:"))
        self.semaine_spin = QSpinBox()
        self.semaine_spin.setRange(1, 53)
        self.semaine_spin.setValue(datetime.now().isocalendar()[1])
        semaine_layout.addWidget(self.semaine_spin)
        prod_layout.addLayout(semaine_layout)
        
        # Année
        annee_layout = QHBoxLayout()
        annee_layout.addWidget(QLabel("Année:"))
        self.annee_spin = QSpinBox()
        self.annee_spin.setRange(2020, 2030)
        self.annee_spin.setValue(datetime.now().year)
        annee_layout.addWidget(self.annee_spin)
        prod_layout.addLayout(annee_layout)
        
        layout.addWidget(prod_group)
        
        # Groupe commande client
        cmd_group = QGroupBox("Commande client")
        cmd_layout = QVBoxLayout(cmd_group)
        
        self.commande_input = QLineEdit()
        self.commande_input.setPlaceholderText("Nom du client")
        cmd_layout.addWidget(self.commande_input)
        
        layout.addWidget(cmd_group)
        
        # Bouton traitement
        self.process_btn = QPushButton("Tester le traitement")
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        layout.addWidget(self.process_btn)
        
        # Barre de progression
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        # Espace flexible
        layout.addStretch()
        
        return left_widget
    
    def create_right_panel(self):
        """Crée le panneau de résultats à droite"""
        right_widget = QWidget()
        layout = QVBoxLayout(right_widget)
        
        # Titre
        title = QLabel("Résultats (Test)")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Onglets pour les résultats
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Onglet Résumé
        self.summary_tab = QWidget()
        self.summary_layout = QVBoxLayout(self.summary_tab)
        self.summary_text = QTextEdit()
        self.summary_text.setReadOnly(True)
        self.summary_layout.addWidget(self.summary_text)
        self.tabs.addTab(self.summary_tab, "Résumé")
        
        # Onglet Configurations
        self.config_tab = QWidget()
        self.config_layout = QVBoxLayout(self.config_tab)
        self.config_table = QTableWidget()
        self.config_layout.addWidget(self.config_table)
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
        
        return right_widget
    
    def select_files(self):
        """Sélectionne les fichiers PDF"""
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
    
    def clear_files(self):
        """Efface la sélection de fichiers"""
        self.selected_files = []
        self.file_label.setText("Aucun fichier sélectionné")
        self.clear_files_btn.setEnabled(False)
        self.process_btn.setEnabled(False)
    
    def process_files(self):
        """Traite les fichiers sélectionnés"""
        if not self.selected_files:
            QMessageBox.warning(self, "Attention", "Aucun fichier sélectionné")
            return
        
        # Récupération des paramètres
        semaine_prod = self.semaine_spin.value()
        annee_prod = self.annee_spin.value()
        commande_client = [self.commande_input.text()] * len(self.selected_files)
        
        # Désactivation de l'interface
        self.process_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(0)
        
        # Création et lancement du thread de traitement
        self.processing_thread = SimpleProcessingThread(
            self.selected_files, semaine_prod, annee_prod, commande_client
        )
        self.processing_thread.progress_updated.connect(self.progress_bar.setValue)
        self.processing_thread.result_ready.connect(self.display_results)
        self.processing_thread.error_occurred.connect(self.handle_error)
        self.processing_thread.finished.connect(self.on_processing_finished)
        self.processing_thread.start()
    
    def display_results(self, result):
        """Affiche les résultats du traitement"""
        # Onglet Résumé
        summary = f"Fichier: {result.get('filename', 'N/A')}\n"
        summary += f"Statut: {result.get('status', 'N/A')}\n"
        summary += f"Configurations matelas: {len(result.get('configurations_matelas', []))}\n"
        summary += f"Éléments pré-import: {len(result.get('pre_import', []))}\n"
        
        self.summary_text.setText(summary)
        
        # Onglet Configurations
        self.display_configurations(result.get('configurations_matelas', []))
        
        # Onglet Pré-import
        self.display_preimport(result.get('pre_import', []))
        
        # Onglet JSON
        self.json_text.setText(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Sélection de l'onglet résumé
        self.tabs.setCurrentIndex(0)
    
    def display_configurations(self, configurations):
        """Affiche les configurations dans un tableau"""
        if not configurations:
            self.config_table.setRowCount(0)
            self.config_table.setColumnCount(0)
            return
        
        # Headers
        headers = ["Index", "Noyau", "Quantité", "Dimensions", "Housse", "Matière"]
        self.config_table.setColumnCount(len(headers))
        self.config_table.setHorizontalHeaderLabels(headers)
        
        # Données
        self.config_table.setRowCount(len(configurations))
        for i, config in enumerate(configurations):
            self.config_table.setItem(i, 0, QTableWidgetItem(str(config.get('matelas_index', ''))))
            self.config_table.setItem(i, 1, QTableWidgetItem(config.get('noyau', '')))
            self.config_table.setItem(i, 2, QTableWidgetItem(str(config.get('quantite', ''))))
            
            dims = config.get('dimensions', {})
            dim_str = f"{dims.get('largeur', '')}x{dims.get('longueur', '')}" if dims else ""
            self.config_table.setItem(i, 3, QTableWidgetItem(dim_str))
            
            self.config_table.setItem(i, 4, QTableWidgetItem(config.get('housse', '')))
            self.config_table.setItem(i, 5, QTableWidgetItem(config.get('matiere_housse', '')))
        
        self.config_table.resizeColumnsToContents()
    
    def display_preimport(self, preimport_data):
        """Affiche les données de pré-import dans un tableau"""
        if not preimport_data:
            self.preimport_table.setRowCount(0)
            self.preimport_table.setColumnCount(0)
            return
        
        # Headers (premiers champs importants)
        headers = ["Client", "Commande", "Semaine", "Noyau", "Quantité", "Dimensions"]
        self.preimport_table.setColumnCount(len(headers))
        self.preimport_table.setHorizontalHeaderLabels(headers)
        
        # Données
        self.preimport_table.setRowCount(len(preimport_data))
        for i, item in enumerate(preimport_data):
            self.preimport_table.setItem(i, 0, QTableWidgetItem(item.get('Client_D1', '')))
            self.preimport_table.setItem(i, 1, QTableWidgetItem(item.get('numero_D2', '')))
            self.preimport_table.setItem(i, 2, QTableWidgetItem(item.get('semaine_D5', '')))
            self.preimport_table.setItem(i, 3, QTableWidgetItem(item.get('noyau', '')))
            self.preimport_table.setItem(i, 4, QTableWidgetItem(str(item.get('quantite', ''))))
            self.preimport_table.setItem(i, 5, QTableWidgetItem(item.get('1piece_D11', '')))
        
        self.preimport_table.resizeColumnsToContents()
    
    def handle_error(self, error_msg):
        """Gère les erreurs de traitement"""
        QMessageBox.critical(self, "Erreur", f"Erreur lors du traitement:\n{error_msg}")
    
    def on_processing_finished(self):
        """Appelé quand le traitement est terminé"""
        self.process_btn.setEnabled(True)
        self.progress_bar.setVisible(False)
        self.progress_bar.setValue(0)


def main():
    """Point d'entrée de l'application"""
    app = QApplication(sys.argv)
    
    # Style global
    app.setStyle('Fusion')
    
    # Création et affichage de la fenêtre principale
    window = SimpleMatelasApp()
    window.show()
    
    # Lancement de l'application
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 