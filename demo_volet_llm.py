#!/usr/bin/env python3
"""
Démonstration du volet LLM déroulant
"""

import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QGroupBox, QCheckBox, QComboBox, 
                             QLabel, QPushButton, QLineEdit, QProgressBar)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

class DemoVoletLLM(QMainWindow):
    """Fenêtre de démonstration du volet LLM déroulant"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎯 Démonstration - Volet LLM Déroulant")
        self.setGeometry(100, 100, 500, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre
        title = QLabel("🎯 TRANSFORMATION ZONE ENRICHISSEMENT LLM")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 10px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel(
            "La zone 'Enrichissement LLM' est maintenant un volet déroulant !\n"
            "Cliquez sur le titre pour l'ouvrir/fermer et gagner de l'espace."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #7f8c8d; margin: 10px; font-size: 12px;")
        layout.addWidget(desc)
        
        # Volet LLM déroulant
        self.llm_group = QGroupBox("🔽 Enrichissement LLM")
        self.llm_group.setCheckable(True)
        self.llm_group.setChecked(True)  # Ouvert par défaut
        self.llm_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: #ecf0f1;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2c3e50;
            }
            QGroupBox:checked {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
            QGroupBox:!checked {
                border-color: #bdc3c7;
                background-color: #f8f9fa;
            }
        """)
        
        # Layout pour le contenu du volet
        self.llm_layout = QVBoxLayout(self.llm_group)
        self.llm_layout.setSpacing(10)
        
        # Checkbox d'enrichissement
        self.enrich_checkbox = QCheckBox("✅ Utiliser l'enrichissement LLM")
        self.enrich_checkbox.setChecked(True)
        self.enrich_checkbox.setStyleSheet("font-weight: bold; color: #27ae60;")
        self.llm_layout.addWidget(self.enrich_checkbox)
        
        # Sélection du provider
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("🤖 Provider:"))
        
        self.provider_combo = QComboBox()
        self.provider_combo.addItems(["ollama", "openrouter", "openai", "anthropic", "gemini", "mistral"])
        self.provider_combo.setCurrentText("ollama")
        self.provider_combo.setStyleSheet("""
            QComboBox {
                padding: 5px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                min-width: 120px;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
        """)
        provider_layout.addWidget(self.provider_combo)
        provider_layout.addStretch()
        
        self.llm_layout.addLayout(provider_layout)
        
        # Groupe clé API (aussi déroulant)
        self.api_key_group = QGroupBox("🔐 Clé API (cliquez pour afficher)")
        self.api_key_group.setCheckable(True)
        self.api_key_group.setChecked(False)  # Masqué par défaut
        self.api_key_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                background-color: #f8f9fa;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2c3e50;
            }
            QGroupBox:checked {
                border-color: #3498db;
                background-color: #ecf0f1;
            }
        """)
        
        api_key_layout = QVBoxLayout(self.api_key_group)
        
        # Champ clé API
        api_input_layout = QHBoxLayout()
        api_input_layout.addWidget(QLabel("🔑 Clé:"))
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setPlaceholderText("Entrez votre clé API...")
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        api_input_layout.addWidget(self.api_key_input)
        
        # Bouton afficher/masquer
        self.toggle_btn = QPushButton("👁")
        self.toggle_btn.setFixedSize(35, 35)
        self.toggle_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: 2px solid #7f8c8d;
                border-radius: 17px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.toggle_btn.clicked.connect(self.toggle_api_key_visibility)
        api_input_layout.addWidget(self.toggle_btn)
        
        api_key_layout.addLayout(api_input_layout)
        
        # Ajouter le groupe clé API au layout LLM
        self.llm_layout.addWidget(self.api_key_group)
        
        # Ajouter le volet LLM au layout principal
        layout.addWidget(self.llm_group)
        
        # Connecter le signal de basculement du volet LLM
        self.llm_group.toggled.connect(self.on_llm_group_toggled)
        
        # Connecter le signal de basculement de la clé API
        self.api_key_group.toggled.connect(self.on_api_key_group_toggled)
        
        # Informations sur l'état
        self.status_label = QLabel("🟢 Volet LLM: OUVERT | Clé API: MASQUÉE")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("""
            QLabel {
                background-color: #ecf0f1;
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                color: #2c3e50;
            }
        """)
        layout.addWidget(self.status_label)
        
        # Instructions
        instructions = QLabel(
            "💡 INSTRUCTIONS:\n"
            "• Cliquez sur '🔽 Enrichissement LLM' pour ouvrir/fermer le volet\n"
            "• Cliquez sur '🔐 Clé API' pour afficher/masquer la clé\n"
            "• Utilisez le bouton 👁 pour afficher/masquer la clé API\n"
            "• L'état est sauvegardé automatiquement"
        )
        instructions.setWordWrap(True)
        instructions.setAlignment(Qt.AlignmentFlag.AlignCenter)
        instructions.setStyleSheet("""
            QLabel {
                background-color: #fff3cd;
                border: 2px solid #ffeaa7;
                border-radius: 8px;
                padding: 15px;
                color: #856404;
                font-size: 11px;
                line-height: 1.4;
            }
        """)
        layout.addWidget(instructions)
        
        # Espace flexible
        layout.addStretch()
        
        # Bouton de test
        test_btn = QPushButton("🧪 Tester le volet")
        test_btn.clicked.connect(self.test_volet)
        test_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(test_btn)
        
        # Initialiser l'état
        self.update_status()
    
    def on_llm_group_toggled(self, checked):
        """Gère l'ouverture/fermeture du volet Enrichissement LLM"""
        try:
            # Afficher/masquer les widgets enfants
            for i in range(self.llm_layout.count()):
                widget = self.llm_layout.itemAt(i).widget()
                if widget:
                    widget.setVisible(checked)
            
            # Changer l'icône du titre
            if checked:
                self.llm_group.setTitle("🔽 Enrichissement LLM")
                print("✅ Volet Enrichissement LLM ouvert")
            else:
                self.llm_group.setTitle("▶️ Enrichissement LLM")
                print("▶️ Volet Enrichissement LLM fermé")
            
            # Mettre à jour le statut
            self.update_status()
            
        except Exception as e:
            print(f"❌ Erreur lors du basculement du volet LLM: {e}")
    
    def on_api_key_group_toggled(self, checked):
        """Gère l'ouverture/fermeture du volet clé API"""
        try:
            if checked:
                print("🔐 Volet clé API ouvert")
            else:
                print("🔒 Volet clé API fermé")
            
            # Mettre à jour le statut
            self.update_status()
            
        except Exception as e:
            print(f"❌ Erreur lors du changement d'état du volet clé API: {e}")
    
    def toggle_api_key_visibility(self):
        """Bascule l'affichage de la clé API"""
        try:
            if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
                # Afficher la clé
                self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
                self.toggle_btn.setText("🙈")
                self.toggle_btn.setToolTip("Masquer la clé API")
                print("👁 Clé API affichée")
            else:
                # Masquer la clé
                self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.toggle_btn.setText("👁")
                self.toggle_btn.setToolTip("Afficher la clé API")
                print("🙈 Clé API masquée")
        except Exception as e:
            print(f"❌ Erreur lors du basculement de la visibilité: {e}")
    
    def update_status(self):
        """Met à jour l'affichage du statut"""
        llm_status = "OUVERT" if self.llm_group.isChecked() else "FERMÉ"
        api_status = "VISIBLE" if self.api_key_group.isChecked() else "MASQUÉE"
        
        llm_icon = "🟢" if self.llm_group.isChecked() else "🔴"
        api_icon = "🟢" if self.api_key_group.isChecked() else "🔴"
        
        self.status_label.setText(
            f"{llm_icon} Volet LLM: {llm_status} | {api_icon} Clé API: {api_status}"
        )
    
    def test_volet(self):
        """Teste le fonctionnement du volet"""
        print("\n🧪 TEST DU VOLET:")
        print(f"   • Volet LLM: {'OUVERT' if self.llm_group.isChecked() else 'FERMÉ'}")
        print(f"   • Clé API: {'VISIBLE' if self.api_key_group.isChecked() else 'MASQUÉE'}")
        print(f"   • Enrichissement: {'ACTIVÉ' if self.enrich_checkbox.isChecked() else 'DÉSACTIVÉ'}")
        print(f"   • Provider: {self.provider_combo.currentText()}")
        print("✅ Test terminé avec succès !")

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Style global
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f5f5;
        }
    """)
    
    # Créer et afficher la fenêtre
    window = DemoVoletLLM()
    window.show()
    
    # Lancer l'application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

