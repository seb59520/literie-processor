#!/usr/bin/env python3
"""
Interface graphique PyQt6 pour l'application de traitement de devis matelas
Version corrigée pour PyInstaller
"""

import sys
import os
import json
import tempfile
import shutil
import logging
import logging.handlers
import subprocess
import glob
import threading
import re
from datetime import datetime
from typing import List, Dict, Optional

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QFileDialog, QTextEdit, QSpinBox, 
    QLineEdit, QCheckBox, QComboBox, QGroupBox, QScrollArea,
    QProgressBar, QMessageBox, QTabWidget, QTableWidget, QTableWidgetItem,
    QSplitter, QFrame, QMenuBar, QMenu, QTextBrowser, QGridLayout,
    QDialogButtonBox, QDialog, QHeaderView, QFormLayout,
    QListWidget, QListWidgetItem, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon, QAction
import webbrowser

# Configuration du path pour PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Mode PyInstaller
    base_path = sys._MEIPASS
else:
    # Mode développement
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path de manière compatible PyInstaller
backend_path = os.path.join(base_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Imports absolus pour PyInstaller
try:
    from backend_interface import backend_interface
    from config import config
    from version import get_version, get_full_version, get_version_info, get_changelog
    from backend.asset_utils import get_asset_path
    
    # Import du module de stockage sécurisé
    try:
        from backend.secure_storage import secure_storage
        SECURE_STORAGE_AVAILABLE = True
    except ImportError as e:
        print(f"Module de stockage sécurisé non disponible: {e}")
        SECURE_STORAGE_AVAILABLE = False
        
except ImportError as e:
    print(f"Erreur d'import critique: {e}")
    print("Vérifiez que tous les modules backend sont disponibles")
    sys.exit(1)

# Configuration du système de logs avancé
def setup_logging():
    """Configure le système de logging avancé avec rotation des fichiers"""
    # Créer le dossier logs s'il n'existe pas
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
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

# Initialiser le logging
logger = setup_logging()

# Copier le reste du fichier app_gui.py ici...
# (Le contenu est trop long, on va créer un script qui copie et corrige automatiquement)

def create_fixed_app_gui():
    """Crée une version corrigée de app_gui.py"""
    
    # Lire le fichier original
    with open('app_gui.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remplacer les imports problématiques
    fixed_content = content.replace(
        "# Import des modules backend existants\nsys.path.append('backend')",
        """# Configuration du path pour PyInstaller
if hasattr(sys, '_MEIPASS'):
    # Mode PyInstaller
    base_path = sys._MEIPASS
else:
    # Mode développement
    base_path = os.path.dirname(os.path.abspath(__file__))

# Ajouter le backend au path de manière compatible PyInstaller
backend_path = os.path.join(base_path, 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Imports absolus pour PyInstaller"""
    )
    
    # Écrire le fichier corrigé
    with open('app_gui_fixed.py', 'w', encoding='utf-8') as f:
        f.write(fixed_content)
    
    print("✅ Fichier app_gui_fixed.py créé avec les imports corrigés")

if __name__ == "__main__":
    create_fixed_app_gui() 