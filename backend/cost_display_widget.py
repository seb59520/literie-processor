"""
Widget PyQt6 pour afficher les coûts API et l'historique des fichiers
Intégrable dans l'interface principale de l'application
"""

import sys
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QTableWidget, QTableWidgetItem, QPushButton,
                            QTabWidget, QGroupBox, QScrollArea, QFrame,
                            QHeaderView, QProgressBar, QTextEdit, QDialog,
                            QDialogButtonBox, QDateEdit, QComboBox)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QDate
from PyQt6.QtGui import QFont, QColor, QPalette
import logging
from datetime import datetime, timedelta
from backend.cost_tracker import cost_tracker

logger = logging.getLogger(__name__)

class CostStatsThread(QThread):
    """Thread pour charger les statistiques de coûts en arrière-plan"""
    stats_ready = pyqtSignal(dict)
    history_ready = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.load_stats = True
        self.load_history = True
    
    def run(self):
        try:
            if self.load_stats:
                daily_stats = cost_tracker.get_daily_stats()
                self.stats_ready.emit(daily_stats)
            
            if self.load_history:
                file_history = cost_tracker.get_file_history(50)
                self.history_ready.emit(file_history)
                
        except Exception as e:
            logger.error(f"Erreur chargement statistiques: {e}")

class CostSummaryWidget(QWidget):
    """Widget résumé des coûts du jour"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre
        title = QLabel("📊 Coûts API du jour")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Frame principal
        main_frame = QFrame()
        main_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        main_layout = QVBoxLayout(main_frame)
        
        # Stats principales
        self.total_cost_label = QLabel("Coût total: $0.00")
        self.total_calls_label = QLabel("Appels API: 0")
        self.total_tokens_label = QLabel("Tokens: 0")
        self.avg_time_label = QLabel("Temps moyen: 0.0s")
        
        # Style des labels
        for label in [self.total_cost_label, self.total_calls_label, 
                     self.total_tokens_label, self.avg_time_label]:
            label.setStyleSheet("QLabel { padding: 5px; background-color: #f0f0f0; border-radius: 3px; }")
        
        main_layout.addWidget(self.total_cost_label)
        main_layout.addWidget(self.total_calls_label)
        main_layout.addWidget(self.total_tokens_label)
        main_layout.addWidget(self.avg_time_label)
        
        layout.addWidget(main_frame)
        self.setLayout(layout)
    
    def update_stats(self, stats):
        """Met à jour l'affichage avec les nouvelles statistiques"""
        try:
            self.total_cost_label.setText(f"💰 Coût total: ${stats.get('total_cost', 0.0):.4f}")
            self.total_calls_label.setText(f"📞 Appels API: {stats.get('total_calls', 0)}")
            self.total_tokens_label.setText(f"🔤 Tokens: {stats.get('total_tokens', 0):,}")
            self.avg_time_label.setText(f"⏱️ Temps moyen: {stats.get('avg_processing_time', 0.0):.2f}s")
            
            # Changer la couleur selon le coût
            cost = stats.get('total_cost', 0.0)
            if cost > 1.0:
                color = "#ff6b6b"  # Rouge si coût élevé
            elif cost > 0.1:
                color = "#ffa726"  # Orange si coût modéré
            else:
                color = "#66bb6a"  # Vert si coût faible
                
            self.total_cost_label.setStyleSheet(f"QLabel {{ padding: 5px; background-color: {color}; color: white; border-radius: 3px; font-weight: bold; }}")
            
        except Exception as e:
            logger.error(f"Erreur mise à jour stats: {e}")

