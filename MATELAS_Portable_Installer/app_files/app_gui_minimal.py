#!/usr/bin/env python3
"""Version ultra-minimale de app_gui pour identifier le crash"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer

# Ajouter le répertoire du projet au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test progressif des imports backend
try:
    from backend.advanced_logging import get_advanced_logger, setup_advanced_logging
    print("✅ advanced_logging importé")
    ADVANCED_LOGGING_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ advanced_logging non disponible: {e}")
    ADVANCED_LOGGING_AVAILABLE = False

class MinimalLiterieApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("🔄 Début init MinimalLiterieApp")
        
        # Test logging
        if ADVANCED_LOGGING_AVAILABLE:
            try:
                setup_advanced_logging()
                self.advanced_logger = get_advanced_logger()
                self.advanced_logger.app_logger.info("MinimalApp initialisée")
                print("✅ Logging avancé OK")
            except Exception as e:
                print(f"⚠️ Erreur logging: {e}")
                self.advanced_logger = None
        else:
            self.advanced_logger = None
        
        # Interface ultra-basique
        self.setWindowTitle("Minimal Literie")
        self.resize(600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Application Minimal - Test"))
        
        # Test Timer (problème potentiel)
        print("🔄 Test Timer...")
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(lambda: print("Timer OK"))
        
        print("✅ Init terminée")

def main():
    print("🚀 Démarrage MinimalLiterieApp")
    app = QApplication(sys.argv)
    
    try:
        window = MinimalLiterieApp()
        print("✅ Fenêtre créée")
        
        window.show()
        print("✅ Fenêtre affichée")
        
        # Démarrer le timer après show
        window.status_timer.start(2000)
        print("✅ Timer démarré")
        
        print("🎯 Démarrage boucle événements")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()