"""
Interface de traitement améliorée avec optimisations UX
"""

import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel,
    QPushButton, QTextEdit, QGroupBox, QFrame, QScrollArea,
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView,
    QSplitter, QDialog, QDialogButtonBox, QFormLayout, QSpinBox,
    QCheckBox, QComboBox, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import (
    Qt, QTimer, pyqtSignal, QThread, QPropertyAnimation,
    QParallelAnimationGroup, QSequentialAnimationGroup, QRect
)
from PyQt6.QtGui import QFont, QColor, QPalette, QPixmap, QIcon

logger = logging.getLogger(__name__)

@dataclass
class ProcessingStepInfo:
    """Information sur une étape de traitement"""
    name: str
    description: str
    estimated_duration: float
    status: str = "pending"  # pending, running, completed, error
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    progress: int = 0

class EnhancedProgressWidget(QWidget):
    """Widget de progression amélioré avec détails des étapes"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.steps = []
        self.current_step_index = 0
        self.start_time = None
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du widget de progression"""
        layout = QVBoxLayout(self)
        
        # En-tête avec progression globale
        header_layout = QHBoxLayout()
        
        self.title_label = QLabel("Traitement en cours...")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        header_layout.addWidget(self.title_label)
        
        header_layout.addStretch()
        
        self.eta_label = QLabel("ETA: Calcul...")
        self.eta_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        header_layout.addWidget(self.eta_label)
        
        layout.addLayout(header_layout)
        
        # Barre de progression principale
        self.main_progress = QProgressBar()
        self.main_progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #ecf0f1;
                border-radius: 8px;
                text-align: center;
                font-weight: bold;
                height: 25px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3498db, stop:1 #2980b9);
                border-radius: 6px;
                margin: 1px;
            }
        """)
        layout.addWidget(self.main_progress)
        
        # Liste des étapes
        self.steps_widget = QScrollArea()
        self.steps_container = QWidget()
        self.steps_layout = QVBoxLayout(self.steps_container)
        self.steps_widget.setWidget(self.steps_container)
        self.steps_widget.setMaximumHeight(200)
        self.steps_widget.setStyleSheet("""
            QScrollArea {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
            }
        """)
        layout.addWidget(self.steps_widget)
        
        # Informations détaillées
        self.details_text = QTextEdit()
        self.details_text.setMaximumHeight(100)
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        layout.addWidget(self.details_text)
    
    def set_steps(self, steps: List[ProcessingStepInfo]):
        """Définit les étapes de traitement"""
        self.steps = steps
        self.current_step_index = 0
        self._update_steps_display()
        
        # Calculer la durée totale estimée
        total_duration = sum(step.estimated_duration for step in steps)
        self.eta_label.setText(f"ETA: {self._format_duration(total_duration)}")
    
    def start_processing(self):
        """Démarre le traitement"""
        self.start_time = time.time()
        self.main_progress.setMaximum(len(self.steps))
        self.main_progress.setValue(0)
        self._update_current_step()
    
    def update_step_progress(self, step_index: int, progress: int, message: str = ""):
        """Met à jour la progression d'une étape"""
        if 0 <= step_index < len(self.steps):
            step = self.steps[step_index]
            step.progress = progress
            
            if message:
                self.add_log_message(f"[{step.name}] {message}")
            
            # Mettre à jour l'affichage
            self._update_steps_display()
            self._update_eta()
    
    def complete_step(self, step_index: int):
        """Marque une étape comme terminée"""
        if 0 <= step_index < len(self.steps):
            step = self.steps[step_index]
            step.status = "completed"
            step.end_time = time.time()
            step.progress = 100
            
            self.main_progress.setValue(step_index + 1)
            self._update_steps_display()
            
            # Passer à l'étape suivante
            if step_index + 1 < len(self.steps):
                self.current_step_index = step_index + 1
                self.start_step(self.current_step_index)
    
    def start_step(self, step_index: int):
        """Démarre une étape spécifique"""
        if 0 <= step_index < len(self.steps):
            step = self.steps[step_index]
            step.status = "running"
            step.start_time = time.time()
            step.progress = 0
            
            self.title_label.setText(f"Traitement: {step.name}")
            self.add_log_message(f"🟡 Démarrage: {step.description}")
            self._update_steps_display()
    
    def error_step(self, step_index: int, error_message: str):
        """Marque une étape en erreur"""
        if 0 <= step_index < len(self.steps):
            step = self.steps[step_index]
            step.status = "error"
            step.end_time = time.time()
            
            self.add_log_message(f"🔴 Erreur: {error_message}")
            self._update_steps_display()
    
    def add_log_message(self, message: str):
        """Ajoute un message aux logs"""
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        self.details_text.append(formatted_message)
        
        # Scroll automatique vers le bas
        scrollbar = self.details_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _update_steps_display(self):
        """Met à jour l'affichage des étapes"""
        # Nettoyer l'ancien affichage
        for i in reversed(range(self.steps_layout.count())):
            self.steps_layout.itemAt(i).widget().setParent(None)
        
        # Ajouter les étapes
        for i, step in enumerate(self.steps):
            step_widget = self._create_step_widget(step, i)
            self.steps_layout.addWidget(step_widget)
    
    def _create_step_widget(self, step: ProcessingStepInfo, index: int) -> QWidget:
        """Crée un widget pour une étape"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        
        # Style selon le statut
        if step.status == "completed":
            widget.setStyleSheet("background-color: #d5f4e6; border: 1px solid #27ae60; border-radius: 3px;")
            status_icon = "✅"
        elif step.status == "running":
            widget.setStyleSheet("background-color: #fff3cd; border: 1px solid #f39c12; border-radius: 3px;")
            status_icon = "🟡"
        elif step.status == "error":
            widget.setStyleSheet("background-color: #f8d7da; border: 1px solid #e74c3c; border-radius: 3px;")
            status_icon = "🔴"
        else:
            widget.setStyleSheet("background-color: #f8f9fa; border: 1px solid #6c757d; border-radius: 3px;")
            status_icon = "⭕"
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(8, 4, 8, 4)
        
        # Icône et nom
        status_label = QLabel(f"{status_icon} {step.name}")
        status_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        layout.addWidget(status_label)
        
        layout.addStretch()
        
        # Barre de progression de l'étape (si en cours)
        if step.status == "running":
            step_progress = QProgressBar()
            step_progress.setMaximum(100)
            step_progress.setValue(step.progress)
            step_progress.setMaximumWidth(100)
            step_progress.setMaximumHeight(15)
            layout.addWidget(step_progress)
        
        # Temps écoulé
        if step.start_time:
            if step.end_time:
                duration = step.end_time - step.start_time
                time_label = QLabel(f"{duration:.1f}s")
            else:
                duration = time.time() - step.start_time
                time_label = QLabel(f"{duration:.1f}s...")
            
            time_label.setStyleSheet("font-size: 10px; color: #6c757d;")
            layout.addWidget(time_label)
        
        return widget
    
    def _update_eta(self):
        """Met à jour l'estimation du temps restant"""
        if not self.start_time or self.current_step_index >= len(self.steps):
            return
        
        elapsed = time.time() - self.start_time
        completed_steps = sum(1 for step in self.steps if step.status == "completed")
        
        if completed_steps > 0:
            avg_time_per_step = elapsed / completed_steps
            remaining_steps = len(self.steps) - completed_steps
            eta = remaining_steps * avg_time_per_step
            
            self.eta_label.setText(f"ETA: {self._format_duration(eta)}")
    
    def _format_duration(self, seconds: float) -> str:
        """Formate une durée en secondes"""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            return f"{int(seconds // 60)}m {int(seconds % 60)}s"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}h {minutes}m"
    
    def _update_current_step(self):
        """Met à jour l'étape courante"""
        if self.current_step_index < len(self.steps):
            self.start_step(self.current_step_index)