class FileHistoryWidget(QWidget):
    """Widget pour l'historique des fichiers traités"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre et bouton refresh
        header_layout = QHBoxLayout()
        title = QLabel("📁 Historique des fichiers")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_history)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Tableau
        self.history_table = QTableWidget()
        self.history_table.setColumnCount(7)
        self.history_table.setHorizontalHeaderLabels([
            "Fichier", "Date", "Taille", "Appels", "Coût", "Temps", "Statut"
        ])
        
        # Configuration du tableau
        header = self.history_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)  # Fichier
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)  # Date
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # Taille
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Appels
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Coût
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Temps
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Statut
        
        self.history_table.setAlternatingRowColors(True)
        self.history_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        
        layout.addWidget(self.history_table)
        self.setLayout(layout)
    
    def update_history(self, history):
        """Met à jour le tableau avec l'historique"""
        try:
            self.history_table.setRowCount(len(history))
            
            for row, session in enumerate(history):
                # Nom du fichier
                file_item = QTableWidgetItem(session.get('file_name', 'Unknown'))
                self.history_table.setItem(row, 0, file_item)
                
                # Date (formatée)
                timestamp = session.get('timestamp', '')
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    date_str = dt.strftime('%d/%m %H:%M')
                except:
                    date_str = timestamp[:16] if timestamp else 'Unknown'
                date_item = QTableWidgetItem(date_str)
                self.history_table.setItem(row, 1, date_item)
                
                # Taille du fichier
                size_bytes = session.get('file_size', 0)
                if size_bytes > 1024*1024:
                    size_str = f"{size_bytes/(1024*1024):.1f} MB"
                elif size_bytes > 1024:
                    size_str = f"{size_bytes/1024:.1f} KB"
                else:
                    size_str = f"{size_bytes} B"
                size_item = QTableWidgetItem(size_str)
                self.history_table.setItem(row, 2, size_item)
                
                # Nombre d'appels
                calls_item = QTableWidgetItem(str(session.get('total_api_calls', 0)))
                calls_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 3, calls_item)
                
                # Coût
                cost = session.get('total_cost', 0.0)
                cost_item = QTableWidgetItem(f"${cost:.4f}")
                cost_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
                
                # Couleur selon le coût
                if cost > 0.1:
                    cost_item.setBackground(QColor("#ffebee"))  # Rouge clair
                elif cost > 0.01:
                    cost_item.setBackground(QColor("#fff3e0"))  # Orange clair
                else:
                    cost_item.setBackground(QColor("#e8f5e8"))  # Vert clair
                    
                self.history_table.setItem(row, 4, cost_item)
                
                # Temps de traitement
                time_s = session.get('processing_time', 0.0)
                time_item = QTableWidgetItem(f"{time_s:.2f}s")
                time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.history_table.setItem(row, 5, time_item)
                
                # Statut
                success = session.get('success', False)
                status_item = QTableWidgetItem("✅" if success else "❌")
                status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                if not success:
                    status_item.setBackground(QColor("#ffcdd2"))
                self.history_table.setItem(row, 6, status_item)
                
        except Exception as e:
            logger.error(f"Erreur mise à jour historique: {e}")
    
    def refresh_history(self):
        """Actualise l'historique"""
        try:
            history = cost_tracker.get_file_history(50)
            self.update_history(history)
        except Exception as e:
            logger.error(f"Erreur actualisation historique: {e}")

class CostReportDialog(QDialog):
    """Dialog pour générer un rapport de coûts détaillé"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Rapport de coûts détaillé")
        self.setModal(True)
        self.resize(600, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Sélection de période
        period_group = QGroupBox("Période")
        period_layout = QHBoxLayout()
        
        period_layout.addWidget(QLabel("Du:"))
        self.start_date = QDateEdit()
        self.start_date.setDate(QDate.currentDate().addDays(-30))
        period_layout.addWidget(self.start_date)
        
        period_layout.addWidget(QLabel("Au:"))
        self.end_date = QDateEdit()
        self.end_date.setDate(QDate.currentDate())
        period_layout.addWidget(self.end_date)
        
        generate_btn = QPushButton("Générer le rapport")
        generate_btn.clicked.connect(self.generate_report)
        period_layout.addWidget(generate_btn)
        
        period_group.setLayout(period_layout)
        layout.addWidget(period_group)
        
        # Zone de rapport
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Courier", 9))
        layout.addWidget(self.report_text)
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
        self.setLayout(layout)
    
    def generate_report(self):
        """Génère et affiche le rapport"""
        try:
            start = self.start_date.date().toString("yyyy-MM-dd")
            end = self.end_date.date().toString("yyyy-MM-dd")
            
            stats = cost_tracker.export_statistics(start, end)
            
            report = f"""
