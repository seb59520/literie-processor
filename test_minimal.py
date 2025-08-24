#!/usr/bin/env python3
"""Test minimal pour identifier le problème de crash"""

import sys
import os
from PyQt6.QtWidgets import QApplication, QMainWindow

# Ajouter le répertoire du projet au chemin Python
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MinimalApp(QMainWindow):
    def __init__(self):
        super().__init__()
        print("✅ MinimalApp init démarré")
        self.setWindowTitle("Test Minimal")
        self.resize(800, 600)
        print("✅ MinimalApp init terminé")

def main():
    print("🚀 Démarrage test minimal")
    app = QApplication(sys.argv)
    
    print("🔧 Création de la fenêtre")
    window = MinimalApp()
    
    print("🎯 Affichage de la fenêtre")
    window.show()
    
    print("✅ Application prête, démarrage boucle événements")
    sys.exit(app.exec())

if __name__ == "__main__":
    main()