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
from pathlib import Path

def setup_advanced_logging(log_level=logging.INFO):
    """Configuration du logging avancé - Version simplifiée portable"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    logger = logging.getLogger("MATELAS")
    logger.setLevel(log_level)
    
    # Handler fichier
    try:
        file_handler = logging.FileHandler(logs_dir / "app.log", encoding='utf-8')
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    except Exception:
        pass
    
    return logger

import subprocess
import glob
import threading
import re
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from aide_generateur_preimport import GenerateurPreImportDialog

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, 
    QLineEdit, QCheckBox, QComboBox, QGroupBox, QScrollArea,
    QProgressBar, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter, QFrame, QMenuBar, QMenu, QTextBrowser, QGridLayout,
    QDialogButtonBox, QDialog, QHeaderView, QFormLayout,
    QListWidget, QListWidgetItem, QStatusBar, QSystemTrayIcon,
    QToolButton, QWidgetAction, QSlider, QSizePolicy
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction, QColor
import webbrowser

# Import des modules backend existants
# # # # # sys.path.append('backend')  # Commenté pour PyInstaller  # Commenté pour PyInstaller  # Commenté pour PyInstaller  # Commenté pour PyInstaller  # Commenté pour PyInstaller
from backend_interface import backend_interface
from config import config
from version import get_version, get_full_version, get_version_info, get_changelog
from backend.asset_utils import get_asset_path

# Import des optimisations
try:
    from ui_optimizations import UIOptimizationManager, SmartProgressBar
    # from enhanced_processing_ui import OptimizedProcessingDialog, EnhancedProgressWidget
    from gui_enhancements import MatelasAppEnhancements, SmartFileSelector, EnhancedStatusBar
    from backend.file_validation import FileValidator, validate_pdf_file
    from backend.llm_cache import llm_cache
    from backend.timeout_manager import timeout_manager
    from backend.advanced_logging import get_advanced_logger, setup_advanced_logging
    from backend.cost_tracker import cost_tracker
    from backend.cost_display_widget import CostDisplayWidget
    UI_OPTIMIZATIONS_AVAILABLE = True
    COST_TRACKING_AVAILABLE = True
    print("✅ Optimisations UI et backend chargées")
except ImportError as e:
    print(f"⚠️ Optimisations non disponibles: {e}")
    UI_OPTIMIZATIONS_AVAILABLE = False
    COST_TRACKING_AVAILABLE = False

# Configuration du logging avancé
ADVANCED_LOGGING_AVAILABLE = False
try:
    advanced_logger = setup_advanced_logging()
    ADVANCED_LOGGING_AVAILABLE = True
    print("✅ Système de logging avancé initialisé")
except Exception as e:
    import logging
    advanced_logger = logging.getLogger('MATELAS')
    print(f"Avertissement logging: {e}")
    print("✅ Système de logging avancé initialisé (mode minimal)")
    advanced_logger = None
    ADVANCED_LOGGING_AVAILABLE = False

# Import du module de stockage sécurisé
try:
    from .backend.secure_storage import secure_storage
    SECURE_STORAGE_AVAILABLE = False
except ImportError as e:
    print(f"Module de stockage sécurisé non disponible: {e}")
    SECURE_STORAGE_AVAILABLE = False

# Import du système d'alertes en temps réel
try:
    from real_time_alerts import (
        RealTimeAlertSystem, AlertPanel, AlertNotificationDialog, AlertSettingsDialog,
        AlertType, AlertCategory, create_system_alert, create_processing_alert,
        create_validation_alert, create_network_alert, create_security_alert, create_production_alert
    )
    ALERT_SYSTEM_AVAILABLE = False
except ImportError as e:
    print(f"Système d'alertes non disponible: {e}")
    ALERT_SYSTEM_AVAILABLE = False

# Import du système de mise à jour automatique
try:
    # from backend.auto_updater import AutoUpdater, UpdateInfo
    AUTO_UPDATE_AVAILABLE = False
    print("✅ Système de mise à jour automatique chargé")
except ImportError as e:
    print(f"⚠️ Système de mise à jour non disponible: {e}")
    AUTO_UPDATE_AVAILABLE = False

# Import du générateur de packages correctifs
try:
    from package_builder_gui import show_package_builder_dialog
    from auto_package_gui import show_auto_package_dialog
    from package_consolidator import create_consolidation_gui
    PACKAGE_BUILDER_AVAILABLE = True
    AUTO_PACKAGE_AVAILABLE = True
    CONSOLIDATION_GUI = create_consolidation_gui()
    print("✅ Générateur de packages correctifs chargé")
    print("✅ Générateur automatique de packages chargé")
    print("✅ Consolidateur de packages chargé")
except ImportError as e:
    print(f"⚠️ Générateur de packages non disponible: {e}")
    PACKAGE_BUILDER_AVAILABLE = False
    AUTO_PACKAGE_AVAILABLE = False
    CONSOLIDATION_GUI = None

# Import du validateur de fichiers optimisé
if UI_OPTIMIZATIONS_AVAILABLE:
    try:
        from backend.file_validation import FileValidator
        file_validator = FileValidator({
            'max_file_size_mb': 100,
            'min_file_size_kb': 1,
            'max_pages': 200,
            'min_text_length': 50,
            'max_text_length': 1000000,
            'allowed_extensions': ['.pdf'],
            'allowed_mime_types': ['application/pdf', 'application/x-pdf', 'text/pdf']
        })
        print("✅ Validateur de fichiers optimisé initialisé")
    except Exception as e:
        print(f"⚠️ Erreur initialisation validateur: {e}")
        file_validator = None
else:
    file_validator = None



# Configuration du système de logs avancé
def setup_logging():
    """Configure le système de logging avancé avec rotation des fichiers"""
    # Créer un dossier de logs dans un répertoire accessible
    import sys
    from pathlib import Path
    
    if getattr(sys, 'frozen', False):
        # Si exécutable PyInstaller - utiliser le dossier utilisateur
        log_dir = Path.home() / "MatelasApp" / "logs"
    else:
        # Si script Python normal - utiliser le dossier du projet
        log_dir = Path(__file__).parent / "logs"
    
    # Créer le dossier s'il n'existe pas
    log_dir.mkdir(parents=True, exist_ok=True)
    log_dir = str(log_dir)  # Convertir en string pour compatibilité
    
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

def extract_commande_number(filename):
    """
    Extrait le numéro de commande du nom de fichier.
    Recherche un chiffre dans le nom de fichier (ex: 'Commande GALOO 435' -> '435')
    
    Args:
        filename (str): Nom du fichier
        
    Returns:
        str: Numéro de commande trouvé ou chaîne vide si aucun numéro trouvé
    """
    # Rechercher un ou plusieurs chiffres dans le nom de fichier
    match = re.search(r'\d+', filename)
    if match:
        return match.group()
    return ""

# Initialiser le logging
logger = setup_logging()

class ProcessingThread(QThread):
    """Thread pour le traitement des fichiers PDF"""
    progress_updated = pyqtSignal(int)
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    log_message = pyqtSignal(str, str)  # message, level
    recommendations_ready = pyqtSignal(dict)  # résultats d'analyse pour recommandations
    noyau_alerts_ready = pyqtSignal(dict)  # alertes de noyaux non détectés
    
    def __init__(self, files, enrich_llm, llm_provider, openrouter_api_key, 
                 semaine_prod, annee_prod, commande_client, skip_analysis=False, noyau_corrections=None):
        super().__init__()
        self.files = files
        self.enrich_llm = enrich_llm
        
        self.llm_provider = llm_provider
        self.openrouter_api_key = openrouter_api_key
        self.semaine_prod = semaine_prod
        self.annee_prod = annee_prod
        self.commande_client = commande_client
        self.skip_analysis = skip_analysis  # Si True, on passe directement au traitement
        self.noyau_corrections = noyau_corrections or {}  # Corrections de noyaux appliquées
        
        # Les semaines de production seront calculées dynamiquement selon le contenu
        self.semaine_matelas = semaine_prod
        self.annee_matelas = annee_prod
        self.semaine_sommiers = semaine_prod
        self.annee_sommiers = annee_prod
        
        # Logger spécifique pour ce thread
        self.thread_logger = logging.getLogger(f"ProcessingThread_{id(self)}")
    
    def analyze_llm_content(self, llm_result):
        """Analyse le contenu LLM pour détecter matelas et sommiers"""
        try:
            if not llm_result:
                return False, False, 0, 0
            
            # Nettoyer et parser le JSON LLM
            import json
            import re
            
            # Nettoyer le texte pour extraire le JSON
            cleaned_text = llm_result.strip()
            
            # Chercher un bloc JSON dans le texte
            json_match = re.search(r'\{.*\}', cleaned_text, re.DOTALL)
            if json_match:
                cleaned_result = json_match.group()
            else:
                cleaned_result = cleaned_text
            
            try:
                llm_data = json.loads(cleaned_result)
            except json.JSONDecodeError:
                self.log_message.emit(f"JSON invalide dans la réponse LLM: {cleaned_result[:200]}...", "WARNING")
                return False, False, 0, 0
            
            # Extraction des articles selon le nouveau format
            articles = llm_data.get('articles', [])
            matelas_articles = []
            sommier_articles = []
            
            for article in articles:
                article_type = article.get('type', '').lower()
                description = article.get('description', '').upper()
                
                if article_type == 'matelas' or 'MATELAS' in description:
                    matelas_articles.append(article)
                elif article_type == 'sommier' or 'SOMMIER' in description:
                    sommier_articles.append(article)
            
            has_matelas = len(matelas_articles) > 0
            has_sommiers = len(sommier_articles) > 0
            
            self.log_message.emit(f"Analyse LLM: {len(matelas_articles)} matelas, {len(sommier_articles)} sommiers", "DEBUG")
            
            return has_matelas, has_sommiers, len(matelas_articles), len(sommier_articles)
            
        except Exception as e:
            self.log_message.emit(f"Erreur analyse LLM: {str(e)}", "WARNING")
            return False, False, 0, 0
    
    def analyze_text_content(self, text):
        """Analyse basique du texte pour détecter matelas et sommiers"""
        try:
            if not text:
                # Si pas de texte, ne pas faire d'hypothèse par défaut
                return False, False, 0, 0
            
            text_upper = text.upper()
            lines = text_upper.split('\n')
            
            # Compter uniquement les lignes qui commencent par "MATELAS" ou "SOMMIER"
            matelas_count = 0
            sommier_count = 0
            
            for line in lines:
                line = line.strip()
                if line.startswith('MATELAS'):
                    matelas_count += 1
                elif line.startswith('SOMMIER'):
                    sommier_count += 1
            
            has_matelas = matelas_count > 0
            has_sommiers = sommier_count > 0
            
            self.log_message.emit(f"Analyse texte: Matelas={has_matelas}({matelas_count}), Sommiers={has_sommiers}({sommier_count})", "DEBUG")
            
            return has_matelas, has_sommiers, matelas_count, sommier_count
            
        except Exception as e:
            self.log_message.emit(f"Erreur analyse texte: {str(e)}", "WARNING")
            # En cas d'erreur, ne pas faire d'hypothèse par défaut
            return False, False, 0, 0
    
    def detect_noyau_alerts(self, llm_data, file_path):
        """Détecte les noyaux non détectés (INCONNU) dans les données LLM"""
        try:
            alerts = []
            
            # Extraction des articles matelas
            articles = llm_data.get('articles', [])
            matelas_articles = []
            
            for article in articles:
                description = article.get('description', '').upper()
                if (description.startswith('MATELAS') and 
                    'PROTEGE MATELAS' not in description and 
                    'PROTÈGE MATELAS' not in description and 
                    'SURMATELAS' not in description):
                    matelas_articles.append(article)
            
            if not matelas_articles:
                return alerts
            
            # Détection des noyaux
            from backend.matelas_utils import detecter_noyau_matelas
            noyaux_matelas = detecter_noyau_matelas(matelas_articles)
            
            # Identifier les noyaux INCONNU
            for i, noyau_info in enumerate(noyaux_matelas):
                if noyau_info['noyau'] == 'INCONNU':
                    # Récupérer l'article correspondant
                    if i < len(matelas_articles):
                        article = matelas_articles[i]
                        alert = {
                            'index': noyau_info['index'],
                            'description': article.get('description', ''),
                            'noyau': noyau_info['noyau'],
                            'quantite': article.get('quantite', 1),
                            'dimensions': article.get('dimensions', '')
                        }
                        alerts.append(alert)
            
            return alerts
            
        except Exception as e:
            self.log_message.emit(f"Erreur détection alertes noyaux: {str(e)}", "WARNING")
            return []
    
    def run(self):
        try:
            total_files = len(self.files)
            self.log_message.emit(f"Début du traitement de {total_files} fichiers", "INFO")
            self.progress_updated.emit(5)
            
            # Si on doit passer l'analyse préliminaire, aller directement au traitement
            if self.skip_analysis:
                self.log_message.emit("Continuation du traitement avec les semaines confirmées...", "INFO")
                self.progress_updated.emit(50)
                self._do_final_processing()
                return
            
            # Initialisation et validation
            self.log_message.emit("Validation des fichiers et préparation...", "INFO")
            self.progress_updated.emit(10)
            
            # Analyse préliminaire pour détecter le contenu des fichiers
            self.log_message.emit("Analyse préliminaire du contenu...", "INFO")
            self.progress_updated.emit(15)
            
            # Analyser le contenu de chaque fichier pour détecter matelas/sommiers
            file_analysis_results = {}
            
            for i, file_path in enumerate(self.files):
                try:
                    self.log_message.emit(f"Analyse du fichier {i+1}/{total_files}: {os.path.basename(file_path)}", "INFO")
                    
                    # Extraction du texte du PDF avec gestion d'erreur robuste
                    text = ""
                    try:
                        import fitz  # PyMuPDF
                        doc = fitz.open(file_path)
                        text = "\n".join(page.get_text() for page in doc)
                        doc.close()
                        self.log_message.emit(f"Texte extrait: {len(text)} caractères", "DEBUG")
                    except ImportError:
                        self.log_message.emit("PyMuPDF non disponible, utilisation de l'analyse basique", "WARNING")
                        text = "MATELAS SOMMIER"  # Texte par défaut pour l'analyse basique
                    except Exception as e:
                        self.log_message.emit(f"Erreur extraction PDF: {str(e)}", "WARNING")
                        text = "MATELAS SOMMIER"  # Texte par défaut
                    
                    # Analyse du contenu avec fallback robuste
                    has_matelas = False
                    has_sommiers = False
                    matelas_count = 0
                    sommier_count = 0
                    
                    if self.enrich_llm and text:
                        try:
                            self.log_message.emit(f"Analyse LLM du fichier {i+1}/{total_files}...", "INFO")
                            
                            # Appel LLM pour analyse rapide
                            import asyncio
                            llm_result = None
                            
                            if self.llm_provider in ["ollama", "openrouter", "openai", "anthropic", "gemini", "mistral"]:
                                try:
                                    from backend.llm_provider import llm_manager
                                    
                                    # Configurer le provider
                                    llm_manager.set_provider(self.llm_provider, self.openrouter_api_key)
                                    
                                    # Prompt spécifique pour l'analyse du contenu
                                    prompt = f"""Analyse le contenu de cette commande de literie et identifie PRÉCISÉMENT les articles présents.

Contenu de la commande:
{text}

IMPORTANT: 
- Un MATELAS est un article de literie sur lequel on dort (latex, mousse, memory foam, etc.)
- Un SOMMIER est un support en bois avec des lattes ou un cadre pour soutenir le matelas
- Ne confonds PAS matelas et sommiers
- Si tu n'es pas sûr, ne fais pas d'hypothèse

Réponds uniquement avec un JSON au format suivant:
{{
    "articles": [
        {{
            "description": "Description précise de l'article",
            "type": "matelas" ou "sommier" (selon la nature exacte),
            "quantite": nombre
        }}
    ]
}}

