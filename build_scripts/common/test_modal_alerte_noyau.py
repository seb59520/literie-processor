#!/usr/bin/env python3
"""
Script de test pour afficher le modal d'alerte d'absence de noyau
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QGroupBox, QTableWidget, QTableWidgetItem, QComboBox, QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor

def create_noyau_alert_dialog():
    """Crée et affiche le dialog d'alerte de noyaux non détectés"""
    
    # Données de test pour simuler des alertes de noyaux
    test_alerts = {
        "Commande_Client_Test.pdf": [
            {
                'index': 1,
                'description': 'MATELAS 140x190 LATEX NATUREL CONFORT',
                'noyau': 'INCONNU',
                'quantite': 2,
                'dimensions': '140x190'
            },
            {
                'index': 3,
                'description': 'MATELAS 160x200 MOUSSE RAINUREE 7 ZONES',
                'noyau': 'INCONNU',
                'quantite': 1,
                'dimensions': '160x200'
            }
        ],
        "Devis_Entreprise_Test.pdf": [
            {
                'index': 2,
                'description': 'MATELAS 180x200 LATEX MIXTE CONFORT',
                'noyau': 'INCONNU',
                'quantite': 3,
                'dimensions': '180x200'
            }
        ]
    }
    
    # Créer le dialog
    dialog = NoyauAlertDialog(test_alerts)
    return dialog

