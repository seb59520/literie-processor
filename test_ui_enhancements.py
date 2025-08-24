#!/usr/bin/env python3
"""
Script de test pour les améliorations de l'interface utilisateur
"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt6.QtCore import Qt

# Ajouter le chemin pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui_enhancements import SmartFileSelector, EnhancedStatusBar, MatelasAppEnhancements
from enhanced_processing_ui import OptimizedProcessingDialog, create_processing_steps_for_files
from ui_optimizations import SmartProgressBar, AnimationManager

class TestMainWindow(QMainWindow):
    """Fenêtre de test pour les améliorations UI"""
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        """Configure l'interface de test"""
        self.setWindowTitle("Test des améliorations UI - Application Matelas")
        self.setGeometry(100, 100, 1000, 700)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title_widget = QWidget()
        title_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 8px;
                margin: 5px;
            }
        """)
        title_layout = QVBoxLayout(title_widget)
        
        from PyQt6.QtWidgets import QLabel
        title_label = QLabel("🧪 Test des Améliorations Interface")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                background: transparent;
                border: none;
                margin: 0px;
            }
        """)
        title_layout.addWidget(title_label)
        layout.addWidget(title_widget)
        
        # Sélecteur de fichiers intelligent
        file_selector_group = QWidget()
        file_selector_group.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }
        """)
        file_selector_layout = QVBoxLayout(file_selector_group)
        
        selector_title = QLabel("📁 Sélecteur de Fichiers Intelligent")
        selector_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        file_selector_layout.addWidget(selector_title)
        
        self.file_selector = SmartFileSelector()
        self.file_selector.files_selected.connect(self.on_files_selected)
        file_selector_layout.addWidget(self.file_selector)
        
        layout.addWidget(file_selector_group)
        
        # Boutons de test
        buttons_group = QWidget()
        buttons_layout = QVBoxLayout(buttons_group)
        
        buttons_title = QLabel("🚀 Tests de Fonctionnalités")
        buttons_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        buttons_layout.addWidget(buttons_title)
        
        # Bouton test progression
        self.test_progress_button = QPushButton("📊 Tester Barre de Progression Intelligente")
        self.test_progress_button.clicked.connect(self.test_smart_progress)
        self.test_progress_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        buttons_layout.addWidget(self.test_progress_button)
        
        # Bouton test dialogue de traitement
        self.test_dialog_button = QPushButton("💬 Tester Dialogue de Traitement Optimisé")
        self.test_dialog_button.clicked.connect(self.test_processing_dialog)
        self.test_dialog_button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
        """)
        buttons_layout.addWidget(self.test_dialog_button)
        
        # Bouton test animations
        self.test_animations_button = QPushButton("✨ Tester Animations")
        self.test_animations_button.clicked.connect(self.test_animations)
        self.test_animations_button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        """)
        buttons_layout.addWidget(self.test_animations_button)
        
        layout.addWidget(buttons_group)
        
        # Zone d'informations
        info_group = QWidget()
        info_group.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                margin: 5px;
                padding: 10px;
            }
        """)
        info_layout = QVBoxLayout(info_group)
        
        info_title = QLabel("ℹ️ Informations")
        info_title.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 5px;")
        info_layout.addWidget(info_title)
        
        self.info_text = QLabel("Sélectionnez des fichiers et testez les fonctionnalités...")
        self.info_text.setStyleSheet("color: #6c757d; font-size: 12px;")
        self.info_text.setWordWrap(True)
        info_layout.addWidget(self.info_text)
        
        layout.addWidget(info_group)
        
        # Barre de statut améliorée
        enhanced_status_bar = EnhancedStatusBar()
        self.setStatusBar(enhanced_status_bar)
        
        # Variables
        self.selected_files = []
        self.animation_manager = AnimationManager()
        
        # Message de bienvenue
        self.statusBar().showMessage("Interface de test chargée - Prêt pour les tests !")
    
    def on_files_selected(self, files):
        """Gestionnaire de sélection de fichiers"""
        self.selected_files = files
        count = len(files)
        
        if count == 0:
            self.info_text.setText("Aucun fichier sélectionné")
            self.test_dialog_button.setEnabled(False)
        else:
            file_list = "\\n".join([f"• {os.path.basename(f)}" for f in files[:5]])
            if count > 5:
                file_list += f"\\n... et {count - 5} autres fichiers"
            
            self.info_text.setText(
                f"Fichiers sélectionnés ({count}):\\n{file_list}"
            )
            self.test_dialog_button.setEnabled(True)
        
        self.statusBar().showMessage(f"{count} fichier(s) sélectionné(s)")
    
    def test_smart_progress(self):
        """Test de la barre de progression intelligente"""
        # Créer une fenêtre de test pour la progression
        from PyQt6.QtWidgets import QDialog, QVBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Test Barre de Progression Intelligente")
        dialog.setModal(True)
        dialog.resize(500, 200)
        
        layout = QVBoxLayout(dialog)
        
        # Ajouter une barre de progression intelligente
        progress_bar = SmartProgressBar()
        layout.addWidget(progress_bar)
        
        # Boutons de contrôle
        from PyQt6.QtWidgets import QHBoxLayout
        controls_layout = QHBoxLayout()
        
        start_button = QPushButton("Démarrer")
        start_button.clicked.connect(lambda: self._simulate_progress(progress_bar))
        controls_layout.addWidget(start_button)
        
        close_button = QPushButton("Fermer")
        close_button.clicked.connect(dialog.accept)
        controls_layout.addWidget(close_button)
        
        layout.addLayout(controls_layout)
        
        dialog.exec()
    
    def _simulate_progress(self, progress_bar):
        """Simule une progression"""
        from PyQt6.QtCore import QTimer
        
        progress_bar.start_progress(100)
        
        self.progress_timer = QTimer()
        self.progress_value = 0
        
        def update_progress():
            self.progress_value += 2
            progress_bar.update_progress(self.progress_value)
            
            if self.progress_value >= 100:
                self.progress_timer.stop()
        
        self.progress_timer.timeout.connect(update_progress)
        self.progress_timer.start(100)  # Mise à jour toutes les 100ms
    
    def test_processing_dialog(self):
        """Test du dialogue de traitement optimisé"""
        if not self.selected_files:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                self, 
                "Aucun fichier", 
                "Veuillez d'abord sélectionner des fichiers PDF pour tester le dialogue de traitement."
            )
            return
        
        # Créer et afficher le dialogue optimisé
        dialog = OptimizedProcessingDialog(self.selected_files, self)
        
        # Animation d'apparition
        fade_in = self.animation_manager.fade_in(dialog)
        fade_in.start()
        
        # Démarrer le traitement simulé
        dialog.start_processing()
        
        result = dialog.exec()
        
        if result:
            self.statusBar().showMessage("Test de traitement terminé avec succès!")
        else:
            self.statusBar().showMessage("Test de traitement annulé")
    
    def test_animations(self):
        """Test des animations"""
        # Animer le titre
        title_widget = self.centralWidget().layout().itemAt(0).widget()
        
        # Animation de pulsation
        pulse_animation = self.animation_manager.scale_in(title_widget, duration=500)
        pulse_animation.start()
        
        self.statusBar().showMessage("Animation de test lancée!")
        
        # Programmer une autre animation après un délai
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1000, lambda: self._animate_buttons())
    
    def _animate_buttons(self):
        """Anime les boutons un par un"""
        buttons_widget = self.centralWidget().layout().itemAt(2).widget()
        buttons_layout = buttons_widget.layout()
        
        for i in range(1, buttons_layout.count()):  # Ignorer le titre
            widget = buttons_layout.itemAt(i).widget()
            if widget:
                # Animer avec un délai progressif
                from PyQt6.QtCore import QTimer
                QTimer.singleShot(
                    i * 200, 
                    lambda w=widget: self.animation_manager.slide_in(w, 'left').start()
                )

def main():
    """Fonction principale"""
    app = QApplication(sys.argv)
    
    # Configuration de l'application
    app.setApplicationName("Test Améliorations UI Matelas")
    app.setApplicationVersion("1.0.0")
    
    # Style sombre optionnel
    app.setStyleSheet("""
        QMainWindow {
            background-color: #f5f6fa;
        }
        QWidget {
            font-family: 'Segoe UI', Arial, sans-serif;
        }
    """)
    
    # Créer et afficher la fenêtre de test
    window = TestMainWindow()
    window.show()
    
    # Animation d'apparition de la fenêtre
    animation_manager = AnimationManager()
    fade_in = animation_manager.fade_in(window)
    fade_in.start()
    
    print("🧪 Interface de test des améliorations UI lancée")
    print("📁 Sélectionnez des fichiers PDF pour tester les fonctionnalités")
    print("🚀 Utilisez les boutons pour tester les différentes améliorations")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())