╔══════════════════════════════════════════════╗
║           RAPPORT DE COÛTS API               ║
╚══════════════════════════════════════════════╝

Période: {start} au {end}

📊 STATISTIQUES GLOBALES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Nombre total d'appels: {stats.get('global_stats', {}).get('total_calls', 0):,}
• Coût total: ${stats.get('global_stats', {}).get('total_cost', 0.0):.4f}
• Tokens consommés: {stats.get('global_stats', {}).get('total_tokens', 0):,}
• Fichiers traités: {stats.get('global_stats', {}).get('total_files', 0)}

🏆 TOP MODÈLES (par coût)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            
            for i, model in enumerate(stats.get('top_models', [])[:10], 1):
                report += f"{i:2}. {model['provider']}/{model['model']}\n"
                report += f"    Appels: {model['calls']:,} | Coût: ${model['cost']:.4f}\n"
            
            if not stats.get('top_models'):
                report += "Aucune donnée disponible pour cette période.\n"
            
            report += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Rapport généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}
"""
            
            self.report_text.setPlainText(report)
            
        except Exception as e:
            logger.error(f"Erreur génération rapport: {e}")
            self.report_text.setPlainText(f"Erreur lors de la génération du rapport: {e}")

class CostDisplayWidget(QWidget):
    """Widget principal pour l'affichage des coûts et historique"""
    
    def __init__(self):
        super().__init__()
        self.stats_thread = None
        self.init_ui()
        self.setup_timer()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Titre principal
        title = QLabel("💰 Tracking des coûts API")
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(14)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Boutons d'action
        buttons_layout = QHBoxLayout()
        
        self.refresh_btn = QPushButton("🔄 Actualiser")
        self.refresh_btn.clicked.connect(self.refresh_data)
        buttons_layout.addWidget(self.refresh_btn)
        
        self.report_btn = QPushButton("📋 Rapport détaillé")
        self.report_btn.clicked.connect(self.show_detailed_report)
        buttons_layout.addWidget(self.report_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        # Tab 1: Résumé du jour
        self.summary_widget = CostSummaryWidget()
        self.tab_widget.addTab(self.summary_widget, "📊 Résumé")
        
        # Tab 2: Historique des fichiers
        self.history_widget = FileHistoryWidget()
        self.tab_widget.addTab(self.history_widget, "📁 Historique")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
        
        # Charger les données initiales
        self.refresh_data()
    
    def setup_timer(self):
        """Configure le timer pour l'actualisation automatique"""
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(30000)  # Actualisation toutes les 30 secondes
    
    def refresh_data(self):
        """Actualise toutes les données"""
        if self.stats_thread and self.stats_thread.isRunning():
            return
            
        self.stats_thread = CostStatsThread()
        self.stats_thread.stats_ready.connect(self.summary_widget.update_stats)
        self.stats_thread.history_ready.connect(self.history_widget.update_history)
        self.stats_thread.finished.connect(self.on_refresh_finished)
        self.stats_thread.start()
        
        self.refresh_btn.setEnabled(False)
        self.refresh_btn.setText("⏳ Chargement...")
    
    def on_refresh_finished(self):
        """Appelée quand l'actualisation est terminée"""
        self.refresh_btn.setEnabled(True)
        self.refresh_btn.setText("🔄 Actualiser")
    
    def show_detailed_report(self):
        """Affiche le dialog de rapport détaillé"""
        dialog = CostReportDialog(self)
        dialog.exec()
    
    def get_current_session_cost(self, session_id: str) -> float:
        """Récupère le coût de la session en cours"""
        try:
            return cost_tracker.get_session_cost(session_id)
        except Exception as e:
            logger.error(f"Erreur récupération coût session: {e}")
            return 0.0


# Fonction utilitaire pour intégrer le widget dans l'app principale
def create_cost_display_widget() -> CostDisplayWidget:
    """Crée et retourne une instance du widget de coûts"""
    return CostDisplayWidget()


if __name__ == "__main__":
    # Test du widget
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    widget = CostDisplayWidget()
    widget.show()
    sys.exit(app.exec())