class NoyauAlertDialog(QDialog):
    """Dialog pour gérer les alertes de noyaux non détectés"""
    
    def __init__(self, noyau_alerts, parent=None):
        super().__init__(parent)
        self.noyau_alerts = noyau_alerts
        self.corrections = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Alertes - Noyaux Non Détectés")
        self.setModal(True)
        self.resize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("⚠️ Noyaux Non Détectés")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #e74c3c; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("Certains noyaux de matelas n'ont pas pu être détectés automatiquement. "
                           "Veuillez sélectionner le type de noyau approprié pour chaque matelas :")
        description.setWordWrap(True)
        description.setStyleSheet("color: #34495e; margin: 5px; padding: 10px; background-color: #f8f9fa; border-radius: 5px;")
        layout.addWidget(description)
        
        # Scroll area pour les alertes
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Créer un groupe pour chaque fichier avec alertes
        for filename, alerts in self.noyau_alerts.items():
            if alerts:  # Seulement si il y a des alertes
                group = self.create_file_group(filename, alerts)
                scroll_layout.addWidget(group)
        
        # Espaceur en bas
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Boutons d'action
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Bouton Appliquer toutes les corrections
        apply_all_btn = QPushButton("✅ Appliquer toutes les corrections")
        apply_all_btn.clicked.connect(self.apply_all_corrections)
        apply_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(apply_all_btn)
        
        # Espace entre les boutons
        button_layout.addSpacing(10)
        
        # Bouton Annuler
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def create_file_group(self, filename, alerts):
        """Crée un groupe pour un fichier avec ses alertes"""
        group = QGroupBox(f"📄 {os.path.basename(filename)}")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e74c3c;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #fdf2f2;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #e74c3c;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Créer un tableau pour les alertes
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Index", "Description", "Noyau Détecté", "Correction"])
        table.setRowCount(len(alerts))
        
        # Types de noyaux disponibles
        types_noyau = [
            "LATEX NATUREL",
            "LATEX MIXTE 7 ZONES", 
            "MOUSSE RAINUREE 7 ZONES",
            "LATEX RENFORCE",
            "SELECT 43",
            "MOUSSE VISCO"
        ]
        
        for i, alert in enumerate(alerts):
            # Index
            index_item = QTableWidgetItem(str(alert['index']))
            index_item.setFlags(index_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            table.setItem(i, 0, index_item)
            
            # Description (tronquée)
            description = alert['description']
            if len(description) > 80:
                description = description[:77] + "..."
            desc_item = QTableWidgetItem(description)
            desc_item.setFlags(desc_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            desc_item.setToolTip(alert['description'])
            table.setItem(i, 1, desc_item)
            
            # Noyau détecté (INCONNU)
            noyau_item = QTableWidgetItem(alert['noyau'])
            noyau_item.setFlags(noyau_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            noyau_item.setBackground(QColor(255, 200, 200))  # Rouge clair
            table.setItem(i, 2, noyau_item)
            
            # Combo box pour la correction
            combo = QComboBox()
            combo.addItem("-- Sélectionner un noyau --")
            combo.addItems(types_noyau)
            combo.currentTextChanged.connect(lambda text, f=filename, idx=alert['index']: self.on_correction_changed(f, idx, text))
            table.setCellWidget(i, 3, combo)
            
            # Stocker la référence pour accès ultérieur
            alert['combo'] = combo
        
        # Ajuster la taille des colonnes
        table.resizeColumnsToContents()
        table.setMaximumHeight(300)
        
        layout.addWidget(table)
        
        # Bouton pour appliquer les corrections de ce fichier
        apply_file_btn = QPushButton(f"Appliquer les corrections pour {os.path.basename(filename)}")
        apply_file_btn.clicked.connect(lambda: self.apply_file_corrections(filename, alerts))
        apply_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(apply_file_btn)
        
        return group
    
    def on_correction_changed(self, filename, index, text):
        """Gère le changement de correction"""
        if text != "-- Sélectionner un noyau --":
            if filename not in self.corrections:
                self.corrections[filename] = {}
            self.corrections[filename][index] = text
    
    def apply_file_corrections(self, filename, alerts):
        """Applique les corrections pour un fichier spécifique"""
        corrections_count = 0
        for alert in alerts:
            combo = alert.get('combo')
            if combo and combo.currentText() != "-- Sélectionner un noyau --":
                corrections_count += 1
        
        if corrections_count > 0:
            print(f"✅ {corrections_count} correction(s) appliquée(s) pour {os.path.basename(filename)}")
        else:
            print(f"⚠️ Aucune correction sélectionnée pour {os.path.basename(filename)}")
    
    def apply_all_corrections(self):
        """Applique toutes les corrections"""
        total_corrections = 0
        for filename, alerts in self.noyau_alerts.items():
            for alert in alerts:
                combo = alert.get('combo')
                if combo and combo.currentText() != "-- Sélectionner un noyau --":
                    total_corrections += 1
        
        if total_corrections > 0:
            print(f"✅ {total_corrections} correction(s) appliquée(s) au total")
            self.accept()
        else:
            print("⚠️ Aucune correction sélectionnée")
    
    def get_corrections(self):
        """Récupère toutes les corrections"""
        return self.corrections

def test_modal_alerte_noyau():
    """Test du modal d'alerte de noyaux non détectés"""
    print("🧪 Test du modal d'alerte d'absence de noyau")
    
    app = QApplication(sys.argv)
    
    try:
        # Créer et afficher le dialog
        dialog = create_noyau_alert_dialog()
        
        print("✅ Modal d'alerte créé avec succès")
        print("📋 Instructions de test :")
        print("   1. Le modal affiche les noyaux non détectés par fichier")
        print("   2. Chaque fichier a son propre groupe avec tableau")
        print("   3. Les colonnes sont : Index, Description, Noyau Détecté, Correction")
        print("   4. La colonne 'Noyau Détecté' affiche 'INCONNU' en rouge")
        print("   5. La colonne 'Correction' propose une liste déroulante")
        print("   6. Vous pouvez sélectionner un noyau pour chaque matelas")
        print("   7. Boutons : Appliquer par fichier ou Appliquer tout")
        print("   8. Le modal est modal (bloque l'interface principale)")
        
        print("\n🎯 Test en cours...")
        print("   - Vérifiez l'apparence du modal")
        print("   - Testez les listes déroulantes")
        print("   - Essayez les boutons d'action")
        print("   - Vérifiez que le modal est bien modal")
        
        # Timer pour fermer automatiquement après 60 secondes
        timer = QTimer()
        timer.timeout.connect(dialog.accept)
        timer.start(60000)  # 60 secondes
        
        print("\n⏰ Le modal se fermera automatiquement dans 60 secondes")
        
        result = dialog.exec()
        
        if result == QDialog.DialogCode.Accepted:
            corrections = dialog.get_corrections()
            print(f"✅ Corrections appliquées : {corrections}")
        else:
            print("❌ Modal fermé sans appliquer de corrections")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erreur lors du test du modal : {e}")
        return 1

if __name__ == "__main__":
    sys.exit(test_modal_alerte_noyau()) 