Si tu ne peux pas analyser le contenu ou si tu n'es pas sûr, réponds avec un JSON vide: {{"articles": []}}"""
                                    
                                    # Appeler le LLM
                                    result = llm_manager.call_llm(prompt)
                                    
                                    if result["success"]:
                                        llm_result = result["content"]
                                        self.log_message.emit(f"LLM {self.llm_provider} réussi: {len(llm_result)} caractères", "DEBUG")
                                    else:
                                        error_msg = result.get('error', 'Erreur inconnue')
                                        self.log_message.emit(f"Erreur LLM {self.llm_provider}: {error_msg}", "WARNING")
                                        
                                        # Diagnostic spécifique pour les erreurs 401
                                        if "401" in error_msg or "Unauthorized" in error_msg:
                                            self.log_message.emit(f"🔍 Diagnostic: Clé API {self.llm_provider} invalide ou expirée", "ERROR")
                                            self.log_message.emit(f"💡 Solution: Vérifiez votre clé API dans l'interface de gestion des providers", "INFO")
                                        
                                        llm_result = None
                                        
                                except Exception as e:
                                    self.log_message.emit(f"Erreur {self.llm_provider}: {str(e)}", "WARNING")
                                    llm_result = None
                            
                            # Analyser le résultat LLM
                            if llm_result:
                                has_matelas, has_sommiers, matelas_count, sommier_count = self.analyze_llm_content(llm_result)
                                
                                # Détecter les alertes de noyaux non détectés
                                try:
                                    import json
                                    cleaned_result = llm_result.strip()
                                    json_match = re.search(r'\{.*\}', cleaned_result, re.DOTALL)
                                    if json_match:
                                        cleaned_result = json_match.group()
                                    
                                    llm_data = json.loads(cleaned_result)
                                    noyau_alerts = self.detect_noyau_alerts(llm_data, file_path)
                                    
                                    if noyau_alerts:
                                        self.log_message.emit(f"⚠️ {len(noyau_alerts)} noyau(x) non détecté(s) dans {os.path.basename(file_path)}", "WARNING")
                                        # Stocker les alertes pour affichage ultérieur
                                        if not hasattr(self, 'noyau_alerts_by_file'):
                                            self.noyau_alerts_by_file = {}
                                        self.noyau_alerts_by_file[file_path] = noyau_alerts
                                    
                                except Exception as e:
                                    self.log_message.emit(f"Erreur détection alertes noyaux: {str(e)}", "WARNING")
                            else:
                                # Fallback vers l'analyse basique si LLM échoue
                                has_matelas, has_sommiers, matelas_count, sommier_count = self.analyze_text_content(text)
                                
                        except Exception as e:
                            self.log_message.emit(f"Erreur analyse LLM: {str(e)}, fallback vers analyse basique", "WARNING")
                            has_matelas, has_sommiers, matelas_count, sommier_count = self.analyze_text_content(text)
                    else:
                        # Analyse basique sans LLM
                        has_matelas, has_sommiers, matelas_count, sommier_count = self.analyze_text_content(text)
                    
                    # Calculer les recommandations avec gestion d'erreur
                    try:
                        from backend.date_utils import calculate_production_weeks
                        semaine_actuelle = datetime.now().isocalendar()[1]
                        annee_actuelle = datetime.now().year
                        
                        recommendations = calculate_production_weeks(
                            semaine_actuelle, annee_actuelle, has_matelas, has_sommiers
                        )
                        
                        file_analysis_results[file_path] = {
                            'has_matelas': has_matelas,
                            'has_sommiers': has_sommiers,
                            'matelas_count': matelas_count,
                            'sommier_count': sommier_count,
                            'semaine_actuelle': semaine_actuelle,
                            'annee_actuelle': annee_actuelle,
                            'recommendation': recommendations['recommandation'],
                            'semaine_matelas': recommendations['matelas']['semaine'],
                            'annee_matelas': recommendations['matelas']['annee'],
                            'semaine_sommiers': recommendations['sommiers']['semaine'],
                            'annee_sommiers': recommendations['sommiers']['annee']
                        }
                        
                        self.log_message.emit(f"Analyse réussie: Matelas={has_matelas}, Sommiers={has_sommiers}", "INFO")
                        
                    except Exception as e:
                        self.log_message.emit(f"Erreur calcul recommandations: {str(e)}", "WARNING")
                        # Valeurs par défaut en cas d'erreur de calcul
                        semaine_actuelle = datetime.now().isocalendar()[1]
                        annee_actuelle = datetime.now().year
                        file_analysis_results[file_path] = {
                            'has_matelas': has_matelas,  # Ne pas faire d'hypothèse par défaut
                            'has_sommiers': has_sommiers,
                            'matelas_count': matelas_count,
                            'sommier_count': sommier_count,
                            'semaine_actuelle': semaine_actuelle,
                            'annee_actuelle': annee_actuelle,
                            'recommendation': f"Analyse réussie: {has_matelas} matelas, {has_sommiers} sommiers",
                            'semaine_matelas': semaine_actuelle + 1,
                            'annee_matelas': annee_actuelle,
                            'semaine_sommiers': semaine_actuelle + 1,
                            'annee_sommiers': annee_actuelle
                        }
                    
                except Exception as e:
                    self.log_message.emit(f"Erreur générale lors de l'analyse du fichier {file_path}: {str(e)}", "WARNING")
                    # Valeurs par défaut en cas d'erreur générale
                    file_analysis_results[file_path] = {
                        'has_matelas': False,  # Ne pas faire d'hypothèse par défaut
                        'has_sommiers': False,
                        'matelas_count': 0,
                        'sommier_count': 0,
                        'semaine_actuelle': datetime.now().isocalendar()[1],
                        'annee_actuelle': datetime.now().year,
                        'recommendation': "Erreur d'analyse - vérification manuelle requise",
                        'semaine_matelas': datetime.now().isocalendar()[1] + 1,
                        'annee_matelas': datetime.now().year,
                        'semaine_sommiers': datetime.now().isocalendar()[1] + 1,
                        'annee_sommiers': datetime.now().year
                    }
            
            self.progress_updated.emit(30)
            
            # Vérifier s'il y a des alertes de noyaux
            if hasattr(self, 'noyau_alerts_by_file') and self.noyau_alerts_by_file:
                # Il y a des alertes de noyaux, les afficher en premier
                self.log_message.emit("Affichage des alertes de noyaux non détectés...", "INFO")
                self.noyau_alerts_ready.emit(self.noyau_alerts_by_file)
                return
            else:
                # Pas d'alertes de noyaux, afficher les recommandations de production
                self.log_message.emit("Affichage des recommandations de production...", "INFO")
                self.recommendations_ready.emit(file_analysis_results)
                return
            
        except Exception as e:
            error_msg = f"Erreur lors du traitement: {str(e)}"
            self.log_message.emit(error_msg, "ERROR")
            self.error_occurred.emit(error_msg)
            logger.exception("Erreur dans ProcessingThread")
    
    def _do_final_processing(self):
        """Effectue le traitement final avec les semaines confirmées"""
        try:
            # Simulation de progression pendant le traitement backend
            progress_steps = [55, 60, 65, 70, 75, 80, 85]
            messages = {
                55: "Initialisation du traitement...",
                60: "Extraction du texte des PDF...",
                65: "Validation des données...",
                70: "Analyse du contenu...",
                75: "Préparation des données...",
                80: "Enrichissement avec IA..." if self.enrich_llm else "Traitement des données...",
                85: "Traitement des fichiers individuels..."
            }
            
            for i, progress in enumerate(progress_steps):
                import time
                time.sleep(0.1)
                
                message = messages.get(progress, "Traitement en cours...")
                self.log_message.emit(message, "INFO")
                
                self.progress_updated.emit(progress)
            
            # Appel réel du backend avec les semaines confirmées et callback de progression
            import asyncio
            
            def progress_callback(progress_info):
                """Callback pour recevoir les informations de progression détaillée"""
                message = progress_info['message']
                
                self.log_message.emit(message, "INFO")
                
                # Calculer et émettre la progression générale
                current = progress_info['current_file'] 
                total = progress_info['total_files']
                progress_percent = int(85 + (10 * current / total))  # De 85% à 95%
                self.progress_updated.emit(progress_percent)
            
            # Préparer les informations d'exclusion
            exclusions = {}
            if hasattr(self, 'confirmed_recommendations') and self.confirmed_recommendations:
                for filename, rec in self.confirmed_recommendations.items():
                    exclusions[filename] = {
                        'matelas_excluded': rec.get('matelas_excluded', False),
                        'sommier_excluded': rec.get('sommier_excluded', False)
                    }
                # Log de débogage pour les exclusions
                self.log_message.emit(f"DEBUG Exclusions préparées: {exclusions}", "INFO")
            
            result = asyncio.run(backend_interface.process_pdf_files(
                self.files, self.enrich_llm, self.llm_provider, 
                self.openrouter_api_key, self.semaine_prod, 
                self.annee_prod, self.commande_client,
                semaine_matelas=self.semaine_matelas,
                annee_matelas=self.annee_matelas,
                semaine_sommiers=self.semaine_sommiers,
                annee_sommiers=self.annee_sommiers,
                exclusions=exclusions,
                progress_callback=progress_callback
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
            error_msg = f"Erreur lors du traitement final: {str(e)}"
            self.log_message.emit(error_msg, "ERROR")
            self.error_occurred.emit(error_msg)
            logger.exception("Erreur dans _do_final_processing")

    def continue_processing(self, confirmed_recommendations):
        """Continue le traitement avec les recommandations confirmées par l'utilisateur"""
        try:
            self.log_message.emit("Traitement final avec les semaines confirmées...", "INFO")
            self.progress_updated.emit(50)
            
            # Stocker les informations d'exclusion et les semaines
            self.confirmed_recommendations = confirmed_recommendations
            
            # Mettre à jour les semaines selon les recommandations confirmées
            # Pour l'instant, on utilise les valeurs du premier fichier comme référence globale
            if confirmed_recommendations:
                first_file = list(confirmed_recommendations.keys())[0]
                first_rec = confirmed_recommendations[first_file]
                self.semaine_matelas = first_rec['semaine_matelas']
                self.annee_matelas = first_rec['annee_matelas']
                self.semaine_sommiers = first_rec['semaine_sommiers']
                self.annee_sommiers = first_rec['annee_sommiers']
            
            # Effectuer le traitement final
            self._do_final_processing()
            
        except Exception as e:
            error_msg = f"Erreur lors de la continuation du traitement: {str(e)}"
            self.log_message.emit(error_msg, "ERROR")
            self.error_occurred.emit(error_msg)
            logger.exception("Erreur dans continue_processing")


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
        # Utiliser un répertoire local au lieu du home utilisateur
        if hasattr(sys, '_MEIPASS'):  # PyInstaller
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(__file__)
        self.eula_accepted_file = os.path.join(base_dir, '.matelas_eula_accepted')
        
        # Initialiser le logging avancé
        if ADVANCED_LOGGING_AVAILABLE:
            self.advanced_logger = advanced_logger
            self.advanced_logger.app_logger.info("Application Matelas initialisée")
        else:
            self.advanced_logger = None
        
        # Initialiser le système d'alertes en temps réel
        if ALERT_SYSTEM_AVAILABLE:
            self.alert_system = RealTimeAlertSystem(self)
            self.alert_panel = None
            self.alert_notification_dialogs = []
        else:
            self.alert_system = None
            self.alert_panel = None
        
        # Initialiser les optimisations UI
        if UI_OPTIMIZATIONS_AVAILABLE:
            try:
                self.ui_enhancements = MatelasAppEnhancements(self)
                self.file_validator = file_validator
                print("✅ Améliorations UI initialisées")
            except Exception as e:
                print(f"⚠️ Erreur initialisation UI optimizations: {e}")
                self.ui_enhancements = None
                self.file_validator = None
        else:
            self.ui_enhancements = None
            self.file_validator = None
        
        # Logger spécifique pour l'application
        try:
            self.app_logger = logging.getLogger("LiterieApp")
            self.app_logger.info("Initialisation de l'application LiterieApp")
        except Exception as e:
            print(f"Erreur lors de l'initialisation du logger: {e}")
            self.app_logger = None
        
        try:
            self.check_eula_acceptance()
            self.init_ui()
            
            # Timer pour mettre à jour la barre de statut (démarré après init complète)
            self.status_timer = QTimer()
            self.status_timer.timeout.connect(self.update_status_bar)
            
            # Initialiser le système d'alertes si disponible
            if self.alert_system:
                self.setup_alert_system()
            
            # Appliquer les améliorations UI après l'initialisation complète
            if self.ui_enhancements:
                try:
                    self.ui_enhancements.apply_all_enhancements()
                    if self.app_logger:
                        self.app_logger.info("Améliorations UI appliquées avec succès")
                except Exception as e:
                    print(f"⚠️ Erreur application améliorations UI: {e}")
                    if self.app_logger:
                        self.app_logger.warning(f"Améliorations UI partielles: {e}")
            
            # Initialiser le système de mise à jour automatique
            if AUTO_UPDATE_AVAILABLE:
                try:
                    current_version = get_version()
                    self.auto_updater = AutoUpdater(
                        server_url=config.get_server_url(),  # URL configurable depuis la config
                        current_version=current_version
                    )
                    self.auto_updater.update_available.connect(self.on_update_available)
                    
                    # Vérifier les mises à jour au démarrage (après 5 secondes)
                    QTimer.singleShot(5000, lambda: self.auto_updater.check_for_updates(silent=True))
                    
                    if self.app_logger:
                        self.app_logger.info(f"Système de mise à jour initialisé (version {current_version})")
                    print("✅ Système de mise à jour automatique initialisé")
                except Exception as e:
                    print(f"⚠️ Erreur initialisation auto-updater: {e}")
                    self.auto_updater = None
            else:
                self.auto_updater = None
            
            # Démarrer le timer de statut après init complète
            self.status_timer.start(1000)  # Mise à jour toutes les secondes
            
            if self.app_logger:
                self.app_logger.info("Application initialisée avec succès")
        except Exception as e:
            print(f"Erreur lors de l'initialisation de l'interface: {e}")
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'initialisation: {e}")
            raise
    
    def open_results_folder(self):
        """Ouvre le dossier contenant les fichiers Excel générés"""
        try:
            import os
            import subprocess
            import platform
            from pathlib import Path
            from config import Config
            
            # Obtenir le dossier de sortie Excel configuré
            try:
                config = Config()
                excel_dir = config.get_excel_output_directory()
                results_folder = Path(excel_dir)
            except:
                # Fallback vers dossier par défaut
                results_folder = Path("resultats_excel")
            
            # Créer le dossier s'il n'existe pas
            results_folder.mkdir(exist_ok=True)
            
            # Ouvrir le dossier selon l'OS
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", str(results_folder)])
            elif platform.system() == "Windows":
                os.startfile(str(results_folder))
            else:  # Linux
                subprocess.Popen(["xdg-open", str(results_folder)])
                
            print(f"📁 Dossier Excel ouvert: {results_folder.absolute()}")
            
            # Compter les fichiers Excel
            try:
                excel_files = [f for f in results_folder.glob("*.xlsx")]
                print(f"📊 {len(excel_files)} fichier(s) Excel trouvé(s)")
            except:
                pass
            
        except Exception as e:
            print(f"❌ Erreur ouverture dossier: {e}")
            # Fallback: afficher le chemin et créer un dossier basique
            from PyQt6.QtWidgets import QMessageBox
            fallback_folder = Path("resultats_excel")
            fallback_folder.mkdir(exist_ok=True)
            QMessageBox.information(self, "Dossier de résultats", 
                                  f"Dossier de résultats:\n{fallback_folder.absolute()}\n\n" +
                                  f"Le dossier a été créé et peut être ouvert manuellement.")

    def open_html_report(self):
        """Ouvre ou génère le rapport HTML complet"""
        try:
            from pathlib import Path
            import webbrowser
            from PyQt6.QtWidgets import QMessageBox
            
            # Générer le rapport HTML (même sans résultats)
            html_content = self.generate_html_report()
            
            # Vérifier si le contenu HTML est valide
            if not html_content or len(html_content) < 200:
                QMessageBox.warning(self, "Erreur", "Erreur lors de la génération du rapport HTML.")
                return
            
            # Sauvegarder le rapport
            report_file = Path("rapport_complet.html")
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Vérifier si le fichier a été correctement créé
            if not report_file.exists() or report_file.stat().st_size < 200:
                QMessageBox.warning(self, "Erreur", "Le fichier HTML n'a pas été correctement créé.")
                return
            
            # Ouvrir dans le navigateur
            webbrowser.open(f"file://{report_file.absolute()}")
            print(f"📊 Rapport HTML généré: {report_file.absolute()} ({report_file.stat().st_size} octets)")
            
            # Message d'information si pas de résultats
            if not hasattr(self, 'all_results') or not self.all_results:
                QMessageBox.information(self, "Rapport généré", "Rapport généré avec succès.\n\nNote: Aucun résultat d'analyse disponible.\nTraitez des fichiers PDF pour voir des données.")
            
        except Exception as e:
            print(f"❌ Erreur génération rapport: {e}")
            import traceback
            traceback.print_exc()
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erreur", f"Impossible de générer le rapport:\n{e}")

    def export_analysis_data(self):
        """Exporte les données d'analyse en différents formats"""
        try:
            from PyQt6.QtWidgets import QFileDialog, QMessageBox
            import json
            from pathlib import Path
            
            # Vérifier s'il y a des données à exporter
            if not hasattr(self, 'all_results') or not self.all_results:
                QMessageBox.information(self, "Export", "Aucune donnée à exporter.\nTraitez d'abord des fichiers PDF.")
                return
            
            # Demander le format d'export
            formats = {
                "JSON (*.json)": "json",
                "CSV (*.csv)": "csv", 
                "Texte (*.txt)": "txt"
            }
            
            file_path, selected_filter = QFileDialog.getSaveFileName(
                self, "Exporter les données", "analyse_matelas", 
                ";;".join(formats.keys())
            )
            
            if not file_path:
                return
                
            export_format = formats[selected_filter]
            
            # Préparer les données
            from datetime import datetime
            export_data = {
                "timestamp": str(datetime.now()),
                "nombre_fichiers": len(self.all_results),
                "resultats": self.all_results,
                "configurations": getattr(self, 'all_configurations', []),
                "configurations_sommiers": getattr(self, 'all_configurations_sommiers', [])
            }
            
            # Exporter selon le format
            if export_format == "json":
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
            elif export_format == "csv":
                self.export_to_csv(file_path, export_data)
            elif export_format == "txt":
                self.export_to_txt(file_path, export_data)
            
            print(f"💾 Données exportées: {file_path}")
            QMessageBox.information(self, "Export", f"Données exportées avec succès:\n{file_path}")
            
        except Exception as e:
            print(f"❌ Erreur export: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Erreur", f"Impossible d'exporter les données:\n{e}")

    def generate_html_report(self):
        """Génère le contenu HTML du rapport complet"""
        try:
            from datetime import datetime
            
            # S'assurer que les attributs existent
            all_results = getattr(self, 'all_results', [])
            all_configurations = getattr(self, 'all_configurations', [])
            all_configurations_sommiers = getattr(self, 'all_configurations_sommiers', [])
            
            html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Rapport d'Analyse - Literie Processor</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }}
        .result {{ background: white; margin: 10px 0; padding: 15px; border-left: 4px solid #667eea; border-radius: 4px; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 20px; }}
        .stat-card {{ background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #667eea; }}
        .no-data {{ background: white; padding: 20px; border-radius: 8px; text-align: center; color: #666; }}
        .info-box {{ background: #e3f2fd; border-left: 4px solid #2196f3; padding: 15px; margin: 20px 0; border-radius: 4px; }}
        pre {{ background: #f8f9fa; padding: 10px; border-radius: 4px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Rapport d'Analyse Literie</h1>
        <p>Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-number">{len(all_results)}</div>
            <div>Fichiers traités</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(all_configurations)}</div>
            <div>Configurations matelas</div>
        </div>
        <div class="stat-card">
            <div class="stat-number">{len(all_configurations_sommiers)}</div>
            <div>Configurations sommiers</div>
        </div>
    </div>"""
            
            # Ajouter les résultats ou un message si vide
            if all_results:
                html += '<h2>📋 Résultats d\'analyse</h2>'
                for i, result in enumerate(all_results, 1):
                    html += f"""
    <div class="result">
        <h3>Fichier {i}: {result.get('filename', 'Inconnu')}</h3>
        <pre>{result.get('summary', 'Aucun résumé disponible')}</pre>
    </div>"""
            else:
                html += '''
    <div class="info-box">
        <h3>ℹ️ Aucune donnée disponible</h3>
        <p>Aucun fichier PDF n'a encore été traité.</p>
        <p><strong>Pour générer des données d'analyse :</strong></p>
        <ol>
            <li>Cliquez sur "Sélectionner fichiers PDF" dans l'interface</li>
            <li>Choisissez vos fichiers de devis</li>
            <li>Lancez le traitement</li>
            <li>Revenez voir ce rapport pour les résultats</li>
        </ol>
    </div>'''
            
            html += """
</body>
</html>"""
            return html
            
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            return f"""<html>
<body style="font-family: Arial, sans-serif; margin: 20px;">
    <h1 style="color: red;">❌ Erreur génération rapport</h1>
    <p><strong>Erreur:</strong> {e}</p>
    <pre style="background: #f5f5f5; padding: 10px; border-radius: 4px;">{error_details}</pre>
</body>
</html>"""

    def export_to_csv(self, file_path, data):
        """Exporte les données au format CSV"""
        import csv
        
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # En-têtes
            writer.writerow(['Fichier', 'Timestamp', 'Résumé', 'Configurations'])
            
            # Données
            for result in data['resultats']:
                writer.writerow([
                    result.get('filename', ''),
                    result.get('timestamp', ''),
                    result.get('summary', ''),
                    str(result.get('configurations', ''))
                ])

    def export_to_txt(self, file_path, data):
        """Exporte les données au format texte"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(f"RAPPORT D'ANALYSE LITERIE\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Généré le: {data['timestamp']}\n")
            f.write(f"Nombre de fichiers: {data['nombre_fichiers']}\n\n")
            
            for i, result in enumerate(data['resultats'], 1):
                f.write(f"FICHIER {i}: {result.get('filename', 'Inconnu')}\n")
                f.write(f"{'-'*30}\n")
                f.write(f"{result.get('summary', 'Aucun résumé')}\n\n")

    def get_debug_info(self):
        """Retourne les informations de debug système"""
        try:
            import platform
            from datetime import datetime
            
            # Tentative d'import psutil optionnel
            try:
                import psutil
                memory_info = f"- RAM totale: {psutil.virtual_memory().total / (1024**3):.1f} GB\n- RAM utilisée: {psutil.virtual_memory().percent}%\n- Disque libre: {psutil.disk_usage('.').free / (1024**3):.1f} GB"
            except ImportError:
                memory_info = "- Informations mémoire non disponibles (psutil manquant)"
            
            info = f"""=== INFORMATIONS DE DEBUG ===
Généré le: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

SYSTÈME:
- OS: {platform.system()} {platform.release()}
- Architecture: {platform.architecture()[0]}
- Processeur: {platform.processor() or 'Non disponible'}
- Python: {platform.python_version()}

MÉMOIRE:
{memory_info}

APPLICATION:
- Fichiers traités: {len(getattr(self, 'all_results', []))}
- Configurations: {len(getattr(self, 'all_configurations', []))}
- Provider LLM: {getattr(self, 'current_llm_provider', 'Non défini')}
- Logging avancé: {'✅' if hasattr(self, 'advanced_logger') else '❌'}

INTERFACE:
- Onglets actifs: {self.tabs.count() if hasattr(self, 'tabs') else 0}
- Monitoring: {'✅' if hasattr(self, 'metrics_timer') else '❌'}
"""
            return info
            
        except Exception as e:
            return f"Erreur génération debug: {e}"

    def update_system_metrics(self):
        """Met à jour les métriques système en temps réel"""
        try:
            import psutil
            
            # CPU (sans interval pour éviter les timeouts)
            cpu_percent = psutil.cpu_percent()
            if hasattr(self, 'cpu_label'):
                self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
            
            # Mémoire
            memory = psutil.virtual_memory()
            if hasattr(self, 'memory_label'):
                self.memory_label.setText(f"Mémoire: {memory.percent:.1f}%")
            
            # Disque
            disk = psutil.disk_usage('.')
            if hasattr(self, 'disk_label'):
                disk_percent = (disk.used / disk.total) * 100
                self.disk_label.setText(f"Disque: {disk_percent:.1f}%")
                
        except ImportError:
            # Fallback si psutil n'est pas disponible
            if hasattr(self, 'cpu_label'):
                self.cpu_label.setText("CPU: N/A")
            if hasattr(self, 'memory_label'):
                self.memory_label.setText("Mémoire: N/A") 
            if hasattr(self, 'disk_label'):
                self.disk_label.setText("Disque: N/A")
        except Exception:
            # Ignorer les autres erreurs silencieusement
            pass

    def start_metrics_timer(self):
        """Démarre le timer des métriques système"""
        try:
            if hasattr(self, 'metrics_timer') and hasattr(self, 'cpu_label'):
                self.metrics_timer.start(5000)  # Mise à jour toutes les 5 secondes
                print("✅ Timer de métriques système démarré")
        except Exception as e:
            print(f"⚠️ Impossible de démarrer le timer de métriques: {e}")

    def refresh_logs(self):
        """Actualise l'affichage des logs"""
        try:
            if hasattr(self, 'log_text'):
                # Simuler un rafraîchissement des logs
                from datetime import datetime
                timestamp = datetime.now().strftime('%H:%M:%S')
                refresh_message = f"[{timestamp}] 🔄 Logs actualisés\n"
                
                current_text = self.log_text.toPlainText()
                self.log_text.setPlainText(current_text + refresh_message)
                
                # Scroll vers le bas
                cursor = self.log_text.textCursor()
                cursor.movePosition(cursor.MoveOperation.End)
                self.log_text.setTextCursor(cursor)
                
            print("🔄 Logs actualisés")
            
        except Exception as e:
            print(f"❌ Erreur refresh_logs: {e}")
    
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle(f"Literie Processor - v{get_version()}")
        
        # Gestion automatique de la taille de fenêtre selon l'écran
        self.setup_responsive_window()
        
        # Définir l'icône de la fenêtre avec le logo
        icon_path = get_asset_path("lit-double.ico")
        if icon_path:
            self.setWindowIcon(QIcon(icon_path))
        
        # Création de la barre de menu
        self.create_menu_bar()
        
        # Ajouter la croix rouge en haut à droite
        self.create_close_button()
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QHBoxLayout(central_widget)
        
        # Splitter pour diviser l'interface
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(self.splitter)
        
        # Panneau de gauche (configuration)
        left_panel = self.create_left_panel()
        self.splitter.addWidget(left_panel)
        
        # Panneau de droite (résultats)
        right_panel = self.create_right_panel()
        self.splitter.addWidget(right_panel)
        
        # Proportions du splitter (30% gauche, 70% droite)
        self.splitter.setSizes([400, 1000])
        
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
        
        # Ajuster les éléments selon la taille initiale de la fenêtre
        QTimer.singleShot(100, self.adjust_elements_for_window_size)
    
    def create_close_button(self):
        """Crée le bouton de fermeture (croix rouge) en haut à droite"""
        try:
            # Créer un widget pour contenir le bouton
            self.close_button_widget = QWidget(self)
            self.close_button_widget.setFixedSize(30, 30)
            
            # Créer le bouton de fermeture
            self.close_button = QPushButton("✕", self.close_button_widget)
            self.close_button.setFixedSize(24, 24)
            self.close_button.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: 2px solid #c0392b;
                    border-radius: 12px;
                    font-weight: bold;
                    font-size: 16px;
                    margin: 0px;
                    text-align: center;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                    border-color: #a93226;
                }
                QPushButton:pressed {
                    background-color: #a93226;
                    border-color: #8b241a;
                }
            """)
            self.close_button.setToolTip("Fermer l'application")
            self.close_button.clicked.connect(self.confirm_quit)
            
            # Layout pour centrer le bouton
            layout = QHBoxLayout(self.close_button_widget)
            layout.setContentsMargins(0, 0, 0, 0)
            layout.addWidget(self.close_button)
            
            # Positionner le bouton en haut à droite
            self.position_close_button()
            
            # Connecter le signal de redimensionnement pour repositionner le bouton
            self.resizeEvent = self.resizeEventWithCloseButton
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la création du bouton de fermeture: {e}")
    
    def position_close_button(self):
        """Positionne le bouton de fermeture en haut à droite"""
        try:
            if hasattr(self, 'close_button_widget'):
                # Calculer la position en haut à droite
                x = self.width() - 35
                y = 5
                self.close_button_widget.move(x, y)
                self.close_button_widget.raise_()
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du positionnement du bouton: {e}")
    
    def resizeEventWithCloseButton(self, event):
        """Gère le redimensionnement avec repositionnement du bouton de fermeture"""
        try:
            # Appeler la méthode parent originale
            super().resizeEvent(event)
            
            # Repositionner le bouton de fermeture
            self.position_close_button()
            
            # Ajuster les proportions du splitter selon la taille de la fenêtre
            if hasattr(self, 'splitter'):
                # Utiliser la logique d'optimisation plein écran
                total_width = self.width()
                if total_width >= 1400:
                    # Grande fenêtre : 40% gauche, 60% droite
                    left_width = int(total_width * 0.4)
                    right_width = total_width - left_width
                elif total_width >= 1200:
                    # Fenêtre moyenne : 35% gauche, 65% droite
                    left_width = int(total_width * 0.35)
                    right_width = total_width - left_width
                else:
                    # Petite fenêtre : 30% gauche, 70% droite
                    left_width = int(total_width * 0.3)
                    right_width = total_width - left_width
                
                self.splitter.setSizes([left_width, right_width])
            
            # Ajuster dynamiquement les éléments selon la taille de la fenêtre
            self.adjust_elements_for_window_size()
            
            # Log du redimensionnement
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.debug(f"Fenêtre redimensionnée: {self.width()}x{self.height()}")
                
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du redimensionnement: {e}")
    
    def setup_responsive_window(self):
        """Configure la fenêtre pour s'adapter automatiquement à la taille de l'écran"""
        try:
            # Obtenir la taille de l'écran principal
            screen = QApplication.primaryScreen()
            screen_geometry = screen.geometry()
            screen_width = screen_geometry.width()
            screen_height = screen_geometry.height()
            
            # Calculer la taille optimale de la fenêtre (80% de l'écran)
            window_width = int(screen_width * 0.8)
            window_height = int(screen_height * 0.8)
            
            # S'assurer que la fenêtre ne soit pas trop petite
            min_width = 1200
            min_height = 700
            window_width = max(window_width, min_width)
            window_height = max(window_height, min_height)
            
            # S'assurer que la fenêtre ne dépasse pas l'écran
            window_width = min(window_width, screen_width - 100)
            window_height = min(window_height, screen_height - 100)
            
            # Centrer la fenêtre sur l'écran
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # Appliquer la géométrie
            self.setGeometry(x, y, window_width, window_height)
            
            # Configurer les propriétés de redimensionnement
            self.setMinimumSize(min_width, min_height)
            self.setMaximumSize(screen_width, screen_height)
            
            # Activer le redimensionnement
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            
            # Log des informations de taille
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Fenêtre configurée: {window_width}x{window_height} (écran: {screen_width}x{screen_height})")
            
        except Exception as e:
            # Fallback en cas d'erreur
            self.setGeometry(100, 100, 1400, 900)
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la configuration responsive: {e}")
    

    
    def adjust_elements_for_window_size(self):
        """Ajuste dynamiquement les éléments selon la taille de la fenêtre"""
        try:
            window_width = self.width()
            window_height = self.height()
            
            # OPTIMISATION PLEIN ÉCRAN : Ajuster la répartition des colonnes
            if hasattr(self, 'splitter'):
                # En plein écran, donner plus d'espace à la colonne de gauche
                if window_width >= 1400:
                    # Grande fenêtre : 40% gauche, 60% droite
                    left_ratio = 0.4
                    right_ratio = 0.6
                elif window_width >= 1200:
                    # Fenêtre moyenne : 35% gauche, 65% droite
                    left_ratio = 0.35
                    right_ratio = 0.65
                else:
                    # Petite fenêtre : 30% gauche, 70% droite
                    left_ratio = 0.3
                    right_ratio = 0.7
                
                # Appliquer les ratios au splitter
                self.splitter.setSizes([
                    int(window_width * left_ratio),
                    int(window_width * right_ratio)
                ])
            
            # Calculer les tailles de police adaptatives avec des seuils optimisés
            if window_width < 1200:
                # Très petite fenêtre : polices très petites
                title_font_size = 12
                button_font_size = 9
                label_font_size = 8
                logo_height = 50
            elif window_width < 1250:
                # Petite fenêtre (1220x800) : polices petites optimisées
                title_font_size = 13
                button_font_size = 10
                label_font_size = 9
                logo_height = 55
            elif window_width < 1400:
                # Fenêtre moyenne-petite : polices moyennes
                title_font_size = 14
                button_font_size = 11
                label_font_size = 10
                logo_height = 65
            elif window_width < 1600:
                # Fenêtre moyenne : polices standard
                title_font_size = 16
                button_font_size = 12
                label_font_size = 11
                logo_height = 80
            else:
                # Grande fenêtre : polices plus grandes
                title_font_size = 18
                button_font_size = 13
                label_font_size = 12
                logo_height = 100
            
            # Ajuster le logo
            if hasattr(self, 'logo_label'):
                logo_path = get_asset_path("lit-double.png")
                if logo_path and os.path.exists(logo_path):
                    pixmap = QPixmap(logo_path).scaledToHeight(logo_height, Qt.TransformationMode.SmoothTransformation)
                    self.logo_label.setPixmap(pixmap)
            
            # Ajuster les polices des titres
            if hasattr(self, 'title_label'):
                font = self.title_label.font()
                font.setPointSize(title_font_size)
                self.title_label.setFont(font)
            
            # Ajuster les polices des boutons
            for button_name in ['select_files_btn', 'clear_files_btn', 'process_btn']:
                if hasattr(self, button_name):
                    button = getattr(self, button_name)
                    font = button.font()
                    font.setPointSize(button_font_size)
                    button.setFont(font)
            
            # Ajuster les polices des labels
            for label_name in ['file_label', 'version_label']:
                if hasattr(self, label_name):
                    label = getattr(self, label_name)
                    font = label.font()
                    font.setPointSize(label_font_size)
                    label.setFont(font)
            
            # OPTIMISATION PLEIN ÉCRAN : Ajuster les espacements selon la taille
            if window_width >= 1400:
                # Plein écran : espacements généreux pour une meilleure lisibilité
                group_spacing = 12
                group_margins = 15
                button_height = 35
            elif window_height < 750:
                # Très petite hauteur : espacements très réduits
                group_spacing = 3
                group_margins = 3
                button_height = 25
            elif window_height < 800:
                # Petite hauteur (800px) : espacements réduits optimisés
                group_spacing = 4
                group_margins = 4
                button_height = 25
            elif window_height < 850:
                # Hauteur moyenne-petite : espacements moyens
                group_spacing = 6
                group_margins = 6
                button_height = 30
            else:
                # Hauteur normale : espacements standard
                group_spacing = 8
                group_margins = 10
                button_height = 30
            
            # Appliquer les espacements aux layouts
            if hasattr(self, 'left_panel_layout'):
                self.left_panel_layout.setSpacing(group_spacing)
                self.left_panel_layout.setContentsMargins(group_margins, group_margins, group_margins, group_margins)
            
            # Ajuster la hauteur des boutons
            for button_name in ['select_files_btn', 'clear_files_btn', 'process_btn']:
                if hasattr(self, button_name):
                    button = getattr(self, button_name)
                    button.setMinimumHeight(button_height)
                    button.setMaximumHeight(button_height + 5)
            
            # OPTIMISATION PLEIN ÉCRAN : Ajuster les polices des groupes
            if window_width >= 1400:
                group_title_font_size = 14  # Plus grand en plein écran
            elif window_width < 1250:
                group_title_font_size = 10
            else:
                group_title_font_size = 12
                
            for group in self.findChildren(QGroupBox):
                font = group.font()
                font.setPointSize(group_title_font_size)
                group.setFont(font)
            
            # OPTIMISATION PLEIN ÉCRAN : Ajuster la largeur minimale du panneau gauche
            if hasattr(self, 'left_panel'):
                if window_width >= 1400:
                    # En plein écran, permettre une largeur plus importante
                    self.left_panel.setMinimumWidth(400)
                    self.left_panel.setMaximumWidth(600)
                else:
                    # Fenêtre normale
                    self.left_panel.setMinimumWidth(300)
                    self.left_panel.setMaximumWidth(500)
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'ajustement des éléments: {e}")
    
    def create_left_panel(self):
        """Crée le panneau de configuration à gauche"""
        left_widget = QWidget()
        layout = QVBoxLayout(left_widget)
        
        # Configurer la politique de taille responsive
        left_widget.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        
        # Ajuster les marges et espacements pour une meilleure utilisation de l'espace
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Stocker les références pour les ajustements dynamiques
        self.left_panel_layout = layout
        self.left_panel = left_widget  # Stocker la référence au panneau
        
        # Affichage du logo en haut du panneau
        self.logo_label = QLabel()
        logo_path = get_asset_path("lit-double.png")
        if logo_path:
            logo_pixmap = QPixmap(logo_path).scaledToHeight(80, Qt.TransformationMode.SmoothTransformation)
        else:
            # Fallback: créer un pixmap vide
            logo_pixmap = QPixmap(80, 80)
            logo_pixmap.fill(Qt.GlobalColor.transparent)
        self.logo_label.setPixmap(logo_pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.logo_label)
        
        # Titre
        self.title_label = QLabel("Configuration")
        self.title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        # Version
        self.version_label = QLabel(f"v{get_version()}")
        self.version_label.setFont(QFont("Arial", 10))
        self.version_label.setStyleSheet("color: #666666;")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.version_label)
        
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
        
        # Groupe LLM (volet déroulant)
        self.llm_group = QGroupBox("🔽 Enrichissement LLM")
        self.llm_group.setCheckable(True)
        self.llm_group.setChecked(True)  # Ouvert par défaut
        self.llm_group.toggled.connect(self.on_llm_group_toggled)
        self.llm_layout = QVBoxLayout(self.llm_group)
        
        self.enrich_llm_checkbox = QCheckBox("Utiliser l'enrichissement LLM")
        self.enrich_llm_checkbox.setChecked(True)  # Coché par défaut
        self.llm_layout.addWidget(self.enrich_llm_checkbox)
        
        # Provider LLM
        provider_layout = QHBoxLayout()
        provider_layout.addWidget(QLabel("Provider:"))

        # Liste complète des providers disponibles
        from config import config
        all_providers = ["ollama", "openrouter", "openai", "anthropic", "gemini", "mistral"]
        provider_list = all_providers

        self.llm_provider_combo = QComboBox()
        self.llm_provider_combo.addItems(provider_list)
        self.llm_provider_combo.currentTextChanged.connect(self.on_provider_changed)
        provider_layout.addWidget(self.llm_provider_combo)

        # Bouton d'aide amélioré pour les clés API
        help_btn = QPushButton("🔑")
        help_btn.clicked.connect(lambda: self.show_api_key_help(self.llm_provider_combo.currentText()))
        help_btn.setToolTip("Aide pour obtenir une clé API")
        help_btn.setFixedSize(32, 32)
        help_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: 2px solid #2980b9;
                border-radius: 16px;
                font-weight: bold;
                font-size: 14px;
                margin: 0px;
                text-align: center;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #2980b9;
                border-color: #21618c;
                transform: scale(1.1);
            }
            QPushButton:pressed {
                background-color: #21618c;
                border-color: #1a4a6b;
            }
        """)
        
        # Layout horizontal pour le provider et le bouton d'aide
        provider_help_layout = QHBoxLayout()
        provider_help_layout.addLayout(provider_layout)
        provider_help_layout.addWidget(help_btn)
        provider_help_layout.addStretch()  # Espace flexible à droite
        
        self.llm_layout.addLayout(provider_help_layout)

        # Volet dépliant pour la clé API (masqué par défaut)
        api_key_group = QGroupBox("🔐 Clé API (cliquez pour afficher)")
        api_key_group.setCheckable(True)
        api_key_group.setChecked(False)  # Masqué par défaut
        api_key_group.setStyleSheet("""
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
        
        api_key_layout = QVBoxLayout(api_key_group)
        
        # Label et champ de clé API
        api_key_input_layout = QHBoxLayout()
        api_key_input_layout.addWidget(QLabel("Clé API:"))
        
        self.api_key_input = QLineEdit()
        self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.api_key_input.setPlaceholderText("Entrez votre clé API...")
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
                background-color: #f8f9fa;
            }
        """)
        api_key_input_layout.addWidget(self.api_key_input)
        
        # Bouton pour afficher/masquer la clé
        self.toggle_key_btn = QPushButton("👁")
        self.toggle_key_btn.setFixedSize(35, 35)
        self.toggle_key_btn.setToolTip("Afficher/Masquer la clé API")
        self.toggle_key_btn.clicked.connect(self.toggle_api_key_visibility)
        self.toggle_key_btn.setStyleSheet("""
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
                border-color: #6c7b7d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
                border-color: #5a6c7d;
            }
        """)
        api_key_input_layout.addWidget(self.toggle_key_btn)
        
        api_key_layout.addLayout(api_key_input_layout)
        
        # Connecter le changement d'état du groupe
        api_key_group.toggled.connect(self.on_api_key_group_toggled)
        
        self.llm_layout.addWidget(api_key_group)
        
        # Synchronisation avec la config globale
        current_provider = config.get_current_llm_provider()
        # S'assurer que le provider actuel est dans la liste
        if current_provider not in provider_list:
            current_provider = "ollama"  # Fallback vers Ollama
        index = self.llm_provider_combo.findText(current_provider)
        if index >= 0:
            self.llm_provider_combo.setCurrentIndex(index)
        
        # Initialiser l'affichage des champs de clé API selon le provider actuel
        self.on_provider_changed(current_provider)
        
        # Synchroniser avec la configuration centralisée des clés API
        self.sync_api_keys_from_central_config()
        
        layout.addWidget(self.llm_group)
        
        # Groupe production modernisé sans titre
        prod_group = QGroupBox()
        prod_group.setStyleSheet("""
            QGroupBox {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                margin-top: 5px;
                padding: 8px;
                background-color: #f8f9fa;
            }
        """)
        prod_layout = QVBoxLayout(prod_group)
        prod_layout.setSpacing(5)
        prod_layout.setContentsMargins(10, 8, 10, 8)
        
        # Layout horizontal pour semaine et année sur la même ligne
        date_ref_layout = QHBoxLayout()
        
        # Espace flexible pour centrer les éléments
        date_ref_layout.addStretch()
        
        # Semaine actuelle (référence)
        semaine_container = QWidget()
        semaine_layout = QVBoxLayout(semaine_container)
        semaine_layout.setSpacing(3)
        semaine_layout.setContentsMargins(0, 0, 0, 0)
        semaine_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        semaine_label = QLabel("📆 Semaine actuelle")
        semaine_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 11px;
                margin: 0px;
                padding: 0px;
            }
        """)
        semaine_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        semaine_layout.addWidget(semaine_label)
        
        # Semaine actuelle (affichage visuel uniquement)
        current_week = datetime.now().isocalendar()[1]
        self.semaine_ref_label = QLabel(f"Semaine {current_week}")
        self.semaine_ref_label.setToolTip("Semaine actuelle (non modifiable)\nLes semaines de production seront calculées automatiquement selon le contenu des commandes.")
        self.semaine_ref_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
                margin: 0px;
                color: #2c3e50;
            }
        """)
        self.semaine_ref_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        semaine_layout.addWidget(self.semaine_ref_label)
        
        date_ref_layout.addWidget(semaine_container)
        
        # Espace entre semaine et année
        date_ref_layout.addSpacing(20)
        
        # Année actuelle
        annee_container = QWidget()
        annee_layout = QVBoxLayout(annee_container)
        annee_layout.setSpacing(3)
        annee_layout.setContentsMargins(0, 0, 0, 0)
        annee_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        annee_label = QLabel("📅 Année actuelle")
        annee_label.setStyleSheet("""
            QLabel {
                font-weight: bold;
                color: #2c3e50;
                font-size: 11px;
                margin: 0px;
                padding: 0px;
            }
        """)
        annee_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        annee_layout.addWidget(annee_label)
        
        # Année actuelle (affichage visuel uniquement)
        current_year = datetime.now().year
        self.annee_ref_label = QLabel(f"Année {current_year}")
        self.annee_ref_label.setToolTip("Année actuelle (non modifiable)\nLes semaines de production seront calculées automatiquement selon le contenu des commandes.")
        self.annee_ref_label.setStyleSheet("""
            QLabel {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                background-color: #ecf0f1;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
                margin: 0px;
                color: #2c3e50;
            }
        """)
        self.annee_ref_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        annee_layout.addWidget(self.annee_ref_label)
        
        date_ref_layout.addWidget(annee_container)
        
        # Espace flexible pour centrer les éléments
        date_ref_layout.addStretch()
        
        prod_layout.addLayout(date_ref_layout)
        
        layout.addWidget(prod_group)
        
        # Groupe commande client
        cmd_group = QGroupBox("Commande client")
        self.cmd_layout = QVBoxLayout(cmd_group)
        
        layout.addWidget(cmd_group)
        
        # Stocker une référence au layout principal pour ajouter le message informatif
        self.left_panel_main_layout = layout
        
        # Boutons de traitement et test LLM
        buttons_layout = QHBoxLayout()
        
        self.process_btn = QPushButton("Traiter les fichiers")
        self.process_btn.clicked.connect(self.process_files)
        self.process_btn.setEnabled(False)
        buttons_layout.addWidget(self.process_btn)
        
        self.test_llm_btn = QPushButton("🧪 Test LLM")
        self.test_llm_btn.clicked.connect(self.show_test_llm_app)
        self.test_llm_btn.setToolTip("Ouvrir l'application de test des prompts LLM")
        self.test_llm_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: 2px solid #c0392b;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        # Bouton Test LLM caché (disponible dans le menu Paramètres)
        self.test_llm_btn.setVisible(False)  # Complètement caché
        # buttons_layout.addWidget(self.test_llm_btn)  # Commenté pour cacher complètement
        
        layout.addLayout(buttons_layout)
        
        # Barre de progression
        progress_group = QGroupBox("Progression")
        progress_layout = QVBoxLayout(progress_group)
        
        # Utiliser une barre de progression intelligente si disponible
        if UI_OPTIMIZATIONS_AVAILABLE:
            try:
                self.progress_bar = SmartProgressBar()
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Barre de progression intelligente initialisée")
            except Exception as e:
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.warning(f"Fallback vers barre de progression standard: {e}")
                self.progress_bar = QProgressBar()
        else:
            self.progress_bar = QProgressBar()
        
        self.progress_bar.setVisible(False)
        if hasattr(self.progress_bar, 'setFormat'):
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
        
        # Logo du client
        try:
            # Essayer d'abord avec un logo PNG
            logo_path = get_asset_path("logo_westelynck.png")
            if os.path.exists(logo_path):
                logo_label = QLabel()
                pixmap = QPixmap(logo_path)
                if not pixmap.isNull():
                    # Redimensionner le logo
                    scaled_pixmap = pixmap.scaled(200, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                    logo_label.setPixmap(scaled_pixmap)
                    logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    logo_label.setStyleSheet("background-color: transparent;")
                    
                    # Centrer le logo
                    logo_container = QWidget()
                    logo_layout = QHBoxLayout(logo_container)
                    logo_layout.addStretch()
                    logo_layout.addWidget(logo_label)
                    logo_layout.addStretch()
                    
                    progress_layout.addWidget(logo_container)
                    logger.info("Logo Westelynck PNG ajouté avec succès")
                else:
                    raise Exception("Impossible de charger le logo PNG")
            else:
                # Créer un logo stylisé avec du texte
                logo_label = QLabel("WESTELYNCK")
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                logo_label.setStyleSheet("""
                    QLabel {
                        background-color: #2c3e50;
                        color: white;
                        font-family: 'Arial Black', sans-serif;
                        font-size: 18px;
                        font-weight: bold;
                        padding: 10px;
                        border-radius: 8px;
                        border: 2px solid #34495e;
                    }
                """)
                logo_label.setFixedSize(200, 60)
                
                # Centrer le logo
                logo_container = QWidget()
                logo_layout = QHBoxLayout(logo_container)
                logo_layout.addStretch()
                logo_layout.addWidget(logo_label)
                logo_layout.addStretch()
                
                progress_layout.addWidget(logo_container)
                logger.info("Logo Westelynck stylisé créé avec succès")
                
        except Exception as e:
            logger.error(f"Erreur lors du chargement du logo: {e}")
            # En cas d'erreur, créer un logo simple
            try:
                logo_label = QLabel("WESTELYNCK")
                logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                logo_label.setStyleSheet("""
                    QLabel {
                        background-color: #3498db;
                        color: white;
                        font-family: Arial, sans-serif;
                        font-size: 16px;
                        font-weight: bold;
                        padding: 8px;
                        border-radius: 5px;
                    }
                """)
                logo_label.setFixedSize(180, 50)
                
                # Centrer le logo
                logo_container = QWidget()
                logo_layout = QHBoxLayout(logo_container)
                logo_layout.addStretch()
                logo_layout.addWidget(logo_label)
                logo_layout.addStretch()
                
                progress_layout.addWidget(logo_container)
                logger.info("Logo Westelynck de secours créé")
            except Exception as e2:
                logger.error(f"Impossible de créer le logo de secours: {e2}")
        
        layout.addWidget(progress_group)
        
        # Espace flexible
        layout.addStretch()
        
        # Restaurer l'état du volet LLM
        QTimer.singleShot(100, self.restore_llm_panel_state)
        
        return left_widget
    
    def create_menu_bar(self):
        menubar = self.menuBar()

    # --- Menu Fichier ---
        file_menu = menubar.addMenu('Fichier')
        ouvrir_action = QAction('📄 Ouvrir une commande…', self)
        ouvrir_action.setShortcut('Ctrl+O')
        ouvrir_action.setStatusTip('Ouvrir une commande PDF')
        ouvrir_action.triggered.connect(self.select_files)
        file_menu.addAction(ouvrir_action)
        file_menu.addSeparator()
        exporter_action = QAction('💾 Exporter…', self)
        exporter_action.setStatusTip('Exporter les résultats')
        exporter_action.triggered.connect(self.process_files)
        file_menu.addAction(exporter_action)
        
        # Action pour arrêter le traitement
        self.stop_action = QAction('⏹️ Arrêter le traitement', self)
        self.stop_action.setShortcut('Ctrl+Break')
        self.stop_action.setStatusTip('Arrêter le traitement en cours')
        self.stop_action.triggered.connect(self.stop_processing)
        self.stop_action.setEnabled(False)  # Désactivé par défaut
        file_menu.addAction(self.stop_action)
        
        file_menu.addSeparator()
        quitter_action = QAction('🚪 Quitter', self)
        quitter_action.setShortcut('Ctrl+Q')
        quitter_action.setStatusTip('Quitter l\'application')
        quitter_action.triggered.connect(self.confirm_quit)
        file_menu.addAction(quitter_action)

        # --- Menu Réglages ---
        settings_menu = menubar.addMenu('Réglages')
        general_settings_action = QAction('⚙️ Paramètres généraux', self)
        general_settings_action.setStatusTip('Configurer les paramètres généraux')
        general_settings_action.triggered.connect(self.show_general_settings_dialog)
        settings_menu.addAction(general_settings_action)
        settings_menu.addSeparator()
        api_keys_action = QAction('🔑 Gestion des clés API', self)
        api_keys_action.setStatusTip('Configurer les providers LLM et leurs clés API')
        api_keys_action.triggered.connect(self.show_api_keys_dialog)
        settings_menu.addAction(api_keys_action)
        settings_menu.addSeparator()
        
        # Configuration URL serveur
        server_url_action = QAction('🌐 Configuration Serveur', self)
        server_url_action.setStatusTip('Configurer l\'URL du serveur de mise à jour')
        server_url_action.triggered.connect(self.show_server_url_dialog)
        settings_menu.addAction(server_url_action)
        settings_menu.addSeparator()
        
        # Application de test LLM
        test_llm_action = QAction('🧪 Test LLM', self)
        test_llm_action.setShortcut('Ctrl+T')
        test_llm_action.setStatusTip('Ouvrir l\'application de test des prompts LLM')
        test_llm_action.triggered.connect(self.show_test_llm_app)
        settings_menu.addAction(test_llm_action)
        settings_menu.addSeparator()
        mapping_config_action = QAction('📊 Configuration des Mappings Excel', self)
        mapping_config_action.setStatusTip('Configurer les mappings entre champs pré-import et cellules Excel')
        mapping_config_action.triggered.connect(self.show_mapping_config_dialog)
        settings_menu.addAction(mapping_config_action)
        settings_menu.addSeparator()
        noyau_order_action = QAction('🔢 Ordre des Noyaux', self)
        noyau_order_action.setStatusTip('Configurer l\'ordre d\'affichage des noyaux de matelas')
        noyau_order_action.triggered.connect(self.show_noyau_order_dialog)
        settings_menu.addAction(noyau_order_action)
        settings_menu.addSeparator()
        user_prefs_action = QAction('👤 Préférences utilisateur…', self)
        user_prefs_action.setStatusTip('Préférences utilisateur')
        # user_prefs_action.triggered.connect(self.show_user_prefs_dialog)  # À implémenter si besoin
        settings_menu.addAction(user_prefs_action)

        # --- Menu Diagnostic ---
        diag_menu = menubar.addMenu('Diagnostic')
        preimport_action = QAction('🧩 Générer un pré-import…', self)
        preimport_action.setStatusTip('Générer un fichier de pré-import')
        preimport_action.triggered.connect(self.show_preimport_dialog)  # À implémenter si besoin
        diag_menu.addAction(preimport_action)
        diag_menu.addSeparator()
        diagnostic_action = QAction('🛠️ Diagnostic complet…', self)
        diagnostic_action.setStatusTip('Lancer un diagnostic complet')
        # diagnostic_action.triggered.connect(self.run_full_diagnostic)  # À implémenter si besoin
        diag_menu.addAction(diagnostic_action)
        diag_menu.addSeparator()
        test_action = QAction('🧪 Outils de test rapide…', self)
        test_action.setStatusTip('Accéder aux tests automatisés')
        test_action.triggered.connect(self.show_tests_dialog)
        diag_menu.addAction(test_action)
        diag_menu.addSeparator()
        mapping_action = QAction('📊 Outil de Mapping Excel', self)
        mapping_action.setStatusTip('Configurer les mappings entre champs pré-import et cellules Excel')
        mapping_action.triggered.connect(self.show_mapping_config_dialog)
        diag_menu.addAction(mapping_action)
        diag_menu.addSeparator()
        logs_action = QAction('📋 Logs et rapports…', self)
        logs_action.setStatusTip('Afficher les logs et rapports')
        # logs_action.triggered.connect(self.show_logs_dialog)  # À implémenter si besoin
        diag_menu.addAction(logs_action)
        diag_menu.addSeparator()
        
        # Générateur de packages correctifs
        package_builder_action = QAction('📦 Créer Package Correctif…', self)
        package_builder_action.setStatusTip('Créer un package de mise à jour corrective (accès développeur)')
        package_builder_action.triggered.connect(self.show_package_builder_dialog)
        diag_menu.addAction(package_builder_action)
        
        # Générateur automatique de packages
        auto_package_action = QAction('🤖 Suggestions Automatiques…', self)
        auto_package_action.setStatusTip('Analyser les modifications et suggérer des packages correctifs')
        auto_package_action.triggered.connect(self.show_auto_package_dialog)
        diag_menu.addAction(auto_package_action)
        
        # Consolidation et upload
        diag_menu.addSeparator()
        consolidation_action = QAction('📤 Consolidation & Upload VPS…', self)
        consolidation_action.setStatusTip('Regrouper et uploader les packages vers le VPS')
        consolidation_action.triggered.connect(self.show_consolidation_dialog)
        diag_menu.addAction(consolidation_action)

        # --- Menu Documentation & Aide ---
        help_menu = menubar.addMenu('Documentation & Aide')
        guide_action = QAction('📖 Guide utilisateur…', self)
        guide_action.setShortcut('F1')
        guide_action.setStatusTip('Ouvrir le guide utilisateur')
        guide_action.triggered.connect(self.show_help_guide)
        help_menu.addAction(guide_action)
        help_menu.addSeparator()
        cahier_action = QAction('📜 Cahier des charges…', self)
        cahier_action.setStatusTip('Afficher le cahier des charges')
        # cahier_action.triggered.connect(self.show_cahier_des_charges)  # À implémenter si besoin
        help_menu.addAction(cahier_action)
        changelog_action = QAction('📝 Changelog…', self)
        changelog_action.setStatusTip('Afficher l\'historique des versions')
        changelog_action.triggered.connect(self.show_changelog)
        help_menu.addAction(changelog_action)
        
        # Action de mise à jour (si disponible)
        if AUTO_UPDATE_AVAILABLE:
            update_action = QAction('🔄 Vérifier les mises à jour…', self)
            update_action.setStatusTip('Vérifier et installer les mises à jour')
            update_action.triggered.connect(self.check_for_updates_manual)
            help_menu.addAction(update_action)
        
        help_menu.addSeparator()
        doc_action = QAction('📚 Générer la documentation complète…', self)
        doc_action.setStatusTip('Générer la documentation complète')
        # doc_action.triggered.connect(self.generate_full_doc)  # À implémenter si besoin
        help_menu.addAction(doc_action)
        help_menu.addSeparator()
        about_action = QAction('❓ À propos…', self)
        about_action.setStatusTip('Informations sur l\'application')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Barre de statut avancée
        self.create_advanced_status_bar()

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
        
        # Indicateur de mise à jour (EN PREMIER pour garantir la visibilité)
        self.update_indicator_label = QLabel("🔄 Mise à jour: Vérification...")
        self.update_indicator_label.setStyleSheet("""
            QLabel {
                color: white; 
                font-weight: bold; 
                padding: 4px 8px; 
                background-color: #2E86C1;
                border: 1px solid #1B4F72;
                border-radius: 4px;
                margin: 0px 2px;
                min-width: 150px;
            }
        """)
        self.update_indicator_label.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_indicator_label.mousePressEvent = self.on_update_indicator_clicked
        status_bar.addPermanentWidget(self.update_indicator_label)
        
        # DEBUG: Vérifier que l'indicateur est bien ajouté
        print(f"🔍 DEBUG: Indicateur créé et ajouté à la barre de statut")
        print(f"🔍 DEBUG: Texte initial: {self.update_indicator_label.text()}")
        print(f"🔍 DEBUG: Visible initial: {self.update_indicator_label.isVisible()}")
        self.update_indicator_label.show()  # Force l'affichage dès la création
        
        # Provider LLM
        self.provider_status_label = QLabel()
        status_bar.addPermanentWidget(self.provider_status_label)
        
        # Indicateur d'alertes
        if ALERT_SYSTEM_AVAILABLE:
            self.alert_count_label = QLabel("Alertes: 0")
            self.alert_count_label.setStyleSheet("color: green; font-weight: bold;")
            status_bar.addPermanentWidget(self.alert_count_label)
        
        # Initialisation des statuts
        self.update_provider_status()
        self.update_internet_status()
        self.update_excel_output_status()
        
        # Démarrer la vérification des mises à jour
        self.start_update_checker()
        
        # Timer pour mettre à jour l'état de la connexion internet
        self.internet_timer = QTimer()
        self.internet_timer.timeout.connect(self.update_internet_status)
        self.internet_timer.start(30000)  # Vérifier toutes les 30 secondes
        
        return status_bar

    def show_preimport_dialog(self):
        dlg = GenerateurPreImportDialog(self)
        dlg.exec()

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
            
            if hasattr(self, 'internet_status_label') and self.internet_status_label is not None:
                self.internet_status_label.setText("🌐 Internet: Connecté")
                self.internet_status_label.setStyleSheet("color: green; font-weight: bold;")
            
        except Exception as e:
            if hasattr(self, 'internet_status_label') and self.internet_status_label is not None:
                try:
                    self.internet_status_label.setText("🌐 Internet: Déconnecté")
                    self.internet_status_label.setStyleSheet("color: red; font-weight: bold;")
                except (RuntimeError, AttributeError):
                    # Widget supprimé
                    pass
    
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
        
        # Configuration responsive
        right_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.setSpacing(8)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Titre
        title = QLabel("Résultats")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Onglets pour les résultats
        try:
            self.tabs = QTabWidget()
            layout.addWidget(self.tabs)
            
            # Onglet Résumé
            self.summary_tab = QWidget()
            self.summary_layout = QVBoxLayout(self.summary_tab)
            self.summary_text = QTextBrowser()
            self.summary_text.setOpenExternalLinks(False)
            self.summary_text.anchorClicked.connect(self.open_excel_file)
            
            # Style pour le résumé
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
            
            # Onglet Configurations
            self.config_tab = QWidget()
            self.config_layout = QVBoxLayout(self.config_tab)
            
            # Bouton pour effacer les résultats
            clear_btn = QPushButton("Effacer tous les résultats")
            clear_btn.clicked.connect(self.clear_results)
            self.config_layout.addWidget(clear_btn)
            
            # Sous-onglets pour les configurations
            self.config_subtabs = QTabWidget()
            
            # Configuration matelas
            self.matelas_config_tab = QWidget()
            matelas_layout = QVBoxLayout(self.matelas_config_tab)
            
            # Créer le tableau pour les configurations matelas
            self.matelas_config_table = QTableWidget()
            self.matelas_config_table.setAlternatingRowColors(True)
            self.matelas_config_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.matelas_config_table.verticalHeader().setVisible(False)
            matelas_layout.addWidget(self.matelas_config_table)
            
            # Texte d'information pour les matelas (comme fallback)
            self.config_text = QTextBrowser()
            self.config_text.setStyleSheet("font-family: 'Courier New', monospace; font-size: 10px;")
            self.config_text.setMaximumHeight(100)
            matelas_layout.addWidget(self.config_text)
            
            self.config_subtabs.addTab(self.matelas_config_tab, "Matelas")
            
            # Configuration sommiers
            self.sommiers_config_tab = QWidget()
            sommiers_layout = QVBoxLayout(self.sommiers_config_tab)
            
            # Créer le tableau pour les configurations sommiers
            self.sommiers_config_table = QTableWidget()
            self.sommiers_config_table.setAlternatingRowColors(True)
            self.sommiers_config_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.sommiers_config_table.verticalHeader().setVisible(False)
            sommiers_layout.addWidget(self.sommiers_config_table)
            
            # Texte d'information pour les sommiers (comme fallback)
            self.sommiers_config_text = QTextBrowser()
            self.sommiers_config_text.setStyleSheet("font-family: 'Courier New', monospace; font-size: 10px;")
            self.sommiers_config_text.setMaximumHeight(100)
            sommiers_layout.addWidget(self.sommiers_config_text)
            
            self.config_subtabs.addTab(self.sommiers_config_tab, "Sommiers")
            
            self.config_layout.addWidget(self.config_subtabs)
            self.tabs.addTab(self.config_tab, "Configurations")
            
            # Onglet Pré-import
            self.preimport_tab = QWidget()
            preimport_layout = QVBoxLayout(self.preimport_tab)
            
            # Texte d'information
            preimport_info = QLabel("📋 Données formatées pour import Excel")
            preimport_info.setStyleSheet("font-weight: bold; color: #666; padding: 5px;")
            preimport_layout.addWidget(preimport_info)
            
            # Zone de filtres pour le pré-import
            filter_frame = QFrame()
            filter_frame.setStyleSheet("""
                QFrame {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            filter_layout = QHBoxLayout(filter_frame)
            
            # Label pour les filtres
            filter_label = QLabel("🔍 Filtres :")
            filter_label.setStyleSheet("font-weight: bold; color: #495057;")
            filter_layout.addWidget(filter_label)
            
            # Checkbox pour Matelas
            self.filter_matelas = QCheckBox("Matelas")
            self.filter_matelas.setChecked(True)
            self.filter_matelas.stateChanged.connect(self.apply_preimport_filters)
            self.filter_matelas.setStyleSheet("""
                QCheckBox {
                    font-weight: bold;
                    color: #007bff;
                }
                QCheckBox::indicator:checked {
                    background-color: #007bff;
                    border: 2px solid #007bff;
                }
            """)
            filter_layout.addWidget(self.filter_matelas)
            
            # Checkbox pour Sommiers
            self.filter_sommiers = QCheckBox("Sommiers")
            self.filter_sommiers.setChecked(True)
            self.filter_sommiers.stateChanged.connect(self.apply_preimport_filters)
            self.filter_sommiers.setStyleSheet("""
                QCheckBox {
                    font-weight: bold;
                    color: #28a745;
                }
                QCheckBox::indicator:checked {
                    background-color: #28a745;
                    border: 2px solid #28a745;
                }
            """)
            filter_layout.addWidget(self.filter_sommiers)
            
            # Espaceur
            filter_layout.addStretch()
            
            # Compteur d'éléments
            self.preimport_count_label = QLabel("0 éléments")
            self.preimport_count_label.setStyleSheet("color: #6c757d; font-size: 12px;")
            filter_layout.addWidget(self.preimport_count_label)
            
            preimport_layout.addWidget(filter_frame)
            
            # Créer le tableau pour les données de pré-import
            self.preimport_table = QTableWidget()
            self.preimport_table.setAlternatingRowColors(True)
            self.preimport_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
            self.preimport_table.verticalHeader().setVisible(False)
            preimport_layout.addWidget(self.preimport_table)
            
            # Stocker les données complètes pour le filtrage
            self.all_preimport_data = []
            
            self.tabs.addTab(self.preimport_tab, "Pré-import")
            
            # Onglet Logs
            self.logs_tab = QWidget()
            logs_layout = QVBoxLayout(self.logs_tab)
            
            # Filtre pour les logs
            filter_layout = QHBoxLayout()
            
            filter_label = QLabel("Niveau des logs :")
            filter_layout.addWidget(filter_label)
            
            self.log_filter_combo = QComboBox()
            self.log_filter_combo.addItems(['TOUS', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
            self.log_filter_combo.setCurrentText('INFO')
            self.log_filter_combo.currentTextChanged.connect(self.filter_logs)
            filter_layout.addWidget(self.log_filter_combo)
            
            # Bouton pour effacer les logs
            clear_logs_btn = QPushButton("🗑️ Effacer")
            clear_logs_btn.clicked.connect(lambda: self.log_text.clear())
            filter_layout.addWidget(clear_logs_btn)
            
            # Bouton pour actualiser les logs
            refresh_logs_btn = QPushButton("🔄 Actualiser")
            refresh_logs_btn.clicked.connect(self.refresh_logs)
            filter_layout.addWidget(refresh_logs_btn)
            
            filter_layout.addStretch()
            logs_layout.addLayout(filter_layout)
            
            # Widget de logs avec scrollbar automatique
            self.log_text = QTextEdit()
            self.log_text.setReadOnly(True)
            self.log_text.setFont(QFont("Courier New", 9))
            logs_layout.addWidget(self.log_text)
            
            self.tabs.addTab(self.logs_tab, "Logs")
            
            # Onglet Debug
            debug_tab = QWidget()
            debug_layout = QVBoxLayout(debug_tab)
            
            debug_info = QTextEdit()
            debug_info.setReadOnly(True)
            debug_info.setFont(QFont("Courier New", 9))
            debug_info.setText(self.get_debug_info() if hasattr(self, 'get_debug_info') else "Informations de debug indisponibles")
            debug_layout.addWidget(debug_info)
            
            self.tabs.addTab(debug_tab, "Debug")
            
            # Onglet JSON
            json_tab = QWidget()
            json_layout = QVBoxLayout(json_tab)
            
            self.json_text = QTextEdit()
            self.json_text.setReadOnly(True)
            self.json_text.setFont(QFont("Courier New", 9))
            self.json_text.setPlainText("Aucune donnée JSON disponible")
            json_layout.addWidget(self.json_text)
            
            self.tabs.addTab(json_tab, "JSON")
            
            # Onglet Excel
            excel_tab = QWidget()
            excel_layout = QVBoxLayout(excel_tab)
            
            self.excel_text = QTextEdit()
            self.excel_text.setReadOnly(True)
            self.excel_text.setFont(QFont("Courier New", 9))
            self.excel_text.setPlainText("Aucun fichier Excel généré")
            excel_layout.addWidget(self.excel_text)
            
            self.tabs.addTab(excel_tab, "Excel")
            
            # Onglet Coûts API (si disponible)
            if COST_TRACKING_AVAILABLE:
                try:
                    self.cost_widget = CostDisplayWidget()
                    self.tabs.addTab(self.cost_widget, "💰 Coûts API")
                    print("✅ Onglet de coûts API ajouté")
                except Exception as e:
                    print(f"⚠️ Erreur création onglet coûts: {e}")
            
            # Style coloré pour les onglets
            self.apply_colored_tabs_style()
            
            # Boutons d'action en bas
            buttons_layout = QHBoxLayout()
            
            # Bouton pour ouvrir le dossier de résultats
            open_folder_btn = QPushButton("📁 Ouvrir Dossier Excel")
            open_folder_btn.clicked.connect(self.open_results_folder)
            buttons_layout.addWidget(open_folder_btn)
            
            # Bouton pour ouvrir le rapport HTML
            open_report_btn = QPushButton("📊 Voir Rapport Complet")
            open_report_btn.clicked.connect(self.open_html_report)
            buttons_layout.addWidget(open_report_btn)
            
            # Bouton pour exporter les données
            export_data_btn = QPushButton("💾 Exporter Données")
            export_data_btn.clicked.connect(self.export_analysis_data)
            buttons_layout.addWidget(export_data_btn)
            
            
            layout.addLayout(buttons_layout)
            
            # Système de monitoring avancé (si disponible)
            if ADVANCED_LOGGING_AVAILABLE:
                try:
                    # Séparateur visuel
                    separator = QFrame()
                    separator.setFrameShape(QFrame.Shape.HLine)
                    separator.setFrameShadow(QFrame.Shadow.Sunken)
                    separator.setStyleSheet("background-color: #cccccc; margin: 10px 0px;")
                    layout.addWidget(separator)
                    
                    # Titre et contrôles pour les logs avancés
                    advanced_logs_title = QLabel("📈 Monitoring Avancé")
                    advanced_logs_title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
                    advanced_logs_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    advanced_logs_title.setStyleSheet("color: #2c5282; margin: 5px 0px;")
                    layout.addWidget(advanced_logs_title)
                    
                    # Panneau de métriques en temps réel
                    metrics_widget = QWidget()
                    metrics_layout = QHBoxLayout(metrics_widget)
                    
                    # CPU et Mémoire
                    self.cpu_label = QLabel("CPU: --")
                    self.memory_label = QLabel("Mémoire: --")
                    self.disk_label = QLabel("Disque: --")
                    
                    for label in [self.cpu_label, self.memory_label, self.disk_label]:
                        label.setStyleSheet("""
                            QLabel {
                                background-color: #f8f9fa;
                                border: 1px solid #dee2e6;
                                border-radius: 4px;
                                padding: 5px 10px;
                                font-family: 'Courier New', monospace;
                                font-size: 10px;
                                color: #495057;
                            }
                        """)
                        metrics_layout.addWidget(label)
                    
                    layout.addWidget(metrics_widget)
                    
                    # Panneau des logs avancés (plus compact)
                    self.advanced_logs_text = QTextEdit()
                    self.advanced_logs_text.setReadOnly(True)
                    self.advanced_logs_text.setFont(QFont("Courier New", 8))
                    self.advanced_logs_text.setMaximumHeight(150)
                    self.advanced_logs_text.setStyleSheet("""
                        QTextEdit {
                            background-color: #f8f9fa;
                            border: 1px solid #dee2e6;
                            border-radius: 4px;
                        }
                    """)
                    layout.addWidget(self.advanced_logs_text)
                    
                    # Timer pour mettre à jour les métriques (différé pour éviter les erreurs de thread)
                    try:
                        self.metrics_timer = QTimer(self)
                        self.metrics_timer.timeout.connect(self.update_system_metrics)
                        # Démarrer le timer après un délai pour s'assurer que tout est initialisé
                        QTimer.singleShot(1000, lambda: self.start_metrics_timer())
                    except Exception as timer_error:
                        print(f"⚠️ Impossible de créer le timer de métriques: {timer_error}")
                    
                except Exception as monitor_error:
                    pass  # Ignorer les erreurs de monitoring
            
        except Exception as e:
            # Fallback silencieux
            fallback_label = QLabel("Interface en mode sécurisé")
            layout.addWidget(fallback_label)
        
        return right_widget

    def filter_logs(self):
        """Filtre les logs selon le niveau sélectionné"""
        try:
            if hasattr(self, 'log_filter_combo'):
                level_text = self.log_filter_combo.currentText()
                if level_text != 'TOUS':
                    level = getattr(logging, level_text)
                    if hasattr(self, 'log_handler'):
                        self.log_handler.setLevel(level)
                print(f"🔄 Filtrage logs: {level_text}")
        except Exception as e:
            print(f"❌ Erreur filtrage logs: {e}")
    
    def clear_logs(self):
        """Efface l'affichage des logs"""
        if hasattr(self, 'log_text'):
            self.log_text.clear()
        if hasattr(self, 'app_logger') and self.app_logger:
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
                
                # Supprimer les anciens messages informatifs du layout principal
                if hasattr(self, 'left_panel_main_layout'):
                    # Parcourir tous les widgets du layout principal
                    for i in range(self.left_panel_main_layout.count()):
                        item = self.left_panel_main_layout.itemAt(i)
                        if item.widget() is not None:
                            widget = item.widget()
                            # Vérifier si c'est un label informatif (contient "fichiers sélectionnés")
                            if isinstance(widget, QLabel) and "fichiers sélectionnés" in widget.text():
                                widget.deleteLater()
                # Créer un widget scrollable pour les commandes client
                scroll_widget = QWidget()
                scroll_layout = QVBoxLayout(scroll_widget)
                scroll_layout.setSpacing(5)
                
                # Créer un champ par fichier dans le layout scrollable
                for i, file in enumerate(self.selected_files):
                    hbox = QHBoxLayout()
                    label = QLabel(f"Commande/Client pour {os.path.basename(file)} :")
                    lineedit = QLineEdit()
                    lineedit.setPlaceholderText("Nom du client")
                    
                    # Extraire le numéro de commande du nom de fichier et pré-remplir le champ
                    filename = os.path.basename(file)
                    commande_number = extract_commande_number(filename)
                    if commande_number:
                        lineedit.setText(commande_number)
                        if hasattr(self, 'app_logger') and self.app_logger:
                            self.app_logger.info(f"Numéro de commande extrait automatiquement: {commande_number} pour {filename}")
                    
                    hbox.addWidget(label)
                    hbox.addWidget(lineedit)
                    scroll_layout.addLayout(hbox)
                    self.commande_lineedits.append(lineedit)
                
                # Créer un QScrollArea pour limiter l'affichage à 3 commandes maximum
                scroll_area = QScrollArea()
                scroll_area.setWidget(scroll_widget)
                scroll_area.setWidgetResizable(True)
                scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
                scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
                
                # Limiter la hauteur pour afficher maximum 3 commandes
                # Hauteur approximative d'une ligne : 35px + marges
                max_height = 3 * 35  # 3 lignes * 35px
                scroll_area.setMaximumHeight(max_height)
                scroll_area.setMinimumHeight(105)  # Hauteur minimale pour 3 lignes
                
                # Forcer l'affichage de l'ascenseur si nécessaire
                if len(self.selected_files) > 3:
                    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
                
                # Ajouter le scroll area au layout principal
                self.cmd_layout.addWidget(scroll_area)
                
                # Ajouter un label informatif si plus de 3 fichiers (en dehors du groupe commande client)
                if len(self.selected_files) > 3:
                    info_label = QLabel(f"📋 {len(self.selected_files)} fichiers sélectionnés - Utilisez l'ascenseur pour voir tous les champs")
                    info_label.setStyleSheet("color: #666; font-style: italic; font-size: 10px; margin-top: 5px;")
                    info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    # Ajouter le message après le groupe commande client dans le layout principal
                    self.left_panel_main_layout.addWidget(info_label)
                
                # Les recommandations de production seront calculées automatiquement lors du traitement
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
            
            # Vérifier que les widgets sont initialisés
            if not hasattr(self, 'api_key_input'):
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.warning("Widgets API non initialisés, attente de l'initialisation")
                return
            
            # Mettre à jour l'affichage des champs de clé API
            if provider in ["openrouter", "openai", "anthropic", "gemini", "mistral"]:
                # Charger la clé API correspondante depuis la configuration centralisée
                api_key = config.get_llm_api_key(provider)
                if api_key:
                    self.api_key_input.setText(api_key)
                    if hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.info(f"Clé API {provider} chargée depuis la configuration centralisée")
                else:
                    # Si pas de clé spécifique, essayer la clé OpenRouter comme fallback
                    if provider != "openrouter":
                        fallback_key = config.get_openrouter_api_key()
                        if fallback_key:
                            self.api_key_input.setText(fallback_key)
                            if hasattr(self, 'app_logger') and self.app_logger:
                                self.app_logger.info(f"Utilisation de la clé OpenRouter comme fallback pour {provider}")
                        else:
                            self.api_key_input.clear()
                            if hasattr(self, 'app_logger') and self.app_logger:
                                self.app_logger.warning(f"Aucune clé API trouvée pour {provider}")
                    else:
                        self.api_key_input.clear()
                        if hasattr(self, 'app_logger') and self.app_logger:
                            self.app_logger.warning("Aucune clé API OpenRouter trouvée")
                        
            elif provider == "ollama":
                # Vider le champ de clé API pour Ollama
                self.api_key_input.clear()
            
            # Mettre à jour la barre de statut
            self.update_provider_status()
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Provider LLM changé: {provider}")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du changement de provider: {e}")
    
    def on_api_key_group_toggled(self, checked):
        """Gère l'ouverture/fermeture du volet dépliant de la clé API"""
        try:
            if hasattr(self, 'app_logger') and self.app_logger:
                if checked:
                    self.app_logger.info("Volet clé API ouvert")
                else:
                    self.app_logger.info("Volet clé API fermé")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du changement d'état du volet clé API: {e}")
    
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
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Volet Enrichissement LLM ouvert")
            else:
                self.llm_group.setTitle("▶️ Enrichissement LLM")
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Volet Enrichissement LLM fermé")
            
            # Sauvegarder l'état
            self.save_llm_panel_state(checked)
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du basculement du volet LLM: {e}")
    
    def save_llm_panel_state(self, is_open):
        """Sauvegarde l'état du volet Enrichissement LLM"""
        try:
            from config import config
            current_config = config.get_config()
            current_config['llm_panel_open'] = is_open
            config.save_config(current_config)
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la sauvegarde de l'état du volet: {e}")
    
    def restore_llm_panel_state(self):
        """Restaure l'état du volet Enrichissement LLM"""
        try:
            from config import config
            current_config = config.get_config()
            is_open = current_config.get('llm_panel_open', True)  # Ouvert par défaut
            
            if hasattr(self, 'llm_group'):
                self.llm_group.setChecked(is_open)
                self.on_llm_group_toggled(is_open)
                
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la restauration de l'état du volet: {e}")
    
    def toggle_api_key_visibility(self):
        """Bascule l'affichage de la clé API entre visible et masquée"""
        try:
            if self.api_key_input.echoMode() == QLineEdit.EchoMode.Password:
                # Afficher la clé
                self.api_key_input.setEchoMode(QLineEdit.EchoMode.Normal)
                self.toggle_key_btn.setText("🙈")
                self.toggle_key_btn.setToolTip("Masquer la clé API")
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.debug("Clé API affichée")
            else:
                # Masquer la clé
                self.api_key_input.setEchoMode(QLineEdit.EchoMode.Password)
                self.toggle_key_btn.setText("👁")
                self.toggle_key_btn.setToolTip("Afficher la clé API")
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.debug("Clé API masquée")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors du basculement de la visibilité de la clé API: {e}")
    
    def sync_api_keys_from_central_config(self):
        """Synchronise les clés API avec la configuration centralisée"""
        try:
            current_provider = self.llm_provider_combo.currentText()
            
            # Charger la clé API depuis la configuration centralisée
            if current_provider in ["openrouter", "openai", "anthropic", "gemini", "mistral"]:
                api_key = config.get_llm_api_key(current_provider)
                if api_key and hasattr(self, 'api_key_input'):
                    self.api_key_input.setText(api_key)
                    if hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.info(f"Clé API {current_provider} synchronisée depuis la configuration centralisée")
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la synchronisation des clés API: {e}")
    
    def diagnose_api_key_issue(self, provider, api_key):
        """Diagnostique les problèmes de clé API et propose des solutions"""
        try:
            if not api_key:
                return f"Aucune clé API fournie pour {provider}"
            
            # Vérifier le format de la clé selon le provider
            if provider == "openai":
                if not api_key.startswith("sk-"):
                    return f"Format de clé OpenAI invalide. La clé doit commencer par 'sk-'. Clé actuelle: {api_key[:10]}..."
                if len(api_key) < 20:
                    return f"Clé OpenAI trop courte. Longueur actuelle: {len(api_key)} caractères"
                    
            elif provider == "anthropic":
                if not api_key.startswith("sk-ant-"):
                    return f"Format de clé Anthropic invalide. La clé doit commencer par 'sk-ant-'. Clé actuelle: {api_key[:10]}..."
                    
            elif provider == "gemini":
                if not api_key.startswith("AIza"):
                    return f"Format de clé Gemini invalide. La clé doit commencer par 'AIza'. Clé actuelle: {api_key[:10]}..."
                    
            elif provider == "mistral":
                if not api_key.startswith("mist-"):
                    return f"Format de clé Mistral invalide. La clé doit commencer par 'mist-'. Clé actuelle: {api_key[:10]}..."
                    
            elif provider == "openrouter":
                if not api_key.startswith("sk-or-"):
                    return f"Format de clé OpenRouter invalide. La clé doit commencer par 'sk-or-'. Clé actuelle: {api_key[:10]}..."
            
            # Tester la connexion
            from backend.llm_provider import llm_manager
            llm_manager.set_provider(provider, api_key)
            
            if llm_manager.test_connection():
                return f"Clé API {provider} valide et connexion réussie"
            else:
                return f"Clé API {provider} format correct mais connexion échouée. Vérifiez votre quota ou l'état du service"
                
        except Exception as e:
            return f"Erreur lors du diagnostic de la clé {provider}: {str(e)}"
    
    def show_api_key_help(self, provider):
        """Affiche l'aide pour obtenir une clé API"""
        help_text = {
            "openai": """
🔑 <b>Comment obtenir une clé API OpenAI :</b>

1. Allez sur <a href="https://platform.openai.com/api-keys">https://platform.openai.com/api-keys</a>
2. Connectez-vous à votre compte OpenAI
3. Cliquez sur "Create new secret key"
4. Copiez la clé (elle commence par 'sk-')
5. Collez-la dans l'interface de gestion des providers

⚠️ <b>Important :</b> Gardez votre clé secrète et ne la partagez jamais
            """,
            "anthropic": """
🔑 <b>Comment obtenir une clé API Anthropic :</b>

1. Allez sur <a href="https://console.anthropic.com/">https://console.anthropic.com/</a>
2. Connectez-vous à votre compte Anthropic
3. Allez dans "API Keys"
4. Cliquez sur "Create Key"
5. Copiez la clé (elle commence par 'sk-ant-')
6. Collez-la dans l'interface de gestion des providers
            """,
            "gemini": """
🔑 <b>Comment obtenir une clé API Google Gemini :</b>

1. Allez sur <a href="https://makersuite.google.com/app/apikey">https://makersuite.google.com/app/apikey</a>
2. Connectez-vous avec votre compte Google
3. Cliquez sur "Create API Key"
4. Copiez la clé (elle commence par 'AIza')
5. Collez-la dans l'interface de gestion des providers
            """,
            "mistral": """
🔑 <b>Comment obtenir une clé API Mistral :</b>

1. Allez sur <a href="https://console.mistral.ai/api-keys/">https://console.mistral.ai/api-keys/</a>
2. Connectez-vous à votre compte Mistral
3. Cliquez sur "Create new key"
4. Copiez la clé (elle commence par 'mist-')
5. Collez-la dans l'interface de gestion des providers
            """,
            "openrouter": """
🔑 <b>Comment obtenir une clé API OpenRouter :</b>

1. Allez sur <a href="https://openrouter.ai/keys">https://openrouter.ai/keys</a>
2. Connectez-vous à votre compte OpenRouter
3. Cliquez sur "Create API Key"
4. Copiez la clé (elle commence par 'sk-or-')
5. Collez-la dans l'interface de gestion des providers
            """
        }
        
        if provider in help_text:
            QMessageBox.information(self, f"Aide - Clé API {provider}", help_text[provider])
        else:
            QMessageBox.information(self, "Aide", f"Consultez la documentation officielle de {provider} pour obtenir une clé API")
    
    def process_files(self):
        """Traite les fichiers sélectionnés"""
        try:
            if not self.selected_files:
                QMessageBox.warning(self, "Attention", "Aucun fichier sélectionné")
                return
            
            # Validation améliorée des fichiers
            if self.file_validator and UI_OPTIMIZATIONS_AVAILABLE:
                try:
                    validation_results = self.file_validator.validate_multiple_files(self.selected_files)
                    validation_summary = self.file_validator.get_validation_summary(validation_results)
                    
                    if self.app_logger:
                        self.app_logger.info(
                            f"Validation: {validation_summary['valid_files']}/{validation_summary['total_files']} "
                            f"fichiers valides ({validation_summary['total_size_mb']:.1f} MB total)"
                        )
                    
                    # Vérifier s'il y a des fichiers invalides
                    invalid_files = []
                    for file_path, result in zip(self.selected_files, validation_results):
                        if not result.is_valid:
                            invalid_files.append(f"• {os.path.basename(file_path)}: {'; '.join(result.errors)}")
                    
                    if invalid_files:
                        error_msg = "Fichiers invalides détectés:\\n" + "\\n".join(invalid_files)
                        QMessageBox.warning(self, "Fichiers invalides", error_msg)
                        return
                    
                except Exception as e:
                    if self.app_logger:
                        self.app_logger.warning(f"Erreur validation avancée, utilisation validation basique: {e}")
                    # Fallback vers validation basique
                    for file_path in self.selected_files:
                        if not os.path.exists(file_path):
                            raise FileNotFoundError(f"Fichier introuvable: {file_path}")
                        if not file_path.lower().endswith('.pdf'):
                            raise ValueError(f"Fichier non PDF: {file_path}")
            else:
                # Validation basique
                for file_path in self.selected_files:
                    if not os.path.exists(file_path):
                        raise FileNotFoundError(f"Fichier introuvable: {file_path}")
                    if not file_path.lower().endswith('.pdf'):
                        raise ValueError(f"Fichier non PDF: {file_path}")
            
            # Récupération des paramètres
            enrich_llm = self.enrich_llm_checkbox.isChecked()
            llm_provider = self.llm_provider_combo.currentText()
            
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Configuration LLM: Provider={llm_provider}, Enrichissement={'Activé' if enrich_llm else 'Désactivé'}")
            
            # Récupérer la clé API selon le provider
            api_key = None
            if llm_provider in ["openrouter", "openai", "anthropic", "gemini", "mistral"]:
                # Essayer d'abord depuis l'interface
                api_key = self.api_key_input.text().strip()
                
                # Si pas de clé dans l'interface, essayer depuis la configuration centralisée
                if not api_key:
                    api_key = config.get_llm_api_key(llm_provider)
                    if api_key and hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.info(f"Clé API {llm_provider} récupérée depuis la configuration centralisée")
                
                # Si toujours pas de clé, essayer OpenRouter comme fallback
                if not api_key and llm_provider != "openrouter":
                    api_key = config.get_openrouter_api_key()
                    if api_key and hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.info(f"Utilisation de la clé OpenRouter comme fallback pour {llm_provider}")
                        
            elif llm_provider == "ollama":
                api_key = None  # Ollama ne nécessite pas de clé API
            
            # Pour la compatibilité avec l'ancien code, garder openrouter_api_key
            openrouter_api_key = api_key
            
            if hasattr(self, 'app_logger') and self.app_logger:
                if api_key:
                    self.app_logger.info(f"Clé API trouvée pour {llm_provider}")
                else:
                    self.app_logger.warning(f"Aucune clé API trouvée pour {llm_provider}")
            
            # Récupérer les paramètres de référence (semaine et année actuelles)
            from datetime import datetime
            semaine_ref = datetime.now().isocalendar()[1]
            annee_ref = datetime.now().year
            
            # Pour la compatibilité avec l'ancien code, utiliser les valeurs actuelles
            semaine_prod = semaine_ref
            annee_prod = annee_ref
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
                
                # Sauvegarder la clé API selon le provider
                if llm_provider in ["openrouter", "openai", "anthropic", "gemini", "mistral"] and openrouter_api_key:
                    if llm_provider == "openrouter":
                        config.set_openrouter_api_key(openrouter_api_key)
                    else:
                        config.set_llm_api_key(llm_provider, openrouter_api_key)
                
                # Sauvegarder la commande client si disponible
                if hasattr(self, 'commande_input') and self.commande_input:
                    config.set_last_commande_client(self.commande_input.text())
                
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Configuration sauvegardée")
            except Exception as e:
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.warning(f"Erreur lors de la sauvegarde de la configuration: {e}")
            
            # Validation LLM
            if llm_provider in ["openrouter", "openai", "anthropic", "gemini", "mistral"]:
                if not openrouter_api_key:
                    provider_names = {
                        "openrouter": "OpenRouter",
                        "openai": "OpenAI",
                        "anthropic": "Anthropic", 
                        "gemini": "Gemini",
                        "mistral": "Mistral"
                    }
                    raise ValueError(f"Clé API {provider_names.get(llm_provider, llm_provider)} requise")
                
                # Nettoyer la clé API
                openrouter_api_key = openrouter_api_key.strip()
                
                # Validation du format selon le provider
                if llm_provider == "openrouter" and not openrouter_api_key.startswith("sk-or-"):
                    raise ValueError("Format de clé API OpenRouter invalide (doit commencer par 'sk-or-')")
                elif llm_provider == "openai" and not openrouter_api_key.startswith("sk-"):
                    raise ValueError("Format de clé API OpenAI invalide (doit commencer par 'sk-')")
                elif llm_provider == "anthropic" and not openrouter_api_key.startswith("sk-ant-"):
                    raise ValueError("Format de clé API Anthropic invalide (doit commencer par 'sk-ant-')")
                elif llm_provider == "gemini" and not openrouter_api_key.startswith("AIza"):
                    raise ValueError("Format de clé API Gemini invalide (doit commencer par 'AIza')")
                elif llm_provider == "mistral" and not openrouter_api_key.startswith("mist-"):
                    raise ValueError("Format de clé API Mistral invalide (doit commencer par 'mist-')")
            
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
            
            # Debug: vérifier les conditions du dialogue optimisé
            if self.app_logger:
                self.app_logger.info(f"UI_OPTIMIZATIONS_AVAILABLE: {UI_OPTIMIZATIONS_AVAILABLE}")
                self.app_logger.info(f"ui_enhancements: {self.ui_enhancements is not None}")
            
            # Dialogue optimisé temporairement désactivé - retour au système standard qui fonctionne
            if self.app_logger:
                self.app_logger.info("Utilisation du système de traitement standard (fiable)")
            
            # Création et lancement du thread de traitement standard
            self.processing_thread = ProcessingThread(
                self.selected_files, enrich_llm, llm_provider, openrouter_api_key,
                semaine_prod, annee_prod, commande_client
            )
            
            # Alerte de début de traitement
            if self.alert_system and ALERT_SYSTEM_AVAILABLE:
                self.add_processing_alert(
                    "Début du traitement",
                    f"Démarrage du traitement de {len(self.selected_files)} fichier(s) avec {llm_provider}",
                    None,  # Utilise la valeur par défaut
                    "Interface"
                )
            self.processing_thread.progress_updated.connect(self.on_progress_updated)
            self.processing_thread.result_ready.connect(self.display_results)
            self.processing_thread.error_occurred.connect(self.handle_error)
            self.processing_thread.log_message.connect(self.log_message_to_text_browser)
            self.processing_thread.recommendations_ready.connect(self.show_production_recommendations)
            self.processing_thread.noyau_alerts_ready.connect(self.show_noyau_alerts)
            self.processing_thread.finished.connect(self.on_processing_finished)
            
            self.processing_thread.start()
            
            # Activer l'action d'arrêt
            if hasattr(self, 'stop_action'):
                self.stop_action.setEnabled(True)
            
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
                configs_sommiers = len(result.get('configurations_sommiers', []))
                preimport = len(result.get('pre_import', []))
                excel = len(result.get('fichiers_excel', []))
                exclusions = result.get('exclusion_messages', [])
                
                summary += f"<p><strong>{i}. {filename}</strong><br>"
                summary += f"   Statut: {status}<br>"
                summary += f"   Configurations matelas: {configs}<br>"
                summary += f"   Configurations sommiers: {configs_sommiers}<br>"
                summary += f"   Pré-import: {preimport}<br>"
                summary += f"   Excel: {excel}<br>"
                
                # Afficher les exclusions s'il y en a
                if exclusions:
                    summary += f"   🚫 <span style='color: #e74c3c;'><strong>Exclusions:</strong> {'; '.join(exclusions)}</span><br>"
                
                summary += "</p>"
            
            # Ajouter les liens hypertextes dans l'onglet Résumé
            if self.all_excel_files:
                # Dédupliquer la liste des fichiers Excel pour éviter les doublons
                unique_excel_files = list(set(self.all_excel_files))
                unique_excel_files.sort()  # Trier pour un affichage cohérent
                
                summary += "<h4>📁 Fichiers Excel générés:</h4>"
                for fichier in unique_excel_files:
                    # Créer un lien cliquable avec gestion spéciale pour Windows
                    file_path = os.path.abspath(fichier)
                    if os.path.exists(file_path):
                        # Utiliser le chemin direct sans préfixe file:// pour une meilleure compatibilité
                        import platform
                        if platform.system() == "Windows":
                            # Sur Windows, utiliser le chemin direct avec des backslashes
                            link_path = file_path.replace('/', '\\')
                        else:
                            # Sur macOS/Linux, utiliser le chemin direct
                            link_path = file_path
                        
                        summary += f"<p>🔗 <a href='{link_path}'>{os.path.basename(fichier)}</a></p>"
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
                if hasattr(self, 'json_text'):
                    self.json_text.setText(json_text)
            except Exception as e:
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.error(f"Erreur lors de la sérialisation JSON: {e}")
                if hasattr(self, 'json_text'):
                    self.json_text.setText("Erreur lors de la sérialisation JSON")
            
            # Onglet Fichiers Excel
            if self.all_excel_files:
                # Dédupliquer la liste des fichiers Excel pour éviter les doublons
                unique_excel_files = list(set(self.all_excel_files))
                unique_excel_files.sort()  # Trier pour un affichage cohérent
                
                excel_info = f"Fichiers Excel générés ({len(unique_excel_files)} uniques):\n\n"
                for fichier in unique_excel_files:
                    excel_info += f"✅ {fichier}\n"
            else:
                excel_info = "Aucun fichier Excel généré"
            if hasattr(self, 'excel_text'):
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
            
            # Gestion des différents formats d'URL
            if file_path.startswith('file://'):
                # Enlever le préfixe 'file://' et gérer les caractères spéciaux
                file_path = file_path[7:]
                # Décoder les caractères spéciaux (espaces, caractères accentués, etc.)
                import urllib.parse
                file_path = urllib.parse.unquote(file_path)
            elif file_path.startswith('file:///'):
                # Format Windows avec 3 slashes
                file_path = file_path[8:]
                import urllib.parse
                file_path = urllib.parse.unquote(file_path)
            
            # Normaliser le chemin pour Windows
            import platform
            if platform.system() == "Windows":
                # Convertir les slashes forward en backslashes si nécessaire
                file_path = file_path.replace('/', '\\')
                # Gérer les chemins réseau Windows (\\serveur\partage)
                if file_path.startswith('\\\\'):
                    # C'est un chemin réseau Windows, le laisser tel quel
                    pass
                elif file_path.startswith('\\'):
                    # Chemin relatif avec backslash, le convertir en absolu
                    file_path = os.path.abspath(file_path)
            
            # Vérifier que le fichier existe
            if not os.path.exists(file_path):
                # Essayer avec différents encodages pour les caractères spéciaux
                import urllib.parse
                try:
                    # Essayer avec l'encodage système
                    decoded_path = file_path.encode('latin-1').decode('utf-8')
                    if os.path.exists(decoded_path):
                        file_path = decoded_path
                except:
                    pass
                
                if not os.path.exists(file_path):
                    # Afficher un message d'erreur détaillé
                    error_msg = f"Le fichier {os.path.basename(file_path)} n'existe pas.\n\nChemin tenté: {file_path}"
                    QMessageBox.warning(self, "Fichier non trouvé", error_msg)
                    return
            
            # Ouvrir le fichier avec l'application par défaut
            system = platform.system()
            if system == "Darwin":  # macOS
                subprocess.run(["open", file_path])
            elif system == "Windows":
                try:
                    # Méthode recommandée pour Windows
                    os.startfile(file_path)
                except Exception as e:
                    # Fallback avec subprocess si os.startfile échoue
                    try:
                        subprocess.run(["start", file_path], shell=True, check=True)
                    except subprocess.CalledProcessError:
                        # Dernier recours : essayer d'ouvrir avec Excel directement
                        try:
                            subprocess.run(["excel", file_path], shell=True)
                        except:
                            # Si tout échoue, afficher un message d'aide
                            QMessageBox.information(self, "Ouverture manuelle", 
                                f"Impossible d'ouvrir automatiquement le fichier.\n\n"
                                f"Veuillez ouvrir manuellement :\n{file_path}")
                            return
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
            # Stocker les données complètes pour le filtrage
            self.all_preimport_data = preimport_data if preimport_data else []
            
            # Appliquer les filtres
            self.apply_preimport_filters()
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage du pré-import: {e}")
    
    def apply_preimport_filters(self):
        """Applique les filtres sur les données de pré-import"""
        try:
            # Récupérer les données complètes
            preimport_data = getattr(self, 'all_preimport_data', [])
            
            if not preimport_data:
                self.preimport_table.setRowCount(0)
                self.preimport_table.setColumnCount(0)
                if hasattr(self, 'preimport_count_label'):
                    self.preimport_count_label.setText("0 éléments")
                return
            
            # Filtrer les données selon les checkboxes
            show_matelas = getattr(self, 'filter_matelas', None) and self.filter_matelas.isChecked()
            show_sommiers = getattr(self, 'filter_sommiers', None) and self.filter_sommiers.isChecked()
            
            filtered_data = []
            for item in preimport_data:
                type_article = item.get('type_article', 'matelas')
                
                if (type_article == 'matelas' and show_matelas) or \
                   (type_article == 'sommier' and show_sommiers):
                    filtered_data.append(item)
            
            # Mettre à jour le compteur
            if hasattr(self, 'preimport_count_label'):
                total_items = len(preimport_data)
                filtered_items = len(filtered_data)
                self.preimport_count_label.setText(f"{filtered_items}/{total_items} éléments")
            
            # Headers combinés pour matelas et sommiers
            headers = ["Type", "Client", "Commande", "Semaine", "Noyau/Type", "Quantité", "Dimensions", "Hauteur", "Housse/Matériau", "Dimensions Housse", "Longueur Housse", "Poignées"]
            self.preimport_table.setColumnCount(len(headers))
            self.preimport_table.setHorizontalHeaderLabels(headers)
            
            # Afficher les données filtrées
            self.preimport_table.setRowCount(len(filtered_data))
            for i, item in enumerate(filtered_data):
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
                        
                        # Dimensions housse (colonne 9)
                        if item.get('Hmat_luxe3D_C19') == 'X':
                            dim_housse = item.get('Hmat_luxe3D_D19', '')
                        elif item.get('Hmat_polyester_C17') == 'X':
                            dim_housse = item.get('Hmat_polyester_D17', '')
                        elif item.get('Hmat_tencel_C18') == 'X':
                            dim_housse = item.get('Hmat_tencel_D18', '')
                        elif item.get('HSimple_polyester_C13') == 'X':
                            dim_housse = item.get('HSimple_polyester_D13', '')
                        elif item.get('HSimple_tencel_C14') == 'X':
                            dim_housse = item.get('HSimple_tencel_D14', '')
                        elif item.get('HSimple_autre_C15') == 'X':
                            dim_housse = item.get('HSimple_autre_D15', '')
                        else:
                            dim_housse = ''
                        self.preimport_table.setItem(i, 9, QTableWidgetItem(dim_housse))
                        
                        # Longueur housse (colonne 10)
                        longueur_housse = item.get('longueur_D24', '')
                        self.preimport_table.setItem(i, 10, QTableWidgetItem(str(longueur_housse)))
                        
                        # Poignées (colonne 11)
                        poignees = "OUI" if item.get('poignees_C20') == 'X' else "NON"
                        self.preimport_table.setItem(i, 11, QTableWidgetItem(poignees))
                    else:
                        # Matériau pour sommiers
                        materiau = item.get('Materiau_D25', '')
                        self.preimport_table.setItem(i, 8, QTableWidgetItem(materiau))
                        
                        # Colonnes vides pour sommiers
                        self.preimport_table.setItem(i, 9, QTableWidgetItem(''))
                        self.preimport_table.setItem(i, 10, QTableWidgetItem(''))
                        self.preimport_table.setItem(i, 11, QTableWidgetItem(''))
                    
                except Exception as e:
                    if hasattr(self, 'app_logger') and self.app_logger:
                        self.app_logger.error(f"Erreur lors de l'affichage du pré-import {i}: {e}")
                    # Remplir avec des valeurs par défaut en cas d'erreur
                    for j in range(12):
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
            
            # Réinitialiser les données de filtrage du pré-import
            self.all_preimport_data = []
            
            # Effacer l'affichage
            self.summary_text.clear()
            self.matelas_config_table.setRowCount(0)
            self.matelas_config_table.setColumnCount(0)
            self.sommiers_config_table.setRowCount(0)
            self.sommiers_config_table.setColumnCount(0)
            self.preimport_table.setRowCount(0)
            self.preimport_table.setColumnCount(0)
            
            # Réinitialiser le compteur de filtrage
            if hasattr(self, 'preimport_count_label'):
                self.preimport_count_label.setText("0 éléments")
            if hasattr(self, 'json_text'):
                self.json_text.clear()
            if hasattr(self, 'excel_text'):
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
            
            # Alerte d'erreur
            if self.alert_system:
                self.add_processing_alert(
                    "Erreur de traitement",
                    error_msg,
                    AlertType.ERROR,
                    "Traitement"
                )
            
            QMessageBox.critical(self, "Erreur", f"Erreur lors du traitement:\n{error_msg}")
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la gestion d'erreur: {e}")
    
    def show_production_recommendations(self, file_analysis_results):
        """Affiche le dialog de recommandations de production"""
        try:
            # Créer et afficher le dialog
            dialog = ProductionRecommendationDialog(file_analysis_results, self)
            
            # Si l'utilisateur confirme
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Récupérer les recommandations finales
                recommendations = dialog.get_recommendations()
                
                # Continuer le traitement avec les nouvelles semaines
                self.log_message_to_text_browser("Recommandations appliquées, continuation du traitement...", "INFO")
                
                # Créer un nouveau thread pour continuer le traitement
                if hasattr(self, 'processing_thread') and self.processing_thread:
                    # Le thread précédent s'est arrêté après l'analyse préliminaire
                    # On crée un nouveau thread pour la continuation
                    self.continuation_thread = ProcessingThread(
                        self.processing_thread.files,
                        self.processing_thread.enrich_llm,
                        self.processing_thread.llm_provider,
                        self.processing_thread.openrouter_api_key,
                        self.processing_thread.semaine_prod,
                        self.processing_thread.annee_prod,
                        self.processing_thread.commande_client,
                        skip_analysis=True  # Passer directement au traitement final
                    )
                    
                    # Connecter les signaux
                    self.continuation_thread.progress_updated.connect(self.on_progress_updated)
                    self.continuation_thread.result_ready.connect(self.display_results)
                    self.continuation_thread.error_occurred.connect(self.handle_error)
                    self.continuation_thread.log_message.connect(self.log_message_to_text_browser)
                    self.continuation_thread.finished.connect(self.on_processing_finished)
                    
                    # Mettre à jour les semaines selon les recommandations
                    if recommendations:
                        first_file = list(recommendations.keys())[0]
                        first_rec = recommendations[first_file]
                        self.continuation_thread.semaine_matelas = first_rec['semaine_matelas']
                        self.continuation_thread.annee_matelas = first_rec['annee_matelas']
                        self.continuation_thread.semaine_sommiers = first_rec['semaine_sommiers']
                        self.continuation_thread.annee_sommiers = first_rec['annee_sommiers']
                        
                        # IMPORTANT: Transmettre les informations d'exclusion
                        self.continuation_thread.confirmed_recommendations = recommendations
                    
                    # Lancer le thread de continuation
                    self.continuation_thread.start()
                
            else:
                # L'utilisateur a annulé
                self.log_message_to_text_browser("Recommandations annulées par l'utilisateur", "WARNING")
                # Arrêter le traitement
                if hasattr(self, 'processing_thread') and self.processing_thread:
                    self.processing_thread.terminate()
                    self.processing_thread.wait()
                
                # Réactiver les boutons
                self.process_btn.setEnabled(True)
                self.stop_action.setEnabled(False)
                self.progress_bar.setVisible(False)
                self.progress_status_label.setVisible(False)
                
        except Exception as e:
            self.log_message_to_text_browser(f"Erreur lors de l'affichage des recommandations: {str(e)}", "ERROR")
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des recommandations: {e}")
    
    def show_noyau_alerts(self, noyau_alerts):
        """Affiche le dialog d'alertes de noyaux non détectés"""
        try:
            # Créer et afficher le dialog
            dialog = NoyauAlertDialog(noyau_alerts, self)
            
            # Si l'utilisateur confirme
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Récupérer les corrections
                corrections = dialog.get_corrections()
                
                # Continuer le traitement avec les corrections
                self.log_message_to_text_browser("Corrections de noyaux appliquées, continuation du traitement...", "INFO")
                
                # Créer un nouveau thread pour continuer le traitement
                if hasattr(self, 'processing_thread') and self.processing_thread:
                    # Le thread précédent s'est arrêté après la détection des alertes
                    # On crée un nouveau thread pour la continuation
                    self.continuation_thread = ProcessingThread(
                        self.processing_thread.files,
                        self.processing_thread.enrich_llm,
                        self.processing_thread.llm_provider,
                        self.processing_thread.openrouter_api_key,
                        self.processing_thread.semaine_prod,
                        self.processing_thread.annee_prod,
                        self.processing_thread.commande_client,
                        skip_analysis=True,  # Passer directement au traitement final
                        noyau_corrections=corrections  # Passer les corrections
                    )
                    
                    # Connecter les signaux
                    self.continuation_thread.progress_updated.connect(self.on_progress_updated)
                    self.continuation_thread.result_ready.connect(self.display_results)
                    self.continuation_thread.error_occurred.connect(self.handle_error)
                    self.continuation_thread.log_message.connect(self.log_message_to_text_browser)
                    self.continuation_thread.finished.connect(self.on_processing_finished)
                    
                    # Lancer le thread de continuation
                    self.continuation_thread.start()
                
            else:
                # L'utilisateur a annulé
                self.log_message_to_text_browser("Corrections de noyaux annulées par l'utilisateur", "WARNING")
                # Arrêter le traitement
                if hasattr(self, 'processing_thread') and self.processing_thread:
                    self.processing_thread.terminate()
                    self.processing_thread.wait()
                
                # Réactiver les boutons
                self.process_btn.setEnabled(True)
                self.stop_action.setEnabled(False)
                self.progress_bar.setVisible(False)
                self.progress_status_label.setVisible(False)
                
        except Exception as e:
            self.log_message_to_text_browser(f"Erreur lors de l'affichage des alertes de noyaux: {str(e)}", "ERROR")
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des alertes de noyaux: {e}")
    
    def on_processing_finished(self):
        """Appelé quand le traitement est terminé"""
        try:
            # Vérifier si c'est juste la fin de l'analyse préliminaire
            # (pas de résultats encore, donc pas de traitement complet terminé)
            if not hasattr(self, 'all_results') or not self.all_results:
                # C'est juste la fin de l'analyse préliminaire
                # Ne pas masquer la barre de progression ni afficher d'alerte
                # La progression continuera avec le thread de continuation
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Analyse préliminaire terminée - attente confirmation utilisateur")
                return
            
            # Aller automatiquement à l'onglet Résumé si on a des résultats
            if self.all_results:
                self.tab_widget.setCurrentIndex(1)  # Index de l'onglet Résumé
            
            # C'est la fin du traitement complet
            self.progress_bar.setVisible(False)
            self.progress_status_label.setVisible(False)
            self.process_btn.setEnabled(True)
            self.stop_action.setEnabled(False)
            
            # Mise à jour du statut selon le résultat
            if self.all_results:
                self.update_status_indicator("success")
                self.statusBar().showMessage('Traitement terminé avec succès')
                
                # Alerte de succès
                if self.alert_system:
                    self.add_processing_alert(
                        "Traitement terminé",
                        f"Traitement de {len(self.selected_files)} fichier(s) terminé avec succès",
                        AlertType.SUCCESS,
                        "Traitement"
                    )
            else:
                self.update_status_indicator("warning")
                self.statusBar().showMessage('Traitement terminé sans résultats')
                
                # Alerte d'avertissement
                if self.alert_system:
                    self.add_processing_alert(
                        "Traitement terminé",
                        "Traitement terminé sans résultats",
                        AlertType.WARNING,
                        "Traitement"
                    )
            
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
                
                # Désactiver l'action d'arrêt
                if hasattr(self, 'stop_action'):
                    self.stop_action.setEnabled(False)
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de l'arrêt du traitement: {e}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'arrêt du traitement: {e}")
    
    def on_update_available(self, update_info):
        """Appelé quand une mise à jour est disponible"""
        try:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info(f"Mise à jour disponible: {update_info.latest_version}")
            
            # Afficher une notification dans la barre de statut
            self.statusBar().showMessage(
                f"🔄 Mise à jour disponible: v{update_info.latest_version}", 
                10000  # 10 secondes
            )
            
            # Afficher le dialog de mise à jour
            if hasattr(self, 'auto_updater') and self.auto_updater:
                self.auto_updater.show_update_dialog(update_info, self)
                
        except Exception as e:
            print(f"Erreur lors de l'affichage de la mise à jour: {e}")
    
    def check_for_updates_manual(self):
        """Vérification manuelle des mises à jour"""
        try:
            if not AUTO_UPDATE_AVAILABLE or not hasattr(self, 'auto_updater') or not self.auto_updater:
                QMessageBox.information(
                    self,
                    "Système de mise à jour",
                    "Le système de mise à jour automatique n'est pas disponible."
                )
                return
            
            # Afficher un message pendant la vérification
            self.statusBar().showMessage("🔍 Vérification des mises à jour...", 3000)
            
            # Vérifier les mises à jour avec gestion d'erreur
            try:
                update_info = self.auto_updater.check_for_updates(silent=False)
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "Erreur de connexion",
                    f"Impossible de vérifier les mises à jour:\n{str(e)}\n\nVérifiez votre connexion Internet."
                )
                return
            
            if update_info and update_info.available:
                # Une mise à jour est disponible, le dialog sera affiché automatiquement
                pass
            else:
                # Aucune mise à jour disponible
                QMessageBox.information(
                    self,
                    "Mise à jour",
                    f"Votre application est à jour.\n\nVersion actuelle: {get_version()}"
                )
                
        except Exception as e:
            QMessageBox.warning(
                self,
                "Erreur de mise à jour",
                f"Impossible de vérifier les mises à jour:\n{str(e)}"
            )
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur vérification mise à jour: {e}")
    
    def configure_update_settings(self):
        """Ouvre le dialog de configuration des mises à jour"""
        try:
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QSpinBox, QFormLayout, QDialogButtonBox
            
            dialog = QDialog(self)
            dialog.setWindowTitle("⚙️ Configuration des mises à jour")
            dialog.setModal(True)
            dialog.resize(400, 300)
            
            layout = QVBoxLayout(dialog)
            
            # Titre
            title = QLabel("Configuration des Mises à Jour Automatiques")
            title.setStyleSheet("font-weight: bold; font-size: 14px; margin: 10px;")
            layout.addWidget(title)
            
            # Formulaire de configuration
            form = QFormLayout()
            
            # Vérification automatique
            auto_check_cb = QCheckBox()
            if hasattr(self, 'auto_updater') and self.auto_updater:
                auto_check_cb.setChecked(self.auto_updater.config.get("auto_check", True))
            form.addRow("Vérifier automatiquement:", auto_check_cb)
            
            # Intervalle de vérification
            interval_spin = QSpinBox()
            interval_spin.setMinimum(300)  # 5 minutes minimum
            interval_spin.setMaximum(86400)  # 24 heures maximum
            interval_spin.setSuffix(" secondes")
            if hasattr(self, 'auto_updater') and self.auto_updater:
                interval_spin.setValue(self.auto_updater.config.get("check_interval", 3600))
            form.addRow("Intervalle de vérification:", interval_spin)
            
            layout.addLayout(form)
            
            # Boutons
            buttons = QDialogButtonBox(
                QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
            )
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            layout.addWidget(buttons)
            
            # Afficher le dialog
            if dialog.exec() == QDialog.DialogCode.Accepted:
                # Sauvegarder les paramètres
                if hasattr(self, 'auto_updater') and self.auto_updater:
                    self.auto_updater.set_auto_check(auto_check_cb.isChecked())
                    self.auto_updater.set_check_interval(interval_spin.value())
                    
                QMessageBox.information(self, "Configuration", "Paramètres de mise à jour sauvegardés.")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Impossible d'ouvrir la configuration: {str(e)}")
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur configuration mise à jour: {e}")
    
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
        version_info = get_version_info()
        about_text = f"""
        <h2>Literie Processor</h2>
        <p><b>Version :</b> {get_full_version()}</p>
        <p><b>Build :</b> {version_info['build_date']}</p>
        <p><b>Description :</b> Application de traitement automatisé de commandes de literie</p>
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
        <p><b>Changelog :</b> Disponible dans le menu Aide</p>
        """
        
        QMessageBox.about(self, "À propos de Literie Processor", about_text)

    def show_changelog(self):
        """Affiche le changelog de l'application"""
        try:
            from version import get_changelog
            changelog_content = get_changelog()
            
            # Créer une fenêtre dédiée pour le changelog
            from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextBrowser, QPushButton, QHBoxLayout
            from PyQt6.QtCore import Qt
            
            dialog = QDialog(self)
            dialog.setWindowTitle("📋 Changelog - Literie Processor")
            dialog.setModal(True)
            dialog.resize(900, 700)
            
            layout = QVBoxLayout(dialog)
            
            # Titre
            title_label = QLabel("📋 Historique des Versions - Literie Processor")
            title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
            layout.addWidget(title_label)
            
            # Zone de texte pour le changelog
            changelog_browser = QTextBrowser()
            changelog_browser.setOpenExternalLinks(True)
            changelog_browser.setFont(QFont("Consolas", 10))
            changelog_browser.setStyleSheet("""
                QTextBrowser {
                    background-color: #f8f9fa;
                    border: 1px solid #dee2e6;
                    border-radius: 5px;
                    padding: 10px;
                }
            """)
            
            # Convertir le markdown en HTML pour un meilleur affichage
            html_content = self.markdown_to_html_changelog(changelog_content)
            changelog_browser.setHtml(html_content)
            layout.addWidget(changelog_browser)
            
            # Boutons
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            
            close_btn = QPushButton("Fermer")
            close_btn.clicked.connect(dialog.accept)
            close_btn.setStyleSheet("""
                QPushButton {
                    background-color: #007bff;
                    color: white;
                    border: none;
                    padding: 8px 16px;
                    border-radius: 4px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #0056b3;
                }
            """)
            button_layout.addWidget(close_btn)
            
            layout.addLayout(button_layout)
            dialog.exec()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'afficher le changelog : {str(e)}")
    
    def markdown_to_html_changelog(self, markdown_text):
        """Convertit le markdown du changelog en HTML pour un affichage amélioré"""
        html = markdown_text
        
        # Titre principal
        html = html.replace("# Changelog - Matelas Processor", 
                           "<h1 style='color: #2c3e50; text-align: center; margin-bottom: 20px;'>📋 Changelog - Literie Processor</h1>")
        
        # Versions
        html = html.replace("## Version ", "<h2 style='color: #e74c3c; border-bottom: 2px solid #e74c3c; padding-bottom: 5px; margin-top: 30px;'>🚀 Version ")
        html = html.replace(" (", " <span style='color: #7f8c8d; font-size: 0.9em;'>(")
        html = html.replace(")", ")</span></h2>")
        
        # Sections avec emojis
        html = html.replace("### 🎉 Nouveautés", "<h3 style='color: #27ae60; margin-top: 20px;'>🎉 Nouveautés</h3>")
        html = html.replace("### 🔧 Améliorations", "<h3 style='color: #f39c12; margin-top: 20px;'>🔧 Améliorations</h3>")
        html = html.replace("### 🐛 Corrections", "<h3 style='color: #e74c3c; margin-top: 20px;'>🐛 Corrections</h3>")
        html = html.replace("### 📚 Documentation", "<h3 style='color: #3498db; margin-top: 20px;'>📚 Documentation</h3>")
        html = html.replace("### 🔒 Sécurité", "<h3 style='color: #9b59b6; margin-top: 20px;'>🔒 Sécurité</h3>")
        html = html.replace("### 🔧 Fonctionnalités", "<h3 style='color: #1abc9c; margin-top: 20px;'>🔧 Fonctionnalités</h3>")
        
        # Listes
        html = html.replace("- **", "<li style='margin: 5px 0;'><strong style='color: #2c3e50;'>")
        html = html.replace("** :", "</strong> :")
        html = html.replace("** : ", "</strong> : ")
        html = html.replace("**", "</strong>")
        
        # Items simples
        html = html.replace("- ", "<li style='margin: 3px 0; color: #34495e;'>")
        
        # Grouper les listes
        import re
        html = re.sub(r'<li[^>]*>.*?</li>', lambda m: f"<ul style='margin: 10px 0; padding-left: 20px;'>{m.group(0)}</ul>", html, flags=re.DOTALL)
        
        # Séparateurs
        html = html.replace("---", "<hr style='border: 1px solid #ecf0f1; margin: 30px 0;'>")
        
        # Note finale
        html = html.replace("**Note** :", "<p style='background-color: #f8f9fa; padding: 15px; border-left: 4px solid #007bff; margin-top: 20px;'><strong>Note</strong> :")
        
        # Wrapper final
        html = f"""
        <div style='font-family: "Segoe UI", Arial, sans-serif; line-height: 1.6; color: #2c3e50;'>
            {html}
        </div>
        """
        
        return html

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
    
    def start_update_checker(self):
        """Démarre le système de vérification des mises à jour"""
        try:
            # Timer pour vérifier les mises à jour périodiquement
            self.update_check_timer = QTimer(self)  # Associer le timer au parent
            self.update_check_timer.timeout.connect(self.check_for_updates_async)
            self.update_check_timer.start(300000)  # Vérifier toutes les 5 minutes
            
            # Vérification immédiate au démarrage (après un petit délai)
            QTimer.singleShot(2000, self.check_for_updates_async)
            
        except Exception as e:
            self.log_message_to_text_browser(f"Erreur lors du démarrage du vérificateur de mise à jour: {e}", "WARNING")
    
    def ensure_update_indicator_exists(self):
        """S'assurer que l'indicateur de mise à jour existe et est visible"""
        try:
            # Vérifier si l'indicateur existe et est valide
            if (hasattr(self, 'update_indicator_label') and 
                self.update_indicator_label is not None):
                # Tester si le widget Qt est toujours valide
                try:
                    _ = self.update_indicator_label.text()  # Test simple
                    return True  # L'indicateur existe et fonctionne
                except RuntimeError:
                    print("🔄 DEBUG: L'indicateur a été détruit, recréation nécessaire")
                    pass  # L'indicateur a été détruit
            
            # Recréer l'indicateur
            print("🔄 DEBUG: Recréation de l'indicateur de mise à jour")
            
            self.update_indicator_label = QLabel("🔄 Mise à jour: Vérification...")
            self.update_indicator_label.setStyleSheet("""
                QLabel {
                    color: white; 
                    font-weight: bold; 
                    padding: 4px 8px; 
                    background-color: #2E86C1;
                    border: 1px solid #1B4F72;
                    border-radius: 4px;
                    margin: 0px 2px;
                    min-width: 150px;
                }
            """)
            self.update_indicator_label.setCursor(Qt.CursorShape.PointingHandCursor)
            self.update_indicator_label.mousePressEvent = self.on_update_indicator_clicked
            
            # L'ajouter à la barre de statut
            status_bar = self.statusBar()
            status_bar.addPermanentWidget(self.update_indicator_label)
            self.update_indicator_label.show()
            
            print("✅ DEBUG: Indicateur recréé avec succès")
            return True
            
        except Exception as e:
            print(f"❌ DEBUG: Erreur lors de la recréation de l'indicateur: {e}")
            return False

    def check_for_updates_async(self):
        """Vérification asynchrone des mises à jour avec recréation automatique"""
        print("🔍 DEBUG: check_for_updates_async() démarré")
        
        try:
            # S'assurer que l'indicateur existe
            if not self.ensure_update_indicator_exists():
                print("❌ DEBUG: Impossible de créer/recréer l'indicateur")
                return
            
            print("✅ DEBUG: Indicateur disponible pour mise à jour")
                
            from backend.auto_updater import check_for_updates_with_telemetry
            
            print("🔍 DEBUG: Vérification des mises à jour en cours...")
            # Vérifier les mises à jour sur le serveur avec gestion d'erreur
            try:
                update_info = check_for_updates_with_telemetry("http://72.60.47.183")
                print(f"🔍 DEBUG: Résultat update_info: available={getattr(update_info, 'available', None)}")
            except Exception as e:
                print(f"⚠️ DEBUG: Erreur lors de la vérification des mises à jour: {e}")
                # Désactiver l'indicateur en cas d'erreur
                if hasattr(self, 'update_indicator_label') and self.update_indicator_label:
                    self.update_indicator_label.hide()
                return
            
            # Vérifier encore une fois que l'indicateur existe
            if not self.ensure_update_indicator_exists():
                print("❌ DEBUG: Indicateur détruit pendant la vérification")
                return
            
            try:
                if update_info and update_info.available:
                    # Mise à jour disponible
                    current_version = update_info.current_version or "Inconnue"
                    latest_version = update_info.latest_version
                    
                    print(f"🆕 DEBUG: Mise à jour disponible: {current_version} → {latest_version}")
                    
                    self.update_indicator_label.setText(f"🆕 MàJ: {current_version} → {latest_version}")
                    self.update_indicator_label.setStyleSheet("""
                        QLabel {
                            color: white; 
                            font-weight: bold; 
                            padding: 4px 8px; 
                            background-color: #E74C3C;
                            border: 1px solid #C0392B;
                            border-radius: 4px;
                            margin: 0px 2px;
                            min-width: 150px;
                        }
                    """)
                    self.update_indicator_label.setToolTip(f"Nouvelle version {latest_version} disponible !\\nCliquez pour installer")
                    self.update_indicator_label.show()
                    
                    # Sauvegarder les informations de mise à jour
                    self.pending_update_info = update_info
                    print("🆕 DEBUG: Indicateur rouge configuré avec succès")
                    
                else:
                    # Aucune mise à jour ou erreur
                    from version import get_version
                    current_version = get_version()
                    
                    print(f"✅ DEBUG: Aucune mise à jour - Version: {current_version}")
                    
                    self.update_indicator_label.setText(f"✅ À jour v{current_version}")
                    self.update_indicator_label.setStyleSheet("""
                        QLabel {
                            color: white; 
                            font-weight: bold; 
                            padding: 4px 8px; 
                            background-color: #27AE60;
                            border: 1px solid #1E8449;
                            border-radius: 4px;
                            margin: 0px 2px;
                            min-width: 150px;
                        }
                    """)
                    self.update_indicator_label.setToolTip("Application à jour")
                    self.update_indicator_label.show()
                    self.pending_update_info = None
                    
                    print(f"✅ DEBUG: Indicateur vert configuré avec succès")
                    
            except RuntimeError as re:
                print(f"❌ DEBUG: RuntimeError lors de la mise à jour UI: {re}")
                # Réessayer une fois avec recréation
                if self.ensure_update_indicator_exists():
                    print("🔄 DEBUG: Nouvelle tentative après recréation")
                    # Appel récursif une seule fois
                    self.check_for_updates_async()
                return
                
        except Exception as e:
            print(f"❌ DEBUG: Exception dans check_for_updates_async: {e}")
            # Créer indicateur d'erreur
            if self.ensure_update_indicator_exists():
                try:
                    self.update_indicator_label.setText("⚠️ Erreur MàJ")
                    self.update_indicator_label.setStyleSheet("""
                        QLabel {
                            color: white; 
                            font-weight: bold; 
                            padding: 4px 8px; 
                            background-color: #95A5A6;
                            border: 1px solid #7F8C8D;
                            border-radius: 4px;
                            margin: 0px 2px;
                            min-width: 150px;
                        }
                    """)
                    self.update_indicator_label.setToolTip(f"Erreur de vérification: {str(e)}")
                    self.update_indicator_label.show()
                    self.pending_update_info = None
                    print(f"⚠️ DEBUG: Indicateur d'erreur configuré")
                except Exception as e2:
                    print(f"❌ DEBUG: Erreur lors de la config d'erreur: {e2}")
    
    def on_update_indicator_clicked(self, event):
        """Gestionnaire de clic sur l'indicateur de mise à jour"""
        if hasattr(self, 'pending_update_info') and self.pending_update_info:
            # Il y a une mise à jour disponible, ouvrir le dialog de mise à jour
            self.show_update_dialog()
        else:
            # Aucune mise à jour, vérifier manuellement
            self.statusBar().showMessage("🔍 Vérification manuelle des mises à jour...", 3000)
            QTimer.singleShot(500, self.check_for_updates_async)
    
    def show_update_dialog(self):
        """Affiche le dialog de mise à jour"""
        try:
            from backend.auto_updater import TelemetryUpdateDialog
            
            if hasattr(self, 'pending_update_info') and self.pending_update_info:
                # Créer le dialogue sans paramètre parent (non supporté)
                update_dialog = TelemetryUpdateDialog(self.pending_update_info)
                
                # Définir manuellement le parent après création si nécessaire
                update_dialog.setParent(self)
                update_dialog.setModal(True)
                
                result = update_dialog.exec()
                
                if result == QDialog.DialogCode.Accepted:
                    # L'utilisateur a choisi d'installer la mise à jour
                    self.statusBar().showMessage("🔄 Installation de la mise à jour en cours...", 5000)
                    
                    # Marquer qu'une installation est en cours avec le nouveau style
                    if self.ensure_update_indicator_exists():
                        self.update_indicator_label.setText("🔄 Installation...")
                        self.update_indicator_label.setStyleSheet("""
                            QLabel {
                                color: white; 
                                font-weight: bold; 
                                padding: 4px 8px; 
                                background-color: #FF9800;
                                border: 1px solid #E65100;
                                border-radius: 4px;
                                margin: 0px 2px;
                                min-width: 150px;
                            }
                        """)
                        self.update_indicator_label.show()
                    
                else:
                    # L'utilisateur a annulé ou reporté
                    self.statusBar().showMessage("Mise à jour reportée", 2000)
            else:
                self.statusBar().showMessage("Aucune mise à jour disponible", 2000)
                
        except Exception as e:
            self.log_message_to_text_browser(f"Erreur lors de l'affichage du dialog de mise à jour: {e}", "ERROR")
            self.statusBar().showMessage("Erreur lors de la vérification des mises à jour", 3000)

    def apply_colored_tabs_style(self):
        """Applique des couleurs distinctes aux onglets avec une méthode simple et efficace"""
        try:
            # Définir les couleurs pour chaque onglet avec des couleurs vives et distinctes
            tab_colors = [
                "#E3F2FD",  # 0: Résumé - Bleu très clair
                "#F3E5F5",  # 1: Configurations - Violet très clair
                "#E8F5E8",  # 2: Pré-import - Vert très clair
                "#FFF3E0",  # 3: Logs - Orange très clair
                "#FCE4EC",  # 4: Debug - Rose très clair
                "#E0F2F1",  # 5: JSON - Turquoise très clair
                "#F1F8E9",  # 6: Excel - Vert lime très clair
                "#FFF8E1",  # 7: Coûts API - Jaune très clair
            ]

            # Couleurs de bordure correspondantes (plus foncées)
            border_colors = [
                "#2196F3",  # Bleu
                "#9C27B0",  # Violet
                "#4CAF50",  # Vert
                "#FF9800",  # Orange
                "#E91E63",  # Rose
                "#00BCD4",  # Turquoise
                "#8BC34A",  # Vert lime
                "#FFC107",  # Jaune
            ]

            # Créer un style CSS simple avec des sélecteurs de position
            simple_style = """
            QTabWidget::pane {
                border: 2px solid #CCCCCC;
                background-color: white;
                border-radius: 8px;
                margin-top: 5px;
            }
            
            QTabBar::tab {
                background-color: #F5F5F5;
                border: 2px solid #CCCCCC;
                border-bottom: none;
                border-radius: 8px 8px 0px 0px;
                min-width: 120px;
                min-height: 35px;
                padding: 12px 20px;
                margin-right: 2px;
                font-weight: bold;
                font-size: 12px;
                color: #444444;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: none;
                border-width: 3px;
                color: #222222;
                font-weight: bold;
            }
            
            QTabBar::tab:hover:!selected {
                background-color: #F0F8FF;
                color: #1976D2;
            }
            """
            
            # Ajouter les couleurs spécifiques pour les 8 premiers onglets
            for i in range(min(8, len(tab_colors))):
                simple_style += f"""
            QTabBar::tab:nth-child({i+1}) {{
                background-color: {tab_colors[i]};
                border-color: {border_colors[i]};
            }}
            
            QTabBar::tab:nth-child({i+1}):selected {{
                background-color: white;
                border-color: {border_colors[i]};
                border-bottom: 4px solid {border_colors[i]};
            }}
            
            QTabBar::tab:nth-child({i+1}):hover:!selected {{
                background-color: {self.lighten_color(tab_colors[i], 0.2)};
                border-color: {border_colors[i]};
            }}
            """

            # Appliquer le style complet
            self.tabs.setStyleSheet(simple_style)
            
            # Ajouter des emojis aux textes des onglets pour plus de distinction visuelle
            self.add_emoji_to_tabs()
            
            print("🎨 Onglets colorés appliqués avec succès!")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'application des couleurs d'onglets: {e}")
    
    def add_emoji_to_tabs(self):
        """Ajoute des emojis distinctifs aux onglets"""
        try:
            # Mapping des emojis et tooltips
            tab_emoji_mapping = [
                ("📊", "Résumé", "Vue d'ensemble des résultats de traitement"),
                ("⚙️", "Configuration", "Paramètres et réglages de l'application"), 
                ("📥", "Pré-import", "Préparation et validation des données"),
                ("📝", "Logs", "Journaux et monitoring du système"),
                ("🔧", "Debug", "Informations de débogage technique"),
                ("📋", "JSON", "Données structurées et format JSON"),
                ("📈", "Excel", "Résultats et exports Excel"),
                ("💰", "Coûts", "Suivi des coûts d'API")
            ]
            
            # Appliquer les emojis aux onglets existants
            for i in range(min(self.tabs.count(), len(tab_emoji_mapping))):
                emoji, keyword, tooltip = tab_emoji_mapping[i]
                current_text = self.tabs.tabText(i)
                
                # Vérifier si l'emoji n'est pas déjà présent
                if not current_text.startswith(emoji):
                    # Chercher le mot-clé dans le texte actuel
                    if keyword.lower() in current_text.lower():
                        new_text = f"{emoji} {current_text}"
                        self.tabs.setTabText(i, new_text)
                        self.tabs.setTabToolTip(i, tooltip)
                        print(f"  ✅ Onglet {i}: {new_text}")
            
            print(f"🎯 Emojis ajoutés à {min(self.tabs.count(), len(tab_emoji_mapping))} onglets")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'ajout des emojis: {e}")
    
    def darken_color(self, hex_color, factor):
        """Assombrir une couleur hex"""
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(max(0, int(c * (1 - factor))) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        except:
            return hex_color
    
    def lighten_color(self, hex_color, factor):
        """Éclaircir une couleur hex"""
        try:
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            lightened = tuple(min(255, int(c + (255 - c) * factor)) for c in rgb)
            return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"
        except:
            return hex_color

    def show_noyau_order_dialog(self):
        """Ouvre la fenêtre de classement des noyaux (modale drag&drop)"""
        # Récupérer l'ordre des noyaux sauvegardé
        saved_order = config.get_noyau_order()
        
        # Récupérer tous les noyaux distincts rencontrés dans les résultats
        noyaux_from_results = set()
        for result in self.all_results:
            for conf in result.get('configurations_matelas', []):
                noyau = conf.get('Noyau') or conf.get('Type')
                if noyau:
                    noyaux_from_results.add(noyau)
        
        # Combiner l'ordre sauvegardé avec les noyaux des résultats
        all_noyaux = set(saved_order) | noyaux_from_results
        
        # Si aucun noyau trouvé, proposer une liste par défaut
        if not all_noyaux:
            all_noyaux = {
                "LATEX NATUREL",
                "MOUSSE VISCO", 
                "LATEX MIXTE 7 ZONES",
                "MOUSSE RAINUREE 7 ZONES",
                "LATEX RENFORCÉ",
                "SELECT 43"
            }
        
        # Préserver l'ordre sauvegardé et ajouter les nouveaux noyaux à la fin
        ordered_noyaux = []
        
        # D'abord ajouter les noyaux dans l'ordre sauvegardé
        for noyau in saved_order:
            if noyau in all_noyaux:
                ordered_noyaux.append(noyau)
        
        # Ensuite ajouter les nouveaux noyaux qui ne sont pas dans l'ordre sauvegardé
        for noyau in all_noyaux:
            if noyau not in ordered_noyaux:
                ordered_noyaux.append(noyau)
        
        dialog = NoyauOrderDialog(ordered_noyaux, self)
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
    
    def show_package_builder_dialog(self):
        """Affiche le générateur de packages correctifs"""
        if not PACKAGE_BUILDER_AVAILABLE:
            QMessageBox.warning(
                self, 
                "Fonctionnalité non disponible", 
                "Le générateur de packages correctifs n'est pas disponible.\n"
                "Vérifiez que le module package_builder_gui.py est présent."
            )
            return
        
        try:
            # Afficher le générateur de packages avec authentification
            show_package_builder_dialog(self)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'ouverture du générateur de packages:\n{str(e)}"
            )
    
    def show_auto_package_dialog(self):
        """Affiche le générateur automatique de packages"""
        if not AUTO_PACKAGE_AVAILABLE:
            QMessageBox.warning(
                self, 
                "Fonctionnalité non disponible", 
                "Le générateur automatique de packages n'est pas disponible.\n"
                "Vérifiez que les modules auto_package_*.py sont présents."
            )
            return
        
        try:
            # Afficher l'interface de suggestions automatiques
            show_auto_package_dialog(self)
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'ouverture du générateur automatique:\n{str(e)}"
            )
    
    def show_consolidation_dialog(self):
        """Affiche le dialogue de consolidation et upload"""
        if not CONSOLIDATION_GUI:
            QMessageBox.warning(
                self, 
                "Fonctionnalité non disponible", 
                "Le système de consolidation n'est pas disponible.\n"
                "Vérifiez que PyQt6 et paramiko sont installés."
            )
            return
        
        try:
            # Afficher l'interface de consolidation
            dialog = CONSOLIDATION_GUI(self)
            dialog.exec()
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erreur",
                f"Erreur lors de l'ouverture du consolidateur:\n{str(e)}"
            )
    
    def show_server_url_dialog(self):
        """Affiche le dialogue de configuration de l'URL du serveur"""
        dialog = ServerUrlDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Redémarrer l'auto-updater avec la nouvelle URL si nécessaire
            if hasattr(self, 'auto_updater') and self.auto_updater:
                try:
                    self.auto_updater.server_url = config.get_server_url()
                    self.app_logger.info(f"URL serveur mise à jour: {config.get_server_url()}")
                except Exception as e:
                    self.app_logger.error(f"Erreur mise à jour URL serveur: {e}")
    
    def show_maintenance_dialog(self):
        """Affiche le dialogue de maintenance avec les fichiers Markdown"""
        dialog = MaintenanceDialog(self)
        dialog.exec()
    
    def show_mapping_config_dialog(self):
        """Affiche le dialogue de configuration des mappings Excel"""
        try:
            # Import du dialogue de configuration des mappings PyQt6
            from utilities.admin.mapping_config_dialog_qt import MappingConfigDialog
            dialog = MappingConfigDialog(self)
            dialog.exec()
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", f"Module de configuration des mappings non disponible: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ouverture du dialogue de configuration: {e}")

    def show_update_manager(self):
        """Affiche le gestionnaire de mises à jour (fusionné avec Administration)"""
        QMessageBox.information(self, "Information", 
                               "Le gestionnaire de mises à jour a été fusionné avec le système d'Administration.\n"
                               "Veuillez utiliser le menu Réglages → Administration pour accéder à toutes les fonctionnalités.")

    def show_admin_dialog(self):
        """Affiche le dialogue administrateur protégé par mot de passe"""
        try:
            from utilities.admin.admin_dialog import show_admin_dialog
            show_admin_dialog(self)
            # Mettre à jour l'affichage de la version après les opérations d'administration
            self.update_version_display()
        except ImportError as e:
            QMessageBox.warning(self, "Erreur", f"Module d'administration non disponible: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du lancement de l'administration: {e}")
    
    def show_test_llm_app(self):
        """Lance l'application de test LLM"""
        try:
            import subprocess
            import sys
            import os
            
            # Vérifier que le fichier existe
            test_llm_file = "test_llm_prompt.py"
            if not os.path.exists(test_llm_file):
                QMessageBox.warning(self, "Erreur", 
                    f"Fichier {test_llm_file} non trouvé.\n"
                    "Assurez-vous que l'application de test LLM est installée.")
                return
            
            # Lancer l'application de test LLM dans un processus séparé
            try:
                subprocess.Popen([sys.executable, test_llm_file], 
                               stdout=subprocess.PIPE, 
                               stderr=subprocess.PIPE)
                
                # Afficher un message de confirmation
                QMessageBox.information(self, "Test LLM", 
                    "L'application de test LLM a été lancée dans une nouvelle fenêtre.\n\n"
                    "Vous pouvez maintenant tester vos prompts, providers et modèles LLM.")
                
            except Exception as e:
                QMessageBox.warning(self, "Erreur", 
                    f"Erreur lors du lancement de l'application de test LLM:\n{str(e)}")
                
        except Exception as e:
            QMessageBox.warning(self, "Erreur", 
                f"Erreur lors de l'ouverture de l'application de test LLM:\n{str(e)}")
    
    def update_version_display(self):
        """Met à jour l'affichage de la version dans l'interface"""
        current_version = get_version()
        self.setWindowTitle(f"Literie Processor - v{current_version}")
        if hasattr(self, 'version_label'):
            self.version_label.setText(f"v{current_version}")
    
    def setup_alert_system(self):
        """Configure le système d'alertes en temps réel"""
        if not self.alert_system or not ALERT_SYSTEM_AVAILABLE:
            return
            
        try:
            from real_time_alerts import AlertType, AlertCategory
            
            # Connecter les signaux du système d'alertes
            self.alert_system.alert_added.connect(self.on_alert_added)
            self.alert_system.alert_count_changed.connect(self.on_alert_count_changed)
            
            # Le panneau d'alertes est maintenant créé dans create_right_panel
            # et intégré directement sous l'espace de visualisation
            
            # Alerte de démarrage
            self.alert_system.add_alert(
                "Système d'alertes activé",
                "Le système d'alertes en temps réel est maintenant opérationnel",
                AlertType.SUCCESS,
                AlertCategory.SYSTEM,
                "Système"
            )
            
            if self.app_logger:
                self.app_logger.info("Système d'alertes en temps réel initialisé")
                
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'initialisation du système d'alertes: {e}")
    
    def on_alert_added(self, alert):
        """Gère l'ajout d'une nouvelle alerte"""
        try:
            if not ALERT_SYSTEM_AVAILABLE:
                return
                
            from real_time_alerts import AlertType
            
            # Afficher une notification si configurée
            if alert.alert_type in [AlertType.WARNING, AlertType.ERROR, AlertType.CRITICAL]:
                self.show_alert_notification(alert)
            
            # Mettre à jour l'interface si nécessaire
            self.update_alert_display()
            
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors du traitement d'une alerte: {e}")
    
    def on_alert_count_changed(self, count):
        """Gère le changement du nombre d'alertes"""
        try:
            # Mettre à jour l'indicateur dans la barre de statut
            if hasattr(self, 'alert_count_label'):
                self.alert_count_label.setText(f"Alertes: {count}")
                if count > 0:
                    self.alert_count_label.setStyleSheet("color: red; font-weight: bold;")
                else:
                    self.alert_count_label.setStyleSheet("color: green; font-weight: bold;")
            
            # Le panneau d'alertes est maintenant intégré directement sous l'espace de visualisation
            # Pas besoin de mettre à jour le titre d'un onglet
            
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de la mise à jour du compteur d'alertes: {e}")
    
    def show_alert_notification(self, alert):
        """Affiche une notification d'alerte"""
        try:
            if not self.alert_system:
                return
                
            # Créer et afficher le dialog de notification
            notification_dialog = AlertNotificationDialog(alert, self)
            notification_dialog.show()
            
            # Garder une référence pour éviter la suppression prématurée
            self.alert_notification_dialogs.append(notification_dialog)
            
            # Nettoyer les références après fermeture
            notification_dialog.finished.connect(
                lambda: self.alert_notification_dialogs.remove(notification_dialog)
            )
            
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage de la notification: {e}")
    
    def update_alert_display(self):
        """Met à jour l'affichage des alertes"""
        try:
            if self.alert_panel:
                self.alert_panel.update_display()
                
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de la mise à jour de l'affichage des alertes: {e}")
    
    def show_alert_settings(self):
        """Affiche le dialog de configuration des alertes"""
        try:
            if not self.alert_system:
                QMessageBox.information(self, "Information", "Le système d'alertes n'est pas disponible")
                return
                
            dialog = AlertSettingsDialog(self.alert_system, self)
            dialog.exec()
            
        except Exception as e:
            if self.app_logger:
                self.app_logger.error(f"Erreur lors de l'affichage des paramètres d'alertes: {e}")
    
    def add_system_alert(self, title: str, message: str, alert_type=None):
        """Ajoute une alerte système"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.INFO
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.SYSTEM, "Système")
        return None
    
    def add_processing_alert(self, title: str, message: str, alert_type=None, source: str = ""):
        """Ajoute une alerte de traitement"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.INFO
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.PROCESSING, source)
        return None
    
    def add_validation_alert(self, title: str, message: str, alert_type=None, source: str = ""):
        """Ajoute une alerte de validation"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.WARNING
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.VALIDATION, source)
        return None
    
    def add_network_alert(self, title: str, message: str, alert_type=None):
        """Ajoute une alerte réseau"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.ERROR
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.NETWORK, "Réseau")
        return None
    
    def add_security_alert(self, title: str, message: str, alert_type=None):
        """Ajoute une alerte de sécurité"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.CRITICAL
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.SECURITY, "Sécurité")
        return None
    
    def add_production_alert(self, title: str, message: str, alert_type=None, source: str = ""):
        """Ajoute une alerte de production"""
        if self.alert_system and ALERT_SYSTEM_AVAILABLE:
            from real_time_alerts import AlertType, AlertCategory
            if alert_type is None:
                alert_type = AlertType.INFO
            return self.alert_system.add_alert(title, message, alert_type, AlertCategory.PRODUCTION, source)
        return None
    
    def confirm_quit(self):
        """Demande confirmation avant de quitter l'application"""
        try:
            # Vérifier s'il y a un traitement en cours
            if hasattr(self, 'processing_thread') and self.processing_thread and self.processing_thread.isRunning():
                reply = QMessageBox.question(
                    self, 
                    "Traitement en cours", 
                    "⚠️ Un traitement est actuellement en cours.\n\n"
                    "Êtes-vous sûr de vouloir quitter l'application ?\n"
                    "Le traitement sera interrompu.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
            
            # Vérifier s'il y a des résultats non sauvegardés
            if hasattr(self, 'all_results') and self.all_results:
                reply = QMessageBox.question(
                    self, 
                    "Résultats non sauvegardés", 
                    "📊 Des résultats de traitement sont affichés.\n\n"
                    "Êtes-vous sûr de vouloir quitter l'application ?\n"
                    "Les résultats ne seront pas sauvegardés automatiquement.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return
            
            # Demande de confirmation générale
            reply = QMessageBox.question(
                self, 
                "Confirmation de fermeture", 
                "🚪 Êtes-vous sûr de vouloir quitter l'application Literie Processor ?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                # Alerte de fermeture
                if self.alert_system:
                    self.add_system_alert(
                        "Fermeture de l'application",
                        "L'application Literie Processor se ferme...",
                        AlertType.INFO
                    )
                
                # Log de fermeture
                if hasattr(self, 'app_logger') and self.app_logger:
                    self.app_logger.info("Fermeture de l'application demandée par l'utilisateur")
                
                # Fermer l'application
                self.close()
                
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la confirmation de fermeture: {e}")
            else:
                print(f"Erreur lors de la confirmation de fermeture: {e}")
    
    def closeEvent(self, event):
        """Gère l'événement de fermeture de la fenêtre"""
        try:
            # Vérifier s'il y a un traitement en cours
            if hasattr(self, 'processing_thread') and self.processing_thread and self.processing_thread.isRunning():
                reply = QMessageBox.question(
                    self, 
                    "Traitement en cours", 
                    "⚠️ Un traitement est actuellement en cours.\n\n"
                    "Êtes-vous sûr de vouloir fermer l'application ?\n"
                    "Le traitement sera interrompu.",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    event.ignore()
                    return
            
            # Arrêter le timer de vérification des mises à jour
            if hasattr(self, 'update_check_timer') and self.update_check_timer:
                self.update_check_timer.stop()
                self.update_check_timer = None
            
            # Log de fermeture
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.info("Fermeture de l'application")
            
            # Accepter la fermeture
            event.accept()
            
        except Exception as e:
            if hasattr(self, 'app_logger') and self.app_logger:
                self.app_logger.error(f"Erreur lors de la fermeture: {e}")
            # En cas d'erreur, accepter quand même la fermeture
            event.accept()




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


class ServerUrlDialog(QDialog):
    """Dialogue pour configurer l'URL du serveur de mise à jour"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("🌐 Configuration Serveur")
        self.setModal(True)
        self.resize(500, 300)
        self.init_ui()
        self.load_current_settings()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre et description
        title = QLabel("🌐 Configuration du Serveur")
        title.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout.addWidget(title)
        
        description = QLabel(
            "Configurez l'URL du serveur de mise à jour. Cette URL sera utilisée "
            "pour vérifier les mises à jour et télécharger les nouvelles versions.\n\n"
            "Exemples d'URLs valides :\n"
            "• http://localhost:8080 (serveur local)\n"
            "• https://abc123.ngrok.io (tunnel ngrok)\n"
            "• https://monserveur.com:8080 (serveur distant)"
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #666; margin: 10px 0;")
        layout.addWidget(description)
        
        # Configuration URL serveur
        server_group = QGroupBox("URL du serveur de mise à jour")
        server_layout = QFormLayout(server_group)
        
        self.server_url_input = QLineEdit()
        self.server_url_input.setPlaceholderText("https://exemple.ngrok.io ou http://localhost:8080")
        self.server_url_input.textChanged.connect(self.validate_url)
        
        self.url_status = QLabel()
        self.url_status.setStyleSheet("font-size: 11px; margin-top: 5px;")
        
        server_layout.addRow("URL du serveur:", self.server_url_input)
        server_layout.addRow("", self.url_status)
        layout.addWidget(server_group)
        
        # Bouton de test
        self.test_btn = QPushButton("🔍 Tester la connexion")
        self.test_btn.clicked.connect(self.test_connection)
        layout.addWidget(self.test_btn)
        
        # Zone d'information
        self.info_label = QLabel()
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("color: #666; font-size: 10px; margin: 10px 0;")
        layout.addWidget(self.info_label)
        
        # Boutons de dialogue
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def validate_url(self):
        """Valide l'URL saisie"""
        url = self.server_url_input.text().strip()
        if not url:
            self.url_status.setText("")
            return
        
        if url.startswith(('http://', 'https://')):
            self.url_status.setText("✅ Format URL valide")
            self.url_status.setStyleSheet("color: green; font-size: 11px;")
        else:
            self.url_status.setText("⚠️ L'URL doit commencer par http:// ou https://")
            self.url_status.setStyleSheet("color: orange; font-size: 11px;")
    
    def test_connection(self):
        """Teste la connexion au serveur"""
        url = self.server_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une URL de serveur")
            return
        
        self.test_btn.setEnabled(False)
        self.test_btn.setText("⏳ Test en cours...")
        
        try:
            import requests
            import urllib.parse
            
            # Construire l'URL de test (endpoint racine qui existe)
            parsed_url = urllib.parse.urlparse(url)
            if not parsed_url.scheme:
                test_url = f"http://{url}/"
            else:
                test_url = f"{url}/"
            
            # Test de connexion avec timeout court
            response = requests.get(test_url, timeout=5)
            
            if response.status_code == 200:
                # Analyser la réponse pour plus d'informations
                response_info = ""
                try:
                    json_response = response.json()
                    if "message" in json_response:
                        response_info = f"\nMessage: {json_response['message']}"
                    if "status" in json_response:
                        response_info += f"\nStatut serveur: {json_response['status']}"
                except:
                    pass
                
                QMessageBox.information(
                    self, 
                    "✅ Connexion réussie", 
                    f"Le serveur répond correctement!\n\nURL testée: {test_url}\nStatut HTTP: {response.status_code}{response_info}"
                )
                self.info_label.setText(f"✅ Dernière connexion réussie: {test_url}")
            else:
                QMessageBox.warning(
                    self, 
                    "⚠️ Réponse inattendue", 
                    f"Le serveur répond mais avec un statut inattendu.\n\nURL: {test_url}\nStatut: {response.status_code}"
                )
                self.info_label.setText(f"⚠️ Réponse inattendue du serveur (statut {response.status_code})")
        
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(
                self, 
                "❌ Connexion échouée", 
                f"Impossible de se connecter au serveur.\n\nVérifiez que :\n"
                f"• Le serveur fonctionne\n"
                f"• L'URL est correcte\n"
                f"• Votre connexion Internet fonctionne\n\n"
                f"URL testée: {test_url if 'test_url' in locals() else url}"
            )
            self.info_label.setText("❌ Connexion échouée")
        
        except requests.exceptions.Timeout:
            QMessageBox.warning(
                self, 
                "⏰ Timeout", 
                "La connexion a pris trop de temps.\n\nLe serveur est peut-être surchargé ou l'URL incorrecte."
            )
            self.info_label.setText("⏰ Timeout de connexion")
        
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du test: {str(e)}")
            self.info_label.setText(f"❌ Erreur: {str(e)}")
        
        finally:
            self.test_btn.setEnabled(True)
            self.test_btn.setText("🔍 Tester la connexion")
    
    def load_current_settings(self):
        """Charge les paramètres actuels"""
        current_url = config.get_server_url()
        self.server_url_input.setText(current_url)
        self.validate_url()
        self.info_label.setText(f"URL actuelle: {current_url}")
    
    def accept(self):
        """Sauvegarde les paramètres avant fermeture"""
        try:
            url = self.server_url_input.text().strip()
            
            if url and not url.startswith(('http://', 'https://')):
                QMessageBox.warning(
                    self, 
                    "URL invalide", 
                    "L'URL doit commencer par http:// ou https://"
                )
                return
            
            # Sauvegarder la configuration
            config.set_server_url(url)
            
            QMessageBox.information(
                self, 
                "✅ Sauvegardé", 
                f"URL du serveur mise à jour avec succès!\n\nNouvelle URL: {url or '(vide - utilisation par défaut)'}"
            )
            
            super().accept()
        except Exception as e:
            QMessageBox.warning(self, "Erreur", f"Erreur lors de la sauvegarde: {e}")


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


class ProductionRecommendationDialog(QDialog):
    """Dialog pour confirmer les recommandations de production basées sur l'analyse LLM"""
    
    def __init__(self, file_analysis_results, parent=None):
        super().__init__(parent)
        self.file_analysis_results = file_analysis_results
        self.recommendations = {}
        self.excluded_items = {}  # Dict pour stocker les éléments exclus par fichier
        self.init_ui()
        
    def init_ui(self):
        """Initialise l'interface utilisateur"""
        self.setWindowTitle("Recommandations de Production")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel("Recommandations de Production")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Description
        description = QLabel("L'analyse des fichiers a détecté le contenu suivant. Vous pouvez confirmer les semaines de production recommandées et exclure les articles que vous ne souhaitez pas produire :")
        description.setWordWrap(True)
        description.setStyleSheet("color: #34495e; margin: 5px;")
        layout.addWidget(description)
        
        # Explication des boutons
        explanation = QLabel("💡 <b>Workflow des recommandations :</b><br>"
                           "1. <b>Cochez/décochez 'Exclure'</b> : Exclut les matelas/sommiers du traitement (ex: déjà en stock)<br>"
                           "2. <b>Appliquer recommandation</b> : Recalcule les recommandations optimales pour ce fichier uniquement<br>"
                           "3. <b>Appliquer toutes les recommandations</b> : Applique les recommandations optimales à tous les fichiers en une fois<br>"
                           "4. <b>Continuer le traitement</b> : Valide les recommandations et lance le traitement final des fichiers")
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
        apply_all_btn.clicked.connect(self.apply_all_recommendations)
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
        continue_btn.clicked.connect(self.accept)
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
        cancel_btn.clicked.connect(self.reject)
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
        
        # Section d'exclusion d'articles
        exclusion_layout = QHBoxLayout()
        
        # Vérifier s'il y a des matelas/sommiers
        has_matelas = analysis.get('has_matelas', False) or analysis.get('matelas_count', 0) > 0
        has_sommiers = analysis.get('has_sommiers', False) or analysis.get('sommier_count', 0) > 0
        
        # Initialize exclusion checkboxes
        matelas_exclude_checkbox = None
        sommier_exclude_checkbox = None
        
        if has_matelas or has_sommiers:
            exclusion_label = QLabel("🚫 Exclusion de production:")
            exclusion_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
            exclusion_layout.addWidget(exclusion_label)
            
            exclusion_layout.addSpacing(10)
            
            # Checkbox pour exclure les matelas
            if has_matelas:
                matelas_exclude_checkbox = QCheckBox(f"Exclure les matelas ({analysis.get('matelas_count', 0)} article(s))")
                matelas_exclude_checkbox.setToolTip("Cochez pour exclure les matelas de ce fichier du traitement (ex: déjà en stock)")
                matelas_exclude_checkbox.setStyleSheet("color: #2980b9;")
                exclusion_layout.addWidget(matelas_exclude_checkbox)
                
                exclusion_layout.addSpacing(20)
            
            # Checkbox pour exclure les sommiers
            if has_sommiers:
                sommier_exclude_checkbox = QCheckBox(f"Exclure les sommiers ({analysis.get('sommier_count', 0)} article(s))")
                sommier_exclude_checkbox.setToolTip("Cochez pour exclure les sommiers de ce fichier du traitement (ex: déjà en stock)")
                sommier_exclude_checkbox.setStyleSheet("color: #e67e22;")
                exclusion_layout.addWidget(sommier_exclude_checkbox)
            
            exclusion_layout.addStretch()
            layout.addLayout(exclusion_layout)
        
        # Recommandation
        recommendation = analysis.get('recommendation', 'Aucune recommandation')
        recommendation_label = QLabel(f"Recommandation: {recommendation}")
        recommendation_label.setStyleSheet("color: #8e44ad; font-weight: bold; padding: 5px; background-color: #f8f9fa; border-radius: 3px;")
        recommendation_label.setWordWrap(True)
        layout.addWidget(recommendation_label)
        
        # Contrôles de semaine (seulement si il y a des matelas ou sommiers)
        week_layout = QHBoxLayout()
        
        # Semaine matelas (seulement si il y a des matelas)
        if has_matelas:
            matelas_week_layout = QVBoxLayout()
            matelas_week_layout.addWidget(QLabel("Semaine matelas:"))
            
            matelas_week_spin = QSpinBox()
            matelas_week_spin.setRange(1, 53)
            matelas_week_spin.setValue(analysis.get('semaine_matelas', 1))
            matelas_week_layout.addWidget(matelas_week_spin)
            
            matelas_year_spin = QSpinBox()
            matelas_year_spin.setRange(2020, 2030)
            matelas_year_spin.setValue(analysis.get('annee_matelas', datetime.now().year))
            matelas_year_spin.setPrefix("Année: ")
            matelas_week_layout.addWidget(matelas_year_spin)
            
            week_layout.addLayout(matelas_week_layout)
            week_layout.addSpacing(20)
        else:
            matelas_week_spin = None
            matelas_year_spin = None
        
        # Semaine sommiers (seulement si il y a des sommiers)
        if has_sommiers:
            sommier_week_layout = QVBoxLayout()
            sommier_week_layout.addWidget(QLabel("Semaine sommiers:"))
            
            sommier_week_spin = QSpinBox()
            sommier_week_spin.setRange(1, 53)
            sommier_week_spin.setValue(analysis.get('semaine_sommiers', 1))
            sommier_week_layout.addWidget(sommier_week_spin)
            
            sommier_year_spin = QSpinBox()
            sommier_year_spin.setRange(2020, 2030)
            sommier_year_spin.setValue(analysis.get('annee_sommiers', datetime.now().year))
            sommier_year_spin.setPrefix("Année: ")
            sommier_week_layout.addWidget(sommier_year_spin)
            
            week_layout.addLayout(sommier_week_layout)
        else:
            sommier_week_spin = None
            sommier_year_spin = None
        
        # Si il n'y a ni matelas ni sommiers, afficher un message
        if not has_matelas and not has_sommiers:
            no_articles_label = QLabel("⚠️ Aucun matelas ou sommier détecté - Aucune recommandation de production nécessaire")
            no_articles_label.setStyleSheet("color: #e67e22; font-weight: bold; padding: 10px; background-color: #fdf2e9; border-radius: 5px; border: 1px solid #f39c12;")
            no_articles_label.setWordWrap(True)
            week_layout.addWidget(no_articles_label)
        
        # Bouton appliquer recommandation
        apply_btn = QPushButton("Appliquer recommandation")
        apply_btn.clicked.connect(lambda: self.apply_recommendation_for_file(filename, analysis))
        apply_btn.setToolTip("Recalcule et applique les recommandations optimales pour ce fichier uniquement")
        apply_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        week_layout.addWidget(apply_btn)
        
        layout.addLayout(week_layout)
        
        # Stocker les références pour accès ultérieur
        analysis['widgets'] = {
            'matelas_week': matelas_week_spin,
            'matelas_year': matelas_year_spin,
            'sommier_week': sommier_week_spin,
            'sommier_year': sommier_year_spin,
            'matelas_exclude': matelas_exclude_checkbox,
            'sommier_exclude': sommier_exclude_checkbox
        }
        
        return group
    
    def apply_recommendation_for_file(self, filename, analysis):
        """Applique la recommandation pour un fichier spécifique"""
        try:
            from backend.date_utils import calculate_production_weeks
            
            # Récupérer la semaine actuelle depuis l'analyse
            semaine_actuelle = analysis.get('semaine_actuelle', datetime.now().isocalendar()[1])
            annee_actuelle = analysis.get('annee_actuelle', datetime.now().year)
            
            # Calculer les recommandations
            recommendations = calculate_production_weeks(
                semaine_actuelle, annee_actuelle,
                analysis.get('has_matelas', False),
                analysis.get('has_sommiers', False)
            )
            
            # Appliquer aux widgets (seulement si ils existent)
            widgets = analysis['widgets']
            if widgets.get('matelas_week') and widgets.get('matelas_year'):
                widgets['matelas_week'].setValue(recommendations['matelas']['semaine'])
                widgets['matelas_year'].setValue(recommendations['matelas']['annee'])
            if widgets.get('sommier_week') and widgets.get('sommier_year'):
                widgets['sommier_week'].setValue(recommendations['sommiers']['semaine'])
                widgets['sommier_year'].setValue(recommendations['sommiers']['annee'])
            
            QMessageBox.information(self, "Recommandation appliquée", 
                                  f"Recommandation appliquée pour {os.path.basename(filename)}")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", 
                              f"Erreur lors de l'application de la recommandation: {str(e)}")
    
    def apply_all_recommendations(self):
        """Applique toutes les recommandations"""
        try:
            for filename, analysis in self.file_analysis_results.items():
                self.apply_recommendation_for_file(filename, analysis)
            
            QMessageBox.information(self, "Recommandations appliquées", 
                                  "Toutes les recommandations ont été appliquées avec succès.")
            
        except Exception as e:
            QMessageBox.warning(self, "Erreur", 
                              f"Erreur lors de l'application des recommandations: {str(e)}")
    
    def get_recommendations(self):
        """Récupère toutes les recommandations finales"""
        recommendations = {}
        
        for filename, analysis in self.file_analysis_results.items():
            widgets = analysis.get('widgets', {})
            
            # Vérifier s'il y a des matelas et sommiers
            has_matelas = analysis.get('has_matelas', False) or analysis.get('matelas_count', 0) > 0
            has_sommiers = analysis.get('has_sommiers', False) or analysis.get('sommier_count', 0) > 0
            
            # Vérifier l'état d'exclusion
            matelas_excluded = widgets.get('matelas_exclude') and widgets['matelas_exclude'].isChecked() if widgets.get('matelas_exclude') else False
            sommier_excluded = widgets.get('sommier_exclude') and widgets['sommier_exclude'].isChecked() if widgets.get('sommier_exclude') else False
            
            recommendations[filename] = {
                'semaine_matelas': widgets.get('matelas_week', QSpinBox()).value() if has_matelas and widgets.get('matelas_week') else 1,
                'annee_matelas': widgets.get('matelas_year', QSpinBox()).value() if has_matelas and widgets.get('matelas_year') else datetime.now().year,
                'semaine_sommiers': widgets.get('sommier_week', QSpinBox()).value() if has_sommiers and widgets.get('sommier_week') else 1,
                'annee_sommiers': widgets.get('sommier_year', QSpinBox()).value() if has_sommiers and widgets.get('sommier_year') else datetime.now().year,
                'matelas_excluded': matelas_excluded,
                'sommier_excluded': sommier_excluded
            }
        
        return recommendations


class NoyauAlertDialog(QDialog):
    """Dialog pour gérer les alertes de noyaux non détectés"""
    
    def __init__(self, noyau_alerts, parent=None):
        super().__init__(parent)
        self.noyau_alerts = noyau_alerts  # Liste des alertes par fichier
        self.corrections = {}  # Stockage des corrections
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
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Boutons - Organisation uniformisée avec le modal de semaine
        button_layout = QHBoxLayout()
        
        # Bouton Appliquer toutes les corrections
        apply_all_btn = QPushButton("✅ Appliquer toutes les corrections")
        apply_all_btn.clicked.connect(self.apply_all_corrections)
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
        continue_btn.clicked.connect(self.accept)
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
        cancel_btn.clicked.connect(self.reject)
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
                padding: 8px 15px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        layout.addWidget(apply_file_btn)
        
        return group
    
    def on_correction_changed(self, filename, index, correction):
        """Appelé quand une correction est sélectionnée"""
        if correction != "-- Sélectionner un noyau --":
            if filename not in self.corrections:
                self.corrections[filename] = {}
            self.corrections[filename][index] = correction
    
    def apply_file_corrections(self, filename, alerts):
        """Applique les corrections pour un fichier spécifique"""
        corrections_applied = 0
        
        for alert in alerts:
            combo = alert.get('combo')
            if combo and combo.currentText() != "-- Sélectionner un noyau --":
                if filename not in self.corrections:
                    self.corrections[filename] = {}
                self.corrections[filename][alert['index']] = combo.currentText()
                corrections_applied += 1
        
        if corrections_applied > 0:
            QMessageBox.information(self, "Corrections appliquées", 
                                  f"{corrections_applied} correction(s) appliquée(s) pour {os.path.basename(filename)}")
        else:
            QMessageBox.warning(self, "Aucune correction", 
                              "Aucune correction sélectionnée pour ce fichier")
    
    def apply_all_corrections(self):
        """Applique toutes les corrections sélectionnées"""
        total_corrections = 0
        
        for filename, alerts in self.noyau_alerts.items():
            for alert in alerts:
                combo = alert.get('combo')
                if combo and combo.currentText() != "-- Sélectionner un noyau --":
                    if filename not in self.corrections:
                        self.corrections[filename] = {}
                    self.corrections[filename][alert['index']] = combo.currentText()
                    total_corrections += 1
        
        if total_corrections > 0:
            QMessageBox.information(self, "Corrections appliquées", 
                                  f"{total_corrections} correction(s) appliquée(s) au total")
        else:
            QMessageBox.warning(self, "Aucune correction", 
                              "Aucune correction sélectionnée")
    
    def get_corrections(self):
        """Récupère toutes les corrections"""
        return self.corrections


class InteractiveTestDialog(QDialog):
    """Dialogue pour les tests interactifs nécessitant des entrées"""
    def __init__(self, test_file, parent=None):
        super().__init__(parent)
        self.test_file = test_file
        self.inputs = []
        self.setWindowTitle(f"Entrées pour {test_file}")
        self.setModal(True)
        self.resize(500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Titre
        title = QLabel(f"Test interactif: {self.test_file}")
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)
        
        # Description
        desc = QLabel("Ce test nécessite des entrées interactives. Veuillez les fournir ci-dessous:")
        layout.addWidget(desc)
        
        # Zone de saisie des entrées
        self.inputs_text = QTextEdit()
        self.inputs_text.setPlaceholderText("Entrez les réponses aux questions du test (une par ligne):\n\nExemple:\n2.3.0\n2025-01-02\nDescription du test")
        layout.addWidget(self.inputs_text)
        
        # Boutons
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("Lancer le test")
        cancel_btn = QPushButton("Annuler")
        
        ok_btn.clicked.connect(self.accept)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)

    def get_inputs(self):
        """Retourne les entrées saisies"""
        text = self.inputs_text.toPlainText().strip()
        if text:
            return [line.strip() for line in text.split('\n') if line.strip()]
        return []


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
    """Fonction principale pour lancer l'application"""
    import sys
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    try:
        window = MatelasApp()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Erreur lors du lancement de l'application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 