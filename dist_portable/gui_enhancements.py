"""
Améliorations spécifiques pour l'interface graphique de l'application Matelas
"""

import logging
from typing import Dict, Any, List, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QProgressBar, QTextEdit, QGroupBox, QSplitter, QFrame,
    QTabWidget, QScrollArea, QListWidget, QListWidgetItem,
    QToolTip, QStatusBar, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QThread, QPoint, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QPalette, QColor, QCursor

from ui_optimizations import UIOptimizationManager, SmartProgressBar, AnimationManager
from enhanced_processing_ui import OptimizedProcessingDialog, create_processing_steps_for_files

logger = logging.getLogger(__name__)

class SmartFileSelector(QWidget):
    """Sélecteur de fichiers intelligent avec prévisualisation"""
    
    files_selected = pyqtSignal(list)  # Liste des fichiers sélectionnés
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selected_files = []
        self.file_info_cache = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Configure l'interface du sélecteur"""
        layout = QVBoxLayout(self)
        
        # En-tête avec boutons d'action
        header_layout = QHBoxLayout()
        
        self.select_button = QPushButton("📁 Sélectionner fichiers")
        self.select_button.setStyleSheet("""
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
        self.select_button.clicked.connect(self.select_files)
        header_layout.addWidget(self.select_button)
        
        self.clear_button = QPushButton("🗑️ Vider")
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_button.clicked.connect(self.clear_files)
        header_layout.addWidget(self.clear_button)
        
        header_layout.addStretch()
        
        self.count_label = QLabel("Aucun fichier sélectionné")
        self.count_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        header_layout.addWidget(self.count_label)
        
        layout.addLayout(header_layout)
        
        # Zone de drag & drop
        self.drop_zone = QFrame()
        self.drop_zone.setFrameStyle(QFrame.Shape.StyledPanel)
        self.drop_zone.setStyleSheet("""
            QFrame {
                border: 2px dashed #bdc3c7;
                border-radius: 8px;
                background-color: #f8f9fa;
                min-height: 100px;
            }
            QFrame:hover {
                border-color: #3498db;
                background-color: #ebf3fd;
            }
        """)
        self.drop_zone.setAcceptDrops(True)
        
        drop_layout = QVBoxLayout(self.drop_zone)
        drop_icon = QLabel("📂")
        drop_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_icon.setStyleSheet("font-size: 24px;")
        drop_layout.addWidget(drop_icon)
        
        drop_text = QLabel("Glissez-déposez vos fichiers PDF ici\nou cliquez sur 'Sélectionner fichiers'")
        drop_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        drop_text.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        drop_layout.addWidget(drop_text)
        
        layout.addWidget(self.drop_zone)
        
        # Liste des fichiers sélectionnés
        self.files_list = QListWidget()
        self.files_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: white;
            }
            QListWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:hover {
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.files_list)
    
    def select_files(self):
        """Ouvre le dialogue de sélection de fichiers"""
        from PyQt6.QtWidgets import QFileDialog
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Sélectionner les fichiers PDF",
            "",
            "Fichiers PDF (*.pdf)"
        )
        
        if files:
            self.add_files(files)
    
    def add_files(self, files: List[str]):
        """Ajoute des fichiers à la sélection"""
        for file_path in files:
            if file_path not in self.selected_files:
                self.selected_files.append(file_path)
                self._add_file_item(file_path)
        
        self._update_display()
        self.files_selected.emit(self.selected_files)
    
    def clear_files(self):
        """Vide la sélection de fichiers"""
        self.selected_files.clear()
        self.files_list.clear()
        self._update_display()
        self.files_selected.emit([])
    
    def _add_file_item(self, file_path: str):
        """Ajoute un élément de fichier à la liste"""
        import os
        
        item = QListWidgetItem()
        
        # Widget personnalisé pour l'item
        item_widget = QWidget()
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(4, 4, 4, 4)
        
        # Icône
        icon_label = QLabel("📄")
        item_layout.addWidget(icon_label)
        
        # Informations du fichier
        info_layout = QVBoxLayout()
        
        filename = os.path.basename(file_path)
        name_label = QLabel(filename)
        name_label.setStyleSheet("font-weight: bold; font-size: 12px;")
        info_layout.addWidget(name_label)
        
        # Taille du fichier
        try:
            size = os.path.getsize(file_path)
            size_mb = size / (1024 * 1024)
            size_text = f"{size_mb:.1f} MB"
        except:
            size_text = "Taille inconnue"
        
        size_label = QLabel(size_text)
        size_label.setStyleSheet("color: #7f8c8d; font-size: 10px;")
        info_layout.addWidget(size_label)
        
        item_layout.addLayout(info_layout)
        item_layout.addStretch()
        
        # Bouton de suppression
        remove_button = QPushButton("✖")
        remove_button.setMaximumSize(20, 20)
        remove_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 10px;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        remove_button.clicked.connect(lambda: self._remove_file(file_path))
        item_layout.addWidget(remove_button)
        
        item.setSizeHint(item_widget.sizeHint())
        self.files_list.addItem(item)
        self.files_list.setItemWidget(item, item_widget)
    
    def _remove_file(self, file_path: str):
        """Supprime un fichier de la sélection"""
        if file_path in self.selected_files:
            self.selected_files.remove(file_path)
            
            # Trouver et supprimer l'item correspondant
            for i in range(self.files_list.count()):
                item = self.files_list.item(i)
                widget = self.files_list.itemWidget(item)
                # Logic pour identifier le bon item à supprimer
                # (simplifiée ici)
            
            self._rebuild_file_list()
            self._update_display()
            self.files_selected.emit(self.selected_files)
    
    def _rebuild_file_list(self):
        """Reconstruit la liste des fichiers"""
        self.files_list.clear()
        for file_path in self.selected_files:
            self._add_file_item(file_path)
    
    def _update_display(self):
        """Met à jour l'affichage des compteurs"""
        count = len(self.selected_files)
        if count == 0:
            self.count_label.setText("Aucun fichier sélectionné")
        elif count == 1:
            self.count_label.setText("1 fichier sélectionné")
        else:
            self.count_label.setText(f"{count} fichiers sélectionnés")

class EnhancedStatusBar(QStatusBar):
    """Barre de statut améliorée avec informations détaillées"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
        # Timer pour les mises à jour
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_system_info)
        self.update_timer.start(2000)  # Mise à jour toutes les 2 secondes
    
    def setup_ui(self):
        """Configure l'interface de la barre de statut"""
        # Message principal
        self.main_message = QLabel("Prêt")
        self.addWidget(self.main_message)
        
        # Séparateur
        separator1 = QFrame()
        separator1.setFrameShape(QFrame.Shape.VLine)
        separator1.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(separator1)
        
        # Informations système
        self.system_info = QLabel("Système: OK")
        self.addWidget(self.system_info)
        
        # Séparateur
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        self.addWidget(separator2)
        
        # Performance
        self.performance_info = QLabel("Performance: Normale")
        self.addWidget(self.performance_info)
        
        # Espace permanent pour les informations d'état
        self.addPermanentWidget(QLabel("🟢 En ligne"))
    
    def update_system_info(self):
        """Met à jour les informations système"""
        try:
            import psutil
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=None)
            
            # Mémoire
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            
            # Mise à jour des affichages
            if cpu_percent > 80 or memory_percent > 85:
                self.performance_info.setText(f"⚠️ CPU: {cpu_percent:.0f}% RAM: {memory_percent:.0f}%")
                self.performance_info.setStyleSheet("color: orange;")
            elif cpu_percent > 90 or memory_percent > 95:
                self.performance_info.setText(f"🔴 CPU: {cpu_percent:.0f}% RAM: {memory_percent:.0f}%")
                self.performance_info.setStyleSheet("color: red;")
            else:
                self.performance_info.setText(f"✅ CPU: {cpu_percent:.0f}% RAM: {memory_percent:.0f}%")
                self.performance_info.setStyleSheet("color: green;")
                
        except ImportError:
            self.performance_info.setText("Système: Non disponible")