class FileProcessingWidget(QWidget):
    """Widget pour afficher le traitement des fichiers"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_widgets = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface"""
        layout = QVBoxLayout(self)
        
        # En-tête
        header = QLabel("Traitement des fichiers")
        header.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header)
        
        # Zone de défilement pour les fichiers
        scroll_area = QScrollArea()
        self.files_container = QWidget()
        self.files_layout = QVBoxLayout(self.files_container)
        scroll_area.setWidget(self.files_container)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
    
    def add_file(self, filename: str):
        """Ajoute un fichier à traiter"""
        file_widget = self._create_file_widget(filename)
        self.files_layout.addWidget(file_widget)
        self.file_widgets[filename] = file_widget
    
    def update_file_status(self, filename: str, status: str, progress: int = 0):
        """Met à jour le statut d'un fichier"""
        if filename in self.file_widgets:
            widget = self.file_widgets[filename]
            # Mettre à jour le widget (à implémenter selon les besoins)
    
    def _create_file_widget(self, filename: str) -> QWidget:
        """Crée un widget pour un fichier"""
        widget = QFrame()
        widget.setFrameStyle(QFrame.Shape.StyledPanel)
        widget.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin: 2px;
                padding: 5px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        
        # Icône de fichier
        icon_label = QLabel("📄")
        layout.addWidget(icon_label)
        
        # Nom du fichier
        name_label = QLabel(filename)
        name_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(name_label)
        
        layout.addStretch()
        
        # Statut
        status_label = QLabel("En attente...")
        status_label.setStyleSheet("color: #6c757d; font-size: 12px;")
        layout.addWidget(status_label)
        
        return widget

