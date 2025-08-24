#!/usr/bin/env python3
"""
Script de test pour vérifier l'uniformisation des modals semaine et noyau
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QGroupBox, QTableWidget, QTableWidgetItem, QComboBox, QFrame, QSpinBox
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

def test_uniformisation_modals():
    """Test de l'uniformisation des modals semaine et noyau"""
    print("🧪 Test de l'uniformisation des modals")
    
    app = QApplication(sys.argv)
    
    # Données de test pour le modal de semaine
    test_week_data = {
        "Commande_Test_Semaine.pdf": {
            'has_matelas': True,
            'has_sommiers': False,
            'matelas_count': 2,
            'sommier_count': 0,
            'semaine_matelas': 32,
            'annee_matelas': 2025,
            'semaine_sommiers': 31,
            'annee_sommiers': 2025,
            'recommendation': 'Production matelas en S32 (semaine suivante)'
        }
    }
    
    # Données de test pour le modal de noyau
    test_noyau_data = {
        "Commande_Test_Noyau.pdf": [
            {
                'index': 1,
                'description': 'MATELAS 140x190 LATEX NATUREL CONFORT',
                'noyau': 'INCONNU',
                'quantite': 2,
                'dimensions': '140x190'
            },
            {
                'index': 2,
                'description': 'MATELAS 160x200 MOUSSE MEMORY FOAM',
                'noyau': 'INCONNU',
                'quantite': 1,
                'dimensions': '160x200'
            }
        ]
    }
    
    # Créer et afficher le modal de semaine
    print("📅 Affichage du modal de recommandations de semaine...")
    week_dialog = ProductionRecommendationDialog(test_week_data)
    week_dialog.show()
    
    # Timer pour fermer le modal de semaine après 5 secondes
    def show_noyau_modal():
        week_dialog.close()
        print("⚠️ Affichage du modal d'alertes de noyau...")
        noyau_dialog = NoyauAlertDialog(test_noyau_data)
        noyau_dialog.show()
        
        # Timer pour fermer le modal de noyau après 5 secondes
        def close_noyau_modal():
            noyau_dialog.close()
            print("✅ Test terminé - Vérifiez que les deux modals ont la même organisation de boutons")
            app.quit()
        
        QTimer.singleShot(5000, close_noyau_modal)
    
    QTimer.singleShot(5000, show_noyau_modal)
    
    print("📋 Instructions de test :")
    print("   1. Le modal de semaine s'affiche d'abord (5 secondes)")
    print("   2. Vérifiez l'ordre des boutons : Appliquer → Continuer → Annuler")
    print("   3. Le modal de noyau s'affiche ensuite (5 secondes)")
    print("   4. Vérifiez que l'ordre des boutons est identique")
    print("   5. Le bouton '🚀 Continuer le traitement' doit être bien visible et centré")
    
    return app.exec()