class SmartTooltipManager:
    """Gestionnaire de tooltips intelligents"""
    
    def __init__(self):
        self.tooltips = {}
        self.help_texts = {
            'file_selector': """
<b>Sélection de fichiers</b><br>
• Cliquez sur 'Sélectionner fichiers' pour ouvrir l'explorateur<br>
• Ou glissez-déposez vos fichiers PDF directement ici<br>
• Formats supportés: PDF uniquement<br>
• Taille maximale recommandée: 50 MB par fichier
            """,
            'llm_provider': """
<b>Fournisseur d'IA</b><br>
• <b>OpenRouter</b>: Service cloud avec modèles variés<br>
• <b>Ollama</b>: Modèles locaux (plus privé, plus lent)<br>
• <b>OpenAI</b>: GPT-4 et autres modèles OpenAI<br>
<i>💡 OpenRouter est recommandé pour de meilleures performances</i>
            """,
            'processing_options': """
<b>Options de traitement</b><br>
• <b>Enrichissement LLM</b>: Analyse approfondie par IA<br>
• <b>Validation rapide</b>: Traitement basique sans IA<br>
• <b>Mode batch</b>: Traitement optimisé pour plusieurs fichiers
            """
        }
    
    def setup_tooltip(self, widget: QWidget, tooltip_key: str, custom_text: str = None):
        """Configure un tooltip pour un widget"""
        tooltip_text = custom_text or self.help_texts.get(tooltip_key, "")
        if tooltip_text:
            widget.setToolTip(tooltip_text)
            widget.setToolTipDuration(5000)  # 5 secondes
    
    def show_context_help(self, widget: QWidget, position: QPoint = None):
        """Affiche une aide contextuelle"""
        if not position:
            position = QCursor.pos()
        
        # Trouver le tooltip approprié
        tooltip_text = widget.toolTip()
        if tooltip_text:
            QToolTip.showText(position, tooltip_text)