class OptimizedProcessingDialog(QDialog):
    """Dialogue de traitement optimisé"""
    
    def __init__(self, files: List[str], parent=None):
        super().__init__(parent)
        self.files = files
        self.parent_app = parent
        self.processing_steps = []
        self.is_processing = False
        self.setup_ui()
        self.setup_processing_steps()
    
    def setup_ui(self):
        """Configure l'interface du dialogue"""
        self.setWindowTitle("Traitement des fichiers")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Widget de progression principal
        self.progress_widget = EnhancedProgressWidget()
        layout.addWidget(self.progress_widget)
        
        # Séparateur
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        
        # Widget de traitement des fichiers
        self.file_widget = FileProcessingWidget()
        layout.addWidget(self.file_widget)
        
        # Ajouter les fichiers
        for filename in self.files:
            self.file_widget.add_file(filename)
        
        # Boutons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.cancel_button = QPushButton("Annuler")
        self.cancel_button.clicked.connect(self._on_cancel)
        button_layout.addWidget(self.cancel_button)
        
        self.close_button = QPushButton("Fermer")
        self.close_button.clicked.connect(self.accept)
        self.close_button.setEnabled(False)
        button_layout.addWidget(self.close_button)
        
        layout.addLayout(button_layout)
    
    def setup_processing_steps(self):
        """Définit les étapes de traitement"""
        steps = [
            ProcessingStepInfo("Validation", "Validation des fichiers PDF", 2.0),
            ProcessingStepInfo("Extraction", "Extraction du texte", 5.0),
            ProcessingStepInfo("Analyse LLM", "Analyse par intelligence artificielle", 15.0),
            ProcessingStepInfo("Traitement", "Traitement des données", 8.0),
            ProcessingStepInfo("Génération", "Génération des fichiers Excel", 3.0)
        ]
        
        self.progress_widget.set_steps(steps)
    
    def exec(self):
        """Execute le dialogue avec traitement automatique"""
        try:
            # Afficher le dialogue d'abord
            self.show()
            self.progress_widget.add_log_message("🎯 Dialogue optimisé ouvert")
            # Démarrer le traitement automatiquement après un court délai
            QTimer.singleShot(100, self.start_processing)
            result = super().exec()
            self.progress_widget.add_log_message(f"🔚 Dialogue fermé: {result}")
            return result
        except Exception as e:
            print(f"Erreur dans exec(): {e}")
            import traceback
            traceback.print_exc()
            return 0
    
    def start_processing(self):
        """Démarre le traitement"""
        try:
            self.progress_widget.add_log_message("🚀 start_processing appelé")
            
            if self.is_processing:
                self.progress_widget.add_log_message("⚠️ Traitement déjà en cours")
                return
                
            self.is_processing = True
            self.progress_widget.start_processing()
            self.cancel_button.setText("Arrêter")
            self.progress_widget.add_log_message("🎮 Interface mise à jour")
            
            # Toujours utiliser le vrai traitement
            self.progress_widget.add_log_message("🎯 Démarrage du traitement réel")
            self._real_processing()
            
        except Exception as e:
            error_msg = f"❌ Erreur start_processing: {str(e)}"
            self.progress_widget.add_log_message(error_msg)
            print(error_msg)
            import traceback
            traceback.print_exc()
    
    def _simulate_processing(self):
        """Simulation du traitement pour demo"""
        import random
        
        def simulate_step(step_index):
            if step_index >= len(self.processing_steps):
                return
            
            # Simuler la progression de l'étape
            for progress in range(0, 101, 20):
                QTimer.singleShot(
                    step_index * 1000 + progress * 50,
                    lambda p=progress, i=step_index: self.progress_widget.update_step_progress(
                        i, p, f"Progression: {p}%"
                    )
                )
            
            # Marquer l'étape comme terminée
            QTimer.singleShot(
                (step_index + 1) * 1000,
                lambda i=step_index: self.progress_widget.complete_step(i)
            )
            
            # Passer à l'étape suivante
            QTimer.singleShot(
                (step_index + 1) * 1000 + 100,
                lambda i=step_index: simulate_step(i + 1) if i + 1 < 5 else self._processing_completed()
            )
        
        simulate_step(0)
    
    def _real_processing(self):
        """Lance le vrai traitement via ProcessingThread"""
        try:
            self.progress_widget.add_log_message("🔍 Initialisation du traitement...")
            
            # Récupérer les paramètres depuis l'application parente
            if not self.parent_app:
                self._processing_error("❌ Application parente non disponible")
                return
            
            self.progress_widget.add_log_message("📋 Récupération des paramètres...")
            
            # Obtenir les paramètres de traitement avec valeurs par défaut sécurisées
            try:
                enrich_llm = getattr(self.parent_app, 'enrich_llm_checkbox', None)
                enrich_llm = enrich_llm.isChecked() if enrich_llm else True
                
                llm_provider = getattr(self.parent_app, 'current_llm_provider', 'openrouter')
                api_key = getattr(self.parent_app, 'openrouter_api_key', '')
                
                # Obtenir semaine et année de production
                semaine_prod = getattr(self.parent_app, 'semaine_input', None)
                semaine_prod = semaine_prod.value() if semaine_prod else 35
                
                annee_prod = getattr(self.parent_app, 'annee_input', None) 
                annee_prod = annee_prod.value() if annee_prod else 2025
                
                # Commande client par défaut vide (l'utilisateur peut la modifier dans l'interface)
                commande_client = ""
                
                self.progress_widget.add_log_message(f"✅ Paramètres: {llm_provider}, {len(self.files)} fichiers")
                
            except Exception as e:
                self._processing_error(f"❌ Erreur paramètres: {str(e)}")
                return
            
            # Importer ProcessingThread 
            try:
                self.progress_widget.add_log_message("📦 Chargement du module de traitement...")
                
                # Éviter l'import circulaire
                import sys
                app_module = sys.modules.get('__main__')
                if app_module and hasattr(app_module, 'ProcessingThread'):
                    ProcessingThread = app_module.ProcessingThread
                else:
                    from app_gui import ProcessingThread
                    
                self.progress_widget.add_log_message("✅ Module de traitement chargé")
                
            except Exception as e:
                self._processing_error(f"❌ Erreur import: {str(e)}")
                return
            
            # Créer et configurer le thread
            try:
                self.progress_widget.add_log_message("🚀 Création du thread de traitement...")
                
                self.processing_thread = ProcessingThread(
                    self.files, enrich_llm, llm_provider, api_key,
                    semaine_prod, annee_prod, commande_client
                )
                
                # Connecter les signaux
                self.processing_thread.progress_updated.connect(self._on_progress_updated)
                self.processing_thread.result_ready.connect(self._on_result_ready) 
                self.processing_thread.error_occurred.connect(self._on_error)
                self.processing_thread.log_message.connect(self._on_log_message)
                
                self.progress_widget.add_log_message("✅ Thread configuré, démarrage...")
                
                # Démarrer le traitement
                self.processing_thread.start()
                
            except Exception as e:
                self._processing_error(f"❌ Erreur thread: {str(e)}")
                return
            
        except Exception as e:
            self._processing_error(f"❌ Erreur générale: {str(e)}")
    
    def _processing_error(self, error_msg: str):
        """Gère les erreurs de traitement"""
        self.progress_widget.add_log_message(error_msg)
        self.cancel_button.setText("Fermer")
        self.close_button.setEnabled(True)
        self.is_processing = False
    
    def _on_progress_updated(self, progress: int):
        """Met à jour la progression"""
        try:
            self.progress_widget.add_log_message(f"📊 Progression reçue: {progress}%")
            
            # Convertir la progression globale en progression d'étape
            current_step = min(progress // 20, 4)  # 5 étapes, 20% chacune
            step_progress = (progress % 20) * 5    # Progression dans l'étape courante
            
            # Vérifier si le widget de progression a les bonnes étapes
            if hasattr(self.progress_widget, 'update_step_progress'):
                try:
                    self.progress_widget.update_step_progress(
                        current_step, step_progress, 
                        f"Étape {current_step+1}: {step_progress}%"
                    )
                    self.progress_widget.add_log_message(f"🎯 Étape {current_step+1} mise à jour: {step_progress}%")
                except Exception as e:
                    self.progress_widget.add_log_message(f"⚠️ Erreur update_step: {e}")
                    # Fallback sur message simple
                    self.progress_widget.add_log_message(f"📊 Global: {progress}%")
            else:
                # Fallback sur message simple
                self.progress_widget.add_log_message(f"📊 Progression globale: {progress}%")
        except Exception as e:
            self.progress_widget.add_log_message(f"⚠️ Erreur progression: {e}")
    
    def _on_result_ready(self, result: dict):
        """Traitement terminé avec résultats"""
        self.progress_widget.add_log_message("✅ Traitement terminé avec succès!")
        self.progress_widget.add_log_message(f"📊 {len(result)} résultat(s) généré(s)")
        
        # Transférer les résultats à l'application principale
        if self.parent_app and hasattr(self.parent_app, 'display_results'):
            try:
                self.parent_app.display_results(result)
                self.progress_widget.add_log_message("📋 Résultats affichés dans l'interface principale")
            except Exception as e:
                self.progress_widget.add_log_message(f"⚠️ Erreur affichage résultats: {e}")
        
        self._processing_completed()
    
    def _on_error(self, error_msg: str):
        """Gère les erreurs du ProcessingThread"""
        self._processing_error(f"❌ {error_msg}")
    
    def _on_log_message(self, message: str, level: str):
        """Affiche les messages de log"""
        icon = "ℹ️" if level == "INFO" else "⚠️" if level == "WARNING" else "❌"
        self.progress_widget.add_log_message(f"{icon} {message}")
    
    def _processing_completed(self):
        """Traitement terminé"""
        try:
            # Marquer toutes les étapes comme terminées si possible
            if hasattr(self.progress_widget, 'complete_step'):
                # Essayer de compléter 5 étapes (nombre standard)
                for i in range(5):
                    try:
                        self.progress_widget.complete_step(i)
                    except:
                        break
            
            self.cancel_button.setEnabled(False)
            self.close_button.setEnabled(True)
            self.is_processing = False
            self.progress_widget.add_log_message("🎉 Traitement complété!")
        except Exception as e:
            self.progress_widget.add_log_message(f"⚠️ Erreur finalisation: {e}")
    
    def _on_cancel(self):
        """Gère l'annulation du traitement"""
        if self.is_processing and hasattr(self, 'processing_thread'):
            # Arrêter le thread de traitement
            self.processing_thread.terminate()
            self.processing_thread.wait(3000)  # Attendre jusqu'à 3 secondes
            self.progress_widget.add_log_message("⚠️ Traitement annulé par l'utilisateur")
            self.is_processing = False
        
        # Fermer le dialogue
        self.reject()

def create_processing_steps_for_files(files: List[str]) -> List[ProcessingStepInfo]:
    """Crée les étapes de traitement pour une liste de fichiers"""
    base_steps = [
        ("Validation", "Validation des fichiers PDF", 1.0),
        ("Extraction", "Extraction du texte", 2.0),
        ("Analyse", "Analyse par IA", 8.0),
        ("Traitement", "Traitement des données", 3.0),
        ("Export", "Génération Excel", 1.0)
    ]
    
    steps = []
    for name, desc, base_duration in base_steps:
        # Adapter la durée selon le nombre de fichiers
        duration = base_duration * len(files)
        steps.append(ProcessingStepInfo(name, desc, duration))
    
    return steps