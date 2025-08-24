#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier la prévisualisation
"""

import sys
import os

# Ajouter le répertoire au path pour importer les modules
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Tester que tous les imports nécessaires fonctionnent"""
    print("🔍 Test des imports nécessaires")
    print("=" * 50)
    
    try:
        # Test PyQt6
        try:
            from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                        QWidget, QTextEdit, QPushButton, QLabel, QComboBox, 
                                        QLineEdit, QGroupBox, QSplitter, QTabWidget, QTableWidget,
                                        QTableWidgetItem, QMessageBox, QFileDialog, QProgressBar,
                                        QCheckBox, QSpinBox, QDoubleSpinBox, QTextBrowser, QDialog)
            from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
            from PyQt6.QtGui import QFont, QIcon, QPixmap
            print("✅ PyQt6 - Tous les imports réussis")
            return "PyQt6"
        except ImportError as e:
            print(f"❌ PyQt6 - Import échoué: {e}")
        
        # Test PyQt5
        try:
            from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                                        QWidget, QTextEdit, QPushButton, QLabel, QComboBox, 
                                        QLineEdit, QGroupBox, QSplitter, QTabWidget, QTableWidget,
                                        QTableWidgetItem, QMessageBox, QFileDialog, QProgressBar,
                                        QCheckBox, QSpinBox, QDoubleSpinBox, QTextBrowser, QDialog)
            from PyQt5.QtCore import Qt, QThread, pyqtSignal, QTimer
            from PyQt5.QtGui import QFont, QIcon, QPixmap
            print("✅ PyQt5 - Tous les imports réussis")
            return "PyQt5"
        except ImportError as e:
            print(f"❌ PyQt5 - Import échoué: {e}")
        
        print("❌ Aucune version de PyQt disponible")
        return None
        
    except Exception as e:
        print(f"❌ Erreur lors du test des imports: {e}")
        return None

def test_dialog_creation():
    """Tester la création d'une fenêtre de dialogue"""
    print("\n🔧 Test de création de fenêtre de dialogue")
    print("=" * 50)
    
    try:
        # Détecter la version de PyQt
        qt_version = test_imports()
        if not qt_version:
            return False
        
        # Importer selon la version détectée
        if qt_version == "PyQt6":
            from PyQt6.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
            from PyQt6.QtGui import QFont
        else:
            from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel
            from PyQt5.QtGui import QFont
        
        # Créer l'application
        app = QApplication([])
        
        # Créer une fenêtre de dialogue
        dialog = QDialog()
        dialog.setWindowTitle("Test de Prévisualisation")
        dialog.setModal(True)
        dialog.resize(600, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Zone de texte
        text_edit = QTextEdit()
        text_edit.setPlainText("Ceci est un test de prévisualisation.\n\nLe texte extrait du PDF apparaîtra ici.")
        text_edit.setReadOnly(True)
        text_edit.setFont(QFont("Courier", 10))
        layout.addWidget(text_edit)
        
        # Statistiques
        stats_label = QLabel("📊 Statistiques: 67 caractères | 12 mots | 3 lignes")
        stats_label.setStyleSheet("color: #666; font-weight: bold; padding: 5px;")
        layout.addWidget(stats_label)
        
        # Bouton de fermeture
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        print("✅ Fenêtre de dialogue créée avec succès")
        print("✅ Zone de texte configurée")
        print("✅ Statistiques affichées")
        print("✅ Bouton de fermeture ajouté")
        
        # Afficher la fenêtre
        print("\n🖥️ Affichage de la fenêtre de test...")
        dialog.exec()
        
        print("✅ Fenêtre fermée avec succès")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test de création: {e}")
        return False

def test_pdf_extraction_imports():
    """Tester les imports pour l'extraction PDF"""
    print("\n📄 Test des imports d'extraction PDF")
    print("=" * 50)
    
    libraries = {
        "PyMuPDF (fitz)": "import fitz",
        "PyPDF2": "import PyPDF2",
        "reportlab": "from reportlab.pdfgen import canvas"
    }
    
    available_libs = []
    
    for lib_name, import_cmd in libraries.items():
        try:
            exec(import_cmd)
            print(f"✅ {lib_name} - Disponible")
            available_libs.append(lib_name)
        except ImportError:
            print(f"❌ {lib_name} - Non disponible")
    
    return available_libs

def main():
    """Fonction principale"""
    print("🔍 Test de prévisualisation et extraction PDF")
    print("=" * 60)
    
    try:
        # 1. Test des imports PyQt
        qt_version = test_imports()
        if not qt_version:
            print("\n❌ Impossible de tester sans PyQt")
            return False
        
        # 2. Test de création de fenêtre
        dialog_success = test_dialog_creation()
        
        # 3. Test des imports PDF
        pdf_libs = test_pdf_extraction_imports()
        
        # 4. Résumé
        print("\n🎉 Test terminé !")
        print("=" * 60)
        
        if dialog_success:
            print("✅ Prévisualisation fonctionnelle")
        else:
            print("❌ Problème avec la prévisualisation")
        
        if pdf_libs:
            print(f"✅ Bibliothèques PDF disponibles: {', '.join(pdf_libs)}")
        else:
            print("❌ Aucune bibliothèque PDF disponible")
        
        print(f"✅ Version PyQt détectée: {qt_version}")
        
        return dialog_success and len(pdf_libs) > 0
        
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 