class MatelasAppEnhancements:
    """Gestionnaire des améliorations pour MatelasApp"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.animation_manager = AnimationManager()
        self.tooltip_manager = SmartTooltipManager()
        self.ui_optimizer = None
        
    def apply_all_enhancements(self):
        """Applique toutes les améliorations à l'application"""
        try:
            self._enhance_file_selection()
            self._enhance_progress_display()
            self._enhance_status_bar()
            self._setup_tooltips()
            self._apply_responsive_design()
            self._setup_keyboard_shortcuts()
            
            logger.info("Toutes les améliorations UI appliquées avec succès")
        except Exception as e:
            logger.error(f"Erreur lors de l'application des améliorations: {e}")
    
    def _enhance_file_selection(self):
        """Améliore le sélecteur de fichiers"""
        # Remplacer le sélecteur de fichiers existant par SmartFileSelector
        if hasattr(self.main_app, 'file_selector_group'):
            # Créer le nouveau sélecteur intelligent
            smart_selector = SmartFileSelector()
            smart_selector.files_selected.connect(self._on_files_selected)
            
            # Remplacer dans le layout existant
            # (Code d'intégration spécifique selon la structure existante)
    
    def _enhance_progress_display(self):
        """Améliore l'affichage de progression"""
        # Remplacer les barres de progression existantes
        if hasattr(self.main_app, 'progress_bar'):
            smart_progress = SmartProgressBar()
            # Intégration dans le layout existant
    
    def _enhance_status_bar(self):
        """Améliore la barre de statut"""
        if hasattr(self.main_app, 'statusBar'):
            enhanced_status_bar = EnhancedStatusBar()
            self.main_app.setStatusBar(enhanced_status_bar)
    
    def _setup_tooltips(self):
        """Configure les tooltips intelligents"""
        # Ajouter des tooltips aux éléments principaux
        widget_mappings = {
            # 'file_selector': self.main_app.findChild(...),
            # Mapping des widgets selon la structure existante
        }
        
        for key, widget in widget_mappings.items():
            if widget:
                self.tooltip_manager.setup_tooltip(widget, key)
    
    def _apply_responsive_design(self):
        """Applique le design responsive"""
        # Connecter au redimensionnement
        original_resize = self.main_app.resizeEvent
        
        def enhanced_resize_event(event):
            original_resize(event)
            self._handle_window_resize(event.size())
        
        self.main_app.resizeEvent = enhanced_resize_event
    
    def _handle_window_resize(self, size: QSize):
        """Gère le redimensionnement de fenêtre"""
        width = size.width()
        
        # Adapter l'interface selon la taille
        if width < 800:
            # Mode compact
            self._switch_to_compact_mode()
        elif width < 1200:
            # Mode normal
            self._switch_to_normal_mode()
        else:
            # Mode large
            self._switch_to_large_mode()
    
    def _switch_to_compact_mode(self):
        """Bascule en mode compact"""
        if hasattr(self.main_app, 'splitter'):
            self.main_app.splitter.setOrientation(Qt.Orientation.Vertical)
    
    def _switch_to_normal_mode(self):
        """Bascule en mode normal"""
        if hasattr(self.main_app, 'splitter'):
            self.main_app.splitter.setOrientation(Qt.Orientation.Horizontal)
    
    def _switch_to_large_mode(self):
        """Bascule en mode large"""
        self._switch_to_normal_mode()
        # Ajustements spécifiques au mode large
    
    def _setup_keyboard_shortcuts(self):
        """Configure les raccourcis clavier"""
        from PyQt6.QtGui import QKeySequence, QShortcut
        
        shortcuts = [
            (QKeySequence.StandardKey.Open, self._shortcut_open_files),
            (QKeySequence("Ctrl+R"), self._shortcut_start_processing),
            (QKeySequence("Ctrl+Q"), self.main_app.close),
            (QKeySequence("F5"), self._shortcut_refresh),
        ]
        
        for key_sequence, callback in shortcuts:
            shortcut = QShortcut(key_sequence, self.main_app)
            shortcut.activated.connect(callback)
    
    def _shortcut_open_files(self):
        """Raccourci pour ouvrir des fichiers"""
        # Déclencher l'ouverture de fichiers
        pass
    
    def _shortcut_start_processing(self):
        """Raccourci pour démarrer le traitement"""
        # Déclencher le traitement
        pass
    
    def _shortcut_refresh(self):
        """Raccourci pour actualiser"""
        # Actualiser l'interface
        pass
    
    def _on_files_selected(self, files: List[str]):
        """Gestionnaire de sélection de fichiers"""
        self.main_app.selected_files = files
        # Mettre à jour l'interface selon les fichiers sélectionnés
    
    def show_enhanced_processing_dialog(self, files: List[str]):
        """Affiche le dialogue de traitement amélioré"""
        dialog = OptimizedProcessingDialog(files, self.main_app)
        
        # Animation d'apparition
        fade_in = self.animation_manager.fade_in(dialog)
        fade_in.start()
        
        # Démarrer le traitement
        dialog.start_processing()
        
        return dialog.exec()

# Fonction d'intégration principale
def enhance_matelas_app(app_instance):
    """Applique toutes les améliorations à une instance de MatelasApp"""
    enhancements = MatelasAppEnhancements(app_instance)
    enhancements.apply_all_enhancements()
    return enhancements