# Classes de test simplifiées
class ProductionRecommendationDialog(QDialog):
    """Dialog simplifié pour tester les recommandations de production"""
    
    def __init__(self, file_analysis_results, parent=None):
        super().__init__(parent)
        self.file_analysis_results = file_analysis_results
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Test - Recommandations de Production")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("📅 Recommandations de Production")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2980b9; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        explanation = QLabel("Le système a analysé vos fichiers et propose les recommandations de production suivantes :")
        explanation.setWordWrap(True)
        explanation.setStyleSheet("""
            color: #2c3e50; 
            margin: 10px; 
            padding: 10px; 
            background-color: #ecf0f1; 
            border-radius: 5px; 
            border-left: 4px solid #3498db;
        """)
        layout.addWidget(explanation)
        
        # Scroll area pour les fichiers
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Créer un groupe pour chaque fichier
        for i, (filename, analysis) in enumerate(self.file_analysis_results.items()):
            group = self.create_file_group(filename, analysis, i)
            scroll_layout.addWidget(group)
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Boutons - Organisation uniformisée avec le modal de noyau
        button_layout = QHBoxLayout()
        
        # Bouton Appliquer toutes les recommandations
        apply_all_btn = QPushButton("✅ Appliquer toutes les recommandations")
        apply_all_btn.setToolTip("Applique les recommandations optimales de production à tous les fichiers en une seule action")
        apply_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(apply_all_btn)
        
        # Espace flexible pour centrer les boutons
        button_layout.addStretch()
        
        # Bouton Continuer le traitement (PRINCIPAL)
        continue_btn = QPushButton("🚀 Continuer le traitement")
        continue_btn.setToolTip("Valide les recommandations et continue le traitement des fichiers")
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        button_layout.addWidget(continue_btn)
        
        # Espace entre les boutons
        button_layout.addSpacing(10)
        
        # Bouton Annuler
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setToolTip("Annule les recommandations et arrête le traitement")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def create_file_group(self, filename, analysis, index):
        """Crée un groupe pour un fichier"""
        group = QGroupBox(f"Fichier {index + 1}: {os.path.basename(filename)}")
        group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(group)
        
        # Contenu détecté
        content_layout = QHBoxLayout()
        
        # Matelas
        matelas_label = QLabel("Matelas:")
        matelas_label.setStyleSheet("font-weight: bold; color: #2980b9;")
        content_layout.addWidget(matelas_label)
        
        matelas_count = QLabel(f"{analysis.get('matelas_count', 0)} article(s)")
        matelas_count.setStyleSheet("color: #27ae60;")
        content_layout.addWidget(matelas_count)
        
        content_layout.addSpacing(20)
        
        # Sommiers
        sommier_label = QLabel("Sommiers:")
        sommier_label.setStyleSheet("font-weight: bold; color: #e67e22;")
        content_layout.addWidget(sommier_label)
        
        sommier_count = QLabel(f"{analysis.get('sommier_count', 0)} article(s)")
        sommier_count.setStyleSheet("color: #27ae60;")
        content_layout.addWidget(sommier_count)
        
        content_layout.addStretch()
        layout.addLayout(content_layout)
        
        # Recommandation
        recommendation = analysis.get('recommendation', 'Aucune recommandation')
        recommendation_label = QLabel(f"Recommandation: {recommendation}")
        recommendation_label.setStyleSheet("color: #8e44ad; font-weight: bold; padding: 5px; background-color: #f8f9fa; border-radius: 3px;")
        recommendation_label.setWordWrap(True)
        layout.addWidget(recommendation_label)
        
        return group

class NoyauAlertDialog(QDialog):
    """Dialog simplifié pour tester les alertes de noyau"""
    
    def __init__(self, noyau_alerts, parent=None):
        super().__init__(parent)
        self.noyau_alerts = noyau_alerts
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Test - Alertes de Noyaux")
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
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Boutons - Organisation uniformisée avec le modal de semaine
        button_layout = QHBoxLayout()
        
        # Bouton Appliquer toutes les corrections
        apply_all_btn = QPushButton("✅ Appliquer toutes les corrections")
        apply_all_btn.setToolTip("Applique les corrections sélectionnées à tous les matelas")
        apply_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 200px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        button_layout.addWidget(apply_all_btn)
        
        # Espace flexible pour centrer les boutons
        button_layout.addStretch()
        
        # Bouton Continuer le traitement (PRINCIPAL)
        continue_btn = QPushButton("🚀 Continuer le traitement")
        continue_btn.setToolTip("Valide les corrections et continue le traitement")
        continue_btn.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 12px 25px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
                min-width: 180px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        button_layout.addWidget(continue_btn)
        
        # Espace entre les boutons
        button_layout.addSpacing(10)
        
        # Bouton Annuler
        cancel_btn = QPushButton("❌ Annuler")
        cancel_btn.setToolTip("Annule les corrections et arrête le traitement")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                min-width: 120px;
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
            table.setCellWidget(i, 3, combo)
        
        # Ajuster la taille des colonnes
        table.resizeColumnsToContents()
        table.setMaximumHeight(300)
        
        layout.addWidget(table)
        
        return group

if __name__ == "__main__":
    test_uniformisation_modals() 