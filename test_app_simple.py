#!/usr/bin/env python3
"""Version simplifiée de l'app pour isoler le crash"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import QTimer

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("🔄 Début init SimpleApp")
        
        # Test des imports backend
        try:
            from backend.advanced_logging import get_advanced_logger
            print("✅ Backend logging importé")
            self.logger = get_advanced_logger()
            print("✅ Logger créé")
        except Exception as e:
            print(f"⚠️ Problème logger: {e}")
            self.logger = None
        
        # Interface minimale
        self.setWindowTitle("Test Simple App")
        self.resize(800, 600)
        
        # Widget central basique
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.addWidget(QLabel("Application Simple"))
        
        # Test Timer (problème potentiel identifié)
        print("🔄 Test Timer...")
        try:
            self.test_timer = QTimer()
            self.test_timer.timeout.connect(lambda: print("Timer tick"))
            print("✅ Timer créé")
            # NE PAS démarrer le timer pour l'instant
        except Exception as e:
            print(f"❌ Erreur Timer: {e}")
        
        print("✅ Init SimpleApp terminé")

def main():
    print("🚀 Démarrage SimpleApp")
    app = QApplication(sys.argv)
    
    try:
        window = SimpleApp()
        print("✅ SimpleApp créée")
        
        window.show()
        print("✅ Fenêtre affichée")
        
        # Test démarrage timer après show
        if hasattr(window, 'test_timer'):
            try:
                window.test_timer.start(2000)  # 2 secondes
                print("✅ Timer démarré")
            except Exception as e:
                print(f"❌ Erreur démarrage timer: {e}")
        
        print("🎯 Démarrage boucle événements")
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Erreur